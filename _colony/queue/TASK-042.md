# TASK-042: Interactive timer selection for multi-project workflows

**Status:** queue
**Assigned:** alpha
**Priority:** P2
**Depends-On:** TASK-001, TASK-003

## Description
Add `chrono switch "new task" --project NAME` that stops the current timer and immediately starts a new one. This is a convenience for users who switch between tasks frequently. Equivalent to `chrono stop && chrono start`.

## Acceptance Criteria
- [ ] `chrono switch "description" --project NAME --tags tags` stops active timer and starts new one atomically
- [ ] If no timer is running, just starts the new one (same as `chrono start`)
- [ ] Shows summary of stopped timer and confirmation of new timer
- [ ] Core function `switch_timer(db_path, description, project, tags) -> tuple[TimeEntry|None, TimeEntry]` returns (stopped, started)
- [ ] Uses a transaction for atomicity
- [ ] Tests: switch with active timer, switch with no timer, verify both entries
- [ ] At least 4 test cases

## Notes
- This is basically `stop_timer()` + `start_timer()` in one command
- Important: if start fails (bad project), the stop should also be rolled back
- Show both the stopped entry summary and new entry confirmation
