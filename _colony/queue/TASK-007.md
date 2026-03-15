# TASK-007: CLI commands for project management

**Status:** queue
**Assigned:** alpha
**Priority:** P1
**Depends-On:** TASK-001, TASK-004

## Description
Wire up project management core logic to Click CLI commands in `chronolog/cli.py`. Implement `chrono project create`, `chrono project list`, and `chrono project archive` as a Click subgroup with Rich-formatted output.

## Acceptance Criteria
- [ ] `chrono project` is a Click subgroup under the main CLI group
- [ ] `chrono project create NAME` creates a project and prints confirmation
- [ ] `chrono project create` with duplicate name prints a friendly error
- [ ] `chrono project list` shows all active projects in a Rich table (columns: name, created date)
- [ ] `chrono project list --all` includes archived projects with an "archived" indicator
- [ ] `chrono project archive NAME` archives a project and prints confirmation
- [ ] `chrono project archive` with non-existent or already-archived project prints error
- [ ] Cannot archive the "general" project — prints error explaining why
- [ ] CLI tests using Click's `CliRunner` in `tests/test_cli.py`
- [ ] At least 6 test cases

## Notes
- Use `@cli.group()` to create the `project` subgroup
- Use Rich Table for the project list display
- Handle all exceptions from core functions gracefully — show user-friendly messages
- The "general" project should always appear in the list
