"""Fast HuggingFace tokenizers C++ backend wrapper."""

from pathlib import Path
from typing import List, Optional, Sequence
from tokenizers import Tokenizer as HFTokenizer
from tokenizers.models import BPE
from tokenizers.pre_tokenizers import Whitespace
from tokenizers.trainers import BpeTrainer
from zkai.tokenizer.base import EncodingResult, SpecialTokens, TokenizerBase
from zkai.core.logger import get_logger

logger = get_logger("tokenizer.fast")


class FastTokenizer(TokenizerBase):
    """High-performance Rust/C++ tokenizers wrapper."""

    def __init__(self, vocab_size: int = 32000, special_tokens: Optional[SpecialTokens] = None):
        super().__init__(special_tokens)
        self._vocab_size_target = vocab_size
        self._hf_tokenizer = HFTokenizer(BPE(unk_token=self.special_tokens.unk_token))
        self._hf_tokenizer.pre_tokenizer = Whitespace()

    @property
    def vocab_size(self) -> int:
        return self._hf_tokenizer.get_vocab_size()

    def train(self, texts: List[str], vocab_size: Optional[int] = None) -> None:
        target = vocab_size or self._vocab_size_target
        trainer = BpeTrainer(vocab_size=target, special_tokens=self.special_tokens.to_list())
        self._hf_tokenizer.train_from_iterator(texts, trainer=trainer)
        logger.info(f"FastTokenizer trained with vocab size {self.vocab_size}")

    def encode(
        self,
        text: str,
        add_special_tokens: bool = True,
        padding: bool = False,
        max_length: Optional[int] = None,
        truncation: bool = False,
    ) -> EncodingResult:
        enc = self._hf_tokenizer.encode(text, add_special_tokens=add_special_tokens)
        ids = list(enc.ids)
        tokens = list(enc.tokens)

        if truncation and max_length is not None and len(ids) > max_length:
            ids = ids[:max_length]
            tokens = tokens[:max_length]

        att_mask = [1] * len(ids)
        pos_ids = list(range(len(ids)))
        offsets = list(enc.offsets) if enc.offsets else [(0, len(t)) for t in tokens]
        type_ids = list(enc.type_ids) if enc.type_ids else [0] * len(ids)

        return EncodingResult(ids, tokens, att_mask, pos_ids, offsets, type_ids)

    def decode(self, ids: Sequence[int], skip_special_tokens: bool = True) -> str:
        return self._hf_tokenizer.decode(list(ids), skip_special_tokens=skip_special_tokens)

    def save(self, path: str) -> None:
        p = Path(path)
        if p.is_dir() or not p.suffix:
            p.mkdir(parents=True, exist_ok=True)
            file_path = str(p / "tokenizer.json")
        else:
            p.parent.mkdir(parents=True, exist_ok=True)
            file_path = str(p)
        self._hf_tokenizer.save(file_path)

    def load(self, path: str) -> None:
        p = Path(path)
        file_path = str(p / "tokenizer.json") if p.is_dir() else str(p)
        self._hf_tokenizer = HFTokenizer.from_file(file_path)
