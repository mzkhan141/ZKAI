"""Tests for Memory Operating System Daemon."""

import pytest
from zkai.memory_os.daemon import MemoryDaemon, MemorySnapshot, TemporalMemory
from zkai.memory.manager import MemoryManager


def test_memory_daemon_and_gc():
    mm = MemoryManager()
    mm.remember("k1", "low importance content", importance=0.05)
    mm.remember("k2", "high importance content", importance=0.9)

    daemon = MemoryDaemon(mm)
    res = daemon.tick_maintenance()
    assert res["status"] == "success"
    assert res["purged"] == 1


def test_memory_snapshot_and_temporal_decay(tmp_path):
    mm = MemoryManager()
    snap_path = str(tmp_path / "mem_snap.json")
    MemorySnapshot.create_snapshot(mm, snap_path)

    entry = mm.remember("test_key", "val")
    import time
    decay = TemporalMemory.compute_decay(entry, time.time())
    assert decay > 0.0
