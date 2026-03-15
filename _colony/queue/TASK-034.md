# TASK-034: Project statistics and summary command

**Status:** queue
**Assigned:** bravo
**Priority:** P2
**Depends-On:** TASK-001, TASK-003

## Description
Implement `chrono project stats NAME` showing detailed statistics for a project: total hours, entry count, average session duration, most common tags, date of first/last entry. Useful for understanding time investment per project.

## Acceptance Criteria
- [ ] `chrono project stats NAME` displays project statistics in a Rich panel
- [ ] Stats shown: total hours, total entries, average duration per entry, longest session, shortest session
- [ ] Most used tags (top 5) for entries in that project
- [ ] Date range: first entry date to most recent entry date
- [ ] Error message if project doesn't exist or has no entries
- [ ] Function `get_project_stats(db_path, project: str) -> dict` in core.py
- [ ] Tests: project with entries, project with no entries, non-existent project, stats accuracy
- [ ] At least 5 test cases

## Notes
- Use SQL aggregations (SUM, COUNT, AVG, MIN, MAX) for efficiency
- Display using Rich Panel or Table
- This extends the `chrono project` subgroup from TASK-007
