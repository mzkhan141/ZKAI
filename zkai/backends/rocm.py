"""ROCm compute backend for AMD GPUs."""

import torch
from zkai.core.backend import PyTorchBackend


class ROCmBackend(PyTorchBackend):
    """AMD ROCm compute backend (uses PyTorch HIP interface)."""

    def __init__(self):
        is_rocm = torch.cuda.is_available() and getattr(torch.version, "hip", None) is not None
        device_str = "cuda" if is_rocm else "cpu"
        super().__init__(device=device_str)

    def name(self) -> str:
        return "ROCmBackend"

    def is_available(self) -> bool:
        return torch.cuda.is_available() and getattr(torch.version, "hip", None) is not None
