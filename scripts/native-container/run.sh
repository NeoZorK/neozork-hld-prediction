#!/bin/bash

# Native Container Run Script for NeoZork HLD Prediction
# This script starts the native Apple Silicon container

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
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

# Function to check if container exists (including stopped containers)
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

# Function to get container ID from running containers
get_running_container_id() {
    container list | grep "neozork-hld-prediction" | awk '{print $1}'
}

# Function to get container ID from all containers (including stopped)
get_all_container_id() {
    container list --all | grep "neozork-hld-prediction" | awk '{print $1}'
}

# Function to show running containers
show_running_containers() {
    print_status "Running containers (container ls):"
    if container list | grep -q .; then
        container list
    else
        print_warning "No running containers found"
    fi
}

# Function to show all containers (including stopped)
show_all_containers() {
    print_status "All containers (container ls -a):"
    if container list --all | grep -q .; then
        container list --all
    else
        print_warning "No containers found"
    fi
}

# Function to ensure container system service is running
ensure_container_service() {
    # Check if container system service is running
    if ! container system status >/dev/null 2>&1; then
        print_warning "Container system service is not running"
        print_status "Starting container system service..."
        if container system start >/dev/null 2>&1; then
            print_success "Container system service started"
            sleep 2  # Wait for service to fully initialize
        else
            print_error "Failed to start container system service"
            print_status "Please start the container service manually:"
            print_status "  container system start"
            return 1
        fi
    fi
    
    # Verify we can access container service
    if ! container list --all >/dev/null 2>&1; then
        print_warning "Cannot access container service, trying to restart..."
        if container system start >/dev/null 2>&1; then
            print_success "Container system service restarted"
            sleep 2  # Wait for service to fully initialize
            if ! container list --all >/dev/null 2>&1; then
                print_error "Still cannot access container service after restart"
                return 1
            fi
        else
            print_error "Failed to restart container system service"
            return 1
        fi
    fi
    return 0
}

# Function to start container
start_container() {
    print_status "Starting NeoZork HLD Prediction container..."
    
    # Ensure container system service is running
    if ! ensure_container_service; then
        print_error "Cannot start container - container service not available"
        exit 1
    fi
    
    # Additional wait to ensure service is fully ready
    print_status "Waiting for container service to be fully ready..."
    sleep 3
    
    # Check if container exists (including stopped containers)
    if ! check_container_exists; then
        print_error "Container 'neozork-hld-prediction' not found"
        print_error "Please run setup first: ./scripts/native-container/setup.sh"
        exit 1
    fi
    
    # Check if container is already running
    if check_container_running; then
        print_warning "Container is already running"
        show_running_containers
        return 0
    fi
    
    # Show container status before starting
    print_status "Container status before starting:"
    show_all_containers
    
    # Start the container with retry logic (XPC connection errors can be transient)
    print_status "Starting container..."
    local max_retries=3
    local retry_count=0
    local start_success=false
    
    while [ $retry_count -lt $max_retries ]; do
        if [ $retry_count -gt 0 ]; then
            print_warning "Retrying container start (attempt $((retry_count + 1))/$max_retries)..."
            # Ensure container service is running before retry
            print_status "Ensuring container service is running..."
            ensure_container_service
            sleep 2
        fi
        
        # Start container and immediately launch keep-alive process
        # The entrypoint runs interactive bash which exits in non-interactive mode
        # We need to start a keep-alive process very quickly after container starts
        if container start neozork-hld-prediction 2>&1; then
            print_success "Container start command completed"
            
            # Start keep-alive process immediately in background
            # This must happen before the entrypoint bash exits
            (
                # Wait just a moment for container to be ready
                sleep 1
                # Try multiple times to start keep-alive process
                for i in 1 2 3; do
                    if container exec neozork-hld-prediction bash -c "nohup sleep infinity >/dev/null 2>&1 &" 2>/dev/null; then
                        break
                    fi
                    sleep 1
                done
            ) &
            local keep_alive_pid=$!
            
            # Wait a moment for container to fully start
            sleep 4
            
            # Wait for keep-alive process to complete
            wait $keep_alive_pid 2>/dev/null || true
            
            # Verify keep-alive process is running
            sleep 1
            if container exec neozork-hld-prediction bash -c "pgrep -f 'sleep infinity' >/dev/null 2>&1" 2>/dev/null; then
                print_status "Keep-alive process is running"
            else
                print_warning "Keep-alive process may not be running, trying again..."
                container exec neozork-hld-prediction bash -c "nohup sleep infinity >/dev/null 2>&1 &" 2>/dev/null || true
                sleep 2
            fi
            
            # Check if container is now running
            if check_container_running; then
                print_success "Container started successfully and is running"
                start_success=true
                break
            else
                if [ $retry_count -lt $((max_retries - 1)) ]; then
                    print_warning "Container start command succeeded but container is not running, will retry..."
                else
                    print_warning "Container start command succeeded but container is not running after $max_retries attempts"
                    print_status "Checking all containers:"
                    show_all_containers
                fi
            fi
        else
            local exit_code=$?
            retry_count=$((retry_count + 1))
            if [ $retry_count -lt $max_retries ]; then
                print_warning "Container start failed (exit code: $exit_code), will retry..."
            else
                print_error "Failed to start container after $max_retries attempts"
                print_error "Last error: exit code $exit_code"
                print_status "This may be due to XPC connection issues"
                print_status "Try running: container system start"
            fi
        fi
        
        retry_count=$((retry_count + 1))
    done
    
    if [ "$start_success" = true ]; then
        return 0
    else
        return 1
    fi
}

