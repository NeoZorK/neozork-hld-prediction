#!/bin/bash
# Script for testing GitHub Actions workflow locally using act
# Before running this script, ensure you have Docker and act installed.
# act: https://github.com/nektos/act

# Get the project root directory (two levels up from scripts/docker/)
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"

# Change to project root directory
cd "$PROJECT_ROOT"

# Check if running on Apple Silicon (M-series)
if [[ $(uname -m) == "arm64" ]]; then
    echo "Detected Apple Silicon (M-series). Using compatible configuration..."

    # First, remove any existing .actrc file to avoid conflicts
    if [ -f .actrc ]; then
        mv .actrc .actrc.bak
        echo "Backed up existing .actrc file to .actrc.bak"
    fi

    # Create .actrc file with compatible configuration for Apple Silicon
    cat > .actrc <<EOL
-P ubuntu-latest=ghcr.io/catthehacker/ubuntu:act-22.04
--container-architecture linux/amd64
EOL

    # Run act with minimal arguments, allowing it to use .actrc configuration
    echo "Running GitHub Actions workflow locally using act..."
    act -j build

    # Restore original .actrc if it existed
    if [ -f .actrc.bak ]; then
        mv .actrc.bak .actrc
        echo "Restored original .actrc file"
    else
        # If there was no backup, remove the created .actrc
        rm .actrc
    fi
else
    # Run the workflow on other architectures with standard configuration
    echo "Running GitHub Actions workflow locally using act..."
    act -j build -P ubuntu-latest=ghcr.io/catthehacker/ubuntu:act-22.04
fi