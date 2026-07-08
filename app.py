from datetime import date, timedelta

import streamlit as st

from pawpal_system import *

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )



st.divider()

st.subheader("Quick Demo Inputs (UI only)")
owner_name = st.text_input("Owner name", value="Jordan")

if "owner" not in st.session_state:
    st.session_state.owner = Owner(owner_name, [])

if "tasks_by_pet" not in st.session_state:
    st.session_state.tasks_by_pet = {}

if "schedule_generated" not in st.session_state:
    st.session_state.schedule_generated = False

owner = st.session_state.owner
scheduler = Scheduler()

pet_name_col, add_pet_col = st.columns([3, 1])
with pet_name_col:
    pet_name = st.text_input("Pet name", value="Mochi")
with add_pet_col:
    if st.button("Add pet"):
        existing_names = [p.get_name() for p in owner.get_pets()]
        if not pet_name:
            st.warning("Give the pet a name first.")
        elif pet_name in existing_names:
            st.warning(f"{pet_name} is already one of {owner_name}'s pets.")
        else:
            owner.add_a_pet(Pet(pet_name, "", set(), set(), set()))
            st.success(f"🐾 Added {pet_name} to {owner_name}'s pets!")

species = st.selectbox("Species", ["dog", "cat", "other"])

pet_names = [p.get_name() for p in owner.get_pets()]

st.markdown("### Tasks")
st.caption("Add a few tasks. In your final version, these should feed into your scheduler.")

if not pet_names:
    st.info("Add a pet above before assigning tasks.")
    active_pet_name = None
else:
    active_pet_name = st.selectbox("Adding tasks for", pet_names)

col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)
with col4:
    timme = st.time_input("Time")
with col5:
    recurrence = st.selectbox("Recurrence", ["None", "Daily", "Weekly"])

if st.button("Add task"):
    if active_pet_name is None:
        st.warning("Add a pet before adding tasks.")
    elif not task_title.strip():
        st.error("Task title cannot be empty.")
    else:
        existing_tasks = [
            (t["Time"], t["duration_minutes"])
            for t in st.session_state.tasks_by_pet.get(active_pet_name, [])
        ]
        if scheduler.has_time_conflict(existing_tasks, timme, int(duration)):
            st.warning(f"{active_pet_name} already has a task that overlaps {timme.strftime('%H:%M')}.")
        else:
            st.session_state.tasks_by_pet.setdefault(active_pet_name, []).append(
                {
                    "title": task_title,
                    "duration_minutes": int(duration),
                    "priority": priority,
                    "Time": timme,
                    "recurrence": recurrence,
                    "date": date.today(),
                }
            )
            st.success(f"✅ Added \"{task_title}\" for {active_pet_name} at {timme.strftime('%H:%M')}.")

current_tasks = st.session_state.tasks_by_pet.get(active_pet_name, []) if active_pet_name else []
if current_tasks:
    st.write(f"Current tasks for {active_pet_name}:")
    st.table(sorted(current_tasks, key=lambda t: t["Time"]))
else:
    st.info("No tasks yet for this pet. Add one above.")

st.divider()

st.subheader("Task Completion")
st.caption("Mark tasks as complete or not yet done for any pet.")

if pet_names:
    completion_pet_name = st.selectbox("Update tasks for", pet_names, key="completion_pet_choice")
    completion_tasks = st.session_state.tasks_by_pet.get(completion_pet_name, [])
    if completion_tasks:
        newly_spawned = []
        for index, task_data in enumerate(completion_tasks):
            was_complete = task_data.get("complete", False)
            now_complete = st.checkbox(
                f"{task_data['title']} — {task_data['Time'].strftime('%H:%M')}",
                value=was_complete,
                key=f"complete_{completion_pet_name}_{index}",
            )
            task_data["complete"] = now_complete
            recurrence = task_data.get("recurrence", "None")
            if now_complete and not was_complete:
                if recurrence != "None":
                    next_task = dict(task_data)
                    next_task["date"] = task_data.get("date", date.today()) + timedelta(
                        days=1 if recurrence == "Daily" else 7
                    )
                    next_task["complete"] = False
                    newly_spawned.append(next_task)
                    st.success(
                        f"{recurrence} task complete — scheduled \"{task_data['title']}\" for "
                        f"{completion_pet_name} again on {next_task['date']}."
                    )
                else:
                    st.success(f"✅ Marked \"{task_data['title']}\" complete for {completion_pet_name}!")
        if newly_spawned:
            st.session_state.tasks_by_pet[completion_pet_name].extend(newly_spawned)
    else:
        st.info(f"No tasks yet for {completion_pet_name}.")
