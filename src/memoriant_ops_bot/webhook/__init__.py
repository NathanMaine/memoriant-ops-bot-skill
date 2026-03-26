"""Webhook system: HTTP ingress for external event triggers."""

from memoriant_ops_bot.webhook.manager import WebhookManager
from memoriant_ops_bot.webhook.models import WebhookEntry, WebhookResult

__all__ = ["WebhookEntry", "WebhookManager", "WebhookResult"]
