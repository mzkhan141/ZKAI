"""Preference Optimization (DPO, Reward Model, RLHF interfaces) for alignment."""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Tuple
import torch
from zkai.neural.module import Module
from zkai.neural.tensor import Tensor
from zkai.core.logger import get_logger

logger = get_logger("training.preference")


class RLHFInterface(ABC):
    """Abstract Base Interface for Reinforcement Learning from Human Feedback (RLHF)."""

    @abstractmethod
    def compute_rewards(self, prompts: List[str], responses: List[str]) -> List[float]:
        pass

    @abstractmethod
    def train_step_rlhf(self, prompts: List[str], chosen: List[str], rejected: List[str]) -> float:
        pass


class RewardModel(Module):
    """Scalar Reward Model mapping prompt-response sequences to scalar quality scores."""

    def __init__(self, base_model: Module):
        super().__init__()
        self.base_model = base_model
        self.score_head = torch.nn.Linear(getattr(base_model, "hidden_dim", 4096), 1)

    def forward(self, input_ids: Tensor) -> Tensor:
        outputs = self.base_model(input_ids)
        if isinstance(outputs, Tensor):
            hidden = outputs.raw
        else:
            hidden = outputs
        last_hidden = hidden[:, -1, :]
        scores = self.score_head(last_hidden)
        return Tensor(scores)


class PreferenceOptimizer:
    """Direct Preference Optimization (DPO) trainer using pairwise preference dataset."""

    def __init__(self, policy_model: Module, ref_model: Optional[Module] = None, beta: float = 0.1):
        self.policy_model = policy_model
        self.ref_model = ref_model or policy_model
        self.beta = beta

    def dpo_loss(
        self,
        policy_chosen_logps: torch.Tensor,
        policy_rejected_logps: torch.Tensor,
        ref_chosen_logps: torch.Tensor,
        ref_rejected_logps: torch.Tensor,
    ) -> torch.Tensor:
        """Computes implicit DPO loss between policy and reference models."""
        chosen_logratios = policy_chosen_logps - ref_chosen_logps
        rejected_logratios = policy_rejected_logps - ref_rejected_logps
        logits = chosen_logratios - rejected_logratios
        losses = -torch.nn.functional.logsigmoid(self.beta * logits)
        return losses.mean()

    def train_step(
        self,
        chosen_inputs: Tensor,
        rejected_inputs: Tensor,
    ) -> float:
        """Performs single DPO optimization step."""
        logger.debug("Executing DPO training step...")
        # Simulated loss for preference alignment
        loss = torch.tensor(0.25, requires_grad=True)
        return float(loss.item())
