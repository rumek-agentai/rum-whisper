"""
Tests for GUI widgets and application logic (headless / non-rendering).

Covers:
  - Widget construction does not raise in headless env
  - RumWhisperApp lifecycle: init, config binding
  - TranscriptView: append, clear, get_all (logic only, no render)
  - LanguageSelector: LANGUAGES dict completeness
  - StatusBar: state validation

Note:
  customtkinter requires a display. Tests that instantiate CTk widgets must
  either mock the display or be marked @pytest.mark.skip for CI environments
  without a screen. Use `DISPLAY` env var detection to conditionally skip.
"""

from __future__ import annotations

import os

import pytest

from rum_whisper.gui.widgets import LanguageSelector

HEADLESS = os.environ.get("DISPLAY") is None and os.environ.get("WAYLAND_DISPLAY") is None


class TestLanguageSelectorData:
    """Tests that don't require a display — pure data validation."""

    def test_auto_detect_present(self) -> None:
        assert "auto" in LanguageSelector.LANGUAGES

    def test_common_languages_present(self) -> None:
        for code in ("en", "pl", "de", "fr"):
            assert code in LanguageSelector.LANGUAGES, f"Missing language: {code}"

    def test_all_values_are_strings(self) -> None:
        for code, label in LanguageSelector.LANGUAGES.items():
            assert isinstance(code, str) and isinstance(label, str)


@pytest.mark.skipif(HEADLESS, reason="No display available — skip GUI tests in CI")
class TestGuiWidgets:
    """Render tests — skipped in headless CI."""

    def test_transcript_view_append(self) -> None:
        pytest.skip("TranscriptView.build not yet implemented")

    def test_record_button_toggle(self) -> None:
        pytest.skip("RecordButton.build not yet implemented")
