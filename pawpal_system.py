"""
PawPal+ core domain classes (skeleton).

Four classes only:
  - Task (+ subclasses): what needs to get done. Names/attributes/empty
    method stubs only -- no logic.
  - Pet: a single pet and its own task list.
  - Owner: a pet owner and the pets they're responsible for.
  - Scheduler: the only class with real logic. Retrieves, organizes, and
    manages Tasks across every Pet an Owner has.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import date, time


# ---------------------------------------------------------------------------
# Task hierarchy
# ---------------------------------------------------------------------------

# Summary: Abstract base for every kind of pet-care activity that can be
# assigned to a Pet. Only stores what every activity needs.
#   - date / time: when the task is scheduled to happen. Kept as separate
#     stdlib date/time objects (not strings) so Scheduler can sort and
#     compare them directly -- see the comment above Scheduler._sort_key.
#   - duration_minutes: length of the task in minutes. Defaults to 0 for
#     tasks that don't really occupy a span of time (Feeding, Medication).
#   - is_complete: whether this task has been done yet; every task starts
#     incomplete.
#   - get_summary() / mark_complete(): stubs each subclass/caller fills in
#     later (e.g. for the Streamlit UI). Scheduler.complete_task() is the
#     real, working way to flip is_complete -- see the Scheduler section.
#   - get_x()/set_x() below are plain accessors for date/time/
#     duration_minutes/is_complete; every subclass inherits them for free.
class Task(ABC):
    def __init__(self, task_date: date, task_time: time, duration_minutes: int = 0):
        """Initialize a task with its scheduled date, time, and duration."""
        self.date = task_date
        self.time = task_time
        self.duration_minutes = duration_minutes
        self.is_complete = False

    def mark_complete(self) -> None:
        """Mark this task as complete."""
        self.is_complete = True

    def get_date(self) -> date:
        """Return the task's scheduled date."""
        return self.date

    def set_date(self, new_date: date) -> None:
        """Set the task's scheduled date."""
        self.date = new_date

    def get_time(self) -> time:
        """Return the task's scheduled time."""
        return self.time

    def set_time(self, new_time: time) -> None:
        """Set the task's scheduled time."""
        self.time = new_time

    def get_duration_minutes(self) -> int:
        """Return the task's duration in minutes."""
        return self.duration_minutes

    def set_duration_minutes(self, new_duration_minutes: int) -> None:
        """Set the task's duration in minutes."""
        self.duration_minutes = new_duration_minutes

    def get_is_complete(self) -> bool:
        """Return whether the task has been completed."""
        return self.is_complete

    def set_is_complete(self, value: bool) -> None:
        """Set the task's completion status."""
        self.is_complete = value


# Summary: A single walk with the pet.
#   - distance_miles: how far the walk covers.
#   - duration_minutes / date / time / is_complete come from Task.
#   - get_distance_miles()/set_distance_miles(): accessors for the one
#     attribute this subclass adds.
class PetWalk(Task):
    def __init__(self, task_date: date, task_time: time, duration_minutes: int, distance_miles: float):
        """Initialize a walk with its distance in miles."""
        super().__init__(task_date, task_time, duration_minutes)



# Summary: A single feeding event.
#   - food_type: what the pet is being fed.
#   - Treated as instantaneous (duration_minutes stays 0 from Task).
#   - get_food_type()/set_food_type(): accessors for the one attribute
#     this subclass adds.
class Feeding(Task):
    def __init__(self, task_date: date, task_time: time, food_type: str):
        """Initialize a feeding with the type of food given."""
        super().__init__(task_date, task_time)
        self.food_type = food_type

    def get_food_type(self) -> str:
        """Return the food type for this feeding."""
        return self.food_type

    def set_food_type(self, new_food_type: str) -> None:
        """Set the food type for this feeding."""
        self.food_type = new_food_type


