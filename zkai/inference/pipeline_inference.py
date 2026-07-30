"""PipelineInference and ModelSharding for distributing model layers across devices."""

from typing import Any, Dict, List, Optional
import torch
from zkai.neural.module import Module
from zkai.neural.tensor import Tensor
from zkai.core.logger import get_logger

logger = get_logger("inference.pipeline_inference")


class ModelSharding:
    """Partitions model transformer blocks across multiple target devices."""

    def shard_model(self, model: Module, num_devices: int) -> List[List[Module]]:
        """Splits model sub-blocks into equal stage groups per device."""
        all_blocks = list(getattr(model, "blocks", []))
        if not all_blocks:
            return [[model]]

        num_devices = max(1, min(num_devices, len(all_blocks)))
        blocks_per_dev = (len(all_blocks) + num_devices - 1) // num_devices

        shards = []
        for i in range(0, len(all_blocks), blocks_per_dev):
            shards.append(all_blocks[i : i + blocks_per_dev])
        return shards


class PipelineInference:
    """Pipeline parallel inference executor passing hidden states across device stages."""

    def __init__(self, shards: List[List[Module]], devices: List[str]):
        self.shards = shards
        self.devices = devices

    def forward_pipeline(self, input_tensor: Tensor) -> Tensor:
        """Executes forward pass sequentially through pipeline stages."""
        current = input_tensor
        for stage_idx, stage_blocks in enumerate(self.shards):
            dev = self.devices[stage_idx % len(self.devices)]
            logger.debug(f"Forwarding pipeline stage {stage_idx} on device {dev}")
            for block in stage_blocks:
                current = block(current)
        return current
