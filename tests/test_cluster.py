"""Tests for Distributed AI Operating System Cluster."""

import pytest
from zkai.cluster.orchestrator import ClusterOrchestrator
from zkai.cluster.node import ClusterNode


def test_cluster_orchestrator_workload_dispatch():
    orch = ClusterOrchestrator()
    node2 = ClusterNode(node_type="server", vram_mb=24576.0, address="192.168.1.100:8901")
    orch.registry.register(node2)

    res = orch.dispatch_workload("train_large_model", payload={}, required_vram_mb=16384.0)
    assert res["status"] == "success"
    assert res["executed_on_node"] == node2.node_id
