"""
Main application window for rum-whisper.

Owns the customtkinter root window and orchestrates all subsystems:
  - Starts/stops the audio capture loop
  - Feeds audio windows to the transcription engine
  - Appends transcript segments to the text widget
  - Manages app lifecycle (config load, model load, graceful shutdown)

Architecture note:
  The GUI runs on the main thread via Tk's event loop.
  Audio capture and transcription run in a background asyncio event loop
  (asyncio.run_coroutine_threadsafe). Results are delivered back to the GUI
  thread via CTk's .after() callback.
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from rum_whisper.config import AppConfig


class RumWhisperApp:
    """
    Root application window.

    Owns the customtkinter CTk root, all child widgets, and coordinates
    the audio → transcription pipeline in a background thread.

    Usage::

        config = load_config()
        app = RumWhisperApp(config)
        app.mainloop()
    """

    def __init__(self, config: "AppConfig") -> None:
        self._config = config
        # ctk.CTk root — initialized in _build_ui
        self._root: object | None = None

    def mainloop(self) -> None:
        """Build the UI and start the Tk event loop. Blocks until window closes."""
        raise NotImplementedError

    def _build_ui(self) -> None:
        """Construct all widgets and layout. Called once before mainloop."""
        raise NotImplementedError

    def _on_record_toggle(self) -> None:
        """Handle Start/Stop recording button click."""
        raise NotImplementedError

    def _on_copy(self) -> None:
        """Copy transcript text to clipboard."""
        raise NotImplementedError

    def _on_save(self) -> None:
        """Open save-file dialog and write transcript to .txt."""
        raise NotImplementedError

    def _on_model_change(self, model_name: str) -> None:
        """Handle model selector change — unload current, load new model."""
        raise NotImplementedError

    def _on_language_change(self, language_code: str) -> None:
        """Update transcription language. Takes effect on next window."""
        raise NotImplementedError

    def _append_transcript(self, text: str) -> None:
        """
        Thread-safe: append a transcript segment to the text widget.

        Must be called via CTk's .after() from background threads.
        """
        raise NotImplementedError

    def _update_status(self, message: str) -> None:
        """Update the status bar label text."""
        raise NotImplementedError

    def _on_close(self) -> None:
        """Graceful shutdown: stop recording, unload model, destroy window."""
        raise NotImplementedError
