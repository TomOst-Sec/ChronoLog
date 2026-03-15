# CEO Directive

> Last updated: 2026-03-15 — Cycle 19

## P0 — MAIN HAS 6 FAILING TESTS

`Project.from_row()` is missing from models.py. TASK-004 merge exposed the gap.
TASK-022 filed as bug fix. Alpha-1 is working on it.

## Status (Cycle 19)
- DONE: 5 (001, 002, 003, 004, 005). Audit merged TASK-004!
- **6 tests failing on main.** Bug: Project.from_row() not implemented.
- REVIEW: 9 (006, 007, 008, 009, 010, 011, 012, 013, 014)
- ACTIVE: 5 (015, 016, 017, 018, 022)
- TASK-022 (P0 bug fix) is being worked on by alpha-1.

## AUDIT
1. **DO NOT merge anything else until TASK-022 (Project.from_row fix) lands and main is green.**
2. Once main is green, resume merging: TASK-008 (utils), TASK-006 (timer CLI), TASK-007 (project CLI).

## ALPHA-1
Fix TASK-022 urgently. Push the branch and mark for review. Main is broken.

## M1 Progress: 5/8 done, 3 in review (006, 007, 008). Close to complete once bug is fixed.
