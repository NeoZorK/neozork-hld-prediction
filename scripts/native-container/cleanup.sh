#!/bin/bash

# Native Container Cleanup Script for NeoZork HLD Prediction
# This script cleans up containers, images, and temporary files

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
    if container list | grep -q "neozork-hld-prediction"; then
        return 0
    else
        return 1
    fi
}

# Function to check if container is running
check_container_running() {
    if container ps | grep -q "neozork-hld-prediction.*running"; then
        return 0
    else
        return 1
    fi
}

# Function to get container ID
get_container_id() {
    container list | grep "neozork-hld-prediction" | awk '{print $1}'
}

# Function to stop container if running
stop_container() {
    if check_container_running; then
        print_status "Stopping running container..."
        container_id=$(get_container_id)
        if container stop "$container_id"; then
            print_success "Container stopped"
        else
            print_warning "Failed to stop container gracefully"
            if container kill "$container_id"; then
                print_success "Container force stopped"
            else
                print_error "Failed to stop container"
                return 1
            fi
        fi
    else
        print_status "Container is not running"
    fi
}

# Function to remove container
remove_container() {
    if check_container_exists; then
        print_status "Removing container..."
        container_id=$(get_container_id)
        if container rm "$container_id"; then
            print_success "Container removed"
        else
            print_error "Failed to remove container"
            return 1
        fi
    else
        print_status "Container does not exist"
    fi
}

# Function to remove container image
remove_image() {
    print_status "Removing container image..."
    if container rmi neozork-hld-prediction; then
        print_success "Container image removed"
    else
        print_warning "Failed to remove container image (may not exist)"
    fi
}

# Function to cleanup temporary files
cleanup_temp_files() {
    print_status "Cleaning up temporary files..."
    
    # Remove temporary directories
    local temp_dirs=(
        "/tmp/neozork-container"
        "/tmp/matplotlib-cache"
        "/tmp/bash_history"
        "/tmp/bash_config"
        "/tmp/bin"
    )
    
    for dir in "${temp_dirs[@]}"; do
        if [ -d "$dir" ]; then
            rm -rf "$dir"
            print_status "Removed: $dir"
        fi
    done
    
    # Remove temporary files
    local temp_files=(
        "/tmp/mcp_server.pid"
        "/tmp/container_*.log"
    )
    
    for pattern in "${temp_files[@]}"; do
        for file in $pattern; do
            if [ -f "$file" ]; then
                rm -f "$file"
                print_status "Removed: $file"
            fi
        done
    done
}

