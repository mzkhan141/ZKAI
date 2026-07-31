"""Unit tests for AI Kernel Boot Management, State Machine, and Shutdown Sequence."""

import pytest
from zkai.kernel import (
    AIKernel,
    BootConfiguration,
    BootLoader,
    BootPhase,
    BootProfiles,
    DependencyResolver,
    EmergencyShutdown,
    GracefulShutdown,
    KernelState,
    KernelStateMachine,
    SafeMode,
    ShutdownMode,
    StateTransitionManager,
    TransitionPolicies,
)


def test_dependency_resolver():
    deps = {
        "storage": set(),
        "database": {"storage"},
        "memory": {"database"},
        "agent": {"memory"},
    }
    order = DependencyResolver.resolve_order(deps)
    assert order.index("storage") < order.index("database")
    assert order.index("database") < order.index("memory")
    assert order.index("memory") < order.index("agent")


def test_kernel_state_machine_transitions():
    fsm = KernelStateMachine()
    assert fsm.current_state == KernelState.OFFLINE
    
    # Valid transitions
    assert fsm.transition_to(KernelState.BOOTING)
    assert fsm.current_state == KernelState.BOOTING
    
    assert fsm.transition_to(KernelState.INITIALIZING)
    assert fsm.current_state == KernelState.INITIALIZING
    
    assert fsm.transition_to(KernelState.READY)
    assert fsm.current_state == KernelState.READY
    
    # Invalid direct transition from READY -> OFFLINE without SHUTTING_DOWN
    assert not fsm.transition_to(KernelState.OFFLINE)
    assert fsm.current_state == KernelState.READY
    
    # Valid transition to SHUTTING_DOWN then OFFLINE
    assert fsm.transition_to(KernelState.SHUTTING_DOWN)
    assert fsm.transition_to(KernelState.OFFLINE)
    assert fsm.current_state == KernelState.OFFLINE


def test_boot_loader_execution():
    kernel = AIKernel()
    assert kernel.state == KernelState.OFFLINE
    
    kernel.boot()
    assert kernel.state == KernelState.READY
    
    kernel.shutdown()
    assert kernel.state == KernelState.OFFLINE


def test_safe_mode_boot():
    cfg = BootConfiguration()
    safe_cfg = SafeMode.configure_config(cfg)
    assert safe_cfg.safe_mode is True
    assert safe_cfg.profile == BootProfiles.SAFE
    assert BootPhase.NETWORK_CLUSTER not in safe_cfg.enabled_phases


def test_emergency_shutdown():
    kernel = AIKernel()
    kernel.boot()
    assert kernel.state == KernelState.READY
    
    kernel.shutdown(mode=ShutdownMode.EMERGENCY)
    assert kernel.state == KernelState.OFFLINE
