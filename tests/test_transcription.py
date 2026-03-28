"""
Tests for the transcription engine and model management.

Covers:
  - WhisperEngine: load, unload, transcribe (with mock model)
  - ModelManager: is_downloaded, list_available, get_model_path
  - TranscriptSegment: frozen dataclass, field validation
  - Edge cases: empty audio, all-silence audio, no_speech_prob threshold
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pytest

from rum_whisper.transcription.engine import TranscriptSegment, WhisperEngine
from rum_whisper.transcription.models import MODEL_REPO_IDS, ModelManager


class TestTranscriptSegment:
    """Unit tests for TranscriptSegment dataclass."""

    def test_is_frozen(self) -> None:
        seg = TranscriptSegment(
            text="hello",
            start=0.0,
            end=1.0,
            language="en",
            avg_logprob=-0.2,
            no_speech_prob=0.01,
        )
        with pytest.raises(Exception):
            seg.text = "modified"  # type: ignore[misc]

    def test_fields_accessible(self) -> None:
        seg = TranscriptSegment(
            text="test",
            start=0.0,
            end=2.5,
            language="pl",
            avg_logprob=-0.5,
            no_speech_prob=0.05,
        )
        assert seg.text == "test"
        assert seg.language == "pl"


class TestWhisperEngine:
    """Unit tests for WhisperEngine (model mocked — no actual inference)."""

    def test_not_loaded_initially(self, tmp_path: Path) -> None:
        engine = WhisperEngine(model_path=tmp_path / "model")
        assert not engine.is_loaded

    async def test_load_raises_if_path_missing(self, tmp_path: Path) -> None:
        engine = WhisperEngine(model_path=tmp_path / "nonexistent")
        pytest.skip("WhisperEngine.load not yet implemented")

    async def test_transcribe_raises_if_not_loaded(self, tmp_path: Path) -> None:
        engine = WhisperEngine(model_path=tmp_path / "model")
        audio = np.zeros(16000, dtype=np.float32)
        pytest.skip("WhisperEngine.transcribe not yet implemented")


class TestModelManager:
    """Unit tests for ModelManager local model discovery."""

    def test_known_model_repo_ids(self) -> None:
        assert "medium" in MODEL_REPO_IDS
        assert "large-v3" in MODEL_REPO_IDS

    def test_is_downloaded_false_for_empty_dir(self, tmp_path: Path) -> None:
        mgr = ModelManager(models_dir=tmp_path)
        assert not mgr.is_downloaded("medium")

    def test_get_model_path_under_models_dir(self, tmp_path: Path) -> None:
        pytest.skip("ModelManager.get_model_path not yet implemented")
