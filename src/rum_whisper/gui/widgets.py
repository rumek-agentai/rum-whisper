"""
Custom widget components for rum-whisper GUI.

Encapsulates reusable UI elements built on customtkinter primitives.
Each widget is a self-contained CTkFrame subclass.

Widgets:
  RecordButton     — animated start/stop button with pulsing indicator
  TranscriptView   — scrollable text area with auto-scroll and search highlight
  ModelSelector    — dropdown + download-status badge
  LanguageSelector — dropdown with flag icons and "Auto-detect" option
  StatusBar        — bottom status strip with state icon + message label
"""

from __future__ import annotations

from typing import Callable


class RecordButton:
    """
    Animated recording toggle button.

    Shows a pulsing red dot while recording is active.
    Calls `on_toggle(is_recording)` on each click.
    """

    def __init__(self, parent: object, on_toggle: Callable[[bool], None]) -> None:
        self._parent = parent
        self._on_toggle = on_toggle
        self._recording = False

    def set_recording(self, recording: bool) -> None:
        """Update visual state to match recording status."""
        raise NotImplementedError

    def build(self) -> None:
        """Construct and place widgets inside parent frame."""
        raise NotImplementedError


class TranscriptView:
    """
    Scrollable read-only text area for displaying live transcription.

    Supports appending new segments, clearing, and selecting all for copy.
    Auto-scrolls to bottom when new text arrives (unless user scrolled up).
    """

    def __init__(self, parent: object) -> None:
        self._parent = parent

    def append(self, text: str) -> None:
        """
        Append a transcribed segment to the view.

        Args:
            text: Transcript text to append. A newline is added automatically.
        """
        raise NotImplementedError

    def clear(self) -> None:
        """Remove all transcript text."""
        raise NotImplementedError

    def get_all(self) -> str:
        """Return the full transcript text."""
        raise NotImplementedError

    def build(self) -> None:
        """Construct and place widgets inside parent frame."""
        raise NotImplementedError


class ModelSelector:
    """
    Dropdown widget for selecting the active Whisper model.

    Shows download status (downloaded / not downloaded / downloading) next
    to each option. Triggers download if a non-downloaded model is selected.
    """

    def __init__(
        self,
        parent: object,
        on_change: Callable[[str], None],
    ) -> None:
        self._parent = parent
        self._on_change = on_change

    def set_options(self, models: list[str], downloaded: set[str]) -> None:
        """Populate dropdown with available model names and their download state."""
        raise NotImplementedError

    def get_selected(self) -> str:
        """Return currently selected model name."""
        raise NotImplementedError

    def build(self) -> None:
        """Construct and place widgets inside parent frame."""
        raise NotImplementedError


class LanguageSelector:
    """
    Dropdown widget for selecting transcription language.

    First option is always "Auto-detect" (maps to language=None).
    Remaining options are BCP-47 language codes with human-readable labels.
    """

    LANGUAGES: dict[str, str] = {
        "auto": "Auto-detect",
        "en": "English",
        "pl": "Polish",
        "de": "German",
        "fr": "French",
        "es": "Spanish",
        "it": "Italian",
        "pt": "Portuguese",
        "ru": "Russian",
        "zh": "Chinese",
        "ja": "Japanese",
        "ko": "Korean",
    }

    def __init__(
        self,
        parent: object,
        on_change: Callable[[str | None], None],
    ) -> None:
        self._parent = parent
        self._on_change = on_change

    def get_selected_code(self) -> str | None:
        """Return the selected BCP-47 code, or None for auto-detect."""
        raise NotImplementedError

    def build(self) -> None:
        """Construct and place widgets inside parent frame."""
        raise NotImplementedError


class StatusBar:
    """
    Bottom status strip showing current app state and messages.

    Displays a colored state icon (idle / recording / processing / error)
    and a free-form message string.
    """

    def __init__(self, parent: object) -> None:
        self._parent = parent

    def set_message(self, message: str, state: str = "idle") -> None:
        """
        Update status bar text and icon.

        Args:
            message: Human-readable status message.
            state:   One of "idle", "recording", "processing", "error".
        """
        raise NotImplementedError

    def build(self) -> None:
        """Construct and place widgets inside parent frame."""
        raise NotImplementedError
