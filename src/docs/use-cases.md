<p align="center">
  <img src="images/mops-logo.jpeg" alt="MOPS" width="200">
</p>

# Use Cases and Workflows

Real patterns for using MOPS. Each scenario shows the actual commands and flow.

## 1 — Solo Developer with Multiple Machines

**Setup:** MacBook for daily work, Linux VPS for CI/deployment, home server for GPU tasks. One Telegram chat controls all three.

Install MOPS on each machine with the same Telegram bot token and your user ID. Each machine runs its own MOPS instance. Send messages from one Telegram chat and the active instance responds.

For parallel control, use separate bot tokens per machine:

```bash
# On the VPS
mops   # onboarding with vps-bot token

# On the GPU server
mops   # onboarding with gpu-bot token
```

Now you have two Telegram chats — one per machine — both accessible from your phone.

**Typical session:**

```
[VPS chat]
You:   Check if the deploy pipeline finished
Bot:   [Claude streams deployment status]

[GPU chat]
You:   /model gemini
You:   What's the GPU utilization right now?
Bot:   [Gemini checks nvidia-smi output]
```

## 2 — Project Isolation with Telegram Topics

**Setup:** One Telegram group with topics enabled. Each topic maps to a different project context.

Create a Telegram group, enable topics, and add the group ID to `allowed_group_ids`. Each topic gets its own isolated session — provider, model, and conversation history are independent.

```
My Projects/
  Backend API    → Claude, working on auth refactor
  Frontend       → Codex, writing React components
  Data Pipeline  → Gemini, analyzing schemas
  DevOps         → Claude, Kubernetes configs
  Research       → Gemini, reading long docs
```

Switch providers per-topic with `/model`. The choice sticks to that topic only.

**Why this works:** Five parallel AI conversations from one group chat. No context bleed. Each topic preserves its own session across restarts.

## 3 — Background Research While You Code

**Setup:** You're in a focused coding session but need competitive research done.

```
You:   Fix the race condition in the session manager
Bot:   [Claude works on the fix, streaming live]

You:   /session Research the top 5 open-source alternatives to our auth library and
       write a comparison table with license, last commit date, and star count
Bot:   → Started background session "swiftfox"
Bot:   [you keep chatting about the race condition]

...10 minutes later...

Bot:   ✅ swiftfox complete — [comparison table appears]
```

The named session runs in the background with its own context. Your main conversation is uninterrupted.

**Follow up later:**

```
You:   @swiftfox Add pricing information for the commercial options
Bot:   → Background follow-up on swiftfox
```

## 4 — Scheduled Reports with Cron

**Setup:** Daily standup summary, weekly dependency audit, monthly cost report — all automated.

Cron jobs run in isolated task folders under `~/.mops/workspace/cron_tasks/`. Each folder has its own `TASK_DESCRIPTION.md` and optional scripts.

Create the task folder and description:

```bash
mkdir -p ~/.mops/workspace/cron_tasks/daily-standup
```

Then tell MOPS about it through chat — the AI creates the cron entry via `/cron`. Or edit `~/.mops/cron_jobs.json` directly:

```json
[
  {
    "id": "daily-standup",
    "cron": "0 9 * * 1-5",
    "task_folder": "daily-standup",
    "provider": "claude",
    "model": "sonnet",
    "quiet_start": 22,
    "quiet_end": 7
  }
]
```

This runs Monday through Friday at 9 AM, skips quiet hours, and posts the result to your chat.

**Per-job overrides:** Each cron job can use a different provider, model, reasoning effort, and CLI parameters. A weekly deep analysis might use `opus` while daily checks use `sonnet`.

## 5 — Webhook-Triggered Automation

**Setup:** GitHub pushes trigger code review. Monitoring alerts trigger incident triage.

Enable webhooks in config:

```json
{
  "webhooks": {
    "enabled": true,
    "host": "127.0.0.1",
    "port": 8742
  }
}
```

Register a hook through chat or `~/.mops/webhooks.json`:

```json
[
  {
    "id": "github-push",
    "mode": "cron_task",
    "task_folder": "code-review",
    "auth_mode": "hmac",
    "auth_secret": "your-webhook-secret",
    "provider": "claude",
    "model": "opus"
  }
]
```

GitHub sends `POST http://your-server:8742/hooks/github-push` with the push payload. MOPS runs the code review task and posts results to your chat.

**Two modes:**

