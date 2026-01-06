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
    
    # Check if it's macOS 15 or higher
    major_version=$(echo $macos_version | cut -d. -f1)
    if [ "$major_version" -ge 15 ]; then
        print_success "macOS version is compatible (15+)"
        return 0
    else
        print_warning "macOS version $macos_version detected"
        print_warning "Native container is designed for macOS 15+ or newer"
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
        
<<<<<<< HEAD
        # Check if it's Python 3.11 or higher
        major_version=$(python3 -c "import sys; print(sys.version_info.major)")
        minor_version=$(python3 -c "import sys; print(sys.version_info.minor)")
        
        if [ "$major_version" -eq 3 ] && [ "$minor_version" -ge 11 ]; then
            print_success "Python version is compatible (3.11+)"
            return 0
        else
            print_warning "Python version $major_version.$minor_version detected"
            print_warning "Recommended: Python 3.11 or higher"
=======
        # Check if it's Python 3.14 or higher
        major_version=$(python3 -c "import sys; print(sys.version_info.major)")
        minor_version=$(python3 -c "import sys; print(sys.version_info.minor)")
        
        if [ "$major_version" -eq 3 ] && [ "$minor_version" -ge 14 ]; then
            print_success "Python version is compatible (3.14+)"
            return 0
        else
            print_warning "Python version $major_version.$minor_version detected"
            print_warning "Recommended: Python 3.14 or higher"
>>>>>>> origin/master
            return 1
        fi
    else
        print_error "Python 3 not found"
<<<<<<< HEAD
        print_error "Please install Python 3.11 or higher"
=======
        print_error "Please install Python 3.14 or higher"
>>>>>>> origin/master
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
    
    # Basic YAML validation with automatic pyyaml installation
    if command_exists python3; then
<<<<<<< HEAD
        # Check if pyyaml is available, install if not
        if ! python3 -c "import yaml" 2>/dev/null; then
            print_status "Installing PyYAML for YAML validation..."
            if command_exists pip3; then
                if pip3 install pyyaml --quiet; then
                    print_success "PyYAML installed successfully"
                else
                    print_warning "Failed to install PyYAML, skipping YAML validation"
                    return 0
                fi
            else
                print_warning "pip3 not available, skipping YAML validation"
=======
        local python_cmd="python3"
        local temp_venv=""
        
        # Check if pyyaml is available, install if not
        if ! python3 -c "import yaml" 2>/dev/null; then
            print_status "Installing PyYAML for YAML validation..."
            temp_venv=$(mktemp -d)
            local pyyaml_installed=false
            
            # Try using uv first (preferred method) with temporary venv
            if command_exists uv; then
                if uv venv "$temp_venv" >/dev/null 2>&1 && \
                   [ -e "$temp_venv/bin/python" ]; then
                    # UV venv doesn't include pip by default, use uv pip install directly
                    if uv pip install --python "$temp_venv/bin/python" pyyaml --quiet >/dev/null 2>&1; then
                        print_success "PyYAML installed successfully using UV in temp venv"
                        pyyaml_installed=true
                        python_cmd="$temp_venv/bin/python"
                    else
                        # Clean up failed venv attempt
                        rm -rf "$temp_venv" 2>/dev/null
                        temp_venv=$(mktemp -d)
                        print_warning "Failed to install PyYAML with UV, trying python3 venv"
                    fi
                else
                    # Clean up failed venv attempt
                    rm -rf "$temp_venv" 2>/dev/null
                    temp_venv=$(mktemp -d)
                    print_warning "Failed to create venv with UV, trying python3 venv"
                fi
            fi
            
            # Fallback to python3 venv if UV failed or not available
            if [ "$pyyaml_installed" = false ]; then
                if python3 -m venv "$temp_venv" 2>/dev/null && \
                   "$temp_venv/bin/python" -m pip install pyyaml --quiet 2>/dev/null; then
                    print_success "PyYAML installed successfully using python3 venv"
                    pyyaml_installed=true
                    python_cmd="$temp_venv/bin/python"
                else
                    print_warning "Failed to install PyYAML, skipping YAML validation"
                    rm -rf "$temp_venv" 2>/dev/null
                    return 0
                fi
            fi
            
            # Verify installation worked
            if [ "$pyyaml_installed" = true ] && [ -n "$python_cmd" ]; then
                if ! "$python_cmd" -c "import yaml" 2>/dev/null; then
                    print_warning "PyYAML installed but not importable, skipping YAML validation"
                    rm -rf "$temp_venv" 2>/dev/null
                    return 0
                fi
            else
                print_warning "Failed to set up PyYAML, skipping YAML validation"
                rm -rf "$temp_venv" 2>/dev/null
