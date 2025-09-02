#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test for DataManager CSV loading fix

This test verifies that the DataManager correctly handles CSV files
with metadata headers (like MT5 exports) by detecting and skipping
the metadata row.
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


class TestDataManagerCSVFix:
    """Test suite for DataManager CSV loading fix."""
    
    def setup_method(self):
        """Setup method for tests."""
        self.data_manager = DataManager()
    
    def test_load_csv_with_metadata_header(self):
        """Test loading CSV file with metadata header (MT5 format)."""
        # Create a temporary CSV file with MT5 format
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            # Create MT5 format CSV data with metadata header
            csv_content = """2025.04.22 12:42	TF = PERIOD_D1	EURUSD
DateTime,	TickVolume,	Open,	High,	Low,	Close,	predicted_low,predicted_high,pressure,pressure_vector,
1971.01.04 00:00,1,0.53690000,0.53690000,0.53690000,0.53690000,0.00000,0.00000,0.00000,0.00000,
1971.01.05 00:00,1,0.53660000,0.53660000,0.53660000,0.53660000,0.00000,0.00000,0.00000,0.00000,
1971.01.06 00:00,1,0.53650000,0.53650000,0.53650000,0.53650000,0.00000,0.00000,0.00000,0.00000,"""
            
            f.write(csv_content)
            csv_file = f.name
        
        try:
            # Test loading the CSV file
            df = self.data_manager.load_data_from_file(csv_file)
            
            # Verify the data was loaded correctly
            assert df is not None
            assert not df.empty
            assert len(df) == 3  # Should have 3 data rows
            
            # Check that DateTime column was parsed correctly
            assert 'DateTime' in df.columns
            assert pd.api.types.is_datetime64_any_dtype(df['DateTime'])
            
            # Check that we have valid datetime values (not NaN)
            assert df['DateTime'].notna().all(), "All DateTime values should be valid"
            
            # Check that the first row is from 1971-01-04
            first_date = df['DateTime'].iloc[0]
            assert first_date.year == 1971
            assert first_date.month == 1
            assert first_date.day == 4
            
            print("✅ Test passed: CSV with metadata header loaded correctly")
            
        finally:
            # Clean up
            Path(csv_file).unlink(missing_ok=True)
    
    def test_load_csv_without_metadata_header(self):
        """Test loading CSV file without metadata header (standard format)."""
        # Create a temporary CSV file without metadata header
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            # Create standard CSV data without metadata header
            csv_content = """DateTime,Open,High,Low,Close,Volume
2023-01-01 00:00,100.0,105.0,95.0,103.0,1000
2023-01-02 00:00,101.0,106.0,96.0,104.0,1100
2023-01-03 00:00,102.0,107.0,97.0,105.0,1200"""
            
            f.write(csv_content)
            csv_file = f.name
        
        try:
            # Test loading the CSV file
            df = self.data_manager.load_data_from_file(csv_file)
            
            # Verify the data was loaded correctly
            assert df is not None
            assert not df.empty
            assert len(df) == 3  # Should have 3 data rows
            
            # Check that DateTime column was parsed correctly
            assert 'DateTime' in df.columns
            assert pd.api.types.is_datetime64_any_dtype(df['DateTime'])
            
            # Check that we have valid datetime values (not NaN)
            assert df['DateTime'].notna().all(), "All DateTime values should be valid"
            
            print("✅ Test passed: Standard CSV without metadata header loaded correctly")
            
        finally:
            # Clean up
            Path(csv_file).unlink(missing_ok=True)
    
    def test_load_csv_no_header(self):
        """Test loading CSV file without any header (data starts immediately)."""
        # Create a temporary CSV file without header
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            # Create CSV data without header
            csv_content = """2023-01-01 00:00,100.0,105.0,95.0,103.0,1000
2023-01-02 00:00,101.0,106.0,96.0,104.0,1100
2023-01-03 00:00,102.0,107.0,97.0,105.0,1200"""
            
            f.write(csv_content)
            csv_file = f.name
        
        try:
            # Test loading the CSV file
            df = self.data_manager.load_data_from_file(csv_file)
            
            # Verify the data was loaded correctly
            assert df is not None
            assert not df.empty
            assert len(df) == 3  # Should have 3 data rows
            
            print("✅ Test passed: CSV without header loaded correctly")
            
        finally:
            # Clean up
            Path(csv_file).unlink(missing_ok=True)


if __name__ == "__main__":
    # Run tests
    test_instance = TestDataManagerCSVFix()
    test_instance.setup_method()
    
    print("🧪 Running DataManager CSV fix tests...")
    
    test_instance.test_load_csv_with_metadata_header()
    test_instance.test_load_csv_without_metadata_header()
    test_instance.test_load_csv_no_header()
    
    print("✅ All tests passed!")
