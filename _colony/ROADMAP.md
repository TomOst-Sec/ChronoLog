# ChronoLog Roadmap

> Maintained by ATLAS. Updated every 30-minute cycle.
> Last updated: 2026-03-15 cycle 4

## Current Milestone: M1 — Core Timer

Goal: Implement Features 1 (start/stop timer), 2 (project management), and 9 (SQLite storage) from GOALS.md.

## Current Sprint

### Foundation (P0)
| Task | Title | Team | Priority | Status |
|------|-------|------|----------|--------|
| TASK-001 | Project scaffolding & package structure | alpha | P0 | **done** |
| TASK-002 | Data models for entries and projects | bravo | P0 | **review** |
| TASK-003 | SQLite database initialization & schema | alpha | P0 | **review** |

### Core Features (P0/P1)
| Task | Title | Team | Priority | Status |
|------|-------|------|----------|--------|
| TASK-004 | Project management CRUD operations | alpha | P1 | **active** (alpha-1) |
| TASK-005 | Timer start/stop core logic | bravo | P0 | **active** (bravo-1) |
| TASK-008 | Duration formatting & timezone utilities | alpha | P1 | **active** (alpha-3) |

### CLI & Display Layer (P1)
| Task | Title | Team | Priority | Status |
|------|-------|------|----------|--------|
| TASK-006 | CLI commands for timer start/stop/status | bravo | P1 | queue |
| TASK-007 | CLI commands for project management | alpha | P1 | queue |
| TASK-009 | List recent time entries command | alpha | P1 | queue |
| TASK-010 | Edit and delete time entries | bravo | P1 | queue |

### Config & Testing (P1)
| Task | Title | Team | Priority | Status |
|------|-------|------|----------|--------|
| TASK-011 | Configuration system | alpha | P1 | queue |
| TASK-012 | End-to-end integration tests | bravo | P1 | queue |

## Completed
- TASK-001: Project scaffolding (merged by audit)

## Upcoming
- M1 task generation complete. 12 tasks cover all M1 features.
- Next: M2 task generation once M1 tasks are mostly done/review.

## Future Milestones
- **M2: Reporting & Tags** — Features 3, 4, 5, 6 (tags, daily/weekly/range reports, Rich output)
- **M3: Polish** — Features 7, 8, 10 (CSV export)
