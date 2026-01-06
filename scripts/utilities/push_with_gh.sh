#!/bin/bash
# Script to push using GitHub CLI with better handling

set -e

BRANCH="${1:-v0.5.8}"
REMOTE="${2:-origin}"

echo "Attempting to push branch $BRANCH using GitHub CLI..."

# Check if gh is available
if ! command -v gh &> /dev/null; then
    echo "GitHub CLI (gh) is not installed"
    exit 1
fi

# Check authentication
if ! gh auth status &> /dev/null; then
    echo "Not authenticated with GitHub CLI. Run: gh auth login"
    exit 1
fi

# Get repository info
REPO=$(git remote get-url $REMOTE | sed -E 's/.*github.com[:/]([^/]+\/[^/]+)\.git/\1/')
echo "Repository: $REPO"

# Try using gh to set remote protocol to SSH if possible
# But first, let's try direct push with gh's better handling

echo "Configuring git for large push..."
git config http.postBuffer 524288000
git config http.timeout 600

# Try push with gh's credential helper
echo "Attempting push with GitHub CLI support..."
GIT_ASKPASS="gh auth git-credential" git push --force --progress $REMOTE $BRANCH 2>&1 || {
    EXIT_CODE=$?
    echo ""
    echo "Direct push failed. Trying alternative methods..."
    
    # Alternative: Create a new branch and push it
    echo "Creating backup branch: ${BRANCH}-backup-$(date +%s)"
    BACKUP_BRANCH="${BRANCH}-backup-$(date +%s)"
    git branch "$BACKUP_BRANCH" "$BRANCH"
    
    echo "Attempting to push backup branch..."
    if git push $REMOTE "$BACKUP_BRANCH" 2>&1; then
        echo "✓ Successfully pushed backup branch: $BACKUP_BRANCH"
        echo "You can now merge it or set it as the main branch via GitHub web interface"
    else
        echo "✗ Push failed"
        exit $EXIT_CODE
    fi
}

echo "✓ Push completed successfully"

