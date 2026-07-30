"""Audio Recorder for microphone input streams."""

from pathlib import Path
from zkai.core.logger import get_logger

logger = get_logger("audio.recorder")


class AudioRecorder:
    """Microphone audio input stream recorder."""

    def __init__(self, sample_rate: int = 16000):
        self.sample_rate = sample_rate

    def record(self, duration_seconds: float = 5.0, output_path: str = "recorded.wav") -> str:
        logger.info(f"Recording {duration_seconds}s audio to {output_path}...")
        path = Path(output_path)
        path.touch()
        return str(path)
