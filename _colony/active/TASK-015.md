# TASK-015: Daily report — today and yesterday

**Status:** active
**Assigned:** bravo
**Priority:** P1
**Depends-On:** TASK-001, TASK-003

## Description
Implement `chrono report today` and `chrono report yesterday`. Shows all time entries for the given day in a Rich table with totals at the bottom. Feature 4 from GOALS.md (M2).

## Acceptance Criteria
- [ ] `chrono report` is a Click subgroup under the main CLI
- [ ] `chrono report today` shows all entries for today: Start, End, Duration, Project, Tags, Description
- [ ] `chrono report yesterday` shows entries for yesterday
- [ ] Total hours displayed at bottom of table
- [ ] Running entries show "running" for end time
- [ ] Empty days show "No entries for [date]" message
- [ ] Core function `get_entries_for_date(db_path, date) -> list[TimeEntry]`
- [ ] Date comparison handles UTC storage vs local timezone correctly
- [ ] Tests: empty day, day with entries, running entry, date filtering
- [ ] At least 6 test cases

## Notes
- Compare dates in local timezone (entry started 11pm local = next day UTC)
- Use Rich Table for output
- M2 scope — needs M1 core merged first

**Claimed-By:** bravo-1
**Claimed-At:** 1773605603
