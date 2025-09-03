#!/bin/bash
# Memory Optimization Test for Docker Container

set -e

echo "🧪 MEMORY OPTIMIZATION TEST FOR DOCKER"
echo "======================================"

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

# Build and start the container
echo "🔨 Building and starting Docker container..."
docker-compose down
docker-compose build --no-cache
docker-compose up -d

# Wait for container to be ready
echo "⏳ Waiting for container to be ready..."
sleep 10

# Test memory optimization
echo "🧪 Testing memory optimization..."
docker-compose exec neozork-hld python scripts/debug/test_memory_optimization.py

# Test interactive system with EURUSD data
echo "🧪 Testing interactive system with EURUSD data..."
echo "This will test the actual scenario that was causing the 'Killed' error."
echo "The test will load EURUSD data and should complete without memory issues."

# Create a test script that simulates the user interaction
cat > /tmp/test_eurusd_loading.py << 'EOF'
#!/usr/bin/env python3
import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.interactive.core.interactive_system import InteractiveSystem

def test_eurusd_loading():
    """Test loading EURUSD data in interactive system."""
    print("🧪 Testing EURUSD data loading in InteractiveSystem")
    print("=" * 50)
    
    try:
        # Create interactive system
        system = InteractiveSystem()
        
        # Simulate loading EURUSD data
        print("📁 Simulating '3 eurusd' command...")
        
        # Find EURUSD files
        data_dir = Path("data")
        eurusd_files = []
        
        for file_path in data_dir.rglob("*EURUSD*.parquet"):
            file_size_mb = file_path.stat().st_size / (1024 * 1024)
            eurusd_files.append((file_path, file_size_mb))
        
        if not eurusd_files:
            print("❌ No EURUSD files found")
            return False
        
        eurusd_files.sort(key=lambda x: x[1], reverse=True)
        
        print(f"Found {len(eurusd_files)} EURUSD files:")
        for file_path, size_mb in eurusd_files:
            print(f"   {file_path.name}: {size_mb:.1f} MB")
        
        # Test loading the largest file
        largest_file, size_mb = eurusd_files[0]
        print(f"\n🔄 Testing loading of largest file: {largest_file.name}")
        
        # Load the file using DataManager
        df = system.data_manager.load_data_from_file(str(largest_file))
        
        print(f"✅ Successfully loaded {largest_file.name}")
        print(f"   Shape: {df.shape[0]:,} rows × {df.shape[1]} columns")
        
        # Test memory usage
        memory_mb = system.data_manager._estimate_memory_usage(df)
        print(f"   Memory usage: ~{memory_mb} MB")
        
        # Clean up
        del df
        import gc
        gc.collect()
        
        print("✅ EURUSD loading test completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error during EURUSD loading test: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_eurusd_loading()
    sys.exit(0 if success else 1)
EOF

# Copy test script to container and run it
docker cp /tmp/test_eurusd_loading.py neozork-hld:/app/test_eurusd_loading.py
docker-compose exec neozork-hld python test_eurusd_loading.py

# Clean up
rm -f /tmp/test_eurusd_loading.py

echo ""
echo "✅ Memory optimization test completed!"
echo ""
echo "📊 SUMMARY:"
echo "   - Memory optimization features are working"
echo "   - Large file loading is handled properly"
echo "   - EURUSD data can be loaded without memory issues"
echo ""
echo "🚀 You can now run the interactive system safely:"
echo "   docker-compose exec neozork-hld ./interactive_system.py"
echo ""
echo "💡 When loading data, use: '3 eurusd' to load EURUSD files"
echo "   The system will now handle large files without being killed."
