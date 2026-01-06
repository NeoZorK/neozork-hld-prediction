#!/bin/bash

# Native Container Exec Script for NeoZork HLD Prediction
# This script executes commands inside the running native Apple Silicon container

# Exit on error for proper error handling
set -e

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
alias nz="uv run --no-build-isolation python /app/run_analysis.py"
alias eda="uv run --no-build-isolation python /app/scripts/eda_script.py"
alias uv-install="cd /app && uv sync --no-build-isolation || (uv pip install --no-build-isolation --quiet setuptools>=78.1.1 wheel pyproject-metadata meson packaging git+https://github.com/mesonbuild/meson-python.git cython versioneer pybind11 setuptools-scm numpy scipy>=1.16.0 && uv pip install --no-build-isolation --quiet -e .)"
alias uv-update="cd /app && uv sync --no-build-isolation --upgrade || uv pip install --no-build-isolation --quiet --upgrade -r /app/requirements.txt"
alias uv-test="uv run --no-build-isolation python -c 'import sys; print(f\"Python {sys.version}\"); import pandas, numpy, matplotlib; print(\"Core packages imported successfully\")'"
alias uv-pytest="uv run --no-build-isolation pytest tests/ -n auto"

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

# Ensure all dependencies are installed before running uv run commands
# uv run creates isolated environment, so we need to sync dependencies first
if echo "$@" | grep -q "uv run"; then
    echo "Ensuring all dependencies are installed (this ensures correct build order)..." >&2
    # First, ensure venv exists
    if [ ! -f /app/.venv/bin/activate ]; then
        uv venv /app/.venv >/dev/null 2>&1
    fi
    source /app/.venv/bin/activate 2>/dev/null || true
    
    # Install system build dependencies if needed
    if ! command -v ninja >/dev/null 2>&1 || ! command -v cmake >/dev/null 2>&1; then
        export DEBIAN_FRONTEND=noninteractive
        apt-get update -qq -y >/dev/null 2>&1 && \
        apt-get install -y --no-install-recommends ninja-build cmake >/dev/null 2>&1 || true
    fi
    
    # Use uv sync to install all dependencies in correct order
    # This ensures scipy is installed before scikit-learn build
    echo "Syncing dependencies with uv sync (installing in correct order)..." >&2
    cd /app
    uv sync --no-build-isolation >/dev/null 2>&1 || {
        # Fallback: install dependencies step by step in correct order
        echo "uv sync failed, installing dependencies step by step..." >&2
        # Install build tools first
        uv pip install --no-build-isolation --quiet setuptools>=78.1.1 wheel >/dev/null 2>&1 || true
        uv pip install --no-build-isolation --quiet pyproject-metadata meson packaging >/dev/null 2>&1 || true
        uv pip install --no-build-isolation --quiet git+https://github.com/mesonbuild/meson-python.git >/dev/null 2>&1 || true
        uv pip install --no-build-isolation --quiet cython versioneer pybind11 setuptools-scm >/dev/null 2>&1 || true
        # Install numpy BEFORE pandas (required for pandas build with mesonpy)
        uv pip install --no-build-isolation --quiet numpy >/dev/null 2>&1 || true
        # Install scipy BEFORE scikit-learn (CRITICAL: scikit-learn build requires scipy)
        echo "Installing scipy (required before scikit-learn build)..." >&2
        uv pip install --no-build-isolation --quiet scipy>=1.16.0 >/dev/null 2>&1 || true
        # Verify scipy is installed
        if ! python -c "import scipy; print(f'scipy {scipy.__version__} installed')" 2>/dev/null; then
            echo "ERROR: Failed to install scipy, which is required for scikit-learn build" >&2
            exit 1
        fi
        # Now install remaining dependencies (scikit-learn will use installed scipy)
        uv pip install --no-build-isolation --quiet -e . >/dev/null 2>&1 || true
    }
    
    # Verify critical dependencies are installed
    if ! python -c "import scipy" 2>/dev/null; then
        echo "ERROR: scipy is not installed, cannot proceed" >&2
        exit 1
    fi
    
    # Modify command to add --no-build-isolation to use pre-installed packages
    if ! echo "$@" | grep -q -- "--no-build-isolation"; then
        # Replace "uv run" with "uv run --no-build-isolation"
        set -- $(echo "$@" | sed 's/uv run/uv run --no-build-isolation/')
    fi
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
            
            # Step 5: Ensure all dependencies are installed before uv run commands
            # uv run creates isolated environment, so we need to sync dependencies first
            if echo \"$command\" | grep -q \"uv run\"; then
                echo \"Ensuring all dependencies are installed (this ensures correct build order)...\" >&2
                # Ensure venv exists
                if [ ! -f /app/.venv/bin/activate ]; then
                    uv venv /app/.venv >/dev/null 2>&1
                fi
                source /app/.venv/bin/activate 2>/dev/null || true
                
                # Install system build dependencies if needed
                if ! command -v ninja >/dev/null 2>&1 || ! command -v cmake >/dev/null 2>&1; then
                    export DEBIAN_FRONTEND=noninteractive
                    apt-get update -qq -y >/dev/null 2>&1 && \
                    apt-get install -y --no-install-recommends ninja-build cmake >/dev/null 2>&1 || true
                fi
                
                # Use uv sync to install all dependencies in correct order
                # This ensures scipy is installed before scikit-learn build
                cd /app
                uv sync --no-build-isolation >/dev/null 2>&1 || {
                    # Fallback: install dependencies step by step in correct order
                    echo \"uv sync failed, installing dependencies step by step...\" >&2
                    # Install build tools first
                    uv pip install --no-build-isolation --quiet setuptools>=78.1.1 wheel >/dev/null 2>&1 || true
                    uv pip install --no-build-isolation --quiet pyproject-metadata meson packaging >/dev/null 2>&1 || true
                    uv pip install --no-build-isolation --quiet git+https://github.com/mesonbuild/meson-python.git >/dev/null 2>&1 || true
                    uv pip install --no-build-isolation --quiet cython versioneer pybind11 setuptools-scm >/dev/null 2>&1 || true
                    # Install numpy BEFORE pandas (required for pandas build with mesonpy)
                    uv pip install --no-build-isolation --quiet numpy >/dev/null 2>&1 || true
                    # Install scipy BEFORE scikit-learn (CRITICAL: scikit-learn build requires scipy)
                    echo \"Installing scipy (required before scikit-learn build)...\" >&2
                    uv pip install --no-build-isolation --quiet scipy>=1.16.0 >/dev/null 2>&1 || true
                    # Verify scipy is installed
                    if ! python -c \"import scipy; print(f'scipy {scipy.__version__} installed')\" 2>/dev/null; then
                        echo \"ERROR: Failed to install scipy, which is required for scikit-learn build\" >&2
                        exit 1
                    fi
                    # Now install remaining dependencies (scikit-learn will use installed scipy)
                    uv pip install --no-build-isolation --quiet -e . >/dev/null 2>&1 || true
                }
                
                # Verify critical dependencies are installed
                if ! python -c \"import scipy\" 2>/dev/null; then
                    echo \"ERROR: scipy is not installed, cannot proceed\" >&2
                    exit 1
                fi
            fi
            
            # Step 6: Execute the command
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
            # Ensure all dependencies are installed before uv run commands
            # uv run creates isolated environment, so we need to sync dependencies first
            if echo \"$command\" | grep -q \"uv run\"; then
                echo \"Ensuring all dependencies are installed (this ensures correct build order)...\" >&2
                # Ensure venv exists
                if [ ! -f /app/.venv/bin/activate ]; then
                    uv venv /app/.venv >/dev/null 2>&1
                fi
                source /app/.venv/bin/activate 2>/dev/null || true
                
                # Install system build dependencies if needed
                if ! command -v ninja >/dev/null 2>&1 || ! command -v cmake >/dev/null 2>&1; then
                    export DEBIAN_FRONTEND=noninteractive
                    apt-get update -qq -y >/dev/null 2>&1 && \
                    apt-get install -y --no-install-recommends ninja-build cmake >/dev/null 2>&1 || true
                fi
                
                # Use uv sync to install all dependencies in correct order
                # This ensures scipy is installed before scikit-learn build
                cd /app
                uv sync --no-build-isolation >/dev/null 2>&1 || {
                    # Fallback: install dependencies step by step in correct order
                    echo \"uv sync failed, installing dependencies step by step...\" >&2
                    # Install build tools first
                    uv pip install --no-build-isolation --quiet setuptools>=78.1.1 wheel >/dev/null 2>&1 || true
                    uv pip install --no-build-isolation --quiet pyproject-metadata meson packaging >/dev/null 2>&1 || true
                    uv pip install --no-build-isolation --quiet git+https://github.com/mesonbuild/meson-python.git >/dev/null 2>&1 || true
                    uv pip install --no-build-isolation --quiet cython versioneer pybind11 setuptools-scm >/dev/null 2>&1 || true
                    # Install numpy BEFORE pandas (required for pandas build with mesonpy)
                    uv pip install --no-build-isolation --quiet numpy >/dev/null 2>&1 || true
                    # Install scipy BEFORE scikit-learn (CRITICAL: scikit-learn build requires scipy)
                    echo \"Installing scipy (required before scikit-learn build)...\" >&2
                    uv pip install --no-build-isolation --quiet scipy>=1.16.0 >/dev/null 2>&1 || true
                    # Verify scipy is installed
                    if ! python -c \"import scipy; print(f'scipy {scipy.__version__} installed')\" 2>/dev/null; then
                        echo \"ERROR: Failed to install scipy, which is required for scikit-learn build\" >&2
                        exit 1
                    fi
                    # Now install remaining dependencies (scikit-learn will use installed scipy)
                    uv pip install --no-build-isolation --quiet -e . >/dev/null 2>&1 || true
                }
                
                # Verify critical dependencies are installed
                if ! python -c \"import scipy\" 2>/dev/null; then
                    echo \"ERROR: scipy is not installed, cannot proceed\" >&2
                    exit 1
                fi
                
                # Modify command to add --no-build-isolation to use pre-installed packages
                if ! echo \"$command\" | grep -q -- \"--no-build-isolation\"; then
                    command=\"\$(echo \"\$command\" | sed 's/uv run/uv run --no-build-isolation/')\"
                fi
            fi
            cd /app
            eval \"\$command\"
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

