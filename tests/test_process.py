"""Tests for AI Process Management and Supervision."""

import pytest
from zkai.process.process import AIProcess, AgentProcess, ServiceProcess, WorkflowProcess
from zkai.process.manager import ProcessManager, CrashRecovery, Watchdog
from zkai.kernel.types import ProcessState


def test_process_lifecycle():
    proc = AIProcess(name="test_proc")
    assert proc.state == ProcessState.CREATED
    proc.start()
    assert proc.state == ProcessState.RUNNING
    proc.pause()
    assert proc.state == ProcessState.PAUSED
    proc.resume()
    assert proc.state == ProcessState.RUNNING
    proc.stop()
    assert proc.state == ProcessState.STOPPED


def test_process_manager_spawn_and_terminate():
    mgr = ProcessManager()
    proc = AgentProcess(name="agent_proc", agent_instance=None)
    pid = mgr.spawn(proc)
    assert pid == proc.process_id
    assert proc.state == ProcessState.RUNNING
    assert len(mgr.list_processes()) == 1

    mgr.terminate(pid)
    assert len(mgr.list_processes()) == 0


def test_crash_recovery():
    proc = AIProcess(name="flaky_proc")
    proc.max_restarts = 2
    proc.state = ProcessState.FAILED

    recovered1 = CrashRecovery.recover(proc)
    assert recovered1 is True
    assert proc.crash_count == 1
    assert proc.state == ProcessState.RUNNING

    proc.state = ProcessState.FAILED
    recovered2 = CrashRecovery.recover(proc)
    assert recovered2 is True
    assert proc.crash_count == 2

    proc.state = ProcessState.FAILED
    recovered3 = CrashRecovery.recover(proc)
    assert recovered3 is False
    assert proc.state == ProcessState.FAILED
