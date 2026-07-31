"""RealTimeStreaming audio processor."""

from typing import Callable
from zkai.core.logger import get_logger

logger = get_logger("audio.streaming")


class RealTimeStreaming:
    """Processes real-time audio input stream chunks."""

    def __init__(self, callback: Callable[[bytes], None]):
        self.callback = callback

    def process_chunk(self, chunk: bytes) -> None:
        self.callback(chunk)
