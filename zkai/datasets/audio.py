"""AudioDataset for audio files."""

from pathlib import Path
from typing import List, Tuple
from zkai.datasets.base import Dataset


class AudioDataset(Dataset):
    """Dataset iterating over audio files (wav, mp3, flac)."""

    def __init__(self, root_dir: str):
        self.root_dir = Path(root_dir)
        self.audio_paths = list(self.root_dir.rglob("*.wav")) + list(self.root_dir.rglob("*.mp3"))

    def __len__(self) -> int:
        return len(self.audio_paths)

    def __getitem__(self, idx: int) -> Tuple[str, int]:
        return str(self.audio_paths[idx]), 0
