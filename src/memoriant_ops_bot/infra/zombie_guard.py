"""
Zombie Process Guard -- Memoriant Ops Bot
Prevents orphaned subprocess accumulation that caused 800%+ CPU in the original.
Fix for: https://github.com/PleasePrompto/notebooklm-mcp/issues/29

Safeguards:
1. Stdin EOF detection: detect parent disconnect and exit cleanly.
2. Idle timeout: warn at 30 min, self-terminate at 2 hours.
3. Process cleanup on shutdown: walk and kill all child subprocesses.
4. Heartbeat check: verify parent PID is still alive.
"""

from __future__ import annotations

import asyncio
import contextlib
import logging
import os
import signal
import sys
import time
from pathlib import Path

from memoriant_ops_bot.infra.process_tree import (
    force_kill_process_tree,
    list_process_descendants,
)

logger = logging.getLogger(__name__)

# -- Configuration -------------------------------------------------------------

IDLE_WARNING_SECONDS = 30 * 60  # 30 minutes
IDLE_TERMINATE_SECONDS = 2 * 60 * 60  # 2 hours
HEARTBEAT_INTERVAL_SECONDS = 60  # Check every 60 seconds
STDIN_CHECK_INTERVAL_SECONDS = 5  # Check stdin every 5 seconds


