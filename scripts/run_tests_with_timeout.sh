#!/bin/bash

# Script to run tests with timeout on macOS
# Usage: ./scripts/run_tests_with_timeout.sh [timeout_seconds] [pytest_args...]

set -e

# Default timeout in seconds
TIMEOUT=${1:-300}
shift || true

# Pytest arguments (default to all tests)
PYTEST_ARGS=${@:-"tests -n auto --tb=short"}

echo "Running tests with timeout of ${TIMEOUT} seconds..."
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

# Run pytest in background
uv run pytest ${PYTEST_ARGS} &
PYTEST_PID=$!

# Wait for timeout or completion
wait_time=0
while kill -0 $PYTEST_PID 2>/dev/null && [ $wait_time -lt $TIMEOUT ]; do
    sleep 1
    wait_time=$((wait_time + 1))
    
    # Show progress every 30 seconds
    if [ $((wait_time % 30)) -eq 0 ]; then
        echo "Tests running for ${wait_time} seconds..."
    fi
done

# Check if process is still running
if kill -0 $PYTEST_PID 2>/dev/null; then
    echo "Tests timed out after ${TIMEOUT} seconds. Killing process..."
    kill -TERM $PYTEST_PID
    sleep 5
    kill -KILL $PYTEST_PID 2>/dev/null || true
    cleanup
else
    echo "Tests completed successfully in ${wait_time} seconds."
    wait $PYTEST_PID
    exit $?
fi
