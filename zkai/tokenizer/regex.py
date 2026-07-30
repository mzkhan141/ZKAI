"""Regex-based pattern tokenizer."""

from pathlib import Path
import re
from typing import List, Optional, Sequence
from zkai.tokenizer.base import EncodingResult, SpecialTokens, TokenizerBase
from zkai.tokenizer.vocabulary import Vocabulary
from zkai.core.logger import get_logger

logger = get_logger("tokenizer.regex")

GPT4_SPLIT_REGEX = r"""'(?i:[sdmt]|ll|ve|re)|[^\r\n\p{L}\p{N}]?+\p{L}+|\p{N}{1,3}| ?[^\s\p{L}\p{N}]++[\r\n]*|\s*[\r\n]|\s+(?!\S)|\s+"""


class RegexTokenizer(TokenizerBase):
    """Regex-based pre-tokenizer and pattern splitter."""

    def __init__(
        self,
        pattern: str = r"\w+|[^\w\s]",
        vocab_size: int = 5000,
        special_tokens: Optional[SpecialTokens] = None,
    ):
        super().__init__(special_tokens)
        self.pattern = pattern
        self.regex = re.compile(pattern)
        self.vocab = Vocabulary(self.special_tokens)
        self._target_vocab = vocab_size

    @property
    def vocab_size(self) -> int:
        return len(self.vocab)

    def train(self, texts: List[str], vocab_size: Optional[int] = None) -> None:
        target = vocab_size or self._target_vocab
        for text in texts:
            matches = self.regex.findall(text)
            for m in matches:
                self.vocab.add_token(m)
        self.vocab.prune(min_frequency=1, max_vocab_size=target)

    def encode(
        self,
        text: str,
        add_special_tokens: bool = True,
        padding: bool = False,
        max_length: Optional[int] = None,
        truncation: bool = False,
    ) -> EncodingResult:
        raw_matches = self.regex.findall(text)
        tokens = []
        if add_special_tokens:
            tokens.append(self.special_tokens.bos_token)
        tokens.extend(raw_matches)
        if add_special_tokens:
            tokens.append(self.special_tokens.eos_token)

        ids = [self.vocab.token_to_id.get(t, self.vocab.token_to_id.get(self.special_tokens.unk_token, 1)) for t in tokens]
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
        return " ".join(tokens)

    def save(self, path: str) -> None:
        p = Path(path)
        p.mkdir(parents=True, exist_ok=True)
        self.vocab.save(str(p / "vocab.json"))

    def load(self, path: str) -> None:
        p = Path(path)
        self.vocab.load(str(p / "vocab.json"))
