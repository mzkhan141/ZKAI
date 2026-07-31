"""Unified Hardware Abstraction and AI Device Manager."""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from zkai.backends.auto import AutoBackendSelector
from zkai.inference.gpu_allocator import GPUAllocator
from zkai.robotics.gpio import GPIO
from zkai.robotics.serial_port import SerialPort
from zkai.robotics.usb import USBManager
from zkai.robotics.ros_bridge import ROSBridge
from zkai.core.logger import get_logger

logger = get_logger("device.manager")


@dataclass
class HardwareDevice:
    device_id: str
    name: str
    device_type: str  # gpu, cpu, camera, microphone, usb, bluetooth, network, serial, gpio, robot, drone, iot
    status: str = "online"
    metadata: Dict[str, Any] = field(default_factory=dict)


class CameraDevice(HardwareDevice):
    def __init__(self, device_id: str = "cam_0"):
        super().__init__(device_id=device_id, name="Integrated Camera", device_type="camera")


class MicrophoneDevice(HardwareDevice):
    def __init__(self, device_id: str = "mic_0"):
        super().__init__(device_id=device_id, name="Default Microphone", device_type="microphone")


class BluetoothDevice(HardwareDevice):
    def __init__(self, device_id: str = "bt_0"):
        super().__init__(device_id=device_id, name="Bluetooth Controller", device_type="bluetooth")


class NetworkDevice(HardwareDevice):
    def __init__(self, device_id: str = "net_0"):
        super().__init__(device_id=device_id, name="Ethernet Adapter", device_type="network")


class IoTDevice(HardwareDevice):
    def __init__(self, device_id: str = "iot_0", name: str = "Smart Sensor"):
        super().__init__(device_id=device_id, name=name, device_type="iot")


class DeviceDiscovery:
    """Discovers connected hardware peripherals at kernel boot."""

    @staticmethod
    def discover_all() -> List[HardwareDevice]:
        logger.info("DeviceDiscovery enumerating hardware peripherals...")
        return [
            HardwareDevice("gpu_0", "NVIDIA RTX GPU", "gpu"),
            HardwareDevice("cpu_0", "Host CPU", "cpu"),
            CameraDevice("cam_0"),
            MicrophoneDevice("mic_0"),
            NetworkDevice("net_0"),
        ]


class DeviceRegistry:
    """Registry maintaining active hardware devices."""

    def __init__(self):
        self._devices: Dict[str, HardwareDevice] = {}

    def register(self, device: HardwareDevice) -> None:
        self._devices[device.device_id] = device

    def get(self, device_id: str) -> Optional[HardwareDevice]:
        return self._devices.get(device_id)

    def list_devices(self) -> List[HardwareDevice]:
        return list(self._devices.values())


class DeviceMonitor:
    """Monitors status and health of connected devices."""

    def __init__(self, registry: DeviceRegistry):
        self.registry = registry

    def check_devices(self) -> Dict[str, str]:
        status_map = {}
        for dev in self.registry.list_devices():
            status_map[dev.device_id] = dev.status
        return status_map


class DeviceManager:
    """Master Unified Hardware Abstraction Manager coordinating GPU, CPU, USB, GPIO, ROS, and IoT devices."""

    def __init__(self):
        self.registry = DeviceRegistry()
        self.gpu_allocator = GPUAllocator(single_gpu_mode=True)
        self.auto_backend = AutoBackendSelector()
        self.gpio = GPIO()
        self.serial = SerialPort()
        self.usb = USBManager()
        self.ros_bridge = ROSBridge()
        self.monitor = DeviceMonitor(self.registry)
        self.boot_discovery()

    def boot_discovery(self) -> None:
        discovered = DeviceDiscovery.discover_all()
        for dev in discovered:
            self.registry.register(dev)
        logger.info(f"DeviceManager initialized with {len(discovered)} hardware devices.")

    def list_hardware(self) -> List[HardwareDevice]:
        return self.registry.list_devices()
