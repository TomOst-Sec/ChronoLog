# ChronoLog

A command-line time tracker for developers who want to log their workday without leaving the terminal. All data stays on your machine in a single SQLite database -- no cloud, no accounts, no subscriptions.

## Status

**Pre-alpha (M1 in progress)** -- Core timer logic, project management, and database layer are implemented. CLI commands are being wired up.

## Install

Requires Python 3.10+.

```bash
git clone <repo-url>
cd chronolog
pip install -e ".[dev]"
```

## Usage

The CLI skeleton is available:

```bash
chrono --version    # prints 0.1.0
chrono --help       # shows available commands
```

CLI commands for `start`, `stop`, `status`, and `project` management are under development and not yet available as user-facing commands.

## What's Implemented

- **Data models** -- `TimeEntry` and `Project` dataclasses with `to_row()`/`from_row()` for SQLite serialization
- **SQLite database** -- Auto-creates at `~/.chronolog/chrono.db` on first use. Schema: `entries` table and `projects` table. Default "general" project created automatically.
- **Timer core logic** -- `start_timer()`, `stop_timer()`, `get_active_timer()` with single-active-timer enforcement and project validation
- **Project management** -- `create_project()`, `list_projects()`, `archive_project()`, `get_project()` with name validation (alphanumeric + hyphens, max 50 chars)
- **Test suite** -- 35+ tests covering models, database, core logic, and project CRUD

## Tech Stack

- Python 3.10+
- SQLite (built-in `sqlite3` module)
- [Click](https://click.palletsprojects.com/) for CLI
- [Rich](https://rich.readthedocs.io/) for terminal output
- [pytest](https://docs.pytest.org/) for testing

## Data Storage

All data is stored locally in `~/.chronolog/chrono.db` (SQLite). The database and its parent directory are created automatically on first use. Times are stored in UTC as ISO 8601 strings.

## Roadmap

### M1: Core Timer (current)
- ~~SQLite database with schema and connection management~~
- ~~Data models (TimeEntry, Project)~~
- ~~Start/stop timer core logic~~
- ~~Project management CRUD~~
- CLI commands for timer and projects (in review)

### M2: Reporting & Tags
- Tagging system
- Daily, weekly, and date-range reports
- Rich terminal output for reports

### M3: Polish
- CSV export
- Edit/delete entries
- Configuration management

## License

TBD
