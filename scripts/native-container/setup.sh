#!/bin/bash

# Native Container Setup Script for NeoZork HLD Prediction
# This script sets up the native Apple Silicon container environment
# Full feature parity with Docker container

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

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to check macOS version
check_macos_version() {
    print_status "Checking macOS version..."
    
    # Get macOS version
    macos_version=$(sw_vers -productVersion)
    print_status "macOS version: $macos_version"
    
    # Check if it's macOS 26 or higher (Tahoe)
    major_version=$(echo $macos_version | cut -d. -f1)
    if [ "$major_version" -ge 26 ]; then
        print_success "macOS version is compatible (26+)"
        return 0
    else
        print_warning "macOS version $macos_version detected"
        print_warning "Native container is designed for macOS 26+ (Tahoe)"
        print_warning "Some features may not work correctly"
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
        print_error "Please install it from the macOS Developer Beta"
        print_error "You can download it from: https://developer.apple.com/download/all/"
        return 1
    fi
}

# Function to check Python installation
check_python() {
    print_status "Checking Python installation..."
    
    if command_exists python3; then
        python_version=$(python3 --version 2>&1)
        print_success "Python found: $python_version"
        
        # Check if it's Python 3.11 or higher
        major_version=$(python3 -c "import sys; print(sys.version_info.major)")
        minor_version=$(python3 -c "import sys; print(sys.version_info.minor)")
        
        if [ "$major_version" -eq 3 ] && [ "$minor_version" -ge 11 ]; then
            print_success "Python version is compatible (3.11+)"
            return 0
        else
            print_warning "Python version $major_version.$minor_version detected"
            print_warning "Recommended: Python 3.11 or higher"
            return 1
        fi
    else
        print_error "Python 3 not found"
        print_error "Please install Python 3.11 or higher"
        return 1
    fi
}

