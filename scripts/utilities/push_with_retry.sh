#!/bin/bash
# Script to push with retry and better error handling

BRANCH="${1:-v0.5.8}"
REMOTE="${2:-origin}"
MAX_RETRIES=3
RETRY_DELAY=10

echo "Attempting to push branch $BRANCH to $REMOTE"
echo "This may take several minutes due to large number of changes..."

# Configure git for large pushes
git config http.postBuffer 524288000
git config http.timeout 600
git config http.lowSpeedLimit 1000
git config http.lowSpeedTime 300

for i in $(seq 1 $MAX_RETRIES); do
    echo ""
    echo "Attempt $i of $MAX_RETRIES..."
    
    if git push --force --progress $REMOTE $BRANCH 2>&1; then
        echo ""
        echo "✓ Successfully pushed $BRANCH to $REMOTE"
        exit 0
    else
        EXIT_CODE=$?
        echo ""
        echo "✗ Push attempt $i failed with exit code $EXIT_CODE"
        
        if [ $i -lt $MAX_RETRIES ]; then
            echo "Waiting $RETRY_DELAY seconds before retry..."
            sleep $RETRY_DELAY
            RETRY_DELAY=$((RETRY_DELAY * 2))  # Exponential backoff
        fi
    fi
done

echo ""
echo "✗ All push attempts failed"
echo ""
echo "Alternative options:"
echo "1. Try again later (network/GitHub may be experiencing issues)"
echo "2. Use git bundle: git bundle create repo.bundle $BRANCH"
echo "3. Contact repository administrator for assistance"
echo "4. Try pushing from a different network location"

exit 1

