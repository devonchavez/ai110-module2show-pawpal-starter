import streamlit as st
from pawpal_system import Owner, Pet, Task, Scheduler

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

st.subheader("Owner & Pet Information")

col_owner1, col_owner2 = st.columns(2)
with col_owner1:
    owner_name = st.text_input("Owner name", value="Jordan")
with col_owner2:
    owner_age = st.number_input("Owner age", min_value=1, max_value=120, value=30)

st.markdown("**Pet Details**")
col_pet1, col_pet2, col_pet3 = st.columns(3)
with col_pet1:
    pet_name = st.text_input("Pet name", value="Mochi")
    species = st.selectbox("Species", ["dog", "cat", "rabbit", "bird", "other"])
with col_pet2:
    pet_age = st.number_input("Pet age (years)", min_value=0, max_value=50, value=2)
    breed = st.text_input("Breed", value="Mixed")
with col_pet3:
    color = st.text_input("Color", value="Brown")
    weight = st.number_input("Weight (lbs)", min_value=0.1, max_value=500.0, value=10.0, step=0.1)

medical_conditions = st.text_input("Medical conditions (or 'None')", value="None")

st.divider()

# --- Session state init ---
if "tasks" not in st.session_state:
    st.session_state.tasks = []

if "editing_index" not in st.session_state:
    st.session_state.editing_index = None

if "schedule_generated" not in st.session_state:
    st.session_state.schedule_generated = False

if "conflict_warnings" not in st.session_state:
    st.session_state.conflict_warnings = []

if "schedule_sort_by" not in st.session_state:
    st.session_state.schedule_sort_by = "time"


def run_conflict_check(sort_by: str) -> list[str]:
    """Re-run scheduling and conflict detection against current tasks. Returns warnings."""
    pet = Pet(
        name=pet_name.strip() or "Pet",
        age=int(pet_age),
        animal_type=species,
        breed=breed.strip() or "Unknown",
        color=color.strip() or "Unknown",
        weight=float(weight),
        height=0.0,
        medical_conditions=medical_conditions.strip() or "None",
    )
    schedule = Scheduler(sort_by=sort_by)
    warnings = []
    for task_data in st.session_state.tasks:
        task = Task(
            description=task_data["title"],
            time=task_data["time"],
            frequency=task_data["priority"],
            duration_minutes=task_data["duration_minutes"],
            priority=task_data["priority"],
            completed=task_data["completed"],
        )
        w = schedule.schedule_for_pet(pet, task)
        if w:
            warnings.append(w)
    schedule.sort_tasks()
    warnings += schedule.detect_same_time_conflicts()
    return warnings


# ===========================================================================
# PRE-SCHEDULE: Task builder (no mark-complete, full add/edit/delete)
# ===========================================================================
if not st.session_state.schedule_generated:
    st.markdown("### Tasks")
    st.caption("Build your task list below, then generate the schedule.")

    # Add task form
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        task_title = st.text_input("Task title", value="Morning walk")
    with col2:
        duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
    with col3:
        priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)
    with col4:
        task_time = st.text_input("Time (HH:MM)", value="08:00")

    if st.button("Add task"):
        st.session_state.tasks.append(
            {
                "title": task_title,
                "duration_minutes": int(duration),
                "priority": priority,
                "time": task_time,
                "completed": False,
            }
        )
        st.rerun()

    # Task list (no completion checkbox pre-schedule)
    if not st.session_state.tasks:
        st.info("No tasks yet. Add one above.")
    else:
        st.caption(f"{len(st.session_state.tasks)} task(s) — click Edit to modify before generating the schedule.")

        hc1, hc2, hc3, hc4, hc5, hc6 = st.columns([2, 4, 2, 2, 1, 1])
        hc1.markdown("**Time**")
        hc2.markdown("**Task**")
        hc3.markdown("**Duration**")
        hc4.markdown("**Priority**")

        for i, task in enumerate(st.session_state.tasks):
            if st.session_state.editing_index == i:
                with st.container(border=True):
                    ec1, ec2, ec3, ec4 = st.columns([3, 2, 2, 2])
                    with ec1:
                        new_title = st.text_input("Title", value=task["title"], key=f"edit_title_{i}")
                    with ec2:
                        new_time = st.text_input("Time (HH:MM)", value=task["time"], key=f"edit_time_{i}")
                    with ec3:
                        new_duration = st.number_input(
                            "Duration (min)", value=task["duration_minutes"],
                            min_value=1, max_value=240, key=f"edit_dur_{i}"
                        )
                    with ec4:
                        pri_opts = ["low", "medium", "high"]
                        new_priority = st.selectbox(
                            "Priority", pri_opts,
                            index=pri_opts.index(task["priority"]),
                            key=f"edit_pri_{i}"
                        )
                    sc1, sc2 = st.columns(2)
                    with sc1:
                        if st.button("Save", key=f"save_{i}", type="primary"):
                            st.session_state.tasks[i] = {
                                "title": new_title.strip() or task["title"],
                                "time": new_time.strip() or task["time"],
                                "duration_minutes": int(new_duration),
                                "priority": new_priority,
                                "completed": task["completed"],
                            }
                            st.session_state.editing_index = None
                            st.rerun()
                    with sc2:
                        if st.button("Cancel", key=f"cancel_{i}"):
                            st.session_state.editing_index = None
                            st.rerun()
            else:
                rc1, rc2, rc3, rc4, rc5, rc6 = st.columns([2, 4, 2, 2, 1, 1])
                rc1.write(task["time"])
                rc2.markdown(task["title"])
                rc3.write(f"{task['duration_minutes']} min")
                rc4.write(task["priority"].capitalize())
                with rc5:
                    if st.button("Edit", key=f"edit_{i}"):
                        st.session_state.editing_index = i
                        st.rerun()
                with rc6:
                    if st.button("Del", key=f"del_{i}"):
                        st.session_state.tasks.pop(i)
                        if st.session_state.editing_index == i:
                            st.session_state.editing_index = None
                        st.rerun()

    st.divider()
    st.subheader("Build Schedule")
    sort_by = st.selectbox("Sort tasks by", ["time", "description", "frequency"], index=0)

    if st.button("Generate schedule", type="primary"):
        if not st.session_state.tasks:
            st.warning("Add at least one task before generating a schedule.")
        else:
            st.session_state.schedule_sort_by = sort_by
            st.session_state.conflict_warnings = run_conflict_check(sort_by)
            st.session_state.schedule_generated = True
            st.rerun()


