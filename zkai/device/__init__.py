"""AI Device Manager Package for ZKAI AI Operating System."""

from zkai.device.manager import (
    BluetoothDevice,
    CameraDevice,
    DeviceDiscovery,
    DeviceManager,
    DeviceMonitor,
    DeviceRegistry,
    HardwareDevice,
    IoTDevice,
    MicrophoneDevice,
    NetworkDevice,
)

__all__ = [
    "HardwareDevice",
    "CameraDevice",
    "MicrophoneDevice",
    "BluetoothDevice",
    "NetworkDevice",
    "IoTDevice",
    "DeviceDiscovery",
    "DeviceRegistry",
    "DeviceMonitor",
    "DeviceManager",
]
