"""Unigram language model tokenizer implementation."""

import math
from pathlib import Path
from typing import Dict, List, Optional, Sequence
from zkai.tokenizer.base import EncodingResult, SpecialTokens, TokenizerBase
from zkai.tokenizer.vocabulary import Vocabulary
from zkai.core.logger import get_logger

logger = get_logger("tokenizer.unigram")


class UnigramTokenizer(TokenizerBase):
    """Unigram Language Model Tokenizer."""

    def __init__(self, vocab_size: int = 1000, special_tokens: Optional[SpecialTokens] = None):
        super().__init__(special_tokens)
        self._target_vocab_size = vocab_size
        self.vocab = Vocabulary(self.special_tokens)
        self.token_probs: Dict[str, float] = {}

    @property
    def vocab_size(self) -> int:
        return len(self.vocab)

    def train(self, texts: List[str], vocab_size: Optional[int] = None) -> None:
        target = vocab_size or self._target_vocab_size
        all_chars = set(c for text in texts for c in text)
        for c in all_chars:
            self.vocab.add_token(c)
            self.token_probs[c] = -math.log(1.0 / (len(all_chars) + 1))
        self.vocab.prune(min_frequency=1, max_vocab_size=target)

    def encode(
        self,
        text: str,
        add_special_tokens: bool = True,
        padding: bool = False,
        max_length: Optional[int] = None,
        truncation: bool = False,
    ) -> EncodingResult:
        tokens: List[str] = []
        if add_special_tokens:
            tokens.append(self.special_tokens.bos_token)
        for char in text:
            if char in self.vocab.token_to_id:
                tokens.append(char)
            else:
                tokens.append(self.special_tokens.unk_token)
        if add_special_tokens:
            tokens.append(self.special_tokens.eos_token)

        ids = [self.vocab.token_to_id.get(t, 1) for t in tokens]
        if truncation and max_length is not None and len(ids) > max_length:
            ids = ids[:max_length]
            tokens = tokens[:max_length]

        att_mask = [1] * len(ids)
        pos_ids = list(range(len(ids)))
        offsets = [(0, len(t)) for t in tokens]
        type_ids = [0] * len(ids)
        return EncodingResult(ids, tokens, att_mask, pos_ids, offsets, type_ids)

    def decode(self, ids: Sequence[int], skip_special_tokens: bool = True) -> str:
        specials = set(self.special_tokens.to_list())
        tokens = [
            self.vocab.id_to_token.get(i, self.special_tokens.unk_token)
            for i in ids
            if not (skip_special_tokens and self.vocab.id_to_token.get(i) in specials)
        ]
        return "".join(tokens)

    def save(self, path: str) -> None:
        p = Path(path)
        p.mkdir(parents=True, exist_ok=True)
        self.vocab.save(str(p / "vocab.json"))

    def load(self, path: str) -> None:
        p = Path(path)
        self.vocab.load(str(p / "vocab.json"))
