#!/bin/bash

# Native Container Setup Script for NeoZork HLD Prediction
# This script sets up the native Apple Silicon container environment

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

# Function to check project structure
check_project_structure() {
    print_status "Checking project structure..."
    
    required_files=(
        "container.yaml"
        "container-entrypoint.sh"
        "requirements.txt"
        "run_analysis.py"
        "src/"
        "tests/"
        "data/"
        "logs/"
        "results/"
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

# Function to create container
create_container() {
    print_status "Creating native container..."
    
    # Create container using native container application
    if container create --config container.yaml; then
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
    
    # Build container image
    if container build neozork-hld-prediction; then
        print_success "Container image built successfully"
        return 0
    else
        print_error "Failed to build container image"
        return 1
    fi
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
    echo
    print_status "Documentation:"
    echo "  - Native container setup: docs/deployment/native-container-setup.md"
    echo "  - Comparison with Docker: docs/deployment/native-vs-docker-comparison.md"
    echo
}

# Main setup function
main() {
    echo -e "${BLUE}=== NeoZork HLD Prediction Native Container Setup ===${NC}"
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
    
    # Validate container configuration
    if ! validate_container_config; then
        print_error "Container configuration validation failed"
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