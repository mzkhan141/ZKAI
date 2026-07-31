"""Tests for AI Service Manager and OS Core Services."""

import pytest
from zkai.services.service import Service, InferenceService, MemoryService, StorageService
from zkai.services.manager import ServiceManager, HealthMonitor, ServiceSupervisor
from zkai.kernel.types import ServiceState


def test_service_lifecycle():
    srv = Service("custom_service")
    assert srv.state == ServiceState.REGISTERED
    assert srv.is_healthy() is False
    srv.start()
    assert srv.state == ServiceState.HEALTHY
    assert srv.is_healthy() is True
    srv.stop()
    assert srv.state == ServiceState.STOPPED


def test_service_manager_registration_and_health():
    mgr = ServiceManager()
    inf_srv = InferenceService()
    mem_srv = MemoryService()

    mgr.register_and_start(inf_srv)
    mgr.register_and_start(mem_srv)

    assert len(mgr.list_services()) == 2
    health = mgr.health_monitor.check_all()
    assert health["inference_service"] is True
    assert health["memory_service"] is True

    mgr.stop_service("inference_service")
    health_after = mgr.health_monitor.check_all()
    assert health_after["inference_service"] is False

    restarted = mgr.supervisor.restart_failed()
    assert "inference_service" in restarted
