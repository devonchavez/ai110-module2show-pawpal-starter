from pawpal_system import Pet, Task


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
