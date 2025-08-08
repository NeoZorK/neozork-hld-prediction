#!/bin/bash

# Safe Test Runner for Apple Native Container
# This script provides a safe way to run tests in Apple native container
# with fixes for segmentation faults, memory issues, and path problems.

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging function
log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

# Container detection
is_container() {
    [[ -f /.dockerenv ]] || [[ "$NATIVE_CONTAINER" == "true" ]] || [[ "$DOCKER_CONTAINER" == "true" ]]
}

# Check if timeout command is available
has_timeout() {
    command -v timeout >/dev/null 2>&1
}

# Setup environment for safe testing
setup_environment() {
    log "Setting up environment for Apple native container..."
    
    # Set environment variables
    export PYTHONUNBUFFERED=1
    export PYTHONDONTWRITEBYTECODE=1
    export MPLCONFIGDIR=/tmp/matplotlib-cache
    export OMP_NUM_THREADS=1
    export MKL_NUM_THREADS=1
    export OPENBLAS_NUM_THREADS=1
    export PYTHONMALLOC=malloc
    
    # Create necessary directories
    mkdir -p /tmp/matplotlib-cache
    mkdir -p /tmp/pytest-cache
    mkdir -p /tmp/bash_history
    mkdir -p /tmp/bin
    mkdir -p /tmp/bash_config
    mkdir -p logs
    
    log "Environment setup completed"
}

# Get safe worker count for container
get_safe_worker_count() {
    if is_container; then
        # Reduce workers in container to prevent memory issues
        local cpu_count=$(nproc 2>/dev/null || echo 2)
        echo $((cpu_count < 2 ? cpu_count : 2))
    else
        nproc 2>/dev/null || echo 4
    fi
}

# Run command with timeout (if available)
run_with_timeout() {
    local timeout_seconds="$1"
    shift
    local cmd=("$@")
    
    if has_timeout; then
        timeout -k 10 "$timeout_seconds" "${cmd[@]}"
    else
        # Fallback for systems without timeout command
        log "Warning: timeout command not available, running without timeout"
        "${cmd[@]}"
    fi
}

# Run tests with safety measures
run_safe_tests() {
    local test_path="${1:-tests}"
    local max_workers=$(get_safe_worker_count)
    local timeout="${2:-600}"
    
    log "Running tests with $max_workers workers and ${timeout}s timeout..."
    
    # Build pytest command with safety options
    local cmd=(
        "uv" "run" "pytest"
        "$test_path"
        "-v"
        "--tb=short"
        "--disable-warnings"
        "--color=yes"
        "-n" "$max_workers"
        "--maxfail=5"
        "--durations=10"
        "--junitxml=logs/test-results.xml"
    )
    
    # Add container-specific options
    if is_container; then
        cmd+=(
            "--disable-pytest-warnings"
            "--no-header"
            "--no-summary"
            "--strict-markers"
        )
    fi
    
    # Add markers for safe categories
    if is_container; then
        cmd+=("-m" "not slow and not performance")
    fi
    
    log "Command: ${cmd[*]}"
    
    # Run tests with timeout
    if run_with_timeout "$timeout" "${cmd[@]}"; then
        success "Tests completed successfully"
        return 0
    else
        error "Tests failed or timed out"
        return 1
    fi
}

# Run tests in stages to prevent memory issues
run_staged_tests() {
    log "Running tests in stages to prevent memory issues..."
    
    local stages=(
        "basic:unit"
        "indicators:data:export"
        "plotting"
    )
    
    local results=()
    local failed=0
    
    for stage in "${stages[@]}"; do
        local stage_name="${stage%%:*}"
        local markers="${stage##*:}"
        
        log "Running stage: $stage_name with markers: $markers"
        
        # Build command for this stage
        local cmd=(
            "uv" "run" "pytest"
            "tests"
            "-v"
            "--tb=short"
            "--disable-warnings"
            "--color=yes"
            "-n" "1"  # Single worker for stability
            "--maxfail=3"
            "-m" "$markers"
        )
        
        if is_container; then
            cmd+=(
                "--disable-pytest-warnings"
                "--no-header"
                "--no-summary"
                "--strict-markers"
            )
        fi
        
        log "Stage command: ${cmd[*]}"
        
        # Run stage with timeout
        if run_with_timeout 300 "${cmd[@]}"; then
            success "Stage $stage_name completed successfully"
            results+=("$stage_name:SUCCESS")
        else
            error "Stage $stage_name failed"
            results+=("$stage_name:FAILED")
            ((failed++))
        fi
        
        # Cleanup between stages
        log "Cleaning up after stage $stage_name..."
        python -c "import matplotlib.pyplot as plt; plt.close('all')" 2>/dev/null || true
        rm -rf /tmp/matplotlib-cache/* 2>/dev/null || true
        sleep 2
    done
    
    # Print results summary
    log "Stage results:"
    for result in "${results[@]}"; do
        local stage="${result%%:*}"
        local status="${result##*:}"
        if [[ "$status" == "SUCCESS" ]]; then
            success "  $stage: $status"
        else
            error "  $stage: $status"
        fi
    done
    
    return $failed
}

# Cleanup function
cleanup() {
    log "Cleaning up..."
    
    # Close matplotlib figures
    python -c "import matplotlib.pyplot as plt; plt.close('all')" 2>/dev/null || true
    
    # Clean temporary directories
    rm -rf /tmp/matplotlib-cache/* 2>/dev/null || true
    rm -rf /tmp/pytest-cache/* 2>/dev/null || true
    
    log "Cleanup completed"
}

# Main function
main() {
    log "Starting safe test runner for Apple native container..."
    
    # Setup environment
    setup_environment
    
    # Check if we're in a container
    if is_container; then
        log "Running in container environment"
        warning "Using reduced parallelism and memory limits"
    else
        log "Running in native environment"
    fi
    
    # Parse command line arguments
    local mode="${1:-staged}"
    local test_path="${2:-tests}"
    local timeout="${3:-600}"
    
    case "$mode" in
        "staged")
            log "Running tests in staged mode..."
            run_staged_tests
            ;;
        "single")
            log "Running tests in single mode..."
            run_safe_tests "$test_path" "$timeout"
            ;;
        "basic")
            log "Running basic tests only..."
            run_safe_tests "tests -m basic" "$timeout"
            ;;
        "indicators")
            log "Running indicator tests only..."
            run_safe_tests "tests -m indicators" "$timeout"
            ;;
        "plotting")
            log "Running plotting tests only..."
            run_safe_tests "tests -m plotting" "$timeout"
            ;;
        *)
            error "Unknown mode: $mode"
            echo "Usage: $0 [staged|single|basic|indicators|plotting] [test_path] [timeout]"
            exit 1
            ;;
    esac
    
    local exit_code=$?
    
    # Cleanup
    cleanup
    
    if [[ $exit_code -eq 0 ]]; then
        success "All tests completed successfully!"
    else
        error "Some tests failed!"
    fi
    
    exit $exit_code
}

# Trap cleanup on exit
trap cleanup EXIT

# Run main function
main "$@"
