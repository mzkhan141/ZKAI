"""Unit tests for Dataset Engine subsystem."""

import pytest
from zkai.datasets import (
    DataLoader,
    FolderDataset,
    JSONDataset,
    LazyDataset,
    PaddingCollator,
    RandomSampler,
    StreamingDataset,
    TextDataset,
)


def test_text_dataset():
    ds = TextDataset(["line 1", "line 2", "line 3"])
    assert len(ds) == 3
    x, y = ds[0]
    assert x == "line 1"


def test_mapped_filtered_dataset():
    ds = TextDataset(["apple", "banana", "cherry"])
    mapped = ds.map(lambda item: (item[0].upper(), item[1]))
    assert mapped[0][0] == "APPLE"

    filtered = ds.filter(lambda item: "a" in item[0])
    assert len(filtered) == 2


def test_json_dataset(tmp_path):
    json_file = tmp_path / "data.jsonl"
    json_file.write_text('{"text": "hello", "label": "world"}\n', encoding="utf-8")
    ds = JSONDataset(str(json_file))
    assert len(ds) == 1
    x, y = ds[0]
    assert x == "hello"
    assert y == "world"


def test_dataloader():
    ds = TextDataset(["a", "b", "c", "d"])
    loader = DataLoader(ds, batch_size=2)
    assert len(loader) == 2