# IMPORTANT: Set PATH first to include UV installation directory and system tools
# UV installs to ~/.local/bin, so we need to add it to PATH immediately
# Also ensure system tools (gcc, etc.) are in PATH
export PATH="/usr/bin:/usr/sbin:/bin:/sbin:$HOME/.local/bin:/root/.local/bin:$HOME/.cargo/bin:/root/.cargo/bin:$PATH"

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
    # Already set up, but ensure UV and gcc are available
    # Ensure PATH includes UV installation directory
    export PATH="$HOME/.local/bin:/root/.local/bin:$HOME/.cargo/bin:/root/.cargo/bin:$PATH"
    # Check and install gcc and image libraries if not available
    if ! command -v gcc >/dev/null 2>&1 || ! ldconfig -p | grep -q libjpeg >/dev/null 2>&1; then
        echo -n "📦 Installing build tools and image libraries (gcc, libjpeg, etc.) "
        export DEBIAN_FRONTEND=noninteractive
        apt-get update -qq -y >/dev/null 2>&1 && \
        apt-get install -y --no-install-recommends \
            build-essential \
            gcc \
            g++ \
            pkg-config \
            ninja-build \
            cmake \
            libjpeg-dev \
            libjpeg62-turbo \
            libpng-dev \
            libpng16-16 \
            libfreetype6-dev \
            libfreetype6 \
            liblcms2-dev \
            liblcms2-2 \
            libtiff-dev \
            libtiff6 \
            libwebp-dev \
            libwebp7 \
            libopenjp2-7-dev \
            libopenjp2-7 \
            >/dev/null 2>&1 && \
        ldconfig >/dev/null 2>&1 && \
        echo -e " \033[1;32m✓\033[0m" || echo -e " \033[1;33m⚠\033[0m"
    fi
    # Also ensure runtime libraries are available (check if libjpeg.so.62 exists)
    if ! ldconfig -p 2>/dev/null | grep -q libjpeg && [ ! -f /usr/lib/aarch64-linux-gnu/libjpeg.so.62 ] && [ ! -f /usr/lib/arm-linux-gnueabihf/libjpeg.so.62 ]; then
        echo -n "📦 Installing image runtime libraries "
        export DEBIAN_FRONTEND=noninteractive
        apt-get update -qq -y >/dev/null 2>&1 && \
        apt-get install -y --no-install-recommends \
            libjpeg62-turbo \
            libpng16-16 \
            libfreetype6 \
            liblcms2-2 \
            libtiff6 \
            libwebp7 \
            libopenjp2-7 \
            >/dev/null 2>&1 && \
        ldconfig >/dev/null 2>&1 && \
        echo -e " \033[1;32m✓\033[0m" || echo -e " \033[1;33m⚠\033[0m"
    fi
    # Check and install UV if not available
    if ! command -v uv >/dev/null 2>&1; then
        echo -n "📦 Installing UV package manager "
        if command -v curl >/dev/null 2>&1; then
            curl -LsSf https://astral.sh/uv/install.sh | sh >/dev/null 2>&1
            export PATH="$HOME/.local/bin:/root/.local/bin:$HOME/.cargo/bin:/root/.cargo/bin:$PATH"
            echo -e " \033[1;32m✓\033[0m"
        else
            # Install curl first if needed
            export DEBIAN_FRONTEND=noninteractive
            apt-get update -qq -y >/dev/null 2>&1 && \
            apt-get install -y --no-install-recommends curl >/dev/null 2>&1 && \
            curl -LsSf https://astral.sh/uv/install.sh | sh >/dev/null 2>&1 && \
            export PATH="$HOME/.local/bin:/root/.local/bin:$HOME/.cargo/bin:/root/.cargo/bin:$PATH" && \
            echo -e " \033[1;32m✓\033[0m" || echo -e " \033[1;33m⚠\033[0m"
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
        # Create temp file for error output
        error_log=$(mktemp /tmp/apt-install-errors.XXXXXX)
        
        # Try to update package list directly (this is the best network connectivity test)
        # Update package list with retry (up to 3 attempts)
        update_success=false
        for attempt in 1 2 3; do
            if [ $attempt -gt 1 ]; then
                echo -n " (retry $attempt) "
                sleep 2
            fi
            # Use timeout if available, otherwise run directly
            if command -v timeout >/dev/null 2>&1; then
                apt_cmd="timeout 30 apt-get update -qq -y"
            else
                apt_cmd="apt-get update -qq -y"
            fi
            # Capture both stdout and stderr
            if eval "$apt_cmd" >"$error_log" 2>&1; then
                update_success=true
                break
            fi
            # Check if error is lock-related - just skip and show message
            if grep -qi "could not get lock\|unable to acquire.*lock\|is another process using it" "$error_log" 2>/dev/null; then
                if [ $attempt -lt 3 ]; then
                    sleep 3
                    continue
                else
                    echo -e " \033[1;33m⚠\033[0m (apt lock issue - skipping)"
                    echo "   Another apt-get process is holding the lock."
                    echo "   You can try: install-system-deps (after lock is released)"
                    rm -f "$error_log"
                    break
                fi
            fi
            # Check if error is network-related
            if grep -qi "temporary failure\|could not resolve\|failed to fetch\|network\|connection" "$error_log" 2>/dev/null; then
                if [ $attempt -lt 3 ]; then
                    sleep 3
                    continue
                else
                    echo -e " \033[1;33m⚠\033[0m (network connectivity issue)"
                    echo "   Cannot reach package repositories."
                    if [ -f "$error_log" ]; then
                        echo "   Error details:"
                        grep -i "temporary failure\|could not resolve\|failed to fetch" "$error_log" | head -n 3 | sed 's/^/   /'
                    fi
                    echo "   Possible solutions:"
                    echo "   - Check container network settings"
                    echo "   - Try: install-system-deps (may work if network is intermittent)"
                    rm -f "$error_log"
                    break
                fi
            fi
            sleep 2
        done
        
        if [ "$update_success" = true ]; then
            # Install packages with retry (up to 2 attempts)
            install_success=false
            for attempt in 1 2; do
                if [ $attempt -gt 1 ]; then
                    echo -n " (retry $attempt) "
                    sleep 2
                fi
                if apt-get install -y --no-install-recommends \
                    curl wget git \
                    build-essential \
                    gcc \
                    g++ \
                    pkg-config \
                    ninja-build \
                    cmake \
                    libpq-dev \
                    libpq5 \
                    libffi-dev \
                    libxml2-dev \
                    libxslt1-dev \
                    zlib1g-dev \
                    libjpeg-dev \
                    libjpeg62-turbo \
                    libpng-dev \
                    libpng16-16 \
                    libfreetype6-dev \
                    libfreetype6 \
                    liblcms2-dev \
                    liblcms2-2 \
                    libtiff-dev \
                    libtiff6 \
                    libwebp-dev \
                    libwebp7 \
                    libopenjp2-7-dev \
                    libopenjp2-7 \
                    >"$error_log" 2>&1; then
                    # Update library cache after installation
                    ldconfig >/dev/null 2>&1 || true
                    install_success=true
                    break
                fi
                # Check if error is about missing runtime libraries
                if grep -qi "unable to locate package\|package.*not found" "$error_log" 2>/dev/null; then
                    # Try installing without specific version numbers
                    if apt-get install -y --no-install-recommends \
                        libjpeg62-turbo \
                        libpng16-16 \
                        libfreetype6 \
                        liblcms2-2 \
                        libtiff6 \
                        libwebp7 \
                        libopenjp2-7 \
                        >"$error_log" 2>&1; then
                        ldconfig >/dev/null 2>&1 || true
                        install_success=true
                        break
                    fi
                fi
                # Check if error is lock-related - just skip and show message
                if grep -qi "could not get lock\|unable to acquire.*lock\|is another process using it" "$error_log" 2>/dev/null; then
                    if [ $attempt -lt 2 ]; then
                        sleep 3
                        continue
                    else
                        echo -e " \033[1;33m⚠\033[0m (apt lock issue - skipping)"
                        echo "   Another apt-get process is holding the lock."
                        echo "   You can try: install-system-deps (after lock is released)"
                        break
                    fi
                fi
                sleep 2
            done
            
            if [ "$install_success" = true ]; then
                # Update library cache after installation
                ldconfig >/dev/null 2>&1 || true
                # Verify installation - check multiple tools including build tools for pandas
                if command -v gcc >/dev/null 2>&1 && \
                   command -v g++ >/dev/null 2>&1 && \
                   command -v pkg-config >/dev/null 2>&1 && \
                   command -v ninja >/dev/null 2>&1 && \
                   command -v cmake >/dev/null 2>&1 && \
                   command -v curl >/dev/null 2>&1 && \
                   [ -f /usr/include/zlib.h ] && \
                   [ -f /usr/include/png.h ] && \
                   (ldconfig -p 2>/dev/null | grep -q libjpeg || [ -f /usr/lib/aarch64-linux-gnu/libjpeg.so.62 ] || [ -f /usr/lib/arm-linux-gnueabihf/libjpeg.so.62 ] || [ -f /usr/lib/libjpeg.so.62 ]); then
                    echo -e " \033[1;32m✓\033[0m"
                    rm -f "$error_log"
                    # Rebuild Pillow if it was installed before runtime libraries
                    if python -c "import PIL" 2>/dev/null; then
                        echo -n "📦 Rebuilding Pillow with image libraries "
                        (uv pip install --no-build-isolation --force-reinstall --no-cache-dir pillow >/dev/null 2>&1) && \
                        echo -e " \033[1;32m✓\033[0m" || echo -e " \033[1;33m⚠\033[0m"
                    fi
                else
                    echo -e " \033[1;33m⚠\033[0m (partial installation - some tools missing)"
                    echo "   Check: $error_log for details"
                    echo "   You can try: install-system-deps"
                fi
            else
                echo -e " \033[1;33m⚠\033[0m (package installation failed)"
                echo "   Error log: $error_log"
                # Try to show last few lines of error
                if [ -f "$error_log" ]; then
                    echo "   Last errors:"
                    tail -n 5 "$error_log" | sed 's/^/   /'
                fi
                echo "   You can try manually: install-system-deps"
            fi
        elif [ "$update_success" = false ] && [ ! -f "$error_log" ]; then
            # Network error was already handled above
            :
        else
            echo -e " \033[1;33m⚠\033[0m (package list update failed)"
            echo "   Error log: $error_log"
            # Try to show last few lines of error
            if [ -f "$error_log" ]; then
                echo "   Last errors:"
                tail -n 5 "$error_log" | sed 's/^/   /'
            fi
            echo "   Possible causes: network issues, repository problems, or permissions"
            echo "   You can try manually: install-system-deps"
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
            # Ensure all build dependencies are installed before installing main dependencies
            echo -n "📦 Installing Python build dependencies (mesonpy, setuptools, etc.) "
            (
                # Install basic build tools first
                uv pip install --no-build-isolation --quiet setuptools>=78.1.1 wheel >/dev/null 2>&1 || true
                # Install mesonpy dependencies
                uv pip install --no-build-isolation --quiet pyproject-metadata meson packaging >/dev/null 2>&1 || true
                # Install mesonpy from git (required for pandas on Python 3.14)
                uv pip install --no-build-isolation --quiet git+https://github.com/mesonbuild/meson-python.git >/dev/null 2>&1 || true
                # Install other build dependencies
                uv pip install --no-build-isolation --quiet cython versioneer pybind11 setuptools-scm >/dev/null 2>&1 || true
                # Install numpy BEFORE pandas (required for pandas build with mesonpy)
                uv pip install --no-build-isolation --quiet numpy >/dev/null 2>&1 || true
            ) &
            build_deps_pid=$!
                dots=0
            while kill -0 $build_deps_pid 2>/dev/null; do
                    printf "."
                sleep 0.3
                    dots=$((dots + 1))
                if [ $dots -ge 15 ]; then
                        dots=0
                    fi
                done
            wait $build_deps_pid 2>/dev/null
                echo -e " \033[1;32m✓\033[0m"
            echo -n "📦 Installing dependencies (30-120s) "
            (uv pip install --no-build-isolation --quiet -r /app/requirements.txt --quiet 2>/dev/null) &
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
        
        # Install build dependencies before main dependencies
        echo -n "📦 Installing Python build dependencies (mesonpy, setuptools, etc.) "
        (
            source /app/.venv/bin/activate 2>/dev/null || true
            # Install basic build tools first
            uv pip install --no-build-isolation --quiet setuptools>=78.1.1 wheel >/dev/null 2>&1 || true
            # Install mesonpy dependencies
            uv pip install --no-build-isolation --quiet pyproject-metadata meson packaging >/dev/null 2>&1 || true
            # Install mesonpy from git (required for pandas on Python 3.14)
            uv pip install --no-build-isolation --quiet git+https://github.com/mesonbuild/meson-python.git >/dev/null 2>&1 || true
            # Install other build dependencies
            uv pip install --no-build-isolation --quiet cython versioneer pybind11 setuptools-scm >/dev/null 2>&1 || true
            # Install numpy BEFORE pandas (required for pandas build with mesonpy)
            uv pip install --no-build-isolation --quiet numpy >/dev/null 2>&1 || true
        ) &
        build_deps_pid=$!
        dots=0
        while kill -0 $build_deps_pid 2>/dev/null; do
            printf "."
            sleep 0.3
            dots=$((dots + 1))
            if [ $dots -ge 15 ]; then
                dots=0
            fi
        done
        wait $build_deps_pid 2>/dev/null
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
    
    # Ensure setuptools and wheel are installed in the venv (required for uv run)
    # Use uv sync to ensure build dependencies are installed
    echo -n "📦 Ensuring build dependencies (setuptools, wheel) "
    uv sync --no-build-isolation >/dev/null 2>&1 || {
        # Fallback: install setuptools directly if sync fails
        if ! python -c "import setuptools" 2>/dev/null; then
            uv pip install --no-build-isolation --quiet setuptools>=78.1.1 wheel >/dev/null 2>&1 || true
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
alias nz="uv run --no-build-isolation python /app/run_analysis.py"
alias eda="uv run --no-build-isolation python /app/scripts/eda_script.py"
alias uv-install="cd /app && uv sync --no-build-isolation || (uv pip install --no-build-isolation --quiet setuptools>=78.1.1 wheel pyproject-metadata meson packaging git+https://github.com/mesonbuild/meson-python.git cython versioneer pybind11 setuptools-scm numpy scipy>=1.16.0 && uv pip install --no-build-isolation --quiet -e .)"
alias uv-update="cd /app && uv sync --no-build-isolation --upgrade || uv pip install --no-build-isolation --quiet --upgrade -r /app/requirements.txt"
alias uv-test="uv run --no-build-isolation python -c \"import sys; print(f\\\"Python {sys.version}\\\"); import pandas, numpy, matplotlib; print(\\\"Core packages imported successfully\\\")\""
alias uv-pytest="uv run --no-build-isolation pytest tests/ -n auto"

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
if [ ! -f "$HOME/.bashrc" ]; then
    touch "$HOME/.bashrc"
fi
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