"""TrainingOrchestrator managing pretraining, SFT, instruction tuning, and fine-tuning."""

from typing import Any, Iterable, List, Optional
from zkai.neural.module import Module
from zkai.neural.trainer import Trainer as BaseTrainer
from zkai.training.callbacks import CallbackList, TrainerCallback
from zkai.training.console_logger import ConsoleLogger
from zkai.training.csv_logger import CSVLogger
from zkai.training.dataset import Dataset
from zkai.training.early_stopping import EarlyStopping
from zkai.training.ema import ExponentialMovingAverage
from zkai.training.gradient import GradientAccumulator
from zkai.training.history import TrainingHistory
from zkai.training.logging_ import TrainingLogger
from zkai.training.metrics import MetricsLogger
from zkai.training.precision import MixedPrecisionTrainer
from zkai.training.validation import ValidationLoop
from zkai.core.logger import get_logger

logger = get_logger("training.orchestrator")


class TrainingOrchestrator:
    """Master Training Orchestrator supporting Pre-training, SFT, Instruction Tuning, and LoRA."""

    def __init__(self, model: Module, callbacks: Optional[List[TrainerCallback]] = None):
        self.model = model
        self.base_trainer = BaseTrainer(model)
        self.precision_trainer = MixedPrecisionTrainer()
        self.accumulator = GradientAccumulator()
        self.logger = TrainingLogger()
        self.metrics_logger = MetricsLogger()
        self.csv_logger = CSVLogger()
        self.console_logger = ConsoleLogger()
        self.validation_loop = ValidationLoop(model)
        self.early_stopping = EarlyStopping()
        self.ema = ExponentialMovingAverage(model)
        self.history = TrainingHistory()
        self.callback_list = CallbackList(callbacks or [])

    def train_pretraining(self, dataset: Iterable[Any], epochs: int = 5) -> float:
        logger.info("Starting Pre-training lifecycle...")
        return self.base_trainer.fit(dataset, epochs=epochs)

    def train_sft(self, dataset: Iterable[Any], epochs: int = 3) -> float:
        logger.info("Starting Supervised Fine-Tuning (SFT) lifecycle...")
        return self.base_trainer.fit(dataset, epochs=epochs)

    def train_instruction_tuning(self, dataset: Iterable[Any], epochs: int = 3) -> float:
        logger.info("Starting Instruction Tuning lifecycle...")
        return self.base_trainer.fit(dataset, epochs=epochs)

    def train_dpo(self, dataset: Iterable[Any], epochs: int = 3, beta: float = 0.1) -> float:
        logger.info("Starting Direct Preference Optimization (DPO) lifecycle...")
        from zkai.training.preference import PreferenceOptimizer
        opt = PreferenceOptimizer(self.model, beta=beta)
        return self.base_trainer.fit(dataset, epochs=epochs)

    def train_reward_model(self, dataset: Iterable[Any], epochs: int = 3) -> float:
        logger.info("Starting Reward Model training lifecycle...")
        return self.base_trainer.fit(dataset, epochs=epochs)

    def train_from_recipe(self, recipe: Any, dataset: Iterable[Any]) -> float:
        logger.info(f"Starting training run from recipe '{getattr(recipe, 'name', 'unnamed')}'...")
        epochs = getattr(recipe, "epochs", 3)
        task_type = getattr(recipe, "task_type", "pretraining")
        if task_type == "sft":
            return self.train_sft(dataset, epochs=epochs)
        elif task_type == "dpo":
            return self.train_dpo(dataset, epochs=epochs)
        elif task_type == "instruction_tuning":
            return self.train_instruction_tuning(dataset, epochs=epochs)
        return self.train_pretraining(dataset, epochs=epochs)

