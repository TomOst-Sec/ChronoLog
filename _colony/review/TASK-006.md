# TASK-006: CLI commands for timer start/stop/status

**Status:** review
**Assigned:** bravo
**Priority:** P1
**Depends-On:** TASK-001, TASK-005

## Description
Wire up the timer core logic to Click CLI commands in `chronolog/cli.py`. Implement `chrono start`, `chrono stop`, and `chrono status` commands with proper argument handling and Rich-formatted output.

## Acceptance Criteria
- [ ] `chrono start "description" --project NAME --tags tag1,tag2` starts a timer and prints confirmation with Rich formatting (green text showing what started)
- [ ] `chrono start` with no description prints an error
- [ ] `chrono stop` stops the running timer and prints a summary: description, project, duration, tags
- [ ] `chrono stop` when no timer is running prints a friendly error message
- [ ] `chrono status` shows the currently running timer: description, project, tags, elapsed time — or "No timer running" if idle
- [ ] All output uses Rich console for formatting (colors, panels, or tables)
- [ ] `--tags` accepts comma-separated values and splits them into a list
- [ ] CLI tests using Click's `CliRunner` in `tests/test_cli.py`
- [ ] At least 6 test cases covering: start success, start error, stop success, stop error, status running, status idle

## Notes
- Use `click.group()` for the main CLI group (should already exist from TASK-001)
- Use Rich Console for all output — `from rich.console import Console`
- Use Rich Panel or formatted text for status display
- Handle exceptions from core functions and display user-friendly errors (don't show tracebacks)

**Claimed-By:** bravo-1
**Claimed-At:** 1773605363

**Completed-At:** 1773605440
