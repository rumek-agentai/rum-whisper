#!/bin/bash
# Hook: SessionStart — inject git context + lessons

if [ -d ".git" ] || git rev-parse --git-dir &>/dev/null 2>&1; then
    echo "=== Git Context ==="
    echo "Branch: $(git branch --show-current 2>/dev/null)"
    echo "Last 5 commits:"
    git log --oneline -5 2>/dev/null
    echo ""
    echo "Uncommitted changes:"
    git status -sb 2>/dev/null | head -20
    echo "==================="
fi

# Inject lessons learned
if [ -f "LESSONS.md" ]; then
    LESSON_COUNT=$(grep -c '^### ' LESSONS.md 2>/dev/null || echo "0")
    if [ "$LESSON_COUNT" -gt 0 ]; then
        echo ""
        echo "=== LESSONS LEARNED ($LESSON_COUNT entries) ==="
        grep -A 1 '^\*\*Prevention rule:\*\*' LESSONS.md 2>/dev/null | grep -v '^--$'
        echo "Full file: LESSONS.md"
        echo "=============================================="
    fi
fi

# Ensure subagent output directory exists
mkdir -p /tmp/rum-coder-output 2>/dev/null
