"""DocumentParser and FormatDetector."""

from pathlib import Path
from zkai.core.types import DocumentType


class FormatDetector:
    """Detects document format from file extension and header signatures."""

    @staticmethod
    def detect(file_path: str) -> DocumentType:
        suffix = Path(file_path).suffix.lower()
        mapping = {
            ".pdf": DocumentType.PDF,
            ".docx": DocumentType.DOCX,
            ".csv": DocumentType.CSV,
            ".json": DocumentType.JSON,
            ".xml": DocumentType.XML,
            ".html": DocumentType.HTML,
            ".md": DocumentType.MARKDOWN,
            ".py": DocumentType.CODE,
        }
        return mapping.get(suffix, DocumentType.TEXT)


class DocumentParser:
    """Parses raw text and structured payloads from documents."""

    def parse_text(self, raw_content: str) -> str:
        return raw_content.strip()
