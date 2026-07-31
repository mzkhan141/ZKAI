"""Distributed Data Parallel (DDP) trainer wrapper."""

from typing import List, Optional
import torch
import torch.nn as nn
from zkai.neural.module import Module
from zkai.core.logger import get_logger

logger = get_logger("distributed.ddp")


class DDPTrainer:
    """Wraps model for Distributed Data Parallel multi-GPU data parallel execution."""

    def __init__(self, model: Module, device_ids: Optional[List[int]] = None):
        self.model = model
        self.device_ids = device_ids
        logger.info(f"Initialized DDPTrainer on devices: {device_ids}")

    def wrap_model(self) -> Module:
        if torch.cuda.is_available() and hasattr(self.model, '_torch_module') and self.model._torch_module:
            self.model._torch_module = nn.parallel.DistributedDataParallel(
                self.model._torch_module, device_ids=self.device_ids
            )
        return self.model
