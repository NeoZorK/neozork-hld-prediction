#!/bin/bash
# Dependency management script using uv
# This script provides easy commands for managing project dependencies

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

# Check if uv is installed
check_uv() {
    if ! command -v uv >/dev/null 2>&1; then
        log_error "uv is not installed. Please run ./uv_setup/setup_uv.sh first"
        exit 1
    fi
}

# Check if virtual environment exists
check_venv() {
    if [[ ! -d "$PROJECT_ROOT/.venv" ]]; then
        log_warning "Virtual environment not found. Creating one..."
        cd "$PROJECT_ROOT"
        uv venv
        log_success "Virtual environment created"
    fi
}

# Add package
add_package() {
    local package="$1"
    local extra="${2:-}"
    
    log_info "Adding package: $package"
    
    cd "$PROJECT_ROOT"
    
    if [[ -n "$extra" ]]; then
        uv add --extra "$extra" "$package"
    else
        uv add "$package"
    fi
    
    log_success "Package $package added successfully"
}

# Add development package
add_dev_package() {
    local package="$1"
    
    log_info "Adding development package: $package"
    
    cd "$PROJECT_ROOT"
    uv add --dev "$package"
    
    log_success "Development package $package added successfully"
}

# Remove package
remove_package() {
    local package="$1"
    
    log_info "Removing package: $package"
    
    cd "$PROJECT_ROOT"
    uv remove "$package"
    
    log_success "Package $package removed successfully"
}

# List packages
list_packages() {
    log_info "Listing installed packages..."
    
    cd "$PROJECT_ROOT"
    uv pip list
}

# Show package info
show_package() {
    local package="$1"
    
    log_info "Showing info for package: $package"
    
    cd "$PROJECT_ROOT"
    uv pip show "$package"
}

# Check outdated packages
check_outdated() {
    log_info "Checking for outdated packages..."
    
    cd "$PROJECT_ROOT"
    uv pip list --outdated
}

# Update specific package
update_package() {
    local package="$1"
    
    log_info "Updating package: $package"
    
    cd "$PROJECT_ROOT"
    uv add --upgrade "$package"
    
    log_success "Package $package updated successfully"
}

# Sync dependencies
sync_dependencies() {
    log_info "Syncing dependencies..."
    
    cd "$PROJECT_ROOT"
    uv sync
    
    log_success "Dependencies synced successfully"
}

# Generate lock file
generate_lock() {
    log_info "Generating lock file..."
    
    cd "$PROJECT_ROOT"
    uv lock
    
    log_success "Lock file generated"
}

# Install from lock file
install_from_lock() {
    log_info "Installing from lock file..."
    
    cd "$PROJECT_ROOT"
    uv sync --frozen
    
    log_success "Dependencies installed from lock file"
}

# Show dependency tree
show_tree() {
    log_info "Showing dependency tree..."
    
    cd "$PROJECT_ROOT"
    uv pip list --tree
}

# Check for conflicts
check_conflicts() {
    log_info "Checking for dependency conflicts..."
    
    cd "$PROJECT_ROOT"
    uv pip check
    
    log_success "Dependency check completed"
}

# Export requirements
export_requirements() {
    local format="${1:-txt}"
    
    log_info "Exporting requirements in $format format..."
    
    cd "$PROJECT_ROOT"
    
    case "$format" in
        "txt")
            uv pip freeze --exclude-editable > requirements.txt
            log_success "Requirements exported to requirements.txt"
            ;;
        "toml")
            uv pip freeze --exclude-editable --format toml > requirements.toml
            log_success "Requirements exported to requirements.toml"
            ;;
        "json")
            uv pip freeze --exclude-editable --format json > requirements.json
            log_success "Requirements exported to requirements.json"
            ;;
        *)
            log_error "Unsupported format: $format. Use txt, toml, or json"
            exit 1
            ;;
    esac
}

# Show help
show_help() {
    cat << EOF
Usage: $0 <command> [options]

Commands:
  add <package> [extra]     Add a package (optionally with extra)
  add-dev <package>         Add a development package
  remove <package>          Remove a package
  list                      List all installed packages
  show <package>            Show package information
  outdated                  Check for outdated packages
  update <package>          Update a specific package
  sync                      Sync dependencies with lock file
  lock                      Generate lock file
  install-lock              Install from lock file
  tree                      Show dependency tree
  check                     Check for dependency conflicts
  export [format]           Export requirements (txt, toml, json)
  help                      Show this help message

Examples:
  $0 add pandas
  $0 add-dev pytest
  $0 add fastapi api
  $0 remove unused-package
  $0 update numpy
  $0 export toml

EOF
}

# Main function
main() {
    # Check prerequisites
    check_uv
    check_venv
    
    # Parse command
    case "${1:-help}" in
        "add")
            if [[ $# -lt 2 ]]; then
                log_error "Package name required for add command"
                exit 1
            fi
            add_package "$2" "${3:-}"
            ;;
        "add-dev")
            if [[ $# -lt 2 ]]; then
                log_error "Package name required for add-dev command"
                exit 1
            fi
            add_dev_package "$2"
            ;;
        "remove")
            if [[ $# -lt 2 ]]; then
                log_error "Package name required for remove command"
                exit 1
            fi
            remove_package "$2"
            ;;
        "list")
            list_packages
            ;;
        "show")
            if [[ $# -lt 2 ]]; then
                log_error "Package name required for show command"
                exit 1
            fi
            show_package "$2"
            ;;
        "outdated")
            check_outdated
            ;;
        "update")
            if [[ $# -lt 2 ]]; then
                log_error "Package name required for update command"
                exit 1
            fi
            update_package "$2"
            ;;
        "sync")
            sync_dependencies
            ;;
        "lock")
            generate_lock
            ;;
        "install-lock")
            install_from_lock
            ;;
        "tree")
            show_tree
            ;;
        "check")
            check_conflicts
            ;;
        "export")
            export_requirements "${2:-txt}"
            ;;
        "help"|"--help"|"-h")
            show_help
            ;;
        *)
            log_error "Unknown command: $1"
            show_help
            exit 1
            ;;
    esac
}

# Run main function
main "$@"