else:
    st.info("Add a pet and some tasks first.")

st.divider()

st.subheader("Build Schedule")
st.caption("This button should call your scheduling logic once you implement it.")

button_col, sort_col = st.columns(2)
with button_col:
    generate_clicked = st.button("Generate schedule")

if generate_clicked:
    if not pet_names:
        st.warning("Add a pet and some tasks before generating a schedule.")
    else:
        st.session_state.schedule_generated = True

with sort_col:
    if st.session_state.schedule_generated:
        sort_choice = st.selectbox("Sort by", ["Time", "Priority", "Completion"])
    else:
        sort_choice = "Time"

if generate_clicked and pet_names:
    today = date.today()
    task_count = 0
    for pet in owner.get_pets():
        pet.set_task([])
        for task_data in st.session_state.tasks_by_pet.get(pet.get_name(), []):
            new_task = Other(
                task_name=task_data["title"],
                description="",
                task_date=today,
                task_time=task_data["Time"],
                duration_minutes=task_data["duration_minutes"],
                priority=task_data["priority"],
            )
            if task_data.get("complete", False):
                new_task.mark_complete()
            scheduler.add_task(owner, pet, new_task)
            task_count += 1
    st.success(f"📅 Schedule generated with {task_count} task(s) across {len(pet_names)} pet(s)!")

if st.session_state.schedule_generated and pet_names:
    schedule_pet_name = st.selectbox("View schedule for", ["All"] + pet_names, key="schedule_pet_choice")

    task_to_pet = {}
    if schedule_pet_name == "All":
        for pet_obj, task in scheduler.get_all_tasks(owner):
            task_to_pet[task] = pet_obj.get_name()
        schedule = list(task_to_pet.keys())
    else:
        pet = next(p for p in owner.get_pets() if p.get_name() == schedule_pet_name)
        schedule = scheduler.get_tasks_for_pet(pet)
        for task in schedule:
            task_to_pet[task] = pet.get_name()

    if sort_choice == "Priority":
        schedule = scheduler.sort_tasks_by_priority(schedule)
    elif sort_choice == "Completion":
        schedule = scheduler.sort_tasks_by_completion(schedule)
    elif sort_choice == "Time":
        schedule = scheduler.sort_tasks_by_time(schedule)

    if schedule:
        st.write(f"Schedule for {schedule_pet_name}:")
        st.table(
            [
                {
                    "Pet": task_to_pet[t],
                    "Task": t.get_task_name(),
                    "Time": t.get_time().strftime("%H:%M"),
                    "Duration (min)": t.get_duration_minutes(),
                    "Priority": t.priority,
                    "Complete": t.get_is_complete(),
                }
                for t in schedule
                if isinstance(t, Other)
            ]
        )
    else:
        st.info(f"No tasks to schedule yet for {schedule_pet_name}. Add one above.")

st.divider()

st.subheader("Recurring Tasks")
st.caption("Daily and weekly tasks across all pets. Completing one above automatically schedules the next occurrence.")

recurring_rows = []
for pet_obj in owner.get_pets():
    for task_data in st.session_state.tasks_by_pet.get(pet_obj.get_name(), []):
        if task_data.get("recurrence", "None") in ("Daily", "Weekly"):
            recurring_rows.append(
                {
                    "Pet": pet_obj.get_name(),
                    "Task": task_data["title"],
                    "Recurrence": task_data["recurrence"],
                    "Time": task_data["Time"].strftime("%H:%M"),
                    "Next date": task_data.get("date", date.today()),
                    "Priority": task_data["priority"],
                    "Complete": task_data.get("complete", False),
                }
            )

if recurring_rows:
    daily_rows = [row for row in recurring_rows if row["Recurrence"] == "Daily"]
    weekly_rows = [row for row in recurring_rows if row["Recurrence"] == "Weekly"]

    if daily_rows:
        st.markdown("**Daily tasks**")
        st.table(sorted(daily_rows, key=lambda row: (row["Pet"], row["Next date"])))
    if weekly_rows:
        st.markdown("**Weekly tasks**")
        st.table(sorted(weekly_rows, key=lambda row: (row["Pet"], row["Next date"])))
else:
    st.info("No recurring tasks yet. Add a task above and set its Recurrence to Daily or Weekly.")
