"""Project-level exception hierarchy."""


class MopsError(Exception):
    """Base for all mops exceptions."""


class CLIError(MopsError):
    """CLI execution failed."""


class WorkspaceError(MopsError):
    """Workspace initialization or access failed."""


class SessionError(MopsError):
    """Session persistence or lifecycle failed."""


class CronError(MopsError):
    """Cron job scheduling or execution failed."""


class StreamError(MopsError):
    """Streaming output failed."""


class SecurityError(MopsError):
    """Security violation detected."""


class PathValidationError(SecurityError):
    """File path failed validation."""


class WebhookError(MopsError):
    """Webhook server or dispatch failed."""
