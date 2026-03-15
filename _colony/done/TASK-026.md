# TASK-026: Shell completion support for Click CLI

**Status:** review
**Assigned:** alpha
**Priority:** P2
**Depends-On:** TASK-001

## Description
Enable shell tab-completion for all `chrono` commands. Click has built-in completion support for bash, zsh, and fish. Add custom completions for project names and common options.

## Acceptance Criteria
- [ ] Click shell completion is configured and works for bash and zsh
- [ ] Project names auto-complete for `--project` option (custom completion callback querying DB)
- [ ] Subcommands auto-complete (start, stop, status, list, project, report, config, export)
- [ ] Installation instructions added as `chrono completion` command that prints the appropriate shell script
- [ ] `chrono completion --shell bash` and `chrono completion --shell zsh` output correct activation scripts
- [ ] Tests verifying completion callback returns expected project names
- [ ] At least 3 test cases

## Notes
- Click 8.x has built-in shell completion — use `shell_complete` parameter
- For project name completion, use a callback that queries the database
- Keep it simple — don't complete tags or descriptions

**Claimed-By:** alpha-2
**Claimed-At:** 1773605854

**Completed-At:** 1773605918
