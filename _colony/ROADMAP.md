# ChronoLog Roadmap

> Maintained by ATLAS. Updated every 30-minute cycle.
> Last updated: 2026-03-15

## Current Milestone: M1 — Core Timer

Goal: Implement Features 1 (start/stop timer), 2 (project management), and 9 (SQLite storage) from GOALS.md.

## Current Sprint

### Foundation (P0 — must complete first)
| Task | Title | Team | Priority | Depends | Status |
|------|-------|------|----------|---------|--------|
| TASK-001 | Project scaffolding & package structure | alpha | P0 | none | queue |
| TASK-002 | Data models for entries and projects | bravo | P0 | TASK-001 | queue |
| TASK-003 | SQLite database initialization & schema | alpha | P0 | TASK-001 | queue |

### Core Features (P0/P1 — after foundation)
| Task | Title | Team | Priority | Depends | Status |
|------|-------|------|----------|---------|--------|
| TASK-005 | Timer start/stop core logic | bravo | P0 | TASK-001, TASK-003 | queue |
| TASK-004 | Project management CRUD operations | alpha | P1 | TASK-001, TASK-003 | queue |

### CLI Layer (P1 — after core)
| Task | Title | Team | Priority | Depends | Status |
|------|-------|------|----------|---------|--------|
| TASK-006 | CLI commands for timer start/stop/status | bravo | P1 | TASK-001, TASK-005 | queue |
| TASK-007 | CLI commands for project management | alpha | P1 | TASK-001, TASK-004 | queue |

## Completed
(none yet)

## Upcoming (M1 tasks not yet generated)
- List recent entries command (`chrono list`)
- Edit/delete entry support
- Default project config

## Future Milestones
- **M2: Reporting & Tags** — Features 3, 4, 5, 6 (tags, daily/weekly/range reports, Rich output)
- **M3: Polish** — Features 7, 8, 10 (CSV export, edit/delete, config)
