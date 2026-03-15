# TASK-012: End-to-end integration tests for M1 workflow

**Status:** queue
**Assigned:** bravo
**Priority:** P1
**Depends-On:** TASK-001, TASK-003, TASK-005

## Description
Write integration tests that verify the complete M1 user workflow through the CLI. These tests catch issues that unit tests miss — like module wiring, database state transitions, and CLI argument parsing working together.

## Acceptance Criteria
- [ ] Test file `tests/test_integration.py` exists
- [ ] Test: full timer workflow — start, status (shows running), stop, list (shows completed entry)
- [ ] Test: project workflow — create project, start timer with project, stop, verify entry has correct project
- [ ] Test: error cases — start while running, stop while idle, start with non-existent project
- [ ] Test: default project — starting timer without --project uses "general"
- [ ] Test: tags workflow — start with tags, stop, list shows tags correctly
- [ ] All tests use Click's CliRunner for CLI invocation
- [ ] All tests use a temporary database (not user's real DB) via tmp_path or monkeypatch
- [ ] At least 6 integration test cases
- [ ] All tests pass with `pytest tests/test_integration.py -v`

## Notes
- Use `monkeypatch` or environment variable to override the database path to tmp_path
- These tests should invoke CLI commands as a user would, not call core functions directly
- Import and use the Click CliRunner
- If dependent tasks aren't merged yet, this task is blocked — wait for TASK-005 to land
