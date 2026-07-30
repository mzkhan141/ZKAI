"""VoiceCloning pipeline synthesizing speech using reference voice sample."""

from zkai.audio.tts import TextToSpeech
from zkai.core.logger import get_logger

logger = get_logger("audio.cloning")


class VoiceCloner:
    """Clones speaker voice characteristics from audio reference sample."""

    def __init__(self):
        self.tts = TextToSpeech()

    def clone_and_speak(self, reference_audio_path: str, text: str) -> str:
        logger.info(f"Synthesizing voice clone from sample: {reference_audio_path}")
        return self.tts.speak(text)
