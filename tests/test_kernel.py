"""Tests for AI Kernel and Schedulers."""

import pytest
from zkai.kernel.kernel import AIKernel, KernelRuntime
from zkai.kernel.config import KernelConfig
from zkai.kernel.types import ProcessState, ServiceState, ResourceType, SchedulerPolicy
from zkai.kernel.scheduler import (
    KernelScheduler,
    ResourceScheduler,
    GPUScheduler,
    AgentScheduler,
    ModelScheduler,
    ContextScheduler,
)
from zkai.kernel.lifecycle import LifecycleManager, HeartbeatManager


def test_kernel_singleton_and_boot():
    kernel = AIKernel.get_instance()
    kernel.boot()
    assert kernel.lifecycle.is_running is True
    kernel.shutdown()
    assert kernel.lifecycle.is_running is False


def test_resource_and_gpu_schedulers():
    res_sched = ResourceScheduler(cpu_cores=4, memory_mb=1024)
    assert res_sched.allocate(ResourceType.CPU, 2.0) is True
    assert res_sched.allocate(ResourceType.CPU, 3.0) is False  # Exceeds limit

    gpu_sched = GPUScheduler(total_vram_mb=4096)
    assert gpu_sched.reserve_vram(2048) is True
    gpu_sched.free_vram(2048)
    assert gpu_sched.allocated[ResourceType.VRAM] == 0.0


def test_agent_and_model_schedulers():
    agent_sched = AgentScheduler()
    agent_sched.register_agent("agent_a")
    assert agent_sched.get_highest_priority_agent() == "agent_a"

    model_sched = ModelScheduler(max_loaded_models=2)
    model_sched.load_model("m1")
    model_sched.load_model("m2")
    evicted = model_sched.load_model("m3")
    assert evicted == "m1"
    assert "m3" in model_sched.loaded_models


def test_context_scheduler():
    ctx_sched = ContextScheduler(max_tokens=5)
    tokens = [1, 2, 3, 4, 5, 6, 7, 8]
    fitted = ctx_sched.fit_context(tokens)
    assert fitted == [4, 5, 6, 7, 8]


def test_heartbeat_manager():
    hb = HeartbeatManager()
    hb.register_health_check("subsystem_x", lambda: True)
    res = hb.tick()
    assert res["subsystem_x"] is True
    assert hb.total_ticks == 1
