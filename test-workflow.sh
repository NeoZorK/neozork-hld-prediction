#!/bin/bash
# Script for testing GitHub Actions workflow locally using act
# Before running this script, ensure you have Docker and act installed.
# act: https://github.com/nektos/act

# Define the runner image mapping for act.
# This uses a known working image for GitHub Actions runners
ACT_RUNNER_IMAGE_MAPPING="ubuntu-latest=catthehacker/ubuntu:act-latest"

# Check if running on Apple Silicon (M-series)
if [[ $(uname -m) == "arm64" ]]; then
    echo "Detected Apple Silicon (M-series). Using appropriate container architecture..."
    # Run the workflow with explicit container architecture for Apple Silicon
    echo "Running GitHub Actions workflow locally using act..."
    act -j build -P "${ACT_RUNNER_IMAGE_MAPPING}" --container-architecture linux/amd64 --bind
else
    # Run the workflow on other architectures
    echo "Running GitHub Actions workflow locally using act..."
    act -j build -P "${ACT_RUNNER_IMAGE_MAPPING}"
fi

