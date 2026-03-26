<p align="center">
  <img src="https://img.shields.io/badge/claude--code-plugin-8A2BE2" alt="Claude Code Plugin" />
  <img src="https://img.shields.io/badge/skills-4-blue" alt="4 Skills" />
  <img src="https://img.shields.io/badge/agents-2-green" alt="2 Agents" />
  <img src="https://img.shields.io/badge/license-MIT-green" alt="MIT License" />
</p>

# Memoriant Ops Bot Skill

A Claude Code plugin for managing remote AI agents via MOPS (Memoriant Ops Bot System). Control Claude Code, OpenAI Codex CLI, and Google Gemini CLI from any device through Telegram or Matrix. Multi-provider, multi-session, background tasks, and agent health monitoring.

**No servers. No Docker. Just install and use.**

## Install

```bash
/install NathanMaine/memoriant-ops-bot-skill
```

## Cross-Platform Support

### Claude Code (Primary)
```bash
/install NathanMaine/memoriant-ops-bot-skill
```

### OpenAI Codex CLI
```bash
git clone https://github.com/NathanMaine/memoriant-ops-bot-skill.git ~/.codex/skills/ops-bot
codex --enable skills
```

### Gemini CLI
```bash
gemini extensions install https://github.com/NathanMaine/memoriant-ops-bot-skill.git --consent
```

## Skills

| Skill | Command | What It Does |
|-------|---------|-------------|
| **Manage Agents** | `/manage-agents` | List, add, remove, configure sub-agents and provider assignments |
| **Send Remote Command** | `/send-remote-command` | Route prompts to any agent — sync, session, or background mode |
| **Check Status** | `/check-status` | Daemon health, agent status, task queue, sessions, diagnostics |
| **Manage Sessions** | `/manage-sessions` | Create, resume, suspend, and close named conversation sessions |

## Agents

| Agent | Best Model | Specialty |
|-------|-----------|-----------|
| **Ops Coordinator** | Sonnet 4.6 | Agent routing, registry management, health monitoring |
| **Task Dispatcher** | Sonnet 4.6 | Background task queuing, tracking, and result delivery |

## Quick Start

```bash
# Check what's running
/check-status

# List and manage your agents
/manage-agents

# Send a command to the default agent
/send-remote-command

# Start a named session for a specific project
/manage-sessions
```

## Multi-Provider Support

| Provider | CLI | Install |
|----------|-----|---------|
| Claude Code | `claude` | `npm install -g @anthropic-ai/claude-code` |
| OpenAI Codex | `codex` | `npm install -g @openai/codex` |
| Google Gemini | `gemini` | `npm install -g @google/gemini-cli` |

## Status Dashboard

```
MOPS Daemon: RUNNING (PID 42819)

Agent Health:
  main           claude   RUNNING   ✓
  codex-agent    codex    IDLE      ✓
  research       gemini   STOPPED   ✓

Background Tasks:
  RUNNING (1): task-1711369921  main  "Research competitors..."
  QUEUED  (2): task-1711370001, task-1711370042
```

## Session Modes

| Mode | Use Case |
|------|----------|
| Sync | Interactive tasks — response streamed in real time |
| Session | Ongoing project — named context that persists across calls |
| Background | Long-running research or generation — results delivered when done |

## MOPS Architecture

This plugin manages the local MOPS workspace at `~/.mops/`. MOPS itself wraps official CLI binaries as subprocesses — no API key spoofing, no SDK patching. Your subscriptions, your machine, your data.

See [NathanMaine/memoriant-ops-bot](https://github.com/NathanMaine/memoriant-ops-bot) for the full MOPS system.

## Use Cases

- Control your DGX Spark or remote GPU rig from your phone
- Run parallel AI agents on different providers for the same project
- Delegate long research tasks while continuing other work
- Maintain isolated conversation contexts for different projects
- Monitor agent health across a multi-machine setup

## Source Repository

Built from [NathanMaine/memoriant-ops-bot](https://github.com/NathanMaine/memoriant-ops-bot).

## License

MIT — see [LICENSE](LICENSE) for details.
