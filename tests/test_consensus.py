"""Unit tests for Distributed Control Plane, Leader Election, and Consensus."""

import pytest
from zkai.cluster import (
    ClusterNode,
    ClusterOrchestrator,
    ConsensusManager,
    DistributedLockManager,
    LeaderElection,
    NodeRegistry,
)


def test_leader_election():
    registry = NodeRegistry()
    node1 = ClusterNode(node_id="node_100", status="active")
    node2 = ClusterNode(node_id="node_200", status="active")
    registry.register(node1)
    registry.register(node2)

    election = LeaderElection(registry)
    leader = election.elect_leader()
    assert leader == "node_200"


def test_consensus_manager():
    registry = NodeRegistry()
    node1 = ClusterNode(node_id="node_1", status="active")
    registry.register(node1)
    
    election = LeaderElection(registry)
    consensus = ConsensusManager(election)
    assert consensus.agree("proposal_1", {"action": "scale_out"})


def test_distributed_lock_manager():
    locks = DistributedLockManager()
    assert locks.acquire("resource_vram", "node_1")
    # node_2 cannot acquire same lock
    assert not locks.acquire("resource_vram", "node_2")
    
    assert locks.release("resource_vram", "node_1")
    assert locks.acquire("resource_vram", "node_2")


def test_cluster_orchestrator_integration():
    orchestrator = ClusterOrchestrator()
    assert orchestrator.leader_election.current_leader_id is not None
    res = orchestrator.dispatch_workload("inference_task", {})
    assert res["status"] == "success"
