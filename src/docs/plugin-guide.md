# Plugin Guide

How to extend MOPS with new messaging transports and CLI providers.

## Adding a Transport (Discord, Slack, Signal, etc.)

MOPS is transport-agnostic. The orchestrator, session manager, bus, and CLI service know nothing about Telegram or Matrix. Adding a new messenger requires implementing one protocol interface and registering a factory.

### Step 1: Understand BotProtocol

All transports implement `BotProtocol` from `memoriant_ops_bot/messenger/protocol.py`. This is the contract between the transport layer and the supervisor/orchestrator.

Key methods:

```python
@runtime_checkable
class BotProtocol(Protocol):
    @property
    def orchestrator(self) -> Orchestrator | None: ...
    @property
    def config(self) -> AgentConfig: ...
    @property
    def notification_service(self) -> NotificationService: ...

    async def run(self) -> int: ...                           # start event loop, block until shutdown
    async def shutdown(self) -> None: ...                     # graceful teardown
    def register_startup_hook(self, hook) -> None: ...        # post-orchestrator callback
    def set_abort_all_callback(self, callback) -> None: ...   # multi-agent abort
    async def on_async_interagent_result(self, result) -> None: ...
    async def on_task_result(self, result: TaskResult) -> None: ...
    async def on_task_question(self, task_id, question, prompt_preview, chat_id, thread_id=None) -> None: ...
    def file_roots(self, paths: MopsPaths) -> list[Path] | None: ...
```

Study the existing implementations:

- `messenger/telegram/app.py` — full-featured reference (streaming edits, inline keyboards, file handling, group topics)
- `messenger/matrix/bot.py` — second reference (segment streaming, reaction buttons, E2EE rooms)

### Step 2: Create the transport package

```
memoriant_ops_bot/messenger/your_transport/
  __init__.py
  bot.py          # BotProtocol implementation
  startup.py      # startup wiring (orchestrator creation, observer setup)
  transport.py    # MessageBus delivery adapter
```

**bot.py** is your main entry point. It must:

