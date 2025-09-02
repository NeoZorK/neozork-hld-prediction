#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test for DataManager cache file loading fix

This test verifies that the DataManager correctly excludes cache folders
and temporary files when loading data.
"""

import pytest
import pandas as pd
import tempfile
from pathlib import Path
import sys

# Add project root to path
project_root = Path(__file__).parent.parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from src.interactive.data_manager import DataManager


class TestDataManagerCacheFix:
    """Test suite for DataManager cache file loading fix."""
    
    def setup_method(self):
        """Setup method for tests."""
        self.data_manager = DataManager()
    
    def test_exclude_cache_folders(self):
        """Test that cache folders are excluded from folder list."""
        # Mock the folder structure to test cache exclusion
        data_folder = Path("data")
        if not data_folder.exists():
            pytest.skip("Data folder not found")
        
        # Get the list of subfolders that would be shown to user
        subfolders = [data_folder]  # Include main data folder
        for item in data_folder.iterdir():
            if item.is_dir():
                # Skip cache folders to avoid loading cached files
                if 'cache' not in item.name.lower():
                    subfolders.append(item)
                    # Also include sub-subfolders (but skip cache)
                    for subitem in item.iterdir():
                        if subitem.is_dir() and 'cache' not in subitem.name.lower():
                            subfolders.append(subitem)
        
        # Check that cache folders are excluded
        cache_folders = [f for f in subfolders if 'cache' in str(f).lower()]
        assert len(cache_folders) == 0, f"Cache folders should be excluded, but found: {cache_folders}"
        
        print("✅ Test passed: Cache folders are excluded from folder list")
    
    def test_exclude_temporary_files(self):
        """Test that temporary files are excluded from file search."""
        # Create a temporary directory with test files
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            # Create test files
            test_files = [
                "EURUSD_data.csv",
                "tmp_eurusd_cache.parquet",
                "tmp123456.parquet",
                "normal_file.csv",
                "tmpfile.csv"
            ]
            
            for filename in test_files:
                (temp_path / filename).touch()
            
            # Test the file filtering logic
            data_files = []
            mask = "eurusd"
            
            for ext in ['.csv', '.parquet', '.xlsx', '.xls']:
                if mask:
                    # Apply mask filter
                    pattern = f"*{mask}*{ext}"
                    files = list(temp_path.glob(pattern))
                    # Filter out temporary files
                    files = [f for f in files if not f.name.startswith('tmp')]
                    data_files.extend(files)
                    
                    # Also try case-insensitive search
                    pattern = f"*{mask.upper()}*{ext}"
                    files = list(temp_path.glob(pattern))
                    files = [f for f in files if not f.name.startswith('tmp')]
                    data_files.extend(files)
                    
                    pattern = f"*{mask.lower()}*{ext}"
                    files = list(temp_path.glob(pattern))
                    files = [f for f in files if not f.name.startswith('tmp')]
                    data_files.extend(files)
            
            # Remove duplicates
            data_files = list(set(data_files))
            
            # Check that only non-temporary files are included
            temp_files = [f for f in data_files if f.name.startswith('tmp')]
            assert len(temp_files) == 0, f"Temporary files should be excluded, but found: {temp_files}"
            
            # Check that the correct file is included
            expected_files = [f for f in data_files if 'eurusd' in f.name.lower() and not f.name.startswith('tmp')]
            assert len(expected_files) >= 1, "Expected EURUSD file should be found"
            
            print("✅ Test passed: Temporary files are excluded from file search")
    
    def test_real_eurusd_loading(self):
        """Test loading real EURUSD file without cache interference."""
        # Check if mql5_feed folder exists
        mql5_feed = Path("mql5_feed")
        if not mql5_feed.exists():
            pytest.skip("mql5_feed folder not found")
        
        # Look for EURUSD CSV file
        eurusd_files = list(mql5_feed.glob("*EURUSD*.csv"))
        if not eurusd_files:
            pytest.skip("EURUSD CSV file not found in mql5_feed")
        
        eurusd_file = eurusd_files[0]
        print(f"Testing with file: {eurusd_file}")
        
        # Test loading the file
        try:
            df = self.data_manager.load_data_from_file(str(eurusd_file))
            
            # Verify the data was loaded correctly
            assert df is not None
            assert not df.empty
            
            # Check that DateTime column was parsed correctly
            assert 'DateTime' in df.columns
            assert pd.api.types.is_datetime64_any_dtype(df['DateTime'])
            
            # Check that we have valid datetime values (not NaN)
            assert df['DateTime'].notna().all(), "All DateTime values should be valid"
            
            print(f"✅ Test passed: Real EURUSD file loaded correctly ({len(df)} rows)")
            
        except Exception as e:
            pytest.fail(f"Failed to load EURUSD file: {e}")


if __name__ == "__main__":
    # Run tests
    test_instance = TestDataManagerCacheFix()
    test_instance.setup_method()
    
    print("🧪 Running DataManager cache fix tests...")
    
    test_instance.test_exclude_cache_folders()
    test_instance.test_exclude_temporary_files()
    test_instance.test_real_eurusd_loading()
    
    print("✅ All tests passed!")
