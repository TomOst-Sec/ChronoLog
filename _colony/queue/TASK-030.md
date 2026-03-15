# TASK-030: Cancel running timer command

**Status:** queue
**Assigned:** alpha
**Priority:** P2
**Depends-On:** TASK-001, TASK-003, TASK-005

## Description
Implement `chrono cancel` — discard the currently running timer without saving it. Unlike `chrono stop` which saves the entry, cancel deletes it entirely. Useful when you accidentally start a timer or start tracking the wrong task.

## Acceptance Criteria
- [ ] Function `cancel_timer(db_path) -> TimeEntry` — deletes the active entry (end_time IS NULL), returns the deleted entry for confirmation
- [ ] Raises error if no timer is running
- [ ] `chrono cancel` CLI command with confirmation prompt (click.confirm)
- [ ] `chrono cancel --yes` skips confirmation
- [ ] Output shows what was cancelled (description, project, elapsed time)
- [ ] Tests: cancel running timer, cancel with nothing running, verify entry is deleted
- [ ] At least 4 test cases

## Notes
- DELETE FROM entries WHERE end_time IS NULL
- Should only ever be 0 or 1 active timers — assert this
- Show elapsed time before deletion so user knows what they're discarding
