# Troubleshooting

Diagnostic steps for common MOPS issues, organized by symptom.

## Quick Diagnostics

Before diving into specific issues, gather baseline info:

```bash
mops status                    # process state, PID, config path
```

In chat:

```
/diagnose                      # runtime diagnostics (providers, sessions, config)
/status                        # active session, provider, model
```

Logs:

```bash
tail -100 ~/.mops/logs/agent.log
# or
mops service logs              # if running as a service
```

---

## Bot Not Responding

### Symptom: Messages sent but no response, no typing indicator

**Check 1: Is the process running?**

```bash
mops status
```

If not running, start it:

```bash
mops                           # foreground
mops service start             # background service
```

**Check 2: Is your user ID in the allowlist?**

```bash
cat ~/.mops/config/config.json | grep -A5 allowed_user_ids
```

Your Telegram user ID (numeric) must be in the `allowed_user_ids` array. Get your ID from [@userinfobot](https://t.me/userinfobot) on Telegram.

**Check 3: Is the bot token correct?**

Verify in `config.json` that `telegram_token` matches what BotFather gave you. Common mistake: copying the token with trailing whitespace.

**Check 4: Is the bot added to the group?**

For group chats, the bot must be added as a member AND the group ID must be in `allowed_group_ids`. Use `/diagnose` to see which groups are authorized.

**Check 5: Is there a PID lock conflict?**

If MOPS was killed ungracefully, a stale PID lock might prevent restart:

```bash
ls ~/.mops/*.pid               # check for lock files
mops stop                      # clean shutdown attempt
mops                           # restart
```

### Symptom: Bot responds to some users but not others

User not in `allowed_user_ids`. Add their numeric Telegram user ID and the allowlist hot-reloads (no restart needed).

### Symptom: Bot responds in private chat but not in groups

- Group ID not in `allowed_group_ids`
- If `group_mention_only` is `true`, the bot only responds when mentioned by name or replied to
- Bot might lack group message permissions — check BotFather settings (disable privacy mode if needed)

---

## Provider Issues

### Symptom: "Provider not available" or no providers detected

The CLI binary isn't installed or isn't in `$PATH`.

```bash
which claude                   # should show a path
which codex
which gemini
```

If missing, install:

```bash
npm install -g @anthropic-ai/claude-code
npm install -g @openai/codex
npm install -g @google/gemini-cli
```

Then authenticate:

```bash
claude auth
codex auth
gemini                         # interactive auth flow
```

Restart MOPS after installing/authenticating new providers.

### Symptom: CLI installed but authentication fails

**Claude:** Run `claude auth` in a terminal with browser access. The auth flow requires a browser redirect.

**Codex:** Run `codex auth`. Check `~/.codex/` for credential files.

**Gemini:** Run `gemini` interactively first. Gemini may need API key mode — set `gemini_api_key` in `config.json` or `GEMINI_API_KEY` in `~/.mops/.env`.

### Symptom: Model not found or invalid model error

```
/model                         # see available models
/diagnose                      # shows detected models per provider
```

Codex and Gemini models are discovered at runtime and cached. Force a refresh:

```bash
rm ~/.mops/config/codex_models.json
rm ~/.mops/config/gemini_models.json
```

Then restart MOPS.

---

## Streaming Issues

### Symptom: Responses appear all at once instead of streaming

Check `streaming.enabled` in `config.json`:

```json
{
  "streaming": {
    "enabled": true
  }
}
```

If enabled but still not streaming, the provider might not support streaming for certain operations. Check logs for streaming-related errors.

### Symptom: Messages flicker or edit too rapidly

Telegram rate-limits message edits. Increase the edit interval:

```json
{
  "streaming": {
    "edit_interval_seconds": 3.0,
    "min_chars": 300
  }
}
```

### Symptom: Long responses get truncated

Telegram has a 4096-character message limit. MOPS handles this by splitting into multiple messages when `max_chars` is exceeded. If responses are still truncating, check:

```json
{
  "streaming": {
    "max_chars": 4000,
    "append_mode": false
  }
}
```

Setting `append_mode: true` sends continuation as new messages instead of editing.

---

## Docker Sandbox Issues

### Symptom: Docker sandbox won't start

```bash
docker info                    # is Docker running?
docker ps -a                   # is the sandbox container stuck?
```

Force rebuild:

```bash
mops docker rebuild            # removes container + image, rebuilds
```

If Docker consistently fails, MOPS falls back to host execution. Check logs for the specific error:

```bash
grep -i docker ~/.mops/logs/agent.log | tail -20
```

### Symptom: Docker build fails with extras

Large extras (PyTorch, Transformers) can timeout during build:

```bash
mops docker extras             # check which extras are selected
mops docker extras-remove transformers   # remove heavy extras temporarily
mops docker rebuild
```

### Symptom: Files not visible inside Docker container

Check your mounts:

```bash
mops docker mounts             # shows effective mount mapping
```

Mounts are mapped to `/mnt/<basename>` inside the container. If a directory doesn't exist on the host, it's silently skipped. Add mounts:

```bash
mops docker mount /path/to/project
mops docker rebuild            # apply mount changes
```

---

## Session Issues

### Symptom: `/new` doesn't seem to reset the conversation

`/new` resets only the **active provider's** session bucket. If you switched providers and switch back, the old context is still there. This is intentional — it preserves context per provider.

To reset everything for a topic/chat, switch to each provider and `/new` each one, or simply start working in a new topic.

### Symptom: Named sessions disappeared after restart

Named session asyncio task objects are lost on restart. The session data persists in `~/.mops/named_sessions.json`. On Telegram, startup recovery automatically resumes eligible sessions. On Matrix, auto-recovery is not yet implemented — resume manually with `/session @name follow-up`.

### Symptom: Topic sessions are mixing context

Verify topics are properly identified. In `/status`, check that the `topic_id` matches expectations. If sessions appear shared, the topic IDs might not be propagating correctly — check `~/.mops/sessions.json` for the session key format.

---

## Service Management Issues

### Symptom: Service won't start on boot (Linux)

User services require linger:

```bash
sudo loginctl enable-linger $(whoami)
```

Without linger, systemd kills user services on logout.

### Symptom: Service shows running but bot doesn't respond

The service might be in a crash loop. Check service status and logs:

```bash
mops service status
mops service logs
```

If the service is running but the bot isn't responding, there might be a config issue (bad token, missing providers). The service restarts on failure, which can mask configuration problems.

### Symptom: `mops stop` doesn't stop the service

`mops stop` attempts to stop the installed service first so it doesn't respawn. If that fails:

```bash
mops service stop              # stop the service explicitly
```

If the process is running outside the service:

```bash
mops status                    # shows PID
kill <PID>
```

### Symptom: Service logs show nothing (macOS/Windows)

On macOS and Windows, `mops service logs` tails `~/.mops/logs/agent.log` (not a system journal). If the file is empty or missing, the bot might not have started successfully. Run in foreground to see startup errors:

```bash
mops service stop
mops -v                        # verbose foreground
```

---

## Automation Issues

### Symptom: Cron jobs not running

1. Check `cron_jobs.json` exists and has valid entries
2. Verify the task folder exists: `ls ~/.mops/workspace/cron_tasks/<task-name>/`
3. Check quiet hours — jobs skip silently during quiet periods without updating `last_run_status`
4. Check dependencies — if `dependency` is set, the job waits for the dependency group lock
5. Verify the provider binary exists for the job's configured provider

```bash
cat ~/.mops/cron_jobs.json | python -m json.tool
```

### Symptom: Webhook returns errors

Common status codes:

- `401` — auth failed (check bearer token or HMAC secret)
- `404` — hook ID doesn't match any registered webhook
- `429` — rate limited (default 30/minute)
- `error:no_wake_handler` — `wake` mode on Matrix (use `cron_task` mode instead)
- `error:folder_missing` — task folder doesn't exist for `cron_task` mode

Test with curl:

```bash
curl -X POST http://127.0.0.1:8742/hooks/your-hook-id \
  -H "Authorization: Bearer your-token" \
  -H "Content-Type: application/json" \
  -d '{"message": "test"}'
```

### Symptom: Heartbeat never fires

- `heartbeat.enabled` must be `true` **at startup** (not hot-toggled)
- Check quiet hours: if current time is between `quiet_start` and `quiet_end`, heartbeat suppresses
- Check cooldown: heartbeat skips if the user was active within `cooldown_minutes`
- Check logs: `grep heartbeat ~/.mops/logs/agent.log | tail -10`

If you enabled heartbeat after startup, restart MOPS — the observer only starts if enabled at boot time.

---

## Matrix-Specific Issues

### Symptom: Matrix bot can't join encrypted rooms

Install the E2EE extra:

```bash
pip install "matrix-nio[e2e]"
# or for pipx
pipx inject memoriant-ops-bot "matrix-nio[e2e]"
```

The bot needs `libolm` for E2EE. On Ubuntu: `sudo apt install libolm-dev`. On macOS: `brew install libolm`.

### Symptom: Matrix credentials lost after restart

Credentials are stored in `~/.mops/<store_path>/credentials.json` (default `matrix_store`). If the store directory is deleted, the bot needs to re-authenticate. You can also set `access_token` and `device_id` explicitly in `config.json` as a backup.

### Symptom: Matrix commands conflict with Element

Element reserves some `/` commands. MOPS defaults to `!` prefix on Matrix (`!status`, `!model`, etc.). The `/` prefix also works but may collide with Element's built-in commands.

---

## Config Issues

### Symptom: Config changes aren't taking effect

Some settings hot-reload (model, provider, allowlists, streaming, heartbeat config values). Others require restart (transport, tokens, Docker, API, webhooks, timeouts). See `docs/config.md` for the complete hot-reload boundary list.

### Symptom: Config file is corrupted or missing keys

MOPS deep-merges config with defaults on every startup. Missing keys are added automatically without dropping existing values. If the file is malformed JSON:

```bash
python -c "import json; json.load(open('$HOME/.mops/config/config.json'))"
```

Fix JSON syntax errors, or delete and re-run onboarding:

```bash
rm ~/.mops/config/config.json
mops onboarding
```

### Symptom: Sub-agent changes aren't applied

Changes to `agents.json` are watched every 5 seconds. However, only transport/identity changes (token, homeserver) trigger auto-restart. For other field changes on a running sub-agent:

```
/agent_restart <name>
```

Or restart the bot entirely.

---

## Getting More Help

If none of the above resolves your issue:

1. Run `/diagnose` in chat and save the output
2. Collect the last 100 lines of `~/.mops/logs/agent.log`
3. Note your OS, Python version, and provider versions
4. Open an issue at [github.com/NathanMaine/memoriant-ops-bot/issues](https://github.com/NathanMaine/memoriant-ops-bot/issues) using the bug report template
