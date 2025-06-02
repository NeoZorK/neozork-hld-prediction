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

# Создаем скрипт-обертку nz
cat > /tmp/bin/nz << 'EOF'
#!/bin/bash
python /app/run_analysis.py "$@"
EOF
chmod +x /tmp/bin/nz

# Создаем скрипт-обертку eda
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
        echo -e "\033[1;32m=== Opening latest HTML file in lynx: $latest_html ===\033[0m"
        # Get the relative URL path
        relative_path=${latest_html#/app/results/}
        echo -e "\033[1;32m=== You can also access this file at: http://localhost:8080/$relative_path ===\033[0m"

        # Ask if user wants to view in terminal browser
        echo -e "\033[1;33mDo you want to view this HTML file in terminal browser? [y/N]:\033[0m"
        read -r view_html

        if [ "$view_html" = "y" ] || [ "$view_html" = "Y" ]; then
          # Open the HTML file in lynx
          lynx -localhost -force_html "$latest_html"
        fi
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
  cd /app/results && run_python_safely python -m http.server 8080 &
  HTTP_SERVER_PID=$!
  echo -e "\033[1;32mHTTP server started with PID: $HTTP_SERVER_PID\033[0m\n"
else
  echo -e "\033[1;33mSkipping HTTP server startup\033[0m\n"
fi

# Always show help
echo -e "\033[1;32m=== NeoZork HLD Prediction Usage Guide ===\033[0m\n"
run_python_safely python run_analysis.py -h

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
  echo -ne "\033[1;35mneozork-hld>\033[0m "
  read -r cmd
  if [ -n "$cmd" ]; then
    # Проверка на наличие необычных символов (которые могут появиться при использовании backspace)
    if [[ "$cmd" == *$'\e'* ]]; then
      echo -e "\033[1;31m[WARNING] Command contains escape sequences which may cause errors. Please try again.\033[0m"
      continue
    fi

    # Проверяем, начинается ли команда с nz
    if [[ "$cmd" == "nz"* ]]; then
      # Если это команда nz, вызываем её напрямую через wrapper-скрипт
      args="${cmd#nz}"
      echo "Executing: nz$args"
      { /tmp/bin/nz $args; } || {
        echo -e "\033[1;31m[ERROR] Command failed but container will remain running\033[0m"
        echo -e "\033[1;33mYou can try another command\033[0m"
      }
    # Проверяем, начинается ли команда с eda
    elif [[ "$cmd" == "eda"* ]]; then
      # Если это команда eda, вызываем её напрямую через wrapper-скрипт
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
      # Run any other command safely (без использования eval по возможности)
      # Используем {} для группировки и перехвата ошибок без выхода из контейнера
      { bash -c "$cmd"; } || {
        echo -e "\033[1;31m[ERROR] Command failed but container will remain running\033[0m"
        echo -e "\033[1;33mYou can try another command\033[0m"
      }
    fi
  fi
done
