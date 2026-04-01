from pawpal_system import Owner, Pet, Task, Scheduler


def main() -> None:
    owner = Owner(owner_name="Ava Carter", age=36)

    bella = Pet(
        name="Bella",
        age=4,
        animal_type="dog",
        breed="Labrador Retriever",
        color="yellow",
        weight=65.0,
        height=23.0,
        medical_conditions="none",
    )

    luna = Pet(
        name="Luna",
        age=2,
        animal_type="cat",
        breed="Siamese",
        color="seal point",
        weight=10.2,
        height=11.0,
        medical_conditions="allergies",
    )

    owner.add_pet(bella)
    owner.add_pet(luna)

    schedule = Scheduler(sort_by="time")
    warnings: list[str] = []

    warning = schedule.schedule_for_pet(
        bella,
        Task(description="Morning walk", time="08:00", frequency="daily"),
    )
    if warning:
        warnings.append(warning)

    warning = schedule.schedule_for_pet(
        luna,
        Task(description="Medication", time="09:30", frequency="daily"),
    )
    if warning:
        warnings.append(warning)

    warning = schedule.schedule_for_pet(
        bella,
        Task(description="Grooming brush", time="09:30", frequency="daily"),
    )
    if warning:
        warnings.append(warning)

    schedule.sort_tasks()

    print("Today's schedule:")
    for task in schedule.task_summary():
        print(f"- {task}")

    if warnings:
        print("\nWarnings:")
        for warning in warnings:
            print(f"- {warning}")

    print()
    print(f"Owner: {owner.owner_name}")
    for pet in owner.list_pets():
        print(f"  Pet: {pet.name} ({pet.animal_type})")
        for pet_task in pet.list_tasks():
            print(f"    * {pet_task.summary()}")


if __name__ == "__main__":
    main()
