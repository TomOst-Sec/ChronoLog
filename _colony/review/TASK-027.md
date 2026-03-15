# TASK-027: Makefile for common development commands

**Status:** review
**Assigned:** bravo
**Priority:** P2
**Depends-On:** TASK-001

## Description
Create a Makefile with targets for common development tasks. This standardizes how the team runs tests, checks coverage, formats code, and installs dependencies.

## Acceptance Criteria
- [ ] `make install` — runs `pip install -e ".[dev]"`
- [ ] `make test` — runs `pytest`
- [ ] `make test-v` — runs `pytest -v`
- [ ] `make coverage` — runs `pytest --cov=chronolog --cov-report=term-missing`
- [ ] `make lint` — runs any configured linters (ruff or flake8 if in deps)
- [ ] `make clean` — removes `__pycache__`, `.coverage`, `.pytest_cache`, `*.egg-info`
- [ ] `make help` — lists all targets with descriptions (default target)
- [ ] Makefile uses `.PHONY` for all targets
- [ ] At least 2 test cases verifying Makefile targets exist and are syntactically valid

## Notes
- Keep it simple — standard GNU Make, no exotic features
- Use `@` prefix to suppress command echo for clean output
- `help` target can use `grep` on the Makefile itself to list targets

**Claimed-By:** bravo-2
**Claimed-At:** 1773605943

**Completed-At:** 1773606002
