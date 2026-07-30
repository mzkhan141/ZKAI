"""Intelligent MicroKernel Architecture, Minimal Operating Primitives, and Kernel Service Loader for ZKAI."""

from dataclasses import dataclass, field
import time
import uuid
from typing import Any, Callable, Dict, List, Optional, Set
from zkai.core.events import Event, EventBus, default_event_bus
from zkai.core.logger import get_logger
from zkai.kernel.types import KernelState, ServiceState
from zkai.services.service import Service

logger = get_logger("kernel.microkernel")


class KernelBus(EventBus):
    """Low-level Kernel Message & Event Bus for MicroKernel primitives."""

    def __init__(self):
        super().__init__()
        self._kernel_channels: Dict[str, List[Callable[[Any], None]]] = {}

    def subscribe_channel(self, channel_name: str, handler: Callable[[Any], None]) -> None:
        if channel_name not in self._kernel_channels:
            self._kernel_channels[channel_name] = []
        self._kernel_channels[channel_name].append(handler)

    def publish_channel(self, channel_name: str, message: Any) -> None:
        for handler in self._kernel_channels.get(channel_name, []):
            try:
                handler(message)
            except Exception as e:
                logger.error(f"KernelBus channel '{channel_name}' error: {e}")


class IPCManager:
    """Inter-Process & Inter-Service Messaging Primitive within the MicroKernel."""

    def __init__(self, bus: Optional[KernelBus] = None):
        self.bus = bus or KernelBus()
        self._channels: Dict[str, Any] = {}

    def register_channel(self, name: str, channel_instance: Any) -> None:
        self._channels[name] = channel_instance

    def send(self, channel_name: str, payload: Any) -> bool:
        self.bus.publish_channel(channel_name, payload)
        return True


class ResourceManager:
    """Resource Accounting & Allocation Primitive within the MicroKernel."""

    def __init__(self):
        self._allocations: Dict[str, Dict[str, float]] = {}

    def allocate(self, entity_id: str, resource_type: str, amount: float) -> bool:
        if entity_id not in self._allocations:
            self._allocations[entity_id] = {}
        curr = self._allocations[entity_id].get(resource_type, 0.0)
        self._allocations[entity_id][resource_type] = curr + amount
        return True

    def release(self, entity_id: str, resource_type: str, amount: float) -> None:
        if entity_id in self._allocations and resource_type in self._allocations[entity_id]:
            curr = self._allocations[entity_id][resource_type]
            self._allocations[entity_id][resource_type] = max(0.0, curr - amount)

    def get_allocation(self, entity_id: str) -> Dict[str, float]:
        return self._allocations.get(entity_id, {})


class SchedulerCore:
    """Core Scheduling Engine Primitive managing execution task priority queues."""

    def __init__(self):
        self._queue: List[Dict[str, Any]] = []

    def schedule(self, task_id: str, priority: int, action: Callable[[], Any]) -> None:
        self._queue.append({"task_id": task_id, "priority": priority, "action": action, "timestamp": time.time()})
        self._queue.sort(key=lambda x: (-x["priority"], x["timestamp"]))

    def pop_next(self) -> Optional[Callable[[], Any]]:
        if not self._queue:
            return None
        return self._queue.pop(0)["action"]


class LifecycleCore:
    """MicroKernel Primitive for tracking system state transitions and uptime."""

    def __init__(self):
        self.start_time = time.time()
        self.state = KernelState.OFFLINE

    def transition(self, target_state: KernelState) -> None:
        logger.info(f"MicroKernel transition: {self.state.value} -> {target_state.value}")
        self.state = target_state

    def uptime_seconds(self) -> float:
        return time.time() - self.start_time


class KernelRegistry:
    """Central registry maintaining loaded MicroKernel services and modules."""

    def __init__(self):
        self._services: Dict[str, Any] = {}
        self._modules: Dict[str, Any] = {}

    def register_service(self, name: str, service: Any) -> None:
        self._services[name] = service

    def unregister_service(self, name: str) -> Optional[Any]:
        return self._services.pop(name, None)

    def get_service(self, name: str) -> Optional[Any]:
        return self._services.get(name)

    def list_services(self) -> List[str]:
        return list(self._services.keys())


