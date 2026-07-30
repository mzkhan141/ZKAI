"""MemoryPool, ZeroCopyBuffer, and StreamingBuffer for high performance memory recycling."""

from typing import Any, List, Optional
import torch
from zkai.core.logger import get_logger

logger = get_logger("core.memory_pool")


class MemoryPool:
    """Pre-allocated memory tensor pool recycling buffers to avoid CUDA allocation overhead."""

    def __init__(self, buffer_shape: tuple[int, ...], dtype: torch.dtype = torch.float32, pool_size: int = 16):
        self.buffer_shape = buffer_shape
        self.dtype = dtype
        self.free_buffers: List[torch.Tensor] = [torch.zeros(buffer_shape, dtype=dtype) for _ in range(pool_size)]

    def acquire(self) -> torch.Tensor:
        if self.free_buffers:
            return self.free_buffers.pop()
        return torch.zeros(self.buffer_shape, dtype=self.dtype)

    def release(self, buffer: torch.Tensor) -> None:
        buffer.zero_()
        self.free_buffers.append(buffer)


class ZeroCopyBuffer:
    """Zero-copy buffer wrapping numpy arrays or torch memory pointers."""

    def __init__(self, data: Any):
        self._data = data

    def as_torch(self) -> torch.Tensor:
        if isinstance(self._data, torch.Tensor):
            return self._data
        return torch.from_numpy(self._data)


class StreamingBuffer:
    """Circular ring buffer for continuous stream token chunking."""

    def __init__(self, capacity: int = 4096):
        self.capacity = capacity
        self._buffer: List[Any] = []

    def append(self, item: Any) -> None:
        if len(self._buffer) >= self.capacity:
            self._buffer.pop(0)
        self._buffer.append(item)

    def read_all(self) -> List[Any]:
        items = list(self._buffer)
        self._buffer.clear()
        return items
