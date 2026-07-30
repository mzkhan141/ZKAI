"""Language Model Base Class and LLM interfaces."""

from abc import ABC, abstractmethod
from typing import Any, Generator, List, Optional
from zkai.transformer.decoder import Decoder
from zkai.transformer.inference import InferenceEngine
from zkai.core.config import TransformerConfig


class LLM(ABC):
    """Abstract Base Class for Large Language Models."""

    @abstractmethod
    def generate(self, prompt: str, max_tokens: int = 128) -> str:
        pass

    @abstractmethod
    def stream(self, prompt: str) -> Generator[str, None, None]:
        pass


class LanguageModel(LLM):
    """Native ZKAI Language Model encapsulating Decoder Transformer model and inference engine."""

    def __init__(self, config: Optional[TransformerConfig] = None, **kwargs):
        self.config = config or TransformerConfig(**kwargs)
        self.decoder = Decoder(config=self.config)
        self.engine = InferenceEngine(model=self.decoder)

    def train(self, dataset: Any) -> None:
        """Fine-tunes or pre-trains the language model on text datasets."""
        from zkai.neural.trainer import Trainer
        trainer = Trainer(self.decoder)
        trainer.fit(dataset)

    def generate(self, prompt: str, max_tokens: int = 128) -> str:
        return self.engine.generate(prompt, max_new_tokens=max_tokens)

    def stream(self, prompt: str) -> Generator[str, None, None]:
        yield from self.engine.generate_stream(prompt)
