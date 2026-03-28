# rum-whisper

Offline speech-to-text desktop application for Windows — inspired by Mac Whisper.

Records from microphone or system audio, transcribes in real-time using
[faster-whisper](https://github.com/SYSTRAN/faster-whisper) with locally stored models.
No cloud. No API keys. 100% offline.

---

## Features

- **Dual audio source:** Microphone OR system audio (speakers/loopback via WASAPI)
- **Real-time transcription:** Sliding 2–5 second buffers feed the Whisper engine continuously
- **faster-whisper backend:** CTranslate2-optimized — 4× faster than openai-whisper on CPU
- **Offline models:** `medium` (default, ~1.5 GB) and `large-v3` (~3.1 GB) from Hugging Face
- **Language support:** Auto-detect + manual selection (EN, PL, DE, FR, ES, IT, PT, RU, ZH, JA, KO)
- **Simple GUI:** customtkinter — start/stop, model selector, language selector, live transcript
- **Copy to clipboard:** One click to copy full transcript
- **Save as .txt:** Export transcript to file
- **No internet required:** After model download, fully air-gapped capable

---

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Language | Python 3.12+ |
| Package manager | [uv](https://github.com/astral-sh/uv) |
| Audio capture | sounddevice + PyAudioWPatch (WASAPI loopback) |
| Transcription | [faster-whisper](https://github.com/SYSTRAN/faster-whisper) |
| ML backend | CTranslate2 (int8 quantization) |
| Models | Hugging Face Hub — `Systran/faster-whisper-{medium,large-v3}` |
| GUI | [customtkinter](https://github.com/TomSchimansky/CustomTkinter) |
| Config | pydantic-settings |

---

## Requirements

- Windows 10 / 11 (64-bit)
- Python 3.12+
- [uv](https://docs.astral.sh/uv/getting-started/installation/) package manager
- ~2 GB disk space for `medium` model (or ~4 GB for `large-v3`)

---

## Setup

### 1. Clone and install dependencies

```bash
git clone https://github.com/quasar-it/rum-whisper.git
cd rum-whisper
uv sync
```

### 2. Download a model

```bash
# Download medium model (~1.5 GB) — recommended
uv run python -c "
from huggingface_hub import snapshot_download
snapshot_download('Systran/faster-whisper-medium', local_dir='models/medium')
"

# Or large-v3 for higher quality (~3.1 GB)
uv run python -c "
from huggingface_hub import snapshot_download
snapshot_download('Systran/faster-whisper-large-v3', local_dir='models/large-v3')
"
```

### 3. Run

```bash
uv run rum-whisper
```

Or:

```bash
uv run python -m rum_whisper
```

---

## Configuration

Environment variables (prefix `RUM_WHISPER_`):

| Variable | Default | Description |
|----------|---------|-------------|
| `RUM_WHISPER_MODEL` | `medium` | Model size: `medium` or `large-v3` |
| `RUM_WHISPER_LANGUAGE` | _(auto)_ | BCP-47 code, e.g. `en`, `pl` |
| `RUM_WHISPER_DEVICE` | `cpu` | `cpu` or `cuda` |
| `RUM_WHISPER_COMPUTE_TYPE` | `int8` | CTranslate2 compute type |
| `RUM_WHISPER_BUFFER_SECONDS` | `3.0` | Transcription window length |
| `RUM_WHISPER_MODELS_DIR` | `models/` | Path to downloaded models |
| `RUM_WHISPER_THEME` | `dark` | GUI theme: `dark`, `light`, `system` |

---

## Development

### Run tests

```bash
uv run pytest -q --tb=short --no-header
```

With coverage:

```bash
uv run pytest -q --tb=short --no-header --cov=src/rum_whisper --cov-report=term-missing
```

### Lint & format

```bash
uv run ruff check --output-format concise src/ tests/
uv run black --check src/ tests/
uv run isort --check-only src/ tests/
uv run mypy src/
```

### Project structure

```
src/rum_whisper/
├── audio/          # Capture (mic + WASAPI loopback) + sliding buffer
├── transcription/  # faster-whisper engine wrapper + model management
├── gui/            # customtkinter main window + widgets
├── config.py       # pydantic-settings AppConfig
└── clipboard.py    # pyperclip wrapper
```

### Contributing with Claude Code

This project uses Claude Code with specialized subagents:

| Agent | File | Domain |
|-------|------|--------|
| audio-engine | `.claude/agents/audio-engine.md` | Audio capture + buffer |
| transcription | `.claude/agents/transcription.md` | Whisper engine + models |
| gui | `.claude/agents/gui.md` | customtkinter UI |
| tester | `.claude/agents/tester.md` | Test suite |

Run `@project-analyst` before any significant change to update `.claude/PROJECT_ANALYSIS.md`.

---

## License

MIT — see LICENSE file.

---

*Built with [Claude Code](https://claude.ai/code) by Quasar IT*
