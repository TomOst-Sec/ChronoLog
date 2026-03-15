# TASK-032: Rounding and time display preferences

**Status:** queue
**Assigned:** alpha
**Priority:** P2
**Depends-On:** TASK-001, TASK-008

## Description
Add time rounding options for reports and display. Some users prefer times rounded to nearest 5/15 minutes for billing. Add a `round_to` config option and a `--round` flag on report commands.

## Acceptance Criteria
- [ ] Function `round_duration(minutes: float, round_to: int = 1) -> float` in utils.py — rounds to nearest N minutes
- [ ] Supported values: 1 (default, no rounding), 5, 15, 30
- [ ] Config option: `chrono config set round_to 15` (default: 1)
- [ ] Report commands accept `--round N` flag that overrides config
- [ ] Rounding applied in display only — stored data is never modified
- [ ] Tests: round to 5, 15, 30, edge cases (0 minutes, exact boundaries)
- [ ] At least 5 test cases

## Notes
- Round using: `math.ceil(minutes / round_to) * round_to`
- Only affects display in reports and list, not the stored data
- This is a nice-to-have feature beyond GOALS.md scope
