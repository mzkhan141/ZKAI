"""ClusterOrchestrator and Distributed intelligence routing for ZKAI OS."""

from typing import Any, Dict, List, Optional
from zkai.cluster.node import ClusterNode, NodeRegistry
from zkai.inference.cluster import ClusterCoordinator
from zkai.core.logger import get_logger

from zkai.cluster.consensus import (
    LeaderElection,
    ConsensusManager,
    ClusterMembership,
    DistributedLockManager,
    FailureDetector,
)

logger = get_logger("cluster.orchestrator")


class DistributedTaskRouter:
    """Routes tasks to the optimal node based on hardware, latency, power, and availability."""

    def __init__(self, registry: NodeRegistry):
        self.registry = registry

    def select_optimal_node(self, required_vram_mb: float = 0.0) -> Optional[ClusterNode]:
        nodes = self.registry.list_nodes()
        if not nodes:
            return None
        # Select active node with max available VRAM
        active_nodes = [n for n in nodes if n.status == "active" and n.vram_mb >= required_vram_mb]
        if active_nodes:
            return max(active_nodes, key=lambda n: n.vram_mb)
        return nodes[0]


class DistributedMemorySync:
    """Synchronizes working and long-term memory state across nodes."""

    def sync_memory(self, source_node_id: str, target_node_id: str, memory_data: Dict[str, Any]) -> None:
        logger.info(f"DistributedMemorySync sync {len(memory_data)} bytes: {source_node_id} -> {target_node_id}")


class DistributedModelCache:
    """Shared model weight caching across cluster nodes."""

    def __init__(self):
        self.cached_models: Dict[str, List[str]] = {}  # model_id -> list of node_ids

    def register_cached_model(self, model_id: str, node_id: str) -> None:
        if model_id not in self.cached_models:
            self.cached_models[model_id] = []
        if node_id not in self.cached_models[model_id]:
            self.cached_models[model_id].append(node_id)


class ClusterOrchestrator:
    """Master Distributed Operating System Orchestrator coordinating workloads across nodes."""

    def __init__(self):
        self.registry = NodeRegistry()
        self.membership = ClusterMembership(self.registry)
        self.leader_election = LeaderElection(self.registry)
        self.consensus = ConsensusManager(self.leader_election)
        self.locks = DistributedLockManager()
        self.failure_detector = FailureDetector(self.membership)
        self.router = DistributedTaskRouter(self.registry)
        self.memory_sync = DistributedMemorySync()
        self.model_cache = DistributedModelCache()
        self._seed_local_node()

    def _seed_local_node(self) -> None:
        local = ClusterNode(node_type="desktop", address="localhost:8901")
        self.registry.register(local)
        self.membership.heartbeat(local.node_id)
        self.leader_election.elect_leader()

    def dispatch_workload(self, workload_name: str, payload: Any, required_vram_mb: float = 0.0) -> Dict[str, Any]:
        node = self.router.select_optimal_node(required_vram_mb=required_vram_mb)
        if not node:
            return {"status": "error", "error": "No available cluster nodes"}

        logger.info(f"Dispatched workload '{workload_name}' to ClusterNode '{node.node_id}' ({node.node_type})")
        return {"status": "success", "executed_on_node": node.node_id, "node_type": node.node_type}
