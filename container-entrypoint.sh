#!/bin/bash

# Native Apple Silicon Container Entrypoint Script
# This script handles initialization and startup of the NeoZork HLD Prediction container
# Full feature parity with Docker container

set -e

# UV-only mode enforcement
export USE_UV=true
export UV_ONLY=true
export UV_CACHE_DIR=/app/.uv_cache
export UV_VENV_DIR=/app/.venv
export NATIVE_CONTAINER=true
export DOCKER_CONTAINER=false

# Python configuration
export PYTHONUNBUFFERED=1
export PYTHONDONTWRITEBYTECODE=1
export MPLCONFIGDIR=/tmp/matplotlib-cache

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
    mkdir -p /tmp/bash_config 2>/dev/null || true
    
    log_message "Directories created successfully"
}

# Verify UV is available and working
verify_uv() {
    log_message "=== UV Package Manager Status ==="
    if command -v uv &> /dev/null; then
        echo -e "\033[1;32m✅ UV is available: $(uv --version)\033[0m"
    else
        echo -e "\033[1;31m❌ UV is not available - this is required for UV-only mode\033[0m"
        exit 1
    fi

    # Run UV test script to validate environment
    log_message "=== Running UV Environment Test ==="
    if [ -f "/app/scripts/test_uv_docker.py" ]; then
        python /app/scripts/test_uv_docker.py
        if [ $? -eq 0 ]; then
            echo -e "\033[1;32m✅ UV environment test passed\033[0m"
        else
            echo -e "\033[1;33m⚠️  UV environment test had issues - continuing anyway\033[0m"
        fi
    else
        echo -e "\033[1;33m⚠️  UV test script not found - skipping test\033[0m"
    fi
}

# Setup bash history and configuration
setup_bash_environment() {
    log_message "Setting up bash environment..."
    
    # Create history directory with proper permissions
    mkdir -p /tmp/bash_history
    chmod 777 /tmp/bash_history
    export HISTFILE=/tmp/bash_history/.bash_history
    export HISTSIZE=1000
    export HISTCONTROL=ignoreboth
    touch $HISTFILE
    chmod 666 $HISTFILE

    # Create a custom .inputrc file for readline configuration
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

    # Set custom prompt for better identification
    export PS1='\[\033[1;36m\]neozork\[\033[0m\]:\[\033[1;34m\]\w\[\033[0m\]$ '
}

# Create command wrapper scripts
create_command_wrappers() {
    log_message "Creating command wrapper scripts..."
    
    mkdir -p /tmp/bin

    # Create nz command wrapper script
    cat > /tmp/bin/nz << 'EOF'
#!/bin/bash
python /app/run_analysis.py "$@"
EOF
    chmod +x /tmp/bin/nz

    # Create eda command wrapper script
    cat > /tmp/bin/eda << 'EOF'
#!/bin/bash
python /app/src/eda/eda_batch_check.py "$@"
EOF
    chmod +x /tmp/bin/eda

    # Create uv command wrappers for better UX
    cat > /tmp/bin/uv-install << 'EOF'
#!/bin/bash
echo "Installing dependencies using UV..."
uv pip install -r /app/requirements.txt
EOF
    chmod +x /tmp/bin/uv-install

    cat > /tmp/bin/uv-update << 'EOF'
#!/bin/bash
echo "Updating dependencies using UV..."
uv pip install --upgrade -r /app/requirements.txt
EOF
    chmod +x /tmp/bin/uv-update

    cat > /tmp/bin/uv-test << 'EOF'
#!/bin/bash
echo "Running UV environment test..."
python /app/scripts/test_uv_docker.py
EOF
    chmod +x /tmp/bin/uv-test

    # Create pytest wrapper for UV
    cat > /tmp/bin/uv-pytest << 'EOF'
#!/bin/bash
echo "Running pytest with UV..."
uv run pytest tests -n auto
EOF
    chmod +x /tmp/bin/uv-pytest

    # Create MCP server wrapper
    cat > /tmp/bin/mcp-start << 'EOF'
#!/bin/bash
echo "Starting MCP server..."
nohup python /app/neozork_mcp_server.py > /app/logs/mcp_server.log 2>&1 &
MCP_PID=$!
echo $MCP_PID > /tmp/mcp_server.pid
echo "MCP server started with PID: $MCP_PID"
EOF
    chmod +x /tmp/bin/mcp-start

    cat > /tmp/bin/mcp-check << 'EOF'
#!/bin/bash
echo "Checking MCP server status..."
python /app/scripts/check_mcp_status.py
EOF
    chmod +x /tmp/bin/mcp-check

    export PATH="/tmp/bin:$PATH"
}

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

