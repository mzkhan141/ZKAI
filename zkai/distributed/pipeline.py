"""Pipeline Parallel execution wrapper for partitioning model layers across GPUs."""

from typing import List
import torch
from zkai.neural.module import Module
from zkai.core.logger import get_logger

logger = get_logger("distributed.pipeline")


class PipelineParallel:
    """Partitions model layers across GPU devices for pipeline parallelism."""

    def __init__(self, model: Module, num_stages: int = 2):
        self.model = model
        self.num_stages = num_stages
        logger.info(f"Initialized PipelineParallel across {num_stages} stages")
