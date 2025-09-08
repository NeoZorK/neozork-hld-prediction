#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for data loading functionality.

This script tests the data loading functionality without the interactive menu.
"""

import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from interactive.data_management import DataLoader

def test_data_loading():
    """Test data loading functionality."""
    print("🧪 Testing Data Loading Functionality")
    print("=" * 50)
    
    # Initialize data loader
    loader = DataLoader()
    
    # Test 1: Get available data sources
    print("\n1️⃣ Testing available data sources...")
    sources = loader.get_available_data_sources()
    print(f"Available sources: {sources}")
    
    # Test 2: Test CSV converted data loading
    print("\n2️⃣ Testing CSV converted data loading...")
    result = loader.load_csv_converted_data()
    print(f"CSV converted result: {result['status']}")
    if result['status'] == 'success':
        print(f"  • Loaded {result['metadata']['total_files']} files")
        print(f"  • Total size: {result['metadata']['total_size_mb']} MB")
        print(f"  • Symbols: {result['metadata']['symbols']}")
    
    # Test 3: Test raw parquet data loading
    print("\n3️⃣ Testing raw parquet data loading...")
    result = loader.load_raw_parquet_data()
    print(f"Raw parquet result: {result['status']}")
    if result['status'] == 'success':
        print(f"  • Loaded {result['metadata']['total_files']} files")
        print(f"  • Total size: {result['metadata']['total_size_mb']} MB")
        print(f"  • Symbols: {result['metadata']['symbols']}")
    
    # Test 4: Test indicators data loading
    print("\n4️⃣ Testing indicators data loading...")
    result = loader.load_indicators_data()
    print(f"Indicators result: {result['status']}")
    if result['status'] == 'success':
        print(f"  • Loaded {result['metadata']['total_files']} files")
        print(f"  • Total size: {result['metadata']['total_size_mb']} MB")
        print(f"  • Symbols: {result['metadata']['symbols']}")
    
    # Test 5: Test cleaned data loading
    print("\n5️⃣ Testing cleaned data loading...")
    result = loader.load_cleaned_data()
    print(f"Cleaned data result: {result['status']}")
    if result['status'] == 'success':
        print(f"  • Loaded {result['metadata']['total_files']} files")
        print(f"  • Total size: {result['metadata']['total_size_mb']} MB")
        print(f"  • Symbols: {result['metadata']['symbols']}")
    
    print("\n✅ Data loading tests completed!")

if __name__ == "__main__":
    test_data_loading()
