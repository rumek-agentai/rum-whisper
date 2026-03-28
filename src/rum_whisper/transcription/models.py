"""
Model management — download and validate faster-whisper models from Hugging Face Hub.

Supported models:
  - Systran/faster-whisper-medium   (~1.5 GB, good balance of speed/quality)
  - Systran/faster-whisper-large-v3 (~3.1 GB, highest quality)

Models are stored in `models_dir` (default: %APPDATA%/rum-whisper/models/ on Windows).
Download is skipped if the model directory already contains a valid model.

Uses huggingface_hub.snapshot_download for atomic, resumable downloads.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

# Canonical Hugging Face repo IDs for each model size
MODEL_REPO_IDS: dict[str, str] = {
    "medium": "Systran/faster-whisper-medium",
    "large-v3": "Systran/faster-whisper-large-v3",
}

# Files required for a valid faster-whisper model directory
REQUIRED_MODEL_FILES = frozenset({"model.bin", "config.json", "tokenizer.json", "vocabulary.json"})


@dataclass
class ModelInfo:
    """Metadata about a downloaded model."""

    name: str  # e.g. "medium"
    repo_id: str  # HuggingFace repo, e.g. "Systran/faster-whisper-medium"
    local_path: Path  # Absolute path to model directory
    size_bytes: int  # Approximate total size of model files
    is_valid: bool  # All required files present and non-empty


class ModelManager:
    """
    Manages faster-whisper model lifecycle: discovery, download, validation.

    All network access is isolated here — the rest of the app is offline-only.
    """

    def __init__(self, models_dir: Path) -> None:
        self._models_dir = models_dir

    @property
    def models_dir(self) -> Path:
        """Root directory where models are stored."""
        return self._models_dir

    def list_available(self) -> list[ModelInfo]:
        """
        Return metadata for all locally downloaded models.

        Returns:
            List of ModelInfo, empty if no models downloaded yet.
        """
        raise NotImplementedError

    def is_downloaded(self, model_name: str) -> bool:
        """
        Check if a model is fully downloaded and valid.

        Args:
            model_name: Short name, e.g. "medium" or "large-v3".

        Returns:
            True if the model directory contains all required files.
        """
        raise NotImplementedError

    def get_model_path(self, model_name: str) -> Path:
        """
        Return the local path for a model (whether downloaded or not).

        Args:
            model_name: Short name, e.g. "medium".

        Returns:
            Path to the model directory under models_dir.
        """
        raise NotImplementedError

    async def download(
        self,
        model_name: str,
        progress_callback: "ProgressCallback | None" = None,
    ) -> Path:
        """
        Download a model from Hugging Face Hub (async, resumable).

        Args:
            model_name:        Short name, e.g. "medium" or "large-v3".
            progress_callback: Optional callback(downloaded_bytes, total_bytes).

        Returns:
            Path to the downloaded model directory.

        Raises:
            ValueError:   If model_name is not in MODEL_REPO_IDS.
            DownloadError: If the download fails or is interrupted.
        """
        raise NotImplementedError

    def delete(self, model_name: str) -> None:
        """
        Remove a downloaded model from disk.

        Args:
            model_name: Short name, e.g. "medium".

        Raises:
            ValueError: If model_name is not downloaded.
        """
        raise NotImplementedError


# Type alias for download progress callbacks
ProgressCallback = "Callable[[int, int], None]"


class DownloadError(RuntimeError):
    """Raised when a model download fails."""
