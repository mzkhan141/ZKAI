"""Fully Sharded Data Parallel (FSDP) trainer wrapper."""

import torch
from zkai.neural.module import Module
from zkai.core.logger import get_logger

logger = get_logger("distributed.fsdp")


class FSDPTrainer:
    """Fully Sharded Data Parallel (FSDP) wrapper for parameter and gradient sharding."""

    def __init__(self, model: Module):
        self.model = model
        logger.info("Initialized FSDPTrainer")

    def wrap_model(self) -> Module:
        return self.model
