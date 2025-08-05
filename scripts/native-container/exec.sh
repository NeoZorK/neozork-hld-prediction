#!/bin/bash

# Native Container Exec Script for NeoZork HLD Prediction
# This script executes commands inside the running native Apple Silicon container

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

# Update package list and install essential tools
echo "Installing essential tools..."
apt-get update -qq -y
apt-get install -y -qq curl wget git

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
if [ ! -f "/app/.venv/pyvenv.cfg" ] || [ ! -d "/app/.venv/lib/python3.11/site-packages" ]; then
    echo "Installing dependencies with UV..."
    uv pip install -r /app/requirements.txt
else
    echo "Checking for dependency updates..."
    uv pip install -r /app/requirements.txt --upgrade
fi

# Set up environment variables
export PYTHONPATH="/app:$PYTHONPATH"
export PYTHONUNBUFFERED=1
export PYTHONDONTWRITEBYTECODE=1
export MPLCONFIGDIR="/tmp/matplotlib-cache"

# Create useful aliases
alias nz="python /app/run_analysis.py"
alias eda="python /app/scripts/eda_script.py"
alias uv-install="uv pip install -r /app/requirements.txt"
alias uv-update="uv pip install -r /app/requirements.txt --upgrade"
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
    
    # Build exec command
    local exec_cmd="container exec"
    
    if [ "$interactive" = true ]; then
        exec_cmd="$exec_cmd --interactive --tty"
    fi
    
    exec_cmd="$exec_cmd $container_id $command"
    
    # Execute command
    eval "$exec_cmd"
}

# Function to execute enhanced shell in container
execute_enhanced_shell() {
    local container_id=$1
    
    print_status "Starting enhanced shell with automatic venv activation and UV setup..."
    
    # Create temporary script file in container using heredoc
    print_status "Creating enhanced shell script in container..."
    container exec "$container_id" bash -c 'cat > /tmp/enhanced_shell.sh << "EOF"
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

echo "=== NeoZork HLD Prediction Container Shell ==="
echo "Setting up environment..."

# Set non-interactive mode for apt
export DEBIAN_FRONTEND=noninteractive

# Update package list and install essential tools
echo "Installing essential tools..."
apt-get update -qq -y
apt-get install -y -qq curl wget git

# Check if we are in the right directory
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

# Change to app directory
cd /app

# Create virtual environment and install dependencies using uv sync
echo "Creating virtual environment and installing dependencies..."
uv sync

# Activate virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate

# Verify virtual environment is activated
if [ -z "$VIRTUAL_ENV" ]; then
    echo "Error: Virtual environment activation failed"
    exit 1
fi

echo "Virtual environment activated: $VIRTUAL_ENV"

# Set up environment variables
export PYTHONPATH="/app:$PYTHONPATH"
export PYTHONUNBUFFERED=1
export PYTHONDONTWRITEBYTECODE=1
export MPLCONFIGDIR="/tmp/matplotlib-cache"

# Create useful aliases
alias nz="uv run python /app/run_analysis.py"
alias eda="uv run python /app/scripts/eda_script.py"
alias uv-install="uv sync"
alias uv-update="uv sync --upgrade"
alias uv-test="uv run python -c \"import sys; print(f\\\"Python {sys.version}\\\"); import pandas, numpy, matplotlib; print(\\\"Core packages imported successfully\\\")\""
alias uv-pytest="uv run pytest tests/ -n auto"

echo "Environment setup complete!"
echo "Available commands: nz, eda, uv-install, uv-update, uv-test, uv-pytest"
echo "Type \"exit\" or press Ctrl+D to leave the container shell"
echo ""

# Start interactive bash shell with proper signal handling
exec bash --rcfile <(cat << "BASHRC"
# Custom bashrc for container shell
set -o ignoreeof  # Prevent accidental Ctrl+D exit
bind "set bind-tty-special-chars on"  # Enable special character handling

# Function to handle Ctrl+D gracefully
handle_ctrld() {
    echo ""
    echo "Use 'exit' command to leave the container shell, or press Ctrl+D again to force exit"
    return 0
}

# Set up Ctrl+D handler (using EXIT instead of EOF)
trap handle_ctrld EXIT

# Show prompt with container indicator
export PS1="(neozork-container) \w $ "

# Welcome message
echo "Container shell ready. Type 'exit' to leave or use Ctrl+D."
BASHRC
)
EOF'

    # Make the script executable
    container exec "$container_id" chmod +x /tmp/enhanced_shell.sh
    
    # Execute the enhanced shell script with proper signal handling
    print_status "Executing enhanced shell script..."
    
    # Use a wrapper to handle Ctrl+D properly
    container exec --interactive --tty "$container_id" bash -c '
        # Set up signal handlers for the wrapper
        trap "echo \"Container shell wrapper exiting...\"; exit 0" EXIT
        trap "echo \"Received interrupt in wrapper, exiting...\"; exit 0" INT TERM
        
        # Execute the enhanced shell
        /tmp/enhanced_shell.sh
        
        # Cleanup after shell exits
        rm -f /tmp/enhanced_shell.sh
    '
    
    # Additional cleanup
    container exec "$container_id" rm -f /tmp/enhanced_shell.sh 2>/dev/null || true
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