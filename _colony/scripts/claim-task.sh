#!/bin/bash
set -euo pipefail
TASK="${1:?Usage: claim-task.sh TASK-NNN.md <instance>}"
INSTANCE="${2:?Usage: claim-task.sh TASK-NNN.md <instance>}"
cd "$(git rev-parse --show-toplevel)"
if [ ! -f "_colony/queue/$TASK" ]; then echo "ERROR: $TASK not in queue"; exit 1; fi
TEAM="${COLONY_TEAM:-$(echo "$INSTANCE" | sed 's/-[0-9]*$//')}"
ASSIGNED=$(grep -i "Assigned" "_colony/queue/$TASK" | head -1 | tr -d '* ' | cut -d: -f2 | xargs)
if [ -n "$ASSIGNED" ] && [ "$ASSIGNED" != "$TEAM" ]; then echo "ERROR: assigned to $ASSIGNED not $TEAM"; exit 1; fi
mv "_colony/queue/$TASK" "_colony/active/$TASK"
sed -i "s/Status:.*/Status:** active/" "_colony/active/$TASK" 2>/dev/null || true
printf '\n**Claimed-By:** %s\n**Claimed-At:** %s\n' "$INSTANCE" "$(date +%s)" >> "_colony/active/$TASK"
git add "_colony/queue/$TASK" "_colony/active/$TASK"
git commit -m "$INSTANCE: claimed $TASK"
git push origin main || { git reset --soft HEAD~1; git checkout -- _colony/; exit 1; }
echo "OK: $INSTANCE claimed $TASK"
