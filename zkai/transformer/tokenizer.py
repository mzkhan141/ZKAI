"""Tokenization Engine (Vocabulary, BytePairEncoding, SentencePiece, Tokenizer)."""

from collections import Counter, defaultdict
import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union
from tokenizers import Tokenizer as HFTokenizer
from tokenizers.models import BPE
from tokenizers.trainers import BpeTrainer
from tokenizers.pre_tokenizers import Whitespace
from zkai.core.exceptions import ModelError
from zkai.core.logger import get_logger

logger = get_logger("transformer.tokenizer")


class Vocabulary:
    """Vocabulary mapping tokens to integer IDs and vice-versa."""

    def __init__(self, pad_token: str = "<pad>", unk_token: str = "<unk>", bos_token: str = "<s>", eos_token: str = "</s>"):
        self.pad_token = pad_token
        self.unk_token = unk_token
        self.bos_token = bos_token
        self.eos_token = eos_token

        self.token_to_id: Dict[str, int] = {}
        self.id_to_token: Dict[int, str] = {}

        # Add special tokens
        for token in [pad_token, unk_token, bos_token, eos_token]:
            self.add_token(token)

    def add_token(self, token: str) -> int:
        if token not in self.token_to_id:
            idx = len(self.token_to_id)
            self.token_to_id[token] = idx
            self.id_to_token[idx] = token
            return idx
        return self.token_to_id[token]

    def __len__(self) -> int:
        return len(self.token_to_id)


class BytePairEncoding:
    """Native Byte Pair Encoding (BPE) algorithm for subword vocabulary learning."""

    def __init__(self, vocab_size: int = 1000):
        self.vocab_size = vocab_size
        self.merges: Dict[Tuple[str, str], str] = {}

    def train(self, texts: List[str]) -> None:
        """Learns subword merge rules from text corpus."""
        words = [list(text) + ["</w>"] for text in texts]
        vocab_count = len(set(char for word in words for char in word))

        num_merges = self.vocab_size - vocab_count
        for i in range(max(1, num_merges)):
            pairs = defaultdict(int)
            for word in words:
                for j in range(len(word) - 1):
                    pairs[(word[j], word[j + 1])] += 1
            if not pairs:
                break
            best_pair = max(pairs, key=pairs.get)
            merged_token = "".join(best_pair)
            self.merges[best_pair] = merged_token

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


class Tokenizer:
    """Primary Tokenizer interface exposing encoding, decoding, vocabulary creation, and training."""

    def __init__(self, vocab_size: int = 32000):
        self.vocab_size = vocab_size
        self._hf_tokenizer = HFTokenizer(BPE(unk_token="<unk>"))
        self._hf_tokenizer.pre_tokenizer = Whitespace()

    def train_from_texts(self, texts: List[str]) -> None:
        """Trains tokenization rules directly from a list of strings."""
        trainer = BpeTrainer(vocab_size=self.vocab_size, special_tokens=["<pad>", "<unk>", "<s>", "</s>"])
        self._hf_tokenizer.train_from_iterator(texts, trainer=trainer)
        logger.info(f"Trained tokenizer with vocab size {self._hf_tokenizer.get_vocab_size()}")

    def encode(self, text: str, add_special_tokens: bool = True) -> List[int]:
        """Converts raw string into a list of integer token IDs."""
        encoding = self._hf_tokenizer.encode(text)
        return encoding.ids

    def decode(self, ids: List[int], skip_special_tokens: bool = True) -> str:
        """Converts token IDs back to human-readable string."""
        return self._hf_tokenizer.decode(ids, skip_special_tokens=skip_special_tokens)

    def save(self, file_path: str) -> None:
        """Saves tokenizer state to disk."""
        self._hf_tokenizer.save(file_path)

    def load(self, file_path: str) -> None:
        """Loads tokenizer state from file."""
        self._hf_tokenizer = HFTokenizer.from_file(file_path)
