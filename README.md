# ChronoLog

A command-line time tracker for developers who want to log their workday without leaving the terminal. All data stays on your machine in a single SQLite database -- no cloud, no accounts, no subscriptions.

## Status

**Pre-alpha (M1 nearing completion)** -- Timer, project management, entry listing, and configuration are functional via CLI.

## Install

Requires Python 3.10+.

```bash
git clone <repo-url>
cd chronolog
pip install -e ".[dev]"
```

## Usage

### Timer

```bash
chrono start "fixing auth bug" --project backend --tags bugfix,urgent
chrono status              # show what's currently running
chrono stop                # stop the timer and see summary
```

Only one timer can be active at a time. If no `--project` is specified, the "general" project is used.

### Listing Entries

```bash
chrono list                # show 10 most recent entries
chrono list --limit 20     # show more entries
```

Shows entry ID, description, project, start time, and duration in a Rich table. Running entries show elapsed time.

### Projects

```bash
chrono project create backend    # create a new project
chrono project list              # list active projects
chrono project list --all        # include archived projects
chrono project archive backend   # archive a project
```

The "general" project is created automatically and cannot be archived.

### Configuration

```bash
chrono config show          # display current settings
chrono config set default_project backend
```

Config is stored at `~/.chronolog/config.json`.

### Other

```bash
chrono --version    # prints 0.1.0
chrono --help       # shows available commands
```

## Tech Stack

- Python 3.10+
- SQLite (built-in `sqlite3` module)
- [Click](https://click.palletsprojects.com/) for CLI
- [Rich](https://rich.readthedocs.io/) for terminal output
- [pytest](https://docs.pytest.org/) for testing

## Data Storage

All data is stored locally in `~/.chronolog/chrono.db` (SQLite). The database and its parent directory are created automatically on first use. Times are stored in UTC as ISO 8601 strings.

Configuration is stored at `~/.chronolog/config.json`.

## Roadmap

### M1: Core Timer (complete)
- ~~SQLite database with schema and connection management~~
- ~~Data models (TimeEntry, Project)~~
- ~~Start/stop timer core logic~~
- ~~Project management CRUD~~
- ~~CLI commands for timer (start/stop/status)~~
- ~~CLI commands for project management~~
- ~~List recent entries~~
- ~~Configuration system~~
- ~~Custom exception classes~~
- ~~Integration tests~~

### M2: Reporting & Tags
- Tagging system
- Daily, weekly, and date-range reports
- Rich terminal output for reports

### M3: Polish
- CSV export
- Edit/delete entries
- Final documentation

## License

TBD
