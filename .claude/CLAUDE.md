# rum-whisper — Claude Code Project Config

## Project Identity
- **Name:** rum-whisper
- **Type:** Desktop Windows application — offline speech-to-text
- **Inspiration:** Mac Whisper
- **Git identity:** `rum-coder <rum-coder@quasar.us>`
- **Branch:** `rum-coder` (never merge to main — Bartek does that)

## Tech Stack

| Layer | Technology | Version |
|-------|-----------|---------|
| Language | Python | 3.12+ |
| Package manager | uv | latest |
| Audio capture | sounddevice + soundfile | ≥0.4.6 |
| System audio | pyaudiowpatch (WASAPI loopback) | ≥0.2.12 |
| Transcription | faster-whisper (CTranslate2) | ≥1.0.3 |
| Models | Hugging Face Hub | Systran/faster-whisper-medium, large-v3 |
| GUI | customtkinter | ≥5.2.2 |
| Clipboard | pyperclip | ≥1.9.0 |
| Config | pydantic-settings | ≥2.2.1 |
| Tests | pytest | ≥8.2.0 |
| Formatting | black (100 chars) + isort | ≥24.4.0 |
| Linting | ruff + mypy strict | ≥0.4.4 |

## Architecture

```
src/rum_whisper/
├── audio/
│   ├── capture.py    # Mic + system audio via sounddevice/WASAPI
│   └── buffer.py     # Ring buffer, 2-5s chunks for Whisper
├── transcription/
│   ├── engine.py     # faster-whisper wrapper, streaming segments
│   └── models.py     # HuggingFace download, model selection
├── gui/
│   ├── app.py        # Main customtkinter window
│   └── widgets.py    # Custom controls (model selector, etc.)
├── config.py         # Pydantic settings (model, language, buffer size)
├── clipboard.py      # Pyperclip wrapper
├── __main__.py       # Entry point
└── __init__.py
```

## Windows-Specific Notes

- **System audio capture:** WASAPI loopback via pyaudiowpatch. Standard sounddevice does NOT support loopback on Windows.
- **Paths:** Always use `pathlib.Path`, never hardcode `\` separators.
- **Models directory:** Use `platformdirs.user_data_dir("rum-whisper")` for model storage.
- **GPU:** CTranslate2 supports CUDA. Default to CPU, allow GPU if available.
- **Thread safety:** Audio capture runs in a separate thread. Use `queue.Queue` for audio→transcription, `threading.Event` for stop signals. GUI updates via `after()` callback.

## Commit Messages

```
type(scope): description

Optional body: why, what changed, known limitations
```
Types: feat, fix, refactor, test, docs, chore, ci
Scopes: audio, transcription, gui, config, deps

## Token-Efficient CLI (MANDATORY)

| Command | Compact form |
|---------|-------------|
| `git status` | `git status -sb` |
| `git log` | `git log --oneline -n 10` |
| `git diff` | `git diff --stat` (overview first) |
| `git push/pull/commit` | add `--quiet` |
| `pytest` | `pytest -q --tb=short --no-header` |
| `ruff check` | `ruff check --output-format concise --quiet` |
| `ls` | `ls -1` |
| Large files | `head -50` or Read with offset/limit |
| `rg` (search) | `rg -l` (file list) or `rg -m 5` (cap) |
| >50 lines output | pipe `| head -N` |
| git commands | always `--no-pager` |

**Rule:** Before running ANY command that may produce >50 lines, add output limiting.

## Subagent Return Pattern (MANDATORY)

All subagents MUST follow the `DONE|{path}` pattern:

1. Write ALL output to `/tmp/rum-coder-output/{agent}-{slug}.md`
2. Return EXACTLY: `DONE|/tmp/rum-coder-output/{filename}.md`
3. PROHIBITED: summaries, explanations, any text beyond `DONE|{path}`

Include in every subagent task prompt:
```
## OUTPUT INSTRUCTIONS (CRITICAL — Context Preservation)
Return EXACTLY: `DONE|{output_file}` — nothing else.
Write ALL findings to: /tmp/rum-coder-output/{filename}.md
PROHIBITED: summaries or text beyond DONE|{path} in return value.
```

## Self-Improvement Loop (LESSONS.md)

After every corrected mistake:
1. Identify root cause
2. Formulate prevention rule
3. Append to `LESSONS.md` in project root

## Pre-Task Analysis Protocol

Before planning ANY changes:
1. Check if `.claude/PROJECT_ANALYSIS.md` exists
2. If missing → run @project-analyst first
3. If exists → read it, update if needed
4. Sub-agents read `.claude/analysis/{role}.md`

## Impact Analysis Rule

Before modifying any file, sub-agents MUST:
1. `rg` for all usages of functions/classes being changed
2. List affected files under "IMPACT ANALYSIS"
3. Impact > 3 files → STOP and report

## Rules
- Never hardcode credentials — use env vars or pydantic-settings
- Never install new dependencies without checking pyproject.toml first
- Always run tests before committing
- Prefer simple solutions — reliability > cleverness
- Never create a second mechanism for something that already exists
- Read before writing — grep for existing implementations first
- All code must be valid Python 3.12+ with type hints
- No `any` types in mypy strict mode
- GUI operations only on main thread (use `after()` for updates from worker threads)
