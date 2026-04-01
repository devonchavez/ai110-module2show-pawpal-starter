from __future__ import annotations
from dataclasses import dataclass, field
from typing import List


@dataclass
class Task:
    description: str
    time: str
    urgency: str

    def __post_init__(self):
        # add validation or normalization logic here
        pass


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

    def describe(self) -> str:
        return (
            f"{self.name} is a {self.age}-year-old {self.color} {self.animal_type} "
            f"({self.breed}) with medical condition {self.medical_conditions}."
        )


@dataclass
class Owner:
    name: str
    age: int
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        self.pets.append(pet)

    def list_pets(self) -> List[Pet]:
        return self.pets


class Scheduler:
    def __init__(self, sort_by: str = "time") -> None:
        self.tasks: List[Task] = []
        self.sort_by = sort_by

    def add_task(self, task: Task) -> None:
        self.tasks.append(task)

    def get_tasks(self) -> List[Task]:
        return self.tasks

    def sort_tasks(self) -> None:
        # placeholder for sorting logic based on sort_by
        pass

    def schedule_for_pet(self, pet: Pet, task: Task) -> None:
        # placeholder for associating a task with a pet
        self.add_task(task)
