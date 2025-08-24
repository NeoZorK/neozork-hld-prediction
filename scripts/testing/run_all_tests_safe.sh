#!/bin/bash

# Safe test runner for all tests with limited workers to prevent freezing
# Usage: ./scripts/run_all_tests_safe.sh [timeout_seconds]

set -e

# Default timeout in seconds
TIMEOUT=${1:-600}

echo "Running all tests safely with limited workers..."
echo "Timeout: ${TIMEOUT} seconds"

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
echo "Starting all tests with 4 workers (safe mode)..."
echo "This will take longer but should not freeze..."

# Run tests in background
uv run pytest tests -n 4 --dist=worksteal --max-worker-restart=3 --tb=short &
PYTEST_PID=$!

# Wait for timeout or completion
wait_time=0
while kill -0 $PYTEST_PID 2>/dev/null && [ $wait_time -lt $TIMEOUT ]; do
    sleep 5
    wait_time=$((wait_time + 5))
    
    # Show progress every 60 seconds
    if [ $((wait_time % 60)) -eq 0 ]; then
        echo "Tests running for ${wait_time} seconds..."
    fi
done

# Check if process is still running
if kill -0 $PYTEST_PID 2>/dev/null; then
    echo "Tests timed out after ${TIMEOUT} seconds. Killing process..."
    kill -TERM $PYTEST_PID
    sleep 10
    kill -KILL $PYTEST_PID 2>/dev/null || true
    cleanup
else
    echo "Tests completed successfully in ${wait_time} seconds."
    wait $PYTEST_PID
    exit $?
fi
