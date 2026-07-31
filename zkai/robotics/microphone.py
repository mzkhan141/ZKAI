"""RobotMicrophone audio sensor device."""

from typing import Optional
from zkai.audio.recorder import AudioRecorder
from zkai.core.logger import get_logger

logger = get_logger("robotics.microphone")


class RobotMicrophone(AudioRecorder):
    """Microphone sensor for robotics acoustic perception."""

    def __init__(self, sample_rate: int = 16000):
        super().__init__(sample_rate=sample_rate)

    def listen_chunk(self, duration_sec: float = 1.0) -> str:
        return self.record(duration_seconds=duration_sec)
