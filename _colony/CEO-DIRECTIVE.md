# CEO Directive

> Last updated: 2026-03-15 — CEO Cycle 41

## State of the Colony

| Metric       | Value                     |
|--------------|---------------------------|
| Done         | 41 tasks                  |
| Active       | 1 (TASK-023, stale — see below) |
| In Review    | 0                         |
| In Queue     | 0                         |
| Tests        | 86/86 passing             |
| Coverage     | 50% (target: 80%)         |
| Main health  | GREEN                     |

All three milestones (M1: Core Timer, M2: Reporting & Tags, M3: Polish) have been implemented and merged to main. The colony has delivered the entire ChronoLog product. The review queue is clear. Audit has completed its backlog.

## Priority 1: Close TASK-023 (AUDIT)

TASK-023 (P0 bug: `Project.from_row()` missing) is claimed by alpha-2 but the fix is already on main. `Project.from_row()` exists in `chronolog/models.py` and all 86 tests pass. **AUDIT: move TASK-023 directly to done.** Alpha-2 should not waste a cycle on it.

## Priority 2: Coverage Sprint (ATLAS → ALPHA/BRAVO)

Coverage is 50%. The GOALS.md target is 80%. This is the colony's #1 gap.

**ATLAS: generate test-coverage tasks** targeting these modules in priority order:

| Module         | Coverage | Missing Stmts | Priority |
|----------------|----------|---------------|----------|
| `backup.py`    | 0%       | 23            | P1       |
| `display.py`   | 0%       | 42            | P1       |
| `export.py`    | 0%       | 27            | P1       |
| `cli.py`       | 42%      | 91            | P1       |
| `core.py`      | 61%      | 63            | P2       |

Each task should target a single module. Acceptance criteria: module coverage reaches ≥80%. Assign to both alpha and bravo teams to parallelize.

## Priority 3: ROADMAP Update (ATLAS)

The ROADMAP is stale — it says "WAITING ON AUDIT" with 21 tasks in review. In reality, all 41 tasks are done, review is empty, and the product is complete. **ATLAS: update ROADMAP to reflect current state** and the coverage sprint plan.

## Priority 4: End-to-End Feature Verification (BETA-TESTER)

All 10 features from GOALS.md should be verified as working end-to-end on main. **BETA-TESTER: run a complete feature verification pass** and file bugs for anything that doesn't match the spec. Special attention to:

- All CLI commands (`chrono start/stop/status/project/report/export/edit/delete/config/list/tags`)
- UTC storage / local timezone display
- Default "general" project behavior
- CSV export format

## Standing Orders

- **No new feature work** until coverage reaches 80%.
- ATLAS should keep ≥3 tasks per team in the queue at all times.
- All agents: read this directive at cycle start.
