# Beta-Tester Report — Cycle 14

> Date: 2026-03-15
> Tested commit: eb58f57 (HEAD)
> Previous tested: 990cb57 (cycle 13)
> New commits since last test: 17

## Test Suite

```
95/95 tests PASSED (0.13s)
```

No regressions. 9 new tests added by TASK-043 (daily report).

## Coverage

| Module | Coverage | Missing |
|--------|----------|---------|
| `__init__.py` | 100% | — |
| `backup.py` | 0% | 23 stmts |
| `cli.py` | 52% | 92 stmts |
| `config.py` | 85% | 3 stmts |
| `core.py` | 63% | 63 stmts |
| `db.py` | 100% | — |
| `display.py` | 67% | 14 stmts |
| `exceptions.py` | 100% | — |
| `export.py` | 0% | 27 stmts |
| `models.py` | 98% | 1 stmt |
| `utils.py` | 100% | — |
| **TOTAL** | **59%** | **223 stmts** |

Coverage improved from 50% to 59% with TASK-043 merge. Target remains 80%.

## End-to-End Feature Verification (CEO Priority 4)

### Features WORKING on main (5/10)

| # | Feature | CLI | Verified |
|---|---------|-----|----------|
| 1 | Start/Stop Timer | `chrono start/stop/status` | PASS — full lifecycle tested |
| 2 | Project Management | `chrono project create/list/archive` | PASS — create, list, archive all work |
| 4 | Daily Report | `chrono report today/yesterday` | PASS — NEW via TASK-043, Rich table output |
| 9 | SQLite Storage | `~/.chronolog/chrono.db` | PASS — UTC ISO 8601 storage verified |
| 10 | Configuration | `chrono config show/set` | PASS — key/value persistence works |

### Features with core logic but NO CLI command (5/10)

| # | Feature | Core Function Tested | CLI Missing | Task Status |
|---|---------|---------------------|-------------|-------------|
| 3 | Tags listing | `list_tags()` PASS | `chrono tags` | TASK-046 in review |
| 5 | Weekly Report | not on main yet | `chrono report week` | TASK-044 active |
| 6 | Date Range Report | not on main yet | `chrono report --from/--to` | TASK-045 queued |
| 7 | CSV Export | `export_entries_csv()` PASS | `chrono export` | TASK-048 in review |
| 8 | Edit/Delete | `edit_entry()`, `delete_entry()` PASS | `chrono edit/delete` | TASK-047 in review |

### Backend Functions Verified Directly

All core functions tested via Python — all PASS:
- `edit_entry()` — update description, project, tags correctly
- `delete_entry()` — deletes by ID, raises on missing ID
- `list_tags()` — aggregates time per tag, sorts by total time
- `export_entries_csv()` — correct CSV format with proper headers
- `backup_db()` / `restore_db()` — backup, restore, blocks during running timer

### Error Handling Verified
- Double start: blocked with clear error
- Stop when idle: returns error
- Start with nonexistent project: returns error
- Default "general" project: works correctly
- Delete nonexistent entry: raises RuntimeError

### UTC Storage / Local Display
- Times stored as ISO 8601 with +00:00 UTC offset
- `chrono list` displays UTC times in table (GOALS.md says "displayed in local timezone" — minor gap)
- `chrono report today` uses display.py helpers which convert properly

## Bug Filed

### TASK-051: CLI --db option inconsistency (P2, bravo)
Project subcommands (`create/list/archive`) lack the hidden `--db` option that `start/stop/status/list` have. Makes isolated testing of project commands impossible without HOME override.

## Colony Status

| Metric | Value |
|--------|-------|
| Done tasks | 42 |
| In review | 5 (TASK-043, 046, 047, 048, 049) |
| Active | 2 (TASK-044, 050) |
| Queued | 1 (TASK-045) |
| Tests | 95/95 passing |
| Coverage | 59% (target 80%) |
| Main health | GREEN |

## Key Observation

TASK-043 code landed on main via commit 9622dcb but the task file is still in review/. AUDIT should note this was already merged and move to done.

5 tasks in review queue need AUDIT attention — once merged, 8/10 GOALS.md features will be CLI-accessible. Coverage sprint still needed to reach 80% target.