class ZombieGuard:
    """Prevents orphaned subprocess accumulation.

    Usage::

        guard = ZombieGuard()
        await guard.start()
        # ... bot runs ...
        await guard.stop()
    """

    def __init__(
        self,
        *,
        parent_pid: int | None = None,
        idle_warning: float = IDLE_WARNING_SECONDS,
        idle_terminate: float = IDLE_TERMINATE_SECONDS,
        on_terminate: asyncio.Event | None = None,
    ) -> None:
        self._parent_pid = parent_pid or os.getppid()
        self._idle_warning = idle_warning
        self._idle_terminate = idle_terminate
        self._on_terminate = on_terminate or asyncio.Event()
        self._last_activity = time.monotonic()
        self._running = False
        self._tasks: list[asyncio.Task[None]] = []
        self._warned_idle = False
        self._our_pid = os.getpid()

    @property
    def should_terminate(self) -> bool:
        """True if the guard has requested termination."""
        return self._on_terminate.is_set()

    @property
    def terminate_event(self) -> asyncio.Event:
        """Event that is set when termination is requested."""
        return self._on_terminate

    def record_activity(self) -> None:
        """Call this whenever a request is received to reset idle timer."""
        self._last_activity = time.monotonic()
        self._warned_idle = False

    async def start(self) -> None:
        """Start all guard background tasks."""
        if self._running:
            return
        self._running = True
        self._last_activity = time.monotonic()

        self._tasks = [
            asyncio.create_task(self._heartbeat_loop(), name="zombie-heartbeat"),
            asyncio.create_task(self._idle_loop(), name="zombie-idle"),
        ]

        # Only check stdin if we're not on Windows (stdin EOF detection)
        if sys.platform != "win32":
            self._tasks.append(asyncio.create_task(self._stdin_eof_loop(), name="zombie-stdin"))

        logger.info(
            "ZombieGuard started: parent_pid=%d, idle_warning=%ds, idle_terminate=%ds",
            self._parent_pid,
            int(self._idle_warning),
            int(self._idle_terminate),
        )

    async def stop(self) -> None:
        """Stop guard tasks and kill all child subprocesses."""
        self._running = False
        for task in self._tasks:
            task.cancel()
        for task in self._tasks:
            with contextlib.suppress(asyncio.CancelledError):
                await task
        self._tasks.clear()

        # Final cleanup: kill any remaining child processes
        await asyncio.to_thread(self._cleanup_children)
        logger.info("ZombieGuard stopped")

    def _cleanup_children(self) -> None:
        """Walk the subprocess tree and kill all children of our PID."""
        try:
            descendants = list_process_descendants(self._our_pid)
        except Exception:
            logger.debug("Failed to list process descendants", exc_info=True)
            return

        if not descendants:
            return

        logger.info(
            "ZombieGuard cleanup: killing %d child process(es): %s",
            len(descendants),
            descendants[:10],
        )

        for child_pid in descendants:
            try:
                force_kill_process_tree(child_pid)
            except Exception:
                logger.debug("Failed to kill child pid=%d", child_pid, exc_info=True)

    def _is_parent_alive(self) -> bool:
        """Check if the parent process is still running."""
        if self._parent_pid <= 1:
            # PID 1 = init/launchd, means we were already reparented
            return False

        if sys.platform == "win32":
            # On Windows, use os.kill with signal 0 to check
            try:
                os.kill(self._parent_pid, 0)
                return True
            except (OSError, PermissionError):
                return False
        else:
            # On POSIX, check if our current parent matches
            current_parent = os.getppid()
            if current_parent != self._parent_pid:
                # We were reparented (parent died)
                return False

            # Also verify with signal 0
            try:
                os.kill(self._parent_pid, 0)
                return True
            except ProcessLookupError:
                return False
            except PermissionError:
                # Process exists but we can't signal it -- still alive
                return True

    async def _heartbeat_loop(self) -> None:
        """Periodically verify the parent process is still alive."""
        try:
            while self._running:
                await asyncio.sleep(HEARTBEAT_INTERVAL_SECONDS)
                if not self._running:
                    break

                if not self._is_parent_alive():
                    logger.warning(
                        "ZombieGuard: parent process %d is gone, "
                        "requesting shutdown to prevent orphan",
                        self._parent_pid,
                    )
                    self._on_terminate.set()
                    return
        except asyncio.CancelledError:
            pass

    async def _idle_loop(self) -> None:
        """Monitor idle time and warn/terminate as needed."""
        try:
            while self._running:
                await asyncio.sleep(60)  # Check every minute
                if not self._running:
                    break

                idle_seconds = time.monotonic() - self._last_activity

                if idle_seconds >= self._idle_terminate:
                    logger.warning(
                        "ZombieGuard: idle for %.0f minutes, "
                        "self-terminating to prevent resource waste",
                        idle_seconds / 60,
                    )
                    self._on_terminate.set()
                    return

                if idle_seconds >= self._idle_warning and not self._warned_idle:
                    logger.warning(
                        "ZombieGuard: idle for %.0f minutes (will terminate at %.0f minutes)",
                        idle_seconds / 60,
                        self._idle_terminate / 60,
                    )
                    self._warned_idle = True
        except asyncio.CancelledError:
            pass

    async def _stdin_eof_loop(self) -> None:
        """Detect stdin closure (parent disconnect in MCP mode)."""
        try:
            loop = asyncio.get_running_loop()
            reader = asyncio.StreamReader()

            # Try to read from stdin; if it's closed, we get EOF
            try:
                transport, _ = await loop.connect_read_pipe(
                    lambda: asyncio.StreamReaderProtocol(reader),
                    sys.stdin,
                )
            except (OSError, ValueError):
                # stdin is not a pipe or already closed
                logger.debug("ZombieGuard: stdin is not a pipe, skipping EOF detection")
                return

            while self._running:
                try:
                    data = await asyncio.wait_for(
                        reader.read(1),
                        timeout=STDIN_CHECK_INTERVAL_SECONDS,
                    )
                    if not data:
                        # EOF -- parent disconnected
                        logger.warning(
                            "ZombieGuard: stdin EOF detected, "
                            "parent disconnected. Requesting shutdown."
                        )
                        self._on_terminate.set()
                        return
                except asyncio.TimeoutError:
                    continue
        except asyncio.CancelledError:
            pass
        except Exception:
            logger.debug("ZombieGuard: stdin monitoring error", exc_info=True)


# -- Module-level convenience --------------------------------------------------


_guard: ZombieGuard | None = None


def get_guard() -> ZombieGuard | None:
    """Return the global ZombieGuard instance, if started."""
    return _guard


async def start_zombie_guard(
    *,
    terminate_event: asyncio.Event | None = None,
) -> ZombieGuard:
    """Create and start the global ZombieGuard."""
    global _guard  # noqa: PLW0603
    _guard = ZombieGuard(on_terminate=terminate_event)
    await _guard.start()
    return _guard


async def stop_zombie_guard() -> None:
    """Stop and cleanup the global ZombieGuard."""
    global _guard  # noqa: PLW0603
    if _guard is not None:
        await _guard.stop()
        _guard = None
