# TASK-038: JSON export format option

**Status:** review
**Assigned:** alpha
**Priority:** P2
**Depends-On:** TASK-001, TASK-003, TASK-018

## Description
Add JSON as an alternative export format alongside CSV. `chrono export --format json` exports entries as a JSON array. JSON is useful for programmatic consumption and integration with other tools.

## Acceptance Criteria
- [ ] `chrono export --format json --from DATE --to DATE` exports entries as JSON
- [ ] `chrono export --format csv` remains the default behavior
- [ ] JSON output is a list of objects with keys: id, description, project, tags, start_time, end_time, duration_minutes
- [ ] Tags serialized as JSON array (not comma-separated string)
- [ ] Dates formatted as ISO 8601 strings
- [ ] `--output FILE` writes to file, default is stdout
- [ ] Tests: JSON export, format flag, JSON structure validation
- [ ] At least 4 test cases

## Notes
- Use `json.dumps(entries, indent=2, default=str)` for pretty output
- Reuse query logic from CSV export (TASK-018)

**Claimed-By:** alpha-2
**Claimed-At:** 1773606262

**Completed-At:** 1773606393
