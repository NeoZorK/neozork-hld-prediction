#!/bin/bash
# Script for incremental git push when dealing with large number of changes

set -e

BRANCH="${1:-v0.5.8}"
REMOTE="${2:-origin}"

echo "Starting incremental push for branch: $BRANCH to $REMOTE"
echo "This will attempt to push in smaller chunks..."

# Get the base commit (common ancestor)
BASE=$(git merge-base $BRANCH ${REMOTE}/$BRANCH 2>/dev/null || echo "")

if [ -z "$BASE" ]; then
    echo "No common ancestor found. This is a force push situation."
    echo "Attempting direct force push..."
    git push --force $REMOTE $BRANCH
    exit $?
fi

# Get list of commits to push
COMMITS=$(git rev-list ${BASE}..$BRANCH)

COMMIT_COUNT=$(echo "$COMMITS" | wc -l | tr -d ' ')
echo "Found $COMMIT_COUNT commits to push"

if [ "$COMMIT_COUNT" -eq 0 ]; then
    echo "No commits to push"
    exit 0
fi

# Try to push in batches
BATCH_SIZE=100
BATCH_NUM=0

echo "$COMMITS" | while IFS= read -r commit; do
    if [ -z "$commit" ]; then
        continue
    fi
    
    # Try to push up to this commit
    echo "Attempting to push commit batch..."
    if git push $REMOTE $commit:refs/heads/$BRANCH 2>/dev/null; then
        echo "Successfully pushed batch"
    else
        echo "Batch push failed, trying force push for this commit range..."
        git push --force $REMOTE $commit:refs/heads/$BRANCH || {
            echo "Force push also failed. Trying full force push..."
            git push --force $REMOTE $BRANCH
            exit $?
        }
    fi
done

echo "Incremental push completed"

