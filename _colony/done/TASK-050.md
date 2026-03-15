# TASK-050: Adopt custom exceptions in core.py

**Status:** done
**Assigned:** alpha
**Priority:** P2
**Depends-On:** none

## Description
`chronolog/exceptions.py` defines custom exceptions (TimerAlreadyRunningError, NoActiveTimerError, ProjectNotFoundError, etc.) but `core.py` still raises generic RuntimeError and ValueError. Refactor core.py to use the custom exceptions, and update CLI error handling to catch them.

## Acceptance Criteria
- [ ] `start_timer()` raises `TimerAlreadyRunningError` instead of `RuntimeError`
- [ ] `start_timer()` raises `ProjectNotFoundError` instead of `RuntimeError` for missing project
- [ ] `stop_timer()` raises `NoActiveTimerError` instead of `RuntimeError`
- [ ] `create_project()` raises `InvalidProjectNameError` instead of `ValueError` for bad names
- [ ] `create_project()` raises `ProjectExistsError` instead of `ValueError` for duplicates
- [ ] `archive_project()` raises `ProjectNotFoundError` instead of `ValueError`
- [ ] `edit_entry()` raises `EntryNotFoundError` instead of `RuntimeError`
- [ ] `delete_entry()` raises `EntryNotFoundError` instead of `RuntimeError`
- [ ] CLI commands catch `ChronoLogError` (base class) for consistent error handling
- [ ] All existing tests updated to expect new exception types
- [ ] `pytest` passes clean

## Notes
- All custom exceptions inherit from `ChronoLogError` which has a `.message` attribute
- CLI can catch `ChronoLogError` and print `.message` — simplifies error handling
- This is a refactor — no new behavior, just better exception types

**Claimed-By:** alpha-3
**Claimed-At:** 1773608292

**Completed-At:** 1773608647
