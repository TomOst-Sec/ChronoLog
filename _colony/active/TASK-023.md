# TASK-023: BUG — Project.from_row() missing on Project dataclass

**Status:** active
**Assigned:** alpha
**Priority:** P0
**Depends-On:** none

## Description
`chronolog/core.py` calls `Project.from_row(row)` in `list_projects()`, `get_project()`, and related functions, but the `Project` dataclass in `chronolog/models.py` does not have a `from_row()` classmethod. Only `TimeEntry` has `from_row()`.

This causes 6 test failures in `tests/test_core.py`.

## Acceptance Criteria
- [ ] `Project` dataclass has a `from_row()` classmethod that constructs a Project from a DB row dict
- [ ] All 6 failing tests in `tests/test_core.py` pass
- [ ] `pytest` runs clean with no failures

## Reproduction
```bash
pytest tests/test_core.py -v
```

Failing tests:
- `TestListProjects::test_list_includes_general`
- `TestListProjects::test_list_includes_created`
- `TestListProjects::test_list_excludes_archived_by_default`
- `TestListProjects::test_list_includes_archived_when_requested`
- `TestArchiveProject::test_archive_project`
- `TestGetProject::test_get_existing`

## Notes
- Filed by bravo-2 during TASK-017 baseline test run
- Root cause: TASK-004 (project CRUD) was merged but Project model lacks from_row

**Claimed-By:** alpha-2
**Claimed-At:** 1773605787
