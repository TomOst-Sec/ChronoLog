# Beta-Tester Report — Cycle 8

> Date: 2026-03-15
> Tested commit: d090af6 (HEAD of main)
> Last tested commit: 993e23e

## Main Branch Test Results

**50/50 tests PASSED** | Main is GREEN

## CRITICAL BUG FOUND — TASK-037 Filed (P0)

**TASK-006 was marked done but never actually merged to main.**

- `chronolog/cli.py` on main has NO start/stop/status commands — only the base Click group from TASK-001
- `chrono start "test"` → "Error: No such command 'start'"
- AUDIT moved `_colony/review/TASK-006.md` → `_colony/done/TASK-006.md` (commit d797d14) but no merge commit for task/006 exists
- The task/006 branch (42/42 tests) is intact and tested — needs to be properly merged

**Filed as TASK-037 (P0, assigned bravo).** However, this should really be an AUDIT action — re-merge from the existing branch.

## New Merges Since Last Cycle

| Task | Description | Actually Merged? |
|------|-------------|------------------|
| TASK-006 | Timer CLI | NO — task file moved to done but code not merged |
| TASK-013 | Custom exceptions | YES — verified on main |

**Done: 6 tasks (but TASK-006 is a phantom — code not on main)**

## M1 Status

| Criterion | Status |
|---|---|
| Installable | DONE |
| chrono start | BUG — CLI not on main (TASK-037) |
| chrono stop | BUG — CLI not on main (TASK-037) |
| chrono status | BUG — CLI not on main (TASK-037) |
| chrono project CRUD | Core DONE, CLI in review (TASK-007) |
| SQLite auto-create | DONE |
| ≥80% coverage | 99% |
| All tests pass | YES |

**M1 cannot be completed until TASK-037 is resolved.**

## Review Queue

21 tasks in review (down from 21 last cycle — TASK-006 and TASK-013 "cleared" but only TASK-013 actually merged).
