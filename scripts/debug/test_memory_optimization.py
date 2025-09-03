#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Memory Optimization Test Script

This script tests the memory optimization features in the Docker container.
"""

import os
import sys
import gc
import time
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

try:
    import psutil
    from src.interactive.data.data_manager import DataManager
except ImportError as e:
    print(f"Error importing modules: {e}")
    sys.exit(1)


def print_memory_info():
    """Print current memory usage information."""
    try:
        memory = psutil.virtual_memory()
        print(f"\n📊 MEMORY USAGE:")
        print(f"   Total: {memory.total / (1024**3):.1f} GB")
        print(f"   Available: {memory.available / (1024**3):.1f} GB")
        print(f"   Used: {memory.used / (1024**3):.1f} GB ({memory.percent:.1f}%)")
        print(f"   Free: {memory.free / (1024**3):.1f} GB")
    except Exception as e:
        print(f"⚠️  Could not get memory info: {e}")


def test_data_manager_settings():
    """Test DataManager memory settings."""
    print("\n🔧 TESTING DATA MANAGER SETTINGS")
    print("-" * 40)
    
    dm = DataManager()
    
    print(f"Memory optimization enabled: {dm.enable_memory_optimization}")
    print(f"Max memory limit: {dm.max_memory_mb} MB")
    print(f"Chunk size: {dm.chunk_size:,} rows")
    
    # Test memory availability check
    memory_available = dm._check_memory_available()
    print(f"Memory available: {memory_available}")
    
    return dm


def test_large_file_loading():
    """Test loading large files with memory optimization."""
    print("\n📁 TESTING LARGE FILE LOADING")
    print("-" * 40)
    
    dm = DataManager()
    
    # Look for large parquet files in data directory
    data_dir = Path("data")
    if not data_dir.exists():
        print("❌ Data directory not found")
        return
    
    # Find large parquet files
    large_files = []
    for file_path in data_dir.rglob("*.parquet"):
        file_size_mb = file_path.stat().st_size / (1024 * 1024)
        if file_size_mb > 50:  # Files larger than 50MB
            large_files.append((file_path, file_size_mb))
    
    if not large_files:
        print("❌ No large parquet files found")
        return
    
    # Sort by size (largest first)
    large_files.sort(key=lambda x: x[1], reverse=True)
    
    print(f"Found {len(large_files)} large files:")
    for file_path, size_mb in large_files[:5]:  # Show top 5
        print(f"   {file_path.name}: {size_mb:.1f} MB")
    
    # Test loading the largest file
    largest_file, size_mb = large_files[0]
    print(f"\n🔄 Testing loading of largest file: {largest_file.name}")
    
    print_memory_info()
    
    try:
        start_time = time.time()
        start_memory = psutil.virtual_memory().used
        
        # Load the file
        df = dm.load_data_from_file(str(largest_file))
        
        end_time = time.time()
        end_memory = psutil.virtual_memory().used
        
        load_time = end_time - start_time
        memory_used = (end_memory - start_memory) / (1024 * 1024)  # MB
        
        print(f"\n✅ Successfully loaded {largest_file.name}")
        print(f"   Shape: {df.shape[0]:,} rows × {df.shape[1]} columns")
        print(f"   Load time: {load_time:.2f} seconds")
        print(f"   Memory used: {memory_used:.1f} MB")
        print(f"   Memory per row: {memory_used / df.shape[0]:.2f} MB/row")
        
        # Clean up
        del df
        gc.collect()
        
        print_memory_info()
        
    except Exception as e:
        print(f"❌ Error loading {largest_file.name}: {e}")
        import traceback
        traceback.print_exc()


def test_multiple_file_loading():
    """Test loading multiple files with memory management."""
    print("\n📁 TESTING MULTIPLE FILE LOADING")
    print("-" * 40)
    
    # Look for EURUSD files specifically
    data_dir = Path("data")
    eurusd_files = []
    
    for file_path in data_dir.rglob("*EURUSD*.parquet"):
        file_size_mb = file_path.stat().st_size / (1024 * 1024)
        eurusd_files.append((file_path, file_size_mb))
    
    if not eurusd_files:
        print("❌ No EURUSD files found")
        return
    
    eurusd_files.sort(key=lambda x: x[1], reverse=True)
    
    print(f"Found {len(eurusd_files)} EURUSD files:")
    for file_path, size_mb in eurusd_files:
        print(f"   {file_path.name}: {size_mb:.1f} MB")
    
    print_memory_info()
    
    # Test loading multiple files
    dm = DataManager()
    all_data = []
    total_memory = 0
    
    for i, (file_path, size_mb) in enumerate(eurusd_files[:3]):  # Load first 3 files
        try:
            print(f"\n🔄 Loading file {i+1}/{min(3, len(eurusd_files))}: {file_path.name}")
            
            start_memory = psutil.virtual_memory().used
            
            df = dm.load_data_from_file(str(file_path))
            df['source_file'] = file_path.name
            
            end_memory = psutil.virtual_memory().used
            memory_used = (end_memory - start_memory) / (1024 * 1024)
            total_memory += memory_used
            
            all_data.append(df)
            
            print(f"✅ Loaded: {file_path.name} ({df.shape[0]:,} rows, ~{memory_used:.1f}MB)")
            
            # Check memory limits
            if total_memory > dm.max_memory_mb * 0.8:
                print(f"⚠️  Memory usage high ({total_memory:.1f}MB), stopping")
                break
                
        except Exception as e:
            print(f"❌ Error loading {file_path.name}: {e}")
            continue
    
    if all_data:
        print(f"\n📊 Summary:")
        print(f"   Files loaded: {len(all_data)}")
        print(f"   Total rows: {sum(df.shape[0] for df in all_data):,}")
        print(f"   Total memory used: {total_memory:.1f} MB")
        
        # Clean up
        for df in all_data:
            del df
        del all_data
        gc.collect()
        
        print_memory_info()


def main():
    """Main function."""
    print("🧪 MEMORY OPTIMIZATION TEST")
    print("=" * 50)
    
    # Check environment
    print(f"Environment variables:")
    print(f"   MAX_MEMORY_MB: {os.environ.get('MAX_MEMORY_MB', 'Not set')}")
    print(f"   CHUNK_SIZE: {os.environ.get('CHUNK_SIZE', 'Not set')}")
    print(f"   ENABLE_MEMORY_OPTIMIZATION: {os.environ.get('ENABLE_MEMORY_OPTIMIZATION', 'Not set')}")
    
    # Test DataManager settings
    dm = test_data_manager_settings()
    
    # Test large file loading
    test_large_file_loading()
    
    # Test multiple file loading
    test_multiple_file_loading()
    
    print("\n✅ Memory optimization test completed!")


if __name__ == "__main__":
    main()
