This file gives coding agents a current map of the repository.

## Project Overview

Memoriant Ops Bot is a Telegram bot that routes chat input to official provider CLIs (`claude`, `codex`, `gemini`), streams responses back to Telegram, persists per-chat state, and runs cron/webhook/heartbeat automation in-process.

Stack:

- Python 3.11+
- aiogram 3.x
- Pydantic 2.x
- asyncio

## Development Commands

```bash
# Setup
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"

# Run
mops
mops -v

# Tests
pytest
pytest tests/bot/test_app.py
pytest -k "pattern"

# Quality
ruff format .
ruff check .
mypy memoriant_ops_bot
```

## Runtime Flow

```text
Telegram Update
  -> AuthMiddleware
  -> SequentialMiddleware (queue + per-chat lock)
  -> TelegramBot handlers
  -> Orchestrator
  -> CLIService
  -> provider subprocess (claude/codex/gemini)
  -> Telegram output (stream edit or one-shot)
```

## Module Map

| Module | Purpose |
|---|---|
| `bot/` | Telegram handlers, callback routing, streaming delivery, queue UX |
| `orchestrator/` | command registry, directives/hooks, flow routing, observer wiring |
| `cli/` | provider wrappers, stream parsing, auth checks, process registry, model caches |
| `session/` | chat sessions with provider-isolated buckets |
| `background/` | named background sessions (`/session`) with follow-ups |
| `cron/` | in-process scheduler and one-shot task execution |
| `webhook/` | HTTP hooks (`wake` and `cron_task`) |
| `heartbeat/` | periodic proactive checks in active sessions |
| `cleanup/` | daily retention cleanup |
| `workspace/` | home seeding, rules deployment/sync, skill sync |
| `infra/` | PID lock, service backends, Docker manager, update/restart helpers |

## Key Runtime Patterns

- `MopsPaths` (`workspace/paths.py`) is the single source of truth for paths.
- Workspace init is zone-based:
  - Zone 2 overwrite: `CLAUDE.md`, `AGENTS.md`, `GEMINI.md`, and framework cron/webhook tool scripts.
  - Zone 3 seed-once for user-owned files.
- Rules are selected from `RULES*.md` variants and deployed per authenticated provider.
- Rule sync updates existing `CLAUDE.md`, `AGENTS.md`, `GEMINI.md` siblings recursively by mtime.
- Skill sync spans `~/.mops/workspace/skills`, `~/.claude/skills`, `~/.codex/skills`, `~/.gemini/skills`.
  - normal mode: links
  - Docker mode: managed copies (`.mops_managed` marker)
- Streaming fallback is automatic; `/stop` abort checks are enforced during event loop processing.
- Session state is provider-isolated; `/new` resets only the active provider bucket.

## Background Systems

All run as in-process asyncio tasks:

- `BackgroundObserver`
- `CronObserver`
- `HeartbeatObserver`
- `WebhookObserver`
- `CleanupObserver`
- `CodexCacheObserver`
- `GeminiCacheObserver`
- rule sync watcher
- skill sync watcher
- update observer (upgradeable installs)

## Service Backends

- Linux: systemd user service
- macOS: launchd Launch Agent
- Windows: Task Scheduler

`mops service logs` behavior:

- Linux: `journalctl --user -u mops -f`
- macOS/Windows: recent lines from `~/.mops/logs/agent.log` (fallback newest `*.log`)

## CLI Commands

| Command | Effect |
|---|---|
| `mops` | Start bot (runs onboarding if needed) |
| `mops stop` | Stop bot and Docker container |
| `mops restart` | Restart bot |
| `mops upgrade` | Stop, upgrade, restart |
| `mops docker rebuild` | Stop bot, remove container & image, rebuilt on next start |
| `mops docker enable` | Set `docker.enabled = true` |
| `mops docker disable` | Stop container, set `docker.enabled = false` |
| `mops service install` | Install as background service |
| `mops service [sub]` | Service management (status/stop/logs/...) |

## Data Files (`~/.mops`)

- `config/config.json`
- `sessions.json`
- `cron_jobs.json`
- `webhooks.json`
- `logs/agent.log`

## Conventions

- `asyncio_mode = "auto"` in tests
- line length 100
- mypy strict mode
- ruff with strict lint profile
- config deep-merge adds new defaults without dropping user keys
- supervisor restart code is `42`

## Additional Docs

- `CONTRIBUTING.md` — contributor onboarding, quality gates, PR process
- `SECURITY.md` — security model, trust boundaries, responsible disclosure
- `CHANGELOG.md` — release history
- `docs/use-cases.md` — 10 real-world workflow patterns with commands
- `docs/FAQ.md` — common questions and answers
- `docs/troubleshooting.md` — diagnostic steps organized by symptom
- `docs/plugin-guide.md` — how to add new transports and CLI providers
