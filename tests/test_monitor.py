"""Tests for SystemMonitor and Task Manager."""

import pytest
from zkai.monitor.monitor import SystemMonitor, MonitorDashboard


def test_system_monitor_and_dashboard():
    mon = SystemMonitor()
    snap = mon.get_snapshot()
    assert snap.running_agents >= 0
    assert snap.cpu_percent >= 0.0

    report = mon.get_dashboard_report()
    assert "=== ZKAI System Monitor Task Manager ===" in report
    assert "CPU:" in report
