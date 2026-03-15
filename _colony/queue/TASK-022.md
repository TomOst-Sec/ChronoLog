# TASK-022: BUG — Project.from_row missing, 6 tests failing

**Status:** queue
**Assigned:** alpha
**Priority:** P0
**Depends-On:** TASK-002, TASK-004

## Description
`chronolog/core.py` calls `Project.from_row(row)` in `list_projects()` and `get_project()`, but the `Project` dataclass in `chronolog/models.py` does not have a `from_row` class method. `TimeEntry` has `from_row` but `Project` does not.

## Acceptance Criteria
- [ ] `Project` model in `chronolog/models.py` has a `from_row(cls, row)` classmethod that constructs a Project from a sqlite3.Row
- [ ] All 6 failing tests in `tests/test_core.py` pass: TestListProjects (4), TestArchiveProject (1), TestGetProject (1)
- [ ] No regressions in other tests

## Notes
- Filed by alpha-3 during TASK-018 baseline check
- `TimeEntry.from_row` exists and works — `Project.from_row` just needs the same pattern
- Likely a merge gap between TASK-002 (models) and TASK-004 (core CRUD)
