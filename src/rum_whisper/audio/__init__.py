"""
Audio subsystem for rum-whisper.

Provides microphone and system audio (WASAPI loopback) capture,
plus sliding buffer management for real-time transcription.

Public API:
    AudioCapture  — start/stop recording, yields audio chunks
    AudioBuffer   — accumulates chunks into fixed-length numpy windows
"""

from rum_whisper.audio.buffer import AudioBuffer
from rum_whisper.audio.capture import AudioCapture

__all__ = ["AudioCapture", "AudioBuffer"]
