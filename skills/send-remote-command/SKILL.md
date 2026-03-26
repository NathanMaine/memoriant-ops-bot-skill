# send-remote-command

Send a command or prompt to a remote AI agent (Claude Code, Codex CLI, or Gemini CLI) via MOPS, and stream the response back. Supports targeting a specific agent, starting named sessions, and running background tasks.

## Trigger

User says something like:
- `/send-remote-command`
- "send a command to my agent"
- "run this prompt on codex-agent"
- "tell my gemini agent to do X"
- "start a background task on the remote agent"

## What This Skill Does

Routes a user-provided prompt to a specified MOPS agent (or the default main agent), executes it via the agent's CLI subprocess, and streams the response. Supports:
- Direct synchronous execution (response streamed in real time)
- Named session routing (send to a specific conversation context)
- Background task delegation (fire-and-forget with result notification)

## Step-by-Step Instructions

### Step 1: Identify Target Agent

Ask: "Which agent should receive this command? (default: main)"

Load `~/.mops/agents.json` and validate the target agent exists and has status RUNNING or IDLE. If STOPPED, ask the user to start it first or offer to start it.

### Step 2: Get the Command

Ask: "What command or prompt do you want to send?"

Accept:
- A direct prompt string
- A file path (read the file content as the prompt)
- A multi-line prompt (user can paste)

### Step 3: Select Execution Mode

Ask: "How should this run?"

| Mode | When to use | Behavior |
|------|-------------|----------|
| Sync (default) | Short tasks, interactive | Stream response, wait for completion |
| Session | Continuing a conversation | Route to named session context |
| Background | Long-running tasks | Fire-and-forget, notify when done |

### Step 4: Sync Execution

For synchronous mode, construct the CLI command based on provider:

**Claude Code:**
```bash
claude --print "<prompt>"
```

**Codex CLI:**
```bash
codex exec "<prompt>"
```

**Gemini CLI:**
```bash
gemini prompt "<prompt>"
```

Stream the output line by line. Show a spinner while waiting.

### Step 5: Session Routing

For session mode:
1. List existing named sessions from `~/.mops/named_sessions.json`
2. Ask user to select a session or create a new one: "Session name:"
3. Prepend session context marker to the prompt
4. Execute via the appropriate CLI

### Step 6: Background Task

For background mode:
1. Generate a task ID: `task-<timestamp>`
2. Write task entry to `~/.mops/tasks.json`:
```json
{
  "id": "task-1711369921",
  "agent": "<name>",
  "prompt": "<prompt>",
  "status": "QUEUED",
  "created_at": "<ISO>",
  "result": null
}
```
3. Print: "Task queued: task-1711369921. Run /check-status to monitor."
4. Note: actual background execution requires MOPS daemon to be running.

### Step 7: Stream Response

For sync mode, print the CLI output as it arrives. After completion, print:
```
─────────────────────────────────────────
Agent: <name> | Provider: <provider>
Duration: <N>s | Session: <session or none>
─────────────────────────────────────────
```

### Step 8: Log the Interaction

Append to `~/.mops/workspace/memory_system/interactions.md`:
```markdown
## <ISO timestamp>
**Agent:** <name>
**Prompt:** <prompt>
**Mode:** sync / session / background
**Status:** completed / queued
```

## Error Handling

| Error | Response |
|-------|----------|
| Agent not found | "Agent '<name>' not in registry. Run /manage-agents to add it." |
| CLI not found | "Provider CLI '<provider>' not installed. Install it and try again." |
| CLI timeout | "Command timed out after <N>s. Try background mode for long tasks." |
| Agent STOPPED | "Agent '<name>' is stopped. Start it via /check-status or /manage-agents." |
