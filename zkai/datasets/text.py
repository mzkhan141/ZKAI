"""TextDataset for text file corpora."""

from pathlib import Path
from typing import List, Tuple, Union
from zkai.datasets.base import Dataset


class TextDataset(Dataset):
    """Dataset reading line-delimited text documents."""

    def __init__(self, file_path_or_lines: Union[str, List[str]]):
        if isinstance(file_path_or_lines, str):
            self.lines = Path(file_path_or_lines).read_text(encoding="utf-8").splitlines()
        else:
            self.lines = file_path_or_lines

    def __len__(self) -> int:
        return len(self.lines)

    def __getitem__(self, idx: int) -> Tuple[str, str]:
        line = self.lines[idx]
        return line, line
