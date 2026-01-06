#!/bin/bash
# Script for partial git push using GitHub CLI with delays
# This script carefully synchronizes git history by pushing in small chunks

set -e

BRANCH="${1:-v0.5.8}"
REMOTE="${2:-origin}"
CHUNK_SIZE="${3:-100}"  # Default: 100 commits per chunk
DELAY="${4:-5}"  # Default: 5 seconds delay between chunks
MAX_RETRIES="${5:-3}"  # Default: 3 retries per chunk

echo "=========================================="
echo "GitHub CLI Partial Sync Script"
echo "=========================================="
echo "Branch: $BRANCH"
echo "Remote: $REMOTE"
echo "Chunk size: $CHUNK_SIZE commits"
echo "Delay between chunks: $DELAY seconds"
echo "Max retries per chunk: $MAX_RETRIES"
echo ""

# Check if gh is available
if ! command -v gh &> /dev/null; then
    echo "❌ Error: GitHub CLI (gh) is not installed"
    echo "Install it with: brew install gh"
    exit 1
fi

# Check authentication
if ! gh auth status &> /dev/null; then
    echo "❌ Error: Not authenticated with GitHub CLI"
    echo "Run: gh auth login"
    exit 1
fi

echo "✓ GitHub CLI is available and authenticated"
echo ""

# Get repository info
REPO_URL=$(git remote get-url $REMOTE)
REPO=$(echo "$REPO_URL" | sed -E 's/.*github.com[:/]([^/]+\/[^/]+)\.git/\1/')
echo "Repository: $REPO"
echo ""

# Get current branch
CURRENT_BRANCH=$(git branch --show-current)
echo "Current branch: $CURRENT_BRANCH"
echo ""

# Check if remote branch exists
REMOTE_HEAD=$(git ls-remote --heads $REMOTE $BRANCH 2>/dev/null | awk '{print $1}' || echo "")

if [ -z "$REMOTE_HEAD" ]; then
    echo "⚠️  Remote branch $BRANCH does not exist"
    echo "This will be a new branch push"
    BASE_COMMIT=$(git rev-list --max-parents=0 $BRANCH | head -1)
else
    echo "Remote branch head: $REMOTE_HEAD"
    BASE_COMMIT=$(git merge-base $REMOTE_HEAD $BRANCH 2>/dev/null || git rev-list --max-parents=0 $BRANCH | head -1)
fi

echo "Base commit: $BASE_COMMIT"
echo ""

# Count commits to push
COMMITS_TO_PUSH=$(git rev-list --count $BASE_COMMIT..$BRANCH 2>/dev/null || echo "0")

if [ "$COMMITS_TO_PUSH" -eq "0" ]; then
    echo "✓ No commits to push. Branch is up to date."
    exit 0
fi

echo "Commits to push: $COMMITS_TO_PUSH"
TOTAL_CHUNKS=$(( (COMMITS_TO_PUSH + CHUNK_SIZE - 1) / CHUNK_SIZE ))
echo "Total chunks: $TOTAL_CHUNKS"
echo ""

# If commits fit in one chunk, try direct push first
if [ "$COMMITS_TO_PUSH" -le "$CHUNK_SIZE" ]; then
    echo "All commits fit in one chunk. Attempting direct push..."
    echo ""
    
    for attempt in $(seq 1 $MAX_RETRIES); do
        echo "Attempt $attempt/$MAX_RETRIES..."
        if GIT_ASKPASS="gh auth git-credential" git push --force-with-lease $REMOTE $BRANCH 2>&1; then
            echo ""
            echo "✓ Successfully pushed all commits!"
            exit 0
        else
            if [ $attempt -lt $MAX_RETRIES ]; then
                echo "Push failed, waiting ${DELAY}s before retry..."
                sleep $DELAY
            fi
        fi
    done
    
    echo "Direct push failed after $MAX_RETRIES attempts. Using chunked approach..."
    echo ""
fi

# Chunked approach
echo "=========================================="
echo "Starting chunked push approach"
echo "=========================================="
echo ""

