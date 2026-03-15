# TASK-035: Streaks and productivity insights

**Status:** active
**Assigned:** alpha
**Priority:** P2
**Depends-On:** TASK-001, TASK-003

## Description
Implement `chrono insights` command showing productivity patterns: current streak (consecutive days with tracked time), longest streak, most productive day of the week, most productive hour, and total lifetime hours.

## Acceptance Criteria
- [ ] `chrono insights` displays productivity insights in a Rich panel
- [ ] Current streak: number of consecutive days (up to today) with at least one entry
- [ ] Longest streak: historical best consecutive days
- [ ] Most productive weekday: day of week with highest average hours
- [ ] Total lifetime hours tracked
- [ ] Total entries count
- [ ] Function `get_insights(db_path) -> dict` in core.py
- [ ] Tests: empty db, single day, multi-day streak, broken streak
- [ ] At least 5 test cases

## Notes
- Streak calculation: iterate dates backwards from today, count consecutive days with entries
- Use SQL GROUP BY for day-of-week analysis
- Display with Rich Panel and formatted text

**Claimed-By:** alpha-1
**Claimed-At:** 1773606147
