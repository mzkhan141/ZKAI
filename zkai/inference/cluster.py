"""InferenceCluster and ClusterCoordinator managing distributed cluster nodes and automatic failover."""

from typing import Any, Dict, List, Optional
from zkai.inference.gpu_allocator import GPUAllocator
from zkai.inference.replica import ModelReplica, ReplicaManager
from zkai.inference.load_balancer import LoadBalancer, RequestRouter
from zkai.inference.transport import NetworkTransport, SimulatedTransport
from zkai.core.logger import get_logger

logger = get_logger("inference.cluster")


class ClusterCoordinator:
    """Monitors cluster replica health, initiates automatic failover and node recovery."""

    def __init__(self, replica_manager: ReplicaManager):
        self.replica_manager = replica_manager

    def perform_health_check(self) -> Dict[str, str]:
        """Checks status of all registered cluster replicas."""
        statuses = {}
        for r_id, replica in self.replica_manager.replicas.items():
            # Auto-recovery if status was failed
            if replica.status == "failed":
                replica.status = "active"
                logger.info(f"Auto-failover recovered replica '{r_id}'")
            statuses[r_id] = replica.status
        return statuses

    def trigger_failover(self, failed_replica_id: str) -> None:
        """Marks replica as failed and triggers failover reallocation."""
        if failed_replica_id in self.replica_manager.replicas:
            self.replica_manager.replicas[failed_replica_id].status = "failed"
            logger.warning(f"Triggered cluster failover for failed replica '{failed_replica_id}'")


class InferenceCluster:
    """Master Distributed Inference Cluster facade controlling allocation, routing, and transport."""

    def __init__(
        self,
        cluster_name: str = "zkai_cluster",
        single_gpu_mode: bool = True,
        transport: Optional[NetworkTransport] = None,
    ):
        self.cluster_name = cluster_name
        self.gpu_allocator = GPUAllocator(single_gpu_mode=single_gpu_mode)
        self.replica_manager = ReplicaManager()
        self.coordinator = ClusterCoordinator(self.replica_manager)
        self.load_balancer = LoadBalancer(self.replica_manager)
        self.router = RequestRouter(self.load_balancer)
        self.transport = transport or SimulatedTransport()

        self._initialize_default_node()

    def _initialize_default_node(self) -> None:
        dev_id = self.gpu_allocator.allocate_memory(2048.0)
        self.replica_manager.register_replica(
            replica_id=f"{self.cluster_name}_node_0",
            model_name="default",
            device_id=dev_id,
            address="localhost:8001",
        )

    def set_network_transport(self, transport: NetworkTransport) -> None:
        """Allows end-user to configure custom networking transport (HTTP, Socket, custom RPC)."""
        self.transport = transport
        logger.info(f"Updated cluster network transport to {transport.__class__.__name__}")

    def add_node(self, replica_id: str, model_name: str, address: str, memory_mb: float = 2048.0) -> ModelReplica:
        """Adds new worker node to inference cluster."""
        dev_id = self.gpu_allocator.allocate_memory(memory_mb)
        return self.replica_manager.register_replica(
            replica_id=replica_id,
            model_name=model_name,
            device_id=dev_id,
            address=address,
        )

    def route_and_dispatch(self, prompt: str, model_name: str = "default") -> Dict[str, Any]:
        """Routes request to healthiest replica and dispatches message via transport."""
        route_res = self.router.route_request(prompt, model_name=model_name)
        if route_res.get("status") == "error":
            return route_res

        addr = route_res["address"]
        response = self.transport.send(addr, {"action": "generate", "prompt": prompt})
        return {
            "route": route_res,
            "transport_response": response,
        }