# Summary: A medication dose/reminder.
#   - drug_name: name of the medication.
#   - times_per_day: how many doses are expected per day.
#   - dose_counter: how many doses have been logged so far; starts at 0.
#   - Treated as instantaneous (duration_minutes stays 0 from Task).
#   - log_dose_taken(): increments dose_counter by one, capped at
#     times_per_day.
#   - get_x()/set_x() below are plain accessors for the three attributes
#     this subclass adds; set_dose_counter() also doubles as a manual
#     reset hook (e.g. set back to 0 at the start of a new day).
class Medication(Task):
    def __init__(self, task_date: date, task_time: time, drug_name: str, times_per_day: int):
        """Initialize a medication with its drug name and doses per day."""
        super().__init__(task_date, task_time)
        self.drug_name = drug_name
        self.times_per_day = times_per_day
        self.dose_counter = 0

    def log_dose_taken(self) -> None:
        """Increment the dose counter by one, capped at times_per_day."""
        if self.dose_counter < self.times_per_day:
            self.dose_counter +=1

    def get_drug_name(self) -> str:
        """Return the medication's drug name."""
        return self.drug_name

    def set_drug_name(self, new_drug_name: str) -> None:
        """Set the medication's drug name."""
        self.drug_name = new_drug_name

    def get_times_per_day(self) -> int:
        """Return how many doses are expected per day."""
        return self.times_per_day

    def set_times_per_day(self, new_times_per_day: int) -> None:
        """Set how many doses are expected per day."""
        self.times_per_day = new_times_per_day

    def get_dose_counter(self) -> int:
        """Return how many doses have been logged so far."""
        return self.dose_counter

    def set_dose_counter(self, new_dose_counter: int) -> None:
        """Set the dose counter."""
        self.dose_counter = new_dose_counter


# Summary: A veterinary appointment.
#   - visit_name / description: what the appointment is for.
#   - required_documentation: paperwork the owner needs to bring.
#   - duration_minutes / date / time / is_complete come from Task.
#   - get_x()/set_x() below are plain accessors for the three attributes
#     this subclass adds.
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
        """Initialize a vet visit with its name, description, and required documentation."""
        super().__init__(task_date, task_time, duration_minutes)
        self.visit_name = visit_name
        self.description = description
        self.required_documentation = required_documentation

    def get_visit_name(self) -> str:
        """Return the visit's name."""
        return self.visit_name

    def set_visit_name(self, new_visit_name: str) -> None:
        """Set the visit's name."""
        self.visit_name = new_visit_name

    def get_description(self) -> str:
        """Return the visit's description."""
        return self.description

    def set_description(self, new_description: str) -> None:
        """Set the visit's description."""
        self.description = new_description

    def get_required_documentation(self) -> str:
        """Return the documentation required for this visit."""
        return self.required_documentation

    def set_required_documentation(self, new_required_documentation: str) -> None:
        """Set the documentation required for this visit."""
        self.required_documentation = new_required_documentation


# Summary: Catch-all for any pet-care activity that doesn't fit the other
# categories (e.g. grooming, enrichment/play).
#   - task_name / description: what the activity is.
#   - duration_minutes / date / time / is_complete come from Task.
#   - get_x()/set_x() below are plain accessors for the two attributes
#     this subclass adds.
class Other(Task):
    def __init__(self, task_name: str, description: str, task_date: date, task_time: time, duration_minutes: int):
        """Initialize a catch-all task with its name and description."""
        super().__init__(task_date, task_time, duration_minutes)
        self.task_name = task_name
        self.description = description

    def get_task_name(self) -> str:
        """Return the task's name."""
        return self.task_name

    def set_task_name(self, new_task_name: str) -> None:
        """Set the task's name."""
        self.task_name = new_task_name

    def get_description(self) -> str:
        """Return the task's description."""
        return self.description

    def set_description(self, new_description: str) -> None:
        """Set the task's description."""
        self.description = new_description


# ---------------------------------------------------------------------------
# Pet
# ---------------------------------------------------------------------------

