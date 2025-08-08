#!/bin/bash

# Native Container Interactive Script for NeoZork HLD Prediction
# Enhanced version with integrated test management and container operations

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

# Test configuration
TEST_TIMEOUT=300  # 5 minutes
MAX_WORKERS=2     # Safe worker count for container
TEST_STAGES=("basic:unit" "indicators:data:export" "plotting" "cli")

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

# Function to check if we're in a container environment
is_container() {
    [ "$NATIVE_CONTAINER" = "true" ] || [ "$DOCKER_CONTAINER" = "true" ] || [ -f /.dockerenv ]
}

# Function to setup container environment variables
setup_container_environment() {
    print_status "Setting up container environment variables..."
    
    # Set thread limits for stability
    export OMP_NUM_THREADS=1
    export MKL_NUM_THREADS=1
    export OPENBLAS_NUM_THREADS=1
    export PYTHONMALLOC=malloc
    
    # Set Python environment
    export PYTHONUNBUFFERED=1
    export PYTHONDONTWRITEBYTECODE=1
    export MPLCONFIGDIR=/tmp/matplotlib-cache
    
    # Create necessary directories
    mkdir -p /tmp/matplotlib-cache
    mkdir -p logs
    mkdir -p data/cache/uv_cache
    
    print_success "Container environment variables set"
}

# Function to get safe worker count
get_safe_worker_count() {
    if is_container; then
        # In container, use fewer workers for stability
        local cpu_count=$(nproc 2>/dev/null || echo 2)
        local safe_workers=$((cpu_count > 2 ? 2 : cpu_count))
        echo $safe_workers
    else
        # On host, use more workers
        local cpu_count=$(nproc 2>/dev/null || echo 4)
        echo $cpu_count
    fi
}

# Function to check if timeout command exists
has_timeout() {
    command -v timeout >/dev/null 2>&1
}

# Function to run command with timeout (if available)
run_with_timeout() {
    local timeout_seconds=$1
    shift
    
    if has_timeout; then
        timeout $timeout_seconds "$@"
    else
        # Fallback for macOS (no timeout command)
        "$@"
    fi
}

# Function to run safe tests
run_safe_tests() {
    local test_args="$1"
    local worker_count=$(get_safe_worker_count)
    
    print_status "Running tests with $worker_count workers..."
    
    local cmd="uv run pytest $test_args \
        -n $worker_count \
        --maxfail=10 \
        --durations=10 \
        --junitxml=logs/test-results.xml \
        --disable-pytest-warnings \
        --no-header \
        --no-summary \
        --strict-markers"
    
    if is_container; then
        cmd="$cmd -m 'not slow and not performance'"
    fi
    
    print_status "Command: $cmd"
    
    if run_with_timeout $TEST_TIMEOUT bash -c "$cmd"; then
        print_success "Tests completed successfully"
        return 0
    else
        print_warning "Tests completed with some failures"
        return 1
    fi
}

# Function to run staged tests
run_staged_tests() {
    print_header "Running Staged Tests"
    
    setup_container_environment
    
    local total_passed=0
    local total_failed=0
    
    for stage in "${TEST_STAGES[@]}"; do
        print_header "Stage: $stage"
        
        # Use single worker for stability in container
        local worker_count=1
        if ! is_container; then
            worker_count=$(get_safe_worker_count)
        fi
        
        local cmd="uv run pytest tests -m '$stage' \
            -n $worker_count \
            --maxfail=5 \
            --durations=5 \
            --junitxml=logs/test-results-$stage.xml \
            --disable-pytest-warnings \
            --no-header \
            --no-summary"
        
        print_status "Running: $cmd"
        
        if run_with_timeout $TEST_TIMEOUT bash -c "$cmd"; then
            print_success "Stage $stage completed"
            ((total_passed++))
        else
            print_warning "Stage $stage had failures"
            ((total_failed++))
        fi
        
        # Cleanup between stages
        print_status "Cleaning up after stage $stage..."
        uv run python -c "import matplotlib.pyplot as plt; plt.close('all')" 2>/dev/null || true
        find /tmp -name "*.png" -delete 2>/dev/null || true
        find /tmp -name "*.pdf" -delete 2>/dev/null || true
        
        echo
    done
    
    print_header "Staged Tests Summary"
    print_success "Passed stages: $total_passed"
    if [ $total_failed -gt 0 ]; then
        print_warning "Failed stages: $total_failed"
    fi
    
    return $total_failed
}

