# TASK-004: Project management CRUD operations

**Status:** review
**Assigned:** alpha
**Priority:** P1
**Depends-On:** TASK-001, TASK-003

## Description
Implement project management functions in `chronolog/core.py`: create, list, and archive projects. These are the core business logic functions that the CLI will call. Each function takes a db connection/path and operates on the `projects` table.

## Acceptance Criteria
- [ ] Function `create_project(db_path, name: str) -> Project` — creates a new project, raises error if name already exists
- [ ] Function `list_projects(db_path, include_archived: bool = False) -> list[Project]` — returns all projects, optionally including archived ones
- [ ] Function `archive_project(db_path, name: str) -> None` — marks a project as archived, raises error if project doesn't exist or is already archived
- [ ] Function `get_project(db_path, name: str) -> Project | None` — returns a single project by name or None
- [ ] Project names are validated: non-empty, alphanumeric plus hyphens, max 50 chars
- [ ] Cannot archive the "general" project (raise an error)
- [ ] Tests in `tests/test_core.py` covering: create, duplicate create, list, list with archived filter, archive, archive non-existent, archive general, project name validation
- [ ] At least 8 test cases

## Notes
- Import db functions from wherever TASK-003 puts them
- Import Project model from models.py (TASK-002)
- Use the `get_connection` / `init_db` functions from TASK-003
- All functions should init_db before operating (idempotent)

**Claimed-By:** alpha-1
**Claimed-At:** 1773605145

**Completed-At:** 1773605268
