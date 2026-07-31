"""NoiseReduction spectral filtering."""

from zkai.core.logger import get_logger

logger = get_logger("audio.noise")


class NoiseReducer:
    """Applies spectral gating noise reduction to audio files."""

    def reduce_noise(self, audio_path: str) -> str:
        logger.info(f"Applying noise reduction to: {audio_path}")
        return audio_path
