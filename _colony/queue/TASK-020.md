# TASK-020: Test coverage improvement — target 80%+

**Status:** queue
**Assigned:** alpha
**Priority:** P2
**Depends-On:** TASK-001, TASK-003

## Description
Review current test coverage, identify gaps, and add tests to reach 80%+ coverage across the codebase. Run `pytest --cov=chronolog --cov-report=term-missing` to identify uncovered lines, then write tests for the most critical gaps.

## Acceptance Criteria
- [ ] Run coverage report and identify modules below 80%
- [ ] Add tests for uncovered branches in core.py (error paths, edge cases)
- [ ] Add tests for uncovered branches in models.py (edge cases)
- [ ] Add tests for uncovered branches in cli.py (error output, edge cases)
- [ ] Add tests for any uncovered utility functions
- [ ] Overall coverage reaches 80%+ as reported by pytest-cov
- [ ] All new tests pass
- [ ] At least 10 new test cases across modules

## Notes
- Focus on meaningful coverage — test error paths and edge cases, not trivial getters
- Use `pytest --cov=chronolog --cov-report=term-missing` to see exact uncovered lines
- Priority: core.py > cli.py > models.py > utils.py
