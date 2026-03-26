# check-status

Check the live status of MOPS agents, background tasks, active sessions, and the MOPS daemon. Diagnose issues and restart components.

## Trigger

User says something like:
- `/check-status`
- "what's running?"
- "check my agent status"
- "show background tasks"
- "is MOPS running?"
- "diagnose my bot"

## What This Skill Does

Provides a complete runtime status view of the MOPS system:
1. Daemon status (running / stopped / error)
2. Agent health (running / idle / stopped / error)
3. Background task queue (queued / running / completed / failed)
4. Active sessions
5. Scheduled cron jobs
6. Diagnostic checks (CLI availability, config validity)

## Step-by-Step Instructions

### Step 1: Check Daemon Status

Look for the MOPS daemon PID file at `~/.mops/mops.pid`.

If file exists: read PID and check if the process is alive.
If file missing: daemon is not running.

```
MOPS Daemon: RUNNING (PID 42819)
```
or
```
MOPS Daemon: STOPPED — run `mops` to start
```

### Step 2: Check Agent Health

Load `~/.mops/agents.json`. For each agent:
- Check if provider CLI binary exists
- Check agent status field
- Check workspace directory exists
- Check for recent activity in memory system

Display:
```
Agent Health
═══════════════════════════════════════════════════
  main           claude   RUNNING   ✓ CLI found  ✓ workspace
  codex-agent    codex    IDLE      ✓ CLI found  ✓ workspace
  research       gemini   STOPPED   ✓ CLI found  ✓ workspace
```

### Step 3: Check Background Tasks

Load `~/.mops/tasks.json`. Show all tasks, grouped by status:

```
Background Tasks
═══════════════════════════════════════════════════
RUNNING (1):
  task-1711369921  main  "Research the top 5 competitors..."
  Started: 14:32  Elapsed: 00:08:42

QUEUED (2):
  task-1711370001  codex-agent  "Refactor auth module..."
  task-1711370042  main  "Write unit tests for..."

COMPLETED (3, last 24h):
  task-1711360000  main  → 14:01  "Generate README"
  task-1711365000  research  → 15:45  "Summarize paper..."
  task-1711368000  codex-agent  → 16:22  "Debug CSV export"

FAILED (0)
```

### Step 4: Check Active Sessions

Load `~/.mops/named_sessions.json`. Show active sessions:

```
Named Sessions
═══════════════════════════════════════════════════
  auth-work    main    Active   Last: 14:31  3 exchanges
  csv-fix      codex   Idle     Last: 12:10  7 exchanges
```

### Step 5: Check Cron Jobs

Load `~/.mops/cron_jobs.json`. Show scheduled jobs:

```
Cron Jobs
═══════════════════════════════════════════════════
  daily-summary   0 8 * * *   main    Next: 2026-03-26 08:00
  weekly-report   0 9 * * 1   research  Next: 2026-03-31 09:00
```

### Step 6: Run Diagnostics

Check:
- Provider CLI versions: `claude --version`, `codex --version`, `gemini --version`
- Config file validity: `~/.mops/config/config.json` is valid JSON
- Transport status: Telegram bot connected / disconnected
- Memory directory existence: `~/.mops/workspace/memory_system/`

```
Diagnostics
═══════════════════════════════════════════════════
  claude     v1.3.2   ✓
  codex      v0.2.1   ✓
  gemini     not found ✗ — install with: npm install -g @google/gemini-cli
  config     valid    ✓
  telegram   connected (bot: @MyMOPSBot) ✓
  memory     exists   ✓
```

### Step 7: Repair Options

If issues are found, offer:
```
Issues detected:
  [1] Gemini CLI not installed
  [2] research agent is stopped

Options:
  [R] Show repair commands
  [S] Start stopped agents
  [0] Done
```

For [R], show the exact commands needed to fix each issue.

## Quick Status (no-prompt mode)

If the user says "quick status", show a one-line summary only:
```
MOPS: RUNNING | Agents: 3 (1 running, 2 idle) | Tasks: 1 running, 2 queued | Telegram: connected
```