class ServiceLoader:
    """Dynamic Kernel Service Loader supporting hot-reloading and independent service boot."""

    def __init__(self, registry: KernelRegistry):
        self.registry = registry

    def load_service(self, name: str, service_class: Any, *args: Any, **kwargs: Any) -> Any:
        instance = service_class(*args, **kwargs) if callable(service_class) else service_class
        if hasattr(instance, "start"):
            try:
                instance.start()
            except Exception as e:
                logger.error(f"ServiceLoader failed to start '{name}': {e}")
        self.registry.register_service(name, instance)
        logger.info(f"ServiceLoader successfully loaded service '{name}'")
        return instance

    def unload_service(self, name: str) -> bool:
        srv = self.registry.unregister_service(name)
        if srv and hasattr(srv, "stop"):
            try:
                srv.stop()
            except Exception as e:
                logger.error(f"Error stopping unloaded service '{name}': {e}")
        return srv is not None


class KernelModuleLoader:
    """Dynamic C/Python extension module loader for MicroKernel extensions."""

    def __init__(self):
        self.loaded_modules: Dict[str, Any] = {}

    def load_module(self, module_name: str, module_obj: Any) -> None:
        self.loaded_modules[module_name] = module_obj
        logger.info(f"KernelModuleLoader loaded module '{module_name}'")


class KernelHooks:
    """Kernel execution hook callbacks."""

    def __init__(self):
        self._pre_execution: List[Callable[[str], None]] = []
        self._post_execution: List[Callable[[str, Any], None]] = []

    def register_pre(self, hook: Callable[[str], None]) -> None:
        self._pre_execution.append(hook)

    def register_post(self, hook: Callable[[str, Any], None]) -> None:
        self._post_execution.append(hook)

    def run_pre(self, action_name: str) -> None:
        for fn in self._pre_execution:
            fn(action_name)

    def run_post(self, action_name: str, result: Any) -> None:
        for fn in self._post_execution:
            fn(action_name, result)


class KernelExtensions:
    """Container for dynamically loaded Kernel extensions."""

    def __init__(self):
        self.extensions: Dict[str, Any] = {}

    def add_extension(self, name: str, extension: Any) -> None:
        self.extensions[name] = extension


class KernelDiagnostics:
    """Diagnostic health checks for MicroKernel primitives."""

    @staticmethod
    def inspect(microkernel: Any) -> Dict[str, Any]:
        return {
            "state": getattr(microkernel.lifecycle.state, "value", str(microkernel.lifecycle.state)),
            "uptime": microkernel.lifecycle.uptime_seconds(),
            "services_count": len(microkernel.registry.list_services()),
        }


class KernelRecovery:
    """MicroKernel state recovery for failed Kernel Services."""

    @staticmethod
    def recover_service(loader: ServiceLoader, name: str, service_class: Any) -> Any:
        logger.warning(f"KernelRecovery re-booting failed service '{name}'")
        loader.unload_service(name)
        return loader.load_service(name, service_class)


class KernelCore:
    """Core executive binding all MicroKernel primitives together."""

    def __init__(self):
        self.bus = KernelBus()
        self.ipc = IPCManager(self.bus)
        self.resources = ResourceManager()
        self.scheduler = SchedulerCore()
        self.lifecycle = LifecycleCore()
        self.registry = KernelRegistry()
        self.loader = ServiceLoader(self.registry)
        self.hooks = KernelHooks()
        self.extensions = KernelExtensions()
        self.module_loader = KernelModuleLoader()


class MicroKernel:
    """The Intelligent MicroKernel containing minimal operating primitives."""

    def __init__(self):
        self.core = KernelCore()

    @property
    def lifecycle(self) -> LifecycleCore:
        return self.core.lifecycle

    @property
    def registry(self) -> KernelRegistry:
        return self.core.registry

    @property
    def loader(self) -> ServiceLoader:
        return self.core.loader

    def boot(self) -> None:
        self.core.lifecycle.transition(KernelState.BOOTING)
        self.core.lifecycle.transition(KernelState.READY)
        logger.info("MicroKernel fully initialized and in READY state.")

    def shutdown(self) -> None:
        self.core.lifecycle.transition(KernelState.SHUTTING_DOWN)
        for srv_name in list(self.registry.list_services()):
            self.loader.unload_service(srv_name)
        self.core.lifecycle.transition(KernelState.OFFLINE)
        logger.info("MicroKernel cleanly shut down.")
