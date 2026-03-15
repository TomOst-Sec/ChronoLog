# TASK-008: Duration formatting and timezone display utilities

**Status:** review
**Assigned:** alpha
**Priority:** P1
**Depends-On:** TASK-001

## Description
Implement utility functions in `chronolog/utils.py` for formatting durations and converting UTC datetimes to local timezone for display. These utilities are needed by every display command (list, status, reports).

## Acceptance Criteria
- [ ] Function `format_duration(td: timedelta) -> str` — formats timedelta as human-readable: "Xh Ym" for >1h, "Xm" for <1h, "< 1m" for <1 minute
- [ ] Function `utc_to_local(dt: datetime) -> datetime` — converts UTC datetime to local timezone
- [ ] Function `format_datetime(dt: datetime) -> str` — formats as "YYYY-MM-DD HH:MM" in local timezone
- [ ] Function `format_time(dt: datetime) -> str` — formats just time as "HH:MM" in local timezone
- [ ] Function `parse_tags(tags_str: str) -> list[str]` — splits comma-separated tags, strips whitespace, removes empties
- [ ] Function `format_tags(tags: list[str]) -> str` — joins tags with ", " for display
- [ ] All functions have type hints and Google-style docstrings
- [ ] Tests in `tests/test_utils.py` (create this file) covering all functions with edge cases
- [ ] At least 10 test cases

## Notes
- Use `datetime.astimezone()` for timezone conversion
- Duration formatting should handle zero duration gracefully
- parse_tags("") should return [], not [""]
- These are pure utility functions with no DB dependency — easy to test

**Claimed-By:** alpha-3
**Claimed-At:** 1773605224

**Completed-At:** 1773605305
