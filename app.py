from datetime import time

import streamlit as st

from pawpal_system import Owner, Pet, Priority, Scheduler, Task

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

if "owner" not in st.session_state:
    st.session_state["owner"] = Owner(name="Jordan")

owner: Owner = st.session_state["owner"]
scheduler = Scheduler()

st.title("🐾 PawPal+")
st.write("Keep track of your pets' care tasks and today's schedule.")

owner.name = st.text_input("Owner name", value=owner.name)

st.subheader("Your pets")
with st.form("add_pet_form", clear_on_submit=True):
    pet_name = st.text_input("Pet name")
    species = st.selectbox("Species", ["dog", "cat", "other"])
    pet_submitted = st.form_submit_button("Add pet")

if pet_submitted:
    try:
        owner.add_pet(Pet(name=pet_name, species=species))
    except ValueError as error:
        st.error(str(error))
    else:
        st.success(f"Added {pet_name.strip()}!")

if owner.pets:
    st.write(", ".join(f"{pet.name} ({pet.species})" for pet in owner.pets))
else:
    st.info("Add a pet before scheduling care tasks.")

st.subheader("Add a care task")
if owner.pets:
    with st.form("add_task_form", clear_on_submit=True):
        pet_index = st.selectbox(
            "Pet",
            options=range(len(owner.pets)),
            format_func=lambda index: (
                f"{owner.pets[index].name} ({owner.pets[index].species})"
            ),
        )
        description = st.text_input("Task description")
        task_time = st.time_input("Task time", value=time(8, 0))
        frequency = st.selectbox("Frequency", ["daily", "weekly", "one-time"])
        duration_minutes = st.number_input(
            "Duration (minutes)", min_value=1, max_value=240, value=30
        )
        priority_name = st.selectbox("Priority", ["low", "medium", "high"])
        task_submitted = st.form_submit_button("Schedule task")

    if task_submitted:
        try:
            task = Task(
                description=description,
                time=task_time,
                frequency=frequency,
                duration_minutes=int(duration_minutes),
                priority=Priority[priority_name.upper()],
            )
            scheduler.add_task(owner, owner.pets[pet_index], task)
        except ValueError as error:
            st.error(str(error))
        else:
            st.success(f"Scheduled {description.strip()} for {owner.pets[pet_index].name}.")

st.subheader("Today's Schedule")
for warning in scheduler.get_conflict_warnings(owner):
    st.warning(warning)

scheduled_tasks = scheduler.organize_tasks(owner)
if scheduled_tasks:
    for task in scheduled_tasks:
        pet = next(
            pet for pet in owner.pets
            if any(pet_task is task for pet_task in pet.tasks)
        )
        task_time = task.time.strftime("%I:%M %p") if task.time else "Time not set"
        st.write(
            f"**{task_time}** — {pet.name}: {task.description} "
            f"({task.duration_minutes} min, {task.priority.name.lower()} priority)"
        )
else:
    st.info("No pending tasks yet. Add a task above to build today's schedule.")
