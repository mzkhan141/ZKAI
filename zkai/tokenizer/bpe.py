"""Native BytePairEncoding tokenizer implementation with subword regularization."""

from collections import Counter, defaultdict
import json
from pathlib import Path
import random
from typing import Dict, List, Optional, Sequence, Tuple
from zkai.tokenizer.base import EncodingResult, SpecialTokens, TokenizerBase
from zkai.tokenizer.normalization import UnicodeNormalizer
from zkai.tokenizer.vocabulary import Vocabulary
from zkai.core.logger import get_logger

logger = get_logger("tokenizer.bpe")


class BytePairTokenizer(TokenizerBase):
    """Native Byte Pair Encoding tokenizer with merge rules and subword regularization."""

    def __init__(self, vocab_size: int = 1000, special_tokens: Optional[SpecialTokens] = None):
        super().__init__(special_tokens)
        self._vocab_size_target = vocab_size
        self.vocab = Vocabulary(self.special_tokens)
        self.merges: Dict[Tuple[str, str], str] = {}
        self.normalizer = UnicodeNormalizer()

    @property
    def vocab_size(self) -> int:
        return len(self.vocab)

    def train(self, texts: List[str], vocab_size: Optional[int] = None) -> None:
        target_size = vocab_size or self._vocab_size_target
        words = [list(self.normalizer.normalize(text)) + ["</w>"] for text in texts if text.strip()]
        if not words:
            return

        base_chars = set(char for word in words for char in word)
        for char in base_chars:
            self.vocab.add_token(char)

        num_merges = target_size - len(self.vocab)
        for _ in range(max(1, num_merges)):
            pairs = defaultdict(int)
            for word in words:
                for j in range(len(word) - 1):
                    pairs[(word[j], word[j + 1])] += 1
            if not pairs:
                break
            best_pair = max(pairs, key=pairs.get)
            merged_token = "".join(best_pair)
            self.merges[best_pair] = merged_token
            self.vocab.add_token(merged_token)

            new_words = []
            for word in words:
                new_word = []
                j = 0
                while j < len(word):
                    if j < len(word) - 1 and (word[j], word[j + 1]) == best_pair:
                        new_word.append(merged_token)
                        j += 2
                    else:
                        new_word.append(word[j])
                        j += 1
                new_words.append(new_word)
            words = new_words

        logger.info(f"BPE training complete. Merges: {len(self.merges)}, Vocab size: {self.vocab_size}")

    def _encode_word(self, word: str, dropout: float = 0.0) -> List[str]:
        tokens = list(word) + ["</w>"]
        while len(tokens) > 1:
            pairs = [(tokens[i], tokens[i + 1]) for i in range(len(tokens) - 1)]
            mergeable = [p for p in pairs if p in self.merges]
            if not mergeable:
                break
            if dropout > 0.0 and len(mergeable) > 1:
                if random.random() < dropout:
                    mergeable = mergeable[1:]
            pair = min(mergeable, key=lambda p: list(self.merges.keys()).index(p))
            new_tokens = []
            i = 0
            while i < len(tokens):
                if i < len(tokens) - 1 and (tokens[i], tokens[i + 1]) == pair:
                    new_tokens.append(self.merges[pair])
                    i += 2
                else:
                    new_tokens.append(tokens[i])
                    i += 1
            tokens = new_tokens
        return tokens

    def encode(
        self,
        text: str,
        add_special_tokens: bool = True,
        padding: bool = False,
        max_length: Optional[int] = None,
        truncation: bool = False,
        dropout: float = 0.0,
    ) -> EncodingResult:
        normalized = self.normalizer.normalize(text)
        words = normalized.split()
        subwords: List[str] = []

        if add_special_tokens:
            subwords.append(self.special_tokens.bos_token)

        for w in words:
            subwords.extend(self._encode_word(w, dropout=dropout))

        if add_special_tokens:
            subwords.append(self.special_tokens.eos_token)

        ids = [self.vocab.token_to_id.get(tok, self.vocab.token_to_id.get(self.special_tokens.unk_token, 1)) for tok in subwords]

        if truncation and max_length is not None and len(ids) > max_length:
            ids = ids[:max_length]
            subwords = subwords[:max_length]

        attention_mask = [1] * len(ids)
        position_ids = list(range(len(ids)))
        offset_mapping = [(0, len(tok)) for tok in subwords]
        type_ids = [0] * len(ids)

        if padding and max_length is not None and len(ids) < max_length:
            pad_id = self.vocab.token_to_id.get(self.special_tokens.pad_token, 0)
            pad_len = max_length - len(ids)
            ids.extend([pad_id] * pad_len)
            subwords.extend([self.special_tokens.pad_token] * pad_len)
            attention_mask.extend([0] * pad_len)
            position_ids.extend([0] * pad_len)
            offset_mapping.extend([(0, 0)] * pad_len)
            type_ids.extend([0] * pad_len)

        return EncodingResult(
            ids=ids,
            tokens=subwords,
            attention_mask=attention_mask,
            position_ids=position_ids,
            offset_mapping=offset_mapping,
            type_ids=type_ids,
        )

    def decode(self, ids: Sequence[int], skip_special_tokens: bool = True) -> str:
        specials = set(self.special_tokens.to_list())
        tokens = []
        for i in ids:
            tok = self.vocab.id_to_token.get(i, self.special_tokens.unk_token)
            if skip_special_tokens and tok in specials:
                continue
            tokens.append(tok)
        text = "".join(tokens).replace("</w>", " ")
        return text.strip()

    def save(self, path: str) -> None:
        p = Path(path)
        p.mkdir(parents=True, exist_ok=True)
        self.vocab.save(str(p / "vocab.json"))
        merges_data = [f"{k[0]} {k[1]}" for k in self.merges.keys()]
        (p / "merges.txt").write_text("\n".join(merges_data), encoding="utf-8")

    def load(self, path: str) -> None:
        p = Path(path)
        self.vocab.load(str(p / "vocab.json"))
        if (p / "merges.txt").exists():
            lines = (p / "merges.txt").read_text(encoding="utf-8").splitlines()
            self.merges = {}
            for line in lines:
                if line.strip():
                    parts = line.split()
                    if len(parts) == 2:
                        self.merges[(parts[0], parts[1])] = "".join(parts)
