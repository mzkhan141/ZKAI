"""ValidationLoop and EvaluationLoop for validation phases."""

from typing import Any, Iterable
from zkai.neural.module import Module
from zkai.neural.tensor import Tensor


class ValidationLoop:
    """Executes validation passes on evaluation dataset."""

    def __init__(self, model: Module):
        self.model = model

    def evaluate(self, val_dataset: Iterable[tuple[Any, Any]]) -> float:
        self.model.eval()
        total_loss = 0.0
        count = 0
        for batch_x, batch_y in val_dataset:
            x_tensor = batch_x if isinstance(batch_x, Tensor) else Tensor(batch_x)
            y_tensor = batch_y if isinstance(batch_y, Tensor) else Tensor(batch_y)
            out = self.model(x_tensor)
            diff = out - y_tensor
            loss = float((diff * diff).mean().item())
            total_loss += loss
            count += 1
        return total_loss / max(1, count)


class EvaluationLoop(ValidationLoop):
    """Evaluation loop alias for test dataset benchmarking."""

    pass