# Function to cleanup cache directories
cleanup_cache() {
    print_status "Cleaning up cache directories..."
    
    # UV cache
    if [ -d "data/cache/uv_cache" ]; then
        if [ "$CLEAN_CACHE" = true ]; then
            rm -rf data/cache/uv_cache/*
            print_success "UV cache cleaned"
        else
            print_status "UV cache preserved (use --cache to clean)"
        fi
    fi
    
    # Python cache
    if [ -d "__pycache__" ]; then
        rm -rf __pycache__
        print_status "Python cache cleaned"
    fi
    
    # Test cache
    if [ -d ".pytest_cache" ]; then
        rm -rf .pytest_cache
        print_status "Pytest cache cleaned"
    fi
    
    # Find and remove all __pycache__ directories
    find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
    print_status "All Python cache directories cleaned"
}

# Function to cleanup logs
cleanup_logs() {
    print_status "Cleaning up log files..."
    
    if [ -d "logs" ]; then
        if [ "$CLEAN_LOGS" = true ]; then
            find logs -name "*.log" -type f -delete
            print_success "Log files cleaned"
        else
            print_status "Log files preserved (use --logs to clean)"
        fi
    fi
}

# Function to cleanup results
cleanup_results() {
    print_status "Cleaning up result files..."
    
    if [ -d "results" ]; then
        if [ "$CLEAN_RESULTS" = true ]; then
            rm -rf results/*
            print_success "Result files cleaned"
        else
            print_status "Result files preserved (use --results to clean)"
        fi
    fi
}

# Function to show cleanup summary
show_cleanup_summary() {
    echo
    print_success "=== Cleanup Summary ==="
    echo
    
    if [ "$STOP_CONTAINER" = true ]; then
        print_success "✓ Container stopped"
    fi
    
    if [ "$REMOVE_CONTAINER" = true ]; then
        print_success "✓ Container removed"
    fi
    
    if [ "$REMOVE_IMAGE" = true ]; then
        print_success "✓ Container image removed"
    fi
    
    if [ "$CLEAN_TEMP" = true ]; then
        print_success "✓ Temporary files cleaned"
    fi
    
    if [ "$CLEAN_CACHE" = true ]; then
        print_success "✓ Cache directories cleaned"
    fi
    
    if [ "$CLEAN_LOGS" = true ]; then
        print_success "✓ Log files cleaned"
    fi
    
    if [ "$CLEAN_RESULTS" = true ]; then
        print_success "✓ Result files cleaned"
    fi
    
    echo
    print_status "To recreate the container, run: ./scripts/native-container/setup.sh"
}

# Function to show usage
show_usage() {
    echo "Usage: $0 [OPTIONS]"
    echo
    echo "Options:"
    echo "  -h, --help     Show this help message"
    echo "  -a, --all      Clean up everything (equivalent to --stop --remove --image --temp --cache --logs --results)"
    echo "  -s, --stop     Stop running container"
    echo "  -r, --remove   Remove container"
    echo "  -i, --image    Remove container image"
    echo "  -t, --temp     Clean up temporary files"
    echo "  -c, --cache    Clean up cache directories"
    echo "  -l, --logs     Clean up log files"
    echo "  -R, --results  Clean up result files"
    echo "  -f, --force    Force cleanup without confirmation"
    echo
    echo "Examples:"
    echo "  $0 --all       # Clean up everything"
    echo "  $0 --stop      # Stop running container"
    echo "  $0 --remove    # Remove container"
    echo "  $0 --cache     # Clean cache directories"
    echo "  $0 --temp --logs  # Clean temp files and logs"
}

# Parse command line arguments
STOP_CONTAINER=false
REMOVE_CONTAINER=false
REMOVE_IMAGE=false
CLEAN_TEMP=false
CLEAN_CACHE=false
CLEAN_LOGS=false
CLEAN_RESULTS=false
FORCE=false

while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            show_usage
            exit 0
            ;;
        -a|--all)
            STOP_CONTAINER=true
            REMOVE_CONTAINER=true
            REMOVE_IMAGE=true
            CLEAN_TEMP=true
            CLEAN_CACHE=true
            CLEAN_LOGS=true
            CLEAN_RESULTS=true
            shift
            ;;
        -s|--stop)
            STOP_CONTAINER=true
            shift
            ;;
        -r|--remove)
            REMOVE_CONTAINER=true
            shift
            ;;
        -i|--image)
            REMOVE_IMAGE=true
            shift
            ;;
        -t|--temp)
            CLEAN_TEMP=true
            shift
            ;;
        -c|--cache)
            CLEAN_CACHE=true
            shift
            ;;
        -l|--logs)
            CLEAN_LOGS=true
            shift
            ;;
        -R|--results)
            CLEAN_RESULTS=true
            shift
            ;;
        -f|--force)
            FORCE=true
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
    echo -e "${BLUE}=== NeoZork HLD Prediction Native Container Cleanup ===${NC}"
    echo
    
    # Check if any cleanup action is specified
    if [ "$STOP_CONTAINER" = false ] && [ "$REMOVE_CONTAINER" = false ] && [ "$REMOVE_IMAGE" = false ] && [ "$CLEAN_TEMP" = false ] && [ "$CLEAN_CACHE" = false ] && [ "$CLEAN_LOGS" = false ] && [ "$CLEAN_RESULTS" = false ]; then
        print_error "No cleanup action specified"
        show_usage
        exit 1
    fi
    
    # Show what will be cleaned up
    print_status "Cleanup actions to be performed:"
    if [ "$STOP_CONTAINER" = true ]; then echo "  - Stop running container"; fi
    if [ "$REMOVE_CONTAINER" = true ]; then echo "  - Remove container"; fi
    if [ "$REMOVE_IMAGE" = true ]; then echo "  - Remove container image"; fi
    if [ "$CLEAN_TEMP" = true ]; then echo "  - Clean temporary files"; fi
    if [ "$CLEAN_CACHE" = true ]; then echo "  - Clean cache directories"; fi
    if [ "$CLEAN_LOGS" = true ]; then echo "  - Clean log files"; fi
    if [ "$CLEAN_RESULTS" = true ]; then echo "  - Clean result files"; fi
    echo
    
    # Ask for confirmation unless force is specified
    if [ "$FORCE" = false ]; then
        echo -n "Do you want to continue? (y/N): "
        read -r response
        if [ "$response" != "y" ] && [ "$response" != "Y" ]; then
            print_status "Cleanup cancelled"
            exit 0
        fi
    fi
    
    # Perform cleanup actions
    if [ "$STOP_CONTAINER" = true ]; then
        stop_container
    fi
    
    if [ "$REMOVE_CONTAINER" = true ]; then
        remove_container
    fi
    
    if [ "$REMOVE_IMAGE" = true ]; then
        remove_image
    fi
    
    if [ "$CLEAN_TEMP" = true ]; then
        cleanup_temp_files
    fi
    
    if [ "$CLEAN_CACHE" = true ]; then
        cleanup_cache
    fi
    
    if [ "$CLEAN_LOGS" = true ]; then
        cleanup_logs
    fi
    
    if [ "$CLEAN_RESULTS" = true ]; then
        cleanup_results
    fi
    
    # Show cleanup summary
    show_cleanup_summary
}

# Run main function
main "$@" 