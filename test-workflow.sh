#!/bin/bash
# Script for testing GitHub Actions workflow locally using act
# Before running this script, ensure you have Docker and act installed.
# act: https://github.com/nektos/act

# Check if running on Apple Silicon (M-series)
if [[ $(uname -m) == "arm64" ]]; then
    echo "Detected Apple Silicon (M-series). Using compatible configuration..."

    # First, remove any existing .actrc file to avoid conflicts
    if [ -f .actrc ]; then
        mv .actrc .actrc.bak
        echo "Backed up existing .actrc file to .actrc.bak"
    fi

    # Create a custom .actrc file without storage options
    cat > .actrc <<EOL
-P ubuntu-latest=catthehacker/ubuntu:act-latest
--container-architecture linux/amd64
EOL

    # Set env variables to prevent Docker storage options from being used
    export ACT_DISABLE_STORAGE_OPT=true
    export ACT_CONTAINER_OPTIONS="--security-opt seccomp=unconfined"

    # Run act with minimal arguments
    echo "Running GitHub Actions workflow locally using act..."
    act -j build

    # Restore original .actrc if it existed
    if [ -f .actrc.bak ]; then
        mv .actrc.bak .actrc
        echo "Restored original .actrc file"
    else
        rm .actrc
    fi
else
    # Run the workflow on other architectures with standard configuration
    echo "Running GitHub Actions workflow locally using act..."
    act -j build -P ubuntu-latest=catthehacker/ubuntu:act-latest
fi

