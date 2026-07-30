"""Vocabulary management class for mapping tokens to IDs, frequencies, and pruning."""

from collections import Counter
import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union
from zkai.tokenizer.base import SpecialTokens
from zkai.core.logger import get_logger

logger = get_logger("tokenizer.vocabulary")


class Vocabulary:
    """Vocabulary mapping tokens to integer IDs with frequency tracking and pruning."""

    def __init__(self, special_tokens: Optional[SpecialTokens] = None):
        self.special_tokens = special_tokens or SpecialTokens()
        self.token_to_id: Dict[str, int] = {}
        self.id_to_token: Dict[int, str] = {}
        self.token_counts: Counter = Counter()

        for st in self.special_tokens.to_list():
            self.add_token(st, count=0)

    def add_token(self, token: str, count: int = 1) -> int:
        """Adds a token to the vocabulary or increments its frequency count."""
        if token not in self.token_to_id:
            idx = len(self.token_to_id)
            self.token_to_id[token] = idx
            self.id_to_token[idx] = token
        else:
            idx = self.token_to_id[token]
        self.token_counts[token] += count
        return idx

    def prune(self, min_frequency: int = 2, max_vocab_size: Optional[int] = None) -> None:
        """Prunes low-frequency tokens from vocabulary except special tokens."""
        specials = set(self.special_tokens.to_list())
        eligible = [
            (tok, cnt)
            for tok, cnt in self.token_counts.items()
            if tok in specials or cnt >= min_frequency
        ]

        if max_vocab_size is not None and len(eligible) > max_vocab_size:
            special_items = [item for item in eligible if item[0] in specials]
            regular_items = sorted(
                [item for item in eligible if item[0] not in specials],
                key=lambda x: x[1],
                reverse=True,
            )
            eligible = special_items + regular_items[: max_vocab_size - len(special_items)]

        self.token_to_id = {}
        self.id_to_token = {}
        new_counts = Counter()
        for tok, cnt in eligible:
            idx = len(self.token_to_id)
            self.token_to_id[tok] = idx
            self.id_to_token[idx] = tok
            new_counts[tok] = cnt
        self.token_counts = new_counts
        logger.info(f"Vocabulary pruned to size {len(self.token_to_id)}")

    def save(self, file_path: str) -> None:
        """Saves vocabulary state to JSON file."""
        data = {
            "token_to_id": self.token_to_id,
            "token_counts": dict(self.token_counts),
        }
        Path(file_path).write_text(json.dumps(data, indent=2), encoding="utf-8")

    def load(self, file_path: str) -> None:
        """Loads vocabulary state from JSON file."""
        content = json.loads(Path(file_path).read_text(encoding="utf-8"))
        self.token_to_id = content["token_to_id"]
        self.id_to_token = {int(v): k for k, v in self.token_to_id.items()}
        self.token_counts = Counter(content.get("token_counts", {}))

    def __len__(self) -> int:
        return len(self.token_to_id)
