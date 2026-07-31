"""Tests for Voice Operating Layer."""

import pytest
from zkai.voice.runtime import VoiceRuntime, WakeWordDetector, VoiceSession


def test_wake_word_detector():
    ww = WakeWordDetector(keyword="hey zkai")
    assert ww.detect("Hello world hey zkai please help me") is True
    assert ww.detect("Hello world") is False


def test_voice_runtime_and_session():
    vr = VoiceRuntime()
    res = vr.process_voice_input("dummy_audio.wav", caller_role="admin")
    assert "[Voice Response" in res

    sess = VoiceSession("test_session")
    assert sess.is_interrupted is False
    sess.interrupt()
    assert sess.is_interrupted is True
