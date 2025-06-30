#!/bin/bash

# Script to run tests in native container environment
# Excludes Docker-specific tests that expect DOCKER_CONTAINER=true

set -e

echo "🚀 Running tests in native container environment..."
echo "📋 Environment variables:"
echo "   NATIVE_CONTAINER: ${NATIVE_CONTAINER:-not set}"
echo "   DOCKER_CONTAINER: ${DOCKER_CONTAINER:-not set}"
echo "   USE_UV: ${USE_UV:-not set}"
echo "   UV_ONLY: ${UV_ONLY:-not set}"

# Set environment variables for native container
export NATIVE_CONTAINER=true
export DOCKER_CONTAINER=false

# Run tests excluding Docker tests
echo "🧪 Running tests with Docker tests excluded..."

# Use uv to run pytest with proper configuration
uv run pytest tests \
    -v \
    --tb=short \
    --disable-warnings \
    --color=yes \
    -n auto \
    -m "not docker"

echo "✅ Tests completed successfully!" 