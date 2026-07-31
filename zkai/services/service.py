"""Core OS Services and Base Service class for ZKAI AI Operating System."""

from typing import Any, Dict, Optional
from zkai.kernel.types import ServiceState
from zkai.core.logger import get_logger

logger = get_logger("services")


class Service:
    """Base class for all managed core services in the ZKAI AI Operating System."""

    def __init__(self, name: str):
        self.name: str = name
        self.state: ServiceState = ServiceState.REGISTERED
        self.config: Dict[str, Any] = {}
        self.metrics: Dict[str, float] = {}

    def start(self) -> None:
        self.state = ServiceState.STARTING
        logger.info(f"Starting OS Service '{self.name}'...")
        self.state = ServiceState.HEALTHY

    def stop(self) -> None:
        self.state = ServiceState.STOPPING
        logger.info(f"Stopping OS Service '{self.name}'...")
        self.state = ServiceState.STOPPED

    def is_healthy(self) -> bool:
        return self.state == ServiceState.HEALTHY

    def get_metrics(self) -> Dict[str, float]:
        """Returns service metrics dictionary."""
        return dict(self.metrics)


class InferenceService(Service):
    def __init__(self):
        super().__init__("inference_service")


class MemoryService(Service):
    def __init__(self):
        super().__init__("memory_service")


class EmbeddingService(Service):
    def __init__(self):
        super().__init__("embedding_service")


class VisionService(Service):
    def __init__(self):
        super().__init__("vision_service")


class SpeechService(Service):
    def __init__(self):
        super().__init__("speech_service")


class KnowledgeService(Service):
    def __init__(self):
        super().__init__("knowledge_service")


class BrowserService(Service):
    def __init__(self):
        super().__init__("browser_service")


class WorkflowService(Service):
    def __init__(self):
        super().__init__("workflow_service")


class PluginService(Service):
    def __init__(self):
        super().__init__("plugin_service")


class SecurityService(Service):
    def __init__(self):
        super().__init__("security_service")


class StorageService(Service):
    def __init__(self):
        super().__init__("storage_service")