# Function to run basic tests
run_basic_tests() {
    print_header "Running Basic Tests"
    
    setup_container_environment
    
    local cmd="uv run pytest tests -m 'basic or unit' \
        -n 1 \
        --maxfail=5 \
        --durations=5 \
        --junitxml=logs/test-results-basic.xml \
        --disable-pytest-warnings \
        --no-header \
        --no-summary"
    
    print_status "Running: $cmd"
    
    if run_with_timeout $TEST_TIMEOUT bash -c "$cmd"; then
        print_success "Basic tests completed"
        return 0
    else
        print_warning "Basic tests had failures"
        return 1
    fi
}

# Function to run indicator tests
run_indicator_tests() {
    print_header "Running Indicator Tests"
    
    setup_container_environment
    
    local cmd="uv run pytest tests -m 'indicators' \
        -n 1 \
        --maxfail=5 \
        --durations=5 \
        --junitxml=logs/test-results-indicators.xml \
        --disable-pytest-warnings \
        --no-header \
        --no-summary"
    
    print_status "Running: $cmd"
    
    if run_with_timeout $TEST_TIMEOUT bash -c "$cmd"; then
        print_success "Indicator tests completed"
        return 0
    else
        print_warning "Indicator tests had failures"
        return 1
    fi
}

# Function to run plotting tests
run_plotting_tests() {
    print_header "Running Plotting Tests"
    
    setup_container_environment
    
    local cmd="uv run pytest tests -m 'plotting' \
        -n 1 \
        --maxfail=5 \
        --durations=5 \
        --junitxml=logs/test-results-plotting.xml \
        --disable-pytest-warnings \
        --no-header \
        --no-summary"
    
    print_status "Running: $cmd"
    
    if run_with_timeout $TEST_TIMEOUT bash -c "$cmd"; then
        print_success "Plotting tests completed"
        return 0
    else
        print_warning "Plotting tests had failures"
        return 1
    fi
}

# Function to run CLI tests
run_cli_tests() {
    print_header "Running CLI Tests"
    
    setup_container_environment
    
    local cmd="uv run pytest tests -m 'cli' \
        -n 1 \
        --maxfail=5 \
        --durations=5 \
        --junitxml=logs/test-results-cli.xml \
        --disable-pytest-warnings \
        --no-header \
        --no-summary"
    
    print_status "Running: $cmd"
    
    if run_with_timeout $TEST_TIMEOUT bash -c "$cmd"; then
        print_success "CLI tests completed"
        return 0
    else
        print_warning "CLI tests had failures"
        return 1
    fi
}

# Function to run all tests
run_all_tests() {
    print_header "Running All Tests"
    
    setup_container_environment
    
    local worker_count=$(get_safe_worker_count)
    
    local cmd="uv run pytest tests \
        -n $worker_count \
        --maxfail=10 \
        --durations=10 \
        --junitxml=logs/test-results-all.xml \
        --disable-pytest-warnings \
        --no-header \
        --no-summary"
    
    if is_container; then
        cmd="$cmd -m 'not slow and not performance'"
    fi
    
    print_status "Running: $cmd"
    
    if run_with_timeout $TEST_TIMEOUT bash -c "$cmd"; then
        print_success "All tests completed"
        return 0
    else
        print_warning "All tests had failures"
        return 1
    fi
}

