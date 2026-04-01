from datetime import date

from pawpal_system import Pet, Task, Scheduler


def test_task_mark_complete_updates_status() -> None:
    task = Task(description="Brush fur", time="08:00", frequency="Daily")
    assert task.completed is False

    task.mark_complete()

    assert task.completed is True


def test_adding_task_to_pet_increases_task_count() -> None:
    pet = Pet(
        name="Buddy",
        age=5,
        animal_type="Dog",
        breed="Labrador",
        color="Golden",
        weight=30.0,
        height=60.0,
        medical_conditions="None",
    )
    initial_task_count = len(pet.tasks)
    task = Task(description="Feed breakfast", time="07:00", frequency="Daily")

    pet.add_task(task)

    assert len(pet.tasks) == initial_task_count + 1
    assert pet.tasks[-1] is task
    assert task.pet is pet


def test_scheduler_complete_task_reschedules_daily_task() -> None:
    pet = Pet(
        name="Bella",
        age=4,
        animal_type="Dog",
        breed="Labrador",
        color="Yellow",
        weight=65.0,
        height=23.0,
        medical_conditions="None",
    )
    task = Task(
        description="Medication",
        time="09:30",
        frequency="daily",
        due_date=date(2026, 3, 31),
    )
    scheduler = Scheduler()
    scheduler.schedule_for_pet(pet, task)

    next_task = scheduler.complete_task(task, reschedule=True)

    assert task.completed is True
    assert next_task is not None
    assert next_task is not task
    assert next_task.completed is False
    assert next_task.due_date == date(2026, 4, 1)
    assert next_task.pet is pet
    assert next_task in scheduler.tasks
    assert next_task in pet.tasks


def test_scheduler_detects_same_time_conflicts_for_same_pet() -> None:
    pet = Pet(
        name="Milo",
        age=3,
        animal_type="Dog",
        breed="Terrier",
        color="White",
        weight=20.0,
        height=35.0,
        medical_conditions="None",
    )
    task_one = Task(description="Breakfast", time="07:00", frequency="daily")
    task_two = Task(description="Morning walk", time="07:00", frequency="daily")

    scheduler = Scheduler()
    scheduler.schedule_for_pet(pet, task_one)
    scheduler.schedule_for_pet(pet, task_two)

    warnings = scheduler.detect_same_time_conflicts()

    assert len(warnings) == 1
    assert "Milo has multiple tasks" in warnings[0]


def test_scheduler_detects_same_time_conflicts_for_different_pets() -> None:
    pet_a = Pet(
        name="Bella",
        age=4,
        animal_type="Dog",
        breed="Labrador",
        color="Yellow",
        weight=65.0,
        height=23.0,
        medical_conditions="None",
    )
    pet_b = Pet(
        name="Luna",
        age=2,
        animal_type="Cat",
        breed="Siamese",
        color="Seal point",
        weight=10.2,
        height=11.0,
        medical_conditions="Allergies",
    )
    task_a = Task(description="Morning walk", time="08:00", frequency="daily")
    task_b = Task(description="Medication", time="08:00", frequency="daily")

    scheduler = Scheduler()
    scheduler.schedule_for_pet(pet_a, task_a)
    scheduler.schedule_for_pet(pet_b, task_b)

    warnings = scheduler.detect_same_time_conflicts()

    assert len(warnings) == 1
    assert "tasks for Bella and Luna" in warnings[0]


def test_scheduler_filters_tasks_by_completion_and_pet_name() -> None:
    pet_a = Pet(
        name="Bella",
        age=4,
        animal_type="Dog",
        breed="Labrador",
        color="Yellow",
        weight=65.0,
        height=23.0,
        medical_conditions="None",
    )
    pet_b = Pet(
        name="Luna",
        age=2,
        animal_type="Cat",
        breed="Siamese",
        color="Seal point",
        weight=10.2,
        height=11.0,
        medical_conditions="Allergies",
    )

    task_a = Task(description="Morning walk", time="08:00", frequency="Daily")
    task_b = Task(description="Medication", time="09:30", frequency="Daily")

    scheduler = Scheduler()
    scheduler.schedule_for_pet(pet_a, task_a)
    scheduler.schedule_for_pet(pet_b, task_b)

    task_a.mark_complete()

    completed_tasks = scheduler.filter_tasks(completed=True)
    pending_tasks = scheduler.filter_tasks(completed=False)
    bella_tasks = scheduler.filter_tasks(pet_name="bella")
    luna_pending = scheduler.filter_tasks(completed=False, pet_name="Luna")

    assert completed_tasks == [task_a]
    assert pending_tasks == [task_b]
    assert bella_tasks == [task_a]
    assert luna_pending == [task_b]


def test_sort_tasks_orders_by_time_chronologically() -> None:
    # Add tasks in deliberately non-chronological order.
    task_afternoon = Task(description="Evening walk", time="17:00", frequency="daily")
    task_morning = Task(description="Breakfast", time="07:30", frequency="daily")
    task_midday = Task(description="Midday meds", time="12:00", frequency="daily")

    scheduler = Scheduler()
    scheduler.add_task(task_afternoon)
    scheduler.add_task(task_morning)
    scheduler.add_task(task_midday)

    scheduler.sort_tasks()

    times = [task.time for task in scheduler.tasks]
    assert times == ["07:30", "12:00", "17:00"]


def test_daily_task_complete_without_reschedule_creates_no_new_task() -> None:
    pet = Pet(
        name="Oscar",
        age=2,
        animal_type="Cat",
        breed="Maine Coon",
        color="Gray",
        weight=12.0,
        height=14.0,
        medical_conditions="None",
    )
    task = Task(
        description="Morning feed",
        time="08:00",
        frequency="daily",
        due_date=date(2026, 3, 31),
    )
    scheduler = Scheduler()
    scheduler.schedule_for_pet(pet, task)

    next_task = scheduler.complete_task(task, reschedule=False)

    assert task.completed is True
    assert next_task is None
    # Only the original task should be in the scheduler.
    assert len(scheduler.tasks) == 1


def test_scheduler_no_conflict_warning_when_tasks_at_different_times() -> None:
    pet = Pet(
        name="Cleo",
        age=6,
        animal_type="Dog",
        breed="Beagle",
        color="Tricolor",
        weight=22.0,
        height=38.0,
        medical_conditions="None",
    )
    task_one = Task(description="Morning walk", time="07:00", frequency="daily")
    task_two = Task(description="Evening walk", time="18:00", frequency="daily")

    scheduler = Scheduler()
    scheduler.schedule_for_pet(pet, task_one)
    scheduler.schedule_for_pet(pet, task_two)

    warnings = scheduler.detect_same_time_conflicts()

    assert warnings == []
