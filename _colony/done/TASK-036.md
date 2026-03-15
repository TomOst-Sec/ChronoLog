# TASK-036: Rename project command

**Status:** review
**Assigned:** alpha
**Priority:** P2
**Depends-On:** TASK-001, TASK-003, TASK-004

## Description
Implement `chrono project rename OLD_NAME NEW_NAME` to rename a project. This updates the project name and all associated time entries. Currently there's no way to fix a typo in a project name.

## Acceptance Criteria
- [ ] `chrono project rename OLD NEW` renames a project
- [ ] Updates project name in the projects table
- [ ] Updates project field on all entries referencing the old name
- [ ] Error if old project doesn't exist
- [ ] Error if new name already exists
- [ ] Error if trying to rename "general" (protected project)
- [ ] New name validated (same rules as create)
- [ ] Function `rename_project(db_path, old: str, new: str) -> None` in core.py
- [ ] Tests: rename success, old not found, new exists, rename general, entries updated
- [ ] At least 5 test cases

## Notes
- Use a transaction to update both tables atomically
- This is a data-modifying operation — include confirmation prompt in CLI

**Claimed-By:** alpha-3
**Claimed-At:** 1773606247

**Completed-At:** 1773606357
