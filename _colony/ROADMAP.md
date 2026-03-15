# ChronoLog Roadmap

> Maintained by ATLAS. Updated every 30-minute cycle.
> Last updated: 2026-03-15 cycle 10

## Overview
25 total tasks generated. All GOALS.md features covered (M1 + M2 + M3).
305 tests passing across review branches (per beta-tester cycle 5).

## M1: Core Timer — 5 Done, 8 in Review

### Done
TASK-001 (scaffolding), TASK-002 (models), TASK-003 (db), TASK-004 (project CRUD), TASK-005 (timer)

### In Review (waiting on audit)
TASK-006 (timer CLI), TASK-007 (project CLI), TASK-008 (utils), TASK-009 (list entries),
TASK-010 (edit/delete), TASK-011 (config), TASK-012 (integration tests), TASK-013 (exceptions)

### Bug Fix
TASK-022 (P0 Project.from_row bug) — in review

## M2: Reporting & Tags — In Progress

### Active
| Task | Title | Team |
|------|-------|------|
| TASK-016 | Weekly report | alpha |
| TASK-017 | Date range report | bravo |
| TASK-018 | CSV export | alpha |

### Done/Review
TASK-014 (tagging core) — review, TASK-015 (daily report) — review

## Queued (6)

| Task | Title | Team | Priority |
|------|-------|------|----------|
| TASK-019 | Report formatting helpers | bravo | P2 |
| TASK-020 | Test coverage to 80%+ | alpha | P2 |
| TASK-021 | CLI help text polish | bravo | P2 |
| TASK-023 | P0 bug duplicate (from_row) | alpha | P0 |
| TASK-024 | Database indexing | alpha | P2 |
| TASK-025 | Cross-platform paths | bravo | P2 |

## Bottleneck
**Audit review queue: 11 tasks.** This is the sole blocker for the colony.
All dev work is progressing well. Beta-tester confirms all branches pass tests.

## Summary
- Tasks 001-013: M1 (Core Timer)
- Tasks 014-019: M2 (Reports & Tags)
- Tasks 020-025: Quality & Polish
- Queue: 3 alpha, 3 bravo — healthy
