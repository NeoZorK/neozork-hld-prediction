#!/bin/bash

# Test script for interactive native container functionality

echo "Testing interactive script functionality..."

# Test 1: Check if Docker is running
echo "Test 1: Checking if Docker is running..."
if container list --all >/dev/null 2>&1; then
    echo "✓ Docker is running"
else
    echo "✗ Docker is not running"
fi

# Test 2: Check container status
echo "Test 2: Checking container status..."
if container list --all | grep -q "neozork-hld-prediction"; then
    echo "✓ Container exists"
    if container list --all | grep -q "neozork-hld-prediction.*running"; then
        echo "✓ Container is running"
    else
        echo "⚠ Container exists but is stopped"
    fi
else
    echo "✗ Container does not exist"
fi

# Test 3: Test Docker check function manually
echo "Test 3: Testing Docker check function manually..."
if ! container list --all >/dev/null 2>&1; then
    echo "✗ Docker is not running (manual check)"
else
    echo "✓ Docker is running (manual check)"
fi

echo "Testing completed!" 