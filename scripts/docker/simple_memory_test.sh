#!/bin/bash
# Simple Memory Fix Test for Docker

set -e

echo "🧪 Simple Memory Fix Test for Docker"
echo "====================================="

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running"
    exit 1
fi
echo "✅ Docker is running"

# Check if container is running
if ! docker-compose ps | grep -q "neozork-hld.*Up"; then
    echo "⚠️  Starting container..."
    docker-compose up -d
    sleep 10
fi
echo "✅ Container is running"

# Check memory configuration
echo "🔍 Checking memory configuration..."
if grep -q "MAX_MEMORY_MB=6144" docker.env; then
    echo "✅ MAX_MEMORY_MB correctly set to 6144MB"
else
    echo "❌ MAX_MEMORY_MB not set correctly"
    exit 1
fi

if grep -q "memory: 8G" docker-compose.yml; then
    echo "✅ Docker memory limit correctly set to 8G"
else
    echo "❌ Docker memory limit not set correctly"
    exit 1
fi

# Show current memory usage
echo "📊 Current memory usage in container:"
docker-compose exec neozork-hld python -c "
import psutil
memory = psutil.virtual_memory()
print(f'Total: {memory.total / (1024**3):.1f}GB')
print(f'Available: {memory.available / (1024**3):.1f}GB')
print(f'Used: {memory.used / (1024**3):.1f}GB')
print(f'Percent: {memory.percent}%')
"

# Test DataManager configuration
echo "🧪 Testing DataManager configuration..."
docker-compose exec neozork-hld python -c "
import sys
sys.path.insert(0, '/app/src')
from interactive.data_manager import DataManager

dm = DataManager()
print(f'Max memory: {dm.max_memory_mb}MB')
print(f'Warning threshold: {dm.memory_warning_threshold}')
print(f'Critical threshold: {dm.memory_critical_threshold}')

if dm.max_memory_mb >= 6144:
    print('✅ Memory limit correctly set to 6GB+')
else:
    print('❌ Memory limit too low')
    sys.exit(1)

if dm.memory_critical_threshold >= 0.95:
    print('✅ Critical threshold correctly set to 95%+')
else:
    print('❌ Critical threshold too low')
    sys.exit(1)

print('✅ All memory configuration tests passed!')
"

echo "✅ Memory fix test completed successfully!"
echo "The system should now be able to load large EURUSD datasets without premature stopping."
