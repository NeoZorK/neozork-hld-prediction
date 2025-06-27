#!/bin/bash

# Get the project root directory (two levels up from scripts/docker/)
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"

echo "=== Testing Docker History Functionality ==="
echo "Starting interactive Docker container..."
echo "After container starts, try pressing ↑ and ↓ arrows to test history"
echo "Press Ctrl+C to exit"

# Run container in interactive mode
docker run -it --rm \
  -v "$PROJECT_ROOT/data:/app/data" \
  -v "$PROJECT_ROOT/logs:/app/logs" \
  -v "$PROJECT_ROOT/results:/app/results" \
  neozork-hld-prediction 