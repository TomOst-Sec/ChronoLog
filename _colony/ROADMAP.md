# ChronoLog Roadmap

> Maintained by ATLAS. Updated every 30-minute cycle.
> Last updated: 2026-03-15 cycle 16

## STATUS: QUEUE REFILLED — CODERS UNBLOCKED

Previous review backlog has been cleared. 41 tasks done, 1 active.
Core modules are built but many CLI commands are not wired up.
8 new tasks generated (TASK-043 through TASK-050) to fill the gap.

### By the Numbers
- **Done (41):** 001-022, 024-042
- **Active (1):** 023 (P0 bug — Project.from_row, alpha-2)
- **In Review (0):** none
- **Queue (8):** 043, 044, 045, 046, 047, 048, 049, 050
- **On main:** 86 tests, all passing, GREEN

## What's Merged (on main)
- Project scaffolding, pyproject.toml, package structure
- Data models (TimeEntry, Project) with from_row() classmethods
- SQLite database layer (schema, connection, init)
- Project CRUD (create, list, archive, get) — core + CLI
- Timer start/stop/status — core + CLI
- List entries — core + CLI
- Edit/delete entries — core only (no CLI commands yet)
- Configuration system — core + CLI
- CSV export — core only (no CLI command yet)
- Database backup/restore — core only (no CLI commands yet)
- Tag statistics — core only (no CLI command yet)
- Rich display helpers (entries table, summary table, report header)
- Custom exceptions (defined but not adopted in core.py)

## What's Missing (CLI Wiring)
The core logic exists for most features, but CLI commands are not wired up:

### M2: Reports & Tags (alpha team, P1)
- TASK-043: Daily report CLI (`chrono report today/yesterday`)
- TASK-044: Weekly report CLI (`chrono report week`)
- TASK-045: Date range report CLI (`chrono report --from/--to`)
- TASK-046: Tags CLI (`chrono tags`)

### M3: Polish (bravo team, P1-P2)
- TASK-047: Edit/delete CLI (`chrono edit`, `chrono delete`)
- TASK-048: CSV export CLI (`chrono export`)
- TASK-049: Backup/restore CLI (`chrono db backup/restore`)
- TASK-050: Adopt custom exceptions in core.py (alpha, P2)

## Task Catalog
- 001-013: M1 Core Timer
- 014-019: M2 Reports & Tags
- 020-027: Quality & DevEx
- 028-034: Bonus Features
- 035-042: Additional features & fixes
- 043-050: CLI wiring & exception adoption