# Function to cleanup MCP server on exit
cleanup_mcp_server() {
    if [ -f /tmp/mcp_server.pid ]; then
        MCP_PID=$(cat /tmp/mcp_server.pid)
        if kill -0 $MCP_PID 2>/dev/null; then
            echo -e "\n\033[1;33mStopping MCP server (PID: $MCP_PID)...\033[0m"
            kill $MCP_PID
            wait $MCP_PID 2>/dev/null
            echo -e "\033[1;32mMCP server stopped\033[0m"
        fi
        rm -f /tmp/mcp_server.pid
    fi
}

# Set trap to cleanup MCP server on script exit
trap cleanup_mcp_server EXIT

# Initialize bash history with useful commands
init_bash_history() {
    echo -e "\033[1;33mInitializing bash history with useful commands...\033[0m"
    
    # Define useful commands for the container
    local useful_commands=(
        "uv run pytest tests -n auto"
        "nz --interactive"
        "eda -dqc"
        "nz --indicators"
        "nz --metric"
        "nz show csv mn1 eur --rule rsi_div:14,30,70,open"
        "nz show csv mn1 eur --rule rsi_mom:14,30,70,close --strategy 2,5,0.07"
        "python"
        "python -c \"import sys; print('Python version:', sys.version)\""
        "uv pip list"
        "ls -la"
        "pwd"
        "nz demo --rule PHLD"
        "nz yfinance AAPL --rule PHLD"
        "nz mql5 BTCUSD --interval H4 --rule PHLD"
        "eda --data-quality-checks"
        "eda --descriptive-stats"
        "python scripts/check_mcp_status.py"
        "python neozork_mcp_server.py"
        "mcp-start"
        "mcp-check"
        "uv-pytest"
    )
    
    # Add commands to history file
    for cmd in "${useful_commands[@]}"; do
        echo "$cmd" >> "$HISTFILE"
    done
    
    # Load history into current session
    history -r
    
    echo -e "\033[1;32mAdded ${#useful_commands[@]} useful commands to bash history\033[0m"
}

# Run external data feed tests
run_data_feed_tests() {
    echo -e "\033[1;33mWould you like to run tests for external data feeds? (Polygon, YFinance, Binance) [y/N]:\033[0m"
    read -r run_tests

    # Debug output to check what was read
    echo -e "\033[1;34mInput received: '$run_tests'\033[0m"

    # Simplified condition checking
    if [ "$run_tests" = "y" ] || [ "$run_tests" = "Y" ]; then
        echo -e "\n\033[1;32m=== Running external data feed tests in Native Container (UV Mode) ===\033[0m\n"
        # Run the tests using the Docker-specific test runner
        run_python_safely python /app/tests/run_tests_docker.py
    else
        echo -e "\033[1;33mSkipping external data feed tests\033[0m\n"
    fi
}

# Start MCP server
start_mcp_server() {
    echo -e "\033[1;33mWould you like to start the MCP service for enhanced LLM support? [y/N]:\033[0m"
    read -r run_mcp

    # Debug output to check what was read
    echo -e "\033[1;34mInput received: '$run_mcp'\033[0m"

    # Simplified condition checking
    if [ "$run_mcp" = "y" ] || [ "$run_mcp" = "Y" ]; then
        echo -e "\n\033[1;32m=== Starting MCP server in background (UV Mode) ===\033[0m\n"
        # Start MCP server in background and redirect output to prevent EOF
        nohup python neozork_mcp_server.py > /app/logs/mcp_server.log 2>&1 &
        MCP_PID=$!
        echo $MCP_PID > /tmp/mcp_server.pid
        echo -e "\033[1;32mMCP server started in background (PID: $MCP_PID)\033[0m\n"
        # Wait for mcp_server to initialize
        sleep 5
        
        # Check MCP server status
        echo -e "\033[1;33m=== Checking MCP server status ===\033[0m\n"
        if python scripts/check_mcp_status.py; then
            echo -e "\033[1;32m✅ MCP server is running correctly\033[0m\n"
        else
            echo -e "\033[1;31m❌ MCP server check failed\033[0m\n"
        fi
    else
        echo -e "\033[1;33mSkipping MCP server startup\033[0m\n"
    fi
}

