"""Tests for AI Package Manager."""

import pytest
from zkai.packages.manager import PackageManager, PackageRecord, PackageVerifier


def test_package_manager_operations():
    pm = PackageManager()
    installed = pm.install(name="agent-pack-1", version="1.0.0", package_type="agent")
    assert installed is True
    assert len(pm.index.list_all()) == 1

    updated = pm.update("agent-pack-1")
    assert updated is True
    assert pm.index.get("agent-pack-1").version == "1.0.1"

    searched = pm.search("agent")
    assert len(searched) == 1

    removed = pm.remove("agent-pack-1")
    assert removed is True
    assert len(pm.index.list_all()) == 0
