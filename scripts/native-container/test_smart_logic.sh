#!/bin/bash

# Test script for smart container logic
# This script tests the logic for handling different container states

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Container name
CONTAINER_NAME="neozork-hld-prediction"

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

# Function to check if container exists
check_container_exists() {
    if container list --all | grep -q "$CONTAINER_NAME"; then
        return 0
    else
        return 1
    fi
}

# Function to check if container is running
check_container_running() {
    if container list | grep -q "$CONTAINER_NAME"; then
        return 0
    else
        return 1
    fi
}

# Test the smart logic
echo "=== Testing Smart Container Logic ==="
echo

print_status "Checking container status..."

if check_container_exists; then
    print_success "Container exists"
    if check_container_running; then
        print_success "Container is running"
        print_status "Logic: Skip setup and start, open shell directly"
    else
        print_warning "Container exists but is stopped"
        print_status "Logic: Start existing container, then open shell"
    fi
else
    print_warning "Container does not exist"
    print_status "Logic: Run full setup sequence"
fi

echo
print_status "Container list (all):"
container list --all | grep "$CONTAINER_NAME" || echo "No container found"

echo
print_status "Container list (running):"
container list | grep "$CONTAINER_NAME" || echo "No running container found"

echo
print_success "Smart logic test completed!" 