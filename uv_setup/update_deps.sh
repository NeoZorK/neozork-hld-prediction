#!/bin/bash
# Modern dependency update script using uv best practices
# This script updates dependencies and maintains lock file consistency

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
readonly BACKUP_DIR="$PROJECT_ROOT/data/backups/dependencies"
readonly LOCK_BACKUP="$BACKUP_DIR/uv.lock.backup.$(date +%Y%m%d_%H%M%S)"

# Check if uv is installed
check_uv() {
    if ! command -v uv >/dev/null 2>&1; then
        log_error "uv is not installed. Please run ./uv_setup/setup_uv.sh first"
        exit 1
    fi
    
    local version
    version=$(uv --version 2>/dev/null | grep -oE '[0-9]+\.[0-9]+\.[0-9]+' || echo "unknown")
    log_info "Using uv version: $version"
}

# Create backup directory
create_backup() {
    mkdir -p "$BACKUP_DIR"
    
    if [[ -f "$PROJECT_ROOT/uv.lock" ]]; then
        log_info "Creating backup of current lock file..."
        cp "$PROJECT_ROOT/uv.lock" "$LOCK_BACKUP"
        log_success "Lock file backed up to: $LOCK_BACKUP"
    fi
}

# Check for outdated packages
check_outdated() {
    log_info "Checking for outdated packages..."
    
    cd "$PROJECT_ROOT"
    
    # Check outdated packages
    local outdated_count
    outdated_count=$(uv pip list --outdated 2>/dev/null | wc -l || echo "0")
    
    if [[ "$outdated_count" -gt 0 ]]; then
        log_info "Found $outdated_count outdated packages"
        uv pip list --outdated
    else
        log_success "All packages are up to date"
    fi
}

# Update dependencies
update_dependencies() {
    log_info "Updating project dependencies..."
    
    cd "$PROJECT_ROOT"
    
    # Update lock file
    log_info "Updating lock file..."
    uv lock --upgrade
    
    # Install updated dependencies
    log_info "Installing updated dependencies..."
    uv sync
    
    # Verify installation
    log_info "Verifying installation..."
    uv pip check
    
    log_success "Dependencies updated successfully"
}

# Update specific package groups
update_package_groups() {
    log_info "Updating specific package groups..."
    
    cd "$PROJECT_ROOT"
    
    # Update development dependencies
    log_info "Updating development dependencies..."
    uv add --dev --upgrade pytest pytest-cov pytest-xdist pytest-mock black flake8 mypy isort pre-commit
    
    # Update ML dependencies
    log_info "Updating ML dependencies..."
    uv add --upgrade scikit-learn tensorflow torch xgboost lightgbm optuna mlflow
    
    # Update data processing dependencies
    log_info "Updating data processing dependencies..."
    uv add --upgrade pandas numpy scipy matplotlib seaborn plotly mplfinance
    
    log_success "Package groups updated successfully"
}

# Generate requirements files
generate_requirements() {
    log_info "Generating requirements files..."
    
    cd "$PROJECT_ROOT"
    
    # Generate requirements.txt for production
    uv pip freeze --exclude-editable > requirements.txt
    
    # Generate requirements-dev.txt for development
    uv pip freeze --exclude-editable --extra dev > requirements-dev.txt
    
    # Generate requirements-ml.txt for ML dependencies
    uv pip freeze --exclude-editable --extra ml > requirements-ml.txt
    
    log_success "Requirements files generated"
}

# Run tests to verify updates
run_tests() {
    log_info "Running tests to verify updates..."
    
    cd "$PROJECT_ROOT"
    
    # Run fast tests first
    if uv run pytest tests/ -m "not slow" --tb=short -n auto; then
        log_success "Fast tests passed"
    else
        log_warning "Some tests failed, but continuing with update"
    fi
}

# Check for security vulnerabilities
check_security() {
    log_info "Checking for security vulnerabilities..."
    
    cd "$PROJECT_ROOT"
    
    # Use safety if available
    if command -v safety >/dev/null 2>&1; then
        uv run safety check
    else
        log_warning "safety not installed, skipping security check"
        log_info "Install safety with: uv add safety"
    fi
}

# Docker integration
docker_integration() {
    if command -v docker >/dev/null 2>&1; then
        echo ""
        read -p "Rebuild Docker image with updated dependencies? (y/n): " rebuild
        if [[ $rebuild =~ ^[Yy]$ ]]; then
            log_info "Rebuilding Docker image..."
            
            if command -v docker-compose >/dev/null 2>&1; then
                docker-compose build --no-cache
            else
                docker compose build --no-cache
            fi
            
            if [[ $? -eq 0 ]]; then
                log_success "Docker image successfully rebuilt"
            else
                log_error "Error rebuilding Docker image"
            fi
        else
            log_info "Skipping Docker image rebuild"
        fi
    fi
}

# Cleanup old backups
cleanup_backups() {
    log_info "Cleaning up old backups..."
    
    # Keep only last 5 backups
    local backup_count
    backup_count=$(find "$BACKUP_DIR" -name "uv.lock.backup.*" | wc -l)
    
    if [[ $backup_count -gt 5 ]]; then
        find "$BACKUP_DIR" -name "uv.lock.backup.*" -printf '%T@ %p\n' | \
            sort -n | head -n $((backup_count - 5)) | \
            awk '{print $2}' | xargs rm -f
        
        log_info "Removed old backup files"
    fi
}

# Main function
main() {
    log_info "Starting dependency update process..."
    
    # Check prerequisites
    check_uv
    
    # Create backup
    create_backup
    
    # Check for outdated packages
    check_outdated
    
    # Update dependencies
    update_dependencies
    
    # Update specific package groups
    update_package_groups
    
    # Generate requirements files
    generate_requirements
    
    # Run tests
    run_tests
    
    # Check security
    check_security
    
    # Docker integration
    docker_integration
    
    # Cleanup
    cleanup_backups
    
    log_success "Dependency update process completed successfully!"
    log_info "Current lock file: uv.lock"
    log_info "Backup location: $LOCK_BACKUP"
    log_info "To rollback: cp $LOCK_BACKUP uv.lock && uv sync"
}

# Run main function
main "$@"
