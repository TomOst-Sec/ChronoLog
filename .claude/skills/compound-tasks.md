---
description: "Multi-step task execution using compound engineering methodology"
---

# Compound Task Execution

When a task file contains multiple acceptance criteria or the word "multi-step":

## 1. Spec Phase
Restate the requirements in your own words. List every acceptance criterion.
If anything is ambiguous, note it explicitly — don't guess.

## 2. Plan Phase
Break the work into ordered sub-steps. Identify dependencies between steps.
Each sub-step should be independently committable and testable.

Example:
```
Sub-step 1: Create the database migration (no deps)
Sub-step 2: Add the model/types (depends on 1)
Sub-step 3: Write the handler (depends on 2)
Sub-step 4: Add input validation (depends on 3)
Sub-step 5: Write tests for all of the above (depends on 1-4)
```

## 3. Implement Phase
Execute each sub-step in order. After each one:
- Run tests to confirm nothing broke
- Commit with a descriptive message referencing the sub-step
- Do NOT move to the next sub-step if current tests fail

## 4. Verify Phase
After all sub-steps are done:
- Run the FULL test suite (not just your new tests)
- Go back to the spec from Phase 1 — check every acceptance criterion
- If any criterion is not met, go back to Phase 3 for that specific item
- Only move the task to review/ when ALL criteria pass

## Using Engram Throughout
- **Spec phase:** call `recall` to find relevant past decisions about this area
- **Plan phase:** call `search_code` to find existing patterns to follow
- **Implement phase:** call `get_conventions` to match team style
- **Verify phase:** call `remember` to persist what was learned

## Rules
- Never skip Phases 1 and 2. They prevent scope drift and rework.
- Each sub-step gets its own commit. No monolithic commits.
- If Phase 2 reveals the task is too large (>5 sub-steps), note it in the task file but proceed anyway — let the planner break it up next time.
- Time budget: spend ~10% on spec, ~15% on plan, ~60% on implement, ~15% on verify.
