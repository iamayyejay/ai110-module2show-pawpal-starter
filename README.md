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

## 📐 Smarter Scheduling

Example:
**| Feature |**
- `Methods`  
Notes 

------------------------------------------------------------------------------------

**| Task sorting |**
- `Scheduler.sort_by_time()`
- `Scheduler.organize_tasks()`
Orders tasks by time; untimed tasks come last. The organized list excludes      completed tasks and uses priority to break time ties. 

**| Task filtering |**
- `Scheduler.filter_tasks()`
- `Scheduler.get_pending_tasks()`
Filter by pet name (case-insensitive) and/or completion status; pending tasks exclude completed tasks. 

**| Conflict detection |** 
- `Scheduler.find_conflicts()`
- `Scheduler.get_conflict_warnings()` 
Warns when task intervals overlap on the same date. Completed and untimed tasks are ignored. 

**| Recurring tasks |** 
- `Task.create_next_occurrence()`
- `Scheduler.mark_task_complete()` 
Completing daily or weekly tasks creates an incomplete occurrence due 1 or 7 days later. Other frequencies do not repeat automatically. 

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
