# TASK-003: SQLite database initialization and schema

**Status:** active
**Assigned:** alpha
**Priority:** P0
**Depends-On:** TASK-001

## Description
Implement the SQLite database layer in `chronolog/core.py` (or a new `chronolog/db.py` if preferred). Handle database creation, connection management, and schema initialization. The database file lives at `~/.chronolog/chrono.db` and should be auto-created on first run.

## Acceptance Criteria
- [ ] Function `get_db_path()` returns `~/.chronolog/chrono.db` (expanduser), creating the `~/.chronolog/` directory if it doesn't exist
- [ ] Function `get_connection(db_path)` returns a sqlite3 Connection with row_factory set to sqlite3.Row
- [ ] Function `init_db(db_path)` creates the database with two tables:
  - `entries`: id INTEGER PRIMARY KEY AUTOINCREMENT, description TEXT NOT NULL, project TEXT NOT NULL DEFAULT 'general', tags TEXT DEFAULT '', start_time TEXT NOT NULL, end_time TEXT, created_at TEXT NOT NULL
  - `projects`: name TEXT PRIMARY KEY, created_at TEXT NOT NULL, archived INTEGER DEFAULT 0
- [ ] `init_db` inserts a default "general" project if it doesn't already exist
- [ ] `init_db` is idempotent — safe to call multiple times (use CREATE TABLE IF NOT EXISTS)
- [ ] Tests use a temporary database file (via tmp_path fixture), NOT the user's real database
- [ ] At least 5 test cases covering: db creation, schema verification, idempotency, default project, connection factory

## Notes
- Store datetimes as ISO 8601 strings in SQLite
- Use `sqlite3.Row` as row_factory so queries return dict-like rows
- The db module should be usable by both core.py and cli.py

**Claimed-By:** alpha-2
**Claimed-At:** 1773605040
