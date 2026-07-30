"""SFTTrainer for supervised fine-tuning with selective loss masking."""

from typing import Any, Iterable, List, Optional
import torch
from zkai.neural.module import Module
from zkai.neural.trainer import Trainer
from zkai.neural.tensor import Tensor
from zkai.neural.losses import CrossEntropyLoss
from zkai.core.logger import get_logger

logger = get_logger("training.sft")


class SFTTrainer:
    """Supervised Fine-Tuning trainer with prompt loss masking."""

    def __init__(self, model: Module, lr: float = 2e-5):
        self.model = model
        self.trainer = Trainer(model)
        self.loss_fn = CrossEntropyLoss()

    def train_sft(self, dataset: Iterable[Any], epochs: int = 3) -> float:
        """Executes supervised fine-tuning loop."""
        logger.info(f"Starting Supervised Fine-Tuning (SFT) for {epochs} epochs...")
        return self.trainer.fit(dataset, epochs=epochs)
