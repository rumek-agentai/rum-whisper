"""
Audio capture module — microphone and system audio (WASAPI loopback).

Supports two backends:
  - PyAudioWPatch (WASAPI): required for system/loopback capture on Windows
  - sounddevice: fallback for microphone-only capture

Design:
  AudioCapture is a context manager. On __enter__ it opens the audio stream.
  Captured frames are pushed into a queue consumed by AudioBuffer.
  On __exit__ the stream is stopped and the queue is closed.
"""

from __future__ import annotations

import asyncio
from dataclasses import dataclass, field
from enum import Enum
from typing import AsyncIterator

import numpy as np


class CaptureSource(str, Enum):
    """Audio capture source selection."""

    MICROPHONE = "microphone"
    LOOPBACK = "loopback"  # System audio (speakers) via WASAPI


@dataclass
class AudioDevice:
    """Represents an available audio input/output device."""

    index: int
    name: str
    channels: int
    sample_rate: float
    is_loopback: bool = False


@dataclass
class AudioCaptureConfig:
    """Configuration for the audio capture stream."""

    source: CaptureSource = CaptureSource.MICROPHONE
    sample_rate: int = 16000
    channels: int = 1
    chunk_ms: int = 100  # Milliseconds per captured chunk
    device_index: int | None = None


class AudioCapture:
    """
    Manages the audio capture stream.

    Usage::

        async with AudioCapture(config) as capture:
            async for chunk in capture.stream():
                buffer.push(chunk)
    """

    def __init__(self, config: AudioCaptureConfig) -> None:
        self._config = config
        self._queue: asyncio.Queue[np.ndarray] = asyncio.Queue(maxsize=64)
        self._running = False

    async def __aenter__(self) -> "AudioCapture":
        """Open the audio stream."""
        raise NotImplementedError

    async def __aexit__(self, *_: object) -> None:
        """Stop the audio stream and flush the queue."""
        raise NotImplementedError

    async def stream(self) -> AsyncIterator[np.ndarray]:
        """
        Yield captured audio chunks as float32 numpy arrays.

        Yields:
            np.ndarray: Shape (samples,), dtype float32, range [-1.0, 1.0].
        """
        raise NotImplementedError
        yield np.array([])  # type: ignore[misc]  # unreachable — satisfies AsyncIterator

    @staticmethod
    def list_devices() -> list[AudioDevice]:
        """
        Return all available audio devices, including WASAPI loopback targets.

        Returns:
            List of AudioDevice sorted by index.
        """
        raise NotImplementedError
