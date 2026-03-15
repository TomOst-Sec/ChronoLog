# TASK-049: Add backup and restore CLI commands

**Status:** review
**Assigned:** bravo
**Priority:** P2
**Depends-On:** none

## Description
Wire up `backup.backup_db()` and `backup.restore_db()` to CLI commands under a `chrono db` group.

## Acceptance Criteria
- [ ] `chrono db backup` creates a timestamped backup in `~/.chronolog/backups/`
- [ ] `chrono db backup --output /path/to/file.db` backs up to a custom location
- [ ] `chrono db restore /path/to/backup.db` restores from a backup file
- [ ] Restore prompts for confirmation before overwriting
- [ ] Restore fails with clear error if a timer is currently running
- [ ] Restore fails with clear error if backup file doesn't exist
- [ ] Success messages show the backup/restore file path
- [ ] `--db` hidden option for testability
- [ ] Tests exist for both CLI commands
- [ ] `pytest` passes clean

## Notes
- `backup.backup_db()` and `backup.restore_db()` already exist
- Use `click.confirm()` for restore confirmation
- `db` should be a Click group: `chrono db backup`, `chrono db restore`

**Claimed-By:** bravo-1
**Claimed-At:** 1773608455

**Completed-At:** 1773608563
