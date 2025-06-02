#!/bin/bash
set -e

# Welcome message
echo -e "\n\033[1;36m=== NeoZork HLD Prediction Container Started ===\033[0m\n"

# First question - Run data feed tests
echo -e "\033[1;33mWould you like to run tests for external data feeds? (Polygon, YFinance, Binance) [y/N]:\033[0m"
read -r run_tests

# Debug output to check what was read
echo -e "\033[1;34mInput received: '$run_tests'\033[0m"

# Simplified condition checking
if [ "$run_tests" = "y" ] || [ "$run_tests" = "Y" ]; then
  echo -e "\n\033[1;32m=== Running external data feed tests ===\033[0m\n"

  # Process each script individually to handle specific requirements
  for script in /app/scripts/debug_scripts/*.py; do
    script_name=$(basename "$script")
    echo -e "\033[1;34m=== Running test: $script ===\033[0m"

    # Handle special cases for scripts that need arguments
    if [[ "$script_name" == "debug_check_parquet.py" ]]; then
      # Look for a parquet file to use as an example
      sample_parquet=""
      if [ -d "/app/data/raw_parquet" ] && [ "$(ls -A /app/data/raw_parquet)" ]; then
        sample_parquet=$(find /app/data/raw_parquet -name "*.parquet" | head -n 1)
      fi

      if [ -n "$sample_parquet" ]; then
        echo -e "\033[1;35mFound sample parquet file: $sample_parquet\033[0m"
        PYTHONPATH=/app python "$script" "$sample_parquet"
      else
        echo -e "\033[1;33mNo sample parquet file found. Showing usage instead:\033[0m"
        PYTHONPATH=/app python "$script"
      fi
    else
      # Default case for scripts without special requirements
      PYTHONPATH=/app python "$script"
    fi
    echo -e "\n"
  done
else
  echo -e "\033[1;33mSkipping external data feed tests\033[0m\n"
fi

# Second question - Run MCP server
echo -e "\033[1;33mWould you like to start the MCP service for enhanced LLM support? [y/N]:\033[0m"
read -r run_mcp

# Debug output to check what was read
echo -e "\033[1;34mInput received: '$run_mcp'\033[0m"

# Simplified condition checking
if [ "$run_mcp" = "y" ] || [ "$run_mcp" = "Y" ]; then
  echo -e "\n\033[1;32m=== Starting MCP server in background ===\033[0m\n"
  python mcp_server.py &
  echo -e "\033[1;32mMCP server started in background\033[0m\n"
  # Wait for mcp_server to initialize
  sleep 5
else
  echo -e "\033[1;33mSkipping MCP server startup\033[0m\n"
fi

# Third question - Start HTTP server for plots
echo -e "\033[1;33mWould you like to start HTTP server for viewing plotly HTML plots in browser? [y/N]:\033[0m"
read -r run_http

# Debug output to check what was read
echo -e "\033[1;34mInput received: '$run_http'\033[0m"

# Start HTTP server for plots
if [ "$run_http" = "y" ] || [ "$run_http" = "Y" ]; then
  # Check if directory exists and create it if needed
  if [ ! -d "/app/results/plots" ]; then
    mkdir -p /app/results/plots
    echo -e "\033[1;32mCreated directory: /app/results/plots\033[0m"
  fi

  # Start HTTP server in background
  echo -e "\n\033[1;32m=== Starting HTTP server for plots on port 8080 ===\033[0m"
  echo -e "\033[1;32mYou can access plots at: http://localhost:8080\033[0m\n"

  # Use Python's built-in HTTP server
  cd /app/results && python -m http.server 8080 &
  HTTP_SERVER_PID=$!
  echo -e "\033[1;32mHTTP server started with PID: $HTTP_SERVER_PID\033[0m\n"
else
  echo -e "\033[1;33mSkipping HTTP server startup\033[0m\n"
fi

# Always show help
echo -e "\033[1;32m=== NeoZork HLD Prediction Usage Guide ===\033[0m\n"
python run_analysis.py -h

echo -e "\n\033[1;36m=== Container is now ready for use ===\033[0m"
echo -e "\033[1;36mUse the commands above to analyze data\033[0m"

# Show tips for opening plots
echo -e "\n\033[1;36m=== Tips for viewing plotly HTML plots ===\033[0m"
echo -e "\033[1;36m1. Run a command like: python run_analysis.py demo --rule PHLD\033[0m"
echo -e "\033[1;36m2. Find generated HTML at: results/plots/*.html\033[0m"
echo -e "\033[1;36m3. If HTTP server is running, access at: http://localhost:8080/plots/\033[0m"
echo -e "\033[1;36m4. You can also open HTML files directly from the host system at: ./results/plots/\033[0m"

echo -e "\n\033[1;36mPress Ctrl+C to stop the container\033[0m\n"

# Keep container running and accepting input
while true; do
  echo -e "\033[1;35mneozork-hld>\033[0m "
  read -r cmd
  if [ -n "$cmd" ]; then
    eval "$cmd"
  fi
done