# Summary: A single pet and its own list of tasks. Pet is a plain data
# holder -- it does not sort, validate, or schedule anything itself; that
# is Scheduler's job.
#   - name: the pet's name.
#   - age: kept as str per spec (e.g. "3 years", "6 months") rather than
#     int, so non-numeric descriptions are allowed. Flag me if you actually
#     want a numeric age for comparisons/sorting later.
#   - favorite_food: set of foods the pet likes.
#   - food_restriction: set of foods the pet must avoid.
#   - medicine_restriction: set of medications the pet must avoid.
#   - task: every Task assigned to this pet, regardless of date.
#   - get_name()/set_name(), get_age()/set_age(): plain scalar accessors.
#   - get_x()/set_x()/add_x()/remove_x() for favorite_food,
#     food_restriction, medicine_restriction: get/set read or replace the
#     whole set; add/remove mutate a single item.
#   - get_task()/set_task()/add_task(): raw list access/replace/append.
#     This is the low-level version -- prefer Scheduler.add_task() when an
#     Owner is involved, since that one also validates and keeps the list
#     sorted.
#   - remove_task(): matches by (date, time) rather than object identity,
#     so a rebuilt/copied Task with the same schedule still matches.
class Pet:
    def __init__(
        self,
        name: str,
        age: str,
        favorite_food: set[str] = None,
        food_restriction: set[str] = None,
        medicine_restriction: set[str] = None,
    ):
        """Initialize a pet with its name, age, and preferences/restrictions."""
        self.name = name
        self.age = age
        self.favorite_food = favorite_food if favorite_food is not None else set()
        self.food_restriction = food_restriction if food_restriction is not None else set()
        self.medicine_restriction = medicine_restriction if medicine_restriction is not None else set()
        self.task: list[Task] = []

    def get_name(self) -> str:
        """Return the pet's name."""
        return self.name

    def set_name(self, new_name: str) -> None:
        """Set the pet's name."""
        self.name = new_name

    def get_age(self) -> str:
        """Return the pet's age."""
        return self.age

    def set_age(self, new_age: str) -> None:
        """Set the pet's age."""
        self.age = new_age

    def get_favorite_food(self) -> set[str]:
        """Return the pet's set of favorite foods."""
        return self.favorite_food

    def set_favorite_food(self, foods: set[str]) -> None:
        """Replace the pet's set of favorite foods."""
        self.favorite_food = foods if foods is not None else set()

    def add_favorite_food(self, food: str) -> None:
        """Add a single food to the pet's favorites."""
        self.favorite_food.add(food)

    def remove_favorite_food(self, food: str) -> bool:
        """Remove a single food from the pet's favorites, if present."""
        if food in self.favorite_food:
            self.favorite_food.discard(food)
            return True
        return False

    def get_food_restriction(self) -> set[str]:
        """Return the pet's set of food restrictions."""
        return self.food_restriction

    def set_food_restriction(self, restrictions: set[str]) -> None:
        """Replace the pet's set of food restrictions."""
        self.food_restriction = restrictions if restrictions is not None else set()

    def add_food_restriction(self, restriction: str) -> None:
        """Add a single restriction to the pet's food restrictions."""
        self.food_restriction.add(restriction)

    def remove_food_restriction(self, restriction: str) -> bool:
        """Remove a single restriction from the pet's food restrictions, if present."""
        if restriction in self.food_restriction:
            self.food_restriction.discard(restriction)
            return True
        return False

    def get_medicine_restriction(self) -> set[str]:
        """Return the pet's set of medicine restrictions."""
        return self.medicine_restriction

    def set_medicine_restriction(self, restrictions: set[str]) -> None:
        """Replace the pet's set of medicine restrictions."""
        self.medicine_restriction = restrictions if restrictions is not None else set()

    def add_medicine_restriction(self, restriction: str) -> None:
        """Add a single restriction to the pet's medicine restrictions."""
        self.medicine_restriction.add(restriction)

    def remove_medicine_restriction(self, restriction: str) -> bool:
        """Remove a single restriction from the pet's medicine restrictions, if present."""
        if restriction in self.medicine_restriction:
            self.medicine_restriction.discard(restriction)
            return True
        return False

    def get_task(self) -> list[Task]:
        """Return the pet's list of tasks."""
        return self.task

    def set_task(self, tasks: list[Task]) -> None:
        """Replace the pet's list of tasks."""
        self.task = tasks if tasks is not None else []

    def add_task(self, single_task: Task) -> None:
        """Append a task to the pet's task list."""
        self.task.append(single_task)

    def remove_task(self, single_task: Task) -> bool:
        """Remove a task matching the given task's date and time, if present."""
        for index, item in enumerate(self.task):
            if item.time == single_task.time and item.date == single_task.date:
                del self.task[index]
                return True
        return False



# ---------------------------------------------------------------------------
# Owner
# ---------------------------------------------------------------------------

# Summary: A pet owner and the pets they're responsible for. Like Pet, this
# is a plain data holder; Scheduler is what actually organizes/manages
# tasks across the pets listed here.
#   - pets: every Pet this owner is responsible for.
#   - get_all_tasks(): trivial raw access -- flattens each pet's task list
#     into one list with no sorting/filtering. Scheduler builds on top of
#     this to add ordering and querying.
#   - get_pets()/set_pets(): raw list access/replace.
#   - add_a_pet()/remove_pet(): append/remove a single pet. remove_pet()
#     matches by (name, age) rather than object identity, same reasoning
#     as Pet.remove_task().
class Owner:
    def __init__(self, name : str, pets: list[Pet] = None):
        """Initialize an owner with a name and the pets they're responsible for."""
        self.name__ = name
        self.pets = pets if pets is not None else []

    def get_all_tasks(self) -> list[Task]:
        """Return every task across all of this owner's pets, unsorted."""
        return [task for pet in self.pets for task in pet.task]

    def set_name(self, new_name) -> None:
        """Set the owner's name."""
        self.name = new_name

    def get_pets(self) -> list[Pet]:
        """Return the owner's list of pets."""
        return self.pets

    def remove_pet(self, pet: Pet) -> bool:
        """Remove a pet matching the given pet's name and age, if present."""
        for index, item in enumerate(self.pets):
            if item.name == pet.name and item.age == pet.age:
                del self.pets[index]
                return True
        return False

    def add_a_pet(self, pet: Pet) -> None:
        """Append a pet to the owner's list of pets."""
        self.pets.append(pet)

    def get_todays_tasks(self, date : date):
        """Print each pet's tasks that fall on the given date."""
        status = ""
        for pet in self.pets:
            print(f"Today's Schedule for {pet.get_name()}:")
            for tassk in pet.get_task():
                if tassk.get_is_complete():
                    status = "done"
                else:
                    status = "pending"
                if tassk.date == date:
                    print(f"- {type(tassk).__name__} on {tassk.get_date()} at {tassk.get_time()} ({status})")
                else:
                    continue
