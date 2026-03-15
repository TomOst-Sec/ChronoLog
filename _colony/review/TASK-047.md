# TASK-047: Add edit and delete entry CLI commands

**Status:** review
**Assigned:** bravo
**Priority:** P1
**Depends-On:** none

## Description
Wire up the existing `edit_entry()` and `delete_entry()` functions from `core.py` to CLI commands. `chrono edit ID` modifies a past entry. `chrono delete ID` removes an entry with confirmation.

## Acceptance Criteria
- [ ] `chrono edit ID --description "new desc"` updates the description
- [ ] `chrono edit ID --project new-project` updates the project
- [ ] `chrono edit ID --tags "tag1,tag2"` updates the tags
- [ ] Multiple edit flags can be combined in one command
- [ ] `chrono delete ID` prompts for confirmation before deleting
- [ ] `chrono delete ID --yes` skips confirmation
- [ ] Both commands show clear error if entry ID doesn't exist
- [ ] `--db` hidden option for testability
- [ ] Tests exist for both CLI commands
- [ ] `pytest` passes clean

## Notes
- `core.edit_entry()` and `core.delete_entry()` already exist — just wire them to Click
- Use `click.confirm()` for delete confirmation
- Show the updated entry after successful edit
- Follow error handling patterns in existing CLI commands (catch RuntimeError, print with Rich)

**Claimed-By:** bravo-1
**Claimed-At:** 1773608322

**Completed-At:** 1773608429
