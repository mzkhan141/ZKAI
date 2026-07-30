"""WordPiece tokenizer implementation."""

from pathlib import Path
from typing import List, Optional, Sequence
from zkai.tokenizer.base import EncodingResult, SpecialTokens, TokenizerBase
from zkai.tokenizer.normalization import UnicodeNormalizer
from zkai.tokenizer.vocabulary import Vocabulary
from zkai.core.logger import get_logger

logger = get_logger("tokenizer.wordpiece")


class WordPieceTokenizer(TokenizerBase):
    """WordPiece subword tokenizer (BERT-style prefix ##)."""

    def __init__(self, vocab_size: int = 1000, special_tokens: Optional[SpecialTokens] = None):
        super().__init__(special_tokens)
        self._target_vocab_size = vocab_size
        self.vocab = Vocabulary(self.special_tokens)
        self.normalizer = UnicodeNormalizer(lowercase=True)

    @property
    def vocab_size(self) -> int:
        return len(self.vocab)

    def train(self, texts: List[str], vocab_size: Optional[int] = None) -> None:
        target = vocab_size or self._target_vocab_size
        normalized = [self.normalizer.normalize(t) for t in texts if t.strip()]
        for text in normalized:
            words = text.split()
            for w in words:
                if w:
                    self.vocab.add_token(w[0])
                    for char in w[1:]:
                        self.vocab.add_token(f"##{char}")
        self.vocab.prune(min_frequency=1, max_vocab_size=target)

    def encode(
        self,
        text: str,
        add_special_tokens: bool = True,
        padding: bool = False,
        max_length: Optional[int] = None,
        truncation: bool = False,
    ) -> EncodingResult:
        normalized = self.normalizer.normalize(text)
        words = normalized.split()
        subwords: List[str] = []

        if add_special_tokens:
            subwords.append(self.special_tokens.cls_token)

        for word in words:
            start = 0
            is_bad = False
            word_subwords = []
            while start < len(word):
                end = len(word)
                cur_substr = None
                while start < end:
                    substr = word[start:end]
                    if start > 0:
                        substr = f"##{substr}"
                    if substr in self.vocab.token_to_id:
                        cur_substr = substr
                        break
                    end -= 1
                if cur_substr is None:
                    is_bad = True
                    break
                word_subwords.append(cur_substr)
                start = end
            if is_bad:
                subwords.append(self.special_tokens.unk_token)
            else:
                subwords.extend(word_subwords)

        if add_special_tokens:
            subwords.append(self.special_tokens.sep_token)

        ids = [self.vocab.token_to_id.get(w, self.vocab.token_to_id.get(self.special_tokens.unk_token, 1)) for w in subwords]

        if truncation and max_length is not None and len(ids) > max_length:
            ids = ids[:max_length]
            subwords = subwords[:max_length]

        att_mask = [1] * len(ids)
        pos_ids = list(range(len(ids)))
        offsets = [(0, len(s)) for s in subwords]
        type_ids = [0] * len(ids)

        return EncodingResult(ids, subwords, att_mask, pos_ids, offsets, type_ids)

    def decode(self, ids: Sequence[int], skip_special_tokens: bool = True) -> str:
        specials = set(self.special_tokens.to_list())
        tokens = []
        for i in ids:
            tok = self.vocab.id_to_token.get(i, self.special_tokens.unk_token)
            if skip_special_tokens and tok in specials:
                continue
            tokens.append(tok)
        out = " ".join(tokens).replace(" ##", "")
        return out

    def save(self, path: str) -> None:
        p = Path(path)
        p.mkdir(parents=True, exist_ok=True)
        self.vocab.save(str(p / "vocab.json"))

    def load(self, path: str) -> None:
        p = Path(path)
        self.vocab.load(str(p / "vocab.json"))
