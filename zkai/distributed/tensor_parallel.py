"""Tensor Parallelism for splitting individual linear weights across GPUs."""

from zkai.neural.module import Module
from zkai.core.logger import get_logger

logger = get_logger("distributed.tensor_parallel")


class TensorParallel:
    """Splits linear and attention layers horizontally and vertically across devices."""

    def __init__(self, model: Module, tp_degree: int = 2):
        self.model = model
        self.tp_degree = tp_degree
        logger.info(f"Initialized TensorParallel with degree {tp_degree}")
