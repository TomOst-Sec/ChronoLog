# TASK-046: Add tags CLI command

**Status:** active
**Assigned:** alpha
**Priority:** P1
**Depends-On:** none

## Description
Implement `chrono tags` CLI command that lists all used tags with total time per tag. The `list_tags()` function already exists in `core.py` — this task wires it to the CLI with Rich table output.

## Acceptance Criteria
- [ ] `chrono tags` displays a Rich table with columns: Tag, Total Time, Entries
- [ ] Tags sorted by total time (descending) — already done in `list_tags()`
- [ ] Total time displayed as hours and minutes (e.g., "2h 30m")
- [ ] Empty result shows "No tags found" message
- [ ] `--db` hidden option for testability
- [ ] Tests exist for the CLI command
- [ ] `pytest` passes clean

## Notes
- `core.list_tags()` returns `list[dict]` with keys: tag, total_minutes, entry_count
- Format minutes nicely: if >= 60, show "Xh Ym", else show "Xm"
- Follow the same CLI patterns used in other commands (console, Rich tables)

**Claimed-By:** alpha-2
**Claimed-At:** 1773608266
