---
description: "Documentation discipline — keep docs in sync with code, never document unimplemented features"
---

# Documentation Skills

## Cardinal Rule
**Never document features that do not exist.** If it is not merged to main and passing tests, it does not belong in the docs. Verify against the code, not the roadmap.

## 1. README Maintenance

### What Goes in README.md
- Project name and one-line description
- Installation instructions (tested, working)
- Usage examples for every CLI command that exists
- Configuration options that are currently supported
- Contributing guidelines

### What Does NOT Go in README.md
- Planned features
- Features on task branches not yet merged
- Aspirational architecture diagrams
- TODO items

### Verification
Before committing any README change:
```bash
# Verify CLI commands documented actually work
chronolog --help
chronolog <subcommand> --help

# Verify installation instructions work
pip install -e .
```

## 2. docs/ Directory

Keep it minimal and accurate:
- `docs/usage.md` — expanded usage guide
- `docs/architecture.md` — how the code is structured (match reality)
- `docs/contributing.md` — how to contribute

## 3. Sync Protocol

Each cycle:
1. Read `_colony/done/` to see what changed
2. Read the actual source code for current behavior
3. Diff docs against code — are there mismatches?
4. Update docs to match code
5. Remove docs for features that were reverted

## 4. Style
- Clear, direct language
- Code examples over prose
- One concept per section
- Keep it short — developers skim, they do not read
