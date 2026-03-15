# ChronoLog

A command-line time tracker for developers who want to log their workday without leaving the terminal.

## Status

**Pre-alpha** -- Project scaffolding is in place. Core features (timer, projects, database) are under active development.

## Install

Requires Python 3.10+.

```bash
git clone <repo-url>
cd chronolog
pip install -e ".[dev]"
```

## Usage

Currently only the CLI skeleton is available:

```bash
chrono --version    # prints 0.1.0
chrono --help       # shows available commands
```

Timer, project management, and database commands are in progress and not yet available.

## Tech Stack

- Python 3.10+
- SQLite (built-in `sqlite3` module)
- [Click](https://click.palletsprojects.com/) for CLI
- [Rich](https://rich.readthedocs.io/) for terminal output
- [pytest](https://docs.pytest.org/) for testing

## Roadmap

### M1: Core Timer (current)
- Start/stop timer with project assignment
- Project management (create, list, archive)
- SQLite storage with auto-creation

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
