"""Tests for the exception hierarchy."""

from memoriant_ops_bot.errors import (
    CLIError,
    MopsError,
    MopsError,
    PathValidationError,
    SecurityError,
    WorkspaceError,
)


def test_base_error_is_exception() -> None:
    assert issubclass(MopsError, Exception)


def test_cli_error_inherits_base() -> None:
    err = CLIError("cli broke")
    assert isinstance(err, MopsError)
    assert str(err) == "cli broke"


def test_workspace_error_inherits_base() -> None:
    assert isinstance(WorkspaceError("no workspace"), MopsError)


def test_security_error_inherits_base() -> None:
    assert isinstance(SecurityError("blocked"), MopsError)


def test_path_validation_error_inherits_security() -> None:
    err = PathValidationError("outside root")
    assert isinstance(err, SecurityError)
    assert isinstance(err, MopsError)


def test_catch_all_with_base() -> None:
    """All subclasses catchable via MopsError."""
    for cls in (CLIError, WorkspaceError, SecurityError, PathValidationError):
        try:
            raise cls("test")
        except MopsError:
            pass


def test_mops_error_is_same_as_mops_error() -> None:
    """MopsError is the new canonical name, MopsError is a backward-compat alias."""
    assert MopsError is MopsError
    assert issubclass(CLIError, MopsError)