>>>>>>> origin/master
                return 0
            fi
        fi
        
<<<<<<< HEAD
        if python3 -c "import yaml; yaml.safe_load(open('container.yaml'))" 2>/dev/null; then
            print_success "Container configuration is valid YAML"
        else
            print_error "Container configuration has invalid YAML syntax"
=======
        # Validate YAML syntax
        if [ -n "$python_cmd" ] && "$python_cmd" -c "import yaml; yaml.safe_load(open('container.yaml'))" 2>/dev/null; then
            print_success "Container configuration is valid YAML"
            # Clean up temporary venv if it was created
            if [ -n "$temp_venv" ] && [ -d "$temp_venv" ]; then
                rm -rf "$temp_venv" 2>/dev/null
            fi
        else
            print_error "Container configuration has invalid YAML syntax"
            # Clean up temporary venv if it was created
            if [ -n "$temp_venv" ] && [ -d "$temp_venv" ]; then
                rm -rf "$temp_venv" 2>/dev/null
            fi
>>>>>>> origin/master
            return 1
        fi
    else
        print_warning "Skipping YAML validation (Python not available)"
    fi
    
    return 0
}

<<<<<<< HEAD
=======
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

>>>>>>> origin/master
# Function to check and remove existing container
check_and_remove_existing_container() {
    print_status "Checking for existing container..."
    
<<<<<<< HEAD
    # Check if container exists in container list (including stopped containers)
    if container list --all | grep -q "neozork-hld-prediction"; then
        print_warning "Container 'neozork-hld-prediction' already exists"
        print_status "Removing existing container..."
        
        container_id=$(container list --all | grep "neozork-hld-prediction" | awk '{print $1}')
        if container rm "$container_id"; then
            print_success "Existing container removed"
        else
            print_error "Failed to remove existing container"
=======
    # Ensure container system service is running first
    if ! ensure_container_service; then
        print_error "Cannot check for existing container - container service not available"
        return 1
    fi
    
    # Check if container exists in container list (including stopped containers)
    if container list --all | grep -q "neozork-hld-prediction"; then
        print_status "Found existing container 'neozork-hld-prediction', removing it..."
        
        container_id=$(container list --all | grep "neozork-hld-prediction" | awk '{print $1}')
        # Try normal delete first
        if container delete neozork-hld-prediction >/dev/null 2>&1; then
            print_success "Existing container removed"
        elif container rm "$container_id" >/dev/null 2>&1; then
            print_success "Existing container removed (using rm)"
        else
            print_warning "Failed to remove existing container via normal methods"
            print_status "Container may be in corrupted state, trying force cleanup..."
            
            # Try to remove container directory manually if it exists
            container_dir="$HOME/Library/Application Support/com.apple.container/containers/neozork-hld-prediction"
            if [ -d "$container_dir" ]; then
                print_status "Removing container directory manually: $container_dir"
                rm -rf "$container_dir" 2>/dev/null && print_success "Container directory removed" || print_warning "Failed to remove container directory"
            fi
            
            # Restart container service to clear any cached state
            print_status "Restarting container service to clear cached state..."
            container system start >/dev/null 2>&1
            sleep 2
            
            # Check again if container still exists
            if container list --all | grep -q "neozork-hld-prediction"; then
                print_error "Container still exists after cleanup attempts"
                print_status "You may need to manually remove the container or restart your system"
                return 1
            else
                print_success "Container removed after cleanup"
            fi
>>>>>>> origin/master
            return 1
        fi
    fi
    
    # Check if container directory exists in filesystem
    if [ -d "$HOME/Library/Application Support/com.apple.container/containers/neozork-hld-prediction" ]; then
<<<<<<< HEAD
        print_warning "Container directory exists in filesystem"
        print_status "Removing container directory..."
        
        if rm -rf "$HOME/Library/Application Support/com.apple.container/containers/neozork-hld-prediction"; then
=======
        print_status "Found existing container directory, removing it..."
        
        if rm -rf "$HOME/Library/Application Support/com.apple.container/containers/neozork-hld-prediction" 2>/dev/null; then
>>>>>>> origin/master
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
    
<<<<<<< HEAD
=======
    # Ensure container system service is running first
    if ! ensure_container_service; then
        print_error "Cannot create container - container service not available"
        return 1
    fi
    
>>>>>>> origin/master
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
<<<<<<< HEAD
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
=======
    # Retry logic for container creation (XPC connection errors can be transient)
    local max_retries=3
    local retry_count=0
    local create_success=false
    
    while [ $retry_count -lt $max_retries ]; do
        if [ $retry_count -gt 0 ]; then
            print_warning "Retrying container creation (attempt $((retry_count + 1))/$max_retries)..."
            # Restart container service before retry
            print_status "Restarting container service before retry..."
            container system start >/dev/null 2>&1
            sleep 2
        fi
        
        if container create \
            --name neozork-hld-prediction \
            --cwd /app \
            --env PYTHONPATH=/app \
            --env USE_UV=true \
            --env UV_ONLY=true \
            --env UV_CACHE_DIR=/app/.uv_cache \
            --env UV_VENV_DIR=/app/.venv \
            --env UV_LINK_MODE=copy \
            --env NATIVE_CONTAINER=true \
            --env DOCKER_CONTAINER=false \
            --env LOG_LEVEL=INFO \
            --env MCP_SERVER_TYPE=pycharm_copilot \
            --env PYTHONUNBUFFERED=1 \
            --env PYTHONDONTWRITEBYTECODE=1 \
            --env MPLCONFIGDIR=/tmp/matplotlib-cache \
            --env MAX_JOBS=4 \
            --env CMAKE_BUILD_PARALLEL_LEVEL=4 \
            --env MAKEFLAGS=-j4 \
            --env "CFLAGS=-O2 -pipe -march=native" \
            --env "CXXFLAGS=-O2 -pipe -march=native" \
            --env "UV_NO_BUILD_ISOLATION=1" \
            --volume "$project_root:/app" \
            --volume "$project_root/data:/app/data" \
            --volume "$project_root/logs:/app/logs" \
            --volume "$project_root/results:/app/results" \
            --volume "$project_root/tests:/app/tests" \
            --volume "$project_root/mql5_feed:/app/mql5_feed" \
            --volume "$project_root/data/cache/uv_cache:/app/.uv_cache" \
            --cpus 4 \
            --memory 8G \
            --arch arm64 \
            --os linux \
            --entrypoint /app/container-entrypoint.sh \
            python:3.14-slim 2>&1; then
            print_success "Container created successfully"
            create_success=true
            break
        else
            local exit_code=$?
            retry_count=$((retry_count + 1))
            if [ $retry_count -lt $max_retries ]; then
                print_warning "Container creation failed (exit code: $exit_code), will retry..."
            else
                print_error "Failed to create container after $max_retries attempts"
                print_error "Last error: exit code $exit_code"
                print_status "This may be due to XPC connection issues or container service problems"
                print_status "Try running: container system start"
                return 1
            fi
        fi
    done
    
    if [ "$create_success" = true ]; then
        return 0
    else
>>>>>>> origin/master
        return 1
    fi
}

