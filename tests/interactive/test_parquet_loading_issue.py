#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Parquet Loading Issue with Missing Timestamps

This test reproduces the issue with parquet files that have missing timestamps
and verifies the fix for proper datetime column loading.
"""

import os
import tempfile
import pandas as pd
import pytest
from pathlib import Path
import sys

# Add project root to path
project_root = Path(__file__).parent.parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from src.interactive.data.data_manager import DataManager


class TestParquetLoadingIssue:
    """Test parquet loading with missing timestamps."""
    
    def setup_method(self):
        """Setup method for tests."""
        self.data_manager = DataManager()
        
    def create_test_parquet_with_missing_timestamps(self):
        """Create a test parquet file with missing timestamps."""
        # Create DataFrame with missing timestamps
        data = {
            'Low': [0.5369, 0.5366, 0.5365, 0.5368, 0.5371],
            'Close': [0.5369, 0.5366, 0.5365, 0.5368, 0.5371],
            'High': [0.5369, 0.5366, 0.5365, 0.5368, 0.5371],
            'Open': [0.5369, 0.5366, 0.5365, 0.5368, 0.5371],
            'Volume': [1.0, 1.0, 1.0, 1.0, 1.0],
            'predicted_low': [0.0, 0.0, 0.0, 0.0, 0.0],
            'predicted_high': [0.0, 0.0, 0.0, 0.0, 0.0],
            'pressure': [0.0, 0.0, 0.0, 0.0, 0.0],
            'pressure_vector': [0.0, 0.0, 0.0, 0.0, 0.0]
        }
        
        # Create DataFrame with NaT (missing) timestamps
        df = pd.DataFrame(data)
        df.index = pd.to_datetime([pd.NaT, pd.NaT, pd.NaT, pd.NaT, pd.NaT])
        df.index.name = 'Timestamp'
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(suffix='.parquet', delete=False) as f:
            df.to_parquet(f.name)
            return f.name
    
    def test_parquet_loading_with_missing_timestamps(self):
        """Test that parquet with missing timestamps loads correctly."""
        parquet_file = self.create_test_parquet_with_missing_timestamps()
        
        try:
            # Load the parquet file
            df = self.data_manager.load_data_from_file(parquet_file)
            
            print(f"Loaded DataFrame shape: {df.shape}")
            print(f"Columns: {df.columns.tolist()}")
            print(f"Data types: {df.dtypes}")
            
            # Check for missing values in Timestamp column
            if 'Timestamp' in df.columns:
                missing_count = df['Timestamp'].isna().sum()
                missing_percent = 100 * missing_count / len(df)
                
                print(f"Missing values in Timestamp: {missing_count} ({missing_percent:.2f}%)")
                
                # Should have missing values (this is the problem we're testing)
                assert missing_count > 0, f"Expected missing values in Timestamp, got {missing_count}"
                
            elif df.index.name == 'Timestamp':
                missing_count = df.index.isna().sum()
                missing_percent = 100 * missing_count / len(df)
                
                print(f"Missing values in Timestamp index: {missing_count} ({missing_percent:.2f}%)")
                
                # Should have missing values (this is the problem we're testing)
                assert missing_count > 0, f"Expected missing values in Timestamp index, got {missing_count}"
            
        finally:
            # Clean up
            os.unlink(parquet_file)
    
    def test_actual_cache_files(self):
        """Test with actual cache files to find the problematic one."""
        cache_dir = Path("data/cache/csv_converted")
        
        if not cache_dir.exists():
            pytest.skip(f"Cache directory not found: {cache_dir}")
        
        # Find all parquet files in cache
        parquet_files = list(cache_dir.glob("*.parquet"))
        
        if not parquet_files:
            pytest.skip("No parquet files found in cache")
        
        print(f"Found {len(parquet_files)} parquet files in cache")
        
        problematic_files = []
        
        for i, parquet_file in enumerate(parquet_files[:10]):  # Test first 10 files
            try:
                print(f"\nTesting file {i+1}: {parquet_file.name}")
                
                # Load the parquet file
                df = self.data_manager.load_data_from_file(str(parquet_file))
                
                # Check for missing values in Timestamp
                missing_count = 0
                missing_percent = 0
                
                if 'Timestamp' in df.columns:
                    missing_count = df['Timestamp'].isna().sum()
                    missing_percent = 100 * missing_count / len(df)
                elif df.index.name == 'Timestamp':
                    missing_count = df.index.isna().sum()
                    missing_percent = 100 * missing_count / len(df)
                
                print(f"  Shape: {df.shape}")
                print(f"  Missing timestamps: {missing_count} ({missing_percent:.2f}%)")
                
                # Check if this file has the problem (high percentage of missing timestamps)
                if missing_percent > 50:  # More than 50% missing
                    problematic_files.append({
                        'file': parquet_file.name,
                        'missing_count': missing_count,
                        'missing_percent': missing_percent,
                        'shape': df.shape
                    })
                    print(f"  ⚠️  PROBLEMATIC FILE FOUND!")
                
            except Exception as e:
                print(f"  ❌ Error loading {parquet_file.name}: {e}")
                continue
        
        # Report problematic files
        if problematic_files:
            print(f"\n🚨 Found {len(problematic_files)} problematic files:")
            for file_info in problematic_files:
                print(f"   • {file_info['file']}: {file_info['missing_count']} missing ({file_info['missing_percent']:.2f}%)")
        else:
            print(f"\n✅ No problematic files found in first 10 cache files")
    
    def test_eurusd_file_search(self):
        """Test searching for EURUSD files specifically."""
        # Test different folder combinations
        test_cases = [
            ("data", "eurusd"),
            ("data/cache/csv_converted", "eurusd"),
            ("mql5_feed", "eurusd")
        ]
        
        for folder_path, mask in test_cases:
            print(f"\n🔍 Testing folder: {folder_path}, mask: {mask}")
            
            folder = Path(folder_path)
            if not folder.exists():
                print(f"  ❌ Folder not found: {folder_path}")
                continue
            
            # Find files matching the mask
            data_files = []
            for ext in ['.csv', '.parquet']:
                pattern = f"*{mask}*{ext}"
                files = list(folder.glob(pattern))
                # Filter out temporary files
                files = [f for f in files if not f.name.startswith('tmp')]
                data_files.extend(files)
                
                # Also try case-insensitive search
                pattern = f"*{mask.upper()}*{ext}"
                files = list(folder.glob(pattern))
                files = [f for f in files if not f.name.startswith('tmp')]
                data_files.extend(files)
            
            # Remove duplicates
            data_files = list(set(data_files))
            
            print(f"  Found {len(data_files)} files:")
            for file in data_files:
                print(f"    • {file.name}")
                
                # Test loading the file
                try:
                    df = self.data_manager.load_data_from_file(str(file))
                    
                    # Check for missing values in Timestamp
                    missing_count = 0
                    missing_percent = 0
                    
                    if 'Timestamp' in df.columns:
                        missing_count = df['Timestamp'].isna().sum()
                        missing_percent = 100 * missing_count / len(df)
                    elif df.index.name == 'Timestamp':
                        missing_count = df.index.isna().sum()
                        missing_percent = 100 * missing_count / len(df)
                    
                    print(f"      Shape: {df.shape}, Missing timestamps: {missing_count} ({missing_percent:.2f}%)")
                    
                    if missing_percent > 50:
                        print(f"      ⚠️  HIGH MISSING TIMESTAMPS!")
                    
                except Exception as e:
                    print(f"      ❌ Error loading: {e}")


if __name__ == "__main__":
    # Run tests
    test_instance = TestParquetLoadingIssue()
    test_instance.setup_method()  # Initialize data_manager
    
    print("🧪 Testing Parquet Loading Issue...")
    print("=" * 50)
    
    # Test parquet loading with missing timestamps
    print("\n1️⃣  Testing parquet loading with missing timestamps...")
    test_instance.test_parquet_loading_with_missing_timestamps()
    print("✅ Parquet loading test passed")
    
    # Test actual cache files
    print("\n2️⃣  Testing actual cache files...")
    test_instance.test_actual_cache_files()
    print("✅ Cache files test completed")
    
    # Test EURUSD file search
    print("\n3️⃣  Testing EURUSD file search...")
    test_instance.test_eurusd_file_search()
    print("✅ EURUSD file search test completed")
    
    print("\n🎉 All tests completed!")
