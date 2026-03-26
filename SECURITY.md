# Security Policy

## What This Plugin Does

This plugin consists entirely of markdown instruction files (SKILL.md and agent .md files). It contains:
- No executable code
- No shell scripts
- No network calls
- No file system modifications beyond what Claude Code normally does

All agent management, command routing, and session control is performed by Claude Code using its standard tools, guided by the skill instructions in this plugin.

## MOPS Security Model

The MOPS system this plugin interfaces with uses a dual-allowlist model:
- Private chats: sender user ID must be in the allowlist
- Group chats: both group ID and user ID must be in the allowlist
- Allowlists are maintained in `~/.mops/config/config.json`
- Unauthorized groups trigger automatic leave behavior in the MOPS daemon

This plugin reads and updates MOPS registry files (`~/.mops/`) but does not bypass MOPS security controls.

## Data Handling

- Agent registry files (`~/.mops/agents.json`, etc.) are read and written locally
- Conversation history is stored in `~/.mops/workspace/` on your local machine
- No agent data, session history, or task results are transmitted by this plugin
- Commands routed to AI CLIs (Claude, Codex, Gemini) follow those tools' own data handling policies

## Sensitive Configuration

Never store API keys, bot tokens, or credentials in MOPS registry files directly. Use your platform's secure credential management (keychain, environment variables, secret managers).

## Reporting a Vulnerability

If you discover a security issue, please email nathan@memoriant.com (do not open a public issue).

We will respond within 48 hours and provide a fix timeline.

## Auditing This Plugin

This plugin is easy to audit:
1. All files are markdown — readable in any text editor
2. No `node_modules`, no Python packages, no compiled binaries
3. Review any SKILL.md file to see exactly what instructions are given to the AI
4. The `.claude-plugin/plugin.json` lists all skills and agents declared by this plugin
