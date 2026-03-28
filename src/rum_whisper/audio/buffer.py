"""
Audio buffer management for real-time transcription.

Implements a sliding-window buffer that accumulates audio chunks from the
capture stream and emits fixed-length windows to the transcription engine.

Window strategy:
  - Buffer fills to `window_seconds` of audio
  - Emits the full window for transcription
  - Advances by `stride_seconds` (overlap allows better context at boundaries)
  - Drops oldest samples when buffer exceeds `max_seconds`
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterator

import numpy as np


@dataclass
class BufferConfig:
    """Configuration for the sliding audio buffer."""

    sample_rate: int = 16000
    window_seconds: float = 3.0  # Length of each transcription window
    stride_seconds: float = 1.5  # Advance between consecutive windows (50% overlap)
    max_seconds: float = 10.0  # Maximum buffer size before forced flush


class AudioBuffer:
    """
    Thread-safe sliding window buffer for audio samples.

    Accumulates float32 audio chunks and yields fixed-length numpy arrays
    suitable for passing directly to WhisperEngine.transcribe().
    """

    def __init__(self, config: BufferConfig | None = None) -> None:
        self._config = config or BufferConfig()
        self._samples: np.ndarray = np.array([], dtype=np.float32)

    @property
    def duration_seconds(self) -> float:
        """Current buffer length in seconds."""
        return len(self._samples) / self._config.sample_rate

    def push(self, chunk: np.ndarray) -> None:
        """
        Append a captured audio chunk to the buffer.

        Args:
            chunk: float32 array of audio samples.
        """
        raise NotImplementedError

    def windows(self) -> Iterator[np.ndarray]:
        """
        Yield ready transcription windows and advance the buffer.

        Yields:
            np.ndarray: float32 array of shape (window_samples,).
        """
        raise NotImplementedError

    def flush(self) -> np.ndarray | None:
        """
        Return and clear all remaining samples (e.g. at stop).

        Returns:
            Remaining audio as float32 array, or None if buffer is empty.
        """
        raise NotImplementedError

    def clear(self) -> None:
        """Reset the buffer to empty state."""
        raise NotImplementedError
