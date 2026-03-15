# TASK-014: Tagging system — list all tags with time totals

**Status:** active
**Assigned:** alpha
**Priority:** P1
**Depends-On:** TASK-001, TASK-003

## Description
Implement `chrono tags` command showing all used tags with total time per tag. Tags are free-form strings on time entries. This enables cross-project time analysis. Feature 3 from GOALS.md (M2).

## Acceptance Criteria
- [ ] Function `list_tags(db_path) -> list[dict]` — returns unique tags with total_minutes and entry_count, sorted by total time descending
- [ ] Function `get_entries_by_tag(db_path, tag: str) -> list[TimeEntry]` — returns entries containing the given tag
- [ ] `chrono tags` CLI command displays tags in a Rich table: Tag, Total Time, Entry Count
- [ ] Handles entries with multiple comma-separated tags (each tag gets full entry duration credit)
- [ ] Empty/no tags shows "No tags used yet"
- [ ] Tests covering: no tags, single tag, multiple tags per entry, tag totals, entries by tag query
- [ ] At least 6 test cases

## Notes
- Tags stored as comma-separated string in DB. Parse in Python.
- This is M2 scope — needs M1 core (db, models, timer) merged first

**Claimed-By:** alpha-1
**Claimed-At:** 1773605553
