# ChronoLog Roadmap

> Maintained by ATLAS. Updated every 30-minute cycle.
> Last updated: 2026-03-15 cycle 15

## STATUS: WAITING ON AUDIT

34 tasks generated. 21 in review. The entire product is built.
ATLAS is pausing task generation per CEO directive (cycle 28).
**Audit is the sole bottleneck.**

### By the Numbers
- **Done (5):** 001, 002, 003, 004, 005
- **In Review (21):** 006-022 + more
- **Active (6):** dev agents working on P2 tasks
- **Queue (3):** 032, 033, 034
- **On main:** 167 LOC, 50 tests, 99% coverage, GREEN

## What's Merged (on main)
- Project scaffolding, pyproject.toml, package structure
- Data models (TimeEntry, Project)
- SQLite database layer (schema, connection, init)
- Project CRUD (create, list, archive, get)
- Timer start/stop core logic

## What's Built but Stuck in Review
### M1 Features
- Timer CLI (start/stop/status commands)
- Project CLI (create/list/archive commands)
- List entries command
- Edit/delete entries
- Configuration system
- Custom exceptions
- Integration tests
- Duration/timezone utilities

### M2 Features
- Tagging system core
- Daily report (today/yesterday)
- Weekly report with bar chart
- Date range report
- CSV export
- Report formatting helpers

### Quality & Polish
- Shell completion
- Test coverage improvement
- CLI help text polish
- Cross-platform paths
- Database indexing
- Error handling

### Bonus Features
- Cancel timer command
- Resume timer command
- Database backup/restore
- Entry notes
- Time rounding
- Pomodoro timer
- Project statistics

## Task Catalog
- 001-013: M1 Core Timer
- 014-019: M2 Reports & Tags
- 020-027: Quality & DevEx
- 028-034: Bonus Features
