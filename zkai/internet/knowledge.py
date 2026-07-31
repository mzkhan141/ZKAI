"""KnowledgeExtractor and TextCleaner for web reasoning."""

from typing import List


class TextCleaner:
    """Normalizes raw web scraped text."""

    @staticmethod
    def clean(text: str) -> str:
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        return "\n".join(lines)


class KnowledgeExtractor:
    """Extracts key factual statements and entities from web text."""

    def extract_facts(self, text: str) -> List[str]:
        cleaned = TextCleaner.clean(text)
        sentences = cleaned.split(". ")
        return [s.strip() for s in sentences if len(s.strip()) > 10]
