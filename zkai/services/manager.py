"""ServiceManager, ServiceRegistry, and Health Monitoring for OS Services."""

from typing import Any, Dict, List, Optional
from zkai.kernel.types import ServiceState
from zkai.services.service import Service
from zkai.core.logger import get_logger

logger = get_logger("services.manager")


class ServiceRegistry:
    """Registry maintaining active OS Service instances."""

    def __init__(self):
        self._services: Dict[str, Service] = {}

    def register(self, service: Service) -> None:
        self._services[service.name] = service
        logger.info(f"Registered OS Service: '{service.name}'")

    def unregister(self, name: str) -> None:
        if name in self._services:
            del self._services[name]

    def get(self, name: str) -> Optional[Service]:
        return self._services.get(name)

    def list_services(self) -> List[Service]:
        return list(self._services.values())


class ConfigurationManager:
    """Handles dynamic configuration injection for OS services."""

    def __init__(self):
        self._configs: Dict[str, Dict[str, Any]] = {}

    def set_config(self, service_name: str, config: Dict[str, Any]) -> None:
        self._configs[service_name] = config

    def apply_config(self, service: Service) -> None:
        if service.name in self._configs:
            service.config.update(self._configs[service.name])


class HealthMonitor:
    """Performs periodic health checks across registered services."""

    def __init__(self, registry: ServiceRegistry):
        self.registry = registry

    def check_all(self) -> Dict[str, bool]:
        health_status = {}
        for srv in self.registry.list_services():
            is_ok = srv.is_healthy()
            health_status[srv.name] = is_ok
            if not is_ok:
                logger.warning(f"Service '{srv.name}' health check failed (state: {srv.state.value})")
        return health_status


class ServiceSupervisor:
    """Supervises service lifecycle and automatically restarts failed core services."""

    def __init__(self, registry: ServiceRegistry):
        self.registry = registry

    def restart_failed(self) -> List[str]:
        restarted = []
        for srv in self.registry.list_services():
            if srv.state in (ServiceState.FAILED, ServiceState.STOPPED):
                logger.info(f"ServiceSupervisor restarting service '{srv.name}'...")
                srv.start()
                restarted.append(srv.name)
        return restarted


class ServiceManager:
    """Master Service Manager managing registration, startup, shutdown, and health monitoring."""

    def __init__(self):
        self.registry = ServiceRegistry()
        self.config_manager = ConfigurationManager()
        self.health_monitor = HealthMonitor(self.registry)
        self.supervisor = ServiceSupervisor(self.registry)

    def register_and_start(self, service: Service) -> None:
        self.config_manager.apply_config(service)
        self.registry.register(service)
        service.start()

    def stop_service(self, name: str) -> None:
        srv = self.registry.get(name)
        if srv:
            srv.stop()

    def stop_all(self) -> None:
        for srv in self.registry.list_services():
            srv.stop()

    def list_services(self) -> List[Service]:
        return self.registry.list_services()
