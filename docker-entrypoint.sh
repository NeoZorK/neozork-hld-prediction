#!/bin/bash

# Create history directory with proper permissions
mkdir -p /tmp/bash_history
chmod 777 /tmp/bash_history
export HISTFILE=/tmp/bash_history/.bash_history
export HISTSIZE=1000
export HISTCONTROL=ignoreboth
touch $HISTFILE
chmod 666 $HISTFILE

# Create nz command wrapper script in a writable directory
mkdir -p /tmp/bin

# Create the directory if it doesn't exist
cat > /tmp/bin/nz << 'EOF'
#!/bin/bash
python /app/run_analysis.py "$@"
EOF
chmod +x /tmp/bin/nz

# Create eda command wrapper script in a writable directory
cat > /tmp/bin/eda << 'EOF'
#!/bin/bash
python /app/src/eda/eda_batch_check.py "$@"
EOF
chmod +x /tmp/bin/eda

export PATH="/tmp/bin:$PATH"

# Function to handle errors without exiting container
run_python_safely() {
  # Run Python command and capture exit code
  "$@"
  local exit_code=$?

  # If the command failed, print error message but don't exit container
  if [ $exit_code -ne 0 ]; then
    echo -e "\033[1;31m[ERROR] Command failed with exit code $exit_code\033[0m"
    echo -e "\033[1;33mContainer will remain running. You can try another command.\033[0m"
    return $exit_code
  fi

  # Check if HTML files were created in results/plots directory
  if [ -d "/app/results/plots" ]; then
    # Find the most recently modified HTML file
    latest_html=$(find /app/results/plots -name "*.html" -type f -printf "%T@ %p\n" | sort -n | tail -1 | cut -f2- -d" ")

    if [ -n "$latest_html" ]; then
      # Get file modification time
      mod_time=$(stat -c %Y "$latest_html")
      # Get current time
      current_time=$(date +%s)
      # If file was modified in the last 10 seconds, open it
      if [ $((current_time - mod_time)) -lt 10 ]; then
        echo -e "\033[1;32m=== New HTML file generated: $latest_html ===\033[0m"
      fi
    fi
  fi

  return 0
}

# Set PYTHONPATH globally for the entire script
export PYTHONPATH=/app

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
        run_python_safely python "$script" "$sample_parquet"
      else
        echo -e "\033[1;33mNo sample parquet file found. Showing usage instead:\033[0m"
        run_python_safely python "$script"
      fi
    else
      # Default case for scripts without special requirements
      run_python_safely python "$script"
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
  run_python_safely python mcp_server.py &
  echo -e "\033[1;32mMCP server started in background\033[0m\n"
  # Wait for mcp_server to initialize
  sleep 5
else
  echo -e "\033[1;33mSkipping MCP server startup\033[0m\n"
fi

# Always show help
echo -e "\033[1;32m=== NeoZork HLD Prediction Usage Guide ===\033[0m\n"
run_python_safely python run_analysis.py -h

echo -e "\n\033[1;36m=== Container is ready for analysis ===\033[0m"

# Show tips for viewing plots
echo -e "\n\033[1;36m=== Tips for viewing plotly HTML plots ===\033[0m"
echo -e "\033[1;36m1. Run a command like: python run_analysis.py demo --rule PHLD (or: nz demo --rule PHLD)\033[0m"
echo -e "\033[1;36m2. Generated plots are saved to results/plots/*.html\033[0m"
echo -e "\033[1;36m3. To access plots from Docker Desktop:\033[0m"
echo -e "\033[1;36m   - Open Docker Desktop\033[0m"
echo -e "\033[1;36m   - Select your running container\033[0m"
echo -e "\033[1;36m   - Go to 'Press ... -> View Files -> Bind Mounts' tab\033[0m"
echo -e "\033[1;36m   - Find and open the volume mapped to /app/results\033[0m"
echo -e "\033[1;36m   - Navigate to the 'plots' folder to view your HTML files\033[0m"

echo -e "\n\033[1;36mPress Ctrl+C to stop the container\033[0m\n"

# Keep container running and accepting input
echo -e "\n\033[1;36mStarting interactive shell...\033[0m\n"

