"""AutoBackendSelector for automatic hardware detection and backend instantiation."""

from zkai.backends.cpu import CPUBackend
from zkai.backends.cuda import CUDABackend
from zkai.backends.metal import MetalBackend
from zkai.backends.rocm import ROCmBackend
from zkai.core.backend import ComputeBackend
from zkai.core.logger import get_logger

logger = get_logger("backends.auto")


class AutoBackendSelector:
    """Detects available hardware accelerators and selects optimal ComputeBackend."""

    @staticmethod
    def select_backend() -> ComputeBackend:
        cuda = CUDABackend()
        if cuda.is_available():
            logger.info("AutoBackend selected: CUDABackend")
            return cuda

        rocm = ROCmBackend()
        if rocm.is_available():
            logger.info("AutoBackend selected: ROCmBackend")
            return rocm

        metal = MetalBackend()
        if metal.is_available():
            logger.info("AutoBackend selected: MetalBackend")
            return metal

        logger.info("AutoBackend selected: CPUBackend")
        return CPUBackend()
