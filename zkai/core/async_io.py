"""AsyncFileReader and AsyncBatchProcessor for non-blocking asynchronous processing."""

import asyncio
from pathlib import Path
from typing import Any, Callable, List, Optional, Union
from zkai.core.logger import get_logger

logger = get_logger("core.async_io")


class AsyncFileReader:
    """Non-blocking asynchronous file reader using asyncio thread executors."""

    def __init__(self, filepath: Union[str, Path]):
        self.filepath = Path(filepath)

    async def read_text_async(self) -> str:
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, self._read_file_sync)

    def _read_file_sync(self) -> str:
        with open(self.filepath, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()


class AsyncBatchProcessor:
    """Asynchronous batch processor executing tasks concurrently across asyncio tasks."""

    def __init__(self, max_concurrency: int = 8):
        self.semaphore = asyncio.Semaphore(max_concurrency)

    async def process_item(self, item: Any, process_fn: Callable[[Any], Any]) -> Any:
        async with self.semaphore:
            if asyncio.iscoroutinefunction(process_fn):
                return await process_fn(item)
            else:
                loop = asyncio.get_running_loop()
                return await loop.run_in_executor(None, process_fn, item)

    async def process_batch_async(self, items: List[Any], process_fn: Callable[[Any], Any]) -> List[Any]:
        tasks = [self.process_item(item, process_fn) for item in items]
        return await asyncio.gather(*tasks)
