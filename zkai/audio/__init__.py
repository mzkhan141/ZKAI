"""Audio Processing, Speech-to-Text, Text-to-Speech, VAD, and Recording for ZKAI."""

from zkai.audio.cloning import VoiceCloner
from zkai.audio.emotion import EmotionRecognizer, EmotionResult
from zkai.audio.enhancement import AudioEnhancer
from zkai.audio.language_id import LanguageIDResult, LanguageIdentifier
from zkai.audio.music import MusicGenerator
from zkai.audio.noise import NoiseReducer
from zkai.audio.recorder import AudioRecorder
from zkai.audio.separation import SpeakerSeparator
from zkai.audio.speaker import SpeakerRecognizer
from zkai.audio.stt import SpeechToText
from zkai.audio.streaming import RealTimeStreaming
from zkai.audio.tts import TextToSpeech
from zkai.audio.vad import VoiceActivityDetector

__all__ = [
    "SpeechToText",
    "TextToSpeech",
    "VoiceActivityDetector",
    "AudioRecorder",
    "SpeakerRecognizer",
    "VoiceCloner",
    "NoiseReducer",
    "EmotionRecognizer",
    "EmotionResult",
    "LanguageIdentifier",
    "LanguageIDResult",
    "MusicGenerator",
    "SpeakerSeparator",
    "RealTimeStreaming",
    "AudioEnhancer",
]
