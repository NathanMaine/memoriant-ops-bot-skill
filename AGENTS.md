# Memoriant Ops Bot Skill

Remote AI agent management skills for coding agents.

## Available Skills

### manage-agents
List, add, remove, and configure sub-agents in the MOPS workspace. Assign providers (Claude Code, Codex, Gemini) and manage the agent registry.

Skill file: `skills/manage-agents/SKILL.md`

### send-remote-command
Route a prompt to any registered MOPS agent. Supports synchronous streaming, named session routing, and background task delegation.

Skill file: `skills/send-remote-command/SKILL.md`

### check-status
Live status dashboard: daemon health, agent status, background task queue, active sessions, cron jobs, and diagnostic checks.

Skill file: `skills/check-status/SKILL.md`

### manage-sessions
Create, resume, suspend, and close named conversation sessions. Manage isolated conversation contexts across agents and providers.

Skill file: `skills/manage-sessions/SKILL.md`

## Available Agents

### ops-coordinator-agent
Multi-agent routing and lifecycle management agent. Routes commands to the right provider, manages the agent registry, and monitors agent health.

Agent file: `agents/ops-coordinator-agent.md`

### task-dispatcher-agent
Background task queue manager. Delegates long-running work, tracks task status, delivers results, and handles failures and retries.

Agent file: `agents/task-dispatcher-agent.md`

## Install

```bash
# Claude Code (primary)
/install NathanMaine/memoriant-ops-bot-skill

# OpenAI Codex CLI
git clone https://github.com/NathanMaine/memoriant-ops-bot-skill.git ~/.codex/skills/ops-bot
codex --enable skills

# Google Gemini CLI
gemini extensions install https://github.com/NathanMaine/memoriant-ops-bot-skill.git --consent
```

## Source Repository

[NathanMaine/memoriant-ops-bot](https://github.com/NathanMaine/memoriant-ops-bot)
