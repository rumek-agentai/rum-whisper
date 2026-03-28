"""
GUI subsystem for rum-whisper — built with customtkinter.

Provides a modern Windows-native-feeling desktop UI with:
  - Start / Stop recording button
  - Source selector (microphone / system audio)
  - Model selector (medium / large-v3)
  - Language selector (auto-detect + BCP-47 codes)
  - Live transcript text area
  - Copy to clipboard button
  - Save as .txt button
  - Status bar (recording state, model loaded, language detected)

Public API:
    RumWhisperApp — the main application window, run via .mainloop()
"""

from rum_whisper.gui.app import RumWhisperApp

__all__ = ["RumWhisperApp"]
