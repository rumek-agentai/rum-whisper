"""
Application configuration for rum-whisper.

Loads settings from environment variables and/or a JSON config file stored at
%APPDATA%\\rum-whisper\\config.json (Windows) via platformdirs.

Settings are validated with pydantic-settings and are immutable at runtime.
"""

from __future__ import annotations

from enum import Enum
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class WhisperModel(str, Enum):
    """Available faster-whisper model sizes."""

    MEDIUM = "medium"
    LARGE_V3 = "large-v3"


class AudioBackend(str, Enum):
    """Audio capture backend selection."""

    WASAPI = "wasapi"  # PyAudioWPatch — loopback-capable, Windows only
    SOUNDDEVICE = "sounddevice"  # Cross-platform fallback


class AppConfig(BaseSettings):
    """
    Top-level application configuration.

    All fields can be overridden via environment variables prefixed with
    RUM_WHISPER_ (e.g. RUM_WHISPER_MODEL=large-v3).
    """

    model_config = SettingsConfigDict(
        env_prefix="RUM_WHISPER_",
        env_file=".env",
        env_file_encoding="utf-8",
    )

    # Transcription
    model: WhisperModel = Field(default=WhisperModel.MEDIUM, description="Whisper model size")
    language: str | None = Field(
        default=None, description="BCP-47 language code, None = auto-detect"
    )
    device: str = Field(default="cpu", description="Inference device: cpu or cuda")
    compute_type: str = Field(default="int8", description="CTranslate2 compute type")

    # Audio
    audio_backend: AudioBackend = Field(default=AudioBackend.WASAPI)
    buffer_seconds: float = Field(
        default=3.0, ge=1.0, le=10.0, description="Sliding buffer length in seconds"
    )
    sample_rate: int = Field(default=16000, description="Audio sample rate expected by Whisper")
    channels: int = Field(default=1, description="Mono capture")

    # Paths
    models_dir: Path = Field(
        default=Path("models"),
        description="Directory where downloaded model weights are stored",
    )
    output_dir: Path = Field(
        default=Path("."),
        description="Default directory for saved .txt transcripts",
    )

    # GUI
    theme: str = Field(
        default="dark", description="customtkinter color theme: dark / light / system"
    )
    font_size: int = Field(default=14)


def load_config() -> AppConfig:
    """Load and validate application configuration."""
    raise NotImplementedError
