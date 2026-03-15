# TASK-048: Add CSV export CLI command

**Status:** active
**Assigned:** bravo
**Priority:** P1
**Depends-On:** none

## Description
Wire up `export.export_entries_csv()` to a `chrono export` CLI command. The command takes `--from` and `--to` date parameters and an optional `--output` file path.

## Acceptance Criteria
- [ ] `chrono export --from 2024-01-01 --to 2024-01-31` writes CSV to stdout
- [ ] `chrono export --from ... --to ... --output file.csv` writes to a file
- [ ] CSV columns: date, start_time, end_time, duration_minutes, project, tags, description
- [ ] Both `--from` and `--to` are required
- [ ] Invalid date format shows a clear error
- [ ] Success message shows count of exported entries and output path
- [ ] `--db` hidden option for testability
- [ ] Tests exist for the CLI command
- [ ] `pytest` passes clean

## Notes
- `export.export_entries_csv()` already handles the heavy lifting
- Import from `chronolog.export` in cli.py
- Follow the same `--db` pattern used by other commands

**Claimed-By:** bravo-2
**Claimed-At:** 1773608361
