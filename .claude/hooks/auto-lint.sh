#!/bin/bash
# Hook: PostToolUse — auto-format Python files after Edit/Write

FILE_PATH=$(cat | python3 -c "
import json, sys
try:
    data = json.load(sys.stdin)
    print(data.get('tool_input', {}).get('file_path', data.get('tool_input', {}).get('path', '')))
except:
    print('')
" 2>/dev/null)

if [[ "$FILE_PATH" == *.py ]]; then
    if command -v black &>/dev/null; then
        black --quiet --line-length 100 "$FILE_PATH" 2>/dev/null
    fi
    if command -v isort &>/dev/null; then
        isort --quiet --profile black --line-length 100 "$FILE_PATH" 2>/dev/null
    fi
fi