# ===========================================================================
# POST-SCHEDULE: Active schedule — edit to fix warnings, mark complete
# ===========================================================================
else:
    sort_by = st.session_state.schedule_sort_by

    owner = Owner(owner_name=owner_name.strip() or "Unknown", age=int(owner_age))
    pet = Pet(
        name=pet_name.strip() or "Pet",
        age=int(pet_age),
        animal_type=species,
        breed=breed.strip() or "Unknown",
        color=color.strip() or "Unknown",
        weight=float(weight),
        height=0.0,
        medical_conditions=medical_conditions.strip() or "None",
    )
    owner.add_pet(pet)

    completed_count = sum(1 for t in st.session_state.tasks if t["completed"])
    total_count = len(st.session_state.tasks)

    st.success(f"Schedule active for {pet.name} — {completed_count}/{total_count} task(s) complete.")

    col_owner, col_pet = st.columns(2)
    with col_owner:
        st.metric("Owner", f"{owner.owner_name}, age {owner.age}")
    with col_pet:
        st.metric("Pet", f"{pet.name} ({pet.animal_type})")
    st.caption(pet.describe())

    # Conflict warnings (live-updated after edits)
    warnings = st.session_state.conflict_warnings
    if warnings:
        st.markdown("### Conflict Warnings")
        st.caption("Edit the tasks below to resolve these conflicts, then save to recheck.")
        for w in warnings:
            st.warning(w)
    else:
        st.success("No scheduling conflicts detected.")

    st.markdown("### Scheduled Tasks")
    st.caption("Check the box to mark a task done as your day progresses. Click Edit to adjust any task — conflicts recheck on save.")

    hc0, hc1, hc2, hc3, hc4, hc5, hc6 = st.columns([1, 2, 4, 2, 2, 1, 1])
    hc0.markdown("**Done**")
    hc1.markdown("**Time**")
    hc2.markdown("**Task**")
    hc3.markdown("**Duration**")
    hc4.markdown("**Priority**")

    for i, task in enumerate(st.session_state.tasks):
        if st.session_state.editing_index == i:
            with st.container(border=True):
                ec1, ec2, ec3, ec4 = st.columns([3, 2, 2, 2])
                with ec1:
                    new_title = st.text_input("Title", value=task["title"], key=f"edit_title_{i}")
                with ec2:
                    new_time = st.text_input("Time (HH:MM)", value=task["time"], key=f"edit_time_{i}")
                with ec3:
                    new_duration = st.number_input(
                        "Duration (min)", value=task["duration_minutes"],
                        min_value=1, max_value=240, key=f"edit_dur_{i}"
                    )
                with ec4:
                    pri_opts = ["low", "medium", "high"]
                    new_priority = st.selectbox(
                        "Priority", pri_opts,
                        index=pri_opts.index(task["priority"]),
                        key=f"edit_pri_{i}"
                    )
                sc1, sc2 = st.columns(2)
                with sc1:
                    if st.button("Save & recheck", key=f"save_{i}", type="primary"):
                        st.session_state.tasks[i] = {
                            "title": new_title.strip() or task["title"],
                            "time": new_time.strip() or task["time"],
                            "duration_minutes": int(new_duration),
                            "priority": new_priority,
                            "completed": task["completed"],
                        }
                        st.session_state.editing_index = None
                        # Recheck conflicts with updated tasks
                        st.session_state.conflict_warnings = run_conflict_check(sort_by)
                        st.rerun()
                with sc2:
                    if st.button("Cancel", key=f"cancel_{i}"):
                        st.session_state.editing_index = None
                        st.rerun()
        else:
            rc0, rc1, rc2, rc3, rc4, rc5, rc6 = st.columns([1, 2, 4, 2, 2, 1, 1])
            with rc0:
                new_done = st.checkbox(
                    "", value=task["completed"], key=f"done_{i}",
                    label_visibility="collapsed"
                )
                if new_done != task["completed"]:
                    st.session_state.tasks[i]["completed"] = new_done
                    st.rerun()
            with rc1:
                st.write(task["time"])
            with rc2:
                label = f"~~{task['title']}~~" if task["completed"] else task["title"]
                st.markdown(label)
            with rc3:
                st.write(f"{task['duration_minutes']} min")
            with rc4:
                st.write(task["priority"].capitalize())
            with rc5:
                if st.button("Edit", key=f"edit_{i}"):
                    st.session_state.editing_index = i
                    st.rerun()
            with rc6:
                if st.button("Del", key=f"del_{i}"):
                    st.session_state.tasks.pop(i)
                    if st.session_state.editing_index == i:
                        st.session_state.editing_index = None
                    st.session_state.conflict_warnings = run_conflict_check(sort_by)
                    st.rerun()

    st.divider()
    if st.button("Reset & rebuild task list"):
        st.session_state.schedule_generated = False
        st.session_state.conflict_warnings = []
        st.session_state.editing_index = None
        st.rerun()
