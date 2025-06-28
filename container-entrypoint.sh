#!/bin/bash

# Native Apple Silicon Container Entrypoint Script
# This script handles initialization and startup of the NeoZork HLD Prediction container

set -e

# UV-only mode enforcement
export USE_UV=true
export UV_ONLY=true
export UV_CACHE_DIR=/app/.uv_cache
export UV_VENV_DIR=/app/.venv
export NATIVE_CONTAINER=true
export DOCKER_CONTAINER=false

# Function to log messages with timestamps
log_message() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

# Set PYTHONPATH globally
export PYTHONPATH=/app

# Create necessary directories
create_directories() {
    log_message "Creating necessary directories..."
    mkdir -p /app/data/cache/csv_converted \
             /app/data/raw_parquet \
             /app/logs \
             /tmp/matplotlib-cache \
             /app/results/plots \
             /app/.pytest_cache \
             /app/.uv_cache \
             /app/.venv \
             /tmp/bash_history \
             /tmp/bin
}

# Main execution
main() {
    log_message "Starting NeoZork HLD Prediction container..."
    
    # Create directories
    create_directories
    
    log_message "Container ready. Waiting for commands..."
    
    # Keep container running by waiting
    while true; do
        sleep 3600  # Sleep for 1 hour
    done
}

# Run main function
main "$@" 