#!/bin/bash

# Native Container Stop Script for NeoZork HLD Prediction
# This script stops the native Apple Silicon container gracefully

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
    container list --all | grep "neozork-hld-prediction" | awk '{print $1}'
}

# Function to stop container gracefully
stop_container_gracefully() {
    local container_id=$1
    
    print_status "Stopping container gracefully (SIGTERM)..."
    
    # Send SIGTERM signal
    if container stop "$container_id"; then
        print_success "Container stopped gracefully"
        return 0
    else
        print_warning "Graceful stop failed, trying force stop..."
        return 1
    fi
}

# Function to force stop container
force_stop_container() {
    local container_id=$1
    
    print_status "Force stopping container (SIGKILL)..."
    
    # Send SIGKILL signal
    if container kill "$container_id"; then
        print_success "Container force stopped"
        return 0
    else
        print_error "Failed to force stop container"
        return 1
    fi
}

# Function to cleanup container resources
cleanup_container() {
    local container_id=$1
    
    print_status "Cleaning up container resources..."
    
    # Remove container if specified
    if [ "$REMOVE_CONTAINER" = true ]; then
        if container rm "$container_id"; then
            print_success "Container removed"
        else
            print_warning "Failed to remove container"
        fi
    fi
    
    # Cleanup temporary files
    if [ -d "/tmp/neozork-container" ]; then
        rm -rf /tmp/neozork-container
        print_status "Temporary files cleaned up"
    fi
}

# Function to show container status
show_container_status() {
    print_status "Container status:"
    if check_container_running; then
        print_warning "Container is still running"
        container list | grep "neozork-hld-prediction"
    else
        print_success "Container is stopped"
    fi
}

# Function to show usage
show_usage() {
    echo "Usage: $0 [OPTIONS]"
    echo
    echo "Options:"
    echo "  -h, --help     Show this help message"
    echo "  -f, --force    Force stop container (SIGKILL)"
    echo "  -r, --remove   Remove container after stopping"
    echo "  -s, --status   Show container status"
    echo "  -t, --timeout  Timeout in seconds for graceful stop (default: 30)"
    echo
    echo "Examples:"
    echo "  $0              # Stop container gracefully"
    echo "  $0 --force      # Force stop container"
    echo "  $0 --remove     # Stop and remove container"
    echo "  $0 --status     # Show container status"
}

# Parse command line arguments
FORCE_STOP=false
REMOVE_CONTAINER=false
SHOW_STATUS=false
TIMEOUT=30

while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            show_usage
            exit 0
            ;;
        -f|--force)
            FORCE_STOP=true
            shift
            ;;
        -r|--remove)
            REMOVE_CONTAINER=true
            shift
            ;;
        -s|--status)
            SHOW_STATUS=true
            shift
            ;;
        -t|--timeout)
            TIMEOUT="$2"
            shift 2
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
    echo -e "${BLUE}=== NeoZork HLD Prediction Native Container Stopper ===${NC}"
    echo
    
    # Show status if requested
    if [ "$SHOW_STATUS" = true ]; then
        show_container_status
        exit 0
    fi
    
    # Check if container exists
    if ! check_container_exists; then
        print_error "Container 'neozork-hld-prediction' not found"
        exit 1
    fi
    
    # Check if container is running
    if ! check_container_running; then
        print_warning "Container is not running"
        if [ "$REMOVE_CONTAINER" = true ]; then
            print_status "Removing stopped container..."
            container_id=$(get_container_id)
            cleanup_container "$container_id"
        fi
        exit 0
    fi
    
    # Get container ID
    container_id=$(get_container_id)
    if [ -z "$container_id" ]; then
        print_error "Failed to get container ID"
        exit 1
    fi
    
    print_status "Container ID: $container_id"
    
    # Stop container
    if [ "$FORCE_STOP" = true ]; then
        # Force stop immediately
        if force_stop_container "$container_id"; then
            cleanup_container "$container_id"
        else
            exit 1
        fi
    else
        # Graceful stop with timeout
        if stop_container_gracefully "$container_id"; then
            cleanup_container "$container_id"
        else
            print_warning "Graceful stop failed, trying force stop..."
            if force_stop_container "$container_id"; then
                cleanup_container "$container_id"
            else
                exit 1
            fi
        fi
    fi
    
    # Final status check
    echo
    show_container_status
    
    print_success "Container stop operation completed"
}

# Run main function
main "$@" 