# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## UML Class Diagram

The initial class design for owners, pets, care tasks, scheduling constraints, and explained daily plans is in [`diagrams/uml.mmd`](diagrams/uml.mmd). It is a conceptual design to guide implementation and should be updated to match the finished app.

## Implementation Summary

The current Python implementation models care activities as `Task` objects, which store a description, scheduled time, due date, frequency, completion status, duration, and priority. Each `Pet` stores its details and tasks, while `Owner` manages multiple pets and provides `get_all_tasks()` to collect their tasks. `Scheduler` uses that owner method to retrieve tasks across pets, filter out completed tasks, and organize the remaining tasks by time and priority. Completing an owned daily or weekly task through the scheduler adds its next occurrence to the same pet. It can also add tasks to the owner's pets. The sample `main.py` demonstrates a multi-pet schedule in the terminal.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Paste a sample of your app's CLI or Streamlit output here so a reader can see what a generated plan looks like:

Today's Schedule
07:30 AM - Biscuit: Morning walk
08:00 AM - Mochi: Breakfast
06:00 PM - Biscuit: Evening walk

## 🧪 Testing PawPal+

Run the test suite from the project root:

```bash
python -m pytest
```

The tests cover task completion and addition, chronological sorting, task filtering, daily and weekly recurrence, non-recurring tasks, duplicate completion handling, and conflict detection and warnings for overlapping tasks.

Successful terminal output:

```text
============================= test session starts =============================
platform win32 -- Python 3.11.9, pytest-9.1.1, pluggy-1.6.0
rootdir: C:\Users\inthe\Desktop\CodePath\AI110\ai110-module2show-pawpal-starter
plugins: anyio-4.15.1
collected 13 items

tests\test_pawpal.py .............                                       [100%]

============================= 13 passed in 0.04s ==============================
```

Based on the test results I have a Confidence Level of 5 in the systems reliability.


## Features

| Feature | Methods | Notes |
|---|---|---|
| Multi-pet task tracking | `Owner.add_pet()`, `Owner.get_all_tasks()`, `Pet.add_task()`, `Scheduler.add_task()` | Stores care tasks under each pet and lets the scheduler retrieve or add tasks for an owner's pets. |
| Schedule sorting | `Scheduler.sort_by_time()`, `Scheduler.organize_tasks()` | `sort_by_time()` orders tasks chronologically and puts tasks without a time last. `organize_tasks()` excludes completed tasks, orders pending tasks by time, and uses higher priority to break same-time ties. |
| Task filtering | `Scheduler.filter_tasks()`, `Scheduler.get_pending_tasks()` | Filters by optional completion status and pet name; pet-name matching is case-insensitive. The pending-task method returns incomplete tasks across the owner's pets. |
| Conflict warnings | `Scheduler.find_conflicts()`, `Scheduler.get_conflict_warnings()` | Detects overlapping task intervals on the same due date, including tasks for different pets. Completed and untimed tasks are ignored; intervals that only touch at an endpoint are not considered conflicts. Conflicts are returned as records and formatted as warning messages. |
| Recurring tasks | `Task.create_next_occurrence()`, `Scheduler.mark_task_complete()` | Completing a daily task creates an incomplete occurrence due one day later; weekly recurrence is due seven days later. Other frequencies do not recur automatically, and completing the same task again does not create a duplicate occurrence. |
| Streamlit schedule display | `app.py` | The UI lets users enter an owner name, add pets and care tasks, view a time-sorted pending schedule, see conflict warnings, and filter the task list by pet and completion status. |

The current scheduler organizes tasks using their scheduled times, durations, priorities, and recurrence settings. It does not yet optimize around owner availability or preferences, or explain why it selected a particular plan.

## 📸 Demo Walkthrough

### Using the Streamlit app

Start the app from the project root:

```bash
streamlit run app.py
```

1. Enter or update the owner name, then add a pet by entering its name, choosing a species, and selecting **Add pet**.
2. In **Add a care task**, select a pet and enter a task description, time, frequency, duration, and priority. Select **Schedule task** to add it.
3. Review **Today's Schedule**. It lists pending tasks ordered by scheduled time, with untimed tasks last; when tasks share a time, higher-priority tasks come first. The app shows conflict warnings when scheduled task intervals overlap on the same due date.
4. Use **All Care Tasks** to view task details and filter the list by pet and completion status. Task times are sorted chronologically, with untimed tasks last.
5. The scheduler can also create the next daily or weekly occurrence when a task is marked complete through its Python API. The current Streamlit UI does not include a control for marking tasks complete.

### Sample CLI output

Run the sample multi-pet schedule from the project root:

```bash
python main.py
```

Output:

```text
Today's Schedule
Warning: Biscuit: 'Morning walk' overlaps Mochi: 'Morning feeding'.
07:30 AM - Biscuit: Morning walk
07:30 AM - Mochi: Morning feeding
08:00 AM - Mochi: Breakfast
06:00 PM - Biscuit: Evening walk
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
