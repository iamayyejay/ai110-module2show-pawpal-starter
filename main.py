"""Run a sample multi-pet PawPal+ daily schedule."""

from datetime import time

from pawpal_system import Owner, Pet, Scheduler, Task


def main() -> None:
    """Build and print the sample multi-pet schedule with conflict warnings."""
    owner = Owner(name="Jordan")
    dog = Pet(name="Biscuit", species="dog")
    cat = Pet(name="Mochi", species="cat")
    owner.add_pet(dog)
    owner.add_pet(cat)

    scheduler = Scheduler()
    dog.add_task(Task(description="Evening walk", time=time(18, 0)))
    cat.add_task(Task(description="Breakfast", time=time(8, 0), duration_minutes=10))
    dog.add_task(Task(description="Morning walk", time=time(7, 30)))
    cat.add_task(Task(description="Morning feeding", time=time(7, 30)))

    print("Today's Schedule")
    for warning in scheduler.get_conflict_warnings(owner):
        print(f"Warning: {warning}")

    for task in scheduler.organize_tasks(owner):
        pet = next(pet for pet in owner.pets if task in pet.tasks)
        task_time = task.time.strftime("%I:%M %p") if task.time else "Unscheduled"
        print(f"{task_time} - {pet.name}: {task.description}")


if __name__ == "__main__":
    main()