#!/bin/bash

# Universal log analyzer for NeoZork HLD Prediction project
# Collects errors, warnings, and tracebacks from all major logs
# Results are saved in logs/analysis/ and summary is printed

set -e

mkdir -p logs/analysis

# Patterns to search
PATTERN='ERROR|WARN|Traceback|FAIL'

# Analyze container logs (if container exists)
echo "[INFO] Analyzing container logs..."
./scripts/native-container/logs.sh --grep "$PATTERN" > logs/analysis/container_errors.log 2>&1 || true

# Analyze application logs
echo "[INFO] Analyzing application logs..."
./scripts/native-container/logs.sh app --grep "$PATTERN" > logs/analysis/app_errors.log 2>&1 || true

# Analyze MCP logs
echo "[INFO] Analyzing MCP logs..."
./scripts/native-container/logs.sh mcp --grep "$PATTERN" > logs/analysis/mcp_errors.log 2>&1 || true

# Analyze test logs
echo "[INFO] Analyzing test logs..."
./scripts/native-container/logs.sh test --grep "$PATTERN" > logs/analysis/test_errors.log 2>&1 || true

# List UV cache files
echo "[INFO] Listing UV cache files..."
ls data/cache/uv_cache/ > logs/analysis/uv_cache_files.txt 2>&1 || true

# Print summary
echo
echo "==== CONTAINER ERRORS ===="
cat logs/analysis/container_errors.log || echo "No container log errors found."

echo
echo "==== APP ERRORS ===="
cat logs/analysis/app_errors.log || echo "No app log errors found."

echo
echo "==== MCP ERRORS ===="
cat logs/analysis/mcp_errors.log || echo "No MCP log errors found."

echo
echo "==== TEST ERRORS ===="
cat logs/analysis/test_errors.log || echo "No test log errors found."

echo
echo "==== UV CACHE FILES ===="
cat logs/analysis/uv_cache_files.txt || echo "No UV cache files found."

echo

# End of script 