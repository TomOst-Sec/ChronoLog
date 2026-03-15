# ChronoLog Roadmap

> Maintained by ATLAS. Updated every 30-minute cycle.
> Last updated: 2026-03-15 cycle 3

## Current Milestone: M1 — Core Timer

Goal: Implement Features 1 (start/stop timer), 2 (project management), and 9 (SQLite storage) from GOALS.md.

## Current Sprint

### Foundation (P0 — must complete first)
| Task | Title | Team | Priority | Depends | Status |
|------|-------|------|----------|---------|--------|
| TASK-001 | Project scaffolding & package structure | alpha | P0 | none | **review** |
| TASK-002 | Data models for entries and projects | bravo | P0 | TASK-001 | **active** (bravo-1) |
| TASK-003 | SQLite database initialization & schema | alpha | P0 | TASK-001 | **active** (alpha-2) |

### Core Features (P0/P1 — after foundation)
| Task | Title | Team | Priority | Depends | Status |
|------|-------|------|----------|---------|--------|
| TASK-005 | Timer start/stop core logic | bravo | P0 | TASK-001, TASK-003 | queue |
| TASK-004 | Project management CRUD operations | alpha | P1 | TASK-001, TASK-003 | **active** (alpha-1) |
| TASK-008 | Duration formatting & timezone utilities | alpha | P1 | TASK-001 | queue |

### CLI & Display Layer (P1 — after core)
| Task | Title | Team | Priority | Depends | Status |
|------|-------|------|----------|---------|--------|
| TASK-006 | CLI commands for timer start/stop/status | bravo | P1 | TASK-001, TASK-005 | queue |
| TASK-007 | CLI commands for project management | alpha | P1 | TASK-001, TASK-004 | queue |
| TASK-009 | List recent time entries command | alpha | P1 | TASK-001, TASK-003 | queue |
| TASK-010 | Edit and delete time entries | bravo | P1 | TASK-001, TASK-003, TASK-005 | queue |

## Completed
(none yet — TASK-001 awaiting audit review)

## Upcoming (M1 tasks not yet generated)
- Default project config (`chrono config`)

## Future Milestones
- **M2: Reporting & Tags** — Features 3, 4, 5, 6 (tags, daily/weekly/range reports, Rich output)
- **M3: Polish** — Features 7, 8, 10 (CSV export, config)
