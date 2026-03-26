"""Bot command definitions shared across layers.

Commands are ordered by usage frequency (most used first).
Descriptions are kept ≤22 chars so mobile clients don't truncate.

This package also contains Memoriant-specific commands in
``memoriant_commands.py``.
"""

from __future__ import annotations

from memoriant_ops_bot.i18n import t_cmd


def get_bot_commands() -> list[tuple[str, str]]:
    """Return bot commands with translated descriptions."""
    return [
        # Daily
        ("new", t_cmd("bot.new")),
        ("stop", t_cmd("bot.stop")),
        ("interrupt", t_cmd("bot.interrupt")),
        ("model", t_cmd("bot.model")),
        ("status", t_cmd("bot.status")),
        ("memory", t_cmd("bot.memory")),
        # Automation & multi-agent
        ("session", t_cmd("bot.session")),
        ("tasks", t_cmd("bot.tasks")),
        ("cron", t_cmd("bot.cron")),
        ("agent_commands", t_cmd("bot.agent_commands")),
        # Browse & info
        ("showfiles", t_cmd("bot.showfiles")),
        ("info", t_cmd("bot.info")),
        ("help", t_cmd("bot.help")),
        # Maintenance (rare)
        ("diagnose", t_cmd("bot.diagnose")),
        ("upgrade", t_cmd("bot.upgrade")),
        ("restart", t_cmd("bot.restart")),
    ]


def get_multiagent_sub_commands() -> list[tuple[str, str]]:
    """Return multi-agent sub-commands with translated descriptions."""
    return [
        ("agents", t_cmd("multiagent.agents")),
        ("agent_start", t_cmd("multiagent.agent_start")),
        ("agent_stop", t_cmd("multiagent.agent_stop")),
        ("agent_restart", t_cmd("multiagent.agent_restart")),
        ("stop_all", t_cmd("multiagent.stop_all")),
    ]


# Backward-compatible module-level aliases.
BOT_COMMANDS: list[tuple[str, str]] = get_bot_commands()
MULTIAGENT_SUB_COMMANDS: list[tuple[str, str]] = get_multiagent_sub_commands()
