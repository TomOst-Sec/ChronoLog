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
  backup.py         # Database backup and restore
  cli.py            # Click commands: start, stop, status, list, project, config
  config.py         # JSON config at ~/.chronolog/config.json
  core.py           # Timer, entry, project, and tag business logic
  db.py             # SQLite connection, schema init, get_db_path
  display.py        # Rich formatting helpers for report tables
  exceptions.py     # Custom exception hierarchy (ChronoLogError base)
  export.py         # CSV export for date-range entries
  models.py         # TimeEntry and Project dataclasses
  utils.py          # Helpers (stub)
tests/
  __init__.py
  conftest.py       # Shared fixtures (tmp_db_path)
  test_cli.py       # CLI tests via CliRunner
  test_config.py    # Configuration get/set tests
  test_core.py      # Timer, project, entry CRUD tests
  test_db.py        # Database init, schema, connection tests
  test_exceptions.py # Custom exception tests
  test_integration.py # End-to-end workflow tests
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
- `Project` -- dataclass with `name`, `created_at`, `archived` fields, `to_row()`/`from_row()` for DB serialization

### Core Logic (`core.py`)

**Timer functions:**
- `start_timer(db_path, description, project, tags)` -- creates entry with `end_time=None`, enforces single active timer
- `stop_timer(db_path)` -- sets `end_time` on active entry
- `get_active_timer(db_path)` -- returns running entry or None

**Entry management:**
- `list_entries(db_path, limit)` -- recent entries ordered by start_time desc
- `edit_entry(db_path, entry_id, description, project, tags)` -- update specific fields on an entry
- `delete_entry(db_path, entry_id)` -- remove an entry by ID

**Tags:**
- `list_tags(db_path)` -- all tags with total minutes and entry count

**Project management:**
- `create_project(db_path, name)` -- creates project, validates name (alphanumeric + hyphens, 1-50 chars)
- `list_projects(db_path, include_archived)` -- lists projects, optionally including archived
- `archive_project(db_path, name)` -- archives a project (cannot archive "general")
- `get_project(db_path, name)` -- returns a project by name or None

### CSV Export (`export.py`)
- `export_entries_csv(db_path, from_date, to_date, output_path)` -- exports completed entries in date range to CSV. Columns: date, start_time, end_time, duration_minutes, project, tags, description. Times displayed in local timezone.

### Database Backup (`backup.py`)
- `backup_db(db_path, output_path)` -- copies database to `~/.chronolog/backups/` with timestamp, or custom path
- `restore_db(db_path, backup_path)` -- restores from backup (refuses if timer is running)

### Display Helpers (`display.py`)
- `create_entries_table(entries)` -- Rich Table for time entries (Start, End, Duration, Project, Tags, Description)
- `create_summary_table(summaries)` -- Rich Table for project summaries with bar chart
- `format_report_header(title, date_range)` -- Rich Panel header for reports
- `add_total_row(table, total_minutes)` -- adds bold total row to a table

### Configuration (`config.py`)
- `get_config(config_path)` -- reads `~/.chronolog/config.json`, creates with defaults if missing
- `set_config(key, value, config_path)` -- sets a config value and writes to file
- Default config: `{"default_project": "general"}`

### Exceptions (`exceptions.py`)
- `ChronoLogError` -- base exception
- `TimerAlreadyRunningError`, `NoActiveTimerError` -- timer errors
- `ProjectNotFoundError`, `ProjectExistsError`, `InvalidProjectNameError` -- project errors
- `EntryNotFoundError` -- entry errors

### CLI (`cli.py`)
- `chrono start DESCRIPTION [--project] [--tags]` -- start timer
- `chrono stop` -- stop running timer
- `chrono status` -- show active timer
- `chrono list [--limit N]` -- show recent entries
- `chrono project create/list/archive` -- project management
- `chrono config show/set` -- configuration
- All output uses Rich Console for formatting

## Conventions

- **Imports**: Absolute imports only
- **Type hints**: Required on all public functions
- **Docstrings**: Google style on all public functions
- **Tests**: TDD -- write failing tests first, then implement
- **CLI**: Click for commands, Rich for output formatting
- **Database**: SQLite via stdlib `sqlite3`, datetimes stored as ISO 8601 UTC strings
