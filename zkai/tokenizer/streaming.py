"""Streaming tokenizer for real-time and incremental text tokenization."""

from typing import Generator, List, Optional
from zkai.tokenizer.base import EncodingResult, TokenizerBase
from zkai.tokenizer.bpe import BytePairTokenizer


class StreamingTokenizer:
    """Processes streaming text inputs and yields token IDs incrementally."""

    def __init__(self, tokenizer: Optional[TokenizerBase] = None):
        self.tokenizer = tokenizer or BytePairTokenizer()
        self._buffer = ""

    def feed(self, chunk: str) -> List[int]:
        """Feeds a chunk of incoming text and returns newly finalized token IDs."""
        self._buffer += chunk
        words = self._buffer.split(" ")
        if len(words) > 1:
            complete_text = " ".join(words[:-1])
            self._buffer = words[-1]
            enc = self.tokenizer.encode(complete_text, add_special_tokens=False)
            return enc.ids
        return []

    def flush(self) -> List[int]:
        """Flushes remaining buffered text into final token IDs."""
        if self._buffer:
            enc = self.tokenizer.encode(self._buffer, add_special_tokens=False)
            self._buffer = ""
            return enc.ids
        return []
