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

# Function to start container
start_container() {
    print_status "Starting NeoZork HLD Prediction container..."
    
    # Check if container exists
    if ! check_container_exists; then
        print_error "Container 'neozork-hld-prediction' not found"
        print_error "Please run setup first: ./scripts/native-container/setup.sh"
        exit 1
    fi
    
    # Check if container is already running
    if check_container_running; then
        print_warning "Container is already running"
        print_status "Container status:"
        container list | grep "neozork-hld-prediction"
        return 0
    fi
    
    # Start the container
    if container start neozork-hld-prediction; then
        print_success "Container started successfully"
        return 0
    else
        print_error "Failed to start container"
        return 1
    fi
}

# Function to show container status
show_container_status() {
    print_status "Container status:"
    if check_container_running; then
        print_success "Container is running"
        container list --all | grep "neozork-hld-prediction"
    else
        print_warning "Container is not running"
        if check_container_exists; then
            print_status "Container exists but is stopped:"
            container list --all | grep "neozork-hld-prediction"
        fi
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
        exit 1
    fi
}

# Run main function
main "$@" 