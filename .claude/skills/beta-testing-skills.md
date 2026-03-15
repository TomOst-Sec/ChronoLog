---
description: "Beta testing discipline — pytest execution, goal alignment verification, regression detection, bug filing"
---

# Beta Testing Skills (Python)

## 1. Test Execution

### Full Suite
```bash
pytest --tb=long -v
```
Always run with verbose + long tracebacks. You need the details to file accurate bugs.

### Coverage
```bash
pytest --cov=chronolog --cov-report=term-missing
```
Track coverage trends. If coverage drops after a merge, that is a finding worth reporting.

### Targeted Testing
```bash
# Test a specific module
pytest tests/test_cli.py -v

# Test with keyword filter
pytest -k "test_add_entry" -v

# Stop on first failure for quick iteration
pytest -x --tb=short
```

## 2. Goal Alignment Verification

After tests pass, verify that recent changes serve the project goals:

1. Read `_colony/GOALS.md` — what are we building toward?
2. Read `_colony/done/` — what was recently merged?
3. For each merged task, ask:
   - Does this move toward a stated goal?
   - Does the implementation match the task spec's acceptance criteria?
   - Are there side effects not covered by tests?

## 3. Regression Detection

### What Counts as a Regression
- A test that passed yesterday fails today
- A CLI command that worked before produces errors
- Performance degradation (command takes noticeably longer)
- Output format changed without a corresponding task

### How to Detect
1. Run the full test suite after every merge
2. Test all CLI commands with typical inputs
3. Test edge cases: empty input, missing files, bad arguments
4. Compare error messages — are they still helpful?

## 4. Bug Filing Protocol

When you find a bug, create a task file:

```markdown
# TASK-NNN: BUG — <short description>

**Status:** queue
**Assigned:** alpha | bravo
**Priority:** P0 (regression) | P1 (new bug) | P2 (cosmetic)

## Reproduction Steps
1. Exact command or action
2. With exact input
3. In exact environment state

## Expected Behavior
What should happen.

## Actual Behavior
What actually happens. Include full error output.

## Stack Trace
```
paste full traceback here
```

## Environment
- Python version
- OS
- Relevant config
```

### Bug Priority Guide
- **P0:** Breaks existing functionality. Was working, now broken. Blocks other work.
- **P1:** New feature does not work as specified. Does not block others.
- **P2:** Cosmetic issue, unclear error message, minor UX problem.

## 5. Test Report Format

Write `_colony/TEST-REPORT.md` each cycle:

```markdown
# Test Report — <timestamp>

## Summary
- Tests: X passed, Y failed, Z skipped
- Coverage: NN%
- Goal alignment: OK | DRIFT | BLOCKED

## Failures
### test_name_here
- **File:** tests/test_foo.py:42
- **Error:** <brief description>
- **Bug filed:** TASK-NNN

## Coverage Changes
- chronolog/core.py: 85% -> 82% (regression)
- chronolog/cli.py: 90% (stable)

## Goal Alignment Notes
- GOAL-1: on track, 3/5 tasks done
- GOAL-2: blocked, dependency not merged

## Bugs Filed This Cycle
- TASK-NNN: <description>
```
