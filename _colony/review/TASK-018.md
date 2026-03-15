# TASK-018: CSV export command

**Status:** review
**Assigned:** alpha
**Priority:** P1
**Depends-On:** TASK-001, TASK-003

## Description
Implement `chrono export` to export time entries to CSV. Feature 7 from GOALS.md (M2/M3 bridge). CSV is a common interchange format for time tracking data.

## Acceptance Criteria
- [ ] `chrono export --from DATE --to DATE --output file.csv` exports entries to CSV
- [ ] CSV columns: date, start_time, end_time, duration_minutes, project, tags, description
- [ ] Dates and times formatted in local timezone
- [ ] `--output` defaults to stdout if not specified (prints CSV to terminal)
- [ ] `--from` and `--to` required, same format as report command (YYYY-MM-DD)
- [ ] Core function `export_entries_csv(db_path, from_date, to_date, output_path)` handles the export
- [ ] Use Python's built-in `csv` module
- [ ] Tests: export to file, export to stdout, empty range, correct columns
- [ ] At least 5 test cases

## Notes
- Use `csv.DictWriter` for clean code
- Running entries (no end_time) should be excluded from export or marked as "running"
- M2/M3 scope — Feature 7

**Claimed-By:** alpha-3
**Claimed-At:** 1773605621

**Completed-At:** 1773605776
