"""SpeakerSeparation and audio source separation."""

from typing import List
from zkai.core.logger import get_logger

logger = get_logger("audio.separation")


class SpeakerSeparator:
    """Separates overlapping speakers or vocal tracks into isolated stems."""

    def separate_speakers(self, audio_path: str) -> List[str]:
        logger.info(f"Separating vocal channels in: {audio_path}")
        return [f"{audio_path}_stem0.wav", f"{audio_path}_stem1.wav"]
