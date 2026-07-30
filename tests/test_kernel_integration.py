"""Integration test verifying full Kernel-Centric AI Operating System architecture."""

import pytest
from zkai import ZKAI
from zkai.kernel import KernelState, BootPhase


def test_zkai_kernel_centric_boot():
    ai = ZKAI()
    assert ai.kernel.state == KernelState.READY
    
    # Verify all subsystems are registered as Kernel Services
    services = ai.kernel._services
    assert "security_kernel" in services
    assert "storage" in services
    assert "process_manager" in services
    assert "ipc_bus" in services
    assert "service_manager" in services
    assert "session_manager" in services
    assert "tenant_manager" in services
    assert "semantic_filesystem" in services
    assert "models" in services
    assert "memory_os" in services
    assert "knowledge_governor" in services
    assert "device_manager" in services
    assert "cluster_orchestrator" in services
    assert "voice" in services
    assert "apps" in services
    assert "packages" in services
    assert "marketplace" in services
    assert "shell" in services
    assert "monitor" in services
    
    # Verify governor, rollback manager, tracer
    assert ai.governor is not None
    assert ai.rollback_manager is not None
    assert ai.tracer is not None


def test_zkai_architecture_spec_generator(tmp_path):
    from pathlib import Path
    from zkai.kernel.spec import ArchitectureSpec
    spec = ArchitectureSpec(output_dir=str(tmp_path))
    files = spec.generate_all()
    assert len(files) == 12
    for f in files:
        assert Path(f).exists()
