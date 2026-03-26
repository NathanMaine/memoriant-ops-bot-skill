# Developer Quickstart

Fast onboarding path for contributors and junior devs.

## 1) Local setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

Optional for full runtime validation:

- install/auth at least one provider CLI (`claude`, `codex`, `gemini`)
- set up a messaging transport:
  - **Telegram**: bot token from @BotFather + user ID (`allowed_user_ids`)
  - **Matrix**: account on any homeserver (homeserver URL, user ID, password, `allowed_users`)
- for Telegram group support, also set `allowed_group_ids`

## 2) Run the bot

```bash
mops
```

First run starts onboarding and writes config to `~/.mops/config/config.json`.

Primary runtime files/directories:

- `~/.mops/sessions.json`
- `~/.mops/named_sessions.json`
- `~/.mops/tasks.json`
- `~/.mops/chat_activity.json`
- `~/.mops/cron_jobs.json`
- `~/.mops/webhooks.json`
- `~/.mops/startup_state.json`
- `~/.mops/inflight_turns.json`
- `~/.mops/SHAREDMEMORY.md`
- `~/.mops/agents.json`
- `~/.mops/agents/`
- `~/.mops/workspace/`
- `~/.mops/logs/agent.log`

## 3) Quality gates

```bash
pytest
ruff format .
ruff check .
mypy mops_bot
```

Expected: zero warnings, zero errors.

## 4) Core mental model

```text
Telegram / Matrix / API input
  -> ingress layer (TelegramBot / MatrixBot / ApiServer)
  -> orchestrator flow
  -> provider CLI subprocess
  -> response delivery (transport-specific)

background/async results
  -> Envelope adapters
  -> MessageBus
  -> optional session injection
  -> transport delivery (Telegram or Matrix)
```

## 5) Read order in code

Entry + command layer:

- `mops_bot/__main__.py`
- `mops_bot/cli_commands/`

Runtime hot path:

- `mops_bot/multiagent/supervisor.py`
- `mops_bot/messenger/telegram/app.py`
- `mops_bot/messenger/telegram/startup.py`
- `mops_bot/orchestrator/core.py`
- `mops_bot/orchestrator/lifecycle.py`
- `mops_bot/orchestrator/flows.py`

Delivery/task/session core:

- `mops_bot/bus/`
- `mops_bot/session/manager.py`
- `mops_bot/tasks/hub.py`
- `mops_bot/tasks/registry.py`

Provider/API/workspace core:

- `mops_bot/cli/service.py` + provider wrappers
- `mops_bot/api/server.py`
- `mops_bot/workspace/init.py`
- `mops_bot/workspace/rules_selector.py`
- `mops_bot/workspace/skill_sync.py`

## 6) Common debug paths

If command behavior is wrong:

1. `mops_bot/__main__.py`
2. `mops_bot/cli_commands/*`

If Telegram routing is wrong:

1. `mops_bot/messenger/telegram/middleware.py`
2. `mops_bot/messenger/telegram/app.py`
3. `mops_bot/orchestrator/commands.py`
4. `mops_bot/orchestrator/flows.py`

If Matrix routing is wrong:

1. `mops_bot/messenger/matrix/bot.py`
2. `mops_bot/messenger/matrix/transport.py`
3. `mops_bot/orchestrator/flows.py`

If background results look wrong:

1. `mops_bot/bus/adapters.py`
2. `mops_bot/bus/bus.py`
3. `mops_bot/messenger/telegram/transport.py` (or `mops_bot/messenger/matrix/transport.py`)

If tasks are wrong:

1. `mops_bot/tasks/hub.py`
2. `mops_bot/tasks/registry.py`
3. `mops_bot/multiagent/internal_api.py`
4. `mops_bot/_home_defaults/workspace/tools/task_tools/*.py`

If API is wrong:

1. `mops_bot/api/server.py`
2. `mops_bot/orchestrator/lifecycle.py` (API startup wiring)
3. `mops_bot/files/*` (allowed roots, MIME, prompt building)

## 7) Behavior details to remember

- `/stop` and `/stop_all` are pre-routing abort paths in middleware/bot.
- `/new` resets only active provider bucket for the active `SessionKey`.
- session identity is transport-aware: `SessionKey(transport, chat_id, topic_id)`.
- `/model` inside a topic updates only that topic session (not global config).
- task tools now support permanent single-task removal via `delete_task.py` (`/tasks/delete`).
- task routing is topic-aware via `thread_id` and `MOPS_TOPIC_ID`.
- API auth accepts optional `channel_id` for per-channel session isolation.
- startup recovery uses `inflight_turns.json` + recovered named sessions.
- auth allowlists (`allowed_user_ids`, `allowed_group_ids`) are hot-reloadable.
- `mops agents add` is a Telegram-focused scaffold; Matrix sub-agents are supported through `agents.json` or the bundled agent tool scripts.

Continue with `docs/system_overview.md` and `docs/architecture.md` for complete runtime detail.
