# Roadmap

Current priorities and planned work for MOPS. Updated as items are completed.

## Immediate (Next Release)

- [x] GitHub Release + PyPI listing for v0.15.0
- [ ] CI test workflow + badge in README
- [ ] `CODE_OF_CONDUCT.md` (Contributor Covenant)
- [ ] Enable GitHub Discussions
- [ ] Demo video (2-3 min walkthrough: install → onboarding → first message → provider switch → named session)

## Short-Term

- [ ] PyPI project page with full description and metadata
- [ ] GitHub Actions: automated test matrix (Python 3.11–3.14, Ubuntu/macOS/Windows)
- [ ] GitHub Actions: auto-publish to PyPI on tagged release
- [ ] Pre-built config templates (solo dev, team, multi-machine)
- [ ] Onboarding GIF/screenshots in installation docs

## Transport Plugins

- [ ] Discord transport (`BotProtocol` implementation)
- [ ] Slack transport
- [ ] Signal transport
- [ ] IRC transport

## Provider Integrations

- [ ] Auto-detect new CLI providers at startup
- [ ] Provider health monitoring (detect when a CLI stops responding)
- [ ] Cost tracking across providers

## Core Features

- [ ] MCP server integration (expose MOPS capabilities as MCP tools)
- [ ] Web dashboard for session/task/cron monitoring
- [ ] Mobile companion app (lightweight status + quick commands)
- [ ] File sync between phone and agent workspace (beyond Telegram file sends)
- [ ] Voice message support (speech-to-text → CLI → text-to-speech)

## Multi-Agent & Orchestration

- [ ] Agent-to-agent task routing with priority and load balancing
- [ ] Agent templates (pre-configured roles: researcher, coder, reviewer, ops)
- [ ] Shared context window across agents (selective memory sharing)
- [ ] Agent performance metrics and comparison

## Security & Hardening

- [ ] Docker seccomp profiles and resource limits
- [ ] Network isolation for sandboxed execution
- [ ] Audit logging for all CLI executions
- [ ] Rate limiting per user/group

## Developer Experience

- [ ] `mops doctor` command (comprehensive environment check)
- [ ] Plugin scaffolding CLI (`mops plugin init <transport|provider>`)
- [ ] Automated integration test suite with mock CLIs
- [ ] Documentation site (GitHub Pages or similar)

## Community

- [ ] Contributor spotlight in release notes
- [ ] Example cron task library (common automation patterns)
- [ ] Example webhook integrations (GitHub, GitLab, Sentry, PagerDuty)

---

Have an idea? [Open a feature request](https://github.com/NathanMaine/memoriant-ops-bot/issues/new?template=2-feature-request.yml) or start a discussion.
