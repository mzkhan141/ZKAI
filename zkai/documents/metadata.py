"""MetadataExtractor for documents."""

from typing import Dict, Any
from zkai.documents.document import Document


class MetadataExtractor:
    """Extracts summary metadata, word count, line count, and structural metrics from Document objects."""

    @staticmethod
    def extract(doc: Document) -> Dict[str, Any]:
        text = doc.content
        lines = text.splitlines()
        words = text.split()

        return {
            "char_count": len(text),
            "word_count": len(words),
            "line_count": len(lines),
            "doc_type": doc.doc_type.value,
            "file_path": doc.file_path,
        }
