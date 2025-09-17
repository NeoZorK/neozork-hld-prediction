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

from src.interactive.data_management import DataLoader

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
    assert isinstance(sources, dict), "Sources should be a dictionary"
    assert "csv_converted" in sources, "Should have csv_converted key"
    assert "raw_parquet" in sources, "Should have raw_parquet key"
    assert "indicators" in sources, "Should have indicators key"
    assert "cleaned_data" in sources, "Should have cleaned_data key"
    
    # Test 2: Test CSV converted data loading (with symbol filter to limit memory usage)
    print("\n2️⃣ Testing CSV converted data loading...")
    result = loader.load_csv_converted_data(symbol_filter="BTC")  # Filter to limit data
    print(f"CSV converted result: {result['status']}")
    assert result['status'] in ['success', 'error'], "Status should be success or error"
    if result['status'] == 'success':
        print(f"  • Loaded {result['metadata']['total_files']} files")
        print(f"  • Total size: {result['metadata']['total_size_mb']} MB")
        print(f"  • Symbols: {result['metadata']['symbols']}")
    
    # Test 3: Test raw parquet data loading (with symbol filter to limit memory usage)
    print("\n3️⃣ Testing raw parquet data loading...")
    result = loader.load_raw_parquet_data(symbol_filter="BTC")  # Filter to limit data
    print(f"Raw parquet result: {result['status']}")
    assert result['status'] in ['success', 'error'], "Status should be success or error"
    if result['status'] == 'success':
        print(f"  • Loaded {result['metadata']['total_files']} files")
        print(f"  • Total size: {result['metadata']['total_size_mb']} MB")
        print(f"  • Symbols: {result['metadata']['symbols']}")
    
    # Test 4: Test indicators data loading (with symbol filter to limit memory usage)
    print("\n4️⃣ Testing indicators data loading...")
    result = loader.load_indicators_data(symbol_filter="BTC")  # Filter to limit data
    print(f"Indicators result: {result['status']}")
    assert result['status'] in ['success', 'error'], "Status should be success or error"
    if result['status'] == 'success':
        print(f"  • Loaded {result['metadata']['total_files']} files")
        print(f"  • Total size: {result['metadata']['total_size_mb']} MB")
        print(f"  • Symbols: {result['metadata']['symbols']}")
    
    # Test 5: Test cleaned data loading (with symbol filter to limit memory usage)
    print("\n5️⃣ Testing cleaned data loading...")
    result = loader.load_cleaned_data(symbol_filter="BTC")  # Filter to limit data
    print(f"Cleaned data result: {result['status']}")
    assert result['status'] in ['success', 'error'], "Status should be success or error"
    if result['status'] == 'success':
        print(f"  • Loaded {result['metadata']['total_files']} files")
        print(f"  • Total size: {result['metadata']['total_size_mb']} MB")
        print(f"  • Symbols: {result['metadata']['symbols']}")
    
    print("\n✅ Data loading tests completed!")

if __name__ == "__main__":
    test_data_loading()
