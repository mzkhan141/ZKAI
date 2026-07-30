"""Unit tests for Model Hub subsystem."""

import pytest
from zkai.hub import CheckpointRecord, CheckpointRegistry, HubVersionManager, ModelHub


def test_checkpoint_registry():
    reg = CheckpointRegistry()
    rec = CheckpointRecord(version="1.0.0", file_path="model.zk", metrics={"loss": 0.1})
    reg.register("model_a", rec)
    assert len(reg.records["model_a"]) == 1


def test_hub_version_manager():
    res = HubVersionManager.compare_versions("1.0.0", "0.9.0")
    assert res > 0
