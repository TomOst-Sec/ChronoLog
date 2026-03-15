# TASK-028: Resume last timer command

**Status:** review
**Assigned:** alpha
**Priority:** P2
**Depends-On:** TASK-001, TASK-003, TASK-005

## Description
Implement `chrono resume` — restart the most recently stopped timer with the same description, project, and tags. This is a convenience feature for users who work on the same task across breaks.

## Acceptance Criteria
- [ ] Function `resume_timer(db_path) -> TimeEntry` — finds the most recent completed entry and starts a new timer with the same description, project, and tags
- [ ] Raises error if no previous entries exist
- [ ] Raises error if a timer is already running
- [ ] `chrono resume` CLI command with Rich formatted confirmation output
- [ ] Output shows what was resumed: description, project, tags
- [ ] Tests: resume success, resume with no history, resume while running, verify copied fields
- [ ] At least 5 test cases

## Notes
- Query: SELECT * FROM entries WHERE end_time IS NOT NULL ORDER BY end_time DESC LIMIT 1
- Creates a brand new entry — does not modify the old one
- Reuses description, project, and tags from the last completed entry

**Claimed-By:** alpha-1
**Claimed-At:** 1773605914

**Completed-At:** 1773606009
