#!/bin/bash

# Native Container Exec Script for NeoZork HLD Prediction
# This script executes commands inside the running native Apple Silicon container

# Don't exit on error - we want to handle errors gracefully
set +e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if container exists
check_container_exists() {
    if container list --all | grep -q "neozork-hld-prediction"; then
        return 0
    else
        return 1
    fi
}

# Function to check if container is running
check_container_running() {
    if container list | grep -q "neozork-hld-prediction"; then
        return 0
    else
        return 1
    fi
}

# Function to get container ID
get_container_id() {
    container list | grep "neozork-hld-prediction" | awk '{print $1}'
}

# Function to create enhanced shell command with venv activation and UV setup
create_enhanced_shell_command() {
    cat << 'EOF'
#!/bin/bash

# Enhanced shell startup for NeoZork HLD Prediction container
# Automatically activates virtual environment and installs dependencies

echo "=== NeoZork HLD Prediction Container Shell ==="
echo "Setting up environment..."

# Set non-interactive mode for apt
export DEBIAN_FRONTEND=noninteractive

# Update package list and install essential tools and build dependencies
echo "Installing essential tools and build dependencies..."
apt-get update -qq -y
apt-get install -y -qq --no-install-recommends \
    curl wget git \
    build-essential \
    gcc \
    g++ \
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
    >/dev/null 2>&1 || true
apt-get clean >/dev/null 2>&1 || true
rm -rf /var/lib/apt/lists/* >/dev/null 2>&1 || true

# Check if we're in the right directory
if [ ! -f "/app/requirements.txt" ]; then
    echo "Error: requirements.txt not found. Are you in the correct directory?"
    exit 1
fi

# Check if UV is available, install if not
if ! command -v uv >/dev/null 2>&1; then
    echo "Installing UV package manager..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.cargo/bin:$PATH"
    # Also add to system PATH for this session
    export PATH="/root/.cargo/bin:$PATH"
fi

# Check if virtual environment exists
if [ ! -d "/app/.venv" ]; then
    echo "Creating virtual environment..."
    uv venv /app/.venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source /app/.venv/bin/activate

# Check if dependencies are installed
# Note: Python version path may vary (3.11, 3.14, etc.)
if [ ! -f "/app/.venv/pyvenv.cfg" ] || [ ! -d "/app/.venv/lib" ]; then
    echo "Installing dependencies with UV..."
    uv pip install -r /app/requirements.txt
else
    echo "Checking for dependency updates..."
    uv pip install -r /app/requirements.txt --upgrade
fi

# Set up environment variables
# Ensure PATH includes UV installation directory (~/.local/bin)
export PATH="$HOME/.local/bin:/root/.local/bin:$HOME/.cargo/bin:/root/.cargo/bin:$PATH"
export PYTHONPATH="/app:$PYTHONPATH"
export PYTHONUNBUFFERED=1
export PYTHONDONTWRITEBYTECODE=1
export MPLCONFIGDIR="/tmp/matplotlib-cache"

# Create useful aliases
alias nz="python /app/run_analysis.py"
alias eda="python /app/scripts/eda_script.py"
alias uv-install="uv pip install --no-build-isolation --prefer-binary -r /app/requirements.txt"
alias uv-update="uv pip install --no-build-isolation --prefer-binary --upgrade -r /app/requirements.txt"
alias uv-test="uv run python -c 'import sys; print(f\"Python {sys.version}\"); import pandas, numpy, matplotlib; print(\"Core packages imported successfully\")'"
alias uv-pytest="uv run pytest tests/ -n auto"

echo "Environment setup complete!"
echo "Available commands: nz, eda, uv-install, uv-update, uv-test, uv-pytest"
echo "Type 'exit' to leave the container shell"
echo ""

# Start interactive bash shell
exec bash
EOF
}

# Function to execute command in container
execute_in_container() {
    local container_id=$1
    local command=$2
    local interactive=$3
    
    print_status "Executing command in container: $container_id"
    print_status "Command: $command"
    
    # Ensure enhanced shell script exists (it has all the setup logic including UV installation)
    # If it doesn't exist, trigger its creation by calling execute_enhanced_shell setup
    if ! container exec "$container_id" test -f /tmp/enhanced_shell.sh 2>/dev/null; then
        print_status "Setting up environment (creating enhanced shell script)..."
        # Create enhanced shell script using the same method as execute_enhanced_shell
        # We'll create a simplified command wrapper that uses the same setup logic
        local temp_script=$(mktemp)
        cat > "$temp_script" << 'CMD_WRAPPER_EOF'
#!/bin/bash
# Command wrapper that sets up environment and executes a command
# Set PATH to include UV installation directory (~/.local/bin)
export PATH="$HOME/.local/bin:/root/.local/bin:$HOME/.cargo/bin:/root/.cargo/bin:$PATH"
export PYTHONPATH="/app:$PYTHONPATH"
export PYTHONUNBUFFERED=1
export PYTHONDONTWRITEBYTECODE=1
export MPLCONFIGDIR="/tmp/matplotlib-cache"
cd /app

# Install system dependencies if needed (gcc, build-essential)
# This MUST complete synchronously before running commands
if ! command -v gcc >/dev/null 2>&1; then
    export DEBIAN_FRONTEND=noninteractive
    # Install synchronously - wait for completion
    apt-get update -qq -y >/dev/null 2>&1
    apt-get install -y --no-install-recommends \
        build-essential \
        gcc \
        g++ \
        pkg-config \
        curl \
        libpq-dev \
        libpq5 \
        libffi-dev \
        libxml2-dev \
        libxslt1-dev \
        zlib1g-dev \
        libjpeg-dev \
        libpng-dev \
        libfreetype6-dev \
        >/dev/null 2>&1
    apt-get clean >/dev/null 2>&1
    rm -rf /var/lib/apt/lists/* >/dev/null 2>&1
    # Verify installation completed
    if ! command -v gcc >/dev/null 2>&1; then
        echo "ERROR: Failed to install gcc" >&2
        exit 1
    fi
fi

# Install UV if not available
if ! command -v uv >/dev/null 2>&1; then
    # Check if curl is available
    if ! command -v curl >/dev/null 2>&1; then
        # Install curl first if needed
        export DEBIAN_FRONTEND=noninteractive
        apt-get update -qq -y >/dev/null 2>&1
        apt-get install -y --no-install-recommends curl >/dev/null 2>&1
    fi
    # Install UV
    if command -v curl >/dev/null 2>&1; then
        curl -LsSf https://astral.sh/uv/install.sh | sh >/dev/null 2>&1
        # UV installs to ~/.local/bin, update PATH
        export PATH="$HOME/.local/bin:/root/.local/bin:$HOME/.cargo/bin:/root/.cargo/bin:$PATH"
    fi
fi

# Activate venv if it exists
if [ -f /app/.venv/bin/activate ]; then
    source /app/.venv/bin/activate
fi

# Execute the command passed as argument
# Use eval to properly handle commands with multiple arguments
eval "$@"
CMD_WRAPPER_EOF
        container exec -i "$container_id" bash -c "cat > /tmp/cmd_wrapper.sh" < "$temp_script"
        rm -f "$temp_script"
        container exec "$container_id" chmod +x /tmp/cmd_wrapper.sh
    fi
    
    # Build exec command
    local exec_cmd="container exec"
    
    if [ "$interactive" = true ]; then
        exec_cmd="$exec_cmd --interactive --tty"
    fi
    
    # Use command wrapper if it exists, otherwise use enhanced shell script
    # Properly escape the command for execution
    if container exec "$container_id" test -f /tmp/cmd_wrapper.sh 2>/dev/null; then
        # Use command wrapper - properly quote the command
        local wrapped_command="bash -c \"/tmp/cmd_wrapper.sh $command\""
    elif container exec "$container_id" test -f /tmp/enhanced_shell.sh 2>/dev/null; then
        # Use enhanced shell script - execute command through the shell
        # First ensure system dependencies are installed, then setup environment, then run command
        local wrapped_command="bash -c '
            # Step 1: Install system dependencies if needed (gcc, build-essential, etc.)
            # This MUST complete synchronously before running the command
            if ! command -v gcc >/dev/null 2>&1; then
                echo \"Installing system dependencies (gcc, build-essential)...\" >&2
                export DEBIAN_FRONTEND=noninteractive
                # Install synchronously - wait for completion
                apt-get update -qq -y >/dev/null 2>&1
                apt-get install -y --no-install-recommends \
                    build-essential \
                    gcc \
                    g++ \
                    pkg-config \
                    curl \
                    libpq-dev \
                    libpq5 \
                    libffi-dev \
                    libxml2-dev \
                    libxslt1-dev \
                    zlib1g-dev \
                    libjpeg-dev \
                    libpng-dev \
                    libfreetype6-dev \
                    >/dev/null 2>&1
                apt-get clean >/dev/null 2>&1
                rm -rf /var/lib/apt/lists/* >/dev/null 2>&1
                # Verify installation completed
                if ! command -v gcc >/dev/null 2>&1; then
                    echo \"ERROR: Failed to install gcc\" >&2
                    exit 1
                fi
            fi
            
            # Step 2: Execute setup from enhanced_shell.sh (before interactive shell)
            setup_part=\$(sed -n \"/^# Start interactive bash shell/q\" /tmp/enhanced_shell.sh 2>/dev/null)
            if [ -n \"\$setup_part\" ]; then
                # Execute setup synchronously
                echo \"\$setup_part\" | bash
                # Wait for background jobs (UV installation)
                wait 2>/dev/null || true
            fi
            
            # Step 3: Ensure PATH is correct (UV installs to ~/.local/bin)
            export PATH=\"\$HOME/.local/bin:/root/.local/bin:\$HOME/.cargo/bin:/root/.cargo/bin:\$PATH\"
            
            # Step 4: If UV still not found, install it synchronously
            if ! command -v uv >/dev/null 2>&1; then
                if command -v curl >/dev/null 2>&1; then
                    echo \"Installing UV package manager...\" >&2
                    curl -LsSf https://astral.sh/uv/install.sh | sh >/dev/null 2>&1
                    export PATH=\"\$HOME/.local/bin:/root/.local/bin:\$HOME/.cargo/bin:/root/.cargo/bin:\$PATH\"
                fi
            fi
            
            # Step 5: Execute the command
            cd /app
            $command
        '"
    else
        # Fallback: basic setup with system dependencies and UV installation
        local wrapped_command="bash -c '
            # Install system dependencies if needed
            if ! command -v gcc >/dev/null 2>&1; then
                export DEBIAN_FRONTEND=noninteractive
                apt-get update -qq -y >/dev/null 2>&1 && \
                apt-get install -y --no-install-recommends build-essential gcc g++ pkg-config curl libpq-dev libpq5 libffi-dev libxml2-dev libxslt1-dev >/dev/null 2>&1
            fi
            # Set PATH for UV (installs to ~/.local/bin)
            export PATH=\"\$HOME/.local/bin:/root/.local/bin:\$HOME/.cargo/bin:/root/.cargo/bin:\$PATH\"
            # Install UV if needed
            if ! command -v uv >/dev/null 2>&1 && command -v curl >/dev/null 2>&1; then
                curl -LsSf https://astral.sh/uv/install.sh | sh >/dev/null 2>&1
                export PATH=\"\$HOME/.local/bin:/root/.local/bin:\$HOME/.cargo/bin:/root/.cargo/bin:\$PATH\"
            fi
            export PYTHONPATH=\"/app:\$PYTHONPATH\"
            cd /app
            $command
        '"
    fi
    
    exec_cmd="$exec_cmd $container_id $wrapped_command"
    
    # Execute command
    eval "$exec_cmd"
}

# Function to execute enhanced shell in container
execute_enhanced_shell() {
    local container_id=$1
    
    print_status "Starting enhanced shell with automatic venv activation and UV setup..."
    
    # Create temporary script file in container using heredoc
    # Use a temporary file approach to avoid stdin issues when called from menu
    print_status "Creating enhanced shell script in container..."
    # Create script on host first, then copy to container
    local temp_script=$(mktemp)
    cat > "$temp_script" << 'ENHANCED_SHELL_EOF'
#!/bin/bash

# Enhanced shell startup for NeoZork HLD Prediction container
# Automatically activates virtual environment and installs dependencies
# Includes proper Ctrl+D handling and graceful exit

# Set up signal handlers for graceful exit
trap "echo \"Exiting container shell...\"; exit 0" EXIT
trap "echo \"Received interrupt signal, exiting...\"; exit 0" INT TERM

# Function to handle Ctrl+D gracefully
handle_eof() {
    echo ""
    echo "Received EOF (Ctrl+D), exiting gracefully..."
    exit 0
}

# Set up EOF handler (using EXIT instead of EOF)
trap handle_eof EXIT

# IMPORTANT: Set PATH first to include UV installation directory
# UV installs to ~/.local/bin, so we need to add it to PATH immediately
export PATH="$HOME/.local/bin:/root/.local/bin:$HOME/.cargo/bin:/root/.cargo/bin:$PATH"

# Set non-interactive mode for apt
export DEBIAN_FRONTEND=noninteractive

# Change to app directory first
cd /app

# Quick check: if venv exists and has packages, skip most setup
pandas_found=false
if [ -d "/app/.venv" ] && [ -f "/app/.venv/pyvenv.cfg" ]; then
    # Try to find pandas in site-packages (check common Python versions)
    for pyver in python3.14 python3.13 python3.12 python3.11 python3.10; do
        if [ -f "/app/.venv/lib/${pyver}/site-packages/pandas/__init__.py" ] 2>/dev/null; then
            pandas_found=true
            break
        fi
    done
fi

if [ "$pandas_found" = true ]; then
    # Already set up, just activate and continue
    # Ensure PATH includes UV installation directory
    export PATH="$HOME/.local/bin:/root/.local/bin:$HOME/.cargo/bin:/root/.cargo/bin:$PATH"
    # Check and install UV if not available
    if ! command -v uv >/dev/null 2>&1; then
        if command -v curl >/dev/null 2>&1; then
            curl -LsSf https://astral.sh/uv/install.sh | sh >/dev/null 2>&1
            export PATH="$HOME/.local/bin:/root/.local/bin:$HOME/.cargo/bin:/root/.cargo/bin:$PATH"
        fi
    fi
    echo -e "\033[1;32m✓\033[0m Environment ready"
    source .venv/bin/activate 2>/dev/null || true
    export VIRTUAL_ENV_SETUP_SKIPPED=1
else
    # Full setup needed
    echo "=== NeoZork HLD Prediction Container Shell ==="
    echo "Setting up environment (this may take 1-3 minutes on first run)..."
    echo ""
    
    # Check if essential tools and build tools are already installed (skip if present)
    tools_needed=false
    if ! command -v curl >/dev/null 2>&1 || ! command -v wget >/dev/null 2>&1 || ! command -v git >/dev/null 2>&1; then
        tools_needed=true
    fi
    if ! command -v gcc >/dev/null 2>&1; then
        tools_needed=true
    fi
    
    if [ "$tools_needed" = true ]; then
        echo -n "📦 Installing essential tools and build dependencies (15-45s) "
        # Install synchronously and wait for completion
        export DEBIAN_FRONTEND=noninteractive
        apt-get update -qq -y >/dev/null 2>&1 && \
         apt-get install -y --no-install-recommends \
             curl wget git \
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
            >/dev/null 2>&1
        # Verify installation
        if command -v gcc >/dev/null 2>&1 && command -v g++ >/dev/null 2>&1; then
            echo -e " \033[1;32m✓\033[0m"
        else
            echo -e " \033[1;33m⚠\033[0m (installation may have failed)"
        fi
    fi

# Check if we are in the right directory
if [ ! -f "/app/requirements.txt" ]; then
    echo "Error: requirements.txt not found. Are you in the correct directory?"
    exit 1
fi

# Check if UV is available, install if not
if ! command -v uv >/dev/null 2>&1; then
        echo -n "📦 Installing UV package manager (5-15s) "
        # Install UV synchronously to ensure it's available
        curl -LsSf https://astral.sh/uv/install.sh | sh >/dev/null 2>&1
        # Update PATH after UV installation (UV installs to ~/.local/bin)
        export PATH="$HOME/.local/bin:/root/.local/bin:$HOME/.cargo/bin:/root/.cargo/bin:$PATH"
        echo -e " \033[1;32m✓\033[0m"
    fi
    
    # Check if virtual environment exists and has packages installed
    if [ -d "/app/.venv" ] && [ -f "/app/.venv/pyvenv.cfg" ] && [ -d "/app/.venv/lib" ]; then
        # Check if key packages are installed (check common Python versions)
        pandas_found=false
        for pyver in python3.14 python3.13 python3.12 python3.11 python3.10; do
            if [ -f "/app/.venv/lib/${pyver}/site-packages/pandas/__init__.py" ] 2>/dev/null; then
                pandas_found=true
                break
            fi
        done
        
        if [ "$pandas_found" = true ]; then
            echo -e "\033[1;32m✓\033[0m Environment ready"
        else
            echo -n "📦 Installing dependencies (30-120s) "
            (uv pip install --no-build-isolation --prefer-binary -r /app/requirements.txt --quiet 2>/dev/null) &
            install_pid=$!
            dots=0
            start_time=$(date +%s)
            while kill -0 $install_pid 2>/dev/null; do
                elapsed=$(($(date +%s) - start_time))
                if [ $elapsed -ge 180 ]; then
                    kill $install_pid 2>/dev/null
                    echo -e "\033[1;33m⚠ Timeout after 180s - dependencies may be partially installed\033[0m"
                    break
                fi
                printf "."
                sleep 0.5
                dots=$((dots + 1))
                if [ $((dots % 20)) -eq 0 ]; then
                    printf " [${elapsed}s]"
                    sleep 0.1
                    printf "\b\b\b\b\b\b\b\b"
                fi
            done
            wait $install_pid 2>/dev/null
            elapsed=$(($(date +%s) - start_time))
            echo -e " \033[1;32m✓\033[0m (${elapsed}s)"
        fi
    else
        echo -n "📦 Creating virtual environment (2-5s) "
        (uv venv /app/.venv >/dev/null 2>&1) &
        venv_pid=$!
        dots=0
        while kill -0 $venv_pid 2>/dev/null; do
            printf "."
            sleep 0.2
            dots=$((dots + 1))
            if [ $dots -ge 15 ]; then
                echo -e "\033[1;33m⚠ Taking longer than expected...\033[0m"
                dots=0
            fi
        done
        wait $venv_pid
        echo -e " \033[1;32m✓\033[0m"
        
        echo -n "📦 Installing dependencies (30-120s) "
        (uv pip install -r /app/requirements.txt --quiet 2>/dev/null) &
        install_pid=$!
        dots=0
        start_time=$(date +%s)
        while kill -0 $install_pid 2>/dev/null; do
            elapsed=$(($(date +%s) - start_time))
            if [ $elapsed -ge 180 ]; then
                kill $install_pid 2>/dev/null
                echo -e "\033[1;33m⚠ Timeout after 180s - dependencies may be partially installed\033[0m"
                break
            fi
            printf "."
            sleep 0.5
            dots=$((dots + 1))
            if [ $((dots % 20)) -eq 0 ]; then
                printf " [${elapsed}s]"
                sleep 0.1
                printf "\b\b\b\b\b\b\b\b"
            fi
        done
        wait $install_pid 2>/dev/null
        elapsed=$(($(date +%s) - start_time))
        echo -e " \033[1;32m✓\033[0m (${elapsed}s)"
    fi

# Activate virtual environment
    echo -n "🔄 Activating virtual environment "
    source .venv/bin/activate 2>/dev/null || {
        if [ -f "/app/.venv/bin/activate" ]; then
            source /app/.venv/bin/activate
        fi
    }
    echo -e "\033[1;32m✓\033[0m"
fi

# Verify virtual environment is activated
if [ -z "$VIRTUAL_ENV" ]; then
    echo "Error: Virtual environment activation failed"
    exit 1
fi

# Set up environment variables
# Ensure PATH includes UV installation directory (~/.local/bin)
export PATH="$HOME/.local/bin:/root/.local/bin:$HOME/.cargo/bin:/root/.cargo/bin:$PATH"
export PYTHONPATH="/app:$PYTHONPATH"
export PYTHONUNBUFFERED=1
export PYTHONDONTWRITEBYTECODE=1
export MPLCONFIGDIR="/tmp/matplotlib-cache"

# Create useful aliases
alias nz="uv run python /app/run_analysis.py"
alias eda="uv run python /app/scripts/eda_script.py"
alias uv-install="uv pip install --no-build-isolation --prefer-binary -r /app/requirements.txt"
alias uv-update="uv pip install --no-build-isolation --prefer-binary --upgrade -r /app/requirements.txt"
alias uv-test="uv run python -c \"import sys; print(f\\\"Python {sys.version}\\\"); import pandas, numpy, matplotlib; print(\\\"Core packages imported successfully\\\")\""
alias uv-pytest="uv run pytest tests/ -n auto"

# Show brief status
if [ -z "$VIRTUAL_ENV_SETUP_SKIPPED" ]; then
    echo ""
    echo -e "\033[1;32m✓ Environment ready!\033[0m"
echo "Available commands: nz, eda, uv-install, uv-update, uv-test, uv-pytest"
    echo ""
else
echo ""
fi

# Start interactive bash shell with simple configuration
# Ensure PATH is set before starting bash (UV installs to ~/.local/bin)
export PATH="$HOME/.local/bin:/root/.local/bin:$HOME/.cargo/bin:/root/.cargo/bin:$PATH"
# Also ensure /usr/bin is in PATH for gcc and other system tools
export PATH="/usr/bin:/usr/sbin:/bin:/sbin:$PATH"
# Also add PATH to .bashrc so it persists in new bash sessions
if [ -f "$HOME/.bashrc" ]; then
    if ! grep -q "/root/.local/bin" "$HOME/.bashrc" 2>/dev/null; then
        echo 'export PATH="$HOME/.local/bin:/root/.local/bin:$HOME/.cargo/bin:/root/.cargo/bin:$PATH"' >> "$HOME/.bashrc"
    fi
    if ! grep -q "/usr/bin" "$HOME/.bashrc" 2>/dev/null; then
        echo 'export PATH="/usr/bin:/usr/sbin:/bin:/sbin:$PATH"' >> "$HOME/.bashrc"
    fi
else
    echo 'export PATH="$HOME/.local/bin:/root/.local/bin:$HOME/.cargo/bin:/root/.cargo/bin:$PATH"' > "$HOME/.bashrc"
    echo 'export PATH="/usr/bin:/usr/sbin:/bin:/sbin:$PATH"' >> "$HOME/.bashrc"
fi
# Source .bashrc to ensure PATH is loaded in this session
if [ -f "$HOME/.bashrc" ]; then
    source "$HOME/.bashrc" 2>/dev/null || true
fi
# Use exec only if we're in interactive mode, otherwise just start bash
# Use bash -l (login shell) to ensure .bashrc is loaded
if [ -t 0 ]; then
    exec bash -il
else
    # Non-interactive mode - start bash without exec to allow script to continue
    bash -il
fi
ENHANCED_SHELL_EOF
    
    # Copy script to container using container cp or exec with cat
    if command -v container >/dev/null 2>&1 && container cp --help >/dev/null 2>&1; then
        # Use container cp if available
        container cp "$temp_script" "$container_id:/tmp/enhanced_shell.sh" 2>/dev/null || {
            # Fallback: use exec with cat
            container exec -i "$container_id" bash -c "cat > /tmp/enhanced_shell.sh" < "$temp_script"
        }
    else
        # Use exec with cat
        container exec -i "$container_id" bash -c "cat > /tmp/enhanced_shell.sh" < "$temp_script"
    fi
    
    # Clean up temp file
    rm -f "$temp_script"

    # Make the script executable
    container exec "$container_id" chmod +x /tmp/enhanced_shell.sh
    
    # Execute the enhanced shell script with proper signal handling
    print_status "Executing enhanced shell script..."
    
    # Start interactive shell
    print_status "Starting interactive shell..."
    
    # Method 1: Try interactive mode with enhanced shell
    # Suppress stderr to avoid "fd is not a pty" errors when TTY is not available
    print_status "Attempting interactive mode with enhanced shell..."
    if container exec --interactive --tty "$container_id" bash -c '
        trap "exit 0" EXIT INT TERM
            /tmp/enhanced_shell.sh
        rm -f /tmp/enhanced_shell.sh
    ' 2>/dev/null; then
        return 0
    fi
    
    # Method 2: Try simple bash in interactive mode (more reliable)
    print_status "Trying simple interactive bash..."
    if container exec --interactive --tty "$container_id" /bin/bash -i 2>/dev/null; then
        return 0
    fi
    
    # Method 3: Use script command to create pseudo-TTY (works from menu)
    # This is the most reliable method when called from menu scripts
    if command -v script >/dev/null 2>&1; then
        print_status "Using script command to create pseudo-TTY (menu call)..."
        # script creates a pseudo-TTY that works even when stdin is not a TTY
        script -q /dev/null bash -c "container exec --interactive --tty $container_id /bin/bash -i" 2>&1 && return 0
    fi
    
    # Method 4: Direct container exec without TTY flags (fallback)
    print_warning "Interactive TTY methods failed, trying direct exec..."
    container exec "$container_id" /tmp/enhanced_shell.sh 2>&1
    return $?
    
    # Additional cleanup
    container exec "$container_id" rm -f /tmp/enhanced_shell.sh 2>/dev/null || true
    
    # Show exit option if shell was used
    if [ "$SHELL_MODE" = true ]; then
        echo
        print_success "Shell session completed"
        # Simple exit without additional prompts to prevent restart loops
        print_success "Exiting to prevent automatic restart..."
        exit 0
    fi
}

# Function to show available commands
show_available_commands() {
    echo -e "${CYAN}Available Commands:${NC}"
    echo
    echo -e "${BLUE}Analysis Commands:${NC}"
    echo "  nz demo --rule PHLD                    # Run demo analysis"
    echo "  nz yfinance AAPL --rule PHLD          # Analyze Apple stock"
    echo "  nz mql5 BTCUSD --interval H4 --rule PHLD  # Analyze Bitcoin"
    echo "  eda                                    # Run EDA analysis"
    echo
    echo -e "${BLUE}UV Package Manager:${NC}"
    echo "  uv-install                            # Install dependencies"
    echo "  uv-update                             # Update dependencies"
    echo "  uv-test                               # Run UV environment test"
    echo "  uv-pytest                             # Run pytest with UV"
    echo
    echo -e "${BLUE}Testing:${NC}"
    echo "  pytest                                # Run all tests"
    echo "  pytest tests/ -n auto                 # Run tests with multithreading"
    echo "  pytest tests/calculation/             # Run calculation tests"
    echo
    echo -e "${BLUE}Development:${NC}"
    echo "  python run_analysis.py -h             # Show help"
    echo "  python scripts/utilities/test_uv_docker.py      # Test UV environment"
    echo "  python scripts/mcp/check_mcp_status.py    # Check MCP server"
    echo "  python scripts/debug/debug_yfinance.py    # Debug YFinance"
    echo "  python scripts/debug/debug_binance.py     # Debug Binance"
    echo "  python scripts/debug/debug_polygon.py     # Debug Polygon"
    echo "  python scripts/debug/examine_parquet.py   # Examine Parquet files"
    echo
    echo -e "${BLUE}System:${NC}"
    echo "  ls -la /app                           # List application files"
    echo "  ls -la /app/results/plots/            # List generated plots"
    echo "  ps aux | grep python                  # Check running processes"
    echo "  df -h                                 # Check disk usage"
    echo
    echo -e "${BLUE}Interactive Shell:${NC}"
    echo "  bash                                  # Start enhanced bash shell"
    echo "  python                                # Start Python interpreter"
    echo
    echo -e "${GREEN}🆕 Enhanced Shell Features:${NC}"
    echo "  - Automatic virtual environment activation"
    echo "  - Automatic UV dependency installation"
    echo "  - Pre-configured aliases (nz, eda, uv-*)"
    echo "  - Environment variables setup"
    echo "  - Dependency update checking"
}

# Function to show usage
show_usage() {
    echo "Usage: $0 [OPTIONS] [COMMAND]"
    echo
    echo "Options:"
    echo "  -h, --help     Show this help message"
    echo "  -i, --interactive Run command in interactive mode"
    echo "  -c, --command  Execute specific command"
    echo "  -s, --shell    Start enhanced interactive shell (with venv + UV setup)"
    echo "  -l, --list     List available commands"
    echo "  -t, --test     Run test suite"
    echo "  -a, --analysis Run analysis command"
    echo
    echo "Commands:"
    echo "  nz              Main analysis command"
    echo "  eda             EDA analysis"
    echo "  pytest          Run tests"
    echo "  bash            Enhanced interactive shell"
    echo "  python          Python interpreter"
    echo
    echo "Examples:"
    echo "  $0 --shell                    # Start enhanced shell with venv + UV setup"
    echo "  $0 --command 'nz demo'        # Run demo analysis"
    echo "  $0 --test                     # Run test suite"
    echo "  $0 --analysis 'nz yfinance AAPL'  # Analyze Apple stock"
    echo "  $0 'ls -la /app'              # List files in container"
    echo "  $0 'pytest tests/ -n auto'    # Run tests with multithreading"
    echo
    echo "🆕 Enhanced Shell Features:"
    echo "  - Automatic virtual environment activation"
    echo "  - Automatic UV dependency installation and updates"
    echo "  - Pre-configured aliases and environment variables"
    echo "  - Dependency health checking"
}

# Parse command line arguments
INTERACTIVE=false
COMMAND=""
SHELL_MODE=false
LIST_COMMANDS=false
TEST_MODE=false
ANALYSIS_MODE=false

while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            show_usage
            exit 0
            ;;
        -i|--interactive)
            INTERACTIVE=true
            shift
            ;;
        -c|--command)
            COMMAND="$2"
            shift 2
            ;;
        -s|--shell)
            SHELL_MODE=true
            shift
            ;;
        -l|--list)
            LIST_COMMANDS=true
            shift
            ;;
        -t|--test)
            TEST_MODE=true
            shift
            ;;
        -a|--analysis)
            ANALYSIS_MODE=true
            shift
            ;;
        -*)
            print_error "Unknown option: $1"
            show_usage
            exit 1
            ;;
        *)
            if [ -z "$COMMAND" ]; then
                COMMAND="$1"
            else
                COMMAND="$COMMAND $1"
            fi
            shift
            ;;
    esac
done

# Main execution
main() {
    echo -e "${BLUE}=== NeoZork HLD Prediction Native Container Executor ===${NC}"
    echo
    
    # Show available commands if requested
    if [ "$LIST_COMMANDS" = true ]; then
        show_available_commands
        exit 0
    fi
    
    # Check if container exists
    if ! check_container_exists; then
        print_error "Container 'neozork-hld-prediction' not found"
        print_error "Please run setup first: ./scripts/native-container/setup.sh"
        exit 1
    fi
    
    # Check if container is running
    if ! check_container_running; then
        print_error "Container is not running"
        print_error "Please start the container first: ./scripts/native-container/run.sh"
        exit 1
    fi
    
    # Get container ID
    container_id=$(get_container_id)
    if [ -z "$container_id" ]; then
        print_error "Failed to get container ID"
        exit 1
    fi
    
    print_status "Container ID: $container_id"
    
    # Determine command to execute
    local exec_command=""
    
    if [ "$SHELL_MODE" = true ]; then
        # Use enhanced shell with automatic venv activation and UV setup
        execute_enhanced_shell "$container_id"
        return 0
    elif [ "$TEST_MODE" = true ]; then
        exec_command="pytest tests/ -n auto"
    elif [ "$ANALYSIS_MODE" = true ]; then
        if [ -n "$COMMAND" ]; then
            exec_command="$COMMAND"
        else
            exec_command="nz demo --rule PHLD"
        fi
    elif [ -n "$COMMAND" ]; then
        exec_command="$COMMAND"
    else
        print_error "No command specified"
        show_usage
        exit 1
    fi
    
    # Execute command (only for non-shell commands)
    if [ -n "$exec_command" ]; then
        if execute_in_container "$container_id" "$exec_command" "$INTERACTIVE"; then
            print_success "Command executed successfully"
        else
            print_error "Command execution failed"
            exit 1
        fi
    fi
}

# Run main function
main "$@" 