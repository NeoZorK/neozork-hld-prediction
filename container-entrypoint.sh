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
    
    # Create directories with error handling
    mkdir -p /app/data/cache/csv_converted 2>/dev/null || true
    mkdir -p /app/data/raw_parquet 2>/dev/null || true
    mkdir -p /app/logs 2>/dev/null || true
    mkdir -p /tmp/matplotlib-cache 2>/dev/null || true
    mkdir -p /app/results/plots 2>/dev/null || true
    mkdir -p /app/.pytest_cache 2>/dev/null || true
    mkdir -p /app/.uv_cache 2>/dev/null || true
    mkdir -p /app/.venv 2>/dev/null || true
    mkdir -p /tmp/bash_history 2>/dev/null || true
    mkdir -p /tmp/bin 2>/dev/null || true
    
    log_message "Directories created successfully"
}

# Main execution
main() {
    log_message "Starting NeoZork HLD Prediction container..."
    
    # Create directories
    create_directories
    
    log_message "Container ready. Entering idle mode..."
    
    # Keep container running (idle)
    tail -f /dev/null
}

# Run main function
main "$@" 