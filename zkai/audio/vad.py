"""Voice Activity Detection (VAD)."""

import numpy as np
from zkai.core.logger import get_logger

logger = get_logger("audio.vad")


class VoiceActivityDetector:
    """Detects active human speech segments in raw audio streams."""

    def __init__(self, threshold: float = 0.5):
        self.threshold = threshold

    def is_speech(self, pcm_chunk: bytes) -> bool:
        """Determines if the audio chunk contains active human speech."""
        data = np.frombuffer(pcm_chunk, dtype=np.int16).astype(np.float32)
        energy = np.mean(np.abs(data)) if len(data) > 0 else 0
        return energy > (self.threshold * 1000.0)