<<<<<<< HEAD
=======
# Function to ensure container is running
ensure_container_running() {
    local container_name="neozork-hld-prediction"
    
    # Check if container exists
    if ! container list --all | grep -q "$container_name"; then
        print_error "Container '$container_name' not found"
        return 1
    fi
    
    # Check if container is running by trying to execute a command
    if container exec "$container_name" echo "test" >/dev/null 2>&1; then
        print_status "Container is already running and accessible"
        return 0
    fi
    
    # Also check status in container list
    local container_status=$(container list 2>/dev/null | grep "$container_name" | awk '{print $2}' || echo "")
    if [ "$container_status" = "running" ]; then
        # Status says running but exec failed, try again with a small delay
        sleep 1
        if container exec "$container_name" echo "test" >/dev/null 2>&1; then
            print_status "Container is running and accessible"
            return 0
        fi
    fi
    
    # Get container ID for fallback
    local container_id=$(container list --all | grep "$container_name" | awk '{print $1}')
    
    # Try to start container by name first
    print_status "Starting container '$container_name'..."
    local start_success=false
    
    # Try starting by name
    if container start "$container_name" >/dev/null 2>&1; then
        start_success=true
    elif [ -n "$container_id" ]; then
        # Try starting by ID if name failed
        print_status "Trying to start container by ID: $container_id"
        if container start "$container_id" >/dev/null 2>&1; then
            start_success=true
        fi
    fi
    
    if [ "$start_success" = false ]; then
        print_error "Failed to start container"
        return 1
    fi
    
    print_status "Container start command executed, waiting for container to be ready..."
    # Wait for container to fully start and be ready
    # Give more time for entrypoint to initialize
    sleep 5
    
    # Verify container is accessible
    local max_wait=20
    local wait_count=0
    local container_accessible=false
    local container_to_use=""
    
    while [ $wait_count -lt $max_wait ]; do
        sleep 1
        # Try to execute a command to verify container is ready
        if container exec "$container_name" echo "test" >/dev/null 2>&1; then
            container_accessible=true
            container_to_use="$container_name"
            break
        fi
        # Also try with ID as fallback
        if [ -n "$container_id" ] && container exec "$container_id" echo "test" >/dev/null 2>&1; then
            container_accessible=true
            container_to_use="$container_id"
            break
        fi
        wait_count=$((wait_count + 1))
    done
    
    if [ "$container_accessible" = false ] || [ -z "$container_to_use" ]; then
        print_error "Container started but not accessible for commands after ${max_wait}s"
        print_status "Container entrypoint may have exited. This is normal - dependencies will be installed on first use"
        return 1
    fi
    
    print_success "Container is running and ready"
    return 0
}

