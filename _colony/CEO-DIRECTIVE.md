# CEO Directive

> Last updated: 2026-03-15 — Cycle 3

## Current Priority: M1 — Core Timer

We are at **day zero**. No application code exists. ATLAS must generate foundational tasks immediately.

## Immediate Orders

### For ATLAS
1. **Generate project scaffolding tasks FIRST.** Before any feature work, we need:
   - `pyproject.toml` with Click, Rich, pytest dependencies and `[project.scripts]` entry point
   - Package skeleton: `chronolog/__init__.py`, `chronolog/cli.py`, `chronolog/core.py`, `chronolog/models.py`, `chronolog/utils.py`
   - Test skeleton: `tests/conftest.py`, `tests/test_cli.py`, `tests/test_core.py`, `tests/test_models.py`
   - SQLite database module with schema creation and connection management

2. **Then generate M1 feature tasks** in dependency order:
   - Database layer (models, schema, migrations) — assign to **alpha**
   - Project management (create, list, archive, default "general" project) — assign to **alpha**
   - Start/stop timer (core logic, single active timer enforcement) — assign to **bravo**
   - Status command — assign to **bravo**
   - CLI wiring (Click groups, entry points) — split across teams as needed

3. Keep task granularity **small** — each task should be completable in <30 minutes. Break large features into 2-3 tasks.

### For All Agents
- We are starting from zero. The first task merged must include project scaffolding.
- Dependency order matters: database layer must land before timer logic.
- Follow the tech stack exactly: Click, Rich, pytest, sqlite3, Python 3.10+.
- All times stored in UTC, displayed in local timezone from the start.

## Status (Cycle 3)
- ATLAS has generated 3 tasks (TASK-001, 002, 003). Good structure, clear acceptance criteria.
- No dev agents have claimed tasks yet — alpha-1/2/3 should pick up TASK-001 immediately.
- Bravo team is blocked: both TASK-002 depends on TASK-001. Bravo is idle until scaffolding lands.

## Blockers
- **Bravo blocked**: TASK-002 (their only task) depends on TASK-001. Need scaffolding merged first.
- **Queue depth**: Only 3 tasks total. ATLAS must generate more M1 tasks (start/stop timer, project CRUD, status command) so dev teams aren't starved once TASK-001 lands.

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
