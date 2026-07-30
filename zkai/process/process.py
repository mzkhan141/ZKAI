"""Managed AI Process hierarchy for ZKAI AI Operating System."""

import uuid
from typing import Any, Dict, Optional
from zkai.kernel.types import ProcessState
from zkai.core.logger import get_logger

logger = get_logger("process")


class AIProcess:
    """Base class for all managed processes in the ZKAI AI Operating System."""

    def __init__(self, name: str, priority: int = 5):
        self.process_id: str = str(uuid.uuid4())
        self.name: str = name
        self.priority: int = priority
        self.state: ProcessState = ProcessState.CREATED
        self.crash_count: int = 0
        self.max_restarts: int = 3
        self.metadata: Dict[str, Any] = {}

    def start(self) -> None:
        self.state = ProcessState.STARTING
        logger.info(f"Starting process '{self.name}' ({self.process_id})...")
        self.state = ProcessState.RUNNING

    def stop(self) -> None:
        self.state = ProcessState.STOPPING
        logger.info(f"Stopping process '{self.name}' ({self.process_id})...")
        self.state = ProcessState.STOPPED

    def pause(self) -> None:
        if self.state == ProcessState.RUNNING:
            self.state = ProcessState.PAUSED
            logger.info(f"Paused process '{self.name}' ({self.process_id})")

    def resume(self) -> None:
        if self.state == ProcessState.PAUSED:
            self.state = ProcessState.RUNNING
            logger.info(f"Resumed process '{self.name}' ({self.process_id})")

    def restart(self) -> None:
        logger.info(f"Restarting process '{self.name}' ({self.process_id})...")
        self.stop()
        self.start()


class AgentProcess(AIProcess):
    """Managed process wrapper for autonomous Agents."""

    def __init__(self, name: str, agent_instance: Any, priority: int = 10):
        super().__init__(name=name, priority=priority)
        self.agent_instance = agent_instance


class ServiceProcess(AIProcess):
    """Managed process wrapper for OS Services."""

    def __init__(self, name: str, service_instance: Any, priority: int = 8):
        super().__init__(name=name, priority=priority)
        self.service_instance = service_instance


class WorkflowProcess(AIProcess):
    """Managed process wrapper for DAG Workflows."""

    def __init__(self, name: str, workflow_runner: Any, priority: int = 5):
        super().__init__(name=name, priority=priority)
        self.workflow_runner = workflow_runner


class ModelProcess(AIProcess):
    """Managed process wrapper for active Inference Models."""

    def __init__(self, name: str, model_instance: Any, priority: int = 7):
        super().__init__(name=name, priority=priority)
        self.model_instance = model_instance


class SandboxProcess(AIProcess):
    """Managed process executing within capability-restricted sandbox boundaries."""

    def __init__(self, name: str, code: str, priority: int = 1):
        super().__init__(name=name, priority=priority)
        self.code = code
