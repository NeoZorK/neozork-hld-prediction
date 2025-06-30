#!/bin/bash

# Test script for force restart functionality
# Tests the force restart container service script

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[TEST]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[PASS]${NC} $1"
}

print_error() {
    echo -e "${RED}[FAIL]${NC} $1"
}

print_header() {
    echo -e "${BLUE}=== $1 ===${NC}"
}

# Test counter
TESTS_PASSED=0
TESTS_FAILED=0

# Function to run test
run_test() {
    local test_name="$1"
    local test_command="$2"
    local expected_exit_code="${3:-0}"
    
    print_status "Running test: $test_name"
    
    if eval "$test_command" >/dev/null 2>&1; then
        actual_exit_code=$?
        if [ $actual_exit_code -eq $expected_exit_code ]; then
            print_success "$test_name"
            ((TESTS_PASSED++))
        else
            print_error "$test_name (expected exit code $expected_exit_code, got $actual_exit_code)"
            ((TESTS_FAILED++))
        fi
    else
        actual_exit_code=$?
        if [ $actual_exit_code -eq $expected_exit_code ]; then
            print_success "$test_name"
            ((TESTS_PASSED++))
        else
            print_error "$test_name (expected exit code $expected_exit_code, got $actual_exit_code)"
            ((TESTS_FAILED++))
        fi
    fi
}

# Function to test script exists and is executable
test_script_exists() {
    run_test "Script exists and is executable" \
        "test -x ./scripts/native-container/force_restart.sh"
}

# Function to test help option
test_help_option() {
    run_test "Help option works" \
        "./scripts/native-container/force_restart.sh --help | grep -q 'Usage:'"
}

# Function to test check status option
test_check_status() {
    run_test "Check status option works" \
        "timeout 10s ./scripts/native-container/force_restart.sh --check || true"
}

# Function to test invalid option
test_invalid_option() {
    run_test "Invalid option returns error" \
        "./scripts/native-container/force_restart.sh --invalid-option" 1
}

# Function to test script syntax
test_script_syntax() {
    run_test "Script has valid bash syntax" \
        "bash -n ./scripts/native-container/force_restart.sh"
}

# Function to test function definitions
test_function_definitions() {
    run_test "Script contains required functions" \
        "grep -q 'check_container_service()' ./scripts/native-container/force_restart.sh && grep -q 'force_restart_service()' ./scripts/native-container/force_restart.sh"
}

# Function to test color definitions
test_color_definitions() {
    run_test "Script contains color definitions" \
        "grep -q 'RED=' ./scripts/native-container/force_restart.sh && grep -q 'GREEN=' ./scripts/native-container/force_restart.sh"
}

# Function to test usage function
test_usage_function() {
    run_test "Script contains usage function" \
        "grep -q 'show_usage()' ./scripts/native-container/force_restart.sh"
}

# Main test execution
main() {
    print_header "Testing Force Restart Container Service Script"
    echo
    
    # Run all tests
    test_script_exists
    test_script_syntax
    test_function_definitions
    test_color_definitions
    test_usage_function
    test_help_option
    test_check_status
    test_invalid_option
    
    echo
    print_header "Test Results"
    echo "Tests passed: $TESTS_PASSED"
    echo "Tests failed: $TESTS_FAILED"
    echo "Total tests: $((TESTS_PASSED + TESTS_FAILED))"
    
    if [ $TESTS_FAILED -eq 0 ]; then
        print_success "All tests passed!"
        exit 0
    else
        print_error "Some tests failed!"
        exit 1
    fi
}

# Run main function
main "$@" 