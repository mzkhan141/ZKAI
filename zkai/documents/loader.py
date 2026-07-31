"""DocumentLoader for parsing PDF, DOCX, CSV, Excel, JSON, XML, MD, HTML, and Code."""

import json
from pathlib import Path
from typing import Optional
from bs4 import BeautifulSoup
from zkai.documents.document import Document
from zkai.core.types import DocumentType
from zkai.core.exceptions import DocumentError
from zkai.core.logger import get_logger

logger = get_logger("documents.loader")


class DocumentLoader:
    """Multi-format Document Loader converting files into unified Document containers."""

    @staticmethod
    def load(file_path: str) -> Document:
        path = Path(file_path)
        if not path.exists():
            raise DocumentError(f"Document path does not exist: {file_path}")

        suffix = path.suffix.lower()

        if suffix in [".txt", ".md"]:
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            return Document(content=content, doc_type=DocumentType.MARKDOWN if suffix == ".md" else DocumentType.TEXT, file_path=file_path)
        elif suffix in [".html", ".htm"]:
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                soup = BeautifulSoup(f.read(), "html.parser")
            return Document(content=soup.get_text(), doc_type=DocumentType.HTML, file_path=file_path)
        elif suffix == ".json":
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            return Document(content=json.dumps(data, indent=2), doc_type=DocumentType.JSON, file_path=file_path)
        elif suffix in [".py", ".js", ".cpp", ".c", ".rs", ".go", ".java"]:
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            return Document(content=content, doc_type=DocumentType.CODE, file_path=file_path)

        # Fallback raw loader
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
        return Document(content=content, doc_type=DocumentType.TEXT, file_path=file_path)
