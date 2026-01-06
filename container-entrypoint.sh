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

# Limit parallel compilation jobs to reduce memory usage during matplotlib build
export MAX_JOBS=2
export CMAKE_BUILD_PARALLEL_LEVEL=2
export NINJA_STATUS="[%f/%t] "

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
    mkdir -p /app/data/cache/uv_cache 2>/dev/null || true
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
        echo -e "\033[1;33m⚠️  UV is not available - installing UV...\033[0m"
        
        # Install UV using pip
        pip install uv
        
        if command -v uv &> /dev/null; then
            echo -e "\033[1;32m✅ UV installed successfully: $(uv --version)\033[0m"
        else
            echo -e "\033[1;31m❌ Failed to install UV - this is required for UV-only mode\033[0m"
            echo -e "\033[1;33m⚠️  Container will continue without UV-only mode\033[0m"
            export UV_ONLY=false
        fi
    fi

    # Test UV environment
    if [ -f "/app/scripts/utilities/test_uv_docker.py" ]; then
        if python /app/scripts/utilities/test_uv_docker.py; then
            echo -e "\033[1;32m✅ UV environment test passed\033[0m"
        else
            echo -e "\033[1;31m❌ UV environment test failed\033[0m"
        fi
    else
        echo -e "\033[1;33m⚠️  UV test script not found - skipping test\033[0m"
    fi
}

