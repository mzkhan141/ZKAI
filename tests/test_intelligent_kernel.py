"""Comprehensive verification unit tests for ZKAI Intelligent Microkernel Operating System."""

import pytest
from zkai import ZKAI
from zkai.kernel import (
    MicroKernel, AIHypervisor, SelfRecoveryManager, EvolutionEngine,
    CognitiveRuntime, SimulationEngine, DigitalTwin, AutonomousTesting,
    GoalScheduler, KernelIntelligence, KernelState,
)
from zkai.security.capability_os import CapabilityManager, Capability
from zkai.ipc.knowledge_bus import KnowledgeBus, SemanticEvent
from zkai.knowledge.research import ResearchEngine
from zkai.security.governance_engine import GovernanceEngine
from zkai.knowledge.world_model import WorldModel


def test_zkai_intelligent_kernel_initialization():
    ai = ZKAI()
    assert ai.kernel.state == KernelState.READY

    # Verify all 15 intelligent subsystems are wired to AIKernel
    k = ai.kernel
    assert k.microkernel is not None
    assert k.capability_manager is not None
    assert k.hypervisor is not None
    assert k.self_healing is not None
    assert k.evolution is not None
    assert k.cognitive is not None
    assert k.simulation is not None
    assert k.digital_twin is not None
    assert k.autonomous_testing is not None
    assert k.goal_scheduler is not None
    assert k.intelligence is not None


def test_microkernel_primitives():
    mk = MicroKernel()
    mk.boot()
    assert mk.lifecycle.state == KernelState.READY

    # Load service
    from zkai.services import StorageService
    loader = mk.loader
    srv = loader.load_service("storage", StorageService)
    assert srv is not None
    assert "storage" in mk.registry.list_services()

    mk.shutdown()
    assert mk.lifecycle.state == KernelState.OFFLINE


def test_capability_os():
    cap_mgr = CapabilityManager()
    token = cap_mgr.grant_capability("test_agent", "Inference")
    assert token.is_valid()
    assert cap_mgr.verify_capability(token, "Inference", "execute") is True
    assert cap_mgr.verify_capability(token, "USB", "execute") is False


def test_ai_hypervisor():
    hyp = AIHypervisor()
    v_ai = hyp.create_virtual_ai("isolated_test_env")
    assert v_ai.v_kernel.state == "RUNNING"
    assert hyp.terminate_virtual_ai(v_ai.instance_id) is True


def test_self_healing_os():
    healer = SelfRecoveryManager()
    repaired = healer.handle_failure("database", "Corrupted DB index")
    assert repaired is True


def test_evolution_engine():
    evo = EvolutionEngine()
    res = evo.evolve()
    assert res["optimizations"]["memory"] is True
    assert res["optimizations"]["scheduler"] is True


def test_knowledge_bus():
    kbus = KnowledgeBus()
    evt = SemanticEvent(intent="test_intent", payload={"key": "val"})
    kbus.publish_semantic(evt)


def test_cognitive_runtime():
    cog = CognitiveRuntime()
    result = cog.process_objective("Solve complex optimization task")
    assert result["approved"] is True
    assert len(result["plan"]) > 0


def test_simulation_environment():
    sim = SimulationEngine()
    report = sim.run_dry_run("run_python_script", {"code": "print('hello')"})
    assert report.predicted_success is True
    assert report.recommendation == "PROCEED"


def test_autonomous_research():
    res_engine = ResearchEngine()
    report = res_engine.conduct_research("Quantum Neural Architecture Search")
    assert "Research Report" in report


def test_governance_engine():
    gov = GovernanceEngine()
    decision = gov.evaluate_action("test_user", "execute_query", {"query": "SELECT *"})
    assert decision["allowed"] is True

    decision_blocked = gov.evaluate_action("test_user", "unauthorized_system_format")
    assert decision_blocked["allowed"] is False


def test_digital_twin():
    dt = DigitalTwin()
    ai = ZKAI()
    status = dt.sync(ai.kernel)
    assert status["health_prediction"] == "STABLE"


def test_autonomous_testing():
    at = AutonomousTesting()
    ai = ZKAI()
    res = at.run_resilience_sweep(ai.kernel)
    assert res["status"] == "RESILIENT"


def test_semantic_scheduler():
    sched = GoalScheduler()
    goal = sched.schedule_goal("critical research task", urgency=2.0)
    assert goal.priority_score > 1.0
    assert goal.allocated_agent_id == "ResearchAgent"


def test_world_model():
    wm = WorldModel()
    wm.update_world("device_gpu_0", "Hardware", {"vram_mb": 8192})
    ctx = wm.query_context()
    assert isinstance(ctx, str)


def test_kernel_intelligence_layer():
    ki = KernelIntelligence()
    ai = ZKAI()
    res = ki.process_kernel_intelligence_cycle(ai.kernel)
    assert res["intelligence_score"] >= 0.99
