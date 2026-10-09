"""Core data models and task-management logic for PawPal+."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime, time as Time, timedelta
from enum import IntEnum


class Priority(IntEnum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3


@dataclass
class Task:
    description: str
    time: Time | None = None
    frequency: str = "daily"
    is_completed: bool = False
    duration_minutes: int = 30
    priority: Priority = Priority.MEDIUM
    due_date: date = field(default_factory=date.today)

    def __post_init__(self) -> None:
        """Validate the task's required values."""
        if not self.description.strip():
            raise ValueError("Task description cannot be empty.")
        if not self.frequency.strip():
            raise ValueError("Task frequency cannot be empty.")
        if self.duration_minutes <= 0:
            raise ValueError("Task duration must be greater than zero.")

    def mark_complete(self) -> None:
        """Mark this task as completed."""
        self.is_completed = True

    def mark_incomplete(self) -> None:
        """Mark this task as not completed."""
        self.is_completed = False

    def create_next_occurrence(self, completed_on: date) -> Task | None:
        """Create the next recurring task, or return None for unsupported frequencies.

        The new task copies this task's care details, starts incomplete, and is due
        one or seven days after ``completed_on`` for daily or weekly recurrence.
        """
        interval_days = {"daily": 1, "weekly": 7}.get(self.frequency.strip().casefold())
        if interval_days is None:
            return None
        return Task(
            description=self.description,
            time=self.time,
            frequency=self.frequency,
            duration_minutes=self.duration_minutes,
            priority=self.priority,
            due_date=completed_on + timedelta(days=interval_days),
        )


@dataclass
class Pet:
    name: str
    species: str
    age: int = 0
    notes: str = ""
    tasks: list[Task] = field(default_factory=list)

    def __post_init__(self) -> None:
        """Validate the pet's required details."""
        if not self.name.strip():
            raise ValueError("Pet name cannot be empty.")
        if not self.species.strip():
            raise ValueError("Pet species cannot be empty.")
        if self.age < 0:
            raise ValueError("Pet age cannot be negative.")

    def add_task(self, task: Task) -> None:
        """Add a task to this pet."""
        if any(existing is task for existing in self.tasks):
            raise ValueError("Task is already assigned to this pet.")
        self.tasks.append(task)


@dataclass(frozen=True)
class TaskConflict:
    first_pet: Pet
    first_task: Task
    second_pet: Pet
    second_task: Task


@dataclass
class Owner:
    name: str
    pets: list[Pet] = field(default_factory=list)

    def __post_init__(self) -> None:
        """Validate the owner's name."""
        if not self.name.strip():
            raise ValueError("Owner name cannot be empty.")

    def add_pet(self, pet: Pet) -> None:
        """Register a pet with this owner."""
        if any(existing is pet for existing in self.pets):
            raise ValueError("Pet is already registered to this owner.")
        self.pets.append(pet)

    def get_all_tasks(self) -> list[Task]:
        """Return the tasks belonging to all of this owner's pets."""
        return [task for pet in self.pets for task in pet.tasks]


class Scheduler:
    """Retrieves, orders, and updates tasks across all of an owner's pets."""

    def get_all_tasks(self, owner: Owner) -> list[Task]:
        """Retrieve all tasks from the owner's pets."""
        return owner.get_all_tasks()

    def get_pending_tasks(self, owner: Owner) -> list[Task]:
        """Return all incomplete tasks from the owner's pets."""
        return [
            task for task in owner.get_all_tasks()
            if not task.is_completed
        ]

    def filter_tasks(
        self,
        owner: Owner,
        is_completed: bool | None = None,
        pet_name: str | None = None,
    ) -> list[Task]:
        """Filter owned tasks by optional completion status and pet name.

        Pet names are matched case-insensitively. When both filters are supplied,
        a task must satisfy both; omitted filters do not restrict the results.
        """
        normalized_pet_name = pet_name.strip().casefold() if pet_name is not None else None
        return [
            task
            for pet in owner.pets
            for task in pet.tasks
            if (is_completed is None or task.is_completed == is_completed)
            and (
                normalized_pet_name is None
                or pet.name.casefold() == normalized_pet_name
            )
        ]

    def sort_by_time(self, tasks: list[Task]) -> list[Task]:
        """Return tasks chronologically, placing tasks without a time last."""
        return sorted(tasks, key=lambda task: task.time or Time.max)

    def organize_tasks(self, owner: Owner) -> list[Task]:
        """Return pending tasks by time, then priority, with untimed tasks last.

        Earlier scheduled tasks come first; higher priority breaks ties at the
        same time. Completed tasks are omitted.
        """
        return sorted(
            self.get_pending_tasks(owner),
            key=lambda task: (
                task.time is None,
                task.time or Time.max,
                -task.priority,
            ),
        )

    def find_conflicts(self, owner: Owner) -> list[TaskConflict]:
        """Find pending task intervals that overlap on the same due date.

        Tasks without a time and completed tasks are ignored. Intervals that only
        touch at an endpoint are not conflicts. The result identifies both pets
        and tasks for each overlapping pair.
        """
        scheduled: list[tuple[Pet, Task, datetime, datetime]] = []
        for pet in owner.pets:
            for task in pet.tasks:
                if task.is_completed or task.time is None:
                    continue
                start = datetime.combine(task.due_date, task.time)
                end = start + timedelta(minutes=task.duration_minutes)
                scheduled.append((pet, task, start, end))

        conflicts: list[TaskConflict] = []
        for index, (first_pet, first_task, first_start, first_end) in enumerate(scheduled):
            for second_pet, second_task, second_start, second_end in scheduled[index + 1:]:
                if first_task is second_task:
                    continue
                if first_start < second_end and second_start < first_end:
                    conflicts.append(
                        TaskConflict(first_pet, first_task, second_pet, second_task)
                    )
        return conflicts

    def get_conflict_warnings(self, owner: Owner) -> list[str]:
        """Return one readable warning per conflict, or an empty list if none exist."""
        return [
            (
                f"{conflict.first_pet.name}: '{conflict.first_task.description}' overlaps "
                f"{conflict.second_pet.name}: '{conflict.second_task.description}'."
            )
            for conflict in self.find_conflicts(owner)
        ]

    def add_task(self, owner: Owner, pet: Pet, task: Task) -> None:
        """Add a task to a pet registered to the owner."""
        if pet not in owner.pets:
            raise ValueError("Cannot add a task to a pet not owned by this owner.")
        pet.add_task(task)

    def mark_task_complete(
        self,
        owner: Owner,
        task: Task,
        completed_on: date | None = None,
    ) -> None:
        """Complete an owned task and add its next daily or weekly occurrence.

        Raises ValueError if the task is not owned by ``owner``. Repeated calls
        for an already completed task do nothing, preventing duplicate recurrence.
        """
        pet = next(
            (
                pet
                for pet in owner.pets
                if any(owned_task is task for owned_task in pet.tasks)
            ),
            None,
        )
        if pet is None:
            raise ValueError("Cannot complete a task that does not belong to this owner.")
        if task.is_completed:
            return

        task.mark_complete()
        next_task = task.create_next_occurrence(completed_on or date.today())
        if next_task is not None:
            pet.add_task(next_task)
