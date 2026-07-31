"""SentencePiece tokenizer wrapper and native fallback implementation."""

from pathlib import Path
from typing import List, Optional, Sequence
from zkai.tokenizer.base import EncodingResult, SpecialTokens, TokenizerBase
from zkai.tokenizer.bpe import BytePairTokenizer
from zkai.core.logger import get_logger

logger = get_logger("tokenizer.sentencepiece")


class SentencePieceTokenizer(TokenizerBase):
    """SentencePiece subword tokenizer wrapper with native fallback."""

    def __init__(self, model_file: Optional[str] = None, special_tokens: Optional[SpecialTokens] = None):
        super().__init__(special_tokens)
        self.model_file = model_file
        self.fallback_bpe = BytePairTokenizer(special_tokens=self.special_tokens)
        self._sp_processor = None

        if model_file and Path(model_file).exists():
            try:
                import sentencepiece as spm
                self._sp_processor = spm.SentencePieceProcessor()
                self._sp_processor.load(model_file)
            except ImportError:
                logger.warning("sentencepiece package not installed. Using native BPE fallback.")

    @property
    def vocab_size(self) -> int:
        if self._sp_processor:
            return self._sp_processor.get_piece_size()
        return self.fallback_bpe.vocab_size

    def train(self, texts: List[str], vocab_size: int = 32000) -> None:
        if self._sp_processor is None:
            self.fallback_bpe.train(texts, vocab_size=vocab_size)

    def encode(
        self,
        text: str,
        add_special_tokens: bool = True,
        padding: bool = False,
        max_length: Optional[int] = None,
        truncation: bool = False,
    ) -> EncodingResult:
        if self._sp_processor:
            ids = self._sp_processor.encode_as_ids(text)
            tokens = self._sp_processor.encode_as_pieces(text)
            if add_special_tokens:
                ids = [1] + ids + [2]
                tokens = [self.special_tokens.bos_token] + tokens + [self.special_tokens.eos_token]
            if truncation and max_length is not None and len(ids) > max_length:
                ids = ids[:max_length]
                tokens = tokens[:max_length]
            att_mask = [1] * len(ids)
            pos_ids = list(range(len(ids)))
            offsets = [(0, len(t)) for t in tokens]
            type_ids = [0] * len(ids)
            return EncodingResult(ids, tokens, att_mask, pos_ids, offsets, type_ids)
        return self.fallback_bpe.encode(text, add_special_tokens, padding, max_length, truncation)

    def decode(self, ids: Sequence[int], skip_special_tokens: bool = True) -> str:
        if self._sp_processor:
            return self._sp_processor.decode(list(ids))
        return self.fallback_bpe.decode(ids, skip_special_tokens)

    def save(self, path: str) -> None:
        self.fallback_bpe.save(path)

    def load(self, path: str) -> None:
        self.fallback_bpe.load(path)