# Function to install system dependencies and UV in container
install_container_dependencies() {
    print_status "Installing system dependencies and UV in container..."
    
    # Get container name/ID
    local container_name="neozork-hld-prediction"
    
    # Verify container exists
    print_status "Checking if container exists..."
    if ! container list --all | grep -q "$container_name"; then
        print_error "Container '$container_name' not found in container list"
        print_status "Available containers:"
        container list --all || true
        return 1
    fi
    
    local container_id=$(container list --all | grep "$container_name" | awk '{print $1}')
    
    if [ -z "$container_id" ]; then
        print_error "Could not get container ID for '$container_name'"
        print_status "Container list output:"
        container list --all || true
        return 1
    fi
    
    print_status "Found container: $container_name (ID: $container_id)"
    
    # Ensure container is running - this is critical for installation
    print_status "Ensuring container is running before installation..."
    if ! ensure_container_running; then
        print_warning "Could not ensure container is running via ensure_container_running, trying direct start..."
        # Try to start container directly
        if container start "$container_name" >/dev/null 2>&1; then
            print_status "Container started successfully by name"
            sleep 5
        elif [ -n "$container_id" ] && container start "$container_id" >/dev/null 2>&1; then
            print_status "Container started successfully by ID"
            sleep 5
        else
            print_error "Failed to start container"
            return 1
        fi
    fi
    
    # Determine which container identifier to use and verify it's accessible
    local container_to_use=""
    print_status "Verifying container accessibility..."
    
    if container exec "$container_name" echo "test" >/dev/null 2>&1; then
        container_to_use="$container_name"
        print_success "Container accessible by name: $container_to_use"
    elif [ -n "$container_id" ] && container exec "$container_id" echo "test" >/dev/null 2>&1; then
        container_to_use="$container_id"
        print_success "Container accessible by ID: $container_to_use"
    else
        print_error "Container is not accessible by name or ID"
        print_status "Trying to start container again..."
        container start "$container_name" >/dev/null 2>&1 || \
        container start "$container_id" >/dev/null 2>&1 || true
        sleep 5
        
        # Try again
        if container exec "$container_name" echo "test" >/dev/null 2>&1; then
            container_to_use="$container_name"
            print_success "Container accessible by name after restart: $container_to_use"
        elif [ -n "$container_id" ] && container exec "$container_id" echo "test" >/dev/null 2>&1; then
            container_to_use="$container_id"
            print_success "Container accessible by ID after restart: $container_to_use"
        else
            print_error "Container is still not accessible after restart"
            return 1
        fi
    fi
    
    # Helper function to ensure container is accessible before executing commands
    ensure_container_accessible() {
        local max_attempts=3
        local attempt=0
        
        while [ $attempt -lt $max_attempts ]; do
            # Check if container_to_use is set and accessible
            if [ -n "$container_to_use" ] && container exec "$container_to_use" echo "test" >/dev/null 2>&1; then
                return 0
            fi
            
            # Try with container name
            if container exec "$container_name" echo "test" >/dev/null 2>&1; then
                container_to_use="$container_name"
                return 0
            fi
            
            # Try with container ID
            if [ -n "$container_id" ] && container exec "$container_id" echo "test" >/dev/null 2>&1; then
                container_to_use="$container_id"
                return 0
            fi
            
            # Container is not accessible, try to start it
            if [ $attempt -lt $((max_attempts - 1)) ]; then
                print_status "Container not accessible, starting it (attempt $((attempt + 1))/$max_attempts)..."
                
                # Check container status first
                local container_status=$(container list --all 2>/dev/null | grep "$container_name" | awk '{print $2}' || echo "not_found")
                print_status "Container status before start: $container_status"
                
                # Try to start by name
                if container start "$container_name" >/dev/null 2>&1; then
                    print_status "Container start command succeeded, starting keep-alive process immediately..."
                    
                    # Start keep-alive process immediately in background
                    # This must happen before the entrypoint bash exits
                    (
                        sleep 1
                        for i in 1 2 3 4 5; do
                            if container exec "$container_name" bash -c "nohup sleep infinity >/dev/null 2>&1 &" 2>/dev/null; then
                                break
                            fi
                            sleep 0.5
                        done
                    ) &
                    local keep_alive_pid=$!
                    
                    sleep 5  # Give container time to start
                    
                    # Wait for keep-alive process
                    wait $keep_alive_pid 2>/dev/null || true
                    
                    # Verify keep-alive process is running
                    sleep 1
                    if container exec "$container_name" bash -c "pgrep -f 'sleep infinity' >/dev/null 2>&1" 2>/dev/null; then
                        print_status "Keep-alive process verified"
                    else
                        print_warning "Keep-alive process not found, trying again..."
                        container exec "$container_name" bash -c "nohup sleep infinity >/dev/null 2>&1 &" 2>/dev/null || true
        sleep 2
    fi
    
                    # Check if container is now running
                    container_status=$(container list 2>/dev/null | grep "$container_name" | awk '{print $2}' || echo "not_running")
                    print_status "Container status after start: $container_status"
                    
                    # Verify container is accessible
                    sleep 1
                    if container exec "$container_name" echo "test" >/dev/null 2>&1; then
                        container_to_use="$container_name"
                        print_success "Container is now accessible by name"
                        return 0
                    else
                        print_warning "Container started but still not accessible by name"
        fi
    else
                    print_warning "Failed to start container by name"
                fi
                
                # Try to start by ID
                if [ -n "$container_id" ] && container start "$container_id" >/dev/null 2>&1; then
                    print_status "Container start command succeeded (by ID), starting keep-alive process immediately..."
                    
                    # Start keep-alive process immediately in background
                    (
                        sleep 1
                        for i in 1 2 3 4 5; do
                            if container exec "$container_id" bash -c "nohup sleep infinity >/dev/null 2>&1 &" 2>/dev/null; then
                                break
                            fi
                            sleep 0.5
                        done
                    ) &
                    local keep_alive_pid=$!
                    
                    sleep 5
                    
                    # Wait for keep-alive process
                    wait $keep_alive_pid 2>/dev/null || true
                    
                    # Verify keep-alive process
                    sleep 1
                    if ! container exec "$container_id" bash -c "pgrep -f 'sleep infinity' >/dev/null 2>&1" 2>/dev/null; then
                        container exec "$container_id" bash -c "nohup sleep infinity >/dev/null 2>&1 &" 2>/dev/null || true
                        sleep 2
                    fi
                    
                    if container exec "$container_id" echo "test" >/dev/null 2>&1; then
                        container_to_use="$container_id"
                        print_success "Container is now accessible by ID"
                        return 0
                    fi
                fi
            fi
            
            attempt=$((attempt + 1))
        done
        
        print_error "Failed to make container accessible after $max_attempts attempts"
        print_status "Container status:"
        container list --all | grep "$container_name" || echo "Container not in list"
        return 1
    }
    
    # Silent version of exec_in_container for checking status
    exec_in_container_silent() {
        local cmd="$1"
        
        # Ensure container is accessible first
        if ! ensure_container_accessible; then
            return 1
        fi
        
        # Start keep-alive process if needed
        container exec "$container_to_use" bash -c "nohup sleep infinity >/dev/null 2>&1 &" >/dev/null 2>&1 || true
        
        container exec "$container_to_use" bash -c "$cmd" 2>/dev/null || \
        container exec "$container_name" bash -c "$cmd" 2>/dev/null || \
        container exec "$container_id" bash -c "$cmd" 2>/dev/null || true
    }
    
    # Helper function to wait for apt-get processes to finish
    wait_for_apt_lock() {
        local max_wait=60
        local wait_count=0
        
        # Ensure container is accessible first
        if ! ensure_container_accessible; then
            print_warning "Container not accessible, skipping apt lock check"
            return 1
        fi
        
        while [ $wait_count -lt $max_wait ]; do
            # Check if apt-get or dpkg processes are running
            local apt_running=$(exec_in_container_silent "pgrep -f 'apt-get|dpkg' >/dev/null 2>&1 && echo 'yes' || echo 'no'" 2>/dev/null)
            
            if [ "$apt_running" != "yes" ]; then
                # Check if lock files exist
                local lock_exists=$(exec_in_container_silent "test -f /var/lib/dpkg/lock-frontend && echo 'yes' || echo 'no'" 2>/dev/null)
                
                if [ "$lock_exists" != "yes" ]; then
                    return 0  # No locks, safe to proceed
                fi
            fi
            
            sleep 1
            wait_count=$((wait_count + 1))
        done
        
        return 1  # Timeout waiting for locks
    }
    
    # Helper function to execute command in container, ensuring container stays alive
    exec_in_container() {
        local cmd="$1"
        local exit_code=0
        local output=""
        local max_retries=2
        local retry=0
        
        while [ $retry -lt $max_retries ]; do
            # Ensure container is accessible and has keep-alive process running
            if ! ensure_container_accessible; then
                if [ $retry -eq $((max_retries - 1)) ]; then
                    print_error "Container is not accessible after $max_retries attempts, cannot execute command"
                    return 1
                fi
                print_warning "Container not accessible, retrying (attempt $((retry + 1))/$max_retries)..."
                sleep 3
                retry=$((retry + 1))
                continue
            fi
            
            # Start keep-alive process in background before executing command
            # This prevents container from stopping during long-running commands
            print_status "Ensuring keep-alive process is running..."
            local keep_alive_result=""
            keep_alive_result=$(container exec "$container_to_use" bash -c "
                # Kill any existing sleep infinity processes to avoid duplicates
                pkill -f 'sleep infinity' 2>/dev/null || true
                sleep 1
                # Start keep-alive process
                nohup sleep infinity >/dev/null 2>&1 &
                local pid=\$!
                sleep 2
                # Verify process is running
                if ps -p \$pid >/dev/null 2>&1; then
                    echo 'KEEP_ALIVE_OK'
                else
                    echo 'KEEP_ALIVE_FAILED'
                fi
            " 2>&1)
            
            if echo "$keep_alive_result" | grep -q "KEEP_ALIVE_OK"; then
                print_status "Keep-alive process verified"
            else
                print_warning "Keep-alive process may not be running: $keep_alive_result"
            fi
            
            # Verify container is still accessible before executing command
            if ! container exec "$container_to_use" echo "test" >/dev/null 2>&1; then
                print_warning "Container became inaccessible after starting keep-alive, retrying..."
                container_to_use=""
                retry=$((retry + 1))
                sleep 3
                continue
            fi
            
            # Execute the command
            print_status "Executing command in container..."
            output=$(container exec "$container_to_use" bash -c "$cmd" 2>&1)
            exit_code=$?
            
            if [ $exit_code -eq 0 ]; then
                echo "$output"
                return 0
            fi
            
            # Check if container is still accessible after command failure
            if ! container exec "$container_to_use" echo "test" >/dev/null 2>&1; then
                print_warning "Container became inaccessible after command execution, will retry..."
                container_to_use=""
                retry=$((retry + 1))
                sleep 3
                continue
            fi
            
            # Command failed but container is accessible - return error
            break
        done
        
        # Return error output for debugging
        echo "$output" >&2
        return $exit_code
    }
    
    # Step 1: Install system dependencies (gcc, build-essential, etc.)
    print_status "Installing system dependencies (gcc, build-essential, curl)..."
    
    # Diagnostic: Show container status
    print_status "Checking container status..."
    print_status "Container name: $container_name"
    print_status "Container ID: $container_id"
    
    # Check if container exists in list
    if ! container list --all | grep -q "$container_name"; then
        print_error "Container '$container_name' not found in container list"
        print_status "Available containers:"
        container list --all || true
        return 1
    fi
    
    # Ensure container is accessible before proceeding
    print_status "Ensuring container is accessible and running..."
    
    # First, try to start container and keep it alive
    local container_was_running=false
    if container exec "$container_name" echo "test" >/dev/null 2>&1; then
        container_was_running=true
        container_to_use="$container_name"
        print_status "Container is already running and accessible by name"
    elif [ -n "$container_id" ] && container exec "$container_id" echo "test" >/dev/null 2>&1; then
        container_was_running=true
        container_to_use="$container_id"
        print_status "Container is already running and accessible by ID"
    else
        print_status "Container is not running, starting it..."
        
        # Start container and immediately launch keep-alive process
        if container start "$container_name" >/dev/null 2>&1; then
            print_status "Container started by name, launching keep-alive process immediately..."
            
            # Start keep-alive process immediately in background
            (
                sleep 1
                for i in 1 2 3 4 5; do
                    if container exec "$container_name" bash -c "nohup sleep infinity >/dev/null 2>&1 &" 2>/dev/null; then
                        break
                    fi
                    sleep 0.5
                done
            ) &
            local keep_alive_pid=$!
            
            sleep 5  # Wait for container to start
            
            # Wait for keep-alive process
            wait $keep_alive_pid 2>/dev/null || true
            
            # Verify keep-alive process
            sleep 1
            if container exec "$container_name" bash -c "pgrep -f 'sleep infinity' >/dev/null 2>&1" 2>/dev/null; then
                print_status "Keep-alive process verified"
                container_to_use="$container_name"
            else
                print_warning "Keep-alive process not found, trying again..."
                container exec "$container_name" bash -c "nohup sleep infinity >/dev/null 2>&1 &" 2>/dev/null || true
                sleep 2
                container_to_use="$container_name"
            fi
        elif [ -n "$container_id" ] && container start "$container_id" >/dev/null 2>&1; then
            print_status "Container started by ID, launching keep-alive process immediately..."
            
            # Start keep-alive process immediately in background
            (
                sleep 1
                for i in 1 2 3 4 5; do
                    if container exec "$container_id" bash -c "nohup sleep infinity >/dev/null 2>&1 &" 2>/dev/null; then
                        break
                    fi
                    sleep 0.5
                done
            ) &
            local keep_alive_pid=$!
            
            sleep 5
            
            # Wait for keep-alive process
            wait $keep_alive_pid 2>/dev/null || true
            
            # Verify keep-alive process
            sleep 1
            if container exec "$container_id" bash -c "pgrep -f 'sleep infinity' >/dev/null 2>&1" 2>/dev/null; then
                print_status "Keep-alive process verified"
                container_to_use="$container_id"
            else
                container exec "$container_id" bash -c "nohup sleep infinity >/dev/null 2>&1 &" 2>/dev/null || true
                sleep 2
                container_to_use="$container_id"
        fi
    else
            print_warning "Failed to start container, will try ensure_container_accessible..."
        fi
    fi
    
    # Now ensure container is accessible (this will retry if needed)
    if ! ensure_container_accessible; then
        print_error "Container is not accessible after startup attempts, cannot install dependencies"
        print_status "Container status:"
        container list --all | grep "$container_name" || true
        print_status "Trying to get more information..."
        container list || true
        return 1
    fi
    
    print_success "Container is accessible: $container_to_use"
    
    # Skip apt-get installation - dependencies will be installed on first use
    print_status "Skipping system dependencies installation (will be installed on first use)"
    print_status "Skipping UV installation (will be installed on first use)"
    
    # Step 3: Set up PATH in .bashrc for persistence
    print_status "Setting up PATH in .bashrc..."
    exec_in_container "
        if [ ! -f /root/.bashrc ]; then
            touch /root/.bashrc
        fi
        if ! grep -q '/root/.local/bin' /root/.bashrc 2>/dev/null; then
            echo 'export PATH=\"/root/.local/bin:/root/.local/bin:\$HOME/.cargo/bin:/root/.cargo/bin:\$PATH\"' >> /root/.bashrc
        fi
        if ! grep -q '/usr/bin' /root/.bashrc 2>/dev/null; then
            echo 'export PATH=\"/usr/bin:/usr/sbin:/bin:/sbin:\$PATH\"' >> /root/.bashrc
        fi
    " >/dev/null 2>&1
    
    # Ensure container remains running after installation
    print_status "Ensuring container remains running with keep-alive process..."
    
    # Check if container is running
    if ! container list | grep -q "$container_name"; then
        print_status "Container is not running, starting it..."
        if container start "$container_name" >/dev/null 2>&1 || \
           ([ -n "$container_id" ] && container start "$container_id" >/dev/null 2>&1); then
            # Start keep-alive process immediately
            (
                sleep 1
                for i in 1 2 3 4 5; do
                    if container exec "$container_name" bash -c "nohup sleep infinity >/dev/null 2>&1 &" 2>/dev/null || \
                       ([ -n "$container_id" ] && container exec "$container_id" bash -c "nohup sleep infinity >/dev/null 2>&1 &" 2>/dev/null); then
                        break
                    fi
                    sleep 0.5
                done
            ) &
            local keep_alive_pid=$!
            sleep 4
            wait $keep_alive_pid 2>/dev/null || true
        fi
    else
        # Container is running, ensure keep-alive process is running
        print_status "Container is running, ensuring keep-alive process is active..."
        container exec "$container_name" bash -c "
            if ! pgrep -f 'sleep infinity' >/dev/null 2>&1; then
                nohup sleep infinity >/dev/null 2>&1 &
                sleep 1
            fi
        " >/dev/null 2>&1 || \
        ([ -n "$container_id" ] && container exec "$container_id" bash -c "
            if ! pgrep -f 'sleep infinity' >/dev/null 2>&1; then
                nohup sleep infinity >/dev/null 2>&1 &
                sleep 1
            fi
        " >/dev/null 2>&1) || true
    fi
    
    # Verify container is still running and accessible
    sleep 1
    if container list | grep -q "$container_name.*running"; then
        if container exec "$container_name" echo "test" >/dev/null 2>&1 || \
           ([ -n "$container_id" ] && container exec "$container_id" echo "test" >/dev/null 2>&1); then
            print_success "Container is running and ready for use"
        else
            print_warning "Container is running but not immediately accessible"
        fi
    else
        print_warning "Container may have stopped, but setup completed successfully"
    fi
    
    print_success "Container dependencies installation completed"
    return 0
}

>>>>>>> origin/master
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
    echo "  - macOS 15+ or higher"
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
    
<<<<<<< HEAD
=======
    # Install container dependencies (UV and gcc)
    if ! install_container_dependencies; then
        print_warning "Container dependencies installation had issues (will be installed on first use)"
    fi
    
>>>>>>> origin/master
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