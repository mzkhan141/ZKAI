"""GPUAllocator for managing GPU memory, device mapping, single-GPU and multi-GPU placements."""

from dataclasses import dataclass
from typing import Dict, List, Optional
import torch
from zkai.core.logger import get_logger

logger = get_logger("inference.gpu_allocator")


@dataclass
class GPUDevice:
    device_id: int
    device_name: str
    total_memory_mb: float
    used_memory_mb: float = 0.0

    @property
    def free_memory_mb(self) -> float:
        return max(0.0, self.total_memory_mb - self.used_memory_mb)


class GPUAllocator:
    """GPU memory and device allocation manager supporting Single-GPU, Multi-GPU, and CPU modes."""

    def __init__(self, single_gpu_mode: bool = False):
        self.single_gpu_mode = single_gpu_mode
        self.devices: Dict[int, GPUDevice] = {}
        self._discover_devices()

    def _discover_devices(self) -> None:
        if torch.cuda.is_available():
            count = 1 if self.single_gpu_mode else torch.cuda.device_count()
            for i in range(count):
                props = torch.cuda.get_device_properties(i)
                total_mb = props.total_memory / (1024 * 1024)
                self.devices[i] = GPUDevice(device_id=i, device_name=props.name, total_memory_mb=total_mb)
        else:
            # Fallback CPU device representation
            self.devices[0] = GPUDevice(device_id=0, device_name="CPU", total_memory_mb=16384.0)

    def allocate_memory(self, memory_mb: float, preferred_device: Optional[int] = None) -> int:
        """Allocates requested memory in MB on optimal device ID and returns device ID."""
        if preferred_device is not None and preferred_device in self.devices:
            dev = self.devices[preferred_device]
            if dev.free_memory_mb >= memory_mb:
                dev.used_memory_mb += memory_mb
                return preferred_device

        # Select device with most free memory
        best_device_id = max(self.devices.keys(), key=lambda d: self.devices[d].free_memory_mb)
        self.devices[best_device_id].used_memory_mb += memory_mb
        return best_device_id

    def free_memory(self, device_id: int, memory_mb: float) -> None:
        """Releases allocated memory on specified device."""
        if device_id in self.devices:
            self.devices[device_id].used_memory_mb = max(0.0, self.devices[device_id].used_memory_mb - memory_mb)
