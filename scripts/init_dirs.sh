#!/bin/bash

# -*- coding: utf-8 -*-
# scripts/init_dirs.sh

# Always run from the root of the repository, regardless of the current directory
cd "$(dirname "$0")/.." || exit 1

# Create main data directories
mkdir -p data/cache/csv_converted
mkdir -p data/raw_parquet
mkdir -p data/processed

# Log and results directories
mkdir -p logs
mkdir -p results

# Source and script directories
mkdir -p src/eda
mkdir -p scripts/debug_scripts
mkdir -p scripts/log_analysis

# Create directories for notebooks, source, tests, and MQL5 feed
mkdir -p notebooks
mkdir -p src
mkdir -p tests
mkdir -p mql5_feed

# Create .env file with default fields if it does not exist
if [ ! -f .env ]; then
cat > .env <<EOL
# Polygon.io API key
POLYGON_API_KEY=your_polygon_api_key_here

# Binance API keys
BINANCE_API_KEY=your_binance_api_key_here
BINANCE_API_SECRET=your_binance_api_secret_here

# Add other environment variables as needed
EOL
    echo ".env file created with default fields."
else
    echo ".env file already exists, not overwritten."
fi

echo "All required directories have been created."