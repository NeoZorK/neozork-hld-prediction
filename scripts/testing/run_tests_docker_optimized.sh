#!/bin/bash
# -*- coding: utf-8 -*-
"""
Optimized test runner for Docker environment.

This script runs tests with settings optimized for Docker containers
with limited resources and time constraints.
"""

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
MAX_WORKERS=4
TIMEOUT=15
MAX_FAIL=5
MAX_WORKER_RESTART=3

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

# Function to check if we're in Docker
is_docker() {
    [ -f /.dockerenv ] || grep -q docker /proc/1/cgroup 2>/dev/null
}

# Function to run fast tests
run_fast_tests() {
    print_status "Running fast tests optimized for Docker environment..."
    
    uv run pytest \
        -v \
        --tb=short \
        --disable-warnings \
        --timeout=$TIMEOUT \
        --timeout-method=thread \
        -n $MAX_WORKERS \
        --dist=worksteal \
        --max-worker-restart=$MAX_WORKER_RESTART \
        --maxfail=$MAX_FAIL \
        -W ignore \
        tests/eda/test_time_series_analysis_fast.py \
        tests/test_visualization_manager_fast.py \
        tests/interactive/test_core_fast.py
}

# Function to run specific failing tests
run_specific_tests() {
    print_status "Running specific tests that were failing in Docker..."
    
    uv run pytest \
        -v \
        --tb=short \
        --disable-warnings \
        --timeout=10 \
        --timeout-method=thread \
        -n 2 \
        --dist=worksteal \
        --max-worker-restart=2 \
        --maxfail=3 \
        -W ignore \
        tests/eda/test_time_series_analysis_fast.py::TestTimeSeriesAnalyzerFast::test_analyze_volatility_fast \
        tests/eda/test_time_series_analysis_fast.py::TestTimeSeriesAnalyzerFast::test_comprehensive_analysis_fast \
        tests/test_visualization_manager_fast.py::TestVisualizationManagerFast::test_create_statistics_plots_few_columns_basic_fast \
        tests/interactive/test_core_fast.py::TestInteractiveSystemFast::test_run_feature_engineering_analysis_fast
}

# Function to run optimized original tests
run_optimized_original_tests() {
    print_status "Running optimized original tests..."
    
    uv run pytest \
        -v \
        --tb=short \
        --disable-warnings \
        --timeout=$TIMEOUT \
        --timeout-method=thread \
        -n $MAX_WORKERS \
        --dist=worksteal \
        --max-worker-restart=$MAX_WORKER_RESTART \
        --maxfail=$MAX_FAIL \
        -W ignore \
        tests/eda/test_time_series_analysis.py::TestTimeSeriesAnalyzer::test_analyze_volatility \
        tests/eda/test_time_series_analysis.py::TestTimeSeriesAnalyzer::test_comprehensive_analysis_basic \
        tests/eda/test_time_series_analysis.py::TestTimeSeriesAnalyzer::test_comprehensive_analysis_no_data \
        tests/eda/test_time_series_analysis.py::TestTimeSeriesAnalyzer::test_comprehensive_analysis_small_dataset \
        tests/test_visualization_manager.py::TestVisualizationManager::test_create_statistics_plots_many_columns_basic \
        tests/interactive/test_core.py::TestInteractiveSystem::test_run_feature_engineering_analysis
}

# Function to run all tests with Docker optimizations
run_all_tests_docker() {
    print_status "Running all tests with Docker optimizations..."
    
    uv run pytest \
        -v \
        --tb=short \
        --disable-warnings \
        --timeout=30 \
        --timeout-method=thread \
        -n $MAX_WORKERS \
        --dist=worksteal \
        --max-worker-restart=$MAX_WORKER_RESTART \
        --maxfail=$MAX_FAIL \
        -W ignore \
        tests/
}

# Function to show help
show_help() {
    echo "Usage: $0 [OPTION]"
    echo ""
    echo "Options:"
    echo "  fast        Run fast tests optimized for Docker"
    echo "  specific    Run specific failing tests"
    echo "  original    Run optimized original tests"
    echo "  all         Run all tests with Docker optimizations"
    echo "  help        Show this help message"
    echo ""
    echo "Environment variables:"
    echo "  MAX_WORKERS         Number of parallel workers (default: 4)"
    echo "  TIMEOUT            Test timeout in seconds (default: 15)"
    echo "  MAX_FAIL           Maximum number of failures (default: 5)"
    echo "  MAX_WORKER_RESTART Maximum worker restarts (default: 3)"
    echo ""
    echo "Examples:"
    echo "  $0 fast"
    echo "  $0 specific"
    echo "  MAX_WORKERS=2 TIMEOUT=10 $0 all"
}

# Main script
main() {
    # Check if we're in Docker
    if is_docker; then
        print_status "Running in Docker environment"
    else
        print_warning "Not running in Docker environment - some optimizations may not be needed"
    fi
    
    # Parse command line arguments
    case "${1:-fast}" in
        fast)
            run_fast_tests
            ;;
        specific)
            run_specific_tests
            ;;
        original)
            run_optimized_original_tests
            ;;
        all)
            run_all_tests_docker
            ;;
        help|--help|-h)
            show_help
            exit 0
            ;;
        *)
            print_error "Unknown option: $1"
            show_help
            exit 1
            ;;
    esac
    
    # Check exit status
    if [ $? -eq 0 ]; then
        print_success "All tests completed successfully!"
    else
        print_error "Some tests failed!"
        exit 1
    fi
}

# Run main function with all arguments
main "$@"
