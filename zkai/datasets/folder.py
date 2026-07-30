"""FolderDataset for auto-detecting dataset contents from directories."""

from pathlib import Path
from typing import List, Tuple
from zkai.datasets.base import Dataset


class FolderDataset(Dataset):
    """Dataset scanning folder recursively for supported dataset files."""

    def __init__(self, folder_path: str):
        self.folder = Path(folder_path)
        self.files = [p for p in self.folder.rglob("*") if p.is_file()]

    def __len__(self) -> int:
        return len(self.files)

    def __getitem__(self, idx: int) -> Tuple[str, str]:
        path = self.files[idx]
        return str(path), path.suffix
