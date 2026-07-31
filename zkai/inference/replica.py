"""ReplicaManager for managing model replica lifecycles and health monitoring."""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from zkai.core.logger import get_logger

logger = get_logger("inference.replica")


@dataclass
class ModelReplica:
    replica_id: str
    model_name: str
    device_id: int
    address: str
    status: str = "active"  # active, busy, failed, initializing
    active_requests: int = 0


class ReplicaManager:
    """Manages active model replicas across cluster nodes."""

    def __init__(self):
        self.replicas: Dict[str, ModelReplica] = {}

    def register_replica(self, replica_id: str, model_name: str, device_id: int, address: str) -> ModelReplica:
        replica = ModelReplica(replica_id=replica_id, model_name=model_name, device_id=device_id, address=address)
        self.replicas[replica_id] = replica
        logger.info(f"Registered model replica '{replica_id}' on device {device_id} at {address}")
        return replica

    def unregister_replica(self, replica_id: str) -> None:
        if replica_id in self.replicas:
            del self.replicas[replica_id]

    def get_healthy_replicas(self, model_name: Optional[str] = None) -> List[ModelReplica]:
        healthy = [r for r in self.replicas.values() if r.status in ["active", "busy"]]
        if model_name:
            healthy = [r for r in healthy if r.model_name == model_name]
        return healthy
