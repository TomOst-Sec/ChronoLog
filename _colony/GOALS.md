# Project Goals

> ATLAS reads this to generate the roadmap and tasks.

## Product Description

ChronoLog is an open-source command-line time tracker written in Python that developers use to log how they spend their workday without leaving the terminal. It stores all data in a single local SQLite database, supports projects and tags, generates daily/weekly reports, and exports to CSV. No cloud, no accounts, no subscriptions — just `chrono start "fixing auth bug" --project backend --tags bugfix` and get back to work.

## Tech Stack

- Python 3.10+
- SQLite via built-in `sqlite3` module (no external DB dependencies)
- Click for CLI framework
- Rich for terminal output (tables, colors, progress bars)
- pytest for testing

## Features

1. **Start/Stop Timer** — `chrono start "task description" --project NAME --tags tag1,tag2` begins tracking. `chrono stop` ends the current session with a summary. `chrono status` shows what's currently running. Only one timer can be active at a time.

2. **Project Management** — `chrono project create NAME`, `chrono project list`, `chrono project archive NAME`. Projects group time entries. Every time entry must belong to a project. Default project is "general" if none specified.

3. **Tagging System** — Time entries can have zero or more tags. Tags are free-form strings. `chrono tags` lists all used tags with total time per tag. Tags enable cross-project reporting.

4. **Daily Report** — `chrono report today` shows all time entries for today in a Rich table: start time, end time, duration, project, tags, description. `chrono report yesterday` does the same for yesterday. Total hours at the bottom.

5. **Weekly Report** — `chrono report week` shows a breakdown by project for the current week. Each project shows total hours and percentage of the week. Includes a bar chart visualization using Rich.

6. **Date Range Report** — `chrono report --from 2024-01-01 --to 2024-01-31` for custom ranges. Supports both daily detail view and project summary view.

7. **CSV Export** — `chrono export --from DATE --to DATE --output file.csv` exports all time entries in the range to CSV. Columns: date, start_time, end_time, duration_minutes, project, tags, description.

8. **Edit/Delete Entries** — `chrono edit ID --description "new desc" --project new-project` modifies a past entry. `chrono delete ID` removes an entry with confirmation. `chrono list` shows recent entries with IDs for reference.

9. **SQLite Storage** — All data stored in `~/.chronolog/chrono.db`. Auto-created on first run. Schema: `entries` table (id, description, project, tags, start_time, end_time), `projects` table (name, created_at, archived). Migrations for schema changes.

10. **Configuration** — `chrono config set default_project NAME` sets the default project. `chrono config show` displays current settings. Config stored in `~/.chronolog/config.json`. Sensible defaults for everything.

## Constraints

- Zero external services. Everything is local.
- Single SQLite file. No Redis, no Postgres, no files-as-database.
- Must work on macOS, Linux, and Windows.
- All times stored in UTC, displayed in local timezone.
- CLI response time < 100ms for all commands.
- Database must handle 10,000+ entries without degrading.

## Out of Scope

- GUI or web interface
- Team/collaboration features
- Cloud sync
- Invoice generation
- Calendar integration
- Mobile app

## Milestones

### M1: Core Timer (first)
- Features 1, 2, 9 (start/stop, projects, SQLite storage)
- Basic CLI with Click
- pytest setup with at least 80% coverage target
- README with install + usage

### M2: Reporting & Tags (second)
- Features 3, 4, 5, 6 (tags, daily/weekly/range reports)
- Rich terminal output
- Report formatting

### M3: Polish (third)
- Features 7, 8, 10 (CSV export, edit/delete, config)
- Error handling edge cases
- Final README
