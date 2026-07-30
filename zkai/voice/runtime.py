"""Voice Operating Layer Runtime for ZKAI."""

from dataclasses import dataclass, field
import queue
from typing import Any, Dict, List, Optional
from zkai.audio import SpeechToText, TextToSpeech, VoiceActivityDetector, SpeakerRecognizer
from zkai.security.permissions import PermissionManager
from zkai.core.logger import get_logger

logger = get_logger("voice")


@dataclass
class VoiceProfile:
    user_id: str = "default_user"
    preferred_voice: str = "en-US-Neural"
    wake_word: str = "hey zkai"
    always_listening: bool = False


class WakeWordDetector:
    """Detects configured wake word phrase from continuous audio stream."""

    def __init__(self, keyword: str = "hey zkai"):
        self.keyword = keyword.lower()

    def detect(self, audio_chunk: str) -> bool:
        return self.keyword in audio_chunk.lower()


class VoicePermissionManager:
    """Verifies microphone access capabilities."""

    def __init__(self, permission_manager: Optional[PermissionManager] = None):
        self.pm = permission_manager or PermissionManager()

    def check_microphone_access(self, caller: str) -> bool:
        return self.pm.check(caller, "microphone")


class SpeakerSwitcher:
    """Switches active conversation routing based on speaker identification."""

    def __init__(self):
        self.speaker_recognizer = SpeakerRecognizer()

    def identify_speaker(self, audio_path: str) -> str:
        return self.speaker_recognizer.identify_speaker(audio_path)


class ConversationRouter:
    """Routes transcribed speech to agent or chat model endpoints."""

    def route_utterance(self, utterance: str, speaker_id: str = "user") -> str:
        logger.info(f"Routing utterance from speaker '{speaker_id}': '{utterance}'")
        return f"[Voice Response to '{utterance}']"


class StreamingAudioPipeline:
    """Real-time streaming audio pipeline handling continuous speech frames."""

    def __init__(self):
        self.audio_queue: queue.Queue = queue.Queue()

    def push_chunk(self, chunk: bytes) -> None:
        self.audio_queue.put(chunk)

    def process_chunks(self) -> int:
        count = 0
        while not self.audio_queue.empty():
            self.audio_queue.get()
            count += 1
        return count


class VoiceSession:
    """Stateful voice conversation session supporting interrupt handling."""

    def __init__(self, session_id: str = "voice_session_0"):
        self.session_id = session_id
        self.is_active: bool = False
        self.is_interrupted: bool = False

    def interrupt(self) -> None:
        self.is_interrupted = True
        logger.info(f"VoiceSession '{self.session_id}' interrupted by user.")


class VoiceRuntime:
    """Master Voice Operating Layer Runtime coordinating STT, TTS, VAD, WakeWord, and Session routing."""

    def __init__(self, profile: Optional[VoiceProfile] = None):
        self.profile = profile or VoiceProfile()
        self.stt = SpeechToText()
        self.tts = TextToSpeech()
        self.vad = VoiceActivityDetector()
        self.wake_word = WakeWordDetector(keyword=self.profile.wake_word)
        self.router = ConversationRouter()
        self.speaker_switcher = SpeakerSwitcher()
        self.permissions = VoicePermissionManager()
        self.pipeline = StreamingAudioPipeline()
        self.current_session = VoiceSession()

    def process_voice_input(self, audio_path: str, caller_role: str = "user") -> str:
        if not self.permissions.check_microphone_access(caller_role):
            return "Microphone access denied by security policy."

        speaker = self.speaker_switcher.identify_speaker(audio_path)
        transcript = self.stt.transcribe(audio_path)
        response_text = self.router.route_utterance(transcript, speaker_id=speaker)
        return response_text