# Create a file with common commands for the interactive shell
cat > /tmp/neozork_commands.txt << EOL
nz
eda
python
pytest
python run_analysis.py demo --rule PHLD
nz demo --rule PHLD
python run_analysis.py yfinance MSFT --rule PHLD
nz yfinance AAPL --rule PHLD
python run_analysis.py mql5 EURUSD --interval H4 --rule PHLD
nz mql5 BTCUSD --interval H4 --rule PHLD
ls results/plots/
EOL

# Create a custom .inputrc file for readline configuration in a directory with write permissions
mkdir -p /tmp/bash_config
cat > /tmp/bash_config/.inputrc << EOL
# Enable 8-bit input
set meta-flag on
set input-meta on
set convert-meta off
set output-meta on

# Bind the up and down arrow keys for history search
"\e[A": history-search-backward
"\e[B": history-search-forward

# Enable tab completion
TAB: complete

# Use case-insensitive tab completion
set completion-ignore-case on

# Show all completions after a single tab press
set show-all-if-ambiguous on
EOL

# Set the INPUTRC environment variable to use our custom file
export INPUTRC=/tmp/bash_config/.inputrc

# Setup Bash history settings
export HISTSIZE=1000
export HISTFILESIZE=2000
export HISTCONTROL=ignoreboth:erasedups

# Ensure history is preserved between sessions with proper permissions
mkdir -p /tmp/bash_history
touch /tmp/bash_history/.bash_history
chmod 777 /tmp/bash_history/.bash_history
export HISTFILE=/tmp/bash_history/.bash_history

# Preload common commands into history
if [ -f /tmp/neozork_commands.txt ]; then
    cat /tmp/neozork_commands.txt >> /tmp/bash_history/.bash_history
    echo -e "\033[1;36mHistory preloaded with common commands (use UP/DOWN arrows to navigate)\033[0m\n"
fi

# Handle Ctrl+C (SIGINT) to terminate all background processes
cleanup() {
  echo -e "\n\033[1;36mShutting down all background processes...\033[0m"
  # Find and terminate python processes more reliably
  pkill -TERM -f "python mcp_server.py" 2>/dev/null
  sleep 1
  # Force kill if still running
  pkill -9 -f "python mcp_server.py" 2>/dev/null
  exit 0
}

# Set up the trap for SIGINT (Ctrl+C)
trap cleanup SIGINT

# Run the interactive shell with proper readline support
while true; do
  echo -ne "\033[1;35mneozork-hld>\033[0m "
  # Use bash -c to create a properly configured interactive shell that can process arrow keys
  history -a  # Save history after each command

  # Use read with readline support (-e flag)
  if read -e cmd; then
    if [ -n "$cmd" ]; then
      # Add command to history
      history -s "$cmd"

      # Check if the command starts with nz
      if [[ "$cmd" == "nz"* ]]; then
        # If it starts with nz, call the nz wrapper script
        args="${cmd#nz}"
        echo "Executing: nz$args"
        { /tmp/bin/nz $args; } || {
          echo -e "\033[1;31m[ERROR] Command failed but container will remain running\033[0m"
          echo -e "\033[1;33mYou can try another command\033[0m"
        }
      # check if the command starts with eda
      elif [[ "$cmd" == "eda"* ]]; then
        # If it starts with eda, call the eda wrapper script
        args="${cmd#eda}"
        echo "Executing: eda$args"
        { /tmp/bin/eda $args; } || {
          echo -e "\033[1;31m[ERROR] Command failed but container will remain running\033[0m"
          echo -e "\033[1;33mYou can try another command\033[0m"
        }
      # Check if the command is a Python script execution
      elif [[ "$cmd" == *"python run_analysis.py"* ]]; then
        # Extract arguments from the command
        args=$(echo "$cmd" | sed 's/python run_analysis.py//')
        # Run the analysis script with the extracted arguments
        echo "Executing: python /app/run_analysis.py$args"
        { python /app/run_analysis.py$args; } || {
          echo -e "\033[1;31m[ERROR] Command failed but container will remain running\033[0m"
          echo -e "\033[1;33mYou can try another command\033[0m"
        }
      else
        # Run any other command safely (without special handling)
        # Use {} for command grouping to handle errors
        { bash -c "$cmd"; } || {
          echo -e "\033[1;31m[ERROR] Command failed but container will remain running\033[0m"
          echo -e "\033[1;33mYou can try another command\033[0m"
        }
      fi
    fi
  else
    # Handle Ctrl+D (EOF) or read error
    echo -e "\nExit signal received. Use Ctrl+C to fully exit the container."
  fi
done
