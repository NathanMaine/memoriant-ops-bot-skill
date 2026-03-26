# Frequently Asked Questions

## General

### What is MOPS?

MOPS is a Python service that lets you control AI coding agents (Claude Code, Codex CLI, Gemini CLI) from your phone via Telegram or Matrix. It runs on your machine, wraps the official CLI binaries as subprocesses, and streams responses back to your messaging app.

### How is this different from just using the Claude/ChatGPT mobile app?

Mobile apps talk to the provider's cloud API. MOPS talks to the CLI running on *your* machine — it has access to your filesystem, your projects, your local tools, and your hardware. It's the difference between asking an AI a question and having an AI agent operate on your workstation.

### Does this violate any provider terms of service?

No. MOPS runs the official CLI binaries exactly as documented. It doesn't patch SDKs, spoof headers, proxy API calls, or modify CLI behavior. It types your message into the CLI and reads the response — the same thing you do in a terminal, but bridged to your phone.

### What do I need to get started?

Python 3.11+, at least one authenticated CLI (`claude`, `codex`, or `gemini`), and either a Telegram bot token or a Matrix account. Docker is optional but recommended for sandboxing. That's it.

### Is it free?

Yes. MOPS is MIT licensed and uses your existing CLI subscriptions. There is no additional cost.

---

## Setup

### Which messaging platform should I use?

**Telegram** is the primary transport with the most features — live streaming via message edits, inline keyboards, forum topics for parallel conversations, and the most battle-tested code path.

**Matrix** is fully supported and better for self-hosted privacy setups with E2EE. Some features (webhook `wake` mode, startup recovery for named sessions) are currently Telegram-only.

You can run both simultaneously with `"transports": ["telegram", "matrix"]`.

### How do I get a Telegram bot token?

Message [@BotFather](https://t.me/BotFather) on Telegram, send `/newbot`, and follow the prompts. You'll get a token like `123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11`. Then message [@userinfobot](https://t.me/userinfobot) to get your numeric user ID for the allowlist.

### Can multiple people use the same bot?

Yes. Add their Telegram user IDs to `allowed_user_ids` in `config.json`. Each user gets isolated sessions. For group use, also add the group ID to `allowed_group_ids`.

### Can I run MOPS on a server I SSH into?

Yes. This is one of the primary use cases. Install on your VPS, GPU server, or any remote machine. MOPS runs as a background service and you control it from your phone anywhere.

### Does it work on Windows?

Yes. Native Windows is fully supported including service management via Task Scheduler. WSL also works (install as Linux inside WSL).

---

## Usage

### How do I switch between AI providers?

Send `/model` in chat. An interactive selector lets you pick Claude, Codex, or Gemini and choose a specific model. The choice sticks to the current chat or topic.

### Can I use different providers in different conversations?

Yes. In a Telegram group with topics, each topic can use a different provider. Named sessions and sub-agents can also use different providers. All choices are independent and persistent.

### What happens to my conversation when I switch providers?

Each provider has its own session bucket within a conversation. Switching from Claude to Codex preserves your Claude context — switch back and it's still there. `/new` resets only the active provider's session.

### How does streaming work?

On Telegram, MOPS edits messages in place as the response streams in — you see the text appear progressively. On Matrix, responses are sent as growing message segments. Streaming is configurable (chunk sizes, edit intervals, sentence breaks) in `config.json`.

### What's the difference between `/session` and background tasks?

`/session` creates a named background conversation — it has persistent memory and supports follow-ups (`@session-name more work`). Background tasks (via `TaskHub`) are one-shot delegated jobs with their own workspace folders and result injection back into the parent session. Use `/session` for ongoing side conversations, use tasks for discrete units of work.

### Can I send files to the bot?

Yes. Send images, documents, or other files through Telegram or Matrix. MOPS processes them (with configurable image resizing/compression) and passes them to the CLI. The CLI can also send files back through `workspace/output_to_user/`.

---

## Architecture

### Where is my data stored?

Everything is in `~/.mops/` on your machine. Plain JSON for state, Markdown for memory and rules, standard log files. No database, no external services, no cloud storage.

### Does MOPS phone home or collect telemetry?

No. Zero telemetry, zero analytics, zero external network calls. The only network traffic is between your machine and your messaging platform (Telegram/Matrix) and between the CLI and its provider (which the CLI handles independently).

### How does the Docker sandbox work?

When enabled, CLI execution happens inside a Docker container instead of directly on your host. The container has configurable host directory mounts (`docker.mounts`) and optional AI/ML packages. If Docker setup fails at startup, MOPS falls back to host execution gracefully.

### What happens if MOPS crashes?

On restart, MOPS classifies the lifecycle event (first start / service restart / system reboot), recovers in-flight turns from `inflight_turns.json`, and resumes eligible named sessions. If running as a background service, the service manager (systemd/launchd/Task Scheduler) auto-restarts it.

### Can sub-agents talk to each other?

Yes. Sub-agents communicate through the inter-agent bus and internal localhost API. They can delegate tasks to each other, and results flow back to the requesting agent's chat. Each sub-agent has its own isolated workspace and session state.

---

## Troubleshooting

### The bot isn't responding to my messages

1. Check that your user ID is in `allowed_user_ids` in `~/.mops/config/config.json`
2. Run `mops status` to check if the process is running
3. Check `~/.mops/logs/agent.log` for errors
4. Send `/diagnose` in chat for runtime diagnostics
5. Verify your CLI is authenticated: `claude --version`, `codex --version`, or `gemini --version`

### I get "provider not available" errors

The CLI binary for that provider isn't installed or isn't authenticated. Install and authenticate:

```bash
# Claude
npm install -g @anthropic-ai/claude-code && claude auth

# Codex
npm install -g @openai/codex && codex auth

# Gemini
npm install -g @google/gemini-cli
# then run gemini and complete authentication
```

### Streaming is choppy or messages aren't updating

Telegram has rate limits on message edits. Adjust streaming settings in `config.json`:

```json
{
  "streaming": {
    "edit_interval_seconds": 3.0,
    "min_chars": 300,
    "max_chars": 4000
  }
}
```

Increasing `edit_interval_seconds` reduces edit frequency. Increasing `min_chars` accumulates more text before each edit.

### Docker sandbox won't start

```bash
docker info                    # verify Docker is running
mops docker rebuild            # force rebuild the sandbox image
```

If Docker fails, MOPS falls back to host execution automatically. Check `~/.mops/logs/agent.log` for the specific error.

### How do I completely reset MOPS?

```bash
mops stop                      # stop the bot
rm -rf ~/.mops                 # remove all state
mops                           # re-run onboarding from scratch
```

### Where can I get help?

- [GitHub Issues](https://github.com/NathanMaine/memoriant-ops-bot/issues) for bugs and feature requests
- Check the [docs/](https://github.com/NathanMaine/memoriant-ops-bot/tree/main/docs) directory for detailed guides
- [Troubleshooting guide](troubleshooting.md) for in-depth diagnostic steps
- `/diagnose` in chat for runtime diagnostics
