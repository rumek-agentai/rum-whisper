#!/bin/bash
# Hook: PreToolUse — block edits to sensitive files

# Read the file path from stdin JSON
FILE_PATH=$(cat | python3 -c "
import json, sys
try:
    data = json.load(sys.stdin)
    print(data.get('tool_input', {}).get('file_path', data.get('tool_input', {}).get('path', '')))
except:
    print('')
" 2>/dev/null)

# Protected patterns
BLOCKED_PATTERNS=(
    "*.env"
    "*.env.*"
    "*.pem"
    "*.key"
    "*.p12"
    "*.pfx"
)

for pattern in "${BLOCKED_PATTERNS[@]}"; do
    if [[ "$FILE_PATH" == $pattern ]]; then
        python3 -c "
import json, sys
print(json.dumps({
    'hookSpecificOutput': {
        'hookEventName': 'PreToolUse',
        'permissionDecision': 'deny',
        'permissionDecisionReason': 'Protected file pattern: $pattern'
    }
}))
"
        exit 0
    fi
done
