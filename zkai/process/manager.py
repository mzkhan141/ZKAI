"""Process Management, Supervision, and Lifecycle Control."""

from typing import Any, Dict, List, Optional
from zkai.kernel.types import ProcessState
from zkai.process.process import AIProcess
from zkai.core.logger import get_logger

logger = get_logger("process.manager")


class ProcessRegistry:
    """Registry maintaining active AIProcess instances."""

    def __init__(self):
        self._processes: Dict[str, AIProcess] = {}

    def register(self, process: AIProcess) -> None:
        self._processes[process.process_id] = process

    def unregister(self, process_id: str) -> None:
        if process_id in self._processes:
            del self._processes[process_id]

    def get(self, process_id: str) -> Optional[AIProcess]:
        return self._processes.get(process_id)

    def list_all(self) -> List[AIProcess]:
        return list(self._processes.values())


class ResourceController:
    """Enforces resource limits per process."""

    def __init__(self):
        self.limits: Dict[str, Dict[str, float]] = {}

    def set_limit(self, process_id: str, resource: str, max_val: float) -> None:
        if process_id not in self.limits:
            self.limits[process_id] = {}
        self.limits[process_id][resource] = max_val

    def check_limits(self, process_id: str, current_usage: Dict[str, float]) -> bool:
        if process_id not in self.limits:
            return True
        for res, max_val in self.limits[process_id].items():
            if current_usage.get(res, 0.0) > max_val:
                return False
        return True


class LifecycleController:
    """Drives state machine transitions for AIProcess instances."""

    @staticmethod
    def transition(process: AIProcess, target_state: ProcessState) -> None:
        logger.debug(f"Process '{process.name}' state transition: {process.state.value} -> {target_state.value}")
        process.state = target_state


class CrashRecovery:
    """Handles process crash recovery and exponential restart backoff."""

    @staticmethod
    def recover(process: AIProcess) -> bool:
        process.crash_count += 1
        if process.crash_count <= process.max_restarts:
            logger.warning(f"Recovering crashed process '{process.name}' (attempt {process.crash_count}/{process.max_restarts})...")
            process.restart()
            return True
        else:
            logger.error(f"Process '{process.name}' exceeded max restarts ({process.max_restarts}). Marked FAILED.")
            process.state = ProcessState.FAILED
            return False


class Watchdog:
    """Monitors running processes for hangs and resource exhaustion."""

    def __init__(self, registry: ProcessRegistry, crash_recovery: CrashRecovery):
        self.registry = registry
        self.crash_recovery = crash_recovery

    def inspect_processes(self) -> None:
        for proc in self.registry.list_all():
            if proc.state == ProcessState.FAILED:
                self.crash_recovery.recover(proc)


class ProcessSupervisor:
    """Supervises running processes and automatically recovers failed tasks."""

    def __init__(self, registry: ProcessRegistry):
        self.registry = registry
        self.recovery = CrashRecovery()

    def supervise(self) -> None:
        for proc in self.registry.list_all():
            if proc.state == ProcessState.FAILED:
                self.recovery.recover(proc)


class ProcessManager:
    """Master Process Manager overseeing process start, stop, pause, resume, and monitoring."""

    def __init__(self):
        self.registry = ProcessRegistry()
        self.resource_controller = ResourceController()
        self.supervisor = ProcessSupervisor(self.registry)
        self.watchdog = Watchdog(self.registry, self.supervisor.recovery)

    def spawn(self, process: AIProcess) -> str:
        self.registry.register(process)
        process.start()
        return process.process_id

    def terminate(self, process_id: str) -> None:
        proc = self.registry.get(process_id)
        if proc:
            proc.stop()
            self.registry.unregister(process_id)

    def pause(self, process_id: str) -> None:
        proc = self.registry.get(process_id)
        if proc:
            proc.pause()

    def resume(self, process_id: str) -> None:
        proc = self.registry.get(process_id)
        if proc:
            proc.resume()

    def list_processes(self) -> List[AIProcess]:
        return self.registry.list_all()
