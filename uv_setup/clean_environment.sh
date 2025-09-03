#!/bin/bash
# Environment cleanup script for uv
# This script cleans up virtual environment, cache, and temporary files

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
readonly CACHE_DIRS=(
    ".uv_cache"
    ".pytest_cache"
    "__pycache__"
    "*.pyc"
    "*.pyo"
    "*.pyd"
    ".coverage"
    "htmlcov"
    "coverage.xml"
    ".mypy_cache"
    ".ruff_cache"
    ".black_cache"
    ".isort_cache"
)

# Check if running in project directory
check_project() {
    if [[ ! -f "$PROJECT_ROOT/pyproject.toml" ]]; then
        log_error "Not in project directory. Please run from project root."
        exit 1
    fi
    
    log_info "Project root: $PROJECT_ROOT"
}

# Clean virtual environment
clean_venv() {
    log_info "Cleaning virtual environment..."
    
    if [[ -d "$PROJECT_ROOT/.venv" ]]; then
        log_warning "Removing virtual environment..."
        rm -rf "$PROJECT_ROOT/.venv"
        log_success "Virtual environment removed"
    else
        log_info "No virtual environment found"
    fi
}

# Clean cache directories
clean_cache() {
    log_info "Cleaning cache directories..."
    
    local cleaned_count=0
    
    for pattern in "${CACHE_DIRS[@]}"; do
        if [[ "$pattern" == *"*"* ]]; then
            # Handle glob patterns
            while IFS= read -r -d '' file; do
                if [[ -f "$file" ]]; then
                    rm -f "$file"
                    ((cleaned_count++))
                fi
            done < <(find "$PROJECT_ROOT" -name "$pattern" -type f -print0 2>/dev/null || true)
        else
            # Handle directory patterns
            if [[ -d "$PROJECT_ROOT/$pattern" ]]; then
                rm -rf "$PROJECT_ROOT/$pattern"
                ((cleaned_count++))
            fi
        fi
    done
    
    # Clean __pycache__ directories recursively
    while IFS= read -r -d '' dir; do
        rm -rf "$dir"
        ((cleaned_count++))
    done < <(find "$PROJECT_ROOT" -type d -name "__pycache__" -print0 2>/dev/null || true)
    
    log_success "Cleaned $cleaned_count cache items"
}

# Clean build artifacts
clean_build() {
    log_info "Cleaning build artifacts..."
    
    local build_dirs=("build" "dist" "*.egg-info")
    local cleaned_count=0
    
    for pattern in "${build_dirs[@]}"; do
        if [[ "$pattern" == *"*"* ]]; then
            while IFS= read -r -d '' dir; do
                rm -rf "$dir"
                ((cleaned_count++))
            done < <(find "$PROJECT_ROOT" -name "$pattern" -type d -print0 2>/dev/null || true)
        else
            if [[ -d "$PROJECT_ROOT/$pattern" ]]; then
                rm -rf "$PROJECT_ROOT/$pattern"
                ((cleaned_count++))
            fi
        fi
    done
    
    log_success "Cleaned $cleaned_count build artifacts"
}

# Clean temporary files
clean_temp() {
    log_info "Cleaning temporary files..."
    
    local temp_patterns=(
        "*.tmp"
        "*.temp"
        "*.log"
        "*.bak"
        "*.swp"
        "*.swo"
        "*~"
    )
    
    local cleaned_count=0
    
    for pattern in "${temp_patterns[@]}"; do
        while IFS= read -r -d '' file; do
            rm -f "$file"
            ((cleaned_count++))
        done < <(find "$PROJECT_ROOT" -name "$pattern" -type f -print0 2>/dev/null || true)
    done
    
    log_success "Cleaned $cleaned_count temporary files"
}

# Clean uv cache
clean_uv_cache() {
    log_info "Cleaning uv cache..."
    
    if command -v uv >/dev/null 2>&1; then
        uv cache clean
        log_success "uv cache cleaned"
    else
        log_warning "uv not found, skipping cache cleanup"
    fi
}

# Show disk usage
show_disk_usage() {
    log_info "Current disk usage:"
    
    if command -v du >/dev/null 2>&1; then
        du -sh "$PROJECT_ROOT" 2>/dev/null || true
    fi
}

# Interactive cleanup
interactive_cleanup() {
    echo ""
    read -p "Do you want to remove the virtual environment? (y/n): " remove_venv
    if [[ $remove_venv =~ ^[Yy]$ ]]; then
        clean_venv
    fi
    
    echo ""
    read -p "Do you want to clean all caches? (y/n): " clean_caches
    if [[ $clean_caches =~ ^[Yy]$ ]]; then
        clean_cache
        clean_uv_cache
    fi
    
    echo ""
    read -p "Do you want to clean build artifacts? (y/n): " clean_builds
    if [[ $clean_builds =~ ^[Yy]$ ]]; then
        clean_build
    fi
    
    echo ""
    read -p "Do you want to clean temporary files? (y/n): " clean_temps
    if [[ $clean_temps =~ ^[Yy]$ ]]; then
        clean_temp
    fi
}

# Full cleanup (non-interactive)
full_cleanup() {
    log_info "Performing full cleanup..."
    
    clean_venv
    clean_cache
    clean_build
    clean_temp
    clean_uv_cache
    
    log_success "Full cleanup completed"
}

# Main function
main() {
    log_info "Starting environment cleanup..."
    
    # Check project directory
    check_project
    
    # Show current disk usage
    show_disk_usage
    
    # Check command line arguments
    if [[ $# -eq 0 ]]; then
        interactive_cleanup
    elif [[ "$1" == "--full" || "$1" == "-f" ]]; then
        full_cleanup
    elif [[ "$1" == "--help" || "$1" == "-h" ]]; then
        echo "Usage: $0 [OPTIONS]"
        echo "Options:"
        echo "  --full, -f    Perform full cleanup without prompts"
        echo "  --help, -h    Show this help message"
        echo "  (no args)     Interactive cleanup"
        exit 0
    else
        log_error "Unknown option: $1"
        echo "Use --help for usage information"
        exit 1
    fi
    
    # Show final disk usage
    echo ""
    show_disk_usage
    
    log_success "Cleanup completed successfully!"
    log_info "To recreate environment, run: ./uv_setup/setup_uv.sh"
}

# Run main function
main "$@"
