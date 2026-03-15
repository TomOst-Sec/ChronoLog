# TASK-001: Project scaffolding and package structure

**Status:** review
**Assigned:** alpha
**Priority:** P0
**Depends-On:** none

## Description
Set up the ChronoLog Python project from scratch. Create the package structure, pyproject.toml, Click CLI entrypoint, and pytest configuration. This is the foundation everything else builds on.

## Acceptance Criteria
- [ ] `pyproject.toml` exists with project metadata, Python 3.10+ requirement, dependencies (click, rich), dev dependencies (pytest, pytest-cov), and a console script entry point `chrono = "chronolog.cli:cli"`
- [ ] Package directory `chronolog/` exists with `__init__.py`, `cli.py`, `core.py`, `models.py`, `utils.py` (modules can have minimal placeholder content)
- [ ] `chronolog/cli.py` has a Click group `cli` with a `--version` flag that prints the version
- [ ] `tests/` directory exists with `conftest.py`, `test_cli.py`, `test_core.py`, `test_models.py`
- [ ] `tests/conftest.py` has a fixture for a temporary database path (using `tmp_path`)
- [ ] `pytest` runs successfully with at least one passing test (e.g., test that `chrono --version` outputs correctly)
- [ ] `pip install -e ".[dev]"` works without errors

## Notes
- Version should be "0.1.0"
- Use `[project.scripts]` in pyproject.toml for the CLI entry point
- Keep modules minimal — other tasks will fill in the actual logic
- See GOALS.md for tech stack details

**Claimed-By:** alpha-1
**Claimed-At:** 1773604952

**Completed-At:** 1773605073
