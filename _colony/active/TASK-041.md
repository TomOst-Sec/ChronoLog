# TASK-041: Timer auto-stop on midnight boundary

**Status:** active
**Assigned:** alpha
**Priority:** P2
**Depends-On:** TASK-001, TASK-003, TASK-005

## Description
Handle the edge case where a timer runs past midnight. When stopping a timer that spans midnight, split it into two entries (one for each day) so daily reports are accurate. Currently a timer started at 11pm and stopped at 2am shows as a single entry, which makes daily totals misleading.

## Acceptance Criteria
- [ ] Function `stop_timer` detects if the entry spans midnight (local timezone)
- [ ] If spanning midnight: splits into two entries — first ends at 23:59:59, second starts at 00:00:00 next day
- [ ] If spanning multiple midnights: creates one entry per day
- [ ] Original entry is updated (first segment), additional entries are inserted
- [ ] Reports correctly attribute time to each day
- [ ] `--no-split` flag on `chrono stop` to disable splitting (keep as single entry)
- [ ] Tests: same-day stop (no split), midnight span, multi-day span, no-split flag
- [ ] At least 5 test cases

## Notes
- Midnight detection uses local timezone, not UTC
- This is important for accurate daily reports
- Use a transaction for the split operation (atomicity)

**Claimed-By:** alpha-3
**Claimed-At:** 1773606389
