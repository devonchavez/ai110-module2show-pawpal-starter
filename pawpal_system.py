from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Task:
    description: str
    time: str
    frequency: str
    duration_minutes: Optional[int] = None
    priority: Optional[str] = None
    completed: bool = False
    pet: Optional[Pet] = None

    def __post_init__(self) -> None:
        """Normalize task fields after initialization."""
        self.description = self.description.strip()
        self.time = self.time.strip()
        self.frequency = self.frequency.strip().lower()
        if self.priority:
            self.priority = self.priority.strip().lower()

    def mark_complete(self) -> None:
        """Mark this task as completed."""
        self.completed = True

    def mark_incomplete(self) -> None:
        """Mark this task as incomplete."""
        self.completed = False

    def assign_pet(self, pet: Pet) -> None:
        """Assign a pet to this task."""
        self.pet = pet

    def summary(self) -> str:
        """Return a formatted summary string for the task."""
        status = "done" if self.completed else "pending"
        pet_name = self.pet.name if self.pet else "unassigned"
        details = []
        if self.priority:
            details.append(self.priority)
        if self.duration_minutes is not None:
            details.append(f"{self.duration_minutes} min")
        details_text = f" [{', '.join(details)}]" if details else ""
        return f"{self.description} ({self.frequency}) at {self.time} for {pet_name}{details_text} - {status}"


@dataclass
class Pet:
    name: str
    age: int
    animal_type: str
    breed: str
    color: str
    weight: float
    height: float
    medical_conditions: str
    owner: Optional[Owner] = None
    tasks: List[Task] = field(default_factory=list)

    def describe(self) -> str:
        """Return a brief description of the pet."""
        return (
            f"{self.name} is a {self.age}-year-old {self.color} {self.animal_type} "
            f"({self.breed}) with medical conditions: {self.medical_conditions}."
        )

    def add_task(self, task: Task) -> None:
        """Add a task to the scheduler if not already present."""
        task.assign_pet(self)
        self.tasks.append(task)

    def remove_task(self, task: Task) -> None:
        """Remove a task from this pet if present."""
        if task in self.tasks:
            self.tasks.remove(task)
            task.pet = None

    def list_tasks(self) -> List[Task]:
        """Return a list of tasks for this pet."""
        return list(self.tasks)

    def incomplete_tasks(self) -> List[Task]:
        """Return the pet tasks that are not completed."""
        return [task for task in self.tasks if not task.completed]

    def completed_tasks(self) -> List[Task]:
        """Return the pet tasks that are completed."""
        return [task for task in self.tasks if task.completed]


@dataclass
class Owner:
    owner_name: str
    age: int
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to the owner and set ownership."""
        pet.owner = self
        self.pets.append(pet)

    def remove_pet(self, pet: Pet) -> None:
        """Remove a pet from the owner if present."""
        if pet in self.pets:
            pet.owner = None
            self.pets.remove(pet)

    def list_pets(self) -> List[Pet]:
        """Return a list of pets for this owner."""
        return list(self.pets)

    def get_all_tasks(self) -> List[Task]:
        """Return all tasks across the owner’s pets."""
        tasks: List[Task] = []
        for pet in self.pets:
            tasks.extend(pet.tasks)
        return tasks

    def get_pending_tasks(self) -> List[Task]:
        """Return pending tasks in the scheduler."""
        return [task for task in self.get_all_tasks() if not task.completed]

    def get_completed_tasks(self) -> List[Task]:
        """Return completed tasks in the scheduler."""
        return [task for task in self.get_all_tasks() if task.completed]


class Scheduler:
    def __init__(self, sort_by: str = "time") -> None:
        """Initialize the scheduler with an optional sort order."""
        self.tasks: List[Task] = []
        self.sort_by = sort_by

    def add_task(self, task: Task) -> None:
        """Add a task to the scheduler if not already present."""
        if task not in self.tasks:
            self.tasks.append(task)

    def add_pet_tasks(self, pet: Pet) -> None:
        """Add all tasks from a pet into the scheduler."""
        for task in pet.tasks:
            self.add_task(task)

    def get_tasks(self) -> List[Task]:
        """Return a list of tasks currently scheduled."""
        return list(self.tasks)

    def get_tasks_for_pet(self, pet: Pet) -> List[Task]:
        """Return tasks scheduled for a specific pet."""
        return [task for task in self.tasks if task.pet is pet]

    def get_tasks_for_owner(self, owner: Owner) -> List[Task]:
        """Return tasks scheduled for a specific owner."""
        return [task for task in self.tasks if task.pet and task.pet.owner is owner]

    def get_pending_tasks(self) -> List[Task]:
        """Return pending tasks in the scheduler."""
        return [task for task in self.tasks if not task.completed]

    def get_completed_tasks(self) -> List[Task]:
        """Return completed tasks in the scheduler."""
        return [task for task in self.tasks if task.completed]

    def sort_tasks(self) -> None:
        """Sort scheduled tasks by the configured sort key."""
        if self.sort_by == "time":
            self.tasks.sort(key=lambda task: task.time)
        elif self.sort_by == "frequency":
            self.tasks.sort(key=lambda task: task.frequency)
        elif self.sort_by == "description":
            self.tasks.sort(key=lambda task: task.description.lower())
        else:
            self.tasks.sort(key=lambda task: task.time)

    def schedule_for_pet(self, pet: Pet, task: Task) -> None:
        """Schedule a task and assign it to a pet."""
        task.assign_pet(pet)
        pet.add_task(task)
        self.add_task(task)

    def organize_by_pet(self) -> dict[str, List[Task]]:
        """Organize scheduled tasks by pet name."""
        organized: dict[str, List[Task]] = {}
        for task in self.tasks:
            key = task.pet.name if task.pet else "Unassigned"
            organized.setdefault(key, []).append(task)
        return organized

    def task_summary(self) -> List[str]:
        """Return a list of summary strings for all tasks."""
        return [task.summary() for task in self.tasks]
