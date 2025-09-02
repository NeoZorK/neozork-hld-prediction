#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test for DataManager unnamed columns fix

This test verifies that the DataManager correctly removes unnamed columns
from CSV files during loading.
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


class TestDataManagerUnnamedFix:
    """Test suite for DataManager unnamed columns fix."""
    
    def setup_method(self):
        """Setup method for tests."""
        self.data_manager = DataManager()
    
    def test_remove_unnamed_columns(self):
        """Test that unnamed columns are removed during CSV loading."""
        # Create a temporary CSV file with unnamed columns
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            # Create CSV data with unnamed columns (extra commas create unnamed columns)
            csv_content = """DateTime,Open,High,Low,Close,Volume,,
1971-01-04 00:00,0.5369,0.5369,0.5369,0.5369,1,
1971-01-05 00:00,0.5366,0.5366,0.5366,0.5366,1,
1971-01-06 00:00,0.5365,0.5365,0.5365,0.5365,1,"""
            
            f.write(csv_content)
            csv_file = f.name
        
        try:
            # Test loading the CSV file
            df = self.data_manager.load_data_from_file(csv_file)
            
            # Verify that unnamed columns were removed
            unnamed_cols = [col for col in df.columns if col.startswith('Unnamed:')]
            assert len(unnamed_cols) == 0, f"Unnamed columns should be removed, but found: {unnamed_cols}"
            
            # Verify that valid columns remain
            expected_cols = ['DateTime', 'Open', 'High', 'Low', 'Close', 'Volume']
            for col in expected_cols:
                assert col in df.columns, f"Expected column '{col}' not found in DataFrame"
            
            print("✅ Test passed: Unnamed columns were removed correctly")
            
        finally:
            # Clean up
            Path(csv_file).unlink(missing_ok=True)
    
    def test_remove_empty_columns(self):
        """Test that empty columns are removed during CSV loading."""
        # Create a temporary CSV file with empty columns
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            # Create CSV data with empty column names
            csv_content = """DateTime,Open,High,Low,Close,Volume,,
1971-01-04 00:00,0.5369,0.5369,0.5369,0.5369,1,
1971-01-05 00:00,0.5366,0.5366,0.5366,0.5366,1,
1971-01-06 00:00,0.5365,0.5365,0.5365,0.5365,1,"""
            
            f.write(csv_content)
            csv_file = f.name
        
        try:
            # Test loading the CSV file
            df = self.data_manager.load_data_from_file(csv_file)
            
            # Verify that empty columns were removed
            empty_cols = [col for col in df.columns if col == '']
            assert len(empty_cols) == 0, f"Empty columns should be removed, but found: {empty_cols}"
            
            print("✅ Test passed: Empty columns were removed correctly")
            
        finally:
            # Clean up
            Path(csv_file).unlink(missing_ok=True)
    
    def test_preserve_valid_columns(self):
        """Test that valid columns are preserved when removing unnamed columns."""
        # Create a temporary CSV file with mixed valid and unnamed columns
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            # Create CSV data with valid and unnamed columns
            csv_content = """DateTime,Open,High,Low,Close,Volume,Unnamed: 10,predicted_low,predicted_high,pressure,pressure_vector,
1971-01-04 00:00,0.5369,0.5369,0.5369,0.5369,1,,0.61568,0.61591,4.1,4.1,
1971-01-05 00:00,0.5366,0.5366,0.5366,0.5366,1,,0.61568,0.61591,4.1,4.1,
1971-01-06 00:00,0.5365,0.5365,0.5365,0.5365,1,,0.61568,0.61591,4.1,4.1,"""
            
            f.write(csv_content)
            csv_file = f.name
        
        try:
            # Test loading the CSV file
            df = self.data_manager.load_data_from_file(csv_file)
            
            # Verify that valid columns are preserved
            expected_valid_cols = ['DateTime', 'Open', 'High', 'Low', 'Close', 'Volume', 
                                 'predicted_low', 'predicted_high', 'pressure', 'pressure_vector']
            for col in expected_valid_cols:
                assert col in df.columns, f"Valid column '{col}' should be preserved"
            
            # Verify that unnamed columns are removed
            unnamed_cols = [col for col in df.columns if col.startswith('Unnamed:')]
            assert len(unnamed_cols) == 0, f"Unnamed columns should be removed, but found: {unnamed_cols}"
            
            print("✅ Test passed: Valid columns preserved while removing unnamed columns")
            
        finally:
            # Clean up
            Path(csv_file).unlink(missing_ok=True)
    
    def test_real_eurusd_loading_with_unnamed_fix(self):
        """Test loading real EURUSD file to ensure unnamed columns are handled."""
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
            
            # Verify that no unnamed columns exist
            unnamed_cols = [col for col in df.columns if col.startswith('Unnamed:')]
            assert len(unnamed_cols) == 0, f"Unnamed columns should be removed, but found: {unnamed_cols}"
            
            # Verify that valid columns exist (with tab prefix as in real file)
            expected_cols = ['DateTime', '\tOpen', '\tHigh', '\tLow', '\tClose']
            for col in expected_cols:
                assert col in df.columns, f"Expected column '{col}' not found"
            
            print(f"✅ Test passed: Real EURUSD file loaded without unnamed columns ({len(df)} rows)")
            
        except Exception as e:
            pytest.fail(f"Failed to load EURUSD file: {e}")


if __name__ == "__main__":
    # Run tests
    test_instance = TestDataManagerUnnamedFix()
    test_instance.setup_method()
    
    print("🧪 Running DataManager unnamed columns fix tests...")
    
    test_instance.test_remove_unnamed_columns()
    test_instance.test_remove_empty_columns()
    test_instance.test_preserve_valid_columns()
    test_instance.test_real_eurusd_loading_with_unnamed_fix()
    
    print("✅ All tests passed!")
