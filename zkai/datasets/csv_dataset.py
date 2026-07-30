"""CSVDataset for CSV file tabular data."""

import csv
from pathlib import Path
from typing import List, Optional, Tuple
from zkai.datasets.base import Dataset


class CSVDataset(Dataset):
    """Dataset reading tabular CSV data."""

    def __init__(self, file_path: str, input_col: str = "text", label_col: Optional[str] = "label"):
        self.rows: List[dict] = []
        self.input_col = input_col
        self.label_col = label_col
        with open(file_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            self.rows = list(reader)

    def __len__(self) -> int:
        return len(self.rows)

    def __getitem__(self, idx: int) -> Tuple[str, str]:
        row = self.rows[idx]
        inp = row.get(self.input_col, "")
        lbl = row.get(self.label_col, inp) if self.label_col else inp
        return inp, lbl