# Function to show container status
show_container_status() {
    print_status "Container status:"
    echo
    
    # Show running containers
    show_running_containers
    echo
    
    # Show all containers
    show_all_containers
    echo
    
    # Check specific container status
    if check_container_exists; then
        if check_container_running; then
            print_success "Container 'neozork-hld-prediction' is running"
            container_id=$(get_running_container_id)
            print_status "Container ID: $container_id"
        else
            print_warning "Container 'neozork-hld-prediction' exists but is stopped"
            container_id=$(get_all_container_id)
            print_status "Container ID: $container_id"
        fi
    else
        print_warning "Container 'neozork-hld-prediction' does not exist"
    fi
}

# Function to show usage
show_usage() {
    echo "Usage: $0 [OPTIONS]"
    echo
    echo "Options:"
    echo "  -h, --help     Show this help message"
    echo "  -s, --status   Show container status"
    echo "  -f, --foreground Run in foreground mode"
    echo "  -d, --detached Run in detached mode"
    echo
    echo "Examples:"
    echo "  $0              # Start container in interactive mode"
    echo "  $0 --status     # Show container status"
    echo "  $0 --detached   # Start container in background"
}

# Parse command line arguments
FOREGROUND=false
DETACHED=false
SHOW_STATUS=false

while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            show_usage
            exit 0
            ;;
        -s|--status)
            SHOW_STATUS=true
            shift
            ;;
        -f|--foreground)
            FOREGROUND=true
            shift
            ;;
        -d|--detached)
            DETACHED=true
            shift
            ;;
        *)
            print_error "Unknown option: $1"
            show_usage
            exit 1
            ;;
    esac
done

# Main execution
main() {
    echo -e "${BLUE}=== NeoZork HLD Prediction Native Container Runner ===${NC}"
    echo
    
    # Show status if requested
    if [ "$SHOW_STATUS" = true ]; then
        show_container_status
        exit 0
    fi
    
    # Start container
    if start_container; then
        print_success "Container is ready for use"
        echo
        print_status "Available commands inside container:"
        echo "  - nz: Main analysis command"
        echo "  - eda: EDA analysis command"
        echo "  - uv-install: Install dependencies"
        echo "  - uv-update: Update dependencies"
        echo "  - uv-test: Run UV environment test"
        echo
        print_status "To stop the container: ./scripts/native-container/stop.sh"
        print_status "To view logs: ./scripts/native-container/logs.sh"
    else
        print_error "Failed to start container"
        print_status "Container may have started but stopped immediately"
        print_status "Check logs for more information: ./scripts/native-container/logs.sh"
        exit 1
    fi
}

# Run main function
main "$@" 