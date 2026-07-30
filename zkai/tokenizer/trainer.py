"""Unified TokenizerTrainer for learning vocabularies across tokenizer types."""

from typing import List, Optional, Type
from zkai.tokenizer.base import TokenizerBase
from zkai.tokenizer.bpe import BytePairTokenizer
from zkai.core.logger import get_logger

logger = get_logger("tokenizer.trainer")


class TokenizerTrainer:
    """Trainer orchestrator for fitting tokenizers on corpora."""

    def __init__(self, tokenizer_cls: Type[TokenizerBase] = BytePairTokenizer):
        self.tokenizer_cls = tokenizer_cls

    def train_from_texts(
        self,
        texts: List[str],
        vocab_size: int = 32000,
        save_path: Optional[str] = None,
    ) -> TokenizerBase:
        logger.info(f"Fitting {self.tokenizer_cls.__name__} on corpus with target vocab size {vocab_size}...")
        tokenizer = self.tokenizer_cls(vocab_size=vocab_size)
        tokenizer.train(texts, vocab_size=vocab_size)
        if save_path:
            tokenizer.save(save_path)
            logger.info(f"Saved trained tokenizer to {save_path}")
        return tokenizer
