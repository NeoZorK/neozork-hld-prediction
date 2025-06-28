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
    if container list --all | grep -q "neozork-hld-prediction.*running"; then
        return 0
    else
        return 1
    fi
}

# Function to get container ID
get_container_id() {
    container list --all | grep "neozork-hld-prediction" | awk '{print $1}'
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
    echo
    echo -e "${BLUE}Testing:${NC}"
    echo "  pytest                                # Run all tests"
    echo "  pytest tests/ -n auto                 # Run tests with multithreading"
    echo "  pytest tests/calculation/             # Run calculation tests"
    echo
    echo -e "${BLUE}Development:${NC}"
    echo "  python run_analysis.py -h             # Show help"
    echo "  python scripts/test_uv_docker.py      # Test UV environment"
    echo "  python scripts/check_mcp_status.py    # Check MCP server"
    echo
    echo -e "${BLUE}System:${NC}"
    echo "  ls -la /app                           # List application files"
    echo "  ls -la /app/results/plots/            # List generated plots"
    echo "  ps aux | grep python                  # Check running processes"
    echo "  df -h                                 # Check disk usage"
    echo
    echo -e "${BLUE}Interactive Shell:${NC}"
    echo "  bash                                  # Start bash shell"
    echo "  python                                # Start Python interpreter"
}

# Function to show usage
show_usage() {
    echo "Usage: $0 [OPTIONS] [COMMAND]"
    echo
    echo "Options:"
    echo "  -h, --help     Show this help message"
    echo "  -i, --interactive Run command in interactive mode"
    echo "  -c, --command  Execute specific command"
    echo "  -s, --shell    Start interactive shell"
    echo "  -l, --list     List available commands"
    echo "  -t, --test     Run test suite"
    echo "  -a, --analysis Run analysis command"
    echo
    echo "Commands:"
    echo "  nz              Main analysis command"
    echo "  eda             EDA analysis"
    echo "  pytest          Run tests"
    echo "  bash            Interactive shell"
    echo "  python          Python interpreter"
    echo
    echo "Examples:"
    echo "  $0 --shell                    # Start interactive shell"
    echo "  $0 --command 'nz demo'        # Run demo analysis"
    echo "  $0 --test                     # Run test suite"
    echo "  $0 --analysis 'nz yfinance AAPL'  # Analyze Apple stock"
    echo "  $0 'ls -la /app'              # List files in container"
    echo "  $0 'pytest tests/ -n auto'    # Run tests with multithreading"
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
        exec_command="bash"
        INTERACTIVE=true
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
    
    # Execute command
    if execute_in_container "$container_id" "$exec_command" "$INTERACTIVE"; then
        print_success "Command executed successfully"
    else
        print_error "Command execution failed"
        exit 1
    fi
}

# Run main function
main "$@" 