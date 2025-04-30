#!/bin/bash

# Create main data directories
mkdir -p data/cache/csv_converted
mkdir -p data/raw_parquet
mkdir -p data/processed

# Create directories for notebooks, source, tests, and MQL5 feed
mkdir -p notebooks
mkdir -p src
mkdir -p tests
mkdir -p mql5_feed

# Optional: create virtual environment and cache folders
#mkdir -p .cache
#mkdir -p .idea
#mkdir -p .vscode

echo "All required directories have been created."