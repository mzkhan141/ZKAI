"""CUDA compute backend implementation."""

from typing import Optional
import torch
from zkai.core.backend import PyTorchBackend


class CUDABackend(PyTorchBackend):
    """NVIDIA CUDA compute backend with memory management and streams."""

    def __init__(self, device_id: int = 0):
        device_str = f"cuda:{device_id}" if torch.cuda.is_available() else "cpu"
        super().__init__(device=device_str)

    def name(self) -> str:
        return "CUDABackend"

    def is_available(self) -> bool:
        return torch.cuda.is_available()

    def synchronize(self) -> None:
        if torch.cuda.is_available():
            torch.cuda.synchronize()
