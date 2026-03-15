# TASK-044: Add weekly report core logic and CLI command

**Status:** active
**Assigned:** alpha
**Priority:** P1
**Depends-On:** TASK-043

## Description
Implement `chrono report week` command. Shows a breakdown by project for the current week (Monday–Sunday). Each project shows total hours and percentage of total. Includes a bar chart visualization using Rich.

The `display.py` module has `create_summary_table()` which renders project/hours/percentage/bar — use it.

## Acceptance Criteria
- [ ] `report_weekly()` function in `core.py` returns per-project summaries for the current week
- [ ] Each summary dict has keys: `project`, `hours`, `percentage`
- [ ] `chrono report week` displays the summary table with bar chart
- [ ] Total hours shown at bottom
- [ ] Empty week shows a friendly message
- [ ] Tests exist for core function and CLI command
- [ ] `pytest` passes clean

## Notes
- Week starts Monday, ends Sunday
- Percentage = project hours / total hours * 100
- Use `display.create_summary_table()` for rendering
- Only include completed entries (end_time IS NOT NULL)

**Claimed-By:** alpha-2
**Claimed-At:** 1773608595
