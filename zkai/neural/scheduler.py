"""Learning rate schedulers (CosineAnnealing, Warmup, StepLR)."""

from typing import Optional
import torch.optim.lr_scheduler as lr_scheduler
from zkai.neural.optimizers import Optimizer


class Scheduler:
    """Base wrapper for learning rate schedulers."""

    def __init__(self, optimizer: Optimizer):
        self.optimizer = optimizer
        self._scheduler: Optional[lr_scheduler.LRScheduler] = None

    def step(self) -> None:
        if self._scheduler:
            self._scheduler.step()

    def get_last_lr(self) -> list[float]:
        if self._scheduler:
            return self._scheduler.get_last_lr()
        return [self.optimizer.lr]


class StepLR(Scheduler):
    """Decays learning rate by gamma every step_size epochs."""

    def __init__(self, optimizer: Optimizer, step_size: int, gamma: float = 0.1):
        super().__init__(optimizer)
        self._scheduler = lr_scheduler.StepLR(self.optimizer._optimizer, step_size=step_size, gamma=gamma)


class CosineAnnealingLR(Scheduler):
    """Cosine annealing learning rate schedule."""

    def __init__(self, optimizer: Optimizer, T_max: int, eta_min: float = 0.0):
        super().__init__(optimizer)
        self._scheduler = lr_scheduler.CosineAnnealingLR(self.optimizer._optimizer, T_max=T_max, eta_min=eta_min)


class WarmupLR(Scheduler):
    """Linear warmup learning rate schedule."""

    def __init__(self, optimizer: Optimizer, warmup_steps: int):
        super().__init__(optimizer)
        self.warmup_steps = warmup_steps
        self.current_step = 0
        self.base_lr = optimizer.lr

    def step(self) -> None:
        self.current_step += 1
        if self.current_step <= self.warmup_steps:
            new_lr = self.base_lr * (self.current_step / self.warmup_steps)
            for param_group in self.optimizer._optimizer.param_groups:
                param_group['lr'] = new_lr
