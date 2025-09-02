#!/bin/bash

# Docker Test Runner Script
# This script runs tests in the Docker container environment

echo "🐳 Docker Test Runner"
echo "===================="

# Check if we're in a Docker container
if [ -f /.dockerenv ] || [ "$DOCKER_CONTAINER" = "true" ]; then
    echo "✅ Running in Docker container"
else
    echo "❌ This script should run inside a Docker container"
    exit 1
fi

# Change to app directory
cd /app

# Check if UV is available
if command -v uv &> /dev/null; then
    echo "✅ UV is available: $(uv --version)"
else
    echo "❌ UV is not available"
    exit 1
fi

# Run tests with UV in multithreaded mode
echo "🚀 Running tests with UV..."
echo "Command: uv run pytest tests -n auto -v --tb=short"

# Run the Python test runner
python scripts/docker/run_docker_tests.py

echo "🎯 Test execution completed!"
