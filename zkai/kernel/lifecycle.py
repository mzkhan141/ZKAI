"""Lifecycle and Heartbeat management for the AI Kernel."""

import asyncio
import time
from typing import Callable, Dict, List, Optional
from zkai.core.logger import get_logger

logger = get_logger("kernel.lifecycle")


class LifecycleManager:
    """Manages boot up sequence, subsystem registrations, and shutdown ordering."""

    def __init__(self):
        self._startup_hooks: List[Callable[[], None]] = []
        self._shutdown_hooks: List[Callable[[], None]] = []
        self._is_running: bool = False

    def register_startup(self, hook: Callable[[], None]) -> None:
        self._startup_hooks.append(hook)

    def register_shutdown(self, hook: Callable[[], None]) -> None:
        self._shutdown_hooks.append(hook)

    def boot(self) -> None:
        logger.info("Executing Kernel Lifecycle startup sequence...")
        for hook in self._startup_hooks:
            try:
                hook()
            except Exception as e:
                logger.error(f"Startup hook error: {e}")
        self._is_running = True
        logger.info("Kernel Lifecycle boot completed successfully.")

    def shutdown(self) -> None:
        logger.info("Executing Kernel Lifecycle shutdown sequence...")
        for hook in reversed(self._shutdown_hooks):
            try:
                hook()
            except Exception as e:
                logger.error(f"Shutdown hook error: {e}")
        self._is_running = False
        logger.info("Kernel Lifecycle shutdown complete.")

    @property
    def is_running(self) -> bool:
        return self._is_running


class HeartbeatManager:
    """Periodic health tick and pulse monitor for Kernel components."""

    def __init__(self, interval_seconds: float = 2.0):
        self.interval_seconds = interval_seconds
        self._subsystems: Dict[str, Callable[[], bool]] = {}
        self._active: bool = False
        self._tick_count: int = 0

    def register_health_check(self, name: str, health_fn: Callable[[], bool]) -> None:
        self._subsystems[name] = health_fn

    def tick(self) -> Dict[str, bool]:
        self._tick_count += 1
        results = {}
        for name, fn in self._subsystems.items():
            try:
                results[name] = fn()
            except Exception as e:
                logger.warning(f"Health check failed for '{name}': {e}")
                results[name] = False
        return results

    @property
    def total_ticks(self) -> int:
        return self._tick_count
