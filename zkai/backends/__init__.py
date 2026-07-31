"""Compute Backends Subsystem for ZKAI."""

from zkai.backends.auto import AutoBackendSelector
from zkai.backends.cpu import CPUBackend
from zkai.backends.cuda import CUDABackend
from zkai.backends.metal import MetalBackend
from zkai.backends.opencl import OpenCLBackend
from zkai.backends.rocm import ROCmBackend
from zkai.backends.vulkan import VulkanBackend

__all__ = [
    "CPUBackend",
    "CUDABackend",
    "ROCmBackend",
    "MetalBackend",
    "OpenCLBackend",
    "VulkanBackend",
    "AutoBackendSelector",
]