1. Initialize your messaging library's client/connection
2. Set up message handlers that route to `Orchestrator.handle_message()` or `handle_message_streaming()`
3. Implement auth checks (allowlists)
4. Handle command dispatch (your transport's equivalent of `/command`)
5. Implement `send_message`, `edit_message`, and file operations

**startup.py** follows the same pattern as Telegram/Matrix startup:

1. Create the orchestrator via `Orchestrator.create(...)`
2. Wire observers to the message bus
3. Start background systems (config reload, update observer, etc.)
4. Run the transport's event loop

**transport.py** implements the `MessageBus` delivery adapter — how background results (cron, webhook, task completions) get sent through your transport.

### Step 3: Register the transport

In `messenger/registry.py`, add your factory to `_TRANSPORT_FACTORIES`:

```python
# messenger/registry.py
def _create_discord(
    config: AgentConfig,
    *,
    agent_name: str,
    bus: MessageBus | None,
    lock_pool: LockPool | None,
) -> BotProtocol:
    from memoriant_ops_bot.messenger.discord.bot import DiscordBot
    return DiscordBot(config, agent_name=agent_name, bus=bus, lock_pool=lock_pool)

_TRANSPORT_FACTORIES: dict[str, _Factory] = {
    "telegram": _create_telegram,
    "matrix": _create_matrix,
    "discord": _create_discord,  # your new entry
}
```

The factory receives `AgentConfig` plus keyword args for `agent_name`, `bus`, and `lock_pool`, and returns a `BotProtocol` instance.

### Step 4: Add config support

If your transport needs credentials (bot token, server URL, etc.), add a config model:

```python
# In config.py
class DiscordConfig(BaseModel):
    token: str = ""
    guild_ids: list[int] = []
    allowed_user_ids: list[int] = []
```

Add it to `AgentConfig` and update the onboarding wizard in `cli/init_wizard.py` if you want interactive setup.

### Step 5: Session identity

Your transport needs a transport prefix for `SessionKey`. Existing ones:

- `"tg"` — Telegram
- `"mx"` — Matrix
- `"api"` — WebSocket API

Add yours (e.g., `"dc"` for Discord). Chat IDs must be integers — if your platform uses string IDs, create a deterministic int mapping (see Matrix's approach in `messenger/matrix/bot.py`).

### Step 6: Tests

Mirror the test structure:

```
tests/messenger/your_transport/
  __init__.py
  test_bot.py
  test_transport.py
```

Mock the external messaging library. Test auth checks, command routing, and message delivery. Never make real network calls in tests.

### Key design constraints

- **Don't import transport-specific code outside the transport package.** The orchestrator must remain transport-agnostic.
- **Use MessageBus for all async delivery.** Don't create direct-send shortcuts for background results.
- **Implement streaming if your platform supports message edits.** If not, use segment-based delivery (send chunks as separate messages). See `MessengerCapabilities` in `messenger/capabilities.py` — set flags like `supports_streaming_edit`, `supports_inline_buttons`, `supports_reactions` to declare your transport's feature matrix.
- **Handle rate limits.** Every messaging platform has them. Implement backoff in your transport, not in the orchestrator.

---

## Adding a CLI Provider

MOPS wraps CLI binaries as subprocesses. Adding a new provider means teaching MOPS how to invoke a new CLI and parse its output.

### Step 1: Understand the provider interface

All providers extend `BaseCLI(ABC)` from `cli/base.py`. This abstract base class defines two required methods:

```python
class BaseCLI(ABC):
    @abstractmethod
    async def send(
        self,
        prompt: str,
        resume_session: str | None = None,
        continue_session: bool = False,
        timeout_seconds: float | None = None,
        timeout_controller: TimeoutController | None = None,
    ) -> CLIResponse: ...

    @abstractmethod
    def send_streaming(
        self,
        prompt: str,
        resume_session: str | None = None,
        continue_session: bool = False,
        timeout_seconds: float | None = None,
        timeout_controller: TimeoutController | None = None,
    ) -> AsyncGenerator[StreamEvent, None]: ...
```

Study the existing implementations:

- `cli/claude_provider.py` (`ClaudeCodeCLI`) — Claude Code CLI
- `cli/codex_provider.py` (`CodexCLI`) — OpenAI Codex CLI
- `cli/gemini_provider.py` (`GeminiCLI`) — Google Gemini CLI

Each provider also defines:

1. **How to build the subprocess command** — CLI binary name, flags, session resume, model selection
2. **How to parse output** — stdout/stderr parsing, stream event extraction
3. **How to detect auth** — checking if the CLI is installed and authenticated (in `cli/auth.py`)
4. **Model registry** — available models and aliases (in `config.py`)

### Step 2: Create the provider

```python
# cli/newprovider_provider.py

from memoriant_ops_bot.cli.base import BaseCLI, CLIConfig, docker_wrap
from memoriant_ops_bot.cli.types import CLIResponse
from memoriant_ops_bot.cli.stream_events import StreamEvent

class NewProviderCLI(BaseCLI):
    """Wrapper for the newprovider CLI binary."""

    BINARY = "newprovider"

    def __init__(self, config: CLIConfig) -> None:
        self._config = config

    def _build_command(self, prompt: str, resume_session: str | None) -> list[str]:
        """Build the subprocess command list."""
        cmd = [self.BINARY]
        if resume_session:
            cmd.extend(["--resume", resume_session])
        if self._config.model:
            cmd.extend(["--model", self._config.model])
        cmd.append(prompt)
        return cmd

    async def send(self, prompt, resume_session=None, **kwargs) -> CLIResponse:
        """Execute CLI and return full response."""
        cmd = self._build_command(prompt, resume_session)
        cmd, cwd = docker_wrap(cmd, self._config)
        # subprocess execution, output parsing, session ID extraction
        ...

    async def send_streaming(self, prompt, resume_session=None, **kwargs):
        """Execute CLI and yield StreamEvent objects as output arrives."""
        cmd = self._build_command(prompt, resume_session)
        cmd, cwd = docker_wrap(cmd, self._config)
        # async generator yielding StreamEvent instances
        ...
```

The key patterns to follow from existing providers: use `docker_wrap()` to support Docker sandboxing, register processes in `ProcessRegistry` for abort support, and normalize output into `CLIResponse` / `StreamEvent` types.

### Step 3: Register in the factory

`cli/factory.py` maps provider names to implementations. The factory receives a `CLIConfig` (not a string name):

```python
# cli/factory.py
def create_cli(config: CLIConfig) -> BaseCLI:
    """Create a CLI backend instance based on config.provider."""
    if config.provider == "gemini":
        from memoriant_ops_bot.cli.gemini_provider import GeminiCLI
        return GeminiCLI(config)
    if config.provider == "codex":
        from memoriant_ops_bot.cli.codex_provider import CodexCLI
        return CodexCLI(config)
    if config.provider == "newprovider":
        from memoriant_ops_bot.cli.newprovider_provider import NewProviderCLI
        return NewProviderCLI(config)
    from memoriant_ops_bot.cli.claude_provider import ClaudeCodeCLI
    return ClaudeCodeCLI(config)
```

Imports are deferred (inside the function body) to avoid circular imports.

### Step 4: Add auth detection

In `cli/auth.py`, add a check for your CLI. Auth checks return an `AuthResult` dataclass containing the provider name, an `AuthStatus` enum (`AUTHENTICATED`, `INSTALLED`, `NOT_FOUND`), and optional auth file metadata:

```python
def check_newprovider_auth() -> AuthResult:
    """Check if newprovider CLI is installed and authenticated."""
    # Check binary exists (shutil.which or subprocess)
    # Check auth state (config files, token presence, etc.)
    # Return AuthResult(provider="newprovider", status=AuthStatus.AUTHENTICATED, ...)
    ...
```

This is called during onboarding and startup to determine provider availability.

### Step 5: Add model resolution

In `config.py`, update `ModelRegistry`. The existing pattern uses `frozenset` constants and a static `provider_for()` method. Claude models are hardcoded, Gemini uses aliases plus runtime-discovered models, and anything else falls through to Codex:

```python
# config.py — add your provider's known models
NEWPROVIDER_MODELS: frozenset[str] = frozenset({"small", "medium", "large"})

class ModelRegistry:
    @staticmethod
    def provider_for(model_id: str) -> str:
        if model_id in CLAUDE_MODELS:
            return "claude"
        if (
            model_id in _GEMINI_ALIASES
            or model_id in _runtime_gemini[0]
            or model_id.startswith(("gemini-", "auto-gemini-"))
        ):
            return "gemini"
        if model_id in NEWPROVIDER_MODELS:
            return "newprovider"
        return "codex"  # default fallback
```

If your provider supports runtime model discovery (like Codex and Gemini do), add a cache observer similar to `CodexCacheObserver` or `GeminiCacheObserver`.

### Step 6: Stream events (if supported)

If the CLI supports streaming output (JSON events, progressive text), add a stream event parser:

```python
# cli/newprovider_events.py

def parse_stream_event(line: str) -> StreamEvent | None:
    """Parse a single line of streaming output into a normalized event."""
    ...
```

Stream events are normalized to a common format in `cli/stream_events.py` so the orchestrator handles all providers uniformly.

### Step 7: Workspace rules

Add a rule file template for your provider:

```
memoriant_ops_bot/_home_defaults/workspace/NEWPROVIDER.md
```

This file is synced to `~/.mops/workspace/` and cron task folders. Add it to the Zone 2 overwrite list in `workspace/init.py` and the rule sync logic.

### Step 8: Tests

```
tests/cli/test_newprovider_provider.py
```

Mock subprocess calls. Test command building, output parsing, session ID extraction, and error handling. Test with various CLI output formats the provider might produce.

### Checklist for a complete provider integration

- [ ] Provider class extending `BaseCLI` with `send()` and `send_streaming()`
- [ ] Factory registration in `cli/factory.py` (`create_cli()`)
- [ ] Auth detection in `cli/auth.py` (returning `AuthResult`)
- [ ] Model registry entries in `config.py` (`ModelRegistry.provider_for()`)
- [ ] Stream event parser (if streaming is supported)
- [ ] Rule file template in `_home_defaults/workspace/`
- [ ] Zone 2 sync for rule files in `workspace/init.py`
- [ ] Onboarding wizard support in `cli/init_wizard.py`
- [ ] `/model` selector integration in `orchestrator/selectors/`
- [ ] `/diagnose` output for the new provider
- [ ] Tests with mocked subprocess calls
- [ ] Documentation update in README and provider-specific `.md`
