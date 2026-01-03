#!/bin/bash
# Incremental Git Sync Script
# Commits and pushes changes in small batches to avoid timeouts

set -e

BRANCH="${1:-$(git branch --show-current)}"
REMOTE="${2:-origin}"
BATCH_SIZE="${3:-20}"  # Number of files per commit
DELAY="${4:-5}"  # Delay between pushes in seconds
MAX_RETRIES="${5:-3}"  # Max retries per push

echo "=========================================="
echo "Incremental Git Sync Script"
echo "=========================================="
echo "Branch: $BRANCH"
echo "Remote: $REMOTE"
echo "Batch size: $BATCH_SIZE files per commit"
echo "Delay between pushes: $DELAY seconds"
echo "Max retries per push: $MAX_RETRIES"
echo ""

# Check if we're in a git repository
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo "❌ Error: Not in a git repository"
    exit 1
fi

# Get list of modified files (both staged and unstaged)
MODIFIED_FILES=$(git status --short | grep -E '^[AM]' | awk '{print $2}')
# Also include unstaged modified files
UNSTAGED_FILES=$(git status --short | grep -E '^ M' | awk '{print $2}')
# Combine both lists
if [ -n "$UNSTAGED_FILES" ]; then
    if [ -n "$MODIFIED_FILES" ]; then
        MODIFIED_FILES=$(echo -e "$MODIFIED_FILES\n$UNSTAGED_FILES" | sort -u)
    else
        MODIFIED_FILES="$UNSTAGED_FILES"
    fi
fi

if [ -z "$MODIFIED_FILES" ]; then
    echo "✓ No modified files to commit"
    exit 0
fi

TOTAL_FILES=$(echo "$MODIFIED_FILES" | wc -l | tr -d ' ')
echo "Found $TOTAL_FILES modified files"
echo ""

# Function to push with retry
push_with_retry() {
    local retry_count=0
    local success=0
    
    while [ $retry_count -lt $MAX_RETRIES ]; do
        if git push "$REMOTE" "$BRANCH"; then
            success=1
            break
        else
            retry_count=$((retry_count + 1))
            if [ $retry_count -lt $MAX_RETRIES ]; then
                echo "⚠️  Push failed, retrying ($retry_count/$MAX_RETRIES)..."
                sleep 2
            fi
        fi
    done
    
    if [ $success -eq 0 ]; then
        echo "❌ Failed to push after $MAX_RETRIES retries"
        return 1
    fi
    
    return 0
}

# Process files in batches
BATCH_NUM=1
FILE_COUNT=0
BATCH_FILES=()

while IFS= read -r file; do
    BATCH_FILES+=("$file")
    FILE_COUNT=$((FILE_COUNT + 1))
    
    if [ $FILE_COUNT -ge $BATCH_SIZE ]; then
        echo "=========================================="
        echo "Processing batch $BATCH_NUM ($FILE_COUNT files)"
        echo "=========================================="
        
        # Stage files in this batch
        for batch_file in "${BATCH_FILES[@]}"; do
            echo "  + $batch_file"
            git add "$batch_file"
        done
        
        # Commit
        COMMIT_MSG="chore: translate files to English (batch $BATCH_NUM)"
        if git commit -m "$COMMIT_MSG"; then
            echo "✓ Committed batch $BATCH_NUM"
        else
            echo "⚠️  No changes to commit in batch $BATCH_NUM"
        fi
        
        # Push with retry
        if push_with_retry; then
            echo "✓ Pushed batch $BATCH_NUM"
        else
            echo "❌ Failed to push batch $BATCH_NUM"
            exit 1
        fi
        
        # Reset for next batch
        BATCH_FILES=()
        FILE_COUNT=0
        BATCH_NUM=$((BATCH_NUM + 1))
        
        # Delay before next batch (except for last batch)
        if [ $FILE_COUNT -lt $BATCH_SIZE ] && [ -n "$(git status --short | grep -E '^[AM]')" ]; then
            echo "Waiting $DELAY seconds before next batch..."
            sleep $DELAY
        fi
    fi
done <<< "$MODIFIED_FILES"

# Process remaining files
if [ ${#BATCH_FILES[@]} -gt 0 ]; then
    echo "=========================================="
    echo "Processing final batch $BATCH_NUM (${#BATCH_FILES[@]} files)"
    echo "=========================================="
    
    for batch_file in "${BATCH_FILES[@]}"; do
        echo "  + $batch_file"
        git add "$batch_file"
    done
    
    COMMIT_MSG="chore: translate files to English (final batch)"
    if git commit -m "$COMMIT_MSG"; then
        echo "✓ Committed final batch"
    else
        echo "⚠️  No changes to commit in final batch"
    fi
    
    if push_with_retry; then
        echo "✓ Pushed final batch"
    else
        echo "❌ Failed to push final batch"
        exit 1
    fi
fi

# Final status check
echo ""
echo "=========================================="
echo "Sync Complete!"
echo "=========================================="
git status --short
echo ""
echo "✓ All changes have been committed and pushed"

