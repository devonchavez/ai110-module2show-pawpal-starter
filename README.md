# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

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

## Smart Scheduling

### Conflict Detection

#### `detect_conflicts` (line 210)
Checks a candidate task against all already-scheduled tasks for time overlap using `_tasks_overlap`. Returns a formatted warning string (including pet names if available) or `None`. Uses a closed-interval overlap check (`first_start < second_end && second_start < first_end`).

#### `detect_same_time_conflicts` (line 226)
Scans all pairs of scheduled tasks for identical start times. Generates distinct warning messages depending on whether the conflict is between two tasks for the same pet or two different pets.

> **Private helpers:** `_time_to_minutes` converts `"HH:MM"` strings to integer minutes, and `_tasks_overlap` uses those values plus `duration_minutes` to determine overlap — both support the two methods above.

---

### Scheduling

#### `schedule_for_pet` (line 322)
Combines three steps atomically: assigns the pet to the task, runs conflict detection, adds the task to both the pet and the scheduler. Returns any conflict warning to the caller.

#### `complete_task` (line 286)
Marks a task complete and, if `reschedule=True`, auto-generates the next recurring instance via `task.mark_complete()`, then adds it to both the pet and the scheduler.

---

### Filtering & Organization

#### `filter_tasks` (line 265)
Filters by completed status and/or `pet_name` (case-insensitive, strip-normalized). Both filters are optional and composable.

#### `organize_by_pet` (line 333)
Returns a `dict[str, List[Task]]` grouping tasks by pet name, with `"Unassigned"` as the fallback key for tasks without a pet.

#### `sort_tasks` (line 311)
Sorts in-place by `"time"`, `"frequency"`, or `"description"` based on the `sort_by` attribute set at construction. Defaults to time-based sort for unknown keys.

---

## Testing PawPal+

#### `test_sort_tasks_orders_by_time_chronologically` (`test_pawpal.py:169`)
Adds tasks at `17:00`, `07:30`, and `12:00` — intentionally out of order.
Calls `sort_tasks()` and asserts the resulting time list equals `["07:30", "12:00", "17:00"]`.
This was the only scenario with zero existing coverage.

#### `test_daily_task_complete_without_reschedule_creates_no_new_task` (`test_pawpal.py:183`)
Completes a daily task with `reschedule=False` and asserts `next_task` is `None` and the scheduler still holds exactly one task.
The existing recurrence test only covers `reschedule=True`. This covers the negative/opt-out path and guards against accidental rescheduling.

#### `test_scheduler_no_conflict_warning_when_tasks_at_different_times` (`test_pawpal.py:209`)
Schedules two tasks for the same pet at different times (`07:00` and `18:00`) and asserts `detect_same_time_conflicts()` returns an empty list.
The existing conflict tests only assert warnings are raised. This covers the happy path and prevents false positives from slipping through.

---

## Features

- **Chronological task sorting** — `sort_tasks()` orders the daily schedule by start time (HH:MM), keeping the most urgent tasks at the top. Also supports sorting by frequency or description.
- **Overlap-based conflict detection** — `detect_conflicts()` checks a new task against every already-scheduled task using a closed-interval overlap formula (`start_A < end_B && start_B < end_A`), so back-to-back tasks never falsely trigger a warning.
- **Same-time conflict scanning** — `detect_same_time_conflicts()` scans all scheduled task pairs for identical start times and generates distinct warnings for same-pet vs. cross-pet collisions.
- **Daily, weekly, and monthly recurrence** — `Task.mark_complete(reschedule=True)` automatically calculates the next due date and returns a ready-to-schedule copy; monthly recurrence handles month-length edge cases (e.g., Jan 31 → Feb 28).
- **Composable task filtering** — `filter_tasks()` accepts completion status and/or pet name (case-insensitive) as independent, stackable filters.
- **Pet-grouped task organization** — `organize_by_pet()` returns a `dict[pet_name → tasks]` for clear per-pet daily views, with `"Unassigned"` as the fallback bucket.
- **Atomic pet scheduling** — `schedule_for_pet()` assigns the pet, runs conflict detection, and registers the task in one call, so the scheduler is never in a partially-updated state.
- **Multi-owner, multi-pet data model** — `Owner → Pet → Task` hierarchy lets the app track tasks across multiple pets and surface all pending/completed work at any level.