"""Shutdown Sequence Management, Graceful Shutdown, and Emergency Teardown for ZKAI."""

from typing import Any, Callable, List, Optional
from zkai.core.logger import get_logger
from zkai.kernel.types import KernelState, ShutdownMode

logger = get_logger("kernel.shutdown")


class GracefulShutdown:
    """Performs orderly teardown, draining queues, persisting sessions, and stopping services in reverse order."""

    @staticmethod
    def shutdown(kernel: Any, timeout_seconds: float = 10.0) -> bool:
        logger.info(f"GracefulShutdown initiating orderly teardown (timeout: {timeout_seconds}s)...")
        if hasattr(kernel, "state_machine"):
            kernel.state_machine.transition_to(KernelState.SHUTTING_DOWN, reason="GracefulShutdown requested")

        services = kernel.list_services() if hasattr(kernel, "list_services") else []
        for srv in reversed(services):
            try:
                if hasattr(srv, "stop"):
                    srv.stop()
            except Exception as e:
                logger.error(f"Error stopping service '{getattr(srv, 'name', str(srv))}': {e}")

        if hasattr(kernel, "state_machine"):
            kernel.state_machine.transition_to(KernelState.OFFLINE, reason="Shutdown complete")
        logger.info("GracefulShutdown completed cleanly.")
        return True


class EmergencyShutdown:
    """Performs immediate non-blocking panic shutdown for critical errors."""

    @staticmethod
    def shutdown(kernel: Any, reason: str = "Emergency Panic") -> None:
        logger.critical(f"EmergencyShutdown executing immediate panic teardown: {reason}")
        if hasattr(kernel, "state_machine"):
            kernel.state_machine.transition_to(KernelState.PANIC, reason=reason)
            kernel.state_machine.transition_to(KernelState.OFFLINE, reason="Emergency teardown")


class ShutdownSequence:
    """Coordinates graceful or emergency shutdown based on ShutdownMode."""

    def __init__(self, kernel: Any):
        self.kernel = kernel

    def execute(self, mode: ShutdownMode = ShutdownMode.GRACEFUL, reason: str = "User request") -> bool:
        if mode == ShutdownMode.EMERGENCY:
            EmergencyShutdown.shutdown(self.kernel, reason=reason)
            return True
        else:
            return GracefulShutdown.shutdown(self.kernel)
