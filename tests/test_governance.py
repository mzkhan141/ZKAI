"""Unit tests for Kernel Resource Governance, Quotas, Rate Limiting, and Admission Control."""

import pytest
from zkai.kernel import (
    AIKernel,
    CPUQuota,
    GPUQuota,
    RateLimiter,
    ResourceGovernor,
    ResourceType,
    VRAMQuota,
)


def test_resource_governor_allocation():
    governor = ResourceGovernor()
    reqs = {ResourceType.CPU: 2.0, ResourceType.VRAM: 2048.0}
    
    assert governor.request_allocation("proc_1", reqs)
    assert governor.quotas[ResourceType.CPU].allocated == 2.0
    assert governor.quotas[ResourceType.VRAM].allocated == 2048.0
    
    governor.release_allocation("proc_1", reqs)
    assert governor.quotas[ResourceType.CPU].allocated == 0.0
    assert governor.quotas[ResourceType.VRAM].allocated == 0.0


def test_admission_controller_rejection():
    governor = ResourceGovernor()
    # Request more CPU than limit (8.0 limit by default)
    excessive_reqs = {ResourceType.CPU: 16.0}
    assert not governor.request_allocation("proc_2", excessive_reqs)


def test_rate_limiter():
    limiter = RateLimiter(rate_per_sec=100.0, capacity=10.0)
    # Should allow up to capacity
    for _ in range(10):
        assert limiter.consume(1.0)
    # Next attempt fails since capacity exhausted
    assert not limiter.consume(1.0)


def test_kernel_governor_integration():
    kernel = AIKernel()
    assert hasattr(kernel, "governor")
    assert kernel.governor.request_allocation("task_1", {ResourceType.CPU: 1.0})