# Function to cleanup test environment
cleanup_test_environment() {
    print_status "Cleaning up test environment..."
    
    # Close matplotlib figures
    uv run python -c "import matplotlib.pyplot as plt; plt.close('all')" 2>/dev/null || true
    
    # Remove temporary files
    find /tmp -name "*.png" -delete 2>/dev/null || true
    find /tmp -name "*.pdf" -delete 2>/dev/null || true
    find /tmp -name "*.svg" -delete 2>/dev/null || true
    
    # Clear matplotlib cache
    rm -rf /tmp/matplotlib-cache/* 2>/dev/null || true
    
    print_success "Test environment cleaned up"
}

# Function to show test results
show_test_results() {
    print_header "Test Results"
    
    if [ -f "logs/test-results.xml" ]; then
        print_status "Test results available in logs/test-results.xml"
    fi
    
    if [ -f "logs/test-results-all.xml" ]; then
        print_status "All test results available in logs/test-results-all.xml"
    fi
    
    # Show recent test logs
    if [ -f "logs/test.log" ]; then
        print_status "Recent test logs:"
        tail -20 logs/test.log 2>/dev/null || true
    fi
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
    if container list | grep -q "$CONTAINER_NAME"; then
        return 0
    else
        return 1
    fi
}

# Function to start container (full sequence)
start_container_sequence() {
    print_header "Starting Container - Full Sequence"
    echo
    
    # Check if Docker is running
    if ! check_docker_running; then
        print_error "Cannot start container - container service not available"
        if [ -t 0 ]; then
            read -p "Press Enter to continue..."
        fi
        return 1
    fi
    
    # Check if container already exists and is running
    if check_container_exists && check_container_running; then
        print_warning "Container is already running!"
        print_status "Skipping setup and start steps..."
        print_status "Opening interactive shell directly..."
        echo
        if [ -t 0 ]; then
            read -p "Press Enter to continue to shell..." 2>/dev/null || true
        fi
        
        # Execute shell and exit immediately to prevent restart
        ./scripts/native-container/exec.sh --shell
        # If we reach here, it means exec.sh exited, so we should also exit
        print_success "Container session completed"
        exit 0
    fi
    
    # Check if container exists but is stopped
    if check_container_exists && ! check_container_running; then
        print_warning "Container exists but is stopped"
        print_status "Starting existing container..."
        
        if ./scripts/native-container/run.sh; then
            print_success "Container started"
        else
            print_error "Failed to start existing container"
            if [ -t 0 ]; then
                read -p "Press Enter to continue..."
            fi
            return 1
        fi
        
        echo
        print_status "Opening interactive shell..."
        print_status "You will be taken to the container shell."
        print_status "To exit the shell, type 'exit' or press Ctrl+D"
        echo
        if [ -t 0 ]; then
            read -p "Press Enter to continue to shell..."
        fi
        
        # Execute shell and exit immediately to prevent restart
        ./scripts/native-container/exec.sh --shell
        # If we reach here, it means exec.sh exited, so we should also exit
        print_success "Container session completed"
        exit 0
    fi
    
    # Container doesn't exist, run full setup
    print_status "Step 1: Running setup..."
    print_status "This will create container and configure UV environment"
    if ./scripts/native-container/setup.sh; then
        print_success "Setup completed"
    else
        print_error "Setup failed"
        if [ -t 0 ]; then
            read -p "Press Enter to continue..."
        fi
        return 1
    fi
    
    echo
    print_status "Step 2: Starting container..."
    print_status "This will automatically install all dependencies using UV"
    if ./scripts/native-container/run.sh; then
        print_success "Container started"
    else
        print_error "Failed to start container"
        if [ -t 0 ]; then
            read -p "Press Enter to continue..."
        fi
        return 1
    fi
    
    echo
    print_status "Step 3: Checking container status..."
    if ./scripts/native-container/run.sh --status; then
        print_success "Status check completed"
    else
        print_warning "Status check failed"
    fi
    
    echo
    print_status "Step 4: Starting interactive shell..."
    print_status "Virtual environment will be automatically activated"
    print_status "All dependencies will be available immediately"
    print_status "You will be taken to the container shell."
    print_status "To exit the shell, type 'exit' or press Ctrl+D"
    echo
    if [ -t 0 ]; then
        read -p "Press Enter to continue to shell..."
    fi
    
    # Execute shell and exit immediately to prevent restart
    ./scripts/native-container/exec.sh --shell
    # If we reach here, it means exec.sh exited, so we should also exit
    print_success "Container session completed"
    exit 0
}

# Function to stop container (full sequence)
stop_container_sequence() {
    print_header "Stopping Container - Full Sequence"
    echo
    
    # Check if Docker is running
    if ! check_docker_running; then
        print_error "Cannot stop container - container service not available"
        if [ -t 0 ]; then
            read -p "Press Enter to continue..."
        fi
        return 1
    fi
    
    print_status "Step 1: Stopping container..."
    if ./scripts/native-container/stop.sh; then
        print_success "Container stopped"
    else
        print_warning "Container stop completed (may have been already stopped)"
    fi
    
    echo
    print_status "Step 2: Checking final status..."
    if ./scripts/native-container/run.sh --status; then
        print_success "Status check completed"
    else
        print_warning "Status check failed"
    fi
    
    echo
    print_status "Step 3: Cleaning up resources..."
    if ./scripts/native-container/cleanup.sh --all --force; then
        print_success "Cleanup completed"
    else
        print_warning "Cleanup completed (some resources may remain)"
    fi
    
    echo
    print_success "Stop container sequence completed!"
    if [ -t 0 ]; then
        read -p "Press Enter to continue..."
    fi
}

# Function to restart container service
restart_container_service() {
    print_header "Restarting Container Service"
    echo
    
    print_status "Step 1: Stopping container system..."
    if container system stop; then
        print_success "Container system stopped"
    else
        print_warning "Container system stop may have failed or was already stopped"
    fi
    
    echo
    print_status "Step 2: Starting container system..."
    if container system start; then
        print_success "Container system started"
    else
        print_error "Failed to start container system"
        if [ -t 0 ]; then
            read -p "Press Enter to continue..."
        fi
        return 1
    fi
    
    echo
    print_status "Step 3: Checking container system status..."
    if container system status; then
        print_success "Container system is running"
    else
        print_warning "Container system status check failed"
    fi
    
    echo
    print_success "Container service restart completed!"
    if [ -t 0 ]; then
        read -p "Press Enter to continue..."
    fi
}

# Function to stop container with emergency restart option
stop_container_with_emergency_restart() {
    print_header "Stopping Container - Full Sequence"
    echo
    
    # Check if Docker is running
    if ! check_docker_running; then
        print_error "Cannot stop container - container service not available"
        if [ -t 0 ]; then
            read -p "Press Enter to continue..."
        fi
        return 1
    fi
    
    print_status "Step 1: Stopping container..."
    if ./scripts/native-container/stop.sh; then
        print_success "Container stopped"
    else
        print_warning "Container stop may have failed or container was already stopped"
        
        # Check if container is still running
        if check_container_running; then
            print_error "Container is still running after stop attempt"
            echo
            print_warning "The container could not be stopped normally."
            print_warning "This might be due to a stuck container or service issue."
            echo
            
            if [ -t 0 ]; then
                read -p "Do you want to force restart container service then try delete container again? (y/N): " -n 1 -r
                echo
                if [[ $REPLY =~ ^[Yy]$ ]]; then
                    print_status "Proceeding with force restart sequence..."
                    echo
                    
                    # Step 0: Force restart container service
                    print_status "Step 0: Force restarting container service..."
                    if ./scripts/native-container/force_restart.sh --force; then
                        print_success "Container service force restart completed"
                    else
                        print_error "Container service force restart failed"
                        if [ -t 0 ]; then
                            read -p "Press Enter to continue..."
                        fi
                        return 1
                    fi
                    
                    echo
                    print_status "Step 1 (retry): Stopping container after service restart..."
                    if ./scripts/native-container/stop.sh; then
                        print_success "Container stopped after service restart"
                    else
                        print_error "Container still cannot be stopped after service restart"
                        if [ -t 0 ]; then
                            read -p "Press Enter to continue..."
                        fi
                        return 1
                    fi
                else
                    print_status "Skipping force restart, continuing with cleanup..."
                fi
            fi
        fi
    fi
    
    echo
    print_status "Step 2: Checking final status..."
    if ./scripts/native-container/run.sh --status; then
        print_success "Status check completed"
    else
        print_warning "Status check failed"
    fi
    
    echo
    print_status "Step 3: Cleaning up resources..."
    cleanup_output=$(./scripts/native-container/cleanup.sh --all --force 2>&1)
    cleanup_exit_code=$?
    
    if [ $cleanup_exit_code -eq 0 ]; then
        print_success "Cleanup completed"
    else
        print_warning "Cleanup completed (some resources may remain)"
        
        # Check if the error is about container deletion failure
        if echo "$cleanup_output" | grep -q "delete failed for one or more containers"; then
            echo
            print_error "Error: Container deletion failed"
            print_warning "This usually indicates a stuck container or service issue"
            echo
            print_status "Recommended emergency restart service, choose p4 \"Restart service\""
            echo
            
            if [ -t 0 ]; then
                read -p "Do you want to restart container service now? (y/N): " -n 1 -r
                echo
                if [[ $REPLY =~ ^[Yy]$ ]]; then
                    print_status "Proceeding with emergency service restart..."
                    echo
                    
                    # Restart container service
                    if restart_container_service; then
                        print_success "Service restart completed"
                        
                        echo
                        print_status "Step 4: Retrying container stop after service restart..."
                        if ./scripts/native-container/stop.sh; then
                            print_success "Container stopped after service restart"
                        else
                            print_warning "Container stop retry failed"
                        fi
                        
                        echo
                        print_status "Step 5: Final cleanup after service restart..."
                        if ./scripts/native-container/cleanup.sh --all --force; then
                            print_success "Final cleanup completed"
                        else
                            print_warning "Final cleanup completed (some resources may remain)"
                        fi
                    else
                        print_error "Service restart failed"
                        if [ -t 0 ]; then
                            read -p "Press Enter to continue..."
                        fi
                        return 1
                    fi
                else
                    print_status "Skipping emergency service restart"
                fi
            fi
        fi
    fi
    
    echo
    print_success "Stop container sequence completed!"
    if [ -t 0 ]; then
        read -p "Press Enter to continue..."
    fi
}

# Function to show container status
show_container_status() {
    print_header "Container Status"
    
    # Check if Docker is running
    if ! check_docker_running; then
        print_error "Cannot check container status - container service not available"
        if [ -t 0 ]; then
            read -p "Press Enter to continue..."
        fi
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
    
    if [ -t 0 ]; then
        read -p "Press Enter to continue..."
    fi
}

# Function to show help
show_help() {
    print_header "NeoZork HLD Prediction Native Container Manager"
    echo
    echo "This enhanced interface provides container management and testing:"
    echo
    echo -e "${GREEN}Container Management:${NC}"
    echo "1. Start Container - Full setup and interactive shell"
    echo "2. Stop Container - Full cleanup and resource management"
    echo "3. Show Status - Current container status"
    echo "4. Restart Service - Emergency container service restart"
    echo
    echo -e "${CYAN}Testing Features:${NC}"
    echo "5. Run All Tests - Complete test suite execution"
    echo "6. Run Staged Tests - Tests in safe stages"
    echo "7. Run Basic Tests - Core functionality tests"
    echo "8. Run Indicator Tests - Technical indicator tests"
    echo "9. Run Plotting Tests - Visualization tests"
    echo "10. Run CLI Tests - Command line interface tests"
    echo "11. Show Test Results - Display test outcomes"
    echo "12. Cleanup Test Environment - Reset test state"
    echo
    echo -e "${YELLOW}Enhanced Features:${NC}"
    echo "   - 🆕 Integrated test management"
    echo "   - 🆕 Safe container testing with memory management"
    echo "   - 🆕 Staged test execution for stability"
    echo "   - 🆕 Automatic environment setup and cleanup"
    echo "   - 🆕 Test result reporting and analysis"
    echo "   - 🆕 Emergency container service management"
    echo
    echo -e "${MAGENTA}0. Exit${NC}"
    echo "   Exits the script"
    echo
    if [ -t 0 ]; then
        read -p "Press Enter to continue..."
    fi
}

# Function to show main menu
show_main_menu() {
    clear
    print_header "NeoZork HLD Prediction Native Container Manager"
    echo
    print_menu "Main Menu:"
    echo -e "${GREEN}Container Management:${NC}"
    echo "1) Start Container (Full Sequence)"
    echo "2) Stop Container (Full Sequence)"
    echo "3) Show Container Status"
    echo "4) Restart Service"
    echo
    echo -e "${CYAN}Testing Features:${NC}"
    echo "5) Run All Tests"
    echo "6) Run Staged Tests"
    echo "7) Run Basic Tests"
    echo "8) Run Indicator Tests"
    echo "9) Run Plotting Tests"
    echo "10) Run CLI Tests"
    echo "11) Show Test Results"
    echo "12) Cleanup Test Environment"
    echo
    echo -e "${MAGENTA}0) Exit${NC}"
    echo
}

# Main interactive loop
main() {
    while true; do
        show_main_menu
        
        if [ -t 0 ]; then
            read -p "Enter your choice (0-12): " choice 2>/dev/null || true
        else
            # Non-interactive mode - exit gracefully
            print_error "Script requires interactive terminal"
            exit 1
        fi
        
        case $choice in
            1) 
                start_container_sequence
                ;;
            2) 
                stop_container_with_emergency_restart
                ;;
            3) 
                show_container_status
                ;;
            4) 
                restart_container_service
                ;;
            5) 
                run_all_tests
                ;;
            6) 
                run_staged_tests
                ;;
            7) 
                run_basic_tests
                ;;
            8) 
                run_indicator_tests
                ;;
            9) 
                run_plotting_tests
                ;;
            10) 
                run_cli_tests
                ;;
            11) 
                show_test_results
                ;;
            12) 
                cleanup_test_environment
                ;;
            0) 
                print_success "Goodbye!"
                exit 0
                ;;
            *) 
                print_error "Invalid choice"
                if [ -t 0 ]; then
                    read -p "Press Enter to continue..."
                fi
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
    echo "This script provides container management and testing for Apple native container."
    echo "Run without arguments to start the interactive menu."
    echo
    echo "Quick commands:"
    echo "  Start: ./scripts/native-container/setup.sh && ./scripts/native-container/run.sh"
    echo "  Stop:  ./scripts/native-container/stop.sh && ./scripts/native-container/cleanup.sh --all --force"
    echo "  Tests: uv run pytest tests -n 2 --maxfail=10"
    exit 1
fi 