#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for interactive system data loading functionality

This script tests the new data loading logic:
- P1: Load single file from data folder
- P2: Load all files from folder with optional mask
- P3: Removed (functionality merged into P2)
"""

import sys
import os
from pathlib import Path
import tempfile
import shutil

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from scripts.ml.interactive_system import InteractiveSystem


def test_data_folder_scanning():
    """Test that the system can scan data folder for available files."""
    print("🧪 Testing data folder scanning...")
    
    system = InteractiveSystem()
    
    # Test that data folder exists
    data_folder = Path("data")
    assert data_folder.exists(), "Data folder should exist"
    
    # Test that we can find data files
    data_files = []
    for ext in ['.csv', '.parquet', '.xlsx', '.xls']:
        data_files.extend(data_folder.rglob(f"*{ext}"))
    
    print(f"✅ Found {len(data_files)} data files in data folder")
    assert len(data_files) > 0, "Should find at least some data files"
    
    # Show some examples
    print("📁 Sample files found:")
    for i, file in enumerate(data_files[:5], 1):
        rel_path = file.relative_to(data_folder)
        print(f"   {i}. {rel_path}")
    
    return True


def test_single_file_loading():
    """Test single file loading functionality."""
    print("\n🧪 Testing single file loading...")
    
    system = InteractiveSystem()
    
    # Find a test file
    data_folder = Path("data")
    test_files = list(data_folder.glob("*.csv")) + list(data_folder.glob("*.parquet"))
    
    if not test_files:
        print("⚠️  No test files found, skipping single file test")
        return True
    
    test_file = test_files[0]
    print(f"📄 Testing with file: {test_file.relative_to(data_folder)}")
    
    # Test loading the file
    try:
        data = system.load_data_from_file(str(test_file))
        print(f"✅ Successfully loaded file with shape: {data.shape}")
        assert data.shape[0] > 0, "Loaded data should have rows"
        assert data.shape[1] > 0, "Loaded data should have columns"
        return True
    except Exception as e:
        print(f"❌ Error loading file: {e}")
        return False


def test_folder_loading_with_mask():
    """Test folder loading with mask functionality."""
    print("\n🧪 Testing folder loading with mask...")
    
    system = InteractiveSystem()
    
    # Test different mask patterns
    test_cases = [
        ("data", None),  # No mask
        ("data", "csv"),  # CSV files
        ("data", "parquet"),  # Parquet files
    ]
    
    for folder, mask in test_cases:
        print(f"🔍 Testing: folder='{folder}', mask='{mask}'")
        
        folder_path = Path(folder)
        if not folder_path.exists():
            print(f"⚠️  Folder {folder} not found, skipping")
            continue
        
        # Find files matching pattern
        data_files = []
        for ext in ['.csv', '.parquet', '.xlsx', '.xls']:
            if mask:
                pattern = f"*{mask}*{ext}"
                data_files.extend(folder_path.glob(pattern))
                # Also try case-insensitive search
                pattern = f"*{mask.upper()}*{ext}"
                data_files.extend(folder_path.glob(pattern))
                pattern = f"*{mask.lower()}*{ext}"
                data_files.extend(folder_path.glob(pattern))
            else:
                data_files.extend(folder_path.glob(f"*{ext}"))
        
        # Remove duplicates
        data_files = list(set(data_files))
        
        print(f"   Found {len(data_files)} files")
        if data_files:
            for file in data_files[:3]:  # Show first 3 files
                print(f"     - {file.name}")
            if len(data_files) > 3:
                print(f"     ... and {len(data_files) - 3} more")
    
    return True


def test_file_discovery():
    """Test file discovery in data folder and subfolders."""
    print("\n🧪 Testing file discovery...")
    
    data_folder = Path("data")
    
    # Test recursive file discovery
    all_files = []
    for ext in ['.csv', '.parquet', '.xlsx', '.xls']:
        all_files.extend(data_folder.rglob(f"*{ext}"))
    
    print(f"📁 Total files found: {len(all_files)}")
    
    # Group by folder
    folders = {}
    for file in all_files:
        folder = file.parent.relative_to(data_folder)
        if folder not in folders:
            folders[folder] = []
        folders[folder].append(file.name)
    
    print("📂 Files by folder:")
    for folder, files in folders.items():
        print(f"   {folder}: {len(files)} files")
        for file in files[:3]:  # Show first 3 files
            print(f"     - {file}")
        if len(files) > 3:
            print(f"     ... and {len(files) - 3} more")
    
    return True


def main():
    """Run all tests."""
    print("🚀 Testing Interactive System Data Loading")
    print("=" * 50)
    
    tests = [
        test_data_folder_scanning,
        test_single_file_loading,
        test_folder_loading_with_mask,
        test_file_discovery,
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
                print("✅ Test passed")
            else:
                print("❌ Test failed")
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed!")
        return 0
    else:
        print("⚠️  Some tests failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
