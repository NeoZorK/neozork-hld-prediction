#!/usr/bin/env bats

# Setup - runs before each test
setup() {
    # Create a temporary directory for testing
    TEST_DIR="$(mktemp -d)"
    
    # Copy the init_dirs.sh script to the test directory
    cp "$(pwd)/scripts/init_dirs.sh" "$TEST_DIR/"
    
    # Change to the test directory
    cd "$TEST_DIR"
    
    # Make the script executable
    chmod +x init_dirs.sh
}

# Teardown - runs after each test
teardown() {
    # Remove the temporary test directory
    rm -rf "$TEST_DIR"
}

# Test if script creates all required directories
@test "check if all required directories are created" {
    # Run the script
    ./init_dirs.sh
    
    # Check if main data directories exist
    [ -d "data/cache/csv_converted" ]
    [ -d "data/raw_parquet" ]
    [ -d "data/processed" ]
    
    # Check if log and results directories exist
    [ -d "logs" ]
    [ -d "results" ]
    
    # Check if source and script directories exist
    [ -d "src/eda" ]
    [ -d "scripts/debug_scripts" ]
    [ -d "scripts/log_analysis" ]
    [ -d "scripts/data_processing" ]
    
    # Check if other required directories exist
    [ -d "notebooks" ]
    [ -d "src" ]
    [ -d "tests" ]
    [ -d "mql5_feed" ]
}

# Test if .env file is created when it doesn't exist
@test "check if .env file is created when missing" {
    # Run the script
    ./init_dirs.sh
    
    # Check if .env file exists
    [ -f ".env" ]
    
    # Check if .env file contains required fields
    grep -q "POLYGON_API_KEY=" ".env"
    grep -q "BINANCE_API_KEY=" ".env"
    grep -q "BINANCE_API_SECRET=" ".env"
}

# Test if existing .env file is not overwritten
@test "check if existing .env file is preserved" {
    # Create a custom .env file
    echo "CUSTOM_API_KEY=test_value" > ".env"
    
    # Run the script
    ./init_dirs.sh
    
    # Check if the custom content is preserved
    grep -q "CUSTOM_API_KEY=test_value" ".env"
}

# Test script execution from different directories
@test "check if script works when run from different directory" {
    # Create a subdirectory
    mkdir -p "subdir"
    cd "subdir"
    
    # Run the script from subdirectory
    ../init_dirs.sh
    
    # Check if directories are created in the correct location
    [ -d "../data/cache/csv_converted" ]
    [ -d "../data/raw_parquet" ]
    [ -d "../src/eda" ]
}

# Test directory permissions
@test "check if directories have correct permissions" {
    # Run the script
    ./init_dirs.sh
    
    # Check if directories are readable and writable
    [ -r "data/cache/csv_converted" ] && [ -w "data/cache/csv_converted" ]
    [ -r "data/raw_parquet" ] && [ -w "data/raw_parquet" ]
    [ -r "src/eda" ] && [ -w "src/eda" ]
}

# Test error handling when directory creation fails
@test "check error handling when directory creation fails" {
    # Create a file with the same name as a directory we want to create
    touch "data"
    
    # Run the script and check if it fails
    run ./init_dirs.sh
    [ "$status" -eq 1 ]
}

# Test if script is idempotent
@test "check if script is idempotent" {
    # Run the script twice
    ./init_dirs.sh
    run ./init_dirs.sh
    
    # Check if second run was successful
    [ "$status" -eq 0 ]
    
    # Check if all directories still exist
    [ -d "data/cache/csv_converted" ]
    [ -d "data/raw_parquet" ]
    [ -d "src/eda" ]
} 