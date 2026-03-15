# TASK-033: Pomodoro-style timer with duration limit

**Status:** review
**Assigned:** alpha
**Priority:** P2
**Depends-On:** TASK-001, TASK-003, TASK-005

## Description
Add an optional duration limit to timers. `chrono start --for 25m` starts a timer that auto-stops after 25 minutes. Useful for Pomodoro technique or timeboxed work sessions.

## Acceptance Criteria
- [ ] `chrono start "task" --for DURATION` accepts duration strings: "25m", "1h", "1h30m", "90m"
- [ ] Function `parse_duration_string(s: str) -> timedelta` in utils.py
- [ ] When `--for` is set, the entry stores a `planned_duration` (store as minutes in a new column or in notes)
- [ ] `chrono status` shows remaining time when a duration limit is set
- [ ] Timer does NOT auto-stop (CLI is not a daemon) — but status shows "overtime" if past limit
- [ ] Tests: parse duration strings, status with limit, status overtime
- [ ] At least 5 test cases

## Notes
- Parse with regex: `(\d+)h|(\d+)m` patterns
- Since CLI can't run as daemon, auto-stop isn't possible. Just show warning in status.
- Store planned_end_time or planned_minutes in the entry
- Nice-to-have feature beyond core GOALS.md scope

**Claimed-By:** alpha-2
**Claimed-At:** 1773606079

**Completed-At:** 1773606225
