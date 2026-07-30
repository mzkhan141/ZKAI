"""Unicode normalization and text cleaning utilities for tokenization."""

import re
import unicodedata
from typing import Optional


class UnicodeNormalizer:
    """Unicode normalizer handling NFC, NFD, NFKC, NFKD, accent removal, and whitespace normalization."""

    def __init__(
        self,
        form: str = "NFKC",
        lowercase: bool = False,
        strip_accents: bool = False,
        clean_whitespace: bool = True,
    ):
        self.form = form
        self.lowercase = lowercase
        self.strip_accents = strip_accents
        self.clean_whitespace = clean_whitespace

    def normalize(self, text: str) -> str:
        """Normalizes string based on configuration."""
        if not text:
            return ""

        if self.clean_whitespace:
            text = re.sub(r"\s+", " ", text).strip()

        if self.lowercase:
            text = text.lower()

        if self.form in ("NFC", "NFD", "NFKC", "NFKD"):
            text = unicodedata.normalize(self.form, text)

        if self.strip_accents:
            nfd = unicodedata.normalize("NFD", text)
            text = "".join(c for c in nfd if unicodedata.category(c) != "Mn")

        return text
