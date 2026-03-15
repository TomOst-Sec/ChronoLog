# TASK-025: Cross-platform path handling and Windows compatibility

**Status:** queue
**Assigned:** bravo
**Priority:** P2
**Depends-On:** TASK-001

## Description
Ensure all file path handling works correctly on Windows, macOS, and Linux. GOALS.md requires cross-platform support. Review and fix any hardcoded path separators, home directory lookups, or platform-specific assumptions.

## Acceptance Criteria
- [ ] All path construction uses `pathlib.Path` instead of string concatenation
- [ ] `get_db_path()` uses `Path.home() / ".chronolog" / "chrono.db"` (platform-safe)
- [ ] `get_config_path()` uses `Path.home() / ".chronolog" / "config.json"` (platform-safe)
- [ ] Directory creation uses `Path.mkdir(parents=True, exist_ok=True)`
- [ ] No hardcoded `/` or `\\` path separators in source code
- [ ] Tests verify path construction produces valid paths on current platform
- [ ] At least 4 test cases

## Notes
- `pathlib.Path` handles platform differences automatically
- `Path.home()` works on all platforms
- This is mostly a refactor — review existing code and update path handling
- If paths already use pathlib, verify and add tests confirming cross-platform behavior
