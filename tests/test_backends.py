"""Unit tests for Compute Backends subsystem."""

import pytest
from zkai.backends import AutoBackendSelector, CPUBackend, CUDABackend, MetalBackend, ROCmBackend


def test_cpu_backend():
    backend = CPUBackend()
    assert backend.is_available() is True
    assert backend.name() == "CPUBackend"


def test_auto_backend_selector():
    backend = AutoBackendSelector.select_backend()
    assert backend is not None
    assert hasattr(backend, "name")
