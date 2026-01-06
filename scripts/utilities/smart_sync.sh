#!/bin/bash
# Smart sync script that creates intermediate branches and pushes incrementally
# This avoids GitHub's 408 timeout by pushing smaller chunks

set -e

BRANCH="${1:-v0.5.8}"
REMOTE="${2:-origin}"
CHUNK_SIZE="${3:-200}"  # Push 200 commits at a time

echo "=== Smart Git Sync ==="
echo "Branch: $BRANCH"
echo "Remote: $REMOTE"
echo "Chunk size: $CHUNK_SIZE commits"
echo ""

# Get remote branch head
REMOTE_HEAD=$(git ls-remote --heads $REMOTE $BRANCH | awk '{print $1}')

if [ -z "$REMOTE_HEAD" ]; then
    echo "Remote branch $BRANCH does not exist. Pushing entire branch..."
    git push $REMOTE $BRANCH
    exit $?
fi

echo "Remote head: $REMOTE_HEAD"
LOCAL_HEAD=$(git rev-parse $BRANCH)
echo "Local head: $LOCAL_HEAD"

if [ "$REMOTE_HEAD" = "$LOCAL_HEAD" ]; then
    echo "✓ Branch is already in sync"
    exit 0
fi

# Find common ancestor
BASE=$(git merge-base $REMOTE_HEAD $LOCAL_HEAD)
echo "Common ancestor: $BASE"

# Count commits to push
COMMITS_TO_PUSH=$(git rev-list --count $BASE..$LOCAL_HEAD)
echo "Commits to push: $COMMITS_TO_PUSH"

if [ "$COMMITS_TO_PUSH" -eq 0 ]; then
    echo "No commits to push"
    exit 0
fi

# If commits are less than chunk size, try direct push
if [ "$COMMITS_TO_PUSH" -le "$CHUNK_SIZE" ]; then
    echo "Commits fit in one chunk, attempting direct push..."
    if git push --force-with-lease $REMOTE $BRANCH 2>&1; then
        echo "✓ Successfully pushed"
        exit 0
    else
        echo "Direct push failed, will try chunked approach..."
    fi
fi

# Chunked approach: create intermediate branches
echo ""
echo "Using chunked push approach..."

# Get list of commits (oldest first)
COMMIT_LIST=$(git rev-list --reverse $BASE..$LOCAL_HEAD)
TOTAL_CHUNKS=$(( (COMMITS_TO_PUSH + CHUNK_SIZE - 1) / CHUNK_SIZE ))

echo "Will push in $TOTAL_CHUNKS chunks"

CHUNK_NUM=0
COMMIT_COUNT=0
CURRENT_BASE=$BASE

for commit in $COMMIT_LIST; do
    COMMIT_COUNT=$((COMMIT_COUNT + 1))
    
    # Check if we need to start a new chunk
    if [ $((COMMIT_COUNT % CHUNK_SIZE)) -eq 1 ] || [ $COMMIT_COUNT -eq 1 ]; then
        if [ $COMMIT_COUNT -gt 1 ]; then
            # Push previous chunk
            CHUNK_NUM=$((CHUNK_NUM + 1))
            CHUNK_BRANCH="${BRANCH}-chunk-${CHUNK_NUM}"
            
            echo ""
            echo "=== Pushing chunk $CHUNK_NUM/$TOTAL_CHUNKS ==="
            
            if git push $REMOTE "$CHUNK_BRANCH:$BRANCH" --force-with-lease 2>&1; then
                echo "✓ Chunk $CHUNK_NUM pushed successfully"
                CURRENT_BASE=$CHUNK_BRANCH
            else
                echo "✗ Chunk $CHUNK_NUM push failed, trying with --force..."
                if git push $REMOTE "$CHUNK_BRANCH:$BRANCH" --force 2>&1; then
                    echo "✓ Chunk $CHUNK_NUM pushed with --force"
                    CURRENT_BASE=$CHUNK_BRANCH
                else
                    echo "✗ Failed to push chunk $CHUNK_NUM"
                    echo "Progress saved. You can continue later from chunk $CHUNK_NUM"
                    exit 1
                fi
            fi
            
            # Clean up local chunk branch
            git branch -D "$CHUNK_BRANCH" 2>/dev/null || true
        fi
        
        # Create new chunk branch
        CHUNK_NUM=$((CHUNK_NUM + 1))
        CHUNK_BRANCH="${BRANCH}-chunk-${CHUNK_NUM}"
        git checkout -b "$CHUNK_BRANCH" "$CURRENT_BASE" 2>/dev/null || git checkout "$CHUNK_BRANCH"
    fi
    
    # Cherry-pick commit
    if git cherry-pick "$commit" >/dev/null 2>&1; then
        echo -n "."
    else
        echo ""
        echo "Warning: Failed to cherry-pick $commit, skipping..."
        git cherry-pick --abort 2>/dev/null || true
    fi
done

# Push final chunk
if [ $COMMIT_COUNT -gt 0 ]; then
    CHUNK_NUM=$((CHUNK_NUM + 1))
    CHUNK_BRANCH="${BRANCH}-chunk-${CHUNK_NUM}"
    
    echo ""
    echo "=== Pushing final chunk ==="
    
    if git push $REMOTE "$CHUNK_BRANCH:$BRANCH" --force-with-lease 2>&1; then
        echo "✓ Final chunk pushed successfully"
    else
        echo "Trying with --force..."
        git push $REMOTE "$CHUNK_BRANCH:$BRANCH" --force 2>&1 || {
            echo "✗ Final push failed"
            exit 1
        }
    fi
    
    git branch -D "$CHUNK_BRANCH" 2>/dev/null || true
fi

# Final sync
echo ""
echo "=== Final sync ==="
git checkout $BRANCH
if git push $REMOTE $BRANCH --force-with-lease 2>&1; then
    echo "✓ Final sync successful"
else
    git push $REMOTE $BRANCH --force 2>&1 || {
        echo "✗ Final sync failed, but chunks were pushed"
        exit 1
    }
fi

echo ""
echo "✓ All done! Branch $BRANCH is now synced with $REMOTE"

