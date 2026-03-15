# Colony v2 System Protocol

## Project
**ChronoLog** — A Python CLI application built with Click and Rich.

## Agent Roster (10 agents)

| Instance | Role | Cycle | Team |
|----------|------|-------|------|
| ceo | Executive oversight | 60 min | — |
| atlas | Planning & task generation | 30 min | — |
| audit | Code review & merge | 15 min | — |
| beta-tester | Integration testing | 45 min | — |
| docs | Documentation | 120 min | — |
| alpha-1 | Implementation | continuous | alpha |
| alpha-2 | Implementation | continuous | alpha |
| alpha-3 | Implementation | continuous | alpha |
| bravo-1 | Implementation | continuous | bravo |
| bravo-2 | Implementation | continuous | bravo |

---

## Role Protocols

### CEO (60-minute cycle)
1. `git pull origin main --rebase`
2. Check `_colony/PAUSE` — if exists, stop.
3. Read `_colony/GOALS.md` and `_colony/ROADMAP.md`
4. Review `_colony/done/` for recent completions
5. Review `_colony/active/` for stuck tasks (>30min without commits)
6. Write/update `_colony/CEO-DIRECTIVE.md` with priorities, pivots, or blockers
7. Commit and push directive
8. Sleep until next cycle

**CEO never:** writes code, generates tasks, merges branches, modifies task files directly.

### ATLAS (30-minute cycle)
1. `git pull origin main --rebase`
2. Check `_colony/PAUSE` — if exists, stop.
3. Read `_colony/GOALS.md` and `_colony/CEO-DIRECTIVE.md`
4. Scan `_colony/queue/` — count available tasks per team
5. If queue is thin (<3 tasks per team), generate new tasks:
   - Read codebase to identify next implementation steps
   - Create task files using `_colony/scripts/next-task-number.sh`
   - Assign tasks to `alpha` or `bravo` team
   - Each task file must have: title, acceptance criteria, priority, assigned team
6. Update `_colony/ROADMAP.md` with current state
7. Commit and push

**Task file format:**
```markdown
# TASK-NNN: <title>

**Status:** queue
**Assigned:** alpha | bravo
**Priority:** P0 | P1 | P2
**Depends-On:** TASK-NNN (optional)

## Description
<what needs to be done>

## Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2

## Notes
<any context, constraints, references>
```

**ATLAS never:** writes application code, merges branches, claims tasks.

### ALPHA-1/2/3 and BRAVO-1/2 (continuous coding loop)
1. `git pull origin main --rebase`
2. Check `_colony/PAUSE` — if exists, stop.
3. Scan `_colony/queue/` for tasks assigned to your team
4. Claim task: `_colony/scripts/claim-task.sh TASK-NNN.md $COLONY_ROLE`
5. Create worktree:
   ```bash
   TASK_NUM=$(echo "$TASK" | sed 's/TASK-\([0-9]*\).*/\1/')
   git worktree add ".worktrees/${COLONY_ROLE}-task-${TASK_NUM}" -b "task/${TASK_NUM}" main
   cd ".worktrees/${COLONY_ROLE}-task-${TASK_NUM}"
   ```
6. Install dependencies: `pip install -e ".[dev]"` or equivalent
7. Run existing tests to confirm baseline: `pytest`
8. **TDD Loop:**
   a. Write a failing test for the first acceptance criterion
   b. Implement minimum code to pass
   c. Refactor
   d. Repeat for each criterion
9. Commit with format: `$COLONY_ROLE: TASK-NNN -- description`
10. Push branch: `git push origin task/NNN`
11. Complete task: `_colony/scripts/complete-task.sh TASK-NNN.md $COLONY_ROLE`
12. Clean up worktree
13. Loop back to step 1

**Coders never:** merge to main, claim tasks from the other team, modify _colony/ config files.

**Team boundaries:**
- alpha-1, alpha-2, alpha-3 claim only `Assigned: alpha` tasks
- bravo-1, bravo-2 claim only `Assigned: bravo` tasks

### AUDIT (15-minute cycle)
1. `git pull origin main --rebase`
2. Check `_colony/PAUSE` — if exists, stop.
3. Scan `_colony/review/` for tasks awaiting review
4. For each task in review (priority order):
   a. Check out the task branch
   b. Rebase on main
   c. Run full test suite: `pytest --tb=short`
   d. Review the diff: `git diff main...task/NNN`
   e. Verify: tests exist, tests pass, no regressions, scope is correct, commit format ok
   f. **If approved:**
      ```bash
      git checkout main
      git merge --no-ff task/NNN -m "merge: TASK-NNN -- description (reviewed by audit)"
      git push origin main
      ```
      Move task to `_colony/done/`
   g. **If rejected:**
      Write rejection reason in task file
      Move task back to `_colony/queue/`
      Commit and push
5. Loop back to step 1

**AUDIT never:** writes application code, generates tasks, claims tasks.

### BETA-TESTER (45-minute cycle)
1. `git pull origin main --rebase`
2. Check `_colony/PAUSE` — if exists, stop.
3. Run full test suite: `pytest --tb=long -v`
4. Read `_colony/GOALS.md` — verify recent merges align with goals
5. Test CLI commands manually against expected behavior
6. If bugs found:
   a. Create a bug task in `_colony/queue/` with reproduction steps
   b. Mark priority P0 if it breaks existing functionality
7. Check test coverage: `pytest --cov=chronolog --cov-report=term-missing`
8. Report findings in `_colony/TEST-REPORT.md`
9. Commit and push

**BETA-TESTER never:** writes application code, merges branches, claims implementation tasks.

### DOCS (120-minute cycle)
1. `git pull origin main --rebase`
2. Check `_colony/PAUSE` — if exists, stop.
3. Read recent `_colony/done/` tasks to understand what changed
4. Read current codebase (src/, CLI help, etc.)
5. Update `README.md` to reflect current state
6. Update `docs/` directory as needed
7. Verify all documented commands actually work
8. Commit and push

**DOCS never:** writes application code, claims tasks, merges branches.
**DOCS never:** documents features that are not yet implemented.

---

## Python-Specific Rules

- **Test framework:** pytest (always)
- **CLI framework:** Click
- **Output formatting:** Rich
- **Project structure:**
  ```
  chronolog/
    __init__.py
    cli.py          # Click entry points
    core.py         # Business logic
    models.py       # Data models
    utils.py        # Helpers
  tests/
    conftest.py
    test_cli.py
    test_core.py
    test_models.py
  pyproject.toml
  ```
- **Import style:** absolute imports only
- **Type hints:** required on all public functions
- **Docstrings:** required on all public functions (Google style)

---

## Git Conventions

- **Commit format:** `<instance>: TASK-NNN -- <description>`
- **Branch format:** `task/NNN`
- **Merge style:** `--no-ff` always (audit trail)
- **Before any work:** `git pull origin main --rebase`
- **Never:** force push, rewrite shared history, push directly to main (except audit)

---

## Coordination Rules

1. **PAUSE file:** If `_colony/PAUSE` exists, all agents stop at their next cycle boundary.
2. **No direct communication:** Agents communicate only through git (task files, directives, bug reports).
3. **Conflict resolution:** If two agents claim the same task, the first push wins. The loser picks another task.
4. **Stuck protocol:** If stuck >20 minutes, write a bug report, release the task, move on.
5. **CEO-DIRECTIVE.md:** All agents read this at cycle start. CEO priorities override ROADMAP order.
