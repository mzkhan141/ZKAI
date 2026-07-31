"""FileExplorer providing file system navigation, read, write, search, and file dialog APIs."""

from pathlib import Path
from typing import List, Optional
from zkai.core.logger import get_logger

logger = get_logger("computer.file_explorer")


class FileExplorer:
    """File Explorer providing disk navigation, reading, writing, and searching."""

    def list_dir(self, directory: str = ".") -> List[str]:
        path = Path(directory)
        return [str(p) for p in path.iterdir()]

    def read_text(self, file_path: str) -> str:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()

    def write_text(self, file_path: str, content: str) -> str:
        path = Path(file_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        logger.info(f"Wrote file {file_path}")
        return str(path)

    def exists(self, file_path: str) -> bool:
        return Path(file_path).exists()
