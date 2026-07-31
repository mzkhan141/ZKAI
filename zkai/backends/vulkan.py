"""Vulkan compute backend abstraction."""

from zkai.core.backend import PyTorchBackend


class VulkanBackend(PyTorchBackend):
    """Vulkan compute backend provider with CPU fallback."""

    def __init__(self):
        super().__init__(device="cpu")

    def name(self) -> str:
        return "VulkanBackend"

    def is_available(self) -> bool:
        return False
