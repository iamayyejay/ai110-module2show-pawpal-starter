from datetime import date, time

from pawpal_system import Owner, Pet, Scheduler, Task


def test_mark_complete_updates_task_status() -> None:
    task = Task(description="Morning walk")

    task.mark_complete()

    assert task.is_completed is True


def test_adding_task_increases_pet_task_count() -> None:
    pet = Pet(name="Mochi", species="cat")
    task = Task(description="Breakfast")

    pet.add_task(task)

    assert len(pet.tasks) == 1
    assert pet.tasks[0] is task


def test_sort_by_time_orders_tasks_and_places_missing_times_last() -> None:
    late_task = Task(description="Evening walk", time=time(18, 0))
    untimed_task = Task(description="Flexible play")
    early_task = Task(description="Breakfast", time=time(7, 30))

    sorted_tasks = Scheduler().sort_by_time([late_task, untimed_task, early_task])

    assert sorted_tasks == [early_task, late_task, untimed_task]


def test_filter_tasks_by_completion_status() -> None:
    pet = Pet(name="Mochi", species="cat")
    pending_task = Task(description="Breakfast")
    completed_task = Task(description="Medication", is_completed=True)
    pet.add_task(pending_task)
    pet.add_task(completed_task)
    owner = Owner(name="Jordan", pets=[pet])

    result = Scheduler().filter_tasks(owner, is_completed=True)

    assert result == [completed_task]


def test_filter_tasks_by_pet_name_and_completion_status() -> None:
    cat = Pet(name="Mochi", species="cat")
    dog = Pet(name="Biscuit", species="dog")
    cat_task = Task(description="Breakfast")
    dog_task = Task(description="Walk")
    completed_cat_task = Task(description="Medication", is_completed=True)
    cat.add_task(cat_task)
    cat.add_task(completed_cat_task)
    dog.add_task(dog_task)
    owner = Owner(name="Jordan", pets=[cat, dog])

    result = Scheduler().filter_tasks(
        owner,
        is_completed=False,
        pet_name="mochi",
    )

    assert result == [cat_task]


def test_completing_daily_task_adds_next_day_occurrence_to_same_pet() -> None:
    pet = Pet(name="Mochi", species="cat")
    task = Task(description="Breakfast", frequency="daily", time=time(8))
    pet.add_task(task)
    owner = Owner(name="Jordan", pets=[pet])

    Scheduler().mark_task_complete(owner, task, completed_on=date(2026, 10, 8))

    next_task = pet.tasks[1]
    assert task.is_completed is True
    assert next_task is not task
    assert next_task.description == task.description
    assert next_task.frequency == task.frequency
    assert next_task.time == task.time
    assert next_task.due_date == date(2026, 10, 9)
    assert next_task.is_completed is False


def test_completing_weekly_task_adds_occurrence_seven_days_later() -> None:
    pet = Pet(name="Biscuit", species="dog")
    task = Task(description="Grooming", frequency="weekly")
    pet.add_task(task)
    owner = Owner(name="Jordan", pets=[pet])

    Scheduler().mark_task_complete(owner, task, completed_on=date(2026, 10, 8))

    assert pet.tasks[1].due_date == date(2026, 10, 15)


def test_completing_one_time_task_does_not_create_occurrence() -> None:
    pet = Pet(name="Mochi", species="cat")
    task = Task(description="Vet visit", frequency="one-time")
    pet.add_task(task)
    owner = Owner(name="Jordan", pets=[pet])

    Scheduler().mark_task_complete(owner, task, completed_on=date(2026, 10, 8))

    assert task.is_completed is True
    assert pet.tasks == [task]


def test_completing_task_twice_does_not_create_duplicate_occurrences() -> None:
    pet = Pet(name="Mochi", species="cat")
    task = Task(description="Breakfast", frequency="daily")
    pet.add_task(task)
    owner = Owner(name="Jordan", pets=[pet])
    scheduler = Scheduler()

    scheduler.mark_task_complete(owner, task, completed_on=date(2026, 10, 8))
    scheduler.mark_task_complete(owner, task, completed_on=date(2026, 10, 8))

    assert len(pet.tasks) == 2


def test_find_conflicts_detects_overlapping_tasks_for_same_pet() -> None:
    pet = Pet(name="Mochi", species="cat")
    first = Task(
        description="Breakfast",
        time=time(8),
        duration_minutes=30,
        due_date=date(2026, 10, 8),
    )
    overlapping = Task(
        description="Medication",
        time=time(8, 15),
        duration_minutes=10,
        due_date=date(2026, 10, 8),
    )
    pet.tasks.extend([first, overlapping])
    owner = Owner(name="Jordan", pets=[pet])

    conflicts = Scheduler().find_conflicts(owner)

    assert len(conflicts) == 1
    assert conflicts[0].first_pet is pet
    assert conflicts[0].first_task is first
    assert conflicts[0].second_pet is pet
    assert conflicts[0].second_task is overlapping


def test_find_conflicts_detects_same_time_across_different_pets() -> None:
    cat = Pet(name="Mochi", species="cat")
    dog = Pet(name="Biscuit", species="dog")
    cat_task = Task(
        description="Breakfast",
        time=time(8),
        due_date=date(2026, 10, 8),
    )
    dog_task = Task(
        description="Walk",
        time=time(8),
        due_date=date(2026, 10, 8),
    )
    cat.tasks.append(cat_task)
    dog.tasks.append(dog_task)
    owner = Owner(name="Jordan", pets=[cat, dog])

    conflicts = Scheduler().find_conflicts(owner)

    assert len(conflicts) == 1
    assert conflicts[0].first_pet is cat
    assert conflicts[0].second_pet is dog


def test_find_conflicts_ignores_adjacent_completed_and_untimed_tasks() -> None:
    pet = Pet(name="Mochi", species="cat")
    pet.tasks.extend([
        Task(
            description="Breakfast",
            time=time(8),
            duration_minutes=30,
            due_date=date(2026, 10, 8),
        ),
        Task(
            description="Medication",
            time=time(8, 30),
            duration_minutes=10,
            due_date=date(2026, 10, 8),
        ),
        Task(
            description="Old task",
            time=time(8, 15),
            due_date=date(2026, 10, 8),
            is_completed=True,
        ),
        Task(description="No scheduled time"),
    ])
    owner = Owner(name="Jordan", pets=[pet])

    assert Scheduler().find_conflicts(owner) == []


def test_conflict_warnings_return_messages_and_empty_list_without_conflicts() -> None:
    pet = Pet(name="Mochi", species="cat")
    pet.tasks.extend([
        Task(
            description="Breakfast",
            time=time(8),
            duration_minutes=30,
            due_date=date(2026, 10, 8),
        ),
        Task(
            description="Medication",
            time=time(8, 15),
            duration_minutes=10,
            due_date=date(2026, 10, 8),
        ),
    ])
    owner = Owner(name="Jordan", pets=[pet])
    scheduler = Scheduler()

    warnings = scheduler.get_conflict_warnings(owner)

    assert warnings == [
        "Mochi: 'Breakfast' overlaps Mochi: 'Medication'."
    ]
    pet.tasks[1].time = time(8, 30)
    assert scheduler.get_conflict_warnings(owner) == []