#!/bin/bash

# Force Restart Container Service Script for NeoZork HLD Prediction
# This script forcefully restarts the container service when normal stop fails

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
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

print_header() {
    echo -e "${CYAN}=== $1 ===${NC}"
}

# Function to check if container service is running
check_container_service() {
    if container system status >/dev/null 2>&1; then
        return 0
    else
        return 1
    fi
}

# Function to force restart container service
force_restart_service() {
    print_header "Force Restarting Container Service"
    echo
    
    print_status "Step 1: Stopping container service..."
    if container system stop; then
        print_success "Container service stopped"
    else
        print_warning "Container service stop completed (may have been already stopped)"
    fi
    
    echo
    print_status "Step 2: Waiting for service to fully stop..."
    sleep 3
    
    echo
    print_status "Step 3: Starting container service..."
    if container system start; then
        print_success "Container service started"
    else
        print_error "Failed to start container service"
        return 1
    fi
    
    echo
    print_status "Step 4: Waiting for service to fully start..."
    sleep 5
    
    echo
    print_status "Step 5: Checking service status..."
    if check_container_service; then
        print_success "Container service is running"
        container system status
    else
        print_error "Container service is not running"
        return 1
    fi
    
    echo
    print_success "Container service force restart completed successfully!"
    return 0
}

# Function to show usage
show_usage() {
    echo "Usage: $0 [OPTIONS]"
    echo
    echo "Options:"
    echo "  -h, --help     Show this help message"
    echo "  -c, --check    Check container service status"
    echo "  -f, --force    Force restart without confirmation"
    echo
    echo "Examples:"
    echo "  $0              # Force restart with confirmation"
    echo "  $0 --check      # Check service status"
    echo "  $0 --force      # Force restart without confirmation"
}

# Parse command line arguments
CHECK_STATUS=false
FORCE_RESTART=false

while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            show_usage
            exit 0
            ;;
        -c|--check)
            CHECK_STATUS=true
            shift
            ;;
        -f|--force)
            FORCE_RESTART=true
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
    echo -e "${BLUE}=== NeoZork HLD Prediction Container Service Force Restart ===${NC}"
    echo
    
    # Check status if requested
    if [ "$CHECK_STATUS" = true ]; then
        print_header "Container Service Status"
        if check_container_service; then
            print_success "Container service is running"
            container system status
        else
            print_error "Container service is not running"
        fi
        exit 0
    fi
    
    # Check current service status
    print_status "Checking current container service status..."
    if check_container_service; then
        print_success "Container service is currently running"
        container system status
    else
        print_warning "Container service is not running"
    fi
    
    echo
    
    # Ask for confirmation unless force flag is set
    if [ "$FORCE_RESTART" = false ]; then
        print_warning "This will forcefully restart the container service."
        print_warning "This may interrupt any running containers."
        echo
        read -p "Do you want to continue? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            print_status "Operation cancelled by user"
            exit 0
        fi
    fi
    
    # Perform force restart
    if force_restart_service; then
        print_success "Force restart completed successfully!"
        echo
        print_status "You can now try stopping the container again:"
        print_status "  ./scripts/native-container/native-container.sh"
        echo
        if [ -t 0 ]; then
            read -p "Press Enter to continue..."
        fi
    else
        print_error "Force restart failed!"
        echo
        print_status "Please check the container service manually:"
        print_status "  container system status"
        echo
        if [ -t 0 ]; then
            read -p "Press Enter to continue..."
        fi
        exit 1
    fi
}

# Run main function
main "$@" 