# manage-sessions

Create, list, resume, and close named conversation sessions in MOPS. Manage conversation contexts across agents and providers.

## Trigger

User says something like:
- `/manage-sessions`
- "start a new session"
- "list my sessions"
- "resume a session"
- "close a session"
- "what sessions are running?"

## What This Skill Does

Named sessions are isolated conversation contexts within MOPS. Each session has its own history, can target a specific agent and provider, and persists across restarts. This skill manages the session lifecycle: create, list, resume, suspend, and close.

## Sessions Overview

From the MOPS architecture:

```
~/.mops/named_sessions.json   — session registry
~/.mops/workspace/sessions/   — per-session context files
  sessions/<name>/
    history.md                — conversation history
    context.json              — session metadata
```

## Step-by-Step Instructions

### Step 1: Load Session Registry

Read `~/.mops/named_sessions.json`. If it doesn't exist, initialize:

```json
{
  "sessions": [],
  "active_session": null,
  "updated_at": "<ISO>"
}
```

### Step 2: Display Session List

```
MOPS Session Manager
═══════════════════════════════════════════════════════
Active Sessions: <N>

  Name         │ Agent        │ Provider │ Status  │ Exchanges │ Last Active
  auth-work    │ main         │ claude   │ ACTIVE  │ 3         │ 14:31 today
  csv-fix      │ codex-agent  │ codex    │ IDLE    │ 7         │ 12:10 today
  research-ai  │ research     │ gemini   │ IDLE    │ 15        │ yesterday

Options:
  [1] Start new session
  [2] Resume a session
  [3] View session history
  [4] Suspend session
  [5] Close session
  [0] Done
```

### Step 3: Start New Session

Prompt:
1. "Session name (letters, numbers, hyphens):"
2. "Initial prompt or goal for this session:"
3. "Which agent? (default: main):"

Validate name is unique. Create session entry:

```json
{
  "name": "<name>",
  "agent": "<agent>",
  "provider": "<provider>",
  "status": "ACTIVE",
  "created_at": "<ISO>",
  "last_active": "<ISO>",
  "exchanges": 0,
  "initial_prompt": "<prompt>",
  "workspace": "~/.mops/workspace/sessions/<name>/"
}
```

Create workspace: `~/.mops/workspace/sessions/<name>/`

Write initial history entry to `~/.mops/workspace/sessions/<name>/history.md`:
```markdown
# Session: <name>
Started: <ISO>
Agent: <agent> | Provider: <provider>

## Initial Goal
<initial_prompt>
```

Send the initial prompt to the agent via `/send-remote-command` in session mode.

### Step 4: Resume a Session

Load the selected session. Show last 5 exchanges from its history file. Set the session to ACTIVE status. Next `/send-remote-command` calls will route to this session context.

### Step 5: View Session History

Read `~/.mops/workspace/sessions/<name>/history.md` and display it. Offer to export to a file.

### Step 6: Suspend Session

Set session status to IDLE. The context is preserved. The session can be resumed later.

```
Session '<name>' suspended. Context preserved.
Resume any time with: /manage-sessions → Resume
```

### Step 7: Close Session

Confirm:
```
Close session '<name>'? The conversation history will be archived.
Type YES to confirm:
```

Move session workspace to `~/.mops/workspace/sessions/archive/<name>-<timestamp>/`.
Remove from active registry.

### Step 8: Session Context in Commands

When `/send-remote-command` is called while a session is ACTIVE, the session name is automatically included. The history from `history.md` is prepended to provide conversation continuity.

## Handoff Protocol

After any session operation, remind the user:
- Use `/send-remote-command` to interact with the active session
- Use `/check-status` to see all session statuses at a glance
- Named sessions persist across MOPS restarts

## Output Files

- `~/.mops/named_sessions.json` — session registry
- `~/.mops/workspace/sessions/<name>/history.md` — conversation history
- `~/.mops/workspace/sessions/<name>/context.json` — session metadata
