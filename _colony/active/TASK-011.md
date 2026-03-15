# TASK-011: Configuration system

**Status:** active
**Assigned:** alpha
**Priority:** P1
**Depends-On:** TASK-001

## Description
Implement the ChronoLog configuration system. Config is stored in `~/.chronolog/config.json`. Users can set defaults (like default project) and view current settings. This is Feature 10 from GOALS.md.

## Acceptance Criteria
- [ ] Config file stored at `~/.chronolog/config.json` (same directory as the database)
- [ ] Function `get_config(config_path: Path | None = None) -> dict` — reads config, returns defaults if file doesn't exist
- [ ] Function `set_config(key: str, value: str, config_path: Path | None = None) -> None` — sets a config value and writes to file
- [ ] Default config: `{"default_project": "general"}`
- [ ] `chrono config show` displays all current settings in a Rich table
- [ ] `chrono config set KEY VALUE` updates a config value
- [ ] Config is used by `start_timer` — if no `--project` is specified, use default_project from config
- [ ] Tests covering: default config creation, get/set, config show CLI, config set CLI, integration with start_timer default
- [ ] At least 6 test cases

## Notes
- Use `json` module for serialization
- Config file should be auto-created with defaults on first read
- Only support string values for now (no nested config)
- Valid keys: `default_project` (can add more later)

**Claimed-By:** alpha-3
**Claimed-At:** 1773605339
