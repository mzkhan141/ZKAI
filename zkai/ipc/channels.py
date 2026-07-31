"""SharedMemoryChannel, StreamingChannel, and BroadcastChannel for ZKAI IPC."""

import asyncio
from typing import Any, AsyncGenerator, Callable, List, Optional
from zkai.ipc.bus import IPCMessage, SystemMessageBus
from zkai.core.logger import get_logger

logger = get_logger("ipc.channels")


class SharedMemoryChannel:
    """Zero-copy buffer channel abstraction for inter-process data sharing."""

    def __init__(self, name: str, size: int = 1048576):
        self.name = name
        self.size = size
        self._buffer: bytearray = bytearray(size)

    def write(self, data: bytes) -> int:
        length = min(len(data), self.size)
        self._buffer[:length] = data[:length]
        return length

    def read(self, length: Optional[int] = None) -> bytes:
        l = length if length is not None else self.size
        return bytes(self._buffer[:l])


class StreamingChannel:
    """Async generator-based streaming channel for token and audio streaming across processes."""

    def __init__(self, capacity: int = 100):
        self.capacity = capacity
        self._queue: asyncio.Queue = asyncio.Queue(maxsize=capacity)

    async def send(self, item: Any) -> None:
        await self._queue.put(item)

    async def stream(self) -> AsyncGenerator[Any, None]:
        while True:
            item = await self._queue.get()
            if item is None:  # Sentinel end token
                break
            yield item

    async def close(self) -> None:
        await self._queue.put(None)


class BroadcastChannel:
    """One-to-many broadcast channel delivering messages to multiple subscriber endpoints."""

    def __init__(self, channel_name: str, bus: Optional[SystemMessageBus] = None):
        self.channel_name = channel_name
        self.bus = bus or SystemMessageBus()

    def broadcast(self, payload: Any) -> None:
        msg = IPCMessage(topic=f"broadcast_{self.channel_name}", payload=payload)
        self.bus.publish_message(msg)

    def subscribe(self, handler: Callable[[Any], None]) -> None:
        def _wrapper(msg: IPCMessage):
            handler(msg.payload)

        self.bus.subscribe_topic(f"broadcast_{self.channel_name}", _wrapper)
