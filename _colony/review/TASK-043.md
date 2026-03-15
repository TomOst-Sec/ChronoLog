# TASK-043: Add daily report core logic and CLI command

**Status:** review
**Assigned:** alpha
**Priority:** P1
**Depends-On:** none

## Description
Implement `chrono report today` and `chrono report yesterday` commands. The core logic must query entries for the specified day, and the CLI must display them in a Rich table showing: start time, end time, duration, project, tags, description, with total hours at the bottom.

The `display.py` module already has `create_entries_table()` and `add_total_row()` helpers — use them.

## Acceptance Criteria
- [ ] `report_daily()` function in `core.py` returns entries for a given date
- [ ] `chrono report today` displays today's entries in a Rich table
- [ ] `chrono report yesterday` displays yesterday's entries
- [ ] Total hours shown at bottom of table
- [ ] Empty result shows a friendly "No entries for <date>" message
- [ ] Tests exist for the core function and CLI command
- [ ] `pytest` passes clean (all tests, no warnings)

## Notes
- Times stored in UTC, display in local timezone
- Use `display.create_entries_table()` for the Rich table
- `report` should be a Click group with subcommands
- The `--db` hidden option pattern is used throughout cli.py for testability

**Claimed-By:** alpha-1
**Claimed-At:** 1773608233

**Completed-At:** 1773608431
