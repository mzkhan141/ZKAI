"""CorpusCleaner providing customizable pipeline for text cleaning, normalization, and quality filtering."""

import re
import unicodedata
from typing import Callable, List, Optional
from zkai.core.logger import get_logger

logger = get_logger("training.corpus_cleaner")


class CorpusCleaner:
    """Text cleaning and normalization pipeline for foundation pretraining corpora."""

    def __init__(
        self,
        lower: bool = False,
        normalize_unicode: bool = True,
        strip_html: bool = True,
        remove_extra_whitespace: bool = True,
        min_length: int = 10,
        max_length: Optional[int] = None,
    ):
        self.lower = lower
        self.normalize_unicode = normalize_unicode
        self.strip_html = strip_html
        self.remove_extra_whitespace = remove_extra_whitespace
        self.min_length = min_length
        self.max_length = max_length
        self.custom_filters: List[Callable[[str], bool]] = []
        self.custom_transforms: List[Callable[[str], str]] = []

    def add_filter(self, filter_fn: Callable[[str], bool]) -> "CorpusCleaner":
        """Adds custom filter function returning True to keep document, False to reject."""
        self.custom_filters.append(filter_fn)
        return self

    def add_transform(self, transform_fn: Callable[[str], str]) -> "CorpusCleaner":
        """Adds custom string transformation function to pipeline."""
        self.custom_transforms.append(transform_fn)
        return self

    def clean_text(self, text: str) -> Optional[str]:
        """Cleans and normalizes a single string, returning None if text fails filters."""
        if not text:
            return None

        cleaned = text

        if self.normalize_unicode:
            cleaned = unicodedata.normalize("NFKC", cleaned)

        if self.strip_html:
            cleaned = re.sub(r"<[^>]+>", "", cleaned)

        if self.lower:
            cleaned = cleaned.lower()

        if self.remove_extra_whitespace:
            cleaned = re.sub(r"\s+", " ", cleaned).strip()

        for transform in self.custom_transforms:
            cleaned = transform(cleaned)

        if len(cleaned) < self.min_length:
            return None

        if self.max_length and len(cleaned) > self.max_length:
            return None

        for filter_fn in self.custom_filters:
            if not filter_fn(cleaned):
                return None

        return cleaned

    def clean_batch(self, texts: List[str]) -> List[str]:
        """Processes a batch of text strings, removing None results."""
        results = []
        for text in texts:
            cleaned = self.clean_text(text)
            if cleaned is not None:
                results.append(cleaned)
        return results
