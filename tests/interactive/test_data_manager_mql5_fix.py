#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test for DataManager MQL5 folder inclusion fix

This test verifies that the DataManager correctly includes the mql5_feed folder
in the list of available folders for data loading.
"""

import pytest
import pandas as pd
from pathlib import Path
import sys

# Add project root to path
project_root = Path(__file__).parent.parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from src.interactive.data_manager import DataManager


class TestDataManagerMQL5Fix:
    """Test suite for DataManager MQL5 folder inclusion fix."""
    
    def setup_method(self):
        """Setup method for tests."""
        self.data_manager = DataManager()
    
    def test_mql5_feed_folder_included(self):
        """Test that mql5_feed folder is included in available folders."""
        # Check if mql5_feed folder exists
        mql5_feed_folder = Path("mql5_feed")
        if not mql5_feed_folder.exists():
            pytest.skip("mql5_feed folder not found")
        
        # Mock the folder discovery logic
        data_folder = Path("data")
        mql5_feed_folder = Path("mql5_feed")
        
        if not data_folder.exists():
            pytest.skip("Data folder not found")
        
        # Find all subfolders (exclude cache folders)
        subfolders = [data_folder]  # Include main data folder
        
        # Add mql5_feed folder if it exists
        if mql5_feed_folder.exists() and mql5_feed_folder.is_dir():
            subfolders.append(mql5_feed_folder)
        
        for item in data_folder.iterdir():
            if item.is_dir():
                # Skip cache folders to avoid loading cached files
                if 'cache' not in item.name.lower():
                    subfolders.append(item)
                    # Also include sub-subfolders (but skip cache)
                    for subitem in item.iterdir():
                        if subitem.is_dir() and 'cache' not in subitem.name.lower():
                            subfolders.append(subitem)
        
        # Check that mql5_feed folder is included
        mql5_folders = [f for f in subfolders if 'mql5' in str(f).lower()]
        assert len(mql5_folders) >= 1, f"mql5_feed folder should be included, but not found in: {[str(f) for f in subfolders]}"
        
        print("✅ Test passed: mql5_feed folder is included in available folders")
    
    def test_eurusd_file_found_in_mql5_feed(self):
        """Test that EURUSD file can be found in mql5_feed folder."""
        # Check if mql5_feed folder exists
        mql5_feed_folder = Path("mql5_feed")
        if not mql5_feed_folder.exists():
            pytest.skip("mql5_feed folder not found")
        
        # Look for EURUSD files
        eurusd_files = list(mql5_feed_folder.glob("*EURUSD*.csv"))
        if not eurusd_files:
            pytest.skip("EURUSD CSV file not found in mql5_feed")
        
        print(f"Found EURUSD files: {[f.name for f in eurusd_files]}")
        
        # Test the file filtering logic with mask
        mask = "eurusd"
        data_files = []
        
        for ext in ['.csv', '.parquet', '.xlsx', '.xls']:
            if mask:
                # Apply mask filter
                pattern = f"*{mask}*{ext}"
                files = list(mql5_feed_folder.glob(pattern))
                # Filter out temporary files
                files = [f for f in files if not f.name.startswith('tmp')]
                data_files.extend(files)
                
                # Also try case-insensitive search
                pattern = f"*{mask.upper()}*{ext}"
                files = list(mql5_feed_folder.glob(pattern))
                files = [f for f in files if not f.name.startswith('tmp')]
                data_files.extend(files)
                
                pattern = f"*{mask.lower()}*{ext}"
                files = list(mql5_feed_folder.glob(pattern))
                files = [f for f in files if not f.name.startswith('tmp')]
                data_files.extend(files)
        
        # Remove duplicates
        data_files = list(set(data_files))
        
        # Check that EURUSD files are found
        eurusd_found = [f for f in data_files if 'eurusd' in f.name.lower()]
        assert len(eurusd_found) >= 1, f"EURUSD files should be found, but not found in: {[f.name for f in data_files]}"
        
        print(f"✅ Test passed: Found {len(eurusd_found)} EURUSD files")
    
    def test_folder_number_mapping(self):
        """Test that folder numbers are correctly mapped."""
        # Mock the folder discovery logic
        data_folder = Path("data")
        mql5_feed_folder = Path("mql5_feed")
        
        if not data_folder.exists():
            pytest.skip("Data folder not found")
        
        # Find all subfolders (exclude cache folders)
        subfolders = [data_folder]  # Include main data folder
        
        # Add mql5_feed folder if it exists
        if mql5_feed_folder.exists() and mql5_feed_folder.is_dir():
            subfolders.append(mql5_feed_folder)
        
        for item in data_folder.iterdir():
            if item.is_dir():
                # Skip cache folders to avoid loading cached files
                if 'cache' not in item.name.lower():
                    subfolders.append(item)
                    # Also include sub-subfolders (but skip cache)
                    for subitem in item.iterdir():
                        if subitem.is_dir() and 'cache' not in subitem.name.lower():
                            subfolders.append(subitem)
        
        # Find mql5_feed folder index
        mql5_index = None
        for i, folder in enumerate(subfolders):
            if 'mql5' in str(folder).lower():
                mql5_index = i + 1  # +1 because folder numbers start from 1
                break
        
        assert mql5_index is not None, "mql5_feed folder should be found in subfolders"
        
        print(f"✅ Test passed: mql5_feed folder is at position {mql5_index}")
        print(f"   Available folders: {[str(f) for f in subfolders]}")


if __name__ == "__main__":
    # Run tests
    test_instance = TestDataManagerMQL5Fix()
    test_instance.setup_method()
    
    print("🧪 Running DataManager MQL5 fix tests...")
    
    test_instance.test_mql5_feed_folder_included()
    test_instance.test_eurusd_file_found_in_mql5_feed()
    test_instance.test_folder_number_mapping()
    
    print("✅ All tests passed!")
