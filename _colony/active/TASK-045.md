# TASK-045: Add date range report CLI command

**Status:** active
**Assigned:** alpha
**Priority:** P1
**Depends-On:** TASK-043

## Description
Implement `chrono report --from YYYY-MM-DD --to YYYY-MM-DD` for custom date range reports. Supports both a detail view (all entries) and a summary view (per-project breakdown).

## Acceptance Criteria
- [ ] `report_range()` function in `core.py` returns entries within a date range
- [ ] `report_range_summary()` in `core.py` returns per-project summaries for a range
- [ ] `chrono report --from 2024-01-01 --to 2024-01-31` shows daily detail view by default
- [ ] `chrono report --from ... --to ... --summary` shows project summary view
- [ ] Both `--from` and `--to` are required when used
- [ ] Invalid date format shows a clear error message
- [ ] Tests exist for core functions and CLI
- [ ] `pytest` passes clean

## Notes
- Reuse `display.create_entries_table()` for detail view
- Reuse `display.create_summary_table()` for summary view
- Date strings must be YYYY-MM-DD format
- Only include completed entries (end_time IS NOT NULL)

**Claimed-By:** alpha-2
**Claimed-At:** 1773608798
