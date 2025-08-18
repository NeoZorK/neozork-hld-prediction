#!/bin/bash

# Safe test runner with limited workers to prevent freezing
# Usage: ./scripts/run_tests_safe.sh [pytest_args...]

set -e

# Pytest arguments (default to all tests)
PYTEST_ARGS=${@:-"tests --tb=short"}

echo "Running tests safely with limited workers..."
echo "Pytest args: ${PYTEST_ARGS}"

# Function to kill background processes
cleanup() {
    echo "Cleaning up background processes..."
    pkill -f "uv run pytest" || true
    pkill -f "pytest" || true
    exit 1
}

# Set up trap to cleanup on exit
trap cleanup SIGINT SIGTERM

# Run pytest with limited workers to prevent freezing
echo "Starting tests with 4 workers (safe mode)..."
uv run pytest ${PYTEST_ARGS} -n 4 --dist=worksteal --max-worker-restart=3

echo "Tests completed successfully."
