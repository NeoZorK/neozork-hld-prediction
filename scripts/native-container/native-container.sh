#!/bin/bash

# Native Container Interactive Script for NeoZork HLD Prediction
# Simplified version with two main commands: Start and Stop

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
        read -p "Press Enter to continue..."
        return 1
    fi
    
    print_status "Step 1: Running setup..."
    if ./scripts/native-container/setup.sh; then
        print_success "Setup completed"
    else
        print_error "Setup failed"
        read -p "Press Enter to continue..."
        return 1
    fi
    
    echo
    print_status "Step 2: Starting container..."
    if ./scripts/native-container/run.sh; then
        print_success "Container started"
    else
        print_error "Failed to start container"
        read -p "Press Enter to continue..."
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
    print_status "You will be taken to the container shell."
    print_status "To exit the shell, type 'exit' or press Ctrl+D"
    echo
    read -p "Press Enter to continue to shell..."
    
    if ./scripts/native-container/exec.sh --shell; then
        print_success "Shell session completed"
    else
        print_warning "Shell session failed or was interrupted"
    fi
    
    echo
    print_success "Start container sequence completed!"
    read -p "Press Enter to continue..."
}

# Function to stop container (full sequence)
stop_container_sequence() {
    print_header "Stopping Container - Full Sequence"
    echo
    
    # Check if Docker is running
    if ! check_docker_running; then
        print_error "Cannot stop container - container service not available"
        read -p "Press Enter to continue..."
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
    read -p "Press Enter to continue..."
}

# Function to show container status
show_container_status() {
    print_header "Container Status"
    
    # Check if Docker is running
    if ! check_docker_running; then
        print_error "Cannot check container status - container service not available"
        read -p "Press Enter to continue..."
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
    
    read -p "Press Enter to continue..."
}

# Function to show help
show_help() {
    print_header "NeoZork HLD Prediction Native Container Manager"
    echo
    echo "This simplified interface provides two main commands:"
    echo
    echo -e "${GREEN}1. Start Container${NC}"
    echo "   Executes the full sequence:"
    echo "   - Setup container (./scripts/native-container/setup.sh)"
    echo "   - Start container (./scripts/native-container/run.sh)"
    echo "   - Check status (./scripts/native-container/run.sh --status)"
    echo "   - Open interactive shell (./scripts/native-container/exec.sh --shell)"
    echo
    echo -e "${RED}2. Stop Container${NC}"
    echo "   Executes the full sequence:"
    echo "   - Stop container (./scripts/native-container/stop.sh)"
    echo "   - Check status (./scripts/native-container/run.sh --status)"
    echo "   - Cleanup resources (./scripts/native-container/cleanup.sh --all --force)"
    echo
    echo -e "${BLUE}3. Show Status${NC}"
    echo "   Shows current container status"
    echo
    echo -e "${YELLOW}4. Help${NC}"
    echo "   Shows this help message"
    echo
    echo -e "${MAGENTA}0. Exit${NC}"
    echo "   Exits the script"
    echo
    read -p "Press Enter to continue..."
}

# Function to show main menu
show_main_menu() {
    clear
    print_header "NeoZork HLD Prediction Native Container Manager"
    echo
    print_menu "Main Menu:"
    echo "1) Start Container (Full Sequence)"
    echo "2) Stop Container (Full Sequence)"
    echo "3) Show Container Status"
    echo "4) Help"
    echo "0) Exit"
    echo
}

# Main interactive loop
main() {
    while true; do
        show_main_menu
        
        read -p "Enter your choice (0-4): " choice
        
        case $choice in
            1) 
                start_container_sequence
                ;;
            2) 
                stop_container_sequence
                ;;
            3) 
                show_container_status
                ;;
            4) 
                show_help
                ;;
            0) 
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
    echo "This script provides a simplified interface for managing the native Apple Silicon container."
    echo "Run without arguments to start the interactive menu."
    echo
    echo "Quick commands:"
    echo "  Start: ./scripts/native-container/setup.sh && ./scripts/native-container/run.sh && ./scripts/native-container/run.sh --status && ./scripts/native-container/exec.sh --shell"
    echo "  Stop:  ./scripts/native-container/stop.sh && ./scripts/native-container/run.sh --status && ./scripts/native-container/cleanup.sh --all --force"
    exit 1
fi 