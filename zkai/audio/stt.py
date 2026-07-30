"""Speech to Text (STT) wrapping OpenAI Whisper with fallback."""

from zkai.core.logger import get_logger

try:
    import whisper
except ImportError:
    whisper = None

logger = get_logger("audio.stt")


class SpeechToText:
    """Speech-to-Text transcription engine powered by Whisper with fallback."""

    def __init__(self, model_name: str = "base"):
        self.model = whisper.load_model(model_name) if whisper else None

    def transcribe(self, audio_file_path: str) -> str:
        """Transcribes an audio file into text."""
        logger.info(f"Transcribing audio file {audio_file_path}...")
        if self.model:
            result = self.model.transcribe(audio_file_path)
            return result.get("text", "")
        return f"[Transcribed audio signal from {audio_file_path}]"
