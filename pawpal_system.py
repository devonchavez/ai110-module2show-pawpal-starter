from __future__ import annotations
from dataclasses import dataclass, field
from datetime import date, timedelta
import calendar
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
    due_date: Optional[date] = None

    def __post_init__(self) -> None:
        """Normalize task fields after initialization."""
        self.description = self.description.strip()
        self.time = self.time.strip()
        self.frequency = self.frequency.strip().lower()
        if self.priority:
            self.priority = self.priority.strip().lower()

    def mark_complete(self, reschedule: bool = False) -> Optional[Task]:
        """Mark this task as completed and optionally create the next occurrence."""
        self.completed = True

        if not reschedule or not self.is_recurring():
            return None

        base_date = self.due_date or date.today()
        next_due = self._next_due_date(base_date)
        if next_due is None:
            return None

        return self.copy_for_next_occurrence(next_due)

    def mark_incomplete(self) -> None:
        """Mark this task as incomplete."""
        self.completed = False

    def is_recurring(self) -> bool:
        """Return True when this task should repeat on a schedule."""
        return self.frequency in {"daily", "weekly", "monthly"}

    def _next_due_date(self, from_date: date) -> Optional[date]:
        """Calculate the next due date based on the task frequency."""
        if self.frequency == "daily":
            return from_date + timedelta(days=1)
        if self.frequency == "weekly":
            return from_date + timedelta(weeks=1)
        if self.frequency == "monthly":
            next_month = from_date.month + 1
            next_year = from_date.year + (next_month - 1) // 12
            next_month = ((next_month - 1) % 12) + 1
            day = min(from_date.day, calendar.monthrange(next_year, next_month)[1])
            return date(next_year, next_month, day)
        return None

    def copy_for_next_occurrence(self, due_date: date) -> Task:
        """Create a new task object for the next recurring occurrence."""
        return Task(
            description=self.description,
            time=self.time,
            frequency=self.frequency,
            duration_minutes=self.duration_minutes,
            priority=self.priority,
            completed=False,
            due_date=due_date,
        )

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

    def _time_to_minutes(self, time_str: str) -> Optional[int]:
        """Convert an HH:MM time string into total minutes."""
        parts = time_str.split(":")
        if len(parts) != 2:
            return None
        try:
            hours = int(parts[0])
            minutes = int(parts[1])
        except ValueError:
            return None
        return hours * 60 + minutes

    def _tasks_overlap(self, first: Task, second: Task) -> bool:
        """Return True when two tasks overlap in time."""
        first_start = self._time_to_minutes(first.time)
        second_start = self._time_to_minutes(second.time)
        if first_start is None or second_start is None:
            return False

        if first.duration_minutes is not None and second.duration_minutes is not None:
            first_end = first_start + first.duration_minutes
            second_end = second_start + second.duration_minutes
            return first_start < second_end and second_start < first_end

        return first_start == second_start

    def detect_conflicts(self, task: Task) -> Optional[str]:
        """Return a warning message if the task conflicts with existing scheduled tasks."""
        for existing in self.tasks:
            if self._tasks_overlap(task, existing):
                if task.pet and existing.pet:
                    return (
                        f'Warning: "{task.description}" for {task.pet.name} '
                        f'conflicts with "{existing.description}" for {existing.pet.name} '
                        f'at {existing.time}.'
                    )
                return (
                    f'Warning: "{task.description}" conflicts with "{existing.description}" '
                    f'at {existing.time}.'
                )
        return None

    def detect_same_time_conflicts(self) -> List[str]:
        """Return warnings for any two scheduled tasks that start at the same time."""
        warnings: List[str] = []
        for index, first in enumerate(self.tasks):
            first_start = self._time_to_minutes(first.time)
            if first_start is None:
                continue

            for second in self.tasks[index + 1 :]:
                second_start = self._time_to_minutes(second.time)
                if second_start is None or first_start != second_start:
                    continue

                if first.pet and second.pet:
                    if first.pet is second.pet:
                        warnings.append(
                            f'Warning: {first.pet.name} has multiple tasks at {first.time}: "{first.description}" and "{second.description}".'
                        )
                    else:
                        warnings.append(
                            f'Warning: tasks for {first.pet.name} and {second.pet.name} are both scheduled at {first.time}. '
                            f'"{first.description}" and "{second.description}" overlap in start time.'
                        )
                else:
                    warnings.append(
                        f'Warning: "{first.description}" and "{second.description}" are both scheduled at {first.time}.'
                    )

        return warnings

    def add_pet_tasks(self, pet: Pet) -> None:
        """Add all tasks from a pet into the scheduler."""
        for task in pet.tasks:
            self.add_task(task)

    def get_tasks(self) -> List[Task]:
        """Return a list of tasks currently scheduled."""
        return list(self.tasks)

    def filter_tasks(
        self,
        completed: Optional[bool] = None,
        pet_name: Optional[str] = None,
    ) -> List[Task]:
        """Return tasks filtered by completion status and/or pet name."""
        filtered: List[Task] = list(self.tasks)

        if completed is not None:
            filtered = [task for task in filtered if task.completed is completed]

        if pet_name is not None:
            normalized_name = pet_name.strip().lower()
            filtered = [
                task
                for task in filtered
                if task.pet is not None and task.pet.name.lower() == normalized_name
            ]

        return filtered

    def complete_task(self, task: Task, reschedule: bool = False) -> Optional[Task]:
        """Mark a task complete and optionally add the next recurring instance."""
        next_task = task.mark_complete(reschedule=reschedule)
        if next_task is not None:
            if task.pet is not None:
                task.pet.add_task(next_task)
            self.add_task(next_task)
        return next_task

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

    def schedule_for_pet(self, pet: Pet, task: Task) -> Optional[str]:
        """Schedule a task and assign it to a pet.

        Returns a warning message if the task conflicts with existing tasks.
        """
        task.assign_pet(pet)
        warning = self.detect_conflicts(task)
        pet.add_task(task)
        self.add_task(task)
        return warning

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