# Install system dependencies required for building Python packages
install_system_dependencies() {
    log_message "Installing system dependencies for building Python packages..."
    
    # Check if we're on Debian/Ubuntu (python:3.14-slim is Debian-based)
    if ! command -v apt-get &> /dev/null; then
        echo -e "\033[1;33m⚠️  apt-get not available - skipping system dependencies installation\033[0m"
        return 1
    fi
    
    # Check if gcc, pkg-config and matplotlib dependencies are already installed
    if command -v gcc &> /dev/null && \
       command -v pkg-config &> /dev/null && \
       [ -f /usr/include/zlib.h ] && \
       [ -f /usr/include/jpeglib.h ] && \
       [ -f /usr/include/png.h ] && \
       [ -f /usr/include/freetype2/freetype/freetype.h ]; then
        echo -e "\033[1;32m✅ Build tools and matplotlib dependencies already installed\033[0m"
        return 0
    fi
    
    echo -e "\033[1;33m📦 Installing build tools, PostgreSQL libraries, and matplotlib dependencies...\033[0m"
    
    # Set non-interactive mode
    export DEBIAN_FRONTEND=noninteractive
    
    # Update package list and install build dependencies with error handling
    if apt-get update -qq >/dev/null 2>&1; then
        if apt-get install -y --no-install-recommends \
            build-essential \
            gcc \
            g++ \
            pkg-config \
            libpq-dev \
            libpq5 \
            libffi-dev \
            libxml2-dev \
            libxslt1-dev \
            curl \
            zlib1g-dev \
            libjpeg-dev \
            libpng-dev \
            libfreetype6-dev \
            liblcms2-dev \
            libtiff-dev \
            libwebp-dev \
            libopenjp2-7-dev \
            >/dev/null 2>&1; then
            apt-get clean >/dev/null 2>&1
            rm -rf /var/lib/apt/lists/* >/dev/null 2>&1
            
            # Verify installation
            if command -v gcc &> /dev/null && \
               command -v pkg-config &> /dev/null && \
               [ -f /usr/include/zlib.h ] && \
               [ -f /usr/include/jpeglib.h ] && \
               [ -f /usr/include/png.h ] && \
               [ -f /usr/include/freetype2/freetype/freetype.h ]; then
                echo -e "\033[1;32m✅ System dependencies installed successfully (including matplotlib dependencies)\033[0m"
                return 0
            else
                echo -e "\033[1;33m⚠️  Installation completed but some dependencies may be missing\033[0m"
                return 1
            fi
        else
            echo -e "\033[1;33m⚠️  Failed to install packages - some packages may fail to build\033[0m"
            return 1
        fi
    else
        echo -e "\033[1;33m⚠️  Failed to update package list\033[0m"
        return 1
    fi
}

# Setup UV environment and install dependencies
setup_uv_environment() {
    log_message "=== Setting up UV Environment and Dependencies ==="
    
    # Install system dependencies first (don't fail if it doesn't work)
    install_system_dependencies || {
        echo -e "\033[1;33m⚠️  System dependencies installation failed - some packages may fail to build\033[0m"
        echo -e "\033[1;33m💡 You can install them manually: apt-get update && apt-get install -y build-essential gcc g++ libpq-dev libpq5 zlib1g-dev libjpeg-dev libpng-dev libfreetype6-dev liblcms2-dev libtiff-dev libwebp-dev libopenjp2-7-dev\033[0m"
    }
    
    # Check if virtual environment exists
    if [ ! -d "/app/.venv" ]; then
        echo -e "\033[1;33m📦 Virtual environment not found - creating new venv...\033[0m"
        
        # Create virtual environment
        if uv venv /app/.venv; then
            echo -e "\033[1;32m✅ Virtual environment created successfully\033[0m"
        else
            echo -e "\033[1;31m❌ Failed to create virtual environment\033[0m"
            echo -e "\033[1;33m⚠️  Continuing without virtual environment\033[0m"
            return 0
        fi
    else
        echo -e "\033[1;32m✅ Virtual environment already exists\033[0m"
    fi
    
    # Activate virtual environment
    echo -e "\033[1;33m🔄 Activating virtual environment...\033[0m"
    source /app/.venv/bin/activate
    
    # Check if dependencies are already installed
    if [ -f "/app/.venv/pyvenv.cfg" ] && [ -d "/app/.venv/lib" ]; then
        echo -e "\033[1;32m✅ Virtual environment is properly configured\033[0m"
        
        # Check if key packages are installed
        if uv pip list | grep -q "pandas"; then
            echo -e "\033[1;32m✅ Dependencies appear to be installed\033[0m"
            echo -e "\033[1;33m🔄 Checking for dependency updates...\033[0m"
            
            # Update dependencies if needed (don't fail on error)
            if uv pip install --upgrade -r /app/requirements.txt; then
                echo -e "\033[1;32m✅ Dependencies updated successfully\033[0m"
            else
                echo -e "\033[1;33m⚠️  Dependency update had issues - continuing anyway\033[0m"
            fi
        else
            echo -e "\033[1;33m📦 Installing dependencies...\033[0m"
            install_dependencies
        fi
    else
        echo -e "\033[1;33m📦 Installing dependencies...\033[0m"
        install_dependencies
    fi
    
    # Verify installation (don't fail on error)
    verify_dependencies || true
}

# Install dependencies using UV
install_dependencies() {
    echo -e "\033[1;33m📦 Installing dependencies from requirements.txt...\033[0m"
    
    # Set environment variables to limit parallel compilation
    export MAX_JOBS=2
    export CMAKE_BUILD_PARALLEL_LEVEL=2
    
    # Install dependencies (don't fail on error)
    if uv pip install -r /app/requirements.txt; then
        echo -e "\033[1;32m✅ Dependencies installed successfully\033[0m"
        return 0
    else
        echo -e "\033[1;31m❌ Failed to install dependencies\033[0m"
        echo -e "\033[1;33m⚠️  You can try manual installation with: uv-install\033[0m"
        echo -e "\033[1;33m⚠️  Continuing without dependencies - they can be installed later\033[0m"
        return 0
    fi
}

# Verify that key dependencies are installed
verify_dependencies() {
    echo -e "\033[1;33m🔍 Verifying key dependencies...\033[0m"
    
    # List of key packages to verify
    key_packages=("pandas" "numpy" "matplotlib" "plotly" "yfinance" "pytest")
    missing_packages=()
    
    for package in "${key_packages[@]}"; do
        if uv pip list | grep -q "$package"; then
            echo -e "\033[1;32m✅ $package is installed\033[0m"
        else
            echo -e "\033[1;31m❌ $package is missing\033[0m"
            missing_packages+=("$package")
        fi
    done
    
    if [ ${#missing_packages[@]} -eq 0 ]; then
        echo -e "\033[1;32m✅ All key dependencies are installed\033[0m"
        return 0
    else
        echo -e "\033[1;33m⚠️  Some packages are missing: ${missing_packages[*]}\033[0m"
        echo -e "\033[1;33m⚠️  You can try manual installation with: uv-install\033[0m"
        return 1
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
    
    # Create .bashrc for automatic venv activation
    cat > /tmp/bash_config/.bashrc << EOL
# Auto-activate virtual environment
if [ -f "/app/.venv/bin/activate" ]; then
    source /app/.venv/bin/activate
    echo -e "\033[1;32m✅ Virtual environment activated\033[0m"
fi

# Add /tmp/bin to PATH for command wrappers
export PATH="/tmp/bin:\$PATH"

# Show available commands
if [ -f "/tmp/neozork_commands.txt" ]; then
    echo -e "\033[1;36m💡 Available commands: cat /tmp/neozork_commands.txt\033[0m"
fi
EOL
    
    # Set BASH_ENV to load our configuration
    export BASH_ENV=/tmp/bash_config/.bashrc
}

# Create command wrapper scripts
create_command_wrappers() {
    log_message "Creating command wrapper scripts..."
    
    mkdir -p /tmp/bin

    # Create nz command wrapper script with venv activation
    cat > /tmp/bin/nz << 'EOF'
#!/bin/bash
source /app/.venv/bin/activate
python /app/run_analysis.py "$@"
EOF
    chmod +x /tmp/bin/nz

    # Create eda command wrapper script with venv activation
    cat > /tmp/bin/eda << 'EOF'
#!/bin/bash
source /app/.venv/bin/activate
python /app/src/eda/eda_batch_check.py "$@"
EOF
    chmod +x /tmp/bin/eda

    # Create uv command wrappers for better UX
    cat > /tmp/bin/uv-install << 'EOF'
#!/bin/bash
echo "Installing dependencies using UV..."
source /app/.venv/bin/activate
uv pip install -r /app/requirements.txt
EOF
    chmod +x /tmp/bin/uv-install

    cat > /tmp/bin/uv-update << 'EOF'
#!/bin/bash
echo "Updating dependencies using UV..."
source /app/.venv/bin/activate
uv pip install --upgrade -r /app/requirements.txt
EOF
    chmod +x /tmp/bin/uv-update

    cat > /tmp/bin/uv-test << 'EOF'
#!/bin/bash
echo "Running UV environment test..."
source /app/.venv/bin/activate
python /app/scripts/test_uv_docker.py
EOF
    chmod +x /tmp/bin/uv-test

    # Create pytest wrapper for UV
    cat > /tmp/bin/uv-pytest << 'EOF'
#!/bin/bash
echo "Running pytest with UV..."
source /app/.venv/bin/activate
uv run pytest tests -n auto
EOF
    chmod +x /tmp/bin/uv-pytest

    # Create safe test runner for native container
    cat > /tmp/bin/uv-test-safe << 'EOF'
#!/bin/bash
echo "Running safe tests for native container..."
source /app/.venv/bin/activate
/app/scripts/run_tests_native_container.sh
EOF
    chmod +x /tmp/bin/uv-test-safe

    # Create MCP server wrapper with venv activation
    cat > /tmp/bin/mcp-start << 'EOF'
#!/bin/bash
echo "Starting MCP server..."
source /app/.venv/bin/activate
nohup python /app/neozork_mcp_server.py > /app/logs/mcp_server.log 2>&1 &
MCP_PID=$!
echo $MCP_PID > /tmp/mcp_server.pid
echo "MCP server started with PID: $MCP_PID"
EOF
    chmod +x /tmp/bin/mcp-start

    cat > /tmp/bin/mcp-check << 'EOF'
#!/bin/bash
echo "Checking MCP server status..."
source /app/.venv/bin/activate
python /app/scripts/check_mcp_status.py
EOF
    chmod +x /tmp/bin/mcp-check

    # Create system dependencies installer wrapper
    cat > /tmp/bin/install-system-deps << 'EOF'
#!/bin/bash
echo "Installing system dependencies for building Python packages (including matplotlib)..."
export DEBIAN_FRONTEND=noninteractive
apt-get update -qq -y
apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    g++ \
    pkg-config \
    libpq-dev \
    libpq5 \
    libffi-dev \
    libxml2-dev \
    libxslt1-dev \
    zlib1g-dev \
    libjpeg-dev \
    libpng-dev \
    libfreetype6-dev \
    liblcms2-dev \
    libtiff-dev \
    libwebp-dev \
    libopenjp2-7-dev \
    >/dev/null 2>&1
apt-get clean >/dev/null 2>&1
rm -rf /var/lib/apt/lists/* >/dev/null 2>&1
echo "System dependencies installed successfully (including matplotlib build dependencies)"
EOF
    chmod +x /tmp/bin/install-system-deps

    export PATH="/tmp/bin:$PATH"
}

# Function to handle errors without exiting container
run_python_safely() {
    # Activate virtual environment
    source /app/.venv/bin/activate
    
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
        "uv run pytest tests -n auto -v --tb=short"
        "uv run pytest tests -n auto -v --tb=short -x"
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
        "python scripts/debug/debug_yfinance.py"
        "python scripts/debug/debug_binance.py"
        "python scripts/debug/debug_polygon.py"
        "python scripts/debug/examine_parquet.py"
        "python scripts/mcp/start_mcp_server_daemon.py"
        "python scripts/mcp/neozork_mcp_manager.py"
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
    # Check if running in interactive mode
    if [ -t 0 ]; then
        echo -e "\033[1;33mWould you like to run tests for external data feeds? (Polygon, YFinance, Binance) [y/N]:\033[0m"
        read -r run_tests

        # Debug output to check what was read
        echo -e "\033[1;34mInput received: '$run_tests'\033[0m"

        # Simplified condition checking
        if [ "$run_tests" = "y" ] || [ "$run_tests" = "Y" ]; then
            echo -e "\n\033[1;32m=== Running external data feed tests in Native Container (UV Mode) ===\033[0m\n"
            # Run the tests using the Docker-specific test runner
            source /app/.venv/bin/activate
            run_python_safely python /app/tests/run_tests_docker.py
        else
            echo -e "\033[1;33mSkipping external data feed tests\033[0m\n"
        fi
    else
        echo -e "\033[1;33mNon-interactive mode - skipping external data feed tests\033[0m\n"
    fi
}

# Start MCP server
start_mcp_server() {
    # Check if running in interactive mode
    if [ -t 0 ]; then
        echo -e "\033[1;33mWould you like to start the MCP service for enhanced LLM support? [y/N]:\033[0m"
        read -r run_mcp

        # Debug output to check what was read
        echo -e "\033[1;34mInput received: '$run_mcp'\033[0m"

        # Simplified condition checking
        if [ "$run_mcp" = "y" ] || [ "$run_mcp" = "Y" ]; then
            echo -e "\n\033[1;32m=== Starting MCP server in background (UV Mode) ===\033[0m\n"
            # Start MCP server in background and redirect output to prevent EOF
            source /app/.venv/bin/activate
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
    else
        echo -e "\033[1;33mNon-interactive mode - skipping MCP server startup\033[0m\n"
    fi
}

# Show usage guide
show_usage_guide() {
    echo -e "\033[1;32m=== NeoZork HLD Prediction Usage Guide (UV Mode) ===\033[0m\n"
    
    # Try to show help, but don't fail if dependencies are missing
    if source /app/.venv/bin/activate 2>/dev/null; then
        if python run_analysis.py -h 2>/dev/null; then
            echo -e "\033[1;32m✅ Help command executed successfully\033[0m"
        else
            echo -e "\033[1;33m⚠️  Help command failed - dependencies may not be installed\033[0m"
            echo -e "\033[1;33m💡 Run 'uv-install' to install dependencies\033[0m"
        fi
    else
        echo -e "\033[1;33m⚠️  Virtual environment not available\033[0m"
        echo -e "\033[1;33m💡 Run 'uv-install' to setup environment\033[0m"
    fi

    echo -e "\n\033[1;36m=== Container is ready for analysis (UV-Only Mode) ===\033[0m"

    # Show UV-specific tips
    echo -e "\n\033[1;36m=== UV Package Manager Commands ===\033[0m"
    echo -e "\033[1;36m- install-system-deps: Install system dependencies for building Python packages\033[0m"
    echo -e "\033[1;36m- uv-install: Install dependencies using UV\033[0m"
    echo -e "\033[1;36m- uv-update: Update dependencies using UV\033[0m"
    echo -e "\033[1;36m- uv-test: Run UV environment test\033[0m"
    echo -e "\033[1;36m- uv-pytest: Run pytest with UV\033[0m"
    echo -e "\033[1;36m- uv-test-safe: Run safe tests for native container\033[0m"
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
# System Dependencies
install-system-deps

# UV Package Manager Commands
uv-install
uv-update
uv-test
uv-pytest
uv pip list
uv pip install <package>

# Testing Commands
pytest
uv run pytest tests -n auto
uv run pytest tests -n auto -v --tb=short
uv run pytest tests -n auto -v --tb=short -x
uv run pytest tests -n auto --tb=no -q
uv-test-safe

# Analysis Commands
nz
eda
python
python run_analysis.py demo --rule PHLD
nz demo --rule PHLD
python run_analysis.py yfinance MSFT --rule PHLD
nz yfinance AAPL --rule PHLD
python run_analysis.py mql5 EURUSD --interval H4 --rule PHLD
nz mql5 BTCUSD --interval H4 --rule PHLD
ls results/plots/

# Debug Commands
python scripts/debug/debug_yfinance.py
python scripts/debug/debug_binance.py
python scripts/debug/debug_polygon.py
python scripts/debug/examine_parquet.py
python scripts/debug/debug_check_parquet.py

# MCP Server Commands
mcp-start
mcp-check
python scripts/check_mcp_status.py
python scripts/mcp/start_mcp_server_daemon.py
python scripts/mcp/neozork_mcp_manager.py
python neozork_mcp_server.py
EOL
}

# Initialize container (called by preStart hook)
init_container() {
    log_message "Initializing container..."
    create_directories
    log_message "Container initialization completed"
}

# Post-start actions (called by postStart hook)
post_start() {
    log_message "Post-start actions completed"
}

# Main execution
main() {
    log_message "Starting NeoZork HLD Prediction container..."
    
    # Handle command line arguments
    case "${1:-}" in
        "init")
            init_container
            ;;
        "post-start")
            post_start
            ;;
        *)
            # Default behavior - full container initialization
            log_message "=== Full Container Initialization ==="
            
            # Step 1: Create directories
            create_directories
            
            # Step 2: Verify UV
            verify_uv
            
            # Step 3: Setup UV environment and install dependencies
            # Don't fail if setup fails - allow manual installation later
            setup_uv_environment || {
                echo -e "\033[1;33m⚠️  UV environment setup had issues - you can install dependencies manually later\033[0m"
                echo -e "\033[1;33m💡 Run 'uv-install' inside the container to install dependencies\033[0m"
            }
            
            # Step 4: Setup bash environment
            setup_bash_environment
            
            # Step 5: Create command wrappers
            create_command_wrappers
            
            # Step 6: Initialize bash history
            init_bash_history
            
            # Step 7: Create commands file
            create_commands_file
            
            # Step 8: Show usage guide
            show_usage_guide
            
            # Step 9: Run data feed tests (interactive)
            run_data_feed_tests
            
            # Step 10: Start MCP server (interactive)
            start_mcp_server
            
            log_message "=== Container initialization completed ==="
            
            # Check if running in interactive mode
            if [ -t 0 ]; then
                log_message "Container is ready for use. Entering interactive mode..."
                # Start interactive bash shell
                exec bash
            else
                log_message "Container is ready for use. Running in non-interactive mode..."
                # Keep container running in background
                tail -f /dev/null
            fi
            ;;
    esac
}

# Run main function
main "$@" 