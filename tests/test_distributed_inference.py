"""Tests for Distributed Inference Cluster and single/multi GPU allocation."""

import pytest
from zkai.inference.cluster import InferenceCluster, ClusterCoordinator
from zkai.inference.gpu_allocator import GPUAllocator
from zkai.inference.load_balancer import LoadBalancer, RequestRouter
from zkai.inference.replica import ReplicaManager
from zkai.inference.transport import SimulatedTransport, HTTPTransport


def test_gpu_allocator_single_gpu_mode():
    allocator = GPUAllocator(single_gpu_mode=True)
    dev_id = allocator.allocate_memory(1024.0)
    assert dev_id in allocator.devices


def test_inference_cluster_routing():
    cluster = InferenceCluster(cluster_name="test_cluster", single_gpu_mode=True)
    node = cluster.add_node("node_1", "default", "localhost:8002")
    assert node.replica_id == "node_1"

    dispatch_res = cluster.route_and_dispatch("Hello cluster")
    assert "route" in dispatch_res
    assert dispatch_res["route"]["status"] == "success"


def test_cluster_coordinator_failover():
    rm = ReplicaManager()
    rep = rm.register_replica("rep1", "model1", 0, "localhost:8001")
    coord = ClusterCoordinator(rm)

    coord.trigger_failover("rep1")
    assert rep.status == "failed"

    statuses = coord.perform_health_check()
    assert statuses["rep1"] == "active"
