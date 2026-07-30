"""ParquetDataset for Apache Parquet files."""

from pathlib import Path
from typing import Any, List, Tuple
from zkai.datasets.base import Dataset


class ParquetDataset(Dataset):
    """Dataset reading Apache Parquet format files with fallback."""

    def __init__(self, file_path: str):
        self.rows: List[dict] = []
        try:
            import pyarrow.parquet as pq
            table = pq.read_table(file_path)
            self.rows = table.to_pylist()
        except ImportError:
            self.rows = [{"data": "pyarrow required for parquet format"}]

    def __len__(self) -> int:
        return len(self.rows)

    def __getitem__(self, idx: int) -> Tuple[Any, Any]:
        row = self.rows[idx]
        return row, row
