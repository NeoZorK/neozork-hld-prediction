#!/bin/bash

# Script to run all tests with automatic environment detection
# Docker tests will be automatically skipped in native container

set -e

echo "🚀 Running all tests with automatic environment detection..."

# Detect environment
if [[ "${NATIVE_CONTAINER}" == "true" ]]; then
    echo "🔍 Detected: Native Container Environment"
    echo "⏭️  Docker tests will be automatically skipped"
elif [[ "${DOCKER_CONTAINER}" == "true" ]] || [[ -f "/.dockerenv" ]]; then
    echo "🔍 Detected: Docker Container Environment"
    echo "⏭️  Native container tests will be automatically skipped"
else
    echo "🔍 Detected: Local Environment"
    echo "ℹ️  All tests will run"
fi

echo "📋 Environment variables:"
echo "   NATIVE_CONTAINER: ${NATIVE_CONTAINER:-not set}"
echo "   DOCKER_CONTAINER: ${DOCKER_CONTAINER:-not set}"
echo "   USE_UV: ${USE_UV:-not set}"
echo "   UV_ONLY: ${UV_ONLY:-not set}"

# Run all tests (Docker tests will be automatically skipped in native container)
echo "🧪 Running all tests..."

# Use uv to run pytest with proper configuration
uv run pytest tests \
    -v \
    --tb=short \
    --disable-warnings \
    --color=yes \
    -n auto

echo "✅ All tests completed successfully!" 