#!/bin/bash

# Script to test mql5_feed folder access in Docker container

echo "=== Testing mql5_feed folder access in Docker container ==="

# Check if we're in a Docker container
if [ -f /.dockerenv ]; then
    echo "✅ Running inside Docker container"
else
    echo "⚠️  Not running inside Docker container"
fi

echo ""
echo "=== Current environment ==="
echo "Current directory: $(pwd)"
echo "Current user: $(whoami)"
echo "User home: $HOME"

echo ""
echo "=== Checking possible mql5_feed locations ==="

# List of possible paths to check
paths=(
    "/app/mql5_feed"
    "/workspace/mql5_feed"
    "/home/neozork/mql5_feed"
    "$(pwd)/mql5_feed"
    "/mql5_feed"
    "/app"
    "/workspace"
    "/home/neozork"
)

for path in "${paths[@]}"; do
    if [ -d "$path" ]; then
        echo "✅ Found directory: $path"
        echo "   Contents: $(ls -la "$path" | head -5)"
        
        # Check if mql5_feed is inside this directory
        if [ -d "$path/mql5_feed" ]; then
            echo "   🎯 Found mql5_feed subdirectory at: $path/mql5_feed"
            echo "   mql5_feed contents: $(ls -la "$path/mql5_feed")"
            
            if [ -d "$path/mql5_feed/indicators" ]; then
                echo "   📁 Found indicators directory"
                echo "   indicators contents: $(ls -la "$path/mql5_feed/indicators")"
            fi
        fi
    else
        echo "❌ Not found: $path"
    fi
done

echo ""
echo "=== Running Python tests ==="

# Try to run the diagnostic test
if command -v python3 &> /dev/null; then
    echo "Running Python diagnostic test..."
    python3 -m pytest tests/docker/test_container_mql5_feed_paths.py::TestContainerMQL5FeedPaths::test_list_possible_paths -v -s
else
    echo "Python3 not found, trying python..."
    python -m pytest tests/docker/test_container_mql5_feed_paths.py::TestContainerMQL5FeedPaths::test_list_possible_paths -v -s
fi

echo ""
echo "=== Testing complete ===" 