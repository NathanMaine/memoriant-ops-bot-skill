# Contributing to MOPS

Thanks for your interest in contributing. MOPS is maintained by [Memoriant Inc.](https://github.com/NathanMaine) and welcomes community contributions.

## Getting Started

```bash
git clone https://github.com/NathanMaine/memoriant-ops-bot.git
cd memoriant-ops-bot
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
```

This installs all dependencies including test, lint, API, and Matrix extras.

## Quality Gates

Every PR must pass all four checks:

```bash
pytest                    # tests (asyncio_mode=auto)
ruff format .             # formatting
ruff check .              # linting (strict profile, select=ALL)
mypy memoriant_ops_bot    # type checking (strict mode)
```

Zero warnings, zero errors. No exceptions.

## Code Standards

**Python 3.11+** is the minimum. The codebase uses modern Python features including `match` statements, `TypeAlias`, and `PEP 695` style where appropriate.

**Line length** is 100 characters.

**Type hints** are mandatory on all public functions and methods. `mypy --strict` is enforced.

**Imports** are sorted by `ruff` with `isort` rules. First-party package is `memoriant_ops_bot`.

**Config models** use Pydantic v2 `BaseModel`. New config fields must include defaults and be backward-compatible with existing `config.json` files (deep-merge adds new keys without dropping user values).

**Async** is the default. All I/O-bound code uses `asyncio`. Blocking calls in the event loop will be flagged in review.

## Project Structure

Read these docs in order before diving into code:

1. `docs/system_overview.md` — fastest mental model
2. `docs/developer_quickstart.md` — contributor onboarding + debug paths
3. `docs/architecture.md` — startup, routing, streaming, callbacks
4. `CLAUDE.md` — module map and runtime patterns (also consumed by coding agents)

Key architectural rules:

- **Transport-agnostic core.** The orchestrator, session manager, bus, and CLI service know nothing about Telegram or Matrix specifics. Transport logic lives in `messenger/telegram/` and `messenger/matrix/`.
- **MessageBus is the single delivery path** for all background/async results. Don't create new direct-send paths.
- **Session identity is `SessionKey(transport, chat_id, topic_id)`.** All session operations must be transport-aware.
- **Zone-based workspace seeding.** Zone 2 files (rule files, tool scripts) are framework-managed and overwritten on update. Zone 3 files are user-owned and seeded once. Don't put user content in Zone 2 paths.

## What to Contribute

### Good first contributions

- Bug fixes with tests
- Documentation improvements
- Translation corrections (see `memoriant_ops_bot/i18n/`)
- Test coverage for untested edge cases

### High-impact contributions

- **New transport plugins** — Discord, Slack, Signal. Implement `BotProtocol` from `messenger/protocol.py`. See `docs/plugin-guide.md` for the full walkthrough.
- **New provider integrations** — add support for new CLI tools. See `docs/plugin-guide.md`.
- **Streaming improvements** — better chunking, error recovery, partial-message handling.
- **Docker sandbox hardening** — seccomp profiles, resource limits, network isolation.

### Before starting large features

Open an issue first to discuss the approach. This saves everyone time if the design needs adjustment.

## Pull Request Process

1. **Fork and branch.** Branch from `main`. Use descriptive branch names (`fix/session-reset-topic`, `feat/discord-transport`).
2. **Write tests.** New features need tests. Bug fixes need regression tests. Tests go in `tests/` mirroring the source structure.
3. **Pass all gates.** Run `pytest && ruff format . && ruff check . && mypy memoriant_ops_bot` before pushing.
4. **Keep PRs focused.** One feature or fix per PR. If you find an unrelated issue while working, open a separate PR.
5. **Write clear commit messages.** Describe what changed and why. Reference issue numbers where applicable.

## Testing

Tests use `pytest` with `pytest-asyncio` (auto mode). Test files mirror the source layout:

```
memoriant_ops_bot/cli/codex_provider.py  →  tests/cli/test_codex_provider.py
memoriant_ops_bot/bus/bus.py             →  tests/bus/test_bus.py
```

Common test patterns:

- Mock subprocess calls (never invoke real CLIs in tests)
- Use `tmp_path` for filesystem operations
- Use `time-machine` for time-dependent tests
- Shared fixtures are in `tests/conftest.py` and per-directory `conftest.py` files

## i18n / Translations

Translation files are in `memoriant_ops_bot/i18n/<lang>/`. Currently supported: `en`, `de`, `nl`, `fr`, `ru`, `es`, `pt`.

To add a language:

1. Copy `memoriant_ops_bot/i18n/en/` to `memoriant_ops_bot/i18n/<code>/`
2. Translate all string values (keys stay in English)
3. Add the language to `i18n/loader.py`
4. Run `pytest tests/i18n/test_completeness.py` to verify all keys are present

To fix a translation: edit the relevant file and submit a PR. Native speaker review is appreciated.

## Reporting Issues

Use the issue templates in `.github/ISSUE_TEMPLATE/`:

- **Bug report** — include `mops status` output, `/diagnose` output, and relevant log lines from `~/.mops/logs/agent.log`
- **Feature request** — describe the use case, not just the desired feature

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
