"""
Whisper transcription engine — wraps faster-whisper for offline inference.

faster-whisper uses CTranslate2 under the hood, providing 4x faster inference
than openai-whisper on CPU with int8 quantization.

Design:
  WhisperEngine is a singleton-style object loaded once at startup.
  It accepts raw float32 audio arrays (16kHz mono) and returns TranscriptSegment
  objects. Thread-safe: inference is serialized via asyncio.Lock.

References:
  https://github.com/SYSTRAN/faster-whisper
"""

from __future__ import annotations

import asyncio
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING

import numpy as np

if TYPE_CHECKING:
    from faster_whisper import WhisperModel as FasterWhisperModel


@dataclass(frozen=True)
class TranscriptSegment:
    """A single transcribed segment returned by WhisperEngine."""

    text: str
    start: float  # Seconds from start of audio window
    end: float  # Seconds from start of audio window
    language: str  # Detected or forced language code (e.g. "en")
    avg_logprob: float  # Confidence indicator (higher = more confident)
    no_speech_prob: float  # Probability that segment contains no speech


class WhisperEngine:
    """
    Offline speech-to-text engine backed by faster-whisper.

    Loads a CTranslate2-converted Whisper model from disk and exposes
    async transcription suitable for use in the GUI event loop.

    Usage::

        engine = WhisperEngine(model_path=Path("models/medium"), device="cpu")
        await engine.load()
        segments = await engine.transcribe(audio_array, language="en")
    """

    def __init__(
        self,
        model_path: Path,
        device: str = "cpu",
        compute_type: str = "int8",
    ) -> None:
        self._model_path = model_path
        self._device = device
        self._compute_type = compute_type
        self._model: FasterWhisperModel | None = None
        self._lock = asyncio.Lock()

    @property
    def is_loaded(self) -> bool:
        """True if the model weights have been loaded into memory."""
        return self._model is not None

    async def load(self) -> None:
        """
        Load the Whisper model into memory (blocking — runs in thread pool).

        Raises:
            FileNotFoundError: If model_path does not exist.
            RuntimeError: If the model format is incompatible.
        """
        raise NotImplementedError

    async def unload(self) -> None:
        """Release model weights and free memory."""
        raise NotImplementedError

    async def transcribe(
        self,
        audio: np.ndarray,
        language: str | None = None,
    ) -> list[TranscriptSegment]:
        """
        Transcribe a float32 audio window.

        Args:
            audio:    float32 numpy array, shape (samples,), 16kHz mono.
            language: BCP-47 code (e.g. "en", "pl") or None for auto-detect.

        Returns:
            List of TranscriptSegment in chronological order.
            Empty list if no speech detected.

        Raises:
            RuntimeError: If engine is not loaded (call load() first).
        """
        raise NotImplementedError
