#!/usr/bin/env node
// AtlasColony — SessionEnd hook
// Appends a JSON line to the agent's log file when a Claude Code session ends.
// Captures session summary for post-mortem analysis and audit trail.
//
// Hook type: SessionEnd
// Env:       ATLAS_AGENT_ID — the agent instance name (e.g. "alpha-1")
// Stdin:     JSON with { summary, duration_ms, ... }
// Output:    Appends to _colony/logs/<agent-id>.log

const fs = require("fs");
const path = require("path");

function main() {
  const agentId = process.env.ATLAS_AGENT_ID;
  if (!agentId) {
    // No agent ID — skip logging
    process.exit(0);
  }

  // Read session info from stdin
  let sessionInfo = {};
  try {
    const input = fs.readFileSync("/dev/stdin", "utf8").trim();
    if (input) {
      sessionInfo = JSON.parse(input);
    }
  } catch (_err) {
    // Stdin may not be available or may not be JSON — proceed with defaults
  }

  // Resolve project root: walk up from cwd until we find _colony/
  let projectDir = process.cwd();
  while (projectDir !== "/") {
    if (fs.existsSync(path.join(projectDir, "_colony"))) break;
    projectDir = path.dirname(projectDir);
  }

  const logsDir = path.join(projectDir, "_colony", "logs");

  // Ensure logs directory exists
  fs.mkdirSync(logsDir, { recursive: true });

  // Build log entry
  const logEntry = {
    agent: agentId,
    timestamp: new Date().toISOString(),
    summary: sessionInfo.summary || "Session ended (no summary provided)",
    type: "session_end",
  };

  // Append as a JSON line to the agent's log file
  const logPath = path.join(logsDir, agentId + ".log");
  fs.appendFileSync(logPath, JSON.stringify(logEntry) + "\n", "utf8");
}

main();
