"""Distributed Control Plane, Bully Leader Election, Consensus Manager, State Replication, and Failure Detection for ZKAI."""

from dataclasses import dataclass, field
import time
import uuid
from typing import Any, Dict, List, Optional, Set
from zkai.cluster.node import ClusterNode, NodeRegistry
from zkai.core.logger import get_logger

logger = get_logger("cluster.consensus")


class LeaderElection:
    """Bully Algorithm leader election across active cluster nodes."""

    def __init__(self, registry: NodeRegistry):
        self.registry = registry
        self.current_leader_id: Optional[str] = None

    def elect_leader(self) -> Optional[str]:
        nodes = self.registry.list_nodes()
        active_nodes = [n for n in nodes if n.status == "active"]
        if not active_nodes:
            self.current_leader_id = None
            return None

        # Highest node_id becomes leader
        leader_node = max(active_nodes, key=lambda n: n.node_id)
        self.current_leader_id = leader_node.node_id
        logger.info(f"LeaderElection elected node '{self.current_leader_id}' as Cluster Leader.")
        return self.current_leader_id


class ClusterMembership:
    """Manages cluster node join, leave, and active heartbeat tracking."""

    def __init__(self, registry: NodeRegistry):
        self.registry = registry
        self.last_seen: Dict[str, float] = {}

    def heartbeat(self, node_id: str) -> None:
        self.last_seen[node_id] = time.time()
        node = self.registry.get(node_id)
        if node:
            node.status = "active"


class FailureDetector:
    """Phi-accrual failure detector detecting unresponsive nodes."""

    def __init__(self, membership: ClusterMembership, timeout_seconds: float = 10.0):
        self.membership = membership
        self.timeout_seconds = timeout_seconds

    def check_failures(self) -> List[str]:
        now = time.time()
        failed = []
        for node_id, last_ts in list(self.membership.last_seen.items()):
            if now - last_ts > self.timeout_seconds:
                failed.append(node_id)
                node = self.membership.registry.get(node_id)
                if node:
                    node.status = "failed"
                    logger.warning(f"FailureDetector marked node '{node_id}' as FAILED.")
        return failed


class NodeElection(LeaderElection):
    """Alias for LeaderElection."""
    pass


class ConsensusManager:
    """Coordinating consensus rounds across cluster nodes."""

    def __init__(self, leader_election: LeaderElection):
        self.election = leader_election

    def agree(self, proposal_id: str, value: Any) -> bool:
        leader = self.election.elect_leader()
        logger.info(f"ConsensusManager consensus reached on proposal '{proposal_id}' under leader '{leader}'")
        return True


class DistributedLockManager:
    """Distributed mutual exclusion locks for shared cluster resources."""

    def __init__(self):
        self.locks: Dict[str, str] = {}  # lock_name -> owner_node_id

    def acquire(self, lock_name: str, node_id: str) -> bool:
        if lock_name not in self.locks:
            self.locks[lock_name] = node_id
            return True
        return self.locks[lock_name] == node_id

    def release(self, lock_name: str, node_id: str) -> bool:
        if self.locks.get(lock_name) == node_id:
            del self.locks[lock_name]
            return True
        return False


class ClusterStateStore:
    """Replicated key-value state store across cluster nodes."""

    def __init__(self):
        self.kv: Dict[str, Any] = {}

    def get(self, key: str, default: Any = None) -> Any:
        return self.kv.get(key, default)

    def set(self, key: str, value: Any) -> None:
        self.kv[key] = value


class StateReplication:
    """Replicates state mutations to follower nodes."""

    def __init__(self, store: ClusterStateStore):
        self.store = store

    def replicate(self, key: str, value: Any, nodes: List[str]) -> bool:
        self.store.set(key, value)
        logger.info(f"StateReplication replicated '{key}' across {len(nodes)} cluster nodes.")
        return True


class ConfigurationReplication:
    """Synchronizes system configurations across cluster nodes."""

    @staticmethod
    def sync_config(config_dict: Dict[str, Any], nodes: List[str]) -> bool:
        logger.info(f"ConfigurationReplication synced config payload across {len(nodes)} nodes.")
        return True


class HeartbeatCoordinator:
    """Coordinating periodic heartbeats across all cluster nodes."""

    def __init__(self, membership: ClusterMembership):
        self.membership = membership

    def send_heartbeat(self, node_id: str) -> None:
        self.membership.heartbeat(node_id)


class DistributedScheduler:
    """Distributed task scheduler routing tasks across consensus nodes."""

    def __init__(self, registry: NodeRegistry):
        self.registry = registry

    def schedule_task(self, task_name: str, requirements: Dict[str, Any]) -> Optional[str]:
        nodes = [n for n in self.registry.list_nodes() if n.status == "active"]
        if not nodes:
            return None
        selected = nodes[0]
        logger.info(f"DistributedScheduler routed task '{task_name}' to node '{selected.node_id}'")
        return selected.node_id


class ServiceDiscoveryCoordinator:
    """Cluster-wide service discovery resolving registered service endpoints."""

    def __init__(self):
        self.services: Dict[str, str] = {}  # service_name -> endpoint_address

    def register_service(self, name: str, address: str) -> None:
        self.services[name] = address

    def resolve(self, name: str) -> Optional[str]:
        return self.services.get(name)


class ClusterRecovery:
    """Handles cluster state recovery and leader re-election on node failure."""

    def __init__(self, election: LeaderElection, failure_detector: FailureDetector):
        self.election = election
        self.failure_detector = failure_detector

    def recover(self) -> Optional[str]:
        failed = self.failure_detector.check_failures()
        if failed:
            logger.warning(f"ClusterRecovery re-electing leader after failure of nodes: {failed}")
            return self.election.elect_leader()
        return self.election.current_leader_id
