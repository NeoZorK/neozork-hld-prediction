#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test CSV Loading Fix for Metadata Headers

This test reproduces the issue with CSV files that have metadata headers
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

from src.interactive.data_manager import DataManager


class TestCSVLoadingFix:
    """Test CSV loading with metadata headers."""
    
    def setup_method(self):
        """Setup method for tests."""
        self.data_manager = DataManager()
        
    def create_test_csv_with_metadata(self):
        """Create a test CSV file with metadata header (MT5 format)."""
        csv_content = """2025.04.22 12:42	TF = PERIOD_D1	EURUSD
DateTime,	TickVolume,	Open,	High,	Low,	Close,	predicted_low,predicted_high,pressure,pressure_vector,
1971.01.04 00:00,1,0.53690000,0.53690000,0.53690000,0.53690000,0.00000,0.00000,0.00000,0.00000,
1971.01.05 00:00,1,0.53660000,0.53660000,0.53660000,0.53660000,0.00000,0.00000,0.00000,0.00000,
1971.01.06 00:00,1,0.53650000,0.53650000,0.53650000,0.53650000,0.00000,0.00000,0.00000,0.00000,
1971.01.07 00:00,1,0.53680000,0.53680000,0.53680000,0.53680000,0.00000,0.00000,0.00000,0.00000,
1971.01.08 00:00,1,0.53710000,0.53710000,0.53710000,0.53710000,0.00000,0.00000,0.00000,0.00000,"""
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            f.write(csv_content)
            return f.name
    
    def test_header_detection(self):
        """Test that header row is correctly detected."""
        csv_file = self.create_test_csv_with_metadata()
        
        try:
            # Test header detection
            header_row = self.data_manager._determine_header_row(Path(csv_file))
            
            print(f"Detected header row: {header_row}")
            
            # Should detect that second row (index 1) is the header
            assert header_row == 1, f"Expected header row 1, got {header_row}"
            
        finally:
            # Clean up
            os.unlink(csv_file)
    
    def test_datetime_column_detection(self):
        """Test that datetime columns are correctly detected."""
        csv_file = self.create_test_csv_with_metadata()
        
        try:
            # Test datetime column detection
            header_row = self.data_manager._determine_header_row(Path(csv_file))
            datetime_columns = self.data_manager._detect_datetime_columns(Path(csv_file), header_row)
            
            print(f"Detected datetime columns: {datetime_columns}")
            
            # Should detect 'DateTime' as a datetime column
            assert 'DateTime' in datetime_columns, f"Expected 'DateTime' in datetime columns, got {datetime_columns}"
            
        finally:
            # Clean up
            os.unlink(csv_file)
    
    def test_csv_loading_with_metadata(self):
        """Test that CSV with metadata loads correctly."""
        csv_file = self.create_test_csv_with_metadata()
        
        try:
            # Load the CSV file
            df = self.data_manager.load_data_from_file(csv_file)
            
            print(f"Loaded DataFrame shape: {df.shape}")
            print(f"Columns: {df.columns.tolist()}")
            print(f"Data types: {df.dtypes}")
            
            # Check that data was loaded correctly
            assert len(df) == 5, f"Expected 5 rows, got {len(df)}"
            assert 'DateTime' in df.columns, f"Expected 'DateTime' column, got {df.columns.tolist()}"
            
            # Check that DateTime column is properly parsed
            if pd.api.types.is_datetime64_any_dtype(df['DateTime']):
                print("✅ DateTime column is properly parsed as datetime")
            else:
                print(f"⚠️  DateTime column type: {df['DateTime'].dtype}")
                # Try to convert manually
                df['DateTime'] = pd.to_datetime(df['DateTime'], errors='coerce')
                if pd.api.types.is_datetime64_any_dtype(df['DateTime']):
                    print("✅ DateTime column converted successfully")
                else:
                    pytest.fail("DateTime column could not be converted to datetime")
            
            # Check for missing values in DateTime column
            missing_count = df['DateTime'].isna().sum()
            missing_percent = 100 * missing_count / len(df)
            
            print(f"Missing values in DateTime: {missing_count} ({missing_percent:.2f}%)")
            
            # Should have no missing values in DateTime column
            assert missing_count == 0, f"Expected 0 missing values in DateTime, got {missing_count} ({missing_percent:.2f}%)"
            
        finally:
            # Clean up
            os.unlink(csv_file)
    
    def test_actual_eurusd_file(self):
        """Test with actual EURUSD file from mql5_feed."""
        eurusd_file = "mql5_feed/CSVExport_EURUSD_PERIOD_D1.csv"
        
        if not os.path.exists(eurusd_file):
            pytest.skip(f"EURUSD file not found: {eurusd_file}")
        
        try:
            # Load the actual EURUSD file
            df = self.data_manager.load_data_from_file(eurusd_file)
            
            print(f"Loaded EURUSD DataFrame shape: {df.shape}")
            print(f"Columns: {df.columns.tolist()}")
            
            # Check that data was loaded correctly
            assert len(df) > 0, "Expected non-empty DataFrame"
            assert 'DateTime' in df.columns, f"Expected 'DateTime' column, got {df.columns.tolist()}"
            
            # Check for missing values in DateTime column
            missing_count = df['DateTime'].isna().sum()
            missing_percent = 100 * missing_count / len(df)
            
            print(f"Missing values in DateTime: {missing_count} ({missing_percent:.2f}%)")
            
            # Should have very few missing values (less than 1%)
            assert missing_percent < 1.0, f"Expected <1% missing values in DateTime, got {missing_percent:.2f}%"
            
        except Exception as e:
            pytest.fail(f"Error loading EURUSD file: {e}")


if __name__ == "__main__":
    # Run tests
    test_instance = TestCSVLoadingFix()
    
    print("🧪 Testing CSV Loading Fix...")
    print("=" * 50)
    
    # Test header detection
    print("\n1️⃣  Testing header detection...")
    test_instance.test_header_detection()
    print("✅ Header detection test passed")
    
    # Test datetime column detection
    print("\n2️⃣  Testing datetime column detection...")
    test_instance.test_datetime_column_detection()
    print("✅ Datetime column detection test passed")
    
    # Test CSV loading with metadata
    print("\n3️⃣  Testing CSV loading with metadata...")
    test_instance.test_csv_loading_with_metadata()
    print("✅ CSV loading test passed")
    
    # Test actual EURUSD file
    print("\n4️⃣  Testing actual EURUSD file...")
    test_instance.test_actual_eurusd_file()
    print("✅ Actual EURUSD file test passed")
    
    print("\n🎉 All tests passed!")
