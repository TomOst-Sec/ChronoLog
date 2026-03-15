# TASK-017: Custom date range report

**Status:** review
**Assigned:** bravo
**Priority:** P1
**Depends-On:** TASK-001, TASK-003

## Description
Implement `chrono report --from DATE --to DATE` for custom date ranges. Supports both a daily detail view and a project summary view. Feature 6 from GOALS.md (M2).

## Acceptance Criteria
- [ ] `chrono report --from 2024-01-01 --to 2024-01-31` shows entries in range
- [ ] Default view: daily detail (same format as today/yesterday report)
- [ ] `--summary` flag: shows project breakdown (same format as weekly report)
- [ ] `--from` and `--to` accept YYYY-MM-DD format
- [ ] `--from` without `--to` defaults to today
- [ ] `--to` without `--from` shows error
- [ ] Core function `get_entries_for_range(db_path, from_date, to_date) -> list[TimeEntry]`
- [ ] Core function `get_range_summary(db_path, from_date, to_date) -> list[dict]`
- [ ] Date validation: from_date must be <= to_date
- [ ] Tests: valid range, invalid range, summary mode, missing dates
- [ ] At least 6 test cases

## Notes
- Parse date strings with `datetime.strptime(s, "%Y-%m-%d").date()`
- Reuse display logic from daily/weekly reports where possible
- M2 scope

**Claimed-By:** bravo-2
**Claimed-At:** 1773605642

**Completed-At:** 1773605812
