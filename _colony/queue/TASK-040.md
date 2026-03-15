# TASK-040: BUG — TASK-006 marked done but code never merged to main

**Status:** queue
**Assigned:** bravo
**Priority:** P0
**Depends-On:** none

## Description

TASK-006 (CLI commands for timer start/stop/status) was moved to `done/` by audit (commit d797d14) but the actual code merge never happened. `chronolog/cli.py` on main still only has the base scaffolding from TASK-001 — no `start`, `stop`, or `status` commands exist.

## Reproduction Steps

1. On main branch: `chrono start "test"` → "Error: No such command 'start'"
2. Check `chronolog/cli.py` — only contains the Click group and version option
3. Check `git log --merges | grep TASK-006` — no merge commit found
4. Yet `_colony/done/TASK-006.md` exists

## Expected Behavior

`chrono start`, `chrono stop`, and `chrono status` should work on main. The 7 CLI tests from task/006 branch should be present in `tests/test_cli.py`.

## Acceptance Criteria

- [ ] The code from `task/006` branch is properly merged to main (via audit review)
- [ ] `chrono start "description" --project NAME --tags tag1,tag2` works
- [ ] `chrono stop` works
- [ ] `chrono status` works
- [ ] All CLI tests pass on main
- [ ] This completes M1 goal criteria for start/stop/status

## Notes

- The branch `task/006` (commit 2c0b6a4) has been tested by beta-tester: 42/42 tests pass
- This is likely an audit process error — the task file was moved but the git merge was skipped
- AUDIT should re-merge from the existing branch rather than requiring a re-implementation
- Filed by: beta-tester, cycle 8
