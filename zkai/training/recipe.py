"""TrainingRecipe for declarative training lifecycle configuration."""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class TrainingRecipe:
    """Declarative training specification container."""

    name: str = "default_recipe"
    task_type: str = "pretraining"  # pretraining, sft, dpo, instruction_tuning
    epochs: int = 3
    learning_rate: float = 3e-4
    batch_size: int = 32
    gradient_accumulation_steps: int = 1
    mixed_precision: str = "float16"
    warmup_ratio: float = 0.05
    weight_decay: float = 0.01
    max_seq_len: int = 2048
    lora_enabled: bool = False
    lora_rank: int = 16
    lora_alpha: float = 32.0
    custom_args: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "task_type": self.task_type,
            "epochs": self.epochs,
            "learning_rate": self.learning_rate,
            "batch_size": self.batch_size,
            "gradient_accumulation_steps": self.gradient_accumulation_steps,
            "mixed_precision": self.mixed_precision,
            "warmup_ratio": self.warmup_ratio,
            "weight_decay": self.weight_decay,
            "max_seq_len": self.max_seq_len,
            "lora_enabled": self.lora_enabled,
            "lora_rank": self.lora_rank,
            "lora_alpha": self.lora_alpha,
            "custom_args": self.custom_args,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "TrainingRecipe":
        return cls(**data)
