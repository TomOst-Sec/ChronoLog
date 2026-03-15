# TASK-024: Database indexing for query performance

**Status:** review
**Assigned:** alpha
**Priority:** P2
**Depends-On:** TASK-001, TASK-003

## Description
Add SQLite indexes to ensure query performance stays under 100ms even with 10,000+ entries (as required by GOALS.md constraints). The most frequent queries are: active timer lookup (NULL end_time), entries by date range, and entries by project.

## Acceptance Criteria
- [ ] Add index on `entries.end_time` for fast active timer lookup (WHERE end_time IS NULL)
- [ ] Add index on `entries.start_time` for date range queries
- [ ] Add index on `entries.project` for project-based filtering
- [ ] Add composite index on `entries(project, start_time)` for report queries
- [ ] Indexes created in `init_db()` using CREATE INDEX IF NOT EXISTS
- [ ] Performance test: insert 10,000 entries, verify key queries complete in <100ms
- [ ] Tests verifying indexes exist after init_db
- [ ] At least 4 test cases

## Notes
- Use `CREATE INDEX IF NOT EXISTS` for idempotency
- The performance test can use `time.perf_counter()` to measure query time
- SQLite indexes are lightweight — don't worry about over-indexing

**Claimed-By:** alpha-1
**Claimed-At:** 1773605816

**Completed-At:** 1773605891
