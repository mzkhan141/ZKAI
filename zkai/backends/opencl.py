"""OpenCL compute backend abstraction."""

from zkai.core.backend import PyTorchBackend


class OpenCLBackend(PyTorchBackend):
    """OpenCL compute backend provider with CPU fallback."""

    def __init__(self):
        super().__init__(device="cpu")

    def name(self) -> str:
        return "OpenCLBackend"

    def is_available(self) -> bool:
        try:
            import pyopencl as cl
            return len(cl.get_platforms()) > 0
        except Exception:
            return False
