#!/bin/bash

# Test script for Docker container bash history functionality
# This script tests if the init_bash_history function works correctly

set -e

echo "🧪 Testing Docker container bash history functionality..."

# Build the container if needed
echo "📦 Building Docker container..."
docker build -t neozork-hld:latest .

# Test 1: Check if init_bash_history function exists in entrypoint
echo "🔍 Test 1: Checking init_bash_history function in entrypoint..."
if grep -q "init_bash_history()" docker-entrypoint.sh; then
    echo "✅ init_bash_history function found in docker-entrypoint.sh"
else
    echo "❌ init_bash_history function not found in docker-entrypoint.sh"
    exit 1
fi

# Test 2: Check if useful commands are defined in the function
echo -e "\n🔍 Test 2: Checking useful commands in init_bash_history function..."
USEFUL_COMMANDS=(
    "uv run pytest tests -n auto"
    "nz --interactive"
    "eda -dqc"
    "nz --indicators"
    "nz --metric"
)

for cmd in "${USEFUL_COMMANDS[@]}"; do
    if grep -q "$cmd" docker-entrypoint.sh; then
        echo "✅ Found command: $cmd"
    else
        echo "❌ Missing command: $cmd"
    fi
done

# Test 3: Check if history loading is configured
echo -e "\n🔍 Test 3: Checking history loading configuration..."
if grep -q "history -r" docker-entrypoint.sh; then
    echo "✅ history -r command found"
else
    echo "❌ history -r command not found"
fi

if grep -q "HISTFILE=" docker-entrypoint.sh; then
    echo "✅ HISTFILE configuration found"
else
    echo "❌ HISTFILE configuration not found"
fi

# Test 4: Run container with non-interactive test
echo -e "\n🔍 Test 4: Testing container with non-interactive command..."
CONTAINER_OUTPUT=$(docker run --rm \
    -v "$(pwd)/data:/app/data" \
    -v "$(pwd)/mql5_feed:/app/mql5_feed" \
    -v "$(pwd)/logs:/app/logs" \
    neozork-hld:latest bash -c "
echo 'Testing history initialization...'
if [ -f /tmp/bash_history/.bash_history ]; then
    echo 'History file exists'
    cat /tmp/bash_history/.bash_history
else
    echo 'History file not found'
fi
" 2>&1)

echo "Container output:"
echo "$CONTAINER_OUTPUT"

# Check if history initialization message appears
if echo "$CONTAINER_OUTPUT" | grep -q "Initializing bash history"; then
    echo "✅ History initialization message found"
else
    echo "❌ History initialization message not found"
fi

# Test 5: Test interactive mode (simulated)
echo -e "\n🔍 Test 5: Testing interactive mode simulation..."
INTERACTIVE_OUTPUT=$(docker run --rm \
    -v "$(pwd)/data:/app/data" \
    -v "$(pwd)/mql5_feed:/app/mql5_feed" \
    -v "$(pwd)/logs:/app/logs" \
    neozork-hld:latest bash -c "
echo 'n' | /app/docker-entrypoint.sh interactive 2>&1 || true
" 2>&1)

echo "Interactive mode output preview:"
echo "$INTERACTIVE_OUTPUT" | head -20

if echo "$INTERACTIVE_OUTPUT" | grep -q "Added.*useful commands to bash history"; then
    echo "✅ History initialization completed successfully"
else
    echo "❌ History initialization failed or message not found"
fi

echo -e "\n✅ Docker container history test completed!" 