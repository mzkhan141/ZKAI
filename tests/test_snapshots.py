"""Unit tests for System Snapshots, Checkpoints, RollbackManager, and RecoveryJournal."""

import tempfile
import pytest
from zkai.kernel import (
    AIKernel,
    KernelCheckpoint,
    RecoveryJournal,
    RollbackManager,
    SystemSnapshot,
)


def test_system_snapshot_serialization():
    snap = SystemSnapshot()
    snap.kernel_checkpoint.active_services = ["service_a", "service_b"]
    d = snap.to_dict()
    
    restored = SystemSnapshot.from_dict(d)
    assert restored.snapshot_id == snap.snapshot_id
    assert restored.kernel_checkpoint.active_services == ["service_a", "service_b"]


def test_rollback_manager_create_and_rollback(tmp_path):
    kernel = AIKernel()
    manager = RollbackManager(kernel, storage_dir=str(tmp_path))
    
    snap1 = manager.create_snapshot()
    assert snap1 is not None
    assert len(manager.history.list_history()) == 1
    
    assert manager.rollback_to_latest()


def test_recovery_journal(tmp_path):
    j_file = str(tmp_path / "journal.jsonl")
    journal = RecoveryJournal(j_file)
    
    journal.append_entry("BOOT", {"status": "ok"})
    journal.append_entry("CHECKPOINT", {"id": "123"})
    
    entries = journal.read_journal()
    assert len(entries) == 2
    assert entries[0]["operation"] == "BOOT"
    assert entries[1]["data"]["id"] == "123"
