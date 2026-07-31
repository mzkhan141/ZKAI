"""LoadBalancer and RequestRouter for distributed request routing and load balancing."""

from typing import Any, Dict, List, Optional
from zkai.inference.replica import ModelReplica, ReplicaManager
from zkai.core.logger import get_logger

logger = get_logger("inference.load_balancer")


class LoadBalancer:
    """Load balancer selecting optimal replica using round-robin or least-connections policy."""

    def __init__(self, replica_manager: ReplicaManager, policy: str = "least_connections"):
        self.replica_manager = replica_manager
        self.policy = policy
        self._rr_index = 0

    def select_replica(self, model_name: Optional[str] = None) -> Optional[ModelReplica]:
        healthy = self.replica_manager.get_healthy_replicas(model_name)
        if not healthy:
            return None

        if self.policy == "round_robin":
            selected = healthy[self._rr_index % len(healthy)]
            self._rr_index += 1
            return selected
        else:
            # Least connections policy
            return min(healthy, key=lambda r: r.active_requests)


class RequestRouter:
    """Routes incoming inference requests to appropriate cluster replicas."""

    def __init__(self, load_balancer: LoadBalancer):
        self.load_balancer = load_balancer

    def route_request(self, prompt: str, model_name: str = "default") -> Dict[str, Any]:
        replica = self.load_balancer.select_replica(model_name)
        if not replica:
            return {"status": "error", "error": "No available healthy replicas"}

        replica.active_requests += 1
        try:
            return {
                "status": "success",
                "replica_id": replica.replica_id,
                "address": replica.address,
                "prompt": prompt,
            }
        finally:
            replica.active_requests = max(0, replica.active_requests - 1)
