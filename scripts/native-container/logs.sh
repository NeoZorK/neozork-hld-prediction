#!/bin/bash

# Native Container Logs Script for NeoZork HLD Prediction
# This script displays logs from the native Apple Silicon container

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
    container ps | grep "neozork-hld-prediction" | awk '{print $1}'
}

# Function to show container logs
show_container_logs() {
    local container_id=$1
    local follow=$2
    local tail_lines=$3
    local filter=$4
    
    print_status "Showing logs for container: $container_id"
    
    # Build log command
    local log_cmd="container logs"
    
    if [ "$follow" = true ]; then
        log_cmd="$log_cmd --follow"
    fi
    
    if [ -n "$tail_lines" ] && [ "$tail_lines" -gt 0 ]; then
        log_cmd="$log_cmd --tail $tail_lines"
    fi
    
    log_cmd="$log_cmd $container_id"
    
    # Apply filter if specified
    if [ -n "$filter" ]; then
        log_cmd="$log_cmd | grep -i '$filter'"
    fi
    
    # Execute log command
    eval "$log_cmd"
}

# Function to show application logs
show_application_logs() {
    local log_file=$1
    local follow=$2
    local tail_lines=$3
    local filter=$4
    
    if [ ! -f "$log_file" ]; then
        print_warning "Log file not found: $log_file"
        return 1
    fi
    
    print_status "Showing application logs: $log_file"
    
    # Build log command
    local log_cmd="cat"
    
    if [ "$follow" = true ]; then
        log_cmd="tail -f"
    elif [ -n "$tail_lines" ] && [ "$tail_lines" -gt 0 ]; then
        log_cmd="tail -n $tail_lines"
    fi
    
    log_cmd="$log_cmd $log_file"
    
    # Apply filter if specified
    if [ -n "$filter" ]; then
        log_cmd="$log_cmd | grep -i '$filter'"
    fi
    
    # Execute log command
    eval "$log_cmd"
}

# Function to list available log files
list_log_files() {
    print_status "Available log files:"
    echo
    
    # Container logs
    echo -e "${CYAN}Container Logs:${NC}"
    if check_container_running; then
        container_id=$(get_container_id)
        echo "  - Container ID: $container_id"
        echo "  - Command: container logs $container_id"
    else
        echo "  - Container not running"
    fi
    echo
    
    # Application logs
    echo -e "${CYAN}Application Logs:${NC}"
    if [ -d "logs" ]; then
        find logs -name "*.log" -type f | while read -r log_file; do
            size=$(du -h "$log_file" | cut -f1)
            modified=$(stat -f "%Sm" "$log_file" 2>/dev/null || stat -c "%y" "$log_file" 2>/dev/null || echo "unknown")
            echo "  - $log_file ($size, modified: $modified)"
        done
    else
        echo "  - No logs directory found"
    fi
    echo
    
    # System logs
    echo -e "${CYAN}System Logs:${NC}"
    echo "  - UV cache: data/cache/uv_cache/"
    echo "  - Test results: logs/test_results/"
    echo "  - MCP server: logs/mcp_server.log"
}

# Function to show usage
show_usage() {
    echo "Usage: $0 [OPTIONS] [LOG_TYPE]"
    echo
    echo "Options:"
    echo "  -h, --help     Show this help message"
    echo "  -f, --follow   Follow log output (real-time)"
    echo "  -n, --lines    Number of lines to show (default: 50)"
    echo "  -g, --grep     Filter logs by pattern"
    echo "  -l, --list     List available log files"
    echo "  -c, --container Show container logs (default)"
    echo "  -a, --app      Show application logs"
    echo "  -s, --system   Show system logs"
    echo
    echo "Log Types:"
    echo "  container      Container logs (default)"
    echo "  app            Application logs"
    echo "  system         System logs"
    echo "  mcp            MCP server logs"
    echo "  test           Test result logs"
    echo "  uv             UV package manager logs"
    echo
    echo "Examples:"
    echo "  $0                    # Show container logs (last 50 lines)"
    echo "  $0 --follow           # Follow container logs in real-time"
    echo "  $0 --lines 100        # Show last 100 lines"
    echo "  $0 --grep 'ERROR'     # Filter logs for ERROR messages"
    echo "  $0 --list             # List available log files"
    echo "  $0 app                # Show application logs"
    echo "  $0 mcp --follow       # Follow MCP server logs"
}

# Parse command line arguments
FOLLOW=false
LINES=50
FILTER=""
LIST_FILES=false
LOG_TYPE="container"

while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            show_usage
            exit 0
            ;;
        -f|--follow)
            FOLLOW=true
            shift
            ;;
        -n|--lines)
            LINES="$2"
            shift 2
            ;;
        -g|--grep)
            FILTER="$2"
            shift 2
            ;;
        -l|--list)
            LIST_FILES=true
            shift
            ;;
        -c|--container)
            LOG_TYPE="container"
            shift
            ;;
        -a|--app)
            LOG_TYPE="app"
            shift
            ;;
        -s|--system)
            LOG_TYPE="system"
            shift
            ;;
        container|app|system|mcp|test|uv)
            LOG_TYPE="$1"
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
    echo -e "${BLUE}=== NeoZork HLD Prediction Native Container Logs ===${NC}"
    echo
    
    # List log files if requested
    if [ "$LIST_FILES" = true ]; then
        list_log_files
        exit 0
    fi
    
    # Check if container exists
    if ! check_container_exists; then
        print_error "Container 'neozork-hld-prediction' not found"
        exit 1
    fi
    
    # Handle different log types
    case "$LOG_TYPE" in
        "container")
            if ! check_container_running; then
                print_warning "Container is not running"
                print_status "Available logs:"
                list_log_files
                exit 1
            fi
            
            container_id=$(get_container_id)
            if [ -z "$container_id" ]; then
                print_error "Failed to get container ID"
                exit 1
            fi
            
            show_container_logs "$container_id" "$FOLLOW" "$LINES" "$FILTER"
            ;;
        "app")
            show_application_logs "logs/app.log" "$FOLLOW" "$LINES" "$FILTER"
            ;;
        "mcp")
            show_application_logs "logs/mcp_server.log" "$FOLLOW" "$LINES" "$FILTER"
            ;;
        "test")
            show_application_logs "logs/test_results.log" "$FOLLOW" "$LINES" "$FILTER"
            ;;
        "uv")
            if [ -d "data/cache/uv_cache" ]; then
                print_status "UV cache directory contents:"
                ls -la data/cache/uv_cache/
            else
                print_warning "UV cache directory not found"
            fi
            ;;
        "system")
            print_status "System information:"
            echo "Container status:"
            if check_container_running; then
                print_success "Running"
                container ps | grep "neozork-hld-prediction"
            else
                print_warning "Not running"
            fi
            echo
            echo "Disk usage:"
            du -sh data/ logs/ results/ 2>/dev/null || echo "Some directories not found"
            echo
            echo "Recent log files:"
            find logs -name "*.log" -type f -exec ls -la {} \; 2>/dev/null | head -10
            ;;
        *)
            print_error "Unknown log type: $LOG_TYPE"
            show_usage
            exit 1
            ;;
    esac
}

# Run main function
main "$@" 