"""
Transcription subsystem for rum-whisper.

Wraps faster-whisper (CTranslate2 backend) for offline speech-to-text.
Handles model loading, inference, and result formatting.

Public API:
    WhisperEngine   — loads model, runs transcription on audio windows
    ModelManager    — downloads / validates models from Hugging Face Hub
    TranscriptSegment — typed result from a single transcription call
"""

from rum_whisper.transcription.engine import TranscriptSegment, WhisperEngine
from rum_whisper.transcription.models import ModelManager

__all__ = ["WhisperEngine", "ModelManager", "TranscriptSegment"]
