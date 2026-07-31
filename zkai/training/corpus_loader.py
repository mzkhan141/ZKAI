"""CorpusLoader for reading, parsing, and streaming raw text corpora across formats."""

import json
import os
from pathlib import Path
from typing import Any, Generator, List, Optional, Union
from zkai.core.exceptions import TrainingError
from zkai.core.logger import get_logger

logger = get_logger("training.corpus_loader")


class CorpusLoader:
    """Multi-format raw corpus loader supporting text, JSONL, CSV, Parquet, and directory trees."""

    def __init__(self, path: Union[str, Path], file_pattern: str = "*"):
        self.path = Path(path)
        self.file_pattern = file_pattern

    def load_documents(self) -> List[str]:
        """Loads all documents from file or directory into a list of strings."""
        if not self.path.exists():
            raise TrainingError(f"Corpus path does not exist: {self.path}")

        documents: List[str] = []
        if self.path.is_file():
            documents.extend(self._load_single_file(self.path))
        elif self.path.is_dir():
            for file_path in sorted(self.path.glob(self.file_pattern)):
                if file_path.is_file():
                    documents.extend(self._load_single_file(file_path))
        return documents

    def stream_documents(self) -> Generator[str, None, None]:
        """Streams documents iteratively without loading entire dataset into memory."""
        if not self.path.exists():
            raise TrainingError(f"Corpus path does not exist: {self.path}")

        if self.path.is_file():
            yield from self._stream_single_file(self.path)
        elif self.path.is_dir():
            for file_path in sorted(self.path.glob(self.file_pattern)):
                if file_path.is_file():
                    yield from self._stream_single_file(file_path)

    def _load_single_file(self, filepath: Path) -> List[str]:
        ext = filepath.suffix.lower()
        if ext in [".txt", ".raw"]:
            with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
                return [content] if content.strip() else []
        elif ext == ".jsonl":
            docs = []
            with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                for line in f:
                    if line.strip():
                        obj = json.loads(line)
                        text = obj.get("text") or obj.get("content") or str(obj)
                        docs.append(text)
            return docs
        elif ext == ".json":
            with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                data = json.load(f)
                if isinstance(data, list):
                    return [d.get("text") or d.get("content") or str(d) if isinstance(d, dict) else str(d) for d in data]
                elif isinstance(data, dict):
                    return [data.get("text") or data.get("content") or str(data)]
                return [str(data)]
        elif ext == ".csv":
            import csv
            docs = []
            with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    text = row.get("text") or row.get("content") or " ".join(row.values())
                    docs.append(text)
            return docs
        else:
            with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                return [f.read()]

    def _stream_single_file(self, filepath: Path) -> Generator[str, None, None]:
        ext = filepath.suffix.lower()
        if ext in [".txt", ".raw"]:
            with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                for line in f:
                    if line.strip():
                        yield line.strip()
        elif ext == ".jsonl":
            with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                for line in f:
                    if line.strip():
                        obj = json.loads(line)
                        text = obj.get("text") or obj.get("content") or str(obj)
                        yield text
        else:
            for doc in self._load_single_file(filepath):
                yield doc
