"""TokenStreamer and StreamingGeneration providing token streaming abstractions."""

import queue
from typing import AsyncGenerator, Generator, Optional
from zkai.core.logger import get_logger

logger = get_logger("transformer.token_streamer")


class TokenStreamer:
    """Thread-safe queue-backed token streamer for streaming inference."""

    def __init__(self, timeout: float = 10.0):
        self.queue: queue.Queue = queue.Queue()
        self.timeout = timeout
        self._stop_signal = object()

    def put(self, token_text: str) -> None:
        """Pushes new decoded token string into queue."""
        self.queue.put(token_text)

    def end(self) -> None:
        """Pushes stop sentinel signal into queue."""
        self.queue.put(self._stop_signal)

    def __iter__(self) -> Generator[str, None, None]:
        while True:
            try:
                item = self.queue.get(timeout=self.timeout)
                if item is self._stop_signal:
                    break
                yield item
            except queue.Empty:
                break


class StreamingGeneration:
    """High-level token generator providing sync and async streaming wrappers."""

    def __init__(self, streamer: TokenStreamer):
        self.streamer = streamer

    def stream_sync(self) -> Generator[str, None, None]:
        yield from self.streamer

    async def stream_async(self) -> AsyncGenerator[str, None]:
        import asyncio
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = None

        while True:
            try:
                if loop and loop.is_running():
                    item = await loop.run_in_executor(None, lambda: self.streamer.queue.get(timeout=self.streamer.timeout))
                else:
                    item = self.streamer.queue.get(timeout=self.streamer.timeout)
                if item is self.streamer._stop_signal:
                    break
                yield item
            except queue.Empty:
                break