- `wake` — injects the payload into your active chat session (conversational)
- `cron_task` — runs an isolated one-shot execution in a task folder (autonomous)

## 6 — Multi-Provider Comparison

**Setup:** You want to see how different AI providers handle the same task.

Use Telegram topics or named sessions to run the same prompt across providers:

```
[Topic: Claude Review]
You:   /model claude
You:   Review this API design for security issues: [paste]

[Topic: Codex Review]
You:   /model codex
You:   Review this API design for security issues: [paste]

[Topic: Gemini Review]
You:   /model gemini
You:   Review this API design for security issues: [paste]
```

Three reviews running in parallel, each in its own context. Compare results side by side in the Telegram group.

## 7 — Sub-Agents for Specialized Roles

**Setup:** A dedicated research agent and a dedicated coding agent, each with their own workspace and memory.

```bash
mops agents add researcher
# → prompts for bot token, user ID, provider (gemini)

mops agents add coder
# → prompts for bot token, user ID, provider (codex)
```

Now you have three Telegram chats:

- **Main** — general orchestration (Claude)
- **researcher** — long-context research (Gemini)
- **coder** — fast code edits (Codex)

Each has its own workspace under `~/.mops/agents/<n>/`, its own session state, and its own persistent memory. They can delegate tasks to each other through the inter-agent bus.

**Cross-agent delegation:**

```
[Main chat]
You:   Research the compliance requirements for SOC 2 Type II and
       write a checklist. Delegate to the researcher agent.
Bot:   → Delegated to researcher
...
Bot:   ← researcher completed: [checklist appears in your main chat]
```

## 8 — Remote Server Management from Phone

**Setup:** MOPS on a production server. You're at lunch and get an alert.

```
You:   Check the last 50 lines of /var/log/app/error.log
Bot:   [Claude reads the log and summarizes the errors]

You:   That looks like the database connection pool is exhausted.
       Show me the current connection count and the pool config.
Bot:   [runs queries, shows results]

You:   Increase the pool max to 50 and restart the app service
Bot:   [Claude executes the changes with confirmation]
```

For sensitive operations, enable Docker sandboxing so the AI operates in an isolated container with only mounted directories accessible.

## 9 — Matrix for Self-Hosted Privacy

**Setup:** You run a Matrix homeserver and don't want data flowing through Telegram's servers.

```bash
mops install matrix
mops
# → onboarding selects Matrix transport
# → provide homeserver URL, bot user ID, password
# → configure allowed rooms and users
```

Matrix supports E2EE rooms, so your conversations with the AI agent are encrypted end-to-end on your own infrastructure.

Commands use `!` prefix by default (`!status`, `!model`, `!session`). Streaming uses segment-based delivery instead of message edits. Reactions serve as interaction buttons.

**Dual-transport:** Run both Telegram and Matrix simultaneously:

```json
{
  "transports": ["telegram", "matrix"]
}
```

Same agent, same workspace, both transports active in parallel.

## 10 — Heartbeat Monitoring

**Setup:** The AI proactively checks on things and only messages you when something needs attention.

```json
{
  "heartbeat": {
    "enabled": true,
    "interval_minutes": 30,
    "quiet_start": 22,
    "quiet_end": 7
  }
}
```

Every 30 minutes (outside quiet hours), the heartbeat prompts the AI to review its memory and cron context. If everything is fine, it responds with `HEARTBEAT_OK` (suppressed — you see nothing). If something needs attention, the alert appears in your chat.

**Per-group targets:** Run heartbeat checks in specific group topics with custom prompts:

```json
{
  "heartbeat": {
    "enabled": true,
    "group_targets": [
      {
        "chat_id": -1001234567890,
        "topic_id": 42,
        "prompt": "Check project build status and alert if any failures.",
        "interval_minutes": 60
      }
    ]
  }
}
```

## Quick Reference: Choosing the Right Mode

| Need | Mode | Setup |
|------|------|-------|
| Quick question from phone | Single chat | Default — just message the bot |
| Multiple projects in parallel | Group topics | Create Telegram group + enable topics |
| Side task without losing context | Named session | `/session <prompt>` |
| Long-running autonomous work | Background task | Delegated via task tools |
| Scheduled recurring work | Cron job | `cron_jobs.json` + task folder |
| Event-driven automation | Webhook | `webhooks.json` + HTTP endpoint |
| Specialized agent roles | Sub-agents | `mops agents add <n>` |
| Proactive monitoring | Heartbeat | `heartbeat.enabled: true` |
