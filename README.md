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

## Using the Actual Tool

The full source code for MOPS (the working Telegram/Matrix bot) from [NathanMaine/memoriant-ops-bot](https://github.com/NathanMaine/memoriant-ops-bot) is bundled in `src/`. The bot is a production Python package (v0.15.1) published to PyPI.

### Install

The easiest install path is via pipx (recommended):

```bash
pipx install memoriant-ops-bot
```

Or install from the bundled source:

```bash
cd src
pip install -e .
```

### Set Up a Telegram Bot

1. Message [@BotFather](https://t.me/BotFather) on Telegram
2. Run `/newbot` and follow the prompts
3. Copy the bot token BotFather gives you

### Configure MOPS

```bash
cp src/config.example.json ~/.mops/config.json
# Edit ~/.mops/config.json and add your Telegram bot token
```

Or just run `mops` and the onboarding wizard will walk you through it interactively.

### Run

```bash
mops
```

The onboarding wizard configures:
- Transport: Telegram (token) or Matrix (homeserver + credentials)
- Timezone
- Optional Docker sandbox for code execution
- Background service installation (launchd on macOS, systemd on Linux)

### Install an AI CLI to Control

```bash
# Pick one or more providers:
npm install -g @anthropic-ai/claude-code && claude auth     # Claude Code
npm install -g @openai/codex && codex auth                  # OpenAI Codex
npm install -g @google/gemini-cli                           # Google Gemini
```

### What the Bot Does

Once running, MOPS bridges your Telegram/Matrix messages to whichever AI CLI you have installed. You send a message from your phone — MOPS passes it to `claude`, `codex`, or `gemini` as a subprocess and streams the response back. No API spoofing. No SDK patches. Your subscriptions, your machine, your data.

- **This Claude Code skill** teaches the AI how to manage MOPS agents programmatically
- **The bot in `src/`** is the actual daemon that runs on your machine and handles real Telegram messages

Works with Claude Code, OpenAI Codex CLI, and Google Gemini CLI.

### Tests

```bash
cd src
pip install -e ".[test]"
pytest
```

### Full Documentation

See the [memoriant-ops-bot repo](https://github.com/NathanMaine/memoriant-ops-bot) for the complete setup guide, architecture docs, Dockerfile, Matrix setup, and more.

## Source Repository

Built from [NathanMaine/memoriant-ops-bot](https://github.com/NathanMaine/memoriant-ops-bot).

## License

MIT — see [LICENSE](LICENSE) for details.
