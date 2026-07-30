"""Memory Compression and Cold Archiving."""

import zlib
import pickle
from typing import Any, List
from zkai.memory.base import MemoryEntry
from zkai.core.logger import get_logger

logger = get_logger("memory.compression")


class MemoryCompressor:
    """Compresses historical memory payloads to optimize memory footprint."""

    @staticmethod
    def compress(entry: MemoryEntry) -> bytes:
        data = pickle.dumps(entry)
        return zlib.compress(data)

    @staticmethod
    def decompress(compressed_data: bytes) -> MemoryEntry:
        raw = zlib.decompress(compressed_data)
        return pickle.loads(raw)


class MemoryArchiver:
    """Cold storage archiver moving stale memories to disk archives."""

    def __init__(self, archive_file: str = "./memory_archive.bin"):
        self.archive_file = archive_file

    def archive(self, entries: List[MemoryEntry]) -> int:
        compressed_blocks = [MemoryCompressor.compress(e) for e in entries]
        with open(self.archive_file, "ab") as f:
            for block in compressed_blocks:
                f.write(len(block).to_bytes(4, byteorder="little"))
                f.write(block)
        logger.info(f"Archived {len(entries)} memory entries to cold storage")
        return len(entries)
