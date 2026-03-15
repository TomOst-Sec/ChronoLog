# TASK-016: Weekly report with project breakdown

**Status:** review
**Assigned:** alpha
**Priority:** P1
**Depends-On:** TASK-001, TASK-003

## Description
Implement `chrono report week` showing a breakdown by project for the current week. Each project shows total hours and percentage. Includes a Rich bar chart visualization. Feature 5 from GOALS.md (M2).

## Acceptance Criteria
- [ ] `chrono report week` shows current week (Monday to Sunday) summary
- [ ] Output grouped by project: Project Name, Total Hours, Percentage of Week
- [ ] Visual bar chart using Rich (e.g., Rich Bar or colored blocks)
- [ ] Core function `get_weekly_summary(db_path, week_start: date) -> list[dict]` — returns project summaries
- [ ] Total hours for the week shown at bottom
- [ ] Empty week shows friendly message
- [ ] Week boundaries are Monday 00:00 local to Sunday 23:59 local
- [ ] Tests: empty week, single project, multiple projects, percentage calculation
- [ ] At least 5 test cases

## Notes
- Use `Rich.Bar` or Unicode blocks for the bar chart
- Percentages should add up to 100% (of tracked time, not of calendar time)
- M2 scope

**Claimed-By:** alpha-2
**Claimed-At:** 1773605607

**Completed-At:** 1773605764
