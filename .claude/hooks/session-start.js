#!/usr/bin/env node
// AtlasColony — SessionStart hook
// Reads _colony/active/ for the task claimed by this agent and injects it
// as context into the Claude Code session.
//
// Hook type: SessionStart
// Env:       ATLAS_AGENT_ID — the agent instance name (e.g. "alpha-1")
// Output:    JSON array of context items to inject into the session

const fs = require("fs");
const path = require("path");

function main() {
  const agentId = process.env.ATLAS_AGENT_ID;
  if (!agentId) {
    // No agent ID — nothing to inject
    process.exit(0);
  }

  // Resolve project root: walk up from cwd until we find _colony/
  let projectDir = process.cwd();
  while (projectDir !== "/") {
    if (fs.existsSync(path.join(projectDir, "_colony"))) break;
    projectDir = path.dirname(projectDir);
  }

  const activeDir = path.join(projectDir, "_colony", "active");
  if (!fs.existsSync(activeDir)) {
    // No active directory — colony not initialized
    process.exit(0);
  }

  // Scan active/ for task files claimed by this agent
  const taskFiles = fs.readdirSync(activeDir).filter(function (f) {
    return f.startsWith("TASK-") && f.endsWith(".md");
  });

  const injectedContext = [];

  for (const taskFile of taskFiles) {
    const filePath = path.join(activeDir, taskFile);
    let content;
    try {
      content = fs.readFileSync(filePath, "utf8");
    } catch (_err) {
      continue;
    }

    // Check if this task is claimed by our agent
    // Look for **Claimed-By:** <agentId> in the task metadata
    const claimedByMatch = content.match(
      /^\*\*Claimed-By:\*\*\s*(.+)/m
    );
    if (!claimedByMatch) continue;

    const claimedBy = claimedByMatch[1].trim();
    if (claimedBy !== agentId) continue;

    // This task belongs to us — inject it as session context
    injectedContext.push({
      type: "text",
      title: "Active Task: " + taskFile,
      content:
        "You are " +
        agentId +
        ". Your currently assigned task:\n\n" +
        "--- " +
        taskFile +
        " ---\n" +
        content +
        "\n--- end ---\n\n" +
        "Implement this task. Follow the task spec exactly. " +
        "When done, run: ./scripts/complete-task.sh " +
        taskFile +
        " " +
        agentId,
    });
  }

  if (injectedContext.length === 0) {
    // No tasks claimed by this agent — nothing to inject
    process.exit(0);
  }

  // Output context items as JSON for Claude Code to consume
  process.stdout.write(JSON.stringify(injectedContext, null, 2) + "\n");
}

main();