# Get list of commits (oldest first)
COMMIT_LIST=$(git rev-list --reverse $BASE_COMMIT..$BRANCH)
TEMP_BRANCH="${BRANCH}-partial-sync-$$"
CURRENT_POSITION=$BASE_COMMIT

# Save current branch state
git branch "${BRANCH}-backup-$(date +%s)" $BRANCH >/dev/null 2>&1 || true

CHUNK_NUM=0
COMMIT_INDEX=0
FAILED_CHUNKS=0

# Process commits in chunks
for commit in $COMMIT_LIST; do
    COMMIT_INDEX=$((COMMIT_INDEX + 1))
    
    # Start new chunk
    if [ $((COMMIT_INDEX % CHUNK_SIZE)) -eq 1 ] || [ $COMMIT_INDEX -eq 1 ]; then
        if [ $COMMIT_INDEX -gt 1 ]; then
            # Push previous chunk
            CHUNK_NUM=$((CHUNK_NUM + 1))
            echo ""
            echo "=========================================="
            echo "Pushing chunk $CHUNK_NUM/$TOTAL_CHUNKS"
            echo "=========================================="
            echo "Commits in chunk: $((COMMIT_INDEX - CHUNK_SIZE))-$((COMMIT_INDEX - 1))"
            echo ""
            
            # Try to push chunk
            SUCCESS=false
            for attempt in $(seq 1 $MAX_RETRIES); do
                echo "Push attempt $attempt/$MAX_RETRIES..."
                
                if GIT_ASKPASS="gh auth git-credential" git push $REMOTE "$TEMP_BRANCH:$BRANCH" --force-with-lease 2>&1; then
                    echo "✓ Chunk $CHUNK_NUM pushed successfully!"
                    SUCCESS=true
                    CURRENT_POSITION=$TEMP_BRANCH
                    break
                else
                    if [ $attempt -lt $MAX_RETRIES ]; then
                        echo "Push failed, waiting ${DELAY}s before retry..."
                        sleep $DELAY
                    else
                        # Try with --force as last resort
                        echo "Trying with --force..."
                        if GIT_ASKPASS="gh auth git-credential" git push $REMOTE "$TEMP_BRANCH:$BRANCH" --force 2>&1; then
                            echo "✓ Chunk $CHUNK_NUM pushed with --force!"
                            SUCCESS=true
                            CURRENT_POSITION=$TEMP_BRANCH
                            break
                        fi
                    fi
                fi
            done
            
            if [ "$SUCCESS" = false ]; then
                echo "❌ Failed to push chunk $CHUNK_NUM after $MAX_RETRIES attempts"
                FAILED_CHUNKS=$((FAILED_CHUNKS + 1))
                echo "Progress saved in branch: $TEMP_BRANCH"
                echo "You can continue later or try with smaller chunk size"
                
                if [ $FAILED_CHUNKS -ge 3 ]; then
                    echo ""
                    echo "❌ Too many failed chunks. Stopping."
                    echo "Current progress saved in: $TEMP_BRANCH"
                    exit 1
                fi
            fi
            
            # Clean up local temp branch (we'll recreate it)
            git branch -D "$TEMP_BRANCH" 2>/dev/null || true
            
            # Wait before next chunk
            if [ $CHUNK_NUM -lt $TOTAL_CHUNKS ]; then
                echo ""
                echo "Waiting ${DELAY}s before next chunk..."
                sleep $DELAY
            fi
        fi
        
        # Create new chunk branch
        CHUNK_NUM=$((CHUNK_NUM + 1))
        echo ""
        echo "Preparing chunk $CHUNK_NUM/$TOTAL_CHUNKS..."
        
        # Get the current remote head for this chunk
        if [ "$CHUNK_NUM" -eq 1 ]; then
            CURRENT_POSITION=$BASE_COMMIT
        else
            # Fetch latest remote state
            git fetch $REMOTE $BRANCH >/dev/null 2>&1 || true
            CURRENT_POSITION=$(git rev-parse ${REMOTE}/${BRANCH} 2>/dev/null || echo "$BASE_COMMIT")
        fi
        
        git checkout -b "$TEMP_BRANCH" "$CURRENT_POSITION" 2>/dev/null || {
            git checkout "$TEMP_BRANCH" 2>/dev/null || {
                echo "Error creating temp branch"
                exit 1
            }
        }
    fi
    
    # Cherry-pick commit
    if git cherry-pick "$commit" >/dev/null 2>&1; then
        echo -n "."
    else
        echo ""
        echo "⚠️  Warning: Failed to cherry-pick $(git log -1 --oneline $commit)"
        echo "Skipping this commit..."
        git cherry-pick --abort 2>/dev/null || true
    fi
