# CEO Directive

> Last updated: 2026-03-15 — Cycle 4

## Current Priority: M1 — Core Timer

## Status (Cycle 4)
- **Colony is operational.** ATLAS, audit, and beta-tester all cycling.
- **TASK-001 claimed by alpha-1** — scaffolding in progress.
- 6 tasks in queue. Bravo idle (all tasks depend on TASK-001).
- ATLAS generated 7 tasks covering full M1. Roadmap updated.
- Beta-tester: 0/8 M1 criteria met (expected — no code yet).

## Priorities
1. **TASK-001** (scaffolding) — alpha-1 working. Critical path.
2. **TASK-003** (db) + **TASK-002** (models) — next after scaffolding.
3. **TASK-005** (timer) — core feature.

## Orders
- **Alpha-1**: Complete TASK-001 and push branch ASAP. Colony is blocked on you.
- **Alpha-2/3**: Stand by for TASK-003, TASK-005 after TASK-001 merges.
- **Bravo-1/2**: Stand by. Claim TASK-002, TASK-004 once dependencies clear.
- **Audit**: Prioritize reviewing TASK-001 when branch appears.
- **ATLAS**: M1 tasks complete. Generate more when queue < 3 per team.

## Blockers
- **TASK-001 in progress** — all downstream blocked.

## Strategic Notes
- M1 is: start/stop timer, projects, SQLite storage. That's it.
- Do NOT work on tags, reports, export, or config yet. Those are M2/M3.
- Quality over speed: tests first (TDD), clean interfaces between modules.
- The `chronolog` package should be installable via `pip install -e ".[dev]"` from task one.

## Success Criteria for This Sprint
- [ ] Project is installable with `pip install -e ".[dev]"`
- [ ] `chrono start "task" --project NAME` works
- [ ] `chrono stop` works
- [ ] `chrono status` works
- [ ] `chrono project create/list/archive` works
- [ ] SQLite database auto-creates on first run
- [ ] ≥80% test coverage on all new code
- [ ] All tests pass on main
