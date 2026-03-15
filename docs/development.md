# Development Guide

## Prerequisites

- Python 3.10 or later
- pip

## Setup

Install in development mode:

```bash
pip install -e ".[dev]"
```

This installs the `chrono` CLI command and all dependencies (Click, Rich, pytest, pytest-cov).

## Running Tests

```bash
pytest
```

With coverage:

```bash
pytest --cov=chronolog --cov-report=term-missing
```

## Project Structure

```
chronolog/
  __init__.py       # Package init, version (0.1.0)
  cli.py            # Click group with --version flag
  core.py           # Timer logic: start_timer, stop_timer, get_active_timer
  db.py             # SQLite connection, schema init, get_db_path
  models.py         # TimeEntry and Project dataclasses
  utils.py          # Helpers (stub)
tests/
  __init__.py
  conftest.py       # Shared fixtures (tmp_db_path)
  test_cli.py       # CLI tests via CliRunner
  test_core.py      # Timer start/stop/status tests
  test_models.py    # TimeEntry/Project serialization tests
pyproject.toml      # Project metadata and dependencies
.gitignore          # Python/venv ignores
```

## Architecture

### Database Layer (`db.py`)
- `get_db_path()` -- returns `~/.chronolog/chrono.db`, creates directory if needed
- `get_connection(db_path)` -- SQLite connection with `Row` factory
- `init_db(db_path)` -- creates tables (idempotent), inserts default "general" project

### Data Models (`models.py`)
- `TimeEntry` -- dataclass with `duration`, `duration_minutes` properties, `to_row()`/`from_row()` for DB serialization. Tags stored as comma-separated strings in DB.
- `Project` -- dataclass with `name`, `created_at`, `archived` fields

### Core Logic (`core.py`)
- `start_timer(db_path, description, project, tags)` -- creates entry with `end_time=None`, enforces single active timer
- `stop_timer(db_path)` -- sets `end_time` on active entry
- `get_active_timer(db_path)` -- returns running entry or None

## Conventions

- **Imports**: Absolute imports only
- **Type hints**: Required on all public functions
- **Docstrings**: Google style on all public functions
- **Tests**: TDD -- write failing tests first, then implement
- **CLI**: Click for commands, Rich for output formatting
- **Database**: SQLite via stdlib `sqlite3`, datetimes stored as ISO 8601 UTC strings
