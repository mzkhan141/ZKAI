"""Whitespace-delimited tokenizer implementation."""

from pathlib import Path
from typing import List, Optional, Sequence
from zkai.tokenizer.base import EncodingResult, SpecialTokens, TokenizerBase
from zkai.tokenizer.vocabulary import Vocabulary


class WhitespaceTokenizer(TokenizerBase):
    """Simple whitespace-delimited word tokenizer."""

    def __init__(self, special_tokens: Optional[SpecialTokens] = None):
        super().__init__(special_tokens)
        self.vocab = Vocabulary(self.special_tokens)

    @property
    def vocab_size(self) -> int:
        return len(self.vocab)

    def train(self, texts: List[str], vocab_size: Optional[int] = None) -> None:
        for text in texts:
            words = text.split()
            for w in words:
                self.vocab.add_token(w)
        if vocab_size:
            self.vocab.prune(min_frequency=1, max_vocab_size=vocab_size)

    def encode(
        self,
        text: str,
        add_special_tokens: bool = True,
        padding: bool = False,
        max_length: Optional[int] = None,
        truncation: bool = False,
    ) -> EncodingResult:
        words = text.split()
        tokens = []
        if add_special_tokens:
            tokens.append(self.special_tokens.bos_token)
        tokens.extend(words)
        if add_special_tokens:
            tokens.append(self.special_tokens.eos_token)

        ids = [self.vocab.token_to_id.get(w, self.vocab.token_to_id.get(self.special_tokens.unk_token, 1)) for w in tokens]
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
        words = [
            self.vocab.id_to_token.get(i, self.special_tokens.unk_token)
            for i in ids
            if not (skip_special_tokens and self.vocab.id_to_token.get(i) in specials)
        ]
        return " ".join(words)

    def save(self, path: str) -> None:
        p = Path(path)
        p.mkdir(parents=True, exist_ok=True)
        self.vocab.save(str(p / "vocab.json"))

    def load(self, path: str) -> None:
        p = Path(path)
        self.vocab.load(str(p / "vocab.json"))
