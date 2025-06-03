#!/bin/bash
# Script for updating dependencies using uv

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "uv is not installed. Running installation script..."
    ./uv_setup/setup_uv.sh

    # Source the environment file to update PATH
    if [ -f "$HOME/.local/bin/env" ]; then
        source $HOME/.local/bin/env
    fi

    if [ $? -ne 0 ]; then
        echo "Failed to install uv. Please install it manually."
        exit 1
    fi
fi

# Colored output functions
info() {
    echo -e "\033[0;34m[INFO]\033[0m $1"
}

success() {
    echo -e "\033[0;32m[SUCCESS]\033[0m $1"
}

warn() {
    echo -e "\033[0;33m[WARNING]\033[0m $1"
}

error() {
    echo -e "\033[0;31m[ERROR]\033[0m $1"
}

# Get the directory of the script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$( dirname "$SCRIPT_DIR" )"

# Activate virtual environment
if [ -d ".venv" ]; then
    info "Activating virtual environment..."
    source .venv/bin/activate
else
    info "Creating virtual environment..."
    uv venv
    source .venv/bin/activate
fi

# Update dependencies
info "Updating dependencies using uv..."
uv pip install --upgrade -r "$PROJECT_ROOT/requirements.txt"

if [ $? -eq 0 ]; then
    success "Dependencies successfully updated!"

    # Generate lock file
    info "Generating lock file to pin versions..."
    uv pip freeze > "$PROJECT_ROOT/requirements-lock.txt"
    success "Lock file generated: requirements-lock.txt"

    # Display installed packages
    info "Installed packages:"
    uv pip list
else
    error "Error updating dependencies"
    exit 1
fi

# Check if docker-compose is available
if command -v docker-compose &> /dev/null || command -v docker &> /dev/null; then
    echo ""
    read -p "Rebuild Docker image with updated dependencies? (y/n): " rebuild
    if [[ $rebuild == "y" || $rebuild == "Y" ]]; then
        info "Rebuilding Docker image..."
        if command -v docker-compose &> /dev/null; then
            docker-compose build
        else
            docker compose build
        fi

        if [ $? -eq 0 ]; then
            success "Docker image successfully rebuilt!"
        else
            error "Error rebuilding Docker image"
        fi
    else
        warn "Skipping Docker image rebuild"
    fi
fi

echo ""
success "Dependency update process completed!"
