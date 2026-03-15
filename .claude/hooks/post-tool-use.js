#!/usr/bin/env node
// AtlasColony — PostToolUse hook
// Writes a heartbeat file after every tool use so the watchdog can detect
// agent liveness without relying on git log scanning (faster, more accurate).
//
// Hook type: PostToolUse
// Env:       ATLAS_AGENT_ID — the agent instance name (e.g. "alpha-1")
// Stdin:     JSON with { tool_name, tool_input, tool_output, success }
// Output:    Heartbeat file at _colony/logs/<agent-id>.heartbeat

const fs = require("fs");
const path = require("path");

function main() {
  const agentId = process.env.ATLAS_AGENT_ID;
  if (!agentId) {
    // No agent ID — skip heartbeat
    process.exit(0);
  }

  // Read tool use info from stdin
  let toolInfo = {};
  try {
    const input = fs.readFileSync("/dev/stdin", "utf8").trim();
    if (input) {
      toolInfo = JSON.parse(input);
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

  // Build heartbeat payload
  const heartbeat = {
    agent: agentId,
    tool: toolInfo.tool_name || "unknown",
    timestamp: Date.now(),
    success: typeof toolInfo.success === "boolean" ? toolInfo.success : true,
  };

  // Write heartbeat file (atomic overwrite)
  const heartbeatPath = path.join(logsDir, agentId + ".heartbeat");
  fs.writeFileSync(heartbeatPath, JSON.stringify(heartbeat) + "\n", "utf8");
}

main();
