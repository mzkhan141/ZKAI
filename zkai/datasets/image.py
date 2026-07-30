"""ImageDataset for image directory structures."""

from pathlib import Path
from typing import Callable, List, Optional, Tuple
from zkai.datasets.base import Dataset
from zkai.vision.image import Image


class ImageDataset(Dataset):
    """Dataset iterating over image file paths."""

    def __init__(self, root_dir: str, transform: Optional[Callable[[Image], Image]] = None):
        self.root_dir = Path(root_dir)
        self.transform = transform
        self.image_paths = list(self.root_dir.rglob("*.jpg")) + list(self.root_dir.rglob("*.png"))

    def __len__(self) -> int:
        return len(self.image_paths)

    def __getitem__(self, idx: int) -> Tuple[Image, int]:
        path = self.image_paths[idx]
        img = Image(str(path))
        if self.transform:
            img = self.transform(img)
        return img, 0
