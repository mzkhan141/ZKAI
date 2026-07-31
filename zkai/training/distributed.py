"""DistributedTrainer for multi-GPU DDP and FSDP distributed training."""

import torch.distributed as dist
from zkai.core.logger import get_logger

logger = get_logger("training.distributed")


class DistributedTrainer:
    """Orchestrates Distributed Data Parallel (DDP) multi-GPU training."""

    def __init__(self, backend: str = "nccl"):
        self.backend = backend

    def init_process_group(self, rank: int, world_size: int) -> None:
        logger.info(f"Initializing process group rank {rank}/{world_size} using {self.backend}")
        dist.init_process_group(backend=self.backend, rank=rank, world_size=world_size)

    def cleanup(self) -> None:
        if dist.is_initialized():
            dist.destroy_process_group()
