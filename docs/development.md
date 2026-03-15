# Development Guide

## Prerequisites

- Python 3.10 or later
- pip

## Setup

Once project scaffolding is complete (TASK-001), install in development mode:

```bash
pip install -e ".[dev]"
```

## Running Tests

```bash
pytest
```

With coverage:

```bash
pytest --cov=chronolog --cov-report=term-missing
```

## Project Structure (planned)

```
chronolog/
  __init__.py       # Package init, version
  cli.py            # Click entry points
  core.py           # Business logic
  models.py         # Data models (TimeEntry, Project)
  utils.py          # Helpers
tests/
  conftest.py       # Shared fixtures
  test_cli.py       # CLI tests via CliRunner
  test_core.py      # Core logic tests
  test_models.py    # Model tests
pyproject.toml      # Project metadata and dependencies
```

## Conventions

- **Imports**: Absolute imports only
- **Type hints**: Required on all public functions
- **Docstrings**: Google style on all public functions
- **Tests**: TDD -- write failing tests first, then implement
- **CLI**: Click for commands, Rich for output formatting
- **Database**: SQLite via stdlib `sqlite3`, datetimes stored as ISO 8601 UTC strings
