[English](README.md) | [Deutsch](README.de.md) | [Nederlands](README.nl.md) | [Francais](README.fr.md) | [Russkij](README.ru.md) | [Espanol](README.es.md) | [Portugues](README.pt.md)

<p align="center">
  <img src="docs/images/mops-logo.jpeg" alt="MOPS" width="280">
</p>

<h1 align="center">MOPS</h1>

<p align="center">
  <em>Multi-provider AI agent control from your phone.</em>
</p>

<p align="center">
  <a href="#quick-start">Quick Start</a> &middot;
  <a href="#how-it-works">How It Works</a> &middot;
  <a href="#features">Features</a> &middot;
  <a href="docs/use-cases.md">Use Cases</a> &middot;
  <a href="docs/installation.md">Install Guide</a> &middot;
  <a href="docs/architecture.md">Architecture</a>
</p>

<p align="center">
  <img src="https://github.com/NathanMaine/memoriant-ops-bot/actions/workflows/tests.yml/badge.svg" alt="Tests">
  <img src="https://img.shields.io/badge/providers-Claude%20%7C%20Codex%20%7C%20Gemini-blue" alt="Providers">
  <img src="https://img.shields.io/badge/transport-Telegram%20%7C%20Matrix-green" alt="Transport">
  <img src="https://img.shields.io/badge/license-MIT-lightgrey" alt="License">
  <img src="https://img.shields.io/badge/python-3.11%2B-yellow" alt="Python">
  <img src="https://img.shields.io/pypi/v/memoriant-ops-bot" alt="PyPI">
</p>

---

Run Claude Code, OpenAI Codex CLI, or Google Gemini CLI from Telegram or Matrix. Uses only official CLIs as subprocesses — nothing spoofed, nothing proxied. Your subscriptions, your machine, your data.

<p align="center">
  <img src="docs/images/mops-demo.gif" alt="MOPS Demo — controlling AI agents from Telegram" width="300">
</p>

