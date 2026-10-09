# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- **Briefly describe your initial UML design.**
- **What classes did you include, and what responsibilities did you assign to each?** 

The classes I included are Owner to store owner details and scheduling        preferences, Pet to store pet information and its care tasks, and CareTask to represent activities such as walks, feeding, and medication, including duration and priority. SchedulingConstraints captures the time available and preferences the schedule should respect. Scheduler is responsible for ranking tasks and building a plan. DailyPlan holds the result, with ScheduledTask entries for tasks that fit and UnscheduledTask entries explaining what could not be scheduled. TaskType and Priority define the available task categories and priority levels.

**b. Design changes**

- **Did your design change during implementation?**
- **If yes, describe at least one change and why you made it.**

The initial UML included a broader planning design with scheduling constraints and daily plan objects. During implementation, I narrowed the code to the requested `Task`, `Pet`, `Owner`, and `Scheduler` classes. `Owner.get_all_tasks()` now gathers tasks across pets, and the scheduler organizes those tasks without relying on a single pet.


---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- **What constraints does your scheduler consider (for example: time, priority, preferences)?**
- **How did you decide which constraints mattered most?**

The scheduler filters out completed tasks and orders the remaining tasks by scheduled time, using priority to break ties when tasks have the same time. I prioritized scheduled time because it gives tasks a clear place in the day, then used priority to decide which task comes first when times conflict. Frequency is stored on each task but isn’t used by the scheduler yet, and owner preferences aren’t currently implemented.

**b. Tradeoffs**

- **Describe one tradeoff your scheduler makes.**
- **Why is that tradeoff reasonable for this scenario?**

The scheduler prioritizes each task’s scheduled time over its priority, using priority only to break ties. This keeps tasks at the times the owner assigned, making the schedule easy to follow. The tradeoff is that a high-priority task won’t move ahead of an earlier low-priority task; handling that would require more scheduling rules.
---

## 3. AI Collaboration

**a. How you used AI**

- **How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?**

I used AI to brainstorm the UML, create and refine the Python class skeleton, implement multi-pet task management, draft tests, and update the README and reflection. 

- **What kinds of prompts or questions were most helpful?**

The most helpful prompts were specific about responsibilities and requirements—for example, asking how Scheduler should retrieve tasks across all of an Owner’s pets, and requesting focused tests for task completion and addition. I verified generated code by running the tests and sample script.

**b. Judgment and verification**

- **Describe one moment where you did not accept an AI suggestion as-is.**
- **How did you evaluate or verify what the AI suggested?**

AI suggested reducing duplicated task sources, using explicit time values, deriving totals instead of storing them separately, and representing a task that cannot fit into a schedule. I accepted the multi-pet ownership idea by making each pet's task list the source of truth and having `Owner.get_all_tasks()` supply tasks to `Scheduler`. I also kept task times typed as `datetime.time` and used completion and priority fields to support organizing tasks. I did not carry over the full constraints, slot-finding, and daily-plan system into the final implementation; I kept the scope to the four requested classes, so scheduling across availability windows remains future work.

I verified the result by running the two pytest tests for task completion and task addition (both passed), checking Python syntax and Pylance diagnostics, and running `main.py` to confirm that tasks for two pets printed in time order. I also ran a focused multi-pet check to confirm that the scheduler retrieves tasks through the owner's `get_all_tasks()` method.

---

## 4. Testing and Verification

**a. What you tested**

- **What behaviors did you test?**
- **Why were these tests important?**

I tested that mark_complete() changes a task’s completion status and that adding a task increases the pet’s task count. These tests check two important basics: tasks can be marked done, and they can be assigned to pets. I also ran the sample schedule and a focused check that the scheduler retrieves and organizes tasks across multiple pets.

**b. Confidence**

- **How confident are you that your scheduler works correctly?**
- **What edge cases would you test next if you had more time?**

I’m confident these basic behaviors work, but the tests don’t cover the scheduler comprehensively. Next, I’d add tests for empty owners, completed tasks being excluded, tasks with equal or missing times, priority tie-breaking, duplicate tasks, and attempts to add or complete tasks for pets or owners they don’t belong to.
---

## 5. Reflection

**a. What went well**

- **What part of this project are you most satisfied with?**

I’m most satisfied that the scheduler handles tasks across multiple pets through the owner, rather than being limited to one pet. The sample app also makes the schedule easy to see in the terminal.

**b. What you would improve**

- **If you had another iteration, what would you improve or redesign?**

I’d connect the scheduling logic to the Streamlit UI and add support for availability windows and owner preferences. I’d also expand the tests to cover ordering, completed tasks, and invalid ownership.

**c. Key takeaway**

- **What is one important thing you learned about designing systems or working with AI on this project?**

I learned that clear relationships between classes—especially having Owner provide all pets’ tasks—make the system easier to extend. AI suggestions were useful, but I needed to check that they fit the final project scope and verify the behavior with tests and a sample run.
