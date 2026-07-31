"""CSVLogger for persistent metrics logging to CSV."""

import csv
from pathlib import Path
from typing import Dict


class CSVLogger:
    """Logs epoch metrics to CSV file."""

    def __init__(self, file_path: str = "training_metrics.csv"):
        self.file_path = Path(file_path)
        self.header_written = False

    def log_epoch(self, epoch: int, metrics: Dict[str, float]) -> None:
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        row = {"epoch": epoch, **metrics}
        fieldnames = list(row.keys())
        with open(self.file_path, "a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            if not self.header_written and not self.file_path.exists():
                writer.writeheader()
                self.header_written = True
            writer.writerow(row)
