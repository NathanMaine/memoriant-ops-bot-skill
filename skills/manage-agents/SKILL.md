# manage-agents

List, add, remove, and configure sub-agents in a MOPS (Multi-provider Ops Bot) workspace. Control which AI provider each agent uses and manage agent lifecycle.

## Trigger

User says something like:
- `/manage-agents`
- "list my agents"
- "add a new agent"
- "remove an agent"
- "configure agent providers"
- "show agent status"

## What This Skill Does

Manages the multi-agent registry in `~/.mops/agents.json`. Supports listing active agents, adding new sub-agents with provider assignment, removing agents, and inspecting agent configuration.

## Step-by-Step Instructions

### Step 1: Load Agent Registry

Read `~/.mops/agents.json`. If it doesn't exist, create an empty registry:

```json
{
  "agents": [],
  "updated_at": "<ISO timestamp>"
}
```

### Step 2: Detect Available Providers

Check which AI CLI binaries are available on the system:

```bash
which claude    # Claude Code
which codex     # OpenAI Codex CLI
which gemini    # Google Gemini CLI
```

Report available providers to the user.

### Step 3: Present Management Menu

```
MOPS Agent Manager
═══════════════════════════════════════════════════
Active Agents: <N>

  Name             │ Provider │ Status   │ Sessions
  main             │ claude   │ RUNNING  │ 3
  codex-agent      │ codex    │ IDLE     │ 0
  research         │ gemini   │ STOPPED  │ 1

Options:
  [1] Add agent
  [2] Remove agent
  [3] View agent details
  [4] Start/Stop agent
  [5] Switch provider for agent
  [0] Done
```

### Step 4: Add Agent

Prompt:
1. "Agent name (letters, numbers, hyphens only):"
2. "Provider: [claude / codex / gemini]"
3. "Workspace directory (default: ~/.mops/agents/<name>/):"

Validate:
- Name is unique in the registry
- Provider binary exists on the system
- Name matches `[a-z0-9-]+` pattern

Create workspace directory: `~/.mops/agents/<name>/`

Add to registry:
```json
{
  "name": "<name>",
  "provider": "<provider>",
  "workspace": "~/.mops/agents/<name>/",
  "created_at": "<ISO>",
  "status": "STOPPED",
  "sessions": 0,
  "config": {}
}
```

Print confirmation:
```
Agent '<name>' added with provider <provider>.
Workspace: ~/.mops/agents/<name>/
Run /send-remote-command to interact with this agent.
```

### Step 5: Remove Agent

Confirm before removing:
```
Remove agent '<name>'? This will delete its workspace at ~/.mops/agents/<name>/.
All sessions and memory will be lost. Type YES to confirm:
```

Remove from registry and optionally delete workspace (ask user).

### Step 6: View Agent Details

Show full configuration:
```
Agent: codex-agent
═══════════════════════════════════════
Provider:    codex
Status:      IDLE
Created:     2026-03-20T10:00:00Z
Workspace:   ~/.mops/agents/codex-agent/
Sessions:    0 active
Memory:      ~/.mops/agents/codex-agent/memory_system/

Config:
  model: codex-mini
  context_window: 8192
  background_tasks: disabled
```

### Step 7: Switch Provider

Update the agent's `provider` field in the registry. Warn if the new provider binary is not found.

## Output Files

- `~/.mops/agents.json` — updated registry
- `~/.mops/agents/<name>/` — new agent workspace (when adding)
