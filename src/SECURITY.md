# Security Policy

## Supported Versions

| Version | Supported |
|---------|-----------|
| 0.15.x (latest) | Yes |
| < 0.15.0 | No |

Only the latest release receives security updates. Upgrade with `pipx upgrade memoriant-ops-bot`.

## Architecture Security Model

MOPS is designed with a local-first security model. Understanding the trust boundaries helps evaluate risk.

**What MOPS controls:**

- Subprocess execution of official CLI binaries (`claude`, `codex`, `gemini`) on your machine
- Telegram/Matrix message routing with dual-allowlist authentication
- Local file state in `~/.mops/` (JSON, Markdown, logs)
- Optional Docker sandbox for code execution isolation
- Optional WebSocket API with E2E encryption (NaCl Box)

**Trust boundaries:**

- **Messaging transport → your machine.** Telegram bot tokens and Matrix credentials grant message routing access. Protect these as you would SSH keys.
- **Allowlists are the auth layer.** Every message must pass both user ID and group ID checks. Unauthorized groups trigger auto-leave. Allowlists are hot-reloadable without restart.
- **CLI subprocesses inherit your shell environment.** MOPS does not sandbox CLI execution by default. Enable Docker sandboxing (`mops docker enable`) for untrusted or automated workloads.
- **Webhook/API endpoints are localhost-bound by default.** The webhook server binds to `127.0.0.1:8742`. The API server binds to `0.0.0.0:8741` but requires token auth + E2E encryption. Deploy behind a private network (Tailscale recommended) for remote access.

**What MOPS does NOT do:**

- Proxy or intercept API calls to AI providers
- Store or transmit your API keys (CLIs handle their own auth)
- Phone home, collect telemetry, or contact external services
- Modify CLI binaries or SDK behavior

## Reporting a Vulnerability

**Do not open a public GitHub issue for security vulnerabilities.**

Use GitHub's built-in private vulnerability reporting:

1. Go to the [Security tab](https://github.com/NathanMaine/memoriant-ops-bot/security) of this repository
2. Click **"Report a vulnerability"**
3. Fill in the advisory form with:
   - Description of the vulnerability
   - Steps to reproduce
   - Affected version(s)
   - Potential impact assessment
   - Suggested fix (if you have one)

Your report is private — only repository maintainers can see it. GitHub automatically adds you as a collaborator on the draft advisory so we can work together on a fix.

## Disclosure Timeline

- **Day 0:** Report received via GitHub Security Advisory, acknowledgment sent
- **Day 1–7:** Triage and initial assessment
- **Day 7–30:** Fix development and testing
- **Day 30:** Coordinated disclosure (or earlier if fix is ready)

We will credit reporters in the release notes unless anonymity is requested.

## Security Best Practices for Operators

**Credentials:**

- Keep `telegram_token` and Matrix credentials out of version control
- Use `~/.mops/.env` for external API secrets (not `config.json`)
- Rotate bot tokens if compromise is suspected

**Access control:**

- Keep `allowed_user_ids` and `allowed_group_ids` minimal
- Review allowlists periodically
- Use separate sub-agent bot tokens for different trust levels

**Execution isolation:**

- Enable Docker sandboxing for production and unattended deployments
- Configure `docker.mounts` to expose only needed directories
- Use `file_access: "workspace"` to restrict file operations to `~/.mops/workspace/`

**Network:**

- Run webhook and API servers behind a VPN or private network
- Use Tailscale or WireGuard for remote access rather than exposing ports directly
- Keep SSH key-only auth on VPS deployments

**Updates:**

- Subscribe to GitHub releases for security advisories
- Run `mops upgrade` or `pipx upgrade memoriant-ops-bot` regularly
