"""GradientAccumulator and GradientCheckpointer."""

import torch
from zkai.neural.module import Module


class GradientAccumulator:
    """Manages gradient accumulation steps across batch iterations."""

    def __init__(self, accumulation_steps: int = 1):
        self.accumulation_steps = max(1, accumulation_steps)
        self.current_step = 0

    def should_step(self) -> bool:
        self.current_step += 1
        if self.current_step % self.accumulation_steps == 0:
            return True
        return False


class GradientCheckpointer:
    """Activation gradient checkpointing for memory-saving backward passes."""

    @staticmethod
    def checkpoint(function, *args):
        return torch.utils.checkpoint.checkpoint(function, *args)
