#!/bin/bash

# Auto-run tests in Docker container
# This script automatically answers "N" to all prompts

set -e

echo "=== Auto-running tests in Docker container ==="

# Set environment variables for non-interactive mode
export DOCKER_CONTAINER=true
export USE_UV=true
export UV_ONLY=true
export PYTHONPATH=/app
export PYTHONUNBUFFERED=1

# Create necessary directories
mkdir -p /app/logs
mkdir -p /app/data/cache
mkdir -p /tmp/matplotlib-cache

# Activate virtual environment if it exists
if [ -f "/app/.venv/bin/activate" ]; then
    source /app/.venv/bin/activate
    echo "✅ Virtual environment activated"
else
    echo "⚠️  Virtual environment not found"
fi

# Function to run tests with automatic "N" response
run_tests_with_auto_n() {
    local test_command="$1"
    echo "Running: $test_command"
    
    # Use echo "N" to automatically answer "N" to prompts
    echo "N" | $test_command
}

# Run specific tests that were failing
echo "=== Running specific failing tests ==="

# Test 1: Monte indicator plotting integration
echo "Testing: Monte indicator plotting integration"
run_tests_with_auto_n "uv run pytest tests/plotting/test_monte_indicator_display.py::TestMonteIndicatorDisplay::test_monte_indicator_plotting_integration -v"

# Test 2: CLI flags
echo "Testing: CLI flags"
run_tests_with_auto_n "uv run pytest tests/cli/comprehensive/test_all_flags_pytest.py::test_basic_flags -v"

# Test 3: Seaborn supertrend enhancement
echo "Testing: Seaborn supertrend enhancement"
run_tests_with_auto_n "uv run pytest tests/plotting/test_seaborn_supertrend_enhancement.py::TestSeabornSuperTrendEnhancement::test_modern_styling -v"

# Test 4: Dual chart seaborn fix
echo "Testing: Dual chart seaborn fix"
run_tests_with_auto_n "uv run pytest tests/plotting/test_dual_chart_seaborn_fix.py::TestSeabornDualChartFix::test_no_max_ticks_error tests/plotting/test_dual_chart_seaborn_fix.py::TestSeabornDualChartFix::test_ticks_interval_calculation -v"

# Test 5: Docker container tests
echo "Testing: Docker container tests"
run_tests_with_auto_n "uv run pytest tests/docker/test_container.py -v"

# Test 6: Problematic plotting tests (optimized for Docker)
echo "Testing: Optimized plotting tests"
run_tests_with_auto_n "uv run pytest tests/plotting/test_seaborn_supertrend_enhancement.py::TestSeabornSuperTrendEnhancement::test_other_indicators_modern_styling tests/plotting/test_dual_chart_seaborn_fix.py::TestSeabornDualChartFix::test_ticks_interval_calculation -v"

# Test 7: All plotting tests with multithreading
echo "Testing: All plotting tests with multithreading"
run_tests_with_auto_n "uv run pytest tests/plotting/test_seaborn_supertrend_enhancement.py tests/plotting/test_dual_chart_seaborn_fix.py -n auto -v"

echo "=== All specific tests completed ==="

# Run all tests if requested
if [ "$1" = "--all" ]; then
    echo "=== Running all tests ==="
    run_tests_with_auto_n "uv run pytest tests -n auto"
fi

echo "✅ Test execution completed" 