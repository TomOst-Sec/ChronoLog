# TASK-002: Data models for entries and projects

**Status:** active
**Assigned:** bravo
**Priority:** P0
**Depends-On:** TASK-001

## Description
Define the core data models in `chronolog/models.py`. These are plain Python dataclasses representing time entries and projects. They should handle serialization to/from database rows and include validation logic.

## Acceptance Criteria
- [ ] `TimeEntry` dataclass with fields: `id` (int|None), `description` (str), `project` (str), `tags` (list[str]), `start_time` (datetime in UTC), `end_time` (datetime|None in UTC)
- [ ] `TimeEntry` has a `duration` property that returns timedelta (or None if still running)
- [ ] `TimeEntry` has a `duration_minutes` property that returns float
- [ ] `TimeEntry` has a `to_row()` method that converts to a dict suitable for DB insertion (tags as comma-separated string)
- [ ] `TimeEntry` has a `from_row()` classmethod that constructs from a DB row dict (parsing tags string back to list)
- [ ] `Project` dataclass with fields: `name` (str), `created_at` (datetime), `archived` (bool, default False)
- [ ] All datetimes are stored as UTC (timezone-aware)
- [ ] Tests in `tests/test_models.py` covering: creation, duration calculation, to_row/from_row round-trip, tags serialization, running entry (no end_time)
- [ ] At least 8 test cases

## Notes
- Use `dataclasses` from stdlib, not pydantic
- Tags are stored as comma-separated string in DB but list[str] in Python
- Times must be timezone-aware UTC datetimes (use `datetime.timezone.utc`)

**Claimed-By:** bravo-1
**Claimed-At:** 1773605074
