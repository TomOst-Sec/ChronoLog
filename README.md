# ChronoLog

A command-line time tracker for developers who want to log their workday without leaving the terminal.

## Status

**Pre-alpha** -- Project scaffolding is in progress. No working code exists yet.

## Vision

ChronoLog will be a local-first CLI tool that lets you start/stop timers, organize time entries by project and tags, generate reports, and export to CSV. All data stays on your machine in a single SQLite database. No cloud, no accounts, no subscriptions.

## Planned Tech Stack

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
