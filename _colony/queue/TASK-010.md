# TASK-010: Edit and delete time entries

**Status:** queue
**Assigned:** bravo
**Priority:** P1
**Depends-On:** TASK-001, TASK-003, TASK-005

## Description
Implement the ability to edit and delete time entries. Users need to modify past entries (fix descriptions, change projects) and remove incorrect entries. Includes core functions and CLI commands.

## Acceptance Criteria
- [ ] Function `edit_entry(db_path, entry_id: int, description: str | None = None, project: str | None = None, tags: list[str] | None = None) -> TimeEntry` — updates specified fields, returns updated entry
- [ ] `edit_entry` raises error if entry_id doesn't exist
- [ ] `edit_entry` raises error if specified project doesn't exist
- [ ] Function `delete_entry(db_path, entry_id: int) -> None` — deletes entry by ID
- [ ] `delete_entry` raises error if entry_id doesn't exist
- [ ] `chrono edit ID --description "new" --project NAME` CLI command
- [ ] `chrono delete ID` CLI command with confirmation prompt (use click.confirm)
- [ ] `chrono delete ID --yes` skips confirmation
- [ ] Tests covering: edit description, edit project, edit non-existent, delete, delete non-existent
- [ ] At least 8 test cases

## Notes
- Only update fields that are explicitly provided (not None)
- Cannot edit start_time or end_time through this command (future feature)
- Deleting a running timer should also stop it
