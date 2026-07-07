"""
PawPal+ core domain classes (skeleton).

Mirrors diagrams/uml.mmd. Every method is an empty stub EXCEPT
Calendar.add_task / Calendar.remove_task (and the small helpers they rely
on), which contain the real scheduling logic per the assignment.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import date, time, datetime, timedelta


# ---------------------------------------------------------------------------
# Task hierarchy
# ---------------------------------------------------------------------------

# Summary: Abstract base for every kind of pet-care activity that can be
# placed on the Calendar. Only stores what every activity needs.
#   - date / time: when the task is scheduled to happen.
#   - duration_minutes: length of the task in minutes. Defaults to 0 for
#     tasks that don't really occupy a span of time (Feeding, Medication),
#     so Calendar can treat every Task the same way when checking schedules.
#   - get_summary(): stub each subclass overrides to describe itself
#     (e.g. for the Streamlit UI).
class Task(ABC):
    def __init__(self, task_date: date, task_time: time, duration_minutes: int = 0):
        self.date = task_date
        self.time = task_time
        self.duration_minutes = duration_minutes


# Summary: A single walk with the pet.
#   - distance_miles: how far the walk covers.
#   - duration_minutes / date / time come from Task.
class PetWalk(Task):
    def __init__(self, task_date: date, task_time: time, duration_minutes: int, distance_miles: float):
        super().__init__(task_date, task_time, duration_minutes)
        self.distance_miles = distance_miles


# Summary: A single feeding event.
#   - food_type: what the pet is being fed.
#   - Treated as instantaneous (duration_minutes stays 0 from Task).
class Feeding(Task):
    def __init__(self, task_date: date, task_time: time, food_type: str):
        super().__init__(task_date, task_time)
        self.food_type = food_type


# Summary: A medication dose/reminder.
#   - drug_name: name of the medication.
#   - times_per_day: how many doses are expected per day.
#   - dose_counter: how many doses have been logged so far; starts at 0.
#   - Treated as instantaneous (duration_minutes stays 0 from Task).
class Medication(Task):
    def __init__(self, task_date: date, task_time: time, drug_name: str, times_per_day: int):
        super().__init__(task_date, task_time)
        self.drug_name = drug_name
        self.times_per_day = times_per_day
        self.dose_counter = 0

    def log_dose_taken(self) -> None:
        if self.dose_counter < self.times_per_day:
            self.dose_counter += 1
        else:
            print("Your pet got all its daily dosis")


# Summary: A veterinary appointment.
#   - visit_name / description: what the appointment is for.
#   - required_documentation: paperwork the owner needs to bring.
#   - duration_minutes / date / time come from Task.
class VetVisit(Task):
    def __init__(
        self,
        visit_name: str,
        description: str,
        task_date: date,
        task_time: time,
        required_documentation: str,
        duration_minutes: int,
    ):
        super().__init__(task_date, task_time, duration_minutes)
        self.visit_name = visit_name
        self.description = description
        self.required_documentation = required_documentation


# Summary: Catch-all for any pet-care activity that doesn't fit the other
# categories (e.g. grooming, enrichment/play).
#   - task_name / description: what the activity is.
#   - duration_minutes / date / time come from Task.
class Other(Task):
    def __init__(self, task_name: str, description: str, task_date: date, task_time: time, duration_minutes: int):
        super().__init__(task_date, task_time, duration_minutes)
        self.task_name = task_name
        self.description = description


# ---------------------------------------------------------------------------
# Pet
# ---------------------------------------------------------------------------

# Summary: A pet owned by a User.
#   - name / age / pet_type: basic identity info.
#   - favorite_food / food_restrictions: feeding-related notes.
#   - needs_groom: whether the pet is currently due for grooming.
class Pet:
    def __init__(
        self,
        name: str,
        age: int,
        favorite_food: str,
        pet_type: str,
        food_restrictions: str,
        needs_groom: bool = False,
    ):
        self.name = name
        self.age = age
        self.favorite_food = favorite_food
        self.pet_type = pet_type
        self.food_restrictions = food_restrictions
        self.needs_groom = needs_groom


# ---------------------------------------------------------------------------
# AvailabilitySchedule
# ---------------------------------------------------------------------------

# Summary: One recurring window of time when the owner is free to do
# pet-care tasks (e.g. "before work", "evenings"). It is not tied to a
# specific date -- Calendar checks new tasks against it by time-of-day only.
#   - time: start of the window, stored as an "HH-MM-SS" string per spec.
#   - name / description: label for the window (e.g. "Before work").
#   - duration_minutes: length of the window, in minutes.
#   - parsed_time() / window_end(): small real helpers (not stubs) because
#     Calendar.add_task needs them to compare time windows.
class AvailabilitySchedule:
    def __init__(self, time_str: str, name: str, description: str, duration_minutes: int):
        self.time = time_str
        self.name = name
        self.description = description
        self.duration_minutes = duration_minutes

    def parsed_time(self) -> time:
        hour, minute, second = (int(part) for part in self.time.split("-"))
        return time(hour=hour, minute=minute, second=second)

    def window_end(self) -> time:
        start = datetime.combine(date.today(), self.parsed_time())
        return (start + timedelta(minutes=self.duration_minutes)).time()   ##########


# ---------------------------------------------------------------------------
# User
# ---------------------------------------------------------------------------

# Summary: The pet owner using PawPal+.
#   - name: owner's display name.
#   - availability_schedules: recurring free-time windows (see
#     AvailabilitySchedule) that Calendar uses to validate new tasks.
#   - pets: every pet this owner is responsible for.
class User:
    def __init__(self, name: str):
        self.name = name
        self.availability_schedules = set()
        self.pets = []

    def add_pet(self, pet: Pet) -> None:
        self.pets.append(pet)

    def add_availability(self, slot: AvailabilitySchedule) -> None:
        if slot not in self.availability_schedules:
            self.availability_schedules[slot.time] = slot
    
    def remove_availability(self, slot: AvailabilitySchedule) -> None:
        if slot in self.availability_schedules:
            self.availability_schedules.remove(slot)


# ---------------------------------------------------------------------------
# Day bucket (linked list) used inside Calendar
# ---------------------------------------------------------------------------

# Summary: One node in a day's task bucket.
#   - task: the Task stored at this node.
#   - next: the next node (later start time), or None if this is the last.
class _TaskNode:
    def __init__(self, task: Task):
        self.task = task
        self.next = None


# Summary: Singly linked list acting as the "bucket" for a single calendar
# day. Kept sorted by start time so a day's tasks are always read from
# lowest time to highest time, as required.
#   - head: earliest task in the day, or None if the day is empty.
#   - insert_sorted() / remove(): real logic -- this is the data structure
#     Calendar.add_task / remove_task rely on.
class _DayBucket:
    def __init__(self):
        self.head = None

    def insert_sorted(self, task: Task) -> None:
        new_node = _TaskNode(task)
        if self.head is None or task.time < self.head.task.time:
            new_node.next = self.head
            self.head = new_node
            return
        current = self.head
        while current.next is not None and current.next.task.time <= task.time:
            current = current.next
        new_node.next = current.next
        current.next = new_node

    def remove(self, task: Task) -> bool:
        previous = None
        current = self.head
        while current is not None:
            if current.task is task:
                if previous is None:
                    self.head = current.next
                else:
                    previous.next = current.next
                return True
            previous = current
            current = current.next
        return False

    def __iter__(self):
        current = self.head
        while current is not None:
            yield current.task
            current = current.next


# ---------------------------------------------------------------------------
# Calendar
# ---------------------------------------------------------------------------

# Summary: Owns every Task for one User and enforces scheduling rules when
# tasks are added or removed. This is the only class with real business
# logic in this file, per the assignment.
#   - user: the owner this calendar belongs to (Calendar -> User in the
#     UML); needed here to check the user's AvailabilitySchedule.
#   - schedule: nested dict keyed [month][week][day-of-month] -> _DayBucket,
#     mirroring the month/week/day 3D layout from the UML. The day level is
#     a linked-list bucket instead of a fixed slot, since any number of
#     tasks can land on the same day.
#   - current_datetime: what "now" is for this calendar; used to reject
#     tasks scheduled in the past.
#   - get_tasks(): stub, left for the UI layer to implement.
#   - add_task() / remove_task(): real logic --
#       1. Rejects any task whose date/time is in the past.
#       2. Rejects any task whose [start, start + duration] window isn't
#          fully covered by at least one of the user's
#          AvailabilitySchedule windows (time-of-day comparison, since
#          AvailabilitySchedule isn't tied to a specific date).
#       3. Otherwise inserts/removes the task in the correct day bucket,
#          keeping that bucket sorted lowest time to highest time.
class Calendar:
    def __init__(self, user: User, current_datetime: datetime = None):
        self.user = user
        self.schedule = {}
        self.current_datetime = current_datetime or datetime.now()

    def get_tasks(self, month: int, week: int, day: int):
        pass

    def add_task(self, task: Task) -> None:
        task_start = datetime.combine(task.date, task.time)
        if task_start < self.current_datetime:
            raise ValueError("Cannot schedule a task in the past.")

        task_end = (datetime.combine(date.today(), task.time) + timedelta(minutes=task.duration_minutes)).time()

        fits_availability = any(
            slot.parsed_time() <= task.time and task_end <= slot.window_end()
            for slot in self.user.availability_schedules
        )
        if not fits_availability:
            raise ValueError("Requested time conflicts with the user's availability schedule.")

        month_key, week_key, day_key = self._locate(task.date)
        week_map = self.schedule.setdefault(month_key, {})
        day_map = week_map.setdefault(week_key, {})
        bucket = day_map.setdefault(day_key, _DayBucket())
        bucket.insert_sorted(task)

    def remove_task(self, task: Task) -> bool:
        month_key, week_key, day_key = self._locate(task.date)
        bucket = self.schedule.get(month_key, {}).get(week_key, {}).get(day_key)
        if bucket is None:
            return False
        return bucket.remove(task)

    @staticmethod
    def _locate(task_date: date):
        _, iso_week, _ = task_date.isocalendar()
        return task_date.month, iso_week, task_date.day
