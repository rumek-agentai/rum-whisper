"""
Clipboard operations for rum-whisper.

Wraps pyperclip to copy transcribed text to the system clipboard.
Handles platform quirks (Windows: no additional backend needed).
"""

from __future__ import annotations


def copy_to_clipboard(text: str) -> None:
    """
    Copy the given text to the system clipboard.

    Args:
        text: The transcribed text to copy.

    Raises:
        ClipboardError: If pyperclip cannot access the clipboard.
    """
    raise NotImplementedError


def get_from_clipboard() -> str:
    """
    Read current clipboard contents.

    Returns:
        The text currently held in the clipboard.
    """
    raise NotImplementedError


class ClipboardError(RuntimeError):
    """Raised when clipboard access fails."""
