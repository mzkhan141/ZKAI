"""ComputeBackend abstraction layer enabling pluggable tensor compute engines."""

from typing import Any, List, Optional, Protocol, Tuple, Union, runtime_checkable
import torch
from zkai.core.types import DeviceType, DType, BackendType
from zkai.core.exceptions import BackendError
from zkai.core.logger import get_logger

logger = get_logger("backend")


@runtime_checkable
class ComputeBackend(Protocol):
    """Protocol defining mandatory tensor operations across all compute backends."""

    def name(self) -> str: ...

    def is_available(self) -> bool: ...

    def get_device(self) -> str: ...

    def set_device(self, device: str) -> None: ...

    def tensor(self, data: Any, dtype: Optional[DType] = None, device: Optional[str] = None) -> Any: ...

    def zeros(self, shape: Tuple[int, ...], dtype: Optional[DType] = None) -> Any: ...

    def ones(self, shape: Tuple[int, ...], dtype: Optional[DType] = None) -> Any: ...

    def randn(self, shape: Tuple[int, ...], dtype: Optional[DType] = None) -> Any: ...

    def matmul(self, a: Any, b: Any) -> Any: ...

    def add(self, a: Any, b: Any) -> Any: ...

    def sub(self, a: Any, b: Any) -> Any: ...

    def mul(self, a: Any, b: Any) -> Any: ...

    def div(self, a: Any, b: Any) -> Any: ...

    def relu(self, a: Any) -> Any: ...

    def gelu(self, a: Any) -> Any: ...

    def silu(self, a: Any) -> Any: ...

    def sigmoid(self, a: Any) -> Any: ...

    def softmax(self, a: Any, dim: int = -1) -> Any: ...


class DeviceManager:
    """Manages system execution devices (CUDA GPU, MPS, CPU) and memory allocation."""

    @staticmethod
    def get_optimal_device() -> str:
        """Determines best available accelerator device."""
        if torch.cuda.is_available():
            return f"cuda:{torch.cuda.current_device()}"
        elif hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
            return "mps"
        return "cpu"

    @staticmethod
    def get_vram_info() -> Tuple[int, int]:
        """Returns (free_vram_bytes, total_vram_bytes) if CUDA is available."""
        if torch.cuda.is_available():
            free_mem, total_mem = torch.cuda.mem_get_info()
            return free_mem, total_mem
        return 0, 0

    @staticmethod
    def empty_cache() -> None:
        """Frees unused cached memory on GPU accelerators."""
        if torch.cuda.is_available():
            torch.cuda.empty_cache()


class PyTorchBackend:
    """Default PyTorch computation backend implementation for ZKAI."""

    DTYPE_MAP = {
        DType.FLOAT32: torch.float32,
        DType.FLOAT16: torch.float16,
        DType.BFLOAT16: torch.bfloat16,
        DType.INT8: torch.int8,
        DType.INT4: torch.int8,  # Quantized storage mapping
        DType.INT32: torch.int32,
        DType.INT64: torch.int64,
        DType.BOOL: torch.bool,
    }

    def __init__(self, device: Optional[str] = None):
        self._device_str = device or DeviceManager.get_optimal_device()
        self._device = torch.device(self._device_str)

    def name(self) -> str:
        return "PyTorchBackend"

    def is_available(self) -> bool:
        return True

    def get_device(self) -> str:
        return str(self._device)

    def set_device(self, device: str) -> None:
        self._device_str = device
        self._device = torch.device(device)

    def _get_torch_dtype(self, dtype: Optional[DType]) -> Optional[torch.dtype]:
        if dtype is None:
            return None
        return self.DTYPE_MAP.get(dtype, torch.float32)

    def tensor(self, data: Any, dtype: Optional[DType] = None, device: Optional[str] = None) -> torch.Tensor:
        dev = torch.device(device) if device else self._device
        torch_dtype = self._get_torch_dtype(dtype)
        if isinstance(data, torch.Tensor):
            return data.to(device=dev, dtype=torch_dtype)
        return torch.tensor(data, dtype=torch_dtype, device=dev)

    def zeros(self, shape: Tuple[int, ...], dtype: Optional[DType] = None) -> torch.Tensor:
        return torch.zeros(shape, dtype=self._get_torch_dtype(dtype), device=self._device)

    def ones(self, shape: Tuple[int, ...], dtype: Optional[DType] = None) -> torch.Tensor:
        return torch.ones(shape, dtype=self._get_torch_dtype(dtype), device=self._device)

    def randn(self, shape: Tuple[int, ...], dtype: Optional[DType] = None) -> torch.Tensor:
        return torch.randn(shape, dtype=self._get_torch_dtype(dtype), device=self._device)

    def matmul(self, a: torch.Tensor, b: torch.Tensor) -> torch.Tensor:
        return torch.matmul(a, b)

    def add(self, a: torch.Tensor, b: torch.Tensor) -> torch.Tensor:
        return torch.add(a, b)

    def sub(self, a: torch.Tensor, b: torch.Tensor) -> torch.Tensor:
        return torch.sub(a, b)

    def mul(self, a: torch.Tensor, b: torch.Tensor) -> torch.Tensor:
        return torch.mul(a, b)

    def div(self, a: torch.Tensor, b: torch.Tensor) -> torch.Tensor:
        return torch.div(a, b)

    def relu(self, a: torch.Tensor) -> torch.Tensor:
        return torch.relu(a)

    def gelu(self, a: torch.Tensor) -> torch.Tensor:
        return torch.nn.functional.gelu(a)

    def silu(self, a: torch.Tensor) -> torch.Tensor:
        return torch.nn.functional.silu(a)

    def sigmoid(self, a: torch.Tensor) -> torch.Tensor:
        return torch.sigmoid(a)

    def softmax(self, a: torch.Tensor, dim: int = -1) -> torch.Tensor:
        return torch.softmax(a, dim=dim)


class BackendManager:
    """Singleton Registry managing current active ComputeBackend instance."""

    _instance: Optional[ComputeBackend] = None

    @classmethod
    def get_backend(cls) -> ComputeBackend:
        if cls._instance is None:
            cls._instance = PyTorchBackend()
            logger.info(f"Initialized default backend: {cls._instance.name()} on device {cls._instance.get_device()}")
        return cls._instance

    @classmethod
    def set_backend(cls, backend: ComputeBackend) -> None:
        if not isinstance(backend, ComputeBackend):
            raise BackendError("Provided object does not satisfy ComputeBackend protocol")
        cls._instance = backend
        logger.info(f"Switched backend to: {backend.name()}")
