# TASK-029: Database backup and restore commands

**Status:** review
**Assigned:** alpha
**Priority:** P2
**Depends-On:** TASK-001, TASK-003

## Description
Implement `chrono backup` and `chrono restore` for database backup. Since all data is in a single SQLite file, backup is just a file copy. This gives users peace of mind.

## Acceptance Criteria
- [ ] `chrono backup` copies `~/.chronolog/chrono.db` to `~/.chronolog/backups/chrono_YYYYMMDD_HHMMSS.db`
- [ ] Creates `backups/` directory if it doesn't exist
- [ ] Prints backup path on success
- [ ] `chrono backup --output PATH` copies to a custom location
- [ ] `chrono restore PATH` copies backup file to `chrono.db` (with confirmation prompt)
- [ ] Restore refuses if a timer is currently running (data safety)
- [ ] Tests: backup creates file, backup custom path, restore, restore while running
- [ ] At least 5 test cases

## Notes
- Use `shutil.copy2` for file copy (preserves metadata)
- Backup timestamp uses local time for readability
- This is a simple file operation — no special SQLite handling needed
- Consider using `sqlite3.backup()` API for a hot-copy approach

**Claimed-By:** alpha-3
**Claimed-At:** 1773605926

**Completed-At:** 1773606015
