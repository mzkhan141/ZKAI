"""VideoDataset for video files."""

from pathlib import Path
from typing import List, Tuple
from zkai.datasets.base import Dataset


class VideoDataset(Dataset):
    """Dataset iterating over video clips."""

    def __init__(self, root_dir: str):
        self.root_dir = Path(root_dir)
        self.video_paths = list(self.root_dir.rglob("*.mp4")) + list(self.root_dir.rglob("*.avi"))

    def __len__(self) -> int:
        return len(self.video_paths)

    def __getitem__(self, idx: int) -> Tuple[str, int]:
        return str(self.video_paths[idx]), 0
