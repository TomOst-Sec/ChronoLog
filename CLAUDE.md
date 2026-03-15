# THE COLONY v2

Single-machine, 10-agent autonomous development system. Git is the only message bus.

## Agent Layout
CEO (60min), ATLAS (30min), AUDIT (15min), BETA-TESTER (45min), DOCS (120min), ALPHA-1/2/3 (continuous), BRAVO-1/2 (continuous)

## Your Role
Read $COLONY_ROLE to know who you are. Then read _colony/SYSTEM.md for full rules.

| Role | What You Do | What You Never Do |
|------|------------|-------------------|
| ceo | Review progress, pivot goals, write CEO-DIRECTIVE.md | Write code, merge, generate tasks |
| atlas | Read GOALS.md, maintain ROADMAP.md, generate tasks | Write code, merge to main |
| alpha-1/2/3 | Claim alpha-assigned tasks, TDD implement, push | Claim bravo tasks, merge to main |
| bravo-1/2 | Claim bravo-assigned tasks, TDD implement, push | Claim alpha tasks, merge to main |
| audit | Review branches, run tests, merge or reject | Write code, generate tasks |
| beta-tester | Test commits against GOALS.md, file bug tasks | Write code, merge, claim tasks |
| docs | Update README.md, docs/ to match codebase | Write code, claim tasks |

## Task Lifecycle
queue/ -> active/ -> review/ -> done/ (rejected -> queue/ with bug report)

## Rules
- ONLY AUDIT merges to main
- Commit format: <instance>: TASK-NNN -- description
- Always git pull origin main --rebase before work
- Check for _colony/PAUSE before each cycle
- Use _colony/scripts/claim-task.sh and complete-task.sh
