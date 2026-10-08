"""Data models and class stubs for the PawPal+ pet-care planner."""

from dataclasses import dataclass, field
from enum import Enum


class TaskType(Enum):
    WALK = "walk"
    FEEDING = "feeding"
    MEDICATION = "medication"
    ENRICHMENT = "enrichment"
    GROOMING = "grooming"
    OTHER = "other"


class Priority(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


@dataclass
class CareTask:
    title: str
    task_type: TaskType
    duration_minutes: int
    priority: Priority
    preferred_time: str = ""
    is_recurring: bool = False
    notes: str = ""

    def update(self, details: dict[str, object]) -> None:
        raise NotImplementedError


@dataclass
class Pet:
    name: str
    species: str
    age: int = 0
    notes: str = ""
    tasks: list[CareTask] = field(default_factory=list)

    def add_task(self, task: CareTask) -> None:
        raise NotImplementedError

    def update_info(self, details: dict[str, object]) -> None:
        raise NotImplementedError


@dataclass
class Owner:
    name: str
    preferred_wake_time: str = ""
    preferred_bed_time: str = ""
    preferred_task_times: list[str] = field(default_factory=list)
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        raise NotImplementedError

    def update_preferences(self, preferences: dict[str, object]) -> None:
        raise NotImplementedError


@dataclass
class SchedulingConstraints:
    date: str
    available_start_time: str
    available_end_time: str
    available_minutes: int
    respect_preferred_times: bool = True

    def validate(self) -> bool:
        raise NotImplementedError


@dataclass
class ScheduledTask:
    task: CareTask
    start_time: str
    end_time: str
    reason: str


@dataclass
class UnscheduledTask:
    task: CareTask
    reason: str


@dataclass
class DailyPlan:
    date: str
    total_scheduled_minutes: int = 0
    summary: str = ""
    scheduled_tasks: list[ScheduledTask] = field(default_factory=list)
    unscheduled_tasks: list[UnscheduledTask] = field(default_factory=list)

    def get_scheduled_tasks(self) -> list[ScheduledTask]:
        raise NotImplementedError

    def get_unscheduled_tasks(self) -> list[UnscheduledTask]:
        raise NotImplementedError

    def explain(self) -> str:
        raise NotImplementedError


class Scheduler:
    def generate_plan(
        self,
        owner: Owner,
        pet: Pet,
        tasks: list[CareTask],
        constraints: SchedulingConstraints,
    ) -> DailyPlan:
        raise NotImplementedError

    def rank_tasks(self, tasks: list[CareTask]) -> list[CareTask]:
        raise NotImplementedError

    def find_available_slot(
        self,
        task: CareTask,
        constraints: SchedulingConstraints,
        plan: DailyPlan,
    ) -> str:
        raise NotImplementedError

    def explain_selection(
        self,
        task: CareTask,
        constraints: SchedulingConstraints,
    ) -> str:
        raise NotImplementedError