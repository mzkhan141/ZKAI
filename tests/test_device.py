"""Tests for Device Manager and Hardware Abstractions."""

import pytest
from zkai.device.manager import DeviceManager, CameraDevice, HardwareDevice


def test_device_manager_discovery():
    dm = DeviceManager()
    devices = dm.list_hardware()
    assert len(devices) >= 5
    types = [d.device_type for d in devices]
    assert "gpu" in types
    assert "cpu" in types
    assert "camera" in types
