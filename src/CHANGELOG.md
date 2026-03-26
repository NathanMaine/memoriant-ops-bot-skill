# Changelog

All notable changes to MOPS are documented here.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.15.0] — 2026-03-12

### Initial Public Release

First open-source release of MOPS (Memoriant Ops Bot).

### Core

- **Multi-provider CLI orchestration** — Claude Code, OpenAI Codex CLI, and Google Gemini CLI as subprocess wrappers. No SDK patching, no API proxying, no spoofed headers.
- **Multi-transport messaging** — Telegram (primary) and Matrix (supported) run simultaneously via `BotProtocol` abstraction. Transport-agnostic core with plugin architecture for future messengers.
- **Real-time streaming** — live message edits on Telegram, segment-based delivery on Matrix. Configurable chunk sizes, edit intervals, and sentence-break behavior.
- **Provider switching** — `/model` command switches between Claude, Codex, and Gemini per-chat, per-topic, or per-session. Model choice persists across restarts.

### Session Management

- **Transport-aware sessions** — `SessionKey(transport, chat_id, topic_id)` isolates conversations across Telegram chats, forum topics, Matrix rooms, and API channels.
- **Provider-isolated session buckets** — switching providers preserves other provider contexts within the same session.
- **Named background sessions** — `/session <prompt>` runs side tasks without interrupting the main conversation. Auto-generated memorable names. Follow-up support via `@session-name`.
- **Telegram group topics** — each forum topic gets independent session state, provider choice, and conversation history.

### Automation

- **Cron scheduler** — time-based job execution in isolated task folders with per-job provider/model overrides, quiet hours, and dependency ordering.
- **Webhook server** — HTTP POST ingress with `wake` (inject into active session) and `cron_task` (isolated execution) modes. Bearer and HMAC auth.
- **Heartbeat observer** — periodic proactive checks with quiet-hour suppression and ACK-token filtering. Per-group-topic target overrides.
- **Cleanup observer** — daily file retention management for media, output, and API files with configurable retention windows.
- **Delegated background tasks** — `TaskHub` with shared registry, topic-aware routing, parent-session result injection, and task question/answer flow.

### Multi-Agent

- **Sub-agent system** — fully isolated agent stacks with own transport credentials, workspace, session files, and provider config. Defined in `agents.json`.
- **Inter-agent communication** — in-memory bus + internal localhost HTTP bridge for cross-agent task delegation and result delivery.
- **Shared knowledge sync** — `SHAREDMEMORY.md` propagation across agent workspaces.

### Infrastructure

- **Background service management** — systemd (Linux), launchd (macOS), Task Scheduler (Windows) with install/start/stop/logs/uninstall lifecycle.
- **Docker sandbox** — optional sidecar container for code execution isolation with configurable host mounts and optional AI/ML package extras (Whisper, PyTorch, OpenCV, Tesseract, etc.).
- **Startup recovery** — lifecycle classification (first start / service restart / system reboot), in-flight turn recovery, and named session resume.
- **Config hot-reload** — model, provider, allowlists, timeouts, streaming, and heartbeat settings reload without restart.
- **PID lock** — prevents duplicate instances.

### API

- **WebSocket API** — optional direct transport with E2E encryption (NaCl Box), streaming events, and per-channel session isolation.
- **HTTP endpoints** — health check, authenticated file download, and file upload.

### Developer Experience

- **7 languages** — English, Deutsch, Nederlands, Français, Русский, Español, Português (UI strings and README translations).
- **Strict quality gates** — mypy strict, ruff ALL, pytest-asyncio, 100% type-annotated public API.
- **Comprehensive docs** — 25+ module-level reference docs, architecture guide, config schema, automation quickstart, developer quickstart, and `llms.txt` for AI agent consumption.
- **Cross-tool skill sync** — shared skills across `~/.claude/`, `~/.codex/`, `~/.gemini/` via symlinks (host) or managed copies (Docker).

### Security

- **Dual-allowlist authentication** — user ID AND group ID must both pass. Fail-closed on empty allowlists.
- **Auto-leave on unauthorized groups** — bot exits groups not in the allowlist.
- **Local-only state** — all data stays in `~/.mops/`. No telemetry, no external services, no phone-home.
- **Hot-reloadable allowlists** — update access control without restart.

[0.15.0]: https://github.com/NathanMaine/memoriant-ops-bot/releases/tag/v0.15.0