> **Released March 12, 2026** — five days before Anthropic shipped [Claude Dispatch](https://mlq.ai/news/anthropic-launches-claude-dispatch-for-remote-desktop-ai-control/). Same concept, different philosophy.

### How does this compare to Claude Dispatch?


|  | MOPS | Claude Dispatch |
|---|---|---|
| **Providers** | Claude + Codex + Gemini | Claude only |
| **Cost** | Free — uses your existing subscriptions | Max plan required ($100+/mo) |
| **Remote from** | Telegram, Matrix, any device | Claude mobile app |
| **Controls** | Any machine — servers, GPU rigs, cloud | Mac desktop only |
| **Parallel agents** | Unlimited — topics, sessions, sub-agents | Single conversation |
| **Open source** | MIT | Proprietary |
| **Background tasks** | Yes, with delegation + follow-ups | Yes |
| **Named sessions** | Yes | No |
| **Plugin system** | Yes — add Discord, Slack, Signal | No |

---

## Quick Start

**Step 1: Install Python** (skip if you already have Python 3.11+)

```bash
# macOS
brew install python@3.11

# Ubuntu/Debian
sudo apt update && sudo apt install python3 python3-pip python3-venv

# Windows — download from https://www.python.org/downloads/
# ✅ Check "Add Python to PATH" during install
```

**Step 2: Install pipx** (a tool for installing Python apps)

```bash
# macOS
brew install pipx && pipx ensurepath

# Linux
pip install pipx && pipx ensurepath

# Windows
pip install pipx
pipx ensurepath
```

> After running `pipx ensurepath`, **close and reopen your terminal** for the command to work.

**Step 3: Install MOPS**

```bash
pipx install memoriant-ops-bot
```

**Step 4: Install at least one AI CLI** (the agent MOPS will control)

```bash
# Pick one or more:
npm install -g @anthropic-ai/claude-code && claude auth     # Claude
npm install -g @openai/codex && codex auth                   # Codex
npm install -g @google/gemini-cli                            # Gemini (auth in CLI)
```

> Don't have Node.js? Install it first: `brew install node` (macOS) or `sudo apt install nodejs npm` (Linux) or download from [nodejs.org](https://nodejs.org)

**Step 5: Get a Telegram bot token** — see the [Telegram Setup Guide](docs/telegram-setup.md)

**Step 6: Run MOPS**

```bash
mops
```

The onboarding wizard walks you through transport setup (Telegram or Matrix), timezone, optional Docker sandbox, and background service installation.

---

## How It Works

MOPS wraps official CLI binaries as subprocesses and bridges them to your messaging platform. No API keys, no SDK patches, no spoofed headers. When you send a message on Telegram, MOPS passes it to the CLI exactly as if you typed it in your terminal.

```
Phone (Telegram/Matrix)
  |
  v
MOPS daemon (your machine)
  |
  +---> claude     (subprocess)
  +---> codex      (subprocess)
  +---> gemini     (subprocess)
  |
  v
Response streamed back to phone
```

All state lives in `~/.mops/` as plain JSON and Markdown. No database, no external services.

---

## Chat Modes

MOPS gives you five levels of interaction. Start simple, scale up as needed.

### 1 &mdash; Single Chat

Your main 1:1 conversation. Every message goes to the active CLI, responses stream back live.

```
You:   "Explain the auth flow in this codebase"
Bot:   [streams Claude Code response]

You:   /model
Bot:   [switch to Codex or Gemini]
```

### 2 &mdash; Group Topics

Create a Telegram group with topics enabled. Each topic gets its own isolated CLI context. Five topics = five parallel conversations, all from one group.

```
My Projects/
  General        -- own context
  Auth           -- own context, own model
  Frontend       -- own context
  Database       -- own context
  Refactor       -- own context
```

### 3 &mdash; Named Sessions

Spin up a side conversation without losing your current context. Like opening a second terminal.

```
You:   "Let's work on authentication"
Bot:   [responds about auth]

/session Fix the broken CSV export
Bot:   [works CSV in separate context]

You:   "Back to auth — add rate limiting"
Bot:   [picks up right where you left off]
```

### 4 &mdash; Background Tasks

Delegate long-running work. You keep chatting, the task runs autonomously, results flow back when done.

```
You:   "Research the top 5 competitors and write a summary"
Bot:   -> delegates, you keep working
Bot:   -> done, summary appears in your chat
```

### 5 &mdash; Sub-Agents

Fully isolated second bot — own workspace, own memory, own CLI, own config. Runs on a different provider if you want.

```bash
mops agents add codex-agent
```

Now you have Claude in your main chat and Codex in a separate chat, working in parallel with independent contexts. They can delegate tasks to each other.

<details>
<summary><strong>Mode comparison table</strong></summary>
<br>

|  | Single | Topics | Sessions | Tasks | Sub-agents |
|---|---|---|---|---|---|
| **What** | Main 1:1 | One topic = one chat | Side context | "Do this in background" | Separate bot |
| **Context** | One per provider | One per topic | Own per session | Own, result flows back | Fully isolated |
| **Workspace** | `~/.mops/` | Shared | Shared | Shared | Own under `agents/` |
| **Setup** | Automatic | Create group + topics | `/session <prompt>` | Automatic | `mops agents add` |

</details>

---

## Features

**Multi-provider** &mdash; Switch between Claude, Codex, and Gemini with `/model`. Per-topic, per-session.

**Multi-transport** &mdash; Telegram and Matrix run simultaneously. Plugin system for Discord, Slack, Signal.

**Real-time streaming** &mdash; Live message edits on Telegram, segment-based on Matrix.

**Persistent memory** &mdash; Plain Markdown files that survive across sessions and reboots.

**Cron & webhooks** &mdash; Schedule recurring tasks with timezone support. Webhook triggers for external integrations.

**Docker sandbox** &mdash; Optional sidecar container with configurable host mounts for safe code execution.

**Background service** &mdash; Install as systemd (Linux), launchd (macOS), or Task Scheduler (Windows).

**Cross-tool skill sync** &mdash; Shared skills across `~/.claude/`, `~/.codex/`, `~/.gemini/`.

**Hot-reload config** &mdash; Change language, model, permissions, scene — no restart needed.

**7 languages** &mdash; English, Deutsch, Nederlands, Francais, Russkij, Espanol, Portugues.

---

## Transport Support

| Platform | Status | Streaming | Interaction | Install |
|---|---|---|---|---|
| **Telegram** | Primary | Live message edits | Inline keyboards | Built-in |
| **Matrix** | Supported | Segment-based | Emoji reactions | `mops install matrix` |

Both run in parallel on the same agent. Adding a new messenger means implementing `BotProtocol` in a sub-package — the core is fully transport-agnostic.

---

## Security

Dual-allowlist model. Every message must pass both checks:

| Chat type | Requirement |
|---|---|
| **Private** | User ID in allowlist |
| **Group** | Group ID in allowlist AND user ID in allowlist |

Allowlists are hot-reloadable. Unauthorized groups trigger auto-leave. All state is local — nothing leaves your machine.

---

## Commands

| Command | What it does |
|---|---|
| `/model` | Switch provider/model |
| `/new` | Reset session |
| `/stop` | Stop current + queued |
| `/session <prompt>` | Start named session |
| `/tasks` | View background tasks |
| `/cron` | Manage scheduled jobs |
| `/agents` | Multi-agent status |
| `/status` | Session/provider info |
| `/diagnose` | Runtime diagnostics |
| `/memory` | View persistent memory |

<details>
<summary><strong>CLI commands</strong></summary>

```bash
mops                    # Start (auto-onboarding)
mops onboarding         # Re-run setup
mops stop               # Stop bot
mops restart            # Restart
mops upgrade            # Upgrade + restart
mops status             # Runtime status
mops uninstall          # Remove everything

mops service install    # Background service
mops service start|stop|logs

mops docker enable      # Docker sandbox
mops docker rebuild
mops docker mount /path

mops agents list        # Sub-agents
mops agents add NAME
mops agents remove NAME

mops install matrix     # Matrix transport
mops install api        # WebSocket API
```

</details>

---

## Workspace

```
~/.mops/
  config/config.json          # Configuration
  sessions.json               # Chat state
  named_sessions.json         # Named sessions
  tasks.json                  # Background tasks
  cron_jobs.json              # Scheduled jobs
  agents.json                 # Sub-agent registry
  SHAREDMEMORY.md             # Cross-agent knowledge
  workspace/
    memory_system/            # Persistent memory
    cron_tasks/               # Cron scripts
    skills/ tools/            # Shared tooling
    tasks/                    # Per-task folders
  agents/<name>/              # Isolated sub-agent workspaces
```

---

## Why This Approach

Other projects patch SDKs, spoof headers, or proxy API calls. That's fragile and risks violating provider ToS.

MOPS runs official CLIs as subprocesses. Nothing more. Your subscription, your machine, your auth. The bot is just a bridge between your phone and your terminal.

---

## Docs

| Guide | Content |
|---|---|
| [Installation](docs/installation.md) | Setup walkthrough |
| [System Overview](docs/system_overview.md) | End-to-end runtime |
| [Architecture](docs/architecture.md) | Routing, streaming, callbacks |
| [Configuration](docs/config.md) | Full config reference |
| [Use Cases & Workflows](docs/use-cases.md) | 10 real-world patterns with commands |
| [FAQ](docs/FAQ.md) | Common questions answered |
| [Troubleshooting](docs/troubleshooting.md) | Diagnostic steps by symptom |
| [Plugin Guide](docs/plugin-guide.md) | Adding transports & providers |
| [Telegram Setup](docs/telegram-setup.md) | Bot token + group setup |
| [Matrix Setup](docs/matrix-setup.md) | Matrix transport |
| [Automation](docs/automation.md) | Cron, webhooks, heartbeat |
| [Service Management](docs/modules/service_management.md) | systemd / launchd / Task Scheduler |

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for setup, quality gates, and contribution guidelines.

```bash
git clone https://github.com/NathanMaine/memoriant-ops-bot.git
cd memoriant-ops-bot
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pytest && ruff format . && ruff check . && mypy memoriant_ops_bot
```

---

[Security Policy](SECURITY.md) · [Changelog](CHANGELOG.md)

<p align="center">
  <strong>MIT License</strong><br>
  Built by <a href="https://github.com/NathanMaine">Memoriant Inc.</a>
</p>
