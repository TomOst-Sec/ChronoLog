# TASK-051: Add --db option to project CLI subcommands

**Status:** review
**Assigned:** bravo
**Priority:** P2
**Depends-On:** none

## Description

The `project create`, `project list`, and `project archive` CLI subcommands are missing the hidden `--db` option that other commands (`start`, `stop`, `status`, `list`) already have. This makes it impossible to test project commands against an isolated database without HOME directory hacks.

## Acceptance Criteria

- [ ] `chrono project create NAME --db PATH` works
- [ ] `chrono project list --db PATH` works
- [ ] `chrono project archive NAME --db PATH` works
- [ ] All existing project CLI tests still pass
- [ ] New tests verify --db option works for each project subcommand

## Notes

Bug found by beta-tester cycle 14 during end-to-end feature verification. The inconsistency between commands that have `--db` and those that don't makes integration testing difficult. Pattern to follow: see `start` command implementation in cli.py for the `--db` option pattern.

## Reproduction

```bash
# These work:
chrono start "test" --db /tmp/test.db
chrono stop --db /tmp/test.db

# These fail:
chrono project create backend --db /tmp/test.db  # Error: No such option: --db
chrono project list --db /tmp/test.db             # Error: No such option: --db
```

**Claimed-By:** bravo-2
**Claimed-At:** 1773608713

**Completed-At:** 1773608831
