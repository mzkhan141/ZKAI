"""Base classes, dataclasses, and abstract interfaces for the Tokenizer subsystem."""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Sequence, Union
from zkai.core.logger import get_logger

logger = get_logger("tokenizer.base")


@dataclass
class Token:
    """Represents an individual token in a sequence."""

    id: int
    text: str
    start: int = 0
    end: int = 0
    token_type_id: int = 0
    special: bool = False


@dataclass
class SpecialTokens:
    """Special tokens used across tokenization strategies."""

    pad_token: str = "<pad>"
    unk_token: str = "<unk>"
    bos_token: str = "<s>"
    eos_token: str = "</s>"
    mask_token: str = "<mask>"
    sep_token: str = "<sep>"
    cls_token: str = "<cls>"

    def to_list(self) -> List[str]:
        return [
            self.pad_token,
            self.unk_token,
            self.bos_token,
            self.eos_token,
            self.mask_token,
            self.sep_token,
            self.cls_token,
        ]


@dataclass
class EncodingResult:
    """Complete output of encoding a sequence or batch."""

    ids: List[int]
    tokens: List[str]
    attention_mask: List[int]
    position_ids: List[int]
    offset_mapping: List[tuple[int, int]]
    type_ids: List[int]


class TokenizerBase(ABC):
    """Abstract Base Class for all ZKAI tokenizers."""

    def __init__(self, special_tokens: Optional[SpecialTokens] = None):
        self.special_tokens = special_tokens or SpecialTokens()
        self._added_tokens: Dict[str, int] = {}

    @property
    @abstractmethod
    def vocab_size(self) -> int:
        """Returns the total vocabulary size."""
        pass

    @abstractmethod
    def encode(
        self,
        text: str,
        add_special_tokens: bool = True,
        padding: bool = False,
        max_length: Optional[int] = None,
        truncation: bool = False,
    ) -> EncodingResult:
        """Encodes raw text string into Tokenizer EncodingResult."""
        pass

    @abstractmethod
    def decode(self, ids: Sequence[int], skip_special_tokens: bool = True) -> str:
        """Decodes integer token IDs back to a text string."""
        pass

    @abstractmethod
    def train(self, texts: List[str], vocab_size: int = 32000) -> None:
        """Learns tokenization vocabulary from text corpus."""
        pass

    @abstractmethod
    def save(self, path: str) -> None:
        """Saves tokenizer state to disk."""
        pass

    @abstractmethod
    def load(self, path: str) -> None:
        """Loads tokenizer state from disk."""
        pass

    def add_special_tokens(self, tokens: List[str]) -> int:
        """Adds custom special tokens to tokenizer dictionary."""
        added = 0
        for token in tokens:
            if token not in self._added_tokens:
                self._added_tokens[token] = self.vocab_size + added
                added += 1
        return added

    def add_tokens(self, tokens: List[str]) -> int:
        """Adds custom regular tokens to tokenizer dictionary."""
        return self.add_special_tokens(tokens)

    def batch_encode(
        self,
        texts: List[str],
        add_special_tokens: bool = True,
        padding: bool = True,
        max_length: Optional[int] = None,
        truncation: bool = True,
    ) -> List[EncodingResult]:
        """Encodes a batch of raw text strings."""
        return [
            self.encode(
                text,
                add_special_tokens=add_special_tokens,
                padding=padding,
                max_length=max_length,
                truncation=truncation,
            )
            for text in texts
        ]
