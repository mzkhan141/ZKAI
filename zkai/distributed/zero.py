"""ZeRO Optimizer (Stage 1, 2, 3) partitioning."""

from typing import Any
from zkai.core.logger import get_logger

logger = get_logger("distributed.zero")


class ZeROOptimizer:
    """ZeRO (Zero Redundancy Optimizer) partitioning optimizer states and gradients."""

    def __init__(self, optimizer: Any, stage: int = 2):
        self.optimizer = optimizer
        self.stage = stage
        logger.info(f"Initialized ZeROOptimizer Stage {stage}")
