"""Tests for MopsPaths and resolve_paths."""

from __future__ import annotations

import os
from pathlib import Path
from unittest.mock import patch

from memoriant_ops_bot.workspace.paths import MopsPaths, resolve_paths


def test_workspace_property() -> None:
    paths = MopsPaths(
        mops_home=Path("/home/test/.mops"),
        home_defaults=Path("/opt/mops/workspace"),
        framework_root=Path("/opt/mops"),
    )
    assert paths.workspace == Path("/home/test/.mops/workspace")


def test_config_path() -> None:
    paths = MopsPaths(
        mops_home=Path("/home/test/.mops"),
        home_defaults=Path("/opt/mops/workspace"),
        framework_root=Path("/opt/mops"),
    )
    assert paths.config_path == Path("/home/test/.mops/config/config.json")


def test_sessions_path() -> None:
    paths = MopsPaths(
        mops_home=Path("/home/test/.mops"),
        home_defaults=Path("/opt/mops/workspace"),
        framework_root=Path("/opt/mops"),
    )
    assert paths.sessions_path == Path("/home/test/.mops/sessions.json")


def test_logs_dir() -> None:
    paths = MopsPaths(
        mops_home=Path("/home/test/.mops"),
        home_defaults=Path("/opt/mops/workspace"),
        framework_root=Path("/opt/mops"),
    )
    assert paths.logs_dir == Path("/home/test/.mops/logs")


def test_home_defaults() -> None:
    paths = MopsPaths(
        mops_home=Path("/x"),
        home_defaults=Path("/opt/mops/workspace"),
        framework_root=Path("/opt/mops"),
    )
    assert paths.home_defaults == Path("/opt/mops/workspace")


def test_resolve_paths_explicit() -> None:
    paths = resolve_paths(mops_home="/tmp/test_home", framework_root="/tmp/test_fw")
    assert paths.mops_home == Path("/tmp/test_home").resolve()
    assert paths.framework_root == Path("/tmp/test_fw").resolve()


def test_resolve_paths_env_vars() -> None:
    with patch.dict(
        os.environ, {"MOPS_HOME": "/tmp/env_home", "MOPS_FRAMEWORK_ROOT": "/tmp/env_fw"}
    ):
        paths = resolve_paths()
        assert paths.mops_home == Path("/tmp/env_home").resolve()
        assert paths.framework_root == Path("/tmp/env_fw").resolve()


def test_resolve_paths_defaults() -> None:
    with patch.dict(os.environ, {}, clear=True):
        env_clean = {
            k: v for k, v in os.environ.items() if k not in ("MOPS_HOME", "MOPS_FRAMEWORK_ROOT")
        }
        with patch.dict(os.environ, env_clean, clear=True):
            paths = resolve_paths()
            assert paths.mops_home == (Path.home() / ".mops").resolve()
