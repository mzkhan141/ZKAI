"""Shared Pytest Fixtures for ZKAI test suite."""

import pytest
import os
import tempfile
from pathlib import Path


@pytest.fixture
def temp_dir():
    """Provides a temporary directory for test artifacts."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def sample_config_dict():
    """Returns a dictionary representing standard ZKAI configuration."""
    return {
        "device": "cpu",
        "precision": "float32",
        "memory_limit": "2GB",
        "reasoning": True,
        "vision": False,
        "browser": False,
        "internet": False,
        "computer": False,
        "coding": True,
    }
