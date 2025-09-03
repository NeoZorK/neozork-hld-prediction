#!/bin/bash
# Modern uv setup script with best practices
# This script installs uv and sets up the development environment

set -euo pipefail

# Colors for output
readonly RED='\033[0;31m'
readonly GREEN='\033[0;32m'
readonly YELLOW='\033[1;33m'
readonly BLUE='\033[0;34m'
readonly NC='\033[0m' # No Color

# Logging functions
log_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
log_success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
log_warning() { echo -e "${YELLOW}[WARNING]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

# Script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Configuration
readonly UV_VERSION="0.2.0"
readonly MIN_PYTHON_VERSION="3.8"
readonly MAX_PYTHON_VERSION="3.12"

# Check if running on macOS
is_macos() {
    [[ "$(uname)" == "Darwin" ]]
}

# Check if running on Linux
is_linux() {
    [[ "$(uname)" == "Linux" ]]
}

# Check Python version
check_python_version() {
    local python_cmd=""
    
    # Try different Python commands
    for cmd in python3 python3.11 python3.10 python3.9 python3.8 python; do
        if command -v "$cmd" >/dev/null 2>&1; then
            local version
            version=$("$cmd" --version 2>&1 | grep -oE '[0-9]+\.[0-9]+' | head -1)
            if [[ -n "$version" ]]; then
                python_cmd="$cmd"
                break
            fi
        fi
    done
    
    if [[ -z "$python_cmd" ]]; then
        log_error "No suitable Python version found. Required: Python ${MIN_PYTHON_VERSION}-${MAX_PYTHON_VERSION}"
        exit 1
    fi
    
    local major_minor
    major_minor=$("$python_cmd" --version 2>&1 | grep -oE '[0-9]+\.[0-9]+' | head -1)
    
    if [[ -n "$major_minor" ]]; then
        log_info "Found Python $major_minor"
        if [[ "$major_minor" < "$MIN_PYTHON_VERSION" || "$major_minor" > "$MAX_PYTHON_VERSION" ]]; then
            log_warning "Python version $major_minor is outside recommended range (${MIN_PYTHON_VERSION}-${MAX_PYTHON_VERSION})"
        fi
    fi
    
    echo "$python_cmd"
}

# Install uv
install_uv() {
    log_info "Installing uv package manager..."
    
    if command -v uv >/dev/null 2>&1; then
        local current_version
        current_version=$(uv --version 2>/dev/null | grep -oE '[0-9]+\.[0-9]+\.[0-9]+' || echo "unknown")
        log_info "uv is already installed (version: $current_version)"
        return 0
    fi
    
    # Create temporary directory
    local temp_dir
    temp_dir=$(mktemp -d)
    trap 'rm -rf "$temp_dir"' EXIT
    
    # Download and install uv
    if is_macos; then
        log_info "Installing uv on macOS..."
        curl -LsSf https://astral.sh/uv/install.sh | sh
    elif is_linux; then
        log_info "Installing uv on Linux..."
        curl -LsSf https://astral.sh/uv/install.sh | sh
    else
        log_error "Unsupported operating system: $(uname)"
        exit 1
    fi
    
    # Add uv to PATH
    export PATH="$HOME/.cargo/bin:$PATH"
    
    # Verify installation
    if command -v uv >/dev/null 2>&1; then
        log_success "uv successfully installed!"
        uv --version
    else
        log_error "Failed to install uv"
        exit 1
    fi
}

# Setup virtual environment
setup_venv() {
    log_info "Setting up virtual environment..."
    
    cd "$PROJECT_ROOT"
    
    if [[ -d ".venv" ]]; then
        log_info "Virtual environment already exists"
    else
        log_info "Creating new virtual environment..."
        uv venv
        log_success "Virtual environment created"
    fi
    
    # Activate virtual environment
    source .venv/bin/activate
    
    # Install project dependencies
    log_info "Installing project dependencies..."
    uv pip install -e .
    
    # Install development dependencies
    log_info "Installing development dependencies..."
    uv pip install -e ".[dev]"
    
    log_success "Dependencies installed successfully"
}

# Setup pre-commit hooks
setup_precommit() {
    log_info "Setting up pre-commit hooks..."
    
    if command -v pre-commit >/dev/null 2>&1; then
        pre-commit install
        pre-commit install --hook-type commit-msg
        log_success "Pre-commit hooks installed"
    else
        log_warning "pre-commit not found, skipping hook installation"
    fi
}

# Generate lock file
generate_lockfile() {
    log_info "Generating lock file..."
    
    cd "$PROJECT_ROOT"
    uv lock
    log_success "Lock file generated: uv.lock"
}

# Main function
main() {
    log_info "Starting uv setup for neozork-hld-prediction project..."
    
    # Check Python version
    local python_cmd
    python_cmd=$(check_python_version)
    
    # Install uv
    install_uv
    
    # Setup virtual environment
    setup_venv
    
    # Setup pre-commit hooks
    setup_precommit
    
    # Generate lock file
    generate_lockfile
    
    log_success "Setup completed successfully!"
    log_info "To activate the virtual environment, run: source .venv/bin/activate"
    log_info "To run tests: uv run pytest"
    log_info "To install new packages: uv add <package_name>"
}

# Run main function
main "$@"
