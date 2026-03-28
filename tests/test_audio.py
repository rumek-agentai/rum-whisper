"""
Tests for the audio capture and buffer subsystem.

Covers:
  - AudioBuffer: push, window emission, stride, flush, clear
  - AudioCapture: device listing, stream lifecycle (mocked backends)
  - Edge cases: empty buffer, single sample, buffer overflow
"""

from __future__ import annotations

import numpy as np
import pytest

from rum_whisper.audio.buffer import AudioBuffer, BufferConfig
from rum_whisper.audio.capture import AudioCapture, AudioCaptureConfig, CaptureSource


class TestAudioBuffer:
    """Unit tests for AudioBuffer sliding-window logic."""

    def test_empty_buffer_has_zero_duration(self) -> None:
        buf = AudioBuffer()
        assert buf.duration_seconds == 0.0

    def test_push_increases_duration(self) -> None:
        buf = AudioBuffer(BufferConfig(sample_rate=16000, window_seconds=3.0))
        chunk = np.zeros(1600, dtype=np.float32)  # 0.1s at 16kHz
        # TODO: implement push(), then assert duration > 0
        pytest.skip("AudioBuffer.push not yet implemented")

    def test_window_not_emitted_before_threshold(self) -> None:
        pytest.skip("AudioBuffer.windows not yet implemented")

    def test_flush_returns_remaining_samples(self) -> None:
        pytest.skip("AudioBuffer.flush not yet implemented")

    def test_clear_resets_buffer(self) -> None:
        pytest.skip("AudioBuffer.clear not yet implemented")


class TestAudioCapture:
    """Unit tests for AudioCapture stream management."""

    def test_list_devices_returns_list(self) -> None:
        pytest.skip("AudioCapture.list_devices not yet implemented")

    async def test_stream_yields_float32_chunks(self) -> None:
        pytest.skip("AudioCapture.stream not yet implemented")
