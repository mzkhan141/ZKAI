"""Central AI Kernel and KernelRuntime for ZKAI AI Operating System."""

from typing import Any, Dict, List, Optional
from zkai.core.events import EventBus, default_event_bus
from zkai.core.logger import get_logger
from zkai.kernel.config import KernelConfig
from zkai.kernel.lifecycle import HeartbeatManager, LifecycleManager
from zkai.kernel.scheduler import KernelScheduler
from zkai.kernel.types import KernelState, ShutdownMode
from zkai.kernel.state_machine import KernelStateMachine
from zkai.kernel.boot import BootLoader, BootConfiguration, ServiceInitializationOrder
from zkai.kernel.shutdown import ShutdownSequence
from zkai.kernel.governance import ResourceGovernor

from zkai.kernel.microkernel import MicroKernel
from zkai.security.capability_os import CapabilityManager
from zkai.kernel.hypervisor import AIHypervisor
from zkai.kernel.self_healing import SelfRecoveryManager
from zkai.kernel.evolution import EvolutionEngine
from zkai.kernel.cognitive import CognitiveRuntime
from zkai.kernel.simulation import SimulationEngine
from zkai.kernel.digital_twin import DigitalTwin
from zkai.kernel.testing import AutonomousTesting
from zkai.kernel.semantic_scheduler import GoalScheduler
from zkai.kernel.intelligence import KernelIntelligence

logger = get_logger("kernel")


class AIKernel:
    """The central AI Kernel singleton coordinating processes, resources, and intelligence scheduling."""

    _instance: Optional["AIKernel"] = None

    def __init__(self, config: Optional[KernelConfig] = None):
        self.config = config or KernelConfig()
        self.state_machine = KernelStateMachine()
        self.scheduler = KernelScheduler(policy=self.config.scheduler_policy)
        self.governor = ResourceGovernor()
        self.lifecycle = LifecycleManager()
        self.heartbeat = HeartbeatManager(interval_seconds=self.config.heartbeat_interval)
        self.event_bus: EventBus = default_event_bus
        self._services: Dict[str, Any] = {}
        self._processes: Dict[str, Any] = {}
        self._service_deps: Dict[str, List[str]] = {}
        self.service_order = ServiceInitializationOrder()
        self.shutdown_sequence = ShutdownSequence(self)

        # Intelligent MicroKernel Operating Subsystems
        self.microkernel = MicroKernel()
        self.capability_manager = CapabilityManager()
        self.hypervisor = AIHypervisor()
        self.self_healing = SelfRecoveryManager()
        self.evolution = EvolutionEngine()
        self.cognitive = CognitiveRuntime()
        self.simulation = SimulationEngine()
        self.digital_twin = DigitalTwin()
        self.autonomous_testing = AutonomousTesting()
        self.goal_scheduler = GoalScheduler()
        self.intelligence = KernelIntelligence()

    @property
    def state(self) -> KernelState:
        return self.state_machine.current_state

    @classmethod
    def get_instance(cls, config: Optional[KernelConfig] = None) -> "AIKernel":
        if cls._instance is None:
            cls._instance = AIKernel(config=config)
        return cls._instance

    def boot(self, boot_config: Optional[BootConfiguration] = None) -> None:
        """Boots the AI Kernel through state machine transitions and BootLoader."""
        if self.state != KernelState.OFFLINE:
            logger.warning(f"Kernel boot called while state is '{self.state.value}'. Skipping.")
            return

        self.state_machine.transition_to(KernelState.BOOTING, reason="Kernel boot initiated")
        logger.info("Booting ZKAI AI Kernel...")
        
        loader = BootLoader(self, config=boot_config)
        loader.boot()
        
        self.state_machine.transition_to(KernelState.INITIALIZING, reason="Initializing registered services")
        self.lifecycle.boot()
        
        # Initialize registered services in dependency order
        ordered_services = self.service_order.compute()
        for name in ordered_services:
            if name in self._services:
                srv = self._services[name]
                if hasattr(srv, "start"):
                    try:
                        srv.start()
                    except Exception as e:
                        logger.error(f"Failed starting Kernel Service '{name}': {e}")

        self.state_machine.transition_to(KernelState.READY, reason="Kernel boot complete")
        logger.info("AI Kernel fully operational in READY state.")

    def shutdown(self, mode: ShutdownMode = ShutdownMode.GRACEFUL) -> None:
        """Shuts down the AI Kernel safely."""
        logger.info(f"Initiating AI Kernel shutdown (mode: {mode.value})...")
        self.shutdown_sequence.execute(mode=mode)
        self.lifecycle.shutdown()
        logger.info("AI Kernel shutdown complete.")

    def register_service(self, name: str, service_instance: Any, dependencies: Optional[List[str]] = None) -> None:
        """Registers a service under Kernel supervision with optional dependency list."""
        self._services[name] = service_instance
        self._service_deps[name] = dependencies or []
        self.service_order.add_service(name, dependencies=dependencies)
        logger.info(f"Registered Kernel Service: '{name}' (deps: {self._service_deps[name]})")

    def get_service(self, name: str) -> Optional[Any]:
        """Retrieves a registered service by name."""
        return self._services.get(name)

    def list_services(self) -> List[Any]:
        """Lists all registered service instances."""
        return list(self._services.values())

    def register_process(self, process_id: str, process_instance: Any) -> None:
        """Registers an active process with the Kernel."""
        self._processes[process_id] = process_instance

    def unregister_process(self, process_id: str) -> None:
        if process_id in self._processes:
            del self._processes[process_id]

    def list_processes(self) -> List[Any]:
        return list(self._processes.values())


class KernelRuntime:
    """Entry point runtime for bootstrapping AIKernel instances."""

    def __init__(self, config: Optional[KernelConfig] = None):
        self.kernel = AIKernel.get_instance(config)

    def start(self) -> None:
        self.kernel.boot()

    def stop(self) -> None:
        self.kernel.shutdown()
