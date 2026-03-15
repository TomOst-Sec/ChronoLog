# TASK-009: List recent time entries command

**Status:** review
**Assigned:** alpha
**Priority:** P1
**Depends-On:** TASK-001, TASK-003

## Description
Implement `chrono list` to show recent time entries with their IDs. This is essential for users to reference entries when editing or deleting them later. Includes both the core query function and the CLI command with Rich table output.

## Acceptance Criteria
- [ ] Function `list_entries(db_path, limit: int = 10) -> list[TimeEntry]` in core.py — returns recent entries ordered by start_time descending
- [ ] `chrono list` displays entries in a Rich table with columns: ID, Description, Project, Tags, Start, End, Duration
- [ ] `chrono list --limit N` controls how many entries to show (default 10)
- [ ] Running entries show "running" instead of end time and a live duration
- [ ] Empty database shows a friendly "No entries yet" message
- [ ] Tests in `tests/test_core.py` for list_entries: empty db, with entries, limit parameter, ordering
- [ ] Tests in `tests/test_cli.py` for CLI output
- [ ] At least 6 test cases total

## Notes
- Duration should be formatted as "Xh Ym" (e.g., "2h 15m" or "45m") — use utils from TASK-008 if available
- Use Rich Table for output
- This command is needed before edit/delete can be useful

**Claimed-By:** alpha-2
**Claimed-At:** 1773605232

**Completed-At:** 1773605431
