"""StreamingCorpus for memory-efficient iteration over massive dataset corpora."""

import random
from typing import Callable, Generator, Iterable, List, Optional
from zkai.training.corpus_loader import CorpusLoader
from zkai.training.corpus_cleaner import CorpusCleaner
from zkai.core.logger import get_logger

logger = get_logger("training.streaming_corpus")


class StreamingCorpus(Iterable[str]):
    """Memory-efficient streaming iterator supporting sharding, shuffling, and cleaning."""

    def __init__(
        self,
        loader: CorpusLoader,
        cleaner: Optional[CorpusCleaner] = None,
        buffer_size: int = 10000,
        shuffle: bool = True,
        shard_id: int = 0,
        num_shards: int = 1,
    ):
        self.loader = loader
        self.cleaner = cleaner
        self.buffer_size = buffer_size
        self.shuffle = shuffle
        self.shard_id = shard_id
        self.num_shards = max(1, num_shards)

    def __iter__(self) -> Generator[str, None, None]:
        buffer: List[str] = []
        doc_count = 0

        for doc in self.loader.stream_documents():
            doc_count += 1
            if (doc_count - 1) % self.num_shards != self.shard_id:
                continue

            if self.cleaner:
                cleaned = self.cleaner.clean_text(doc)
                if cleaned is None:
                    continue
                doc = cleaned

            buffer.append(doc)

            if len(buffer) >= self.buffer_size:
                if self.shuffle:
                    random.shuffle(buffer)
                for item in buffer:
                    yield item
                buffer.clear()

        if buffer:
            if self.shuffle:
                random.shuffle(buffer)
            for item in buffer:
                yield item
            buffer.clear()
