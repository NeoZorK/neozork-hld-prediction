#!/bin/bash

echo "=== Testing Docker History Functionality ==="
echo "Starting interactive Docker container..."
echo "After container starts, try pressing ↑ and ↓ arrows to test history"
echo "Press Ctrl+C to exit"

# Run container in interactive mode
docker run -it --rm \
  -v "$(pwd)/data:/app/data" \
  -v "$(pwd)/logs:/app/logs" \
  -v "$(pwd)/results:/app/results" \
  neozork-hld-prediction 