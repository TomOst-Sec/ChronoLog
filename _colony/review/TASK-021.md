# TASK-021: CLI help text and user experience polish

**Status:** review
**Assigned:** bravo
**Priority:** P2
**Depends-On:** TASK-001

## Description
Ensure all CLI commands have clear, helpful `--help` output and consistent error messaging. Add a top-level help text to the `chrono` command. Polish the user experience of all existing commands.

## Acceptance Criteria
- [ ] Main `chrono` command has a descriptive help text explaining what ChronoLog is
- [ ] All subcommands (`start`, `stop`, `status`, `list`, `project`, `report`, `config`, `export`, `edit`, `delete`) have descriptive help strings
- [ ] All options and arguments have help text in Click decorators
- [ ] Error messages are consistent: red text, no tracebacks, actionable suggestions
- [ ] `chrono` with no arguments shows help (not an error)
- [ ] Add `--verbose` / `-v` flag to main group for debug output (optional, stored in Click context)
- [ ] Tests: verify `--help` output contains expected text for each command
- [ ] At least 5 test cases

## Notes
- Use Click's `help` parameter on `@click.command()` and `@click.option()`
- Use Rich.Console for colored error output
- Keep help text concise — one line per command in the group listing

**Claimed-By:** bravo-2
**Claimed-At:** 1773605842

**Completed-At:** 1773605917
