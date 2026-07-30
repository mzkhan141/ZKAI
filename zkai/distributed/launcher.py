"""MultiNodeLauncher for distributed worker process spawning."""

from typing import Any, Callable
from zkai.core.logger import get_logger

logger = get_logger("distributed.launcher")


class MultiNodeLauncher:
    """Launches distributed training process group across multi-node clusters."""

    def __init__(self, num_nodes: int = 1, gpus_per_node: int = 1):
        self.num_nodes = num_nodes
        self.gpus_per_node = gpus_per_node

    def launch(self, entrypoint_fn: Callable[..., Any]) -> None:
        logger.info(f"Launching distributed cluster with {self.num_nodes} nodes ({self.gpus_per_node} GPUs/node)")
