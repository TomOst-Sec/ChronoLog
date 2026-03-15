# TASK-019: Rich report formatting helpers

**Status:** queue
**Assigned:** bravo
**Priority:** P2
**Depends-On:** TASK-001, TASK-008

## Description
Create reusable Rich formatting helpers for report output. Multiple report commands (daily, weekly, range) need consistent table styling, duration formatting, and summary rows. Centralizing this prevents duplication across TASK-015, 016, 017.

## Acceptance Criteria
- [ ] Module or section in `chronolog/utils.py` (or new `chronolog/display.py`) with report formatting helpers
- [ ] Function `create_entries_table(entries: list[TimeEntry]) -> Table` — creates a Rich Table with standard columns (Start, End, Duration, Project, Tags, Description)
- [ ] Function `create_summary_table(summaries: list[dict]) -> Table` — creates a Rich Table for project summaries (Project, Hours, Percentage, Bar)
- [ ] Function `format_report_header(title: str, date_range: str) -> Panel` — creates a Rich Panel header for reports
- [ ] Function `add_total_row(table: Table, total_minutes: float) -> None` — adds a total row at the bottom
- [ ] All functions have type hints and docstrings
- [ ] Tests in `tests/test_display.py` or `tests/test_utils.py` verifying table creation and formatting
- [ ] At least 5 test cases

## Notes
- Use Rich Table, Panel, and Bar components
- Keep it simple — these are display helpers, not business logic
- Color scheme: green for running entries, default for completed, bold for totals
