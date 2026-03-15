# TASK-005: Timer start/stop core logic

**Status:** active
**Assigned:** bravo
**Priority:** P0
**Depends-On:** TASK-001, TASK-003

## Description
Implement the core timer functions in `chronolog/core.py`: start a timer, stop the running timer, and get the status of the current timer. These are the most important functions in ChronoLog — the primary user workflow.

## Acceptance Criteria
- [ ] Function `start_timer(db_path, description: str, project: str = "general", tags: list[str] | None = None) -> TimeEntry` — inserts a new entry with start_time=now(UTC) and end_time=None
- [ ] `start_timer` raises an error if there is already a running timer (entry with end_time=None)
- [ ] `start_timer` raises an error if the specified project doesn't exist
- [ ] Function `stop_timer(db_path) -> TimeEntry` — sets end_time=now(UTC) on the running entry, returns the completed entry
- [ ] `stop_timer` raises an error if no timer is currently running
- [ ] Function `get_active_timer(db_path) -> TimeEntry | None` — returns the currently running entry or None
- [ ] All datetimes are UTC
- [ ] Tests in `tests/test_core.py` covering: start, start with project/tags, start while running, stop, stop with nothing running, get_active_timer when running, get_active_timer when idle
- [ ] At least 8 test cases

## Notes
- Use `datetime.now(datetime.timezone.utc)` for current time
- Only one timer can be active at a time (enforced by checking for NULL end_time)
- Import TimeEntry from models.py and db functions from TASK-003
- Tags should be stored as comma-separated string in the DB

**Claimed-By:** bravo-1
**Claimed-At:** 1773605208