# Show usage guide
show_usage_guide() {
    echo -e "\033[1;32m=== NeoZork HLD Prediction Usage Guide (UV Mode) ===\033[0m\n"
    run_python_safely python run_analysis.py -h

    echo -e "\n\033[1;36m=== Container is ready for analysis (UV-Only Mode) ===\033[0m"

    # Show UV-specific tips
    echo -e "\n\033[1;36m=== UV Package Manager Commands ===\033[0m"
    echo -e "\033[1;36m- uv-install: Install dependencies using UV\033[0m"
    echo -e "\033[1;36m- uv-update: Update dependencies using UV\033[0m"
    echo -e "\033[1;36m- uv-test: Run UV environment test\033[0m"
    echo -e "\033[1;36m- uv-pytest: Run pytest with UV\033[0m"
    echo -e "\033[1;36m- uv pip install <package>: Install specific package\033[0m"
    echo -e "\033[1;36m- uv pip list: List installed packages\033[0m"

    # Show MCP server commands
    echo -e "\n\033[1;36m=== MCP Server Commands ===\033[0m"
    echo -e "\033[1;36m- mcp-start: Start MCP server\033[0m"
    echo -e "\033[1;36m- mcp-check: Check MCP server status\033[0m"

    # Show tips for viewing plots
    echo -e "\n\033[1;36m=== Tips for viewing plotly HTML plots ===\033[0m"
    echo -e "\033[1;36m1. Run a command like: python run_analysis.py demo --rule PHLD (or: nz demo --rule PHLD)\033[0m"
    echo -e "\033[1;36m2. Generated plots are saved to results/plots/*.html\033[0m"
    echo -e "\033[1;36m3. To access plots from native container:\033[0m"
    echo -e "\033[1;36m   - Check the results/plots directory in your project\033[0m"
    echo -e "\033[1;36m   - Open HTML files in your browser\033[0m"

    echo -e "\n\033[1;36mPress CTRL+C or Ctrl+D to stop the container\033[0m\n"
}

# Create a file with common commands for the interactive shell
create_commands_file() {
    cat > /tmp/neozork_commands.txt << EOL
# UV Package Manager Commands
uv-install
uv-update
uv-test
uv-pytest
uv pip list
uv pip install <package>

# Analysis Commands
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

# MCP Server Commands
mcp-start
mcp-check
python scripts/check_mcp_status.py
python neozork_mcp_server.py
EOL
}

# Main execution
main() {
    log_message "Starting NeoZork HLD Prediction Native Container..."
    
    # Create directories
    create_directories
    
    # Verify UV
    verify_uv
    
    # Setup bash environment
    setup_bash_environment
    
    # Create command wrappers
    create_command_wrappers
    
    # Welcome message
    echo -e "\n\033[1;36m=== NeoZork HLD Prediction Native Container Started (UV-Only Mode) ===\033[0m\n"

    # Check UV cache and dependencies
    echo -e "\033[1;33m=== Checking UV dependencies ===\033[0m"
    if [ -d "/app/.uv_cache" ]; then
        echo -e "\033[1;32m✅ UV cache directory exists\033[0m"
    else
        echo -e "\033[1;33m⚠️  UV cache directory not found, will be created on first use\033[0m"
    fi

    # Run data feed tests
    run_data_feed_tests
    
    # Start MCP server
    start_mcp_server
    
    # Show usage guide
    show_usage_guide
    
    # Create commands file
    create_commands_file
    
    # Initialize bash history
    init_bash_history
    
    echo -e "\033[1;32m=== Container initialization completed ===\033[0m"
    echo -e "\033[1;33mAvailable commands: nz, eda, uv-install, uv-update, uv-test, uv-pytest, mcp-start, mcp-check\033[0m"
    echo -e "\033[1;33mUse 'history' to see available commands, or press ↑/↓ to navigate\033[0m"
    echo -e "\033[1;33mType 'cat /tmp/neozork_commands.txt' to see all available commands\033[0m"
    echo
    
    # Start interactive bash shell
    exec bash -i
}

# Run main function
main "$@" 