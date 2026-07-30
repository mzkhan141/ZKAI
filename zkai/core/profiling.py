"""Performance Profiling, Memory Profiling, and GPU Resource Trackers."""

from dataclasses import dataclass
import time
from typing import Dict, List, Optional, Any
from zkai.core.backend import DeviceManager
from zkai.core.logger import get_logger

logger = get_logger("profiling")


@dataclass
class ProfileResult:
    """Summary of execution profile statistics."""
    name: str
    duration_seconds: float
    cpu_memory_mb: float
    vram_used_mb: float


class Profiler:
    """Performance Profiler for measuring execution time and resource utilization."""

    def __init__(self, name: str = "default_profiler"):
        self.name = name
        self._start_time: Optional[float] = None
        self._results: List[ProfileResult] = []

    def start(self) -> None:
        self._start_time = time.perf_counter()

    def stop(self, section_name: str = "execution") -> ProfileResult:
        if self._start_time is None:
            duration = 0.0
        else:
            duration = time.perf_counter() - self._start_time
            self._start_time = None

        free_vram, total_vram = DeviceManager.get_vram_info()
        vram_used_mb = (total_vram - free_vram) / (1024 * 1024) if total_vram > 0 else 0.0

        res = ProfileResult(
            name=section_name,
            duration_seconds=duration,
            cpu_memory_mb=0.0,
            vram_used_mb=vram_used_mb,
        )
        self._results.append(res)
        logger.debug(f"Profile [{section_name}]: {duration:.4f}s | VRAM Used: {vram_used_mb:.2f}MB")
        return res

    def get_summary(self) -> List[ProfileResult]:
        return self._results


class GPUProfiler:
    """Dedicated tracker for CUDA memory allocations and device compute events."""

    @staticmethod
    def get_memory_stats() -> Dict[str, float]:
        free_bytes, total_bytes = DeviceManager.get_vram_info()
        used_bytes = total_bytes - free_bytes
        return {
            "free_gb": free_bytes / 1e9,
            "used_gb": used_bytes / 1e9,
            "total_gb": total_bytes / 1e9,
        }
