#!/bin/bash
# Complete workflow script for translating Russian words in files
# Usage: ./run_translation_workflow.sh [max_files]

set -e

MAX_FILES="${1:-10}"
WORDS_FILE="/tmp/russian_words_workflow.txt"
CACHE_FILE=".translation_cache.json"

echo "=========================================="
echo "RUSSIAN WORDS TRANSLATION WORKFLOW"
echo "=========================================="
echo ""

# Step 1: Extract Russian words
echo "Step 1: Extracting Russian words from files..."
uv run python3 scripts/utilities/count_russian_files.py \
    --words-output "$WORDS_FILE" \
    --words-from-lines-only \
    --summary-only

if [ ! -f "$WORDS_FILE" ]; then
    echo "Error: Words file not created"
    exit 1
fi

echo "✓ Words extracted to $WORDS_FILE"
echo ""

# Step 2: Translate and replace
echo "Step 2: Translating words and replacing in files..."
uv run python3 scripts/utilities/translate_words_workflow.py \
    --words-file "$WORDS_FILE" \
    --cache-file "$CACHE_FILE" \
    --max-files "$MAX_FILES" \
    --batch-size 50 \
    --delay 0.1 \
    --yes

echo ""
echo "=========================================="
echo "Workflow completed!"
echo "=========================================="
echo ""
echo "To continue with more files, run:"
echo "  ./run_translation_workflow.sh 20"
echo ""