# ---------------------------------------------------------------------------
# Scheduler
# ---------------------------------------------------------------------------

# Summary: The only class with real logic. Retrieves, organizes, and
# manages Tasks that live on an Owner's Pets. Scheduler never stores tasks
# itself -- every Task still lives on its Pet's `task` list; Scheduler just
# knows how to find, order, and mutate those lists correctly.
#   - _sort_key(): orders tasks chronologically. See the datetime note
#     below for why this works.
#   - get_tasks_for_pet(): retrieve -- one pet's tasks, earliest first.
#   - get_all_tasks(): retrieve + organize -- every pet's tasks combined
#     into one earliest-first list, each paired with the pet it belongs to
#     so the caller still knows whose task is whose.
#   - get_tasks_by_date(): retrieve + filter -- everything happening on one
#     specific day, across every pet (useful for building the "daily plan"
#     the README describes).
#   - add_task(): manage -- confirms the pet actually belongs to this
#     owner, appends the task, then re-sorts that pet's list so it stays in
#     chronological order.
#   - remove_task(): manage -- confirms the pet belongs to this owner, then
#     removes the task if present.
#   - complete_task(): manage -- confirms the pet belongs to this owner and
#     the task is actually assigned to that pet, then marks it complete.
#
# datetime note: Task.date is a datetime.date and Task.time is a
# datetime.time. `_sort_key` returns them as a (date, time) tuple instead
# of combining them into a single datetime:
#   - Python compares tuples element-by-element, so sorting by
#     (date, time) naturally orders by date first, then by time within
#     the same date -- exactly "earliest to latest".
#   - date and time objects already support <, <=, == out of the box, so
#     no manual string parsing is needed to compare two tasks.
#   - We don't need datetime.combine()/datetime.now() here because
#     Scheduler only ever orders and filters tasks -- it never does
#     date+time arithmetic (like adding a duration to get an end time),
#     which is the situation that would actually require a combined
#     datetime object.

class Scheduler:

    @staticmethod
    def _sort_key(task: Task) -> tuple[date, time]:
        """Return the (date, time) tuple used to sort a task chronologically."""
        return (task.date, task.time)

    def get_tasks_for_pet(self, pet: Pet) -> list[Task]:
        """Return one pet's tasks, sorted earliest first."""
        return sorted(pet.task, key=self._sort_key)

    def get_all_tasks(self, owner: Owner) -> list[tuple[Pet, Task]]:
        """Return every pet-task pair across the owner's pets, sorted earliest first."""
        combined = [(pet, task) for pet in owner.pets for task in pet.task]
        return sorted(combined, key=lambda pair: self._sort_key(pair[1]))

    def get_tasks_by_date(self, owner: Owner, target_date: date) -> list[tuple[Pet, Task]]:
        """Return every pet-task pair scheduled on the given date."""
        return [pair for pair in self.get_all_tasks(owner) if pair[1].date == target_date]

    def add_task(self, owner: Owner, pet: Pet, task: Task) -> None:
        """Add a task to a pet's list and keep it sorted chronologically."""
        if pet not in owner.pets:
            raise ValueError(f"{pet.name} is not one of this owner's pets.")
        pet.task.append(task)
        pet.task.sort(key=self._sort_key)

    def remove_task(self, owner: Owner, pet: Pet, task: Task) -> bool:
        """Remove a task from a pet's list, if present."""
        if pet not in owner.pets:
            raise ValueError(f"{pet.name} is not one of this owner's pets.")
        if task in pet.task:
            pet.task.remove(task)
            return True
        return False

    def complete_task(self, owner: Owner, pet: Pet, task: Task) -> bool:
        """Mark a task as complete for one of the owner's pets."""
        if pet not in owner.pets:
            raise ValueError(f"{pet.name} is not one of this owner's pets.")
        if task in pet.task:
            task.mark_complete()
            # pet.remove_task(task)
            return True
        return False
