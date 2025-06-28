#!/bin/bash

# Native Container Interactive Script for NeoZork HLD Prediction
# This script provides an interactive interface for managing the native Apple Silicon container

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
NC='\033[0m' # No Color

# Container name
CONTAINER_NAME="neozork-hld-prediction"

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

print_header() {
    echo -e "${CYAN}=== $1 ===${NC}"
}

print_menu() {
    echo -e "${MAGENTA}$1${NC}"
}

# Function to check if Docker is running
check_docker_running() {
    if ! container list --all >/dev/null 2>&1; then
        print_error "Docker/native container service is not running"
        print_status "Please start the container service first:"
        print_status "  container system start"
        return 1
    fi
    return 0
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to check if container exists
check_container_exists() {
    if container list --all | grep -q "$CONTAINER_NAME"; then
        return 0
    else
        return 1
    fi
}

# Function to check if container is running
check_container_running() {
    if container list --all | grep -q "$CONTAINER_NAME.*running"; then
        return 0
    else
        return 1
    fi
}

# Function to get container ID
get_container_id() {
    container list --all | grep "$CONTAINER_NAME" | awk '{print $1}'
}

# Function to check macOS version
check_macos_version() {
    print_status "Checking macOS version..."
    
    macos_version=$(sw_vers -productVersion)
    print_status "macOS version: $macos_version"
    
    major_version=$(echo $macos_version | cut -d. -f1)
    if [ "$major_version" -ge 26 ]; then
        print_success "macOS version is compatible (26+)"
        return 0
    else
        print_warning "macOS version $macos_version detected"
        print_warning "Native container is designed for macOS 26+ (Tahoe)"
        return 1
    fi
}

# Function to check native container application
check_native_container() {
    print_status "Checking native container application..."
    
    if command_exists container; then
        container_version=$(container --version 2>/dev/null || echo "unknown")
        print_success "Native container application found: $container_version"
        return 0
    else
        print_error "Native container application not found"
        return 1
    fi
}

# Function to check Python installation
check_python() {
    print_status "Checking Python installation..."
    
    if command_exists python3; then
        python_version=$(python3 --version 2>&1)
        print_success "Python found: $python_version"
        
        major_version=$(python3 -c "import sys; print(sys.version_info.major)")
        minor_version=$(python3 -c "import sys; print(sys.version_info.minor)")
        
        if [ "$major_version" -eq 3 ] && [ "$minor_version" -ge 11 ]; then
            print_success "Python version is compatible (3.11+)"
            return 0
        else
            print_warning "Python version $major_version.$minor_version detected"
            return 1
        fi
    else
        print_error "Python 3 not found"
        return 1
    fi
}

# Function to check project structure
check_project_structure() {
    print_status "Checking project structure..."
    
    required_files=(
        "container.yaml"
        "container-entrypoint.sh"
        "requirements.txt"
        "run_analysis.py"
        "src/"
        "tests/"
        "data/"
        "logs/"
        "results/"
    )
    
    missing_files=()
    
    for file in "${required_files[@]}"; do
        if [ ! -e "$file" ]; then
            missing_files+=("$file")
        fi
    done
    
    if [ ${#missing_files[@]} -eq 0 ]; then
        print_success "All required files and directories found"
        return 0
    else
        print_error "Missing required files/directories:"
        for file in "${missing_files[@]}"; do
            print_error "  - $file"
        done
        return 1
    fi
}

# Function to create UV cache directory
create_uv_cache() {
    print_status "Creating UV cache directory..."
    
    mkdir -p data/cache/uv_cache
    chmod -R 755 data/cache/uv_cache
    
    print_success "UV cache directory created"
}

# Function to create container
create_container() {
    print_status "Creating native container..."
    
    if container create \
        --name "$CONTAINER_NAME" \
        --cwd /app \
        --env PYTHONPATH=/app \
        --env USE_UV=true \
        --env UV_ONLY=true \
        --env UV_CACHE_DIR=/app/.uv_cache \
        --env UV_VENV_DIR=/app/.venv \
        --env NATIVE_CONTAINER=true \
        --env DOCKER_CONTAINER=false \
        --env LOG_LEVEL=INFO \
        --env MCP_SERVER_TYPE=pycharm_copilot \
        --volume "$(pwd)/data:/app/data" \
        --volume "$(pwd)/logs:/app/logs" \
        --volume "$(pwd)/results:/app/results" \
        --volume "$(pwd)/tests:/app/tests" \
        --volume "$(pwd)/mql5_feed:/app/mql5_feed" \
        --volume "$(pwd)/data/cache/uv_cache:/app/.uv_cache" \
        --volume "$(pwd)/container-entrypoint.sh:/app/container-entrypoint.sh" \
        --cpus 2 \
        --memory 4G \
        --arch arm64 \
        --os linux \
        --entrypoint /app/container-entrypoint.sh \
        python:3.11-slim; then
        print_success "Container created successfully"
        return 0
    else
        print_error "Failed to create container"
        return 1
    fi
}

# Function to start container
start_container() {
    print_status "Starting container..."
    
    # Check if Docker is running
    if ! check_docker_running; then
        print_error "Cannot start container - container service not available"
        return 1
    fi
    
    if ! check_container_exists; then
        print_error "Container '$CONTAINER_NAME' not found"
        print_error "Please run setup first"
        return 1
    fi
    
    if check_container_running; then
        print_warning "Container is already running"
        return 0
    fi
    
    if container start "$CONTAINER_NAME"; then
        print_success "Container started successfully"
        return 0
    else
        print_error "Failed to start container"
        return 1
    fi
}

# Function to stop container
stop_container() {
    print_status "Stopping container..."
    
    # Check if Docker is running
    if ! check_docker_running; then
        print_error "Cannot stop container - container service not available"
        return 1
    fi
    
    if ! check_container_exists; then
        print_error "Container '$CONTAINER_NAME' not found"
        return 1
    fi
    
    if ! check_container_running; then
        print_warning "Container is not running"
        return 0
    fi
    
    container_id=$(get_container_id)
    if container stop "$container_id"; then
        print_success "Container stopped successfully"
        return 0
    else
        print_error "Failed to stop container"
        return 1
    fi
}

# Function to remove container
remove_container() {
    print_status "Removing container..."
    
    # Check if Docker is running
    if ! check_docker_running; then
        print_error "Cannot remove container - container service not available"
        return 1
    fi
    
    if ! check_container_exists; then
        print_warning "Container does not exist"
        return 0
    fi
    
    if check_container_running; then
        print_warning "Container is running, stopping first..."
        stop_container
    fi
    
    container_id=$(get_container_id)
    if container rm "$container_id"; then
        print_success "Container removed successfully"
        return 0
    else
        print_error "Failed to remove container"
        return 1
    fi
}

# Function to show container status
show_container_status() {
    print_header "Container Status"
    
    # Check if Docker is running
    if ! check_docker_running; then
        print_error "Cannot check container status - container service not available"
        return 1
    fi
    
    if check_container_exists; then
        print_success "Container exists: $CONTAINER_NAME"
        if check_container_running; then
            print_success "Status: Running"
            container list | grep "$CONTAINER_NAME"
        else
            print_warning "Status: Stopped"
        fi
    else
        print_warning "Container does not exist"
    fi
}

# Function to show container logs
show_container_logs() {
    print_header "Container Logs"
    
    # Check if Docker is running
    if ! check_docker_running; then
        print_error "Cannot show container logs - container service not available"
        return 1
    fi
    
    if ! check_container_exists; then
        print_error "Container not found"
        return 1
    fi
    
    if ! check_container_running; then
        print_warning "Container is not running"
        return 1
    fi
    
    container_id=$(get_container_id)
    print_status "Showing logs for container: $container_id"
    container logs "$container_id"
}

# Function to execute command in container
execute_in_container() {
    local command="$1"
    local interactive="$2"
    
    # Check if Docker is running
    if ! check_docker_running; then
        print_error "Cannot execute command in container - container service not available"
        return 1
    fi
    
    if ! check_container_exists; then
        print_error "Container not found"
        return 1
    fi
    
    if ! check_container_running; then
        print_error "Container is not running"
        return 1
    fi
    
    container_id=$(get_container_id)
    print_status "Executing command in container: $command"
    
    if [ "$interactive" = true ]; then
        container exec --interactive --tty "$container_id" "$command"
    else
        container exec "$container_id" "$command"
    fi
}

# Function to show available commands
show_available_commands() {
    print_header "Available Commands Inside Container"
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
}

# Function to cleanup resources
cleanup_resources() {
    print_header "Cleanup Resources"
    
    local cleanup_temp=false
    local cleanup_cache=false
    local cleanup_logs=false
    local cleanup_results=false
    
    echo "Select cleanup options:"
    echo "1) Temporary files"
    echo "2) Cache directories"
    echo "3) Log files"
    echo "4) Result files"
    echo "5) All of the above"
    echo "6) Cancel"
    
    read -p "Enter your choice (1-6): " choice
    
    case $choice in
        1) cleanup_temp=true ;;
        2) cleanup_cache=true ;;
        3) cleanup_logs=true ;;
        4) cleanup_results=true ;;
        5) cleanup_temp=true; cleanup_cache=true; cleanup_logs=true; cleanup_results=true ;;
        6) return 0 ;;
        *) print_error "Invalid choice"; return 1 ;;
    esac
    
    if [ "$cleanup_temp" = true ]; then
        print_status "Cleaning temporary files..."
        rm -rf /tmp/neozork-container /tmp/matplotlib-cache /tmp/bash_history /tmp/bash_config /tmp/bin 2>/dev/null || true
        print_success "Temporary files cleaned"
    fi
    
    if [ "$cleanup_cache" = true ]; then
        print_status "Cleaning cache directories..."
        rm -rf __pycache__ .pytest_cache 2>/dev/null || true
        find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
        print_success "Cache directories cleaned"
    fi
    
    if [ "$cleanup_logs" = true ]; then
        print_status "Cleaning log files..."
        if [ -d "logs" ]; then
            find logs -name "*.log" -type f -delete 2>/dev/null || true
            print_success "Log files cleaned"
        fi
    fi
    
    if [ "$cleanup_results" = true ]; then
        print_status "Cleaning result files..."
        if [ -d "results" ]; then
            rm -rf results/* 2>/dev/null || true
            print_success "Result files cleaned"
        fi
    fi
}

# Function to show main menu
show_main_menu() {
    clear
    print_header "NeoZork HLD Prediction Native Container Manager"
    echo
    print_menu "Main Menu:"
    echo "1) Setup container"
    echo "2) Start container"
    echo "3) Stop container"
    echo "4) Remove container"
    echo "5) Show container status"
    echo "6) Show container logs"
    echo "7) Execute command in container"
    echo "8) Start interactive shell"
    echo "9) Run analysis"
    echo "10) Run tests"
    echo "11) Show available commands"
    echo "12) Cleanup resources"
    echo "13) System check"
    echo "14) Exit"
    echo
}

# Function to handle setup
handle_setup() {
    print_header "Container Setup"
    
    # Check if Docker is running
    if ! check_docker_running; then
        print_error "Cannot proceed with setup - container service not available"
        read -p "Press Enter to continue..."
        return 1
    fi
    
    local errors=0
    
    if ! check_macos_version; then
        ((errors++))
    fi
    
    if ! check_native_container; then
        ((errors++))
    fi
    
    if ! check_python; then
        ((errors++))
    fi
    
    if ! check_project_structure; then
        ((errors++))
    fi
    
    if [ $errors -gt 0 ]; then
        print_error "Setup failed due to $errors error(s)"
        read -p "Press Enter to continue..."
        return 1
    fi
    
    print_success "All prerequisites met"
    
    create_uv_cache
    
    if create_container; then
        print_success "Container setup completed successfully"
    else
        print_error "Container setup failed"
    fi
    
    read -p "Press Enter to continue..."
}

# Function to handle command execution
handle_execute_command() {
    print_header "Execute Command in Container"
    
    echo "Enter command to execute:"
    read -p "Command: " command
    
    if [ -n "$command" ]; then
        execute_in_container "$command" false
    else
        print_error "No command specified"
    fi
    
    read -p "Press Enter to continue..."
}

# Function to handle interactive shell
handle_interactive_shell() {
    print_header "Interactive Shell"
    
    print_status "Starting interactive shell..."
    execute_in_container "bash" true
}

# Function to handle analysis
handle_analysis() {
    print_header "Run Analysis"
    
    echo "Select analysis type:"
    echo "1) Demo analysis (nz demo --rule PHLD)"
    echo "2) Apple stock analysis (nz yfinance AAPL --rule PHLD)"
    echo "3) Bitcoin analysis (nz mql5 BTCUSD --interval H4 --rule PHLD)"
    echo "4) EDA analysis (eda)"
    echo "5) Custom command"
    echo "6) Cancel"
    
    read -p "Enter your choice (1-6): " choice
    
    case $choice in
        1) execute_in_container "nz demo --rule PHLD" false ;;
        2) execute_in_container "nz yfinance AAPL --rule PHLD" false ;;
        3) execute_in_container "nz mql5 BTCUSD --interval H4 --rule PHLD" false ;;
        4) execute_in_container "eda" false ;;
        5) 
            read -p "Enter custom command: " custom_cmd
            if [ -n "$custom_cmd" ]; then
                execute_in_container "$custom_cmd" false
            fi
            ;;
        6) return 0 ;;
        *) print_error "Invalid choice" ;;
    esac
    
    read -p "Press Enter to continue..."
}

# Function to handle tests
handle_tests() {
    print_header "Run Tests"
    
    echo "Select test type:"
    echo "1) All tests (pytest)"
    echo "2) Tests with multithreading (pytest tests/ -n auto)"
    echo "3) Calculation tests (pytest tests/calculation/)"
    echo "4) CLI tests (pytest tests/cli/)"
    echo "5) Data tests (pytest tests/data/)"
    echo "6) Custom test command"
    echo "7) Cancel"
    
    read -p "Enter your choice (1-7): " choice
    
    case $choice in
        1) execute_in_container "pytest" false ;;
        2) execute_in_container "pytest tests/ -n auto" false ;;
        3) execute_in_container "pytest tests/calculation/" false ;;
        4) execute_in_container "pytest tests/cli/" false ;;
        5) execute_in_container "pytest tests/data/" false ;;
        6) 
            read -p "Enter custom test command: " custom_test
            if [ -n "$custom_test" ]; then
                execute_in_container "$custom_test" false
            fi
            ;;
        7) return 0 ;;
        *) print_error "Invalid choice" ;;
    esac
    
    read -p "Press Enter to continue..."
}

# Function to handle system check
handle_system_check() {
    print_header "System Check"
    
    echo "Checking system requirements..."
    echo
    
    local all_good=true
    
    if ! check_macos_version; then
        all_good=false
    fi
    
    if ! check_native_container; then
        all_good=false
    fi
    
    if ! check_python; then
        all_good=false
    fi
    
    if ! check_project_structure; then
        all_good=false
    fi
    
    echo
    if [ "$all_good" = true ]; then
        print_success "All system requirements met"
    else
        print_warning "Some system requirements are not met"
    fi
    
    read -p "Press Enter to continue..."
}

# Main interactive loop
main() {
    while true; do
        show_main_menu
        
        read -p "Enter your choice (1-14): " choice
        
        case $choice in
            1) 
                if ! handle_setup; then
                    print_warning "Setup operation failed or was cancelled"
                fi
                ;;
            2) 
                if start_container; then
                    print_success "Container started"
                else
                    print_error "Failed to start container"
                fi
                read -p "Press Enter to continue..."
                ;;
            3) 
                if stop_container; then
                    print_success "Container stopped"
                else
                    print_error "Failed to stop container"
                fi
                read -p "Press Enter to continue..."
                ;;
            4) 
                if remove_container; then
                    print_success "Container removed"
                else
                    print_error "Failed to remove container"
                fi
                read -p "Press Enter to continue..."
                ;;
            5) 
                if ! show_container_status; then
                    print_warning "Could not show container status"
                fi
                read -p "Press Enter to continue..."
                ;;
            6) 
                if ! show_container_logs; then
                    print_warning "Could not show container logs"
                fi
                read -p "Press Enter to continue..."
                ;;
            7) handle_execute_command ;;
            8) handle_interactive_shell ;;
            9) handle_analysis ;;
            10) handle_tests ;;
            11) 
                show_available_commands
                read -p "Press Enter to continue..."
                ;;
            12) cleanup_resources ;;
            13) handle_system_check ;;
            14) 
                print_success "Goodbye!"
                exit 0
                ;;
            *) 
                print_error "Invalid choice"
                read -p "Press Enter to continue..."
                ;;
        esac
    done
}

# Check if running in interactive mode
if [ -t 0 ]; then
    # Interactive mode
    main
else
    # Non-interactive mode - show help
    echo "Usage: $0"
    echo "This script provides an interactive interface for managing the native Apple Silicon container."
    echo "Run without arguments to start the interactive menu."
    exit 1
fi 