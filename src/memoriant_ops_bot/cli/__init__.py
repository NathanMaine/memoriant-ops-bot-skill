"""CLI layer: provider abstraction, process tracking, streaming."""

from memoriant_ops_bot.cli.auth import AuthResult as AuthResult
from memoriant_ops_bot.cli.auth import AuthStatus as AuthStatus
from memoriant_ops_bot.cli.auth import check_all_auth as check_all_auth
from memoriant_ops_bot.cli.base import BaseCLI as BaseCLI
from memoriant_ops_bot.cli.base import CLIConfig as CLIConfig
from memoriant_ops_bot.cli.coalescer import CoalesceConfig as CoalesceConfig
from memoriant_ops_bot.cli.coalescer import StreamCoalescer as StreamCoalescer
from memoriant_ops_bot.cli.factory import create_cli as create_cli
from memoriant_ops_bot.cli.process_registry import ProcessRegistry as ProcessRegistry
from memoriant_ops_bot.cli.service import CLIService as CLIService
from memoriant_ops_bot.cli.service import CLIServiceConfig as CLIServiceConfig
from memoriant_ops_bot.cli.types import AgentRequest as AgentRequest
from memoriant_ops_bot.cli.types import AgentResponse as AgentResponse
from memoriant_ops_bot.cli.types import CLIResponse as CLIResponse

__all__ = [
    "AgentRequest",
    "AgentResponse",
    "AuthResult",
    "AuthStatus",
    "BaseCLI",
    "CLIConfig",
    "CLIResponse",
    "CLIService",
    "CLIServiceConfig",
    "CoalesceConfig",
    "ProcessRegistry",
    "StreamCoalescer",
    "check_all_auth",
    "create_cli",
]
