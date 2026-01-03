#!/bin/bash
# Script for partial git push when dealing with large number of changes
# This creates intermediate branches and pushes them incrementally

set -e

BRANCH="${1:-v0.5.8}"
REMOTE="${2:-origin}"
BATCH_SIZE="${3:-500}"  # Push in batches of 500 commits

echo "Starting partial push for branch: $BRANCH to $REMOTE"
echo "Batch size: $BATCH_SIZE commits"

# Get the base commit (common ancestor)
BASE=$(git merge-base $BRANCH ${REMOTE}/$BRANCH 2>/dev/null || git rev-list --max-parents=0 $BRANCH | head -1)

if [ -z "$BASE" ]; then
    echo "Error: Could not find base commit"
    exit 1
fi

echo "Base commit: $BASE"

# Get list of commits to push (in reverse order - oldest first)
COMMITS=$(git rev-list --reverse ${BASE}..$BRANCH)
TOTAL_COMMITS=$(echo "$COMMITS" | wc -l | tr -d ' ')

echo "Total commits to push: $TOTAL_COMMITS"

if [ "$TOTAL_COMMITS" -eq 0 ]; then
    echo "No commits to push"
    exit 0
fi

# Calculate number of batches
BATCH_COUNT=$(( (TOTAL_COMMITS + BATCH_SIZE - 1) / BATCH_SIZE ))
echo "Will push in $BATCH_COUNT batches"

# Create temporary branch for incremental pushes
TEMP_BRANCH="${BRANCH}-partial-push-$$"
CURRENT_BRANCH=$(git branch --show-current)

# Start from base
git checkout -b "$TEMP_BRANCH" "$BASE" 2>/dev/null || git checkout "$TEMP_BRANCH"

BATCH_NUM=0
COMMIT_INDEX=0

echo "$COMMITS" | while IFS= read -r commit; do
    if [ -z "$commit" ]; then
        continue
    fi
    
    COMMIT_INDEX=$((COMMIT_INDEX + 1))
    
    # Cherry-pick this commit
    if git cherry-pick "$commit" >/dev/null 2>&1; then
        echo "Cherry-picked commit $COMMIT_INDEX/$TOTAL_COMMITS: $(git log -1 --oneline $commit)"
    else
        echo "Warning: Failed to cherry-pick commit $commit, skipping..."
        git cherry-pick --abort 2>/dev/null || true
        continue
    fi
    
    # Push every BATCH_SIZE commits
    if [ $((COMMIT_INDEX % BATCH_SIZE)) -eq 0 ] || [ $COMMIT_INDEX -eq $TOTAL_COMMITS ]; then
        BATCH_NUM=$((BATCH_NUM + 1))
        echo ""
        echo "=== Pushing batch $BATCH_NUM/$BATCH_COUNT (commits 1-$COMMIT_INDEX) ==="
        
        if git push $REMOTE "$TEMP_BRANCH:$BRANCH" --force-with-lease 2>&1; then
            echo "✓ Successfully pushed batch $BATCH_NUM"
        else
            echo "✗ Failed to push batch $BATCH_NUM"
            echo "Trying with --force..."
            if git push $REMOTE "$TEMP_BRANCH:$BRANCH" --force 2>&1; then
                echo "✓ Successfully pushed batch $BATCH_NUM with --force"
            else
                echo "✗ Failed to push even with --force"
                echo "Stopping. Current state saved in branch $TEMP_BRANCH"
                exit 1
            fi
        fi
    fi
done

# Final push to ensure everything is synced
echo ""
echo "=== Final sync ==="
git checkout "$BRANCH" 2>/dev/null || true
if git push $REMOTE "$BRANCH" --force-with-lease 2>&1; then
    echo "✓ Final sync successful"
    # Clean up temp branch
    git branch -D "$TEMP_BRANCH" 2>/dev/null || true
    git checkout "$CURRENT_BRANCH" 2>/dev/null || true
    exit 0
else
    echo "Final sync failed, but partial progress saved in $TEMP_BRANCH"
    exit 1
fi