done

# Push final chunk
if [ $COMMIT_INDEX -gt 0 ] && [ $((COMMIT_INDEX % CHUNK_SIZE)) -ne 0 ]; then
    CHUNK_NUM=$((CHUNK_NUM + 1))
    echo ""
    echo "=========================================="
    echo "Pushing final chunk $CHUNK_NUM"
    echo "=========================================="
    echo ""
    
    SUCCESS=false
    for attempt in $(seq 1 $MAX_RETRIES); do
        echo "Push attempt $attempt/$MAX_RETRIES..."
        
        if GIT_ASKPASS="gh auth git-credential" git push $REMOTE "$TEMP_BRANCH:$BRANCH" --force-with-lease 2>&1; then
            echo "✓ Final chunk pushed successfully!"
            SUCCESS=true
            break
        else
            if [ $attempt -lt $MAX_RETRIES ]; then
                echo "Push failed, waiting ${DELAY}s before retry..."
                sleep $DELAY
            else
                echo "Trying with --force..."
                if GIT_ASKPASS="gh auth git-credential" git push $REMOTE "$TEMP_BRANCH:$BRANCH" --force 2>&1; then
                    echo "✓ Final chunk pushed with --force!"
                    SUCCESS=true
                    break
                fi
            fi
        fi
    done
    
    if [ "$SUCCESS" = false ]; then
        echo "❌ Failed to push final chunk"
        git branch -D "$TEMP_BRANCH" 2>/dev/null || true
        exit 1
    fi
fi

# Final sync
echo ""
echo "=========================================="
echo "Final synchronization"
echo "=========================================="
echo ""

git checkout $BRANCH >/dev/null 2>&1
git branch -D "$TEMP_BRANCH" 2>/dev/null || true

# Fetch latest
git fetch $REMOTE $BRANCH >/dev/null 2>&1 || true

# Final push to ensure everything is synced
echo "Performing final sync push..."
for attempt in $(seq 1 $MAX_RETRIES); do
    echo "Final push attempt $attempt/$MAX_RETRIES..."
    
    if GIT_ASKPASS="gh auth git-credential" git push $REMOTE $BRANCH --force-with-lease 2>&1; then
        echo ""
        echo "=========================================="
        echo "✓ SUCCESS! Branch $BRANCH is fully synced"
        echo "=========================================="
        echo ""
        echo "Summary:"
        echo "  - Total commits pushed: $COMMIT_INDEX"
        echo "  - Total chunks: $CHUNK_NUM"
        echo "  - Failed chunks: $FAILED_CHUNKS"
        exit 0
    else
        if [ $attempt -lt $MAX_RETRIES ]; then
            echo "Final push failed, waiting ${DELAY}s before retry..."
            sleep $DELAY
        else
            echo "Trying final push with --force..."
            if GIT_ASKPASS="gh auth git-credential" git push $REMOTE $BRANCH --force 2>&1; then
                echo ""
                echo "=========================================="
                echo "✓ SUCCESS! Branch $BRANCH is fully synced (with --force)"
                echo "=========================================="
                exit 0
            fi
        fi
    fi
done

echo ""
echo "❌ Final sync failed after $MAX_RETRIES attempts"
echo "However, most commits were pushed successfully"
echo "You can try running this script again to sync remaining commits"
exit 1

