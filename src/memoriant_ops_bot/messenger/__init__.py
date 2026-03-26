"""Messenger abstraction layer — transport-agnostic protocols and registry."""

from memoriant_ops_bot.messenger.capabilities import MessengerCapabilities
from memoriant_ops_bot.messenger.commands import (
    DIRECT_COMMANDS,
    MULTIAGENT_COMMANDS,
    ORCHESTRATOR_COMMANDS,
    classify_command,
)
from memoriant_ops_bot.messenger.multi import MultiBotAdapter
from memoriant_ops_bot.messenger.notifications import (
    CompositeNotificationService,
    NotificationService,
)
from memoriant_ops_bot.messenger.protocol import BotProtocol
from memoriant_ops_bot.messenger.registry import create_bot
from memoriant_ops_bot.messenger.send_opts import BaseSendOpts

__all__ = [
    "DIRECT_COMMANDS",
    "MULTIAGENT_COMMANDS",
    "ORCHESTRATOR_COMMANDS",
    "BaseSendOpts",
    "BotProtocol",
    "CompositeNotificationService",
    "MessengerCapabilities",
    "MultiBotAdapter",
    "NotificationService",
    "classify_command",
    "create_bot",
]
