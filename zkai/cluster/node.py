"""ClusterNode and NodeRegistry for ZKAI Distributed AI OS."""

from dataclasses import dataclass, field
import uuid
from typing import Any, Dict, List, Optional
from zkai.inference.transport import NetworkTransport, SimulatedTransport
from zkai.core.logger import get_logger

logger = get_logger("cluster.node")


@dataclass
class ClusterNode:
    node_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    node_type: str = "desktop"  # desktop, laptop, phone, server, cloud, edge, iot
    address: str = "localhost:8901"
    status: str = "active"
    vram_mb: float = 8192.0
    cpu_cores: int = 8
    shared_identity: Optional[str] = None
    transport: Optional[NetworkTransport] = None


class NodeRegistry:
    """Registry maintaining active nodes in the distributed AI OS cluster."""

    def __init__(self):
        self._nodes: Dict[str, ClusterNode] = {}

    def register(self, node: ClusterNode) -> None:
        if not node.transport:
            node.transport = SimulatedTransport()
        self._nodes[node.node_id] = node
        logger.info(f"Registered Distributed ClusterNode '{node.node_id}' ({node.node_type} at {node.address})")

    def unregister(self, node_id: str) -> None:
        if node_id in self._nodes:
            del self._nodes[node_id]

    def get(self, node_id: str) -> Optional[ClusterNode]:
        return self._nodes.get(node_id)

    def list_nodes(self) -> List[ClusterNode]:
        return list(self._nodes.values())