# Function to check UV installation
check_uv() {
    print_status "Checking UV installation..."
    
    if command_exists uv; then
        uv_version=$(uv --version 2>/dev/null || echo "unknown")
        print_success "UV found: $uv_version"
        return 0
    else
        print_warning "UV not found - will be installed in container"
        print_status "UV will be installed automatically during container setup"
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
        "neozork_mcp_server.py"
        "cursor_mcp_config.json"
        "src/"
        "tests/"
        "data/"
        "logs/"
        "results/"
        "scripts/"
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

# Function to ensure all required directories exist
ensure_required_directories() {
    print_status "Ensuring all required directories exist..."
    
    local required_dirs=(
        "data"
        "logs"
        "results"
        "tests"
        "mql5_feed"
        "data/cache"
        "data/cache/uv_cache"
        "data/cache/csv_converted"
        "data/raw_parquet"
        "results/plots"
    )
    
    for dir in "${required_dirs[@]}"; do
        if [ ! -d "$dir" ]; then
            print_status "Creating directory: $dir"
            mkdir -p "$dir"
            chmod 755 "$dir"
        fi
    done
    
    print_success "All required directories exist"
}

# Function to validate container configuration
validate_container_config() {
    print_status "Validating container configuration..."
    
    if [ ! -f "container.yaml" ]; then
        print_error "container.yaml not found"
        return 1
    fi
    
    # Basic YAML validation
    if command_exists python3; then
        if python3 -c "import yaml; yaml.safe_load(open('container.yaml'))" 2>/dev/null; then
            print_success "Container configuration is valid YAML"
        else
            print_error "Container configuration has invalid YAML syntax"
            return 1
        fi
    else
        print_warning "Skipping YAML validation (Python not available)"
    fi
    
    return 0
}

# Function to check and remove existing container
check_and_remove_existing_container() {
    print_status "Checking for existing container..."
    
    # Check if container exists in container list (including stopped containers)
    if container list --all | grep -q "neozork-hld-prediction"; then
        print_warning "Container 'neozork-hld-prediction' already exists"
        print_status "Removing existing container..."
        
        container_id=$(container list --all | grep "neozork-hld-prediction" | awk '{print $1}')
        if container rm "$container_id"; then
            print_success "Existing container removed"
        else
            print_error "Failed to remove existing container"
            return 1
        fi
    fi
    
    # Check if container directory exists in filesystem
    if [ -d "$HOME/Library/Application Support/com.apple.container/containers/neozork-hld-prediction" ]; then
        print_warning "Container directory exists in filesystem"
        print_status "Removing container directory..."
        
        if rm -rf "$HOME/Library/Application Support/com.apple.container/containers/neozork-hld-prediction"; then
            print_success "Container directory removed"
        else
            print_error "Failed to remove container directory"
            return 1
        fi
    fi
    
    return 0
}

# Function to create container
create_container() {
    print_status "Creating native container..."
    
    # Get absolute paths
    local project_root=$(pwd)
    local entrypoint_file="$project_root/container-entrypoint.sh"
    
    # Verify entrypoint file exists
    if [ ! -f "$entrypoint_file" ]; then
        print_error "Entrypoint file does not exist: $entrypoint_file"
        return 1
    fi
    
    print_status "Using project root: $project_root"
    print_status "Creating container with volume mounts"
    
    # Create container using native container application with volume mounts
    if container create \
        --name neozork-hld-prediction \
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
        --env PYTHONUNBUFFERED=1 \
        --env PYTHONDONTWRITEBYTECODE=1 \
        --env MPLCONFIGDIR=/tmp/matplotlib-cache \
        --volume "$project_root:/app" \
        --volume "$project_root/data:/app/data" \
        --volume "$project_root/logs:/app/logs" \
        --volume "$project_root/results:/app/results" \
        --volume "$project_root/tests:/app/tests" \
        --volume "$project_root/mql5_feed:/app/mql5_feed" \
        --volume "$project_root/data/cache/uv_cache:/app/.uv_cache" \
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

# Function to build container
build_container() {
    print_status "Building container image..."
    
    # For native container, we don't need to build separately
    # The container is created and ready to use
    print_success "Container is ready to use (no separate build step needed)"
    return 0
}

# Function to show next steps
show_next_steps() {
    echo
    print_success "=== Setup Complete! ==="
    echo
    print_status "Next steps:"
    echo "  1. Run the container: ./scripts/native-container/run.sh"
    echo "  2. Stop the container: ./scripts/native-container/stop.sh"
    echo "  3. View logs: ./scripts/native-container/logs.sh"
    echo "  4. Execute commands: ./scripts/native-container/exec.sh"
    echo
    print_status "Available commands inside container:"
    echo "  - nz: Main analysis command"
    echo "  - eda: EDA analysis command"
    echo "  - uv-install: Install dependencies"
    echo "  - uv-update: Update dependencies"
    echo "  - uv-test: Run UV environment test"
    echo "  - uv-pytest: Run pytest with UV"
    echo "  - mcp-start: Start MCP server"
    echo "  - mcp-check: Check MCP server status"
    echo
    print_status "Documentation:"
    echo "  - Native container setup: docs/deployment/native-container-setup.md"
    echo "  - Comparison with Docker: docs/deployment/native-vs-docker-comparison.md"
    echo
}

# Function to show usage
show_usage() {
    echo "Usage: $0 [OPTIONS]"
    echo
    echo "Options:"
    echo "  -h, --help     Show this help message"
    echo
    echo "Description:"
    echo "  This script sets up the native Apple Silicon container environment"
    echo "  for the NeoZork HLD Prediction project with full Docker parity."
    echo
    echo "Prerequisites:"
    echo "  - macOS 26+ (Tahoe) or higher"
    echo "  - Native container application installed"
    echo "  - Python 3.11+ installed"
    echo "  - At least 4GB of available RAM"
    echo "  - 10GB of available disk space"
    echo
    echo "Features:"
    echo "  - UV package manager support"
    echo "  - MCP server integration"
    echo "  - Command wrappers (nz, eda, uv-*)"
    echo "  - Bash history and configuration"
    echo "  - External data feed tests"
    echo "  - Full Docker container parity"
    echo
    echo "Examples:"
    echo "  $0              # Run setup"
    echo "  $0 --help       # Show this help message"
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            show_usage
            exit 0
            ;;
        *)
            print_error "Unknown option: $1"
            show_usage
            exit 1
            ;;
    esac
done

# Main setup function
main() {
    echo -e "${BLUE}=== NeoZork HLD Prediction Native Container Setup (Full Docker Parity) ===${NC}"
    echo
    
    # Check prerequisites
    print_status "Checking prerequisites..."
    
    local errors=0
    
    # Check macOS version
    if ! check_macos_version; then
        ((errors++))
    fi
    
    # Check native container application
    if ! check_native_container; then
        ((errors++))
    fi
    
    # Check Python installation
    if ! check_python; then
        ((errors++))
    fi
    
    # Check UV installation (optional)
    check_uv
    
    # Check project structure
    if ! check_project_structure; then
        ((errors++))
    fi
    
    if [ $errors -gt 0 ]; then
        print_error "Setup failed due to $errors error(s)"
        print_error "Please fix the issues above and run setup again"
        exit 1
    fi
    
    print_success "All prerequisites met"
    echo
    
    # Create UV cache directory
    create_uv_cache
    
    # Ensure all required directories exist
    ensure_required_directories
    
    # Validate container configuration
    if ! validate_container_config; then
        print_error "Container configuration validation failed"
        exit 1
    fi
    
    # Check and remove existing container
    if ! check_and_remove_existing_container; then
        print_error "Failed to remove existing container"
        exit 1
    fi
    
    # Create container
    if ! create_container; then
        print_error "Container creation failed"
        exit 1
    fi
    
    # Build container
    if ! build_container; then
        print_error "Container build failed"
        exit 1
    fi
    
    # Show next steps
    show_next_steps
}

# Run main function
main "$@" 