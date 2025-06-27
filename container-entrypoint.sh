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

# Function to handle errors without exiting container
run_python_safely() {
    log_message "Running: $*"
    "$@"
    local exit_code=$?

    if [ $exit_code -ne 0 ]; then
        log_message "ERROR: Command failed with exit code $exit_code"
        log_message "Container will remain running. You can try another command."
        return $exit_code
    fi

    # Check if HTML files were created in results/plots directory
    if [ -d "/app/results/plots" ]; then
        latest_html=$(find /app/results/plots -name "*.html" -type f -printf "%T@ %p\n" 2>/dev/null | sort -n | tail -1 | cut -f2- -d" ")

        if [ -n "$latest_html" ]; then
            mod_time=$(stat -c %Y "$latest_html" 2>/dev/null || echo "0")
            current_time=$(date +%s)
            if [ $((current_time - mod_time)) -lt 10 ]; then
                log_message "New HTML file generated: $latest_html"
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
            log_message "Stopping MCP server (PID: $MCP_PID)..."
            kill $MCP_PID
            wait $MCP_PID 2>/dev/null
            log_message "MCP server stopped"
        fi
        rm -f /tmp/mcp_server.pid
    fi
}

# Set trap to cleanup MCP server on script exit
trap cleanup_mcp_server EXIT

# Set PYTHONPATH globally
export PYTHONPATH=/app

# Create necessary directories with appropriate permissions
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

    chmod -R 777 /tmp/matplotlib-cache /app/results /app/data /app/logs /app/.pytest_cache /app/.uv_cache /app/.venv /tmp/bash_history /tmp/bin
}

# Initialize UV environment
init_uv_environment() {
    log_message "Initializing UV environment..."
    
    # Check if UV is available
    if ! command -v uv &> /dev/null; then
        log_message "ERROR: UV is not available - installing..."
        curl -sSL https://github.com/astral-sh/uv/releases/latest/download/uv-installer.sh | bash
        export PATH="/root/.local/bin:$PATH"
    fi

    log_message "UV version: $(uv --version)"

    # Initialize UV project if not already done
    if [ ! -f "/app/uv.toml" ]; then
        log_message "Initializing UV project..."
        uv init --python 3.11
    fi

    # Install dependencies
    log_message "Installing dependencies with UV..."
    uv pip install -r requirements.txt
}

# Create command wrappers
create_command_wrappers() {
    log_message "Creating command wrappers..."

    # Create nz command wrapper
    cat > /tmp/bin/nz << 'EOF'
#!/bin/bash
python /app/run_analysis.py "$@"
EOF
    chmod +x /tmp/bin/nz

    # Create eda command wrapper
    cat > /tmp/bin/eda << 'EOF'
#!/bin/bash
python /app/src/eda/eda_batch_check.py "$@"
EOF
    chmod +x /tmp/bin/eda

    # Create UV command wrappers
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

    export PATH="/tmp/bin:$PATH"
}

# Setup bash environment
setup_bash_environment() {
    log_message "Setting up bash environment..."
    
    # Create history file
    export HISTFILE=/tmp/bash_history/.bash_history
    export HISTSIZE=1000
    export HISTCONTROL=ignoreboth
    touch $HISTFILE
    chmod 666 $HISTFILE

    # Create inputrc for better shell experience
    mkdir -p /tmp/bash_config
    printf '%s\n' '"\\e[A": history-search-backward' > /tmp/bash_config/.inputrc
    printf '%s\n' '"\\e[B": history-search-forward' >> /tmp/bash_config/.inputrc
    chmod -R 777 /tmp/bash_config
}

# Initialize container
init_container() {
    log_message "=== NeoZork HLD Prediction Native Container Initialization ==="
    
    create_directories
    init_uv_environment
    create_command_wrappers
    setup_bash_environment
    
    log_message "Container initialization complete"
}

# Post-start actions
post_start() {
    log_message "=== Post-start actions ==="
    
    # Run UV environment test
    if [ -f "/app/scripts/test_uv_docker.py" ]; then
        log_message "Running UV environment test..."
        python /app/scripts/test_uv_docker.py
        if [ $? -eq 0 ]; then
            log_message "UV environment test passed"
        else
            log_message "WARNING: UV environment test had issues"
        fi
    fi
}

# Main interactive mode
interactive_mode() {
    log_message "=== NeoZork HLD Prediction Native Container Started ==="
    
    # Show welcome message
    echo -e "\n\033[1;36m=== NeoZork HLD Prediction Native Container (UV-Only Mode) ===\033[0m\n"
    
    # Check UV cache and dependencies
    echo -e "\033[1;33m=== Checking UV dependencies ===\033[0m"
    if [ -d "/app/.uv_cache" ]; then
        echo -e "\033[1;32m✅ UV cache directory exists\033[0m"
    else
        echo -e "\033[1;33m⚠️  UV cache directory not found, will be created on first use\033[0m"
    fi

    # Ask about running tests
    echo -e "\033[1;33mWould you like to run tests for external data feeds? (Polygon, YFinance, Binance) [y/N]:\033[0m"
    read -r run_tests

    if [ "$run_tests" = "y" ] || [ "$run_tests" = "Y" ]; then
        echo -e "\n\033[1;32m=== Running external data feed tests in Native Container (UV Mode) ===\033[0m\n"
        run_python_safely python /app/tests/run_tests_docker.py
    else
        echo -e "\033[1;33mSkipping external data feed tests\033[0m\n"
    fi

    # Ask about MCP server
    echo -e "\033[1;33mWould you like to start the MCP service for enhanced LLM support? [y/N]:\033[0m"
    read -r run_mcp

    if [ "$run_mcp" = "y" ] || [ "$run_mcp" = "Y" ]; then
        echo -e "\n\033[1;32m=== Starting MCP server in background (UV Mode) ===\033[0m\n"
        nohup python neozork_mcp_server.py > /app/logs/mcp_server.log 2>&1 &
        MCP_PID=$!
        echo $MCP_PID > /tmp/mcp_server.pid
        echo -e "\033[1;32mMCP server started in background (PID: $MCP_PID)\033[0m\n"
        sleep 5
        
        echo -e "\033[1;33m=== Checking MCP server status ===\033[0m\n"
        if python scripts/check_mcp_status.py; then
            echo -e "\033[1;32m✅ MCP server is running correctly\033[0m\n"
        else
            echo -e "\033[1;31m❌ MCP server check failed\033[0m\n"
        fi
    else
        echo -e "\033[1;33mSkipping MCP server startup\033[0m\n"
    fi

    # Show help
    echo -e "\033[1;32m=== NeoZork HLD Prediction Usage Guide (UV Mode) ===\033[0m\n"
    run_python_safely python run_analysis.py -h

    echo -e "\n\033[1;36m=== Container is ready for analysis (UV-Only Mode) ===\033[0m"

    # Show UV-specific tips
    echo -e "\n\033[1;36m=== UV Package Manager Commands ===\033[0m"
    echo -e "\033[1;36m- uv-install: Install dependencies using UV\033[0m"
    echo -e "\033[1;36m- uv-update: Update dependencies using UV\033[0m"
    echo -e "\033[1;36m- uv-test: Run UV environment test\033[0m"
    echo -e "\033[1;36m- nz: Main analysis command\033[0m"
    echo -e "\033[1;36m- eda: EDA analysis command\033[0m"

    # Start interactive shell
    exec bash
}

# Main script logic
case "${1:-interactive}" in
    "init")
        init_container
        ;;
    "post-start")
        post_start
        ;;
    "interactive"|*)
        init_container
        interactive_mode
        ;;
esac 