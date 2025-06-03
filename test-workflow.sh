#!/bin/bash
    # Script for testing GitHub Actions workflow locally using act
    # Before running this script, ensure you have Docker and act installed.
    # act: https://github.com/nektos/act

    # Check if uv should be used (default: false)
    USE_UV=${USE_UV:-false}

    # Handle command line arguments
    while [[ "$#" -gt 0 ]]; do
      case $1 in
        --use-uv) USE_UV=true ;;
        *) echo "Unknown parameter: $1"; exit 1 ;;
      esac
      shift
    done

    # Set environment variables for act
    ENV_VARS=()
    if [ "$USE_UV" = true ]; then
        echo "Using uv for faster dependency installation..."
        ENV_VARS+=(-e "USE_UV=true")
    fi

    # Define container options to work around storage issues on macOS with Apple Silicon
    CONTAINER_OPTS="--userns=host --privileged"

    # Check if running on Apple Silicon (M-series)
    if [[ $(uname -m) == "arm64" ]]; then
        echo "Detected Apple Silicon (M-series). Using appropriate container architecture..."
        # Run the workflow with explicit container architecture for Apple Silicon
        echo "Running GitHub Actions workflow locally using act..."
        act -j build --container-architecture linux/amd64 --container-options "${CONTAINER_OPTS}" "${ENV_VARS[@]}" --bind --container-daemon-socket unix:///var/run/docker.sock
    else
        # Run the workflow on other architectures
        echo "Running GitHub Actions workflow locally using act..."
        act -j build --container-options "${CONTAINER_OPTS}" "${ENV_VARS[@]}"
    fi