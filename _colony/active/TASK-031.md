# TASK-031: Add notes/annotations to time entries

**Status:** active
**Assigned:** bravo
**Priority:** P2
**Depends-On:** TASK-001, TASK-003

## Description
Add the ability to attach notes to time entries. Notes are additional context beyond the description — useful for recording what was accomplished, blockers encountered, or details for later reference.

## Acceptance Criteria
- [ ] Add `notes` TEXT column to entries table (nullable, default empty string)
- [ ] Schema migration: ALTER TABLE entries ADD COLUMN notes TEXT DEFAULT '' if column doesn't exist
- [ ] `chrono note ID "note text"` CLI command — appends a note to an entry
- [ ] `chrono note ID` with no text shows existing notes for that entry
- [ ] Notes are shown in `chrono list` output (truncated to 30 chars in table view)
- [ ] Notes are included in CSV export
- [ ] Function `add_note(db_path, entry_id: int, note: str) -> TimeEntry`
- [ ] Tests: add note, view note, note in list output, note for non-existent entry
- [ ] At least 5 test cases

## Notes
- Use ALTER TABLE for migration — `init_db` should check if column exists
- Notes append (don't replace) — separate multiple notes with newlines
- Keep it simple — no markdown, just plain text

**Claimed-By:** bravo-1
**Claimed-At:** 1773605976
