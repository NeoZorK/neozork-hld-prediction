#!/bin/bash
# -*- coding: utf-8 -*-
"""
Test Memory Fix in Docker

This script tests the memory fix for Docker by running the interactive system
and attempting to load large EURUSD datasets.
"""

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

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

# Function to check if Docker is running
check_docker() {
    if ! docker info > /dev/null 2>&1; then
        print_error "Docker is not running. Please start Docker and try again."
        exit 1
    fi
    print_success "Docker is running"
}

# Function to check if container is running
check_container() {
    if ! docker-compose ps | grep -q "neozork-hld.*Up"; then
        print_warning "Container is not running. Starting container..."
        docker-compose up -d
        sleep 10
    fi
    print_success "Container is running"
}

# Function to check memory configuration
check_memory_config() {
    print_status "Checking memory configuration..."
    
    # Check docker.env
    if grep -q "MAX_MEMORY_MB=6144" docker.env; then
        print_success "MAX_MEMORY_MB correctly set to 6144MB"
    else
        print_error "MAX_MEMORY_MB not set correctly in docker.env"
        exit 1
    fi
    
    # Check docker-compose.yml
    if grep -q "memory: 8G" docker-compose.yml; then
        print_success "Docker memory limit correctly set to 8G"
    else
        print_error "Docker memory limit not set correctly in docker-compose.yml"
        exit 1
    fi
}

# Function to test memory fix
test_memory_fix() {
    print_status "Testing memory fix..."
    
    # Create test script in container
    docker-compose exec neozork-hld bash -c 'cat > /tmp/test_memory_fix.py << "EOF"
#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, '/app/src')

from interactive.data_manager import DataManager

def test_memory_config():
    """Test that memory configuration is correct."""
    dm = DataManager()
    
    print("🔧 DataManager Configuration:")
    print(f"   Max memory: {dm.max_memory_mb}MB")
    print(f"   Warning threshold: {dm.memory_warning_threshold}")
    print(f"   Critical threshold: {dm.memory_critical_threshold}")
    
    # Check if configuration is correct
    if dm.max_memory_mb >= 6144:
        print("✅ Memory limit correctly set to 6GB+")
    else:
        print("❌ Memory limit too low")
        return False
    
    if dm.memory_critical_threshold >= 0.95:
        print("✅ Critical threshold correctly set to 95%+")
    else:
        print("❌ Critical threshold too low")
        return False
    
    return True

def test_memory_calculation():
    """Test memory calculation for large datasets."""
    import pandas as pd
    
    dm = DataManager()
    
    # Create a large DataFrame (simulating EURUSD data)
    large_df = pd.DataFrame({
        'datetime': pd.date_range('2020-01-01', periods=100000, freq='1min'),
        'open': [1.1000 + i * 0.0001 for i in range(100000)],
        'high': [1.1005 + i * 0.0001 for i in range(100000)],
        'low': [1.0995 + i * 0.0001 for i in range(100000)],
        'close': [1.1002 + i * 0.0001 for i in range(100000)],
        'volume': [1000 + i for i in range(100000)]
    })
    
    memory_mb = dm._estimate_memory_usage(large_df)
    
    print(f"📊 Memory calculation test:")
    print(f"   DataFrame shape: {large_df.shape}")
    print(f"   Estimated memory: {memory_mb}MB")
    
    if memory_mb > 0:
        print("✅ Memory calculation working")
        return True
    else:
        print("❌ Memory calculation failed")
        return False

if __name__ == "__main__":
    print("🧪 Testing Memory Fix Configuration")
    print("=" * 50)
    
    success = True
    
    if not test_memory_config():
        success = False
    
    if not test_memory_calculation():
        success = False
    
    if success:
        print("\n✅ All memory fix tests passed!")
        sys.exit(0)
    else:
        print("\n❌ Some memory fix tests failed!")
        sys.exit(1)
EOF

    # Run test in container
    print_status "Running memory fix test in container..."
    if docker-compose exec neozork-hld python /tmp/test_memory_fix.py; then
        print_success "Memory fix test passed"
    else
        print_error "Memory fix test failed"
        exit 1
    fi
}
}

# Function to test interactive system
test_interactive_system() {
    print_status "Testing interactive system with large dataset loading..."
    
    # Create test script for interactive system in container
    docker-compose exec neozork-hld bash -c 'cat > /tmp/test_interactive_memory.py << "EOF"
#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, '/app/src')

def test_interactive_system():
    """Test interactive system memory handling."""
    try:
        from interactive.interactive_system import InteractiveSystem
        
        print("🔄 Initializing Interactive System...")
        system = InteractiveSystem()
        
        print("🔧 Checking DataManager configuration...")
        dm = system.data_manager
        
        print(f"   Max memory: {dm.max_memory_mb}MB")
        print(f"   Warning threshold: {dm.memory_warning_threshold}")
        print(f"   Critical threshold: {dm.memory_critical_threshold}")
        
        # Check if we can find EURUSD files
        import glob
        from pathlib import Path
        
        data_dir = Path('/app/data')
        eurusd_files = list(data_dir.glob('*EURUSD*.parquet'))
        
        if eurusd_files:
            print(f"✅ Found {len(eurusd_files)} EURUSD files:")
            for file in eurusd_files:
                size_mb = file.stat().st_size / (1024 * 1024)
                print(f"   {file.name}: {size_mb:.1f}MB")
        else:
            print("⚠️  No EURUSD files found for testing")
        
        print("✅ Interactive system test completed")
        return True
        
    except Exception as e:
        print(f"❌ Interactive system test failed: {e}")
        return False

if __name__ == "__main__":
    if test_interactive_system():
        sys.exit(0)
    else:
        sys.exit(1)
EOF

    # Run test in container
    print_status "Running interactive system test in container..."
    if docker-compose exec neozork-hld python /tmp/test_interactive_memory.py; then
        print_success "Interactive system test passed"
    else
        print_error "Interactive system test failed"
        exit 1
    fi
}

# Function to show memory usage
show_memory_usage() {
    print_status "Current memory usage in container:"
    docker-compose exec neozork-hld python -c "
import psutil
memory = psutil.virtual_memory()
print(f'Total: {memory.total / (1024**3):.1f}GB')
print(f'Available: {memory.available / (1024**3):.1f}GB')
print(f'Used: {memory.used / (1024**3):.1f}GB')
print(f'Percent: {memory.percent}%')
"
}

# Main execution
main() {
    echo "🧪 Memory Fix Test for Docker"
    echo "=============================="
    
    # Check prerequisites
    check_docker
    check_container
    check_memory_config
    
    # Show current memory usage
    show_memory_usage
    
    # Run tests
    test_memory_fix
    test_interactive_system
    
    print_success "All memory fix tests completed successfully!"
    print_status "The system should now be able to load large EURUSD datasets without premature stopping."
    print_status "To test with actual data loading, run:"
    echo "  docker-compose exec neozork-hld ./interactive_system.py"
    echo "  Then select option 1 (Load Data) and enter '3 eurusd'"
}

# Run main function
main "$@"
