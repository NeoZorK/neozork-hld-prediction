#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test for DataManager column name cleaning functionality.

This test verifies that the DataManager correctly cleans column names
by removing tabs (\t) and trailing commas from CSV headers.
"""

import pytest
import pandas as pd
from pathlib import Path
import tempfile
import os

# Add project root to path
import sys
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.interactive.data_manager import DataManager


class TestDataManagerColumnCleaning:
    """Test cases for column name cleaning functionality."""
    
    def setup_method(self):
        """Set up test environment."""
        self.data_manager = DataManager()
        
    def test_clean_column_names_with_tabs(self):
        """Test cleaning column names that contain tabs."""
        # Create DataFrame with tab-containing column names
        df = pd.DataFrame({
            'DateTime': [1, 2, 3],
            '\tTickVolume': [100, 200, 300],
            '\tOpen': [1.1, 1.2, 1.3],
            '\tHigh': [1.2, 1.3, 1.4],
            '\tLow': [1.0, 1.1, 1.2],
            '\tClose': [1.1, 1.2, 1.3],
            '\tpredicted_low': [1.0, 1.1, 1.2],
            'predicted_high': [1.2, 1.3, 1.4],
            'pressure': [0.1, 0.2, 0.3],
            'pressure_vector': [0.01, 0.02, 0.03]
        })
        
        # Clean column names
        cleaned_df = self.data_manager._clean_column_names(df)
        
        # Verify tabs are removed
        expected_columns = [
            'DateTime', 'TickVolume', 'Open', 'High', 'Low', 'Close',
            'predicted_low', 'predicted_high', 'pressure', 'pressure_vector'
        ]
        
        assert list(cleaned_df.columns) == expected_columns
        assert '\t' not in str(cleaned_df.columns)
        
    def test_clean_column_names_with_trailing_commas(self):
        """Test cleaning column names that contain trailing commas."""
        # Create DataFrame with trailing comma column names
        df = pd.DataFrame({
            'DateTime,': [1, 2, 3],
            'TickVolume,': [100, 200, 300],
            'Open,': [1.1, 1.2, 1.3],
            'High,': [1.2, 1.3, 1.4],
            'Low,': [1.0, 1.1, 1.2],
            'Close,': [1.1, 1.2, 1.3],
            'predicted_low,': [1.0, 1.1, 1.2],
            'predicted_high,': [1.2, 1.3, 1.4],
            'pressure,': [0.1, 0.2, 0.3],
            'pressure_vector,': [0.01, 0.02, 0.03]
        })
        
        # Clean column names
        cleaned_df = self.data_manager._clean_column_names(df)
        
        # Verify trailing commas are removed
        expected_columns = [
            'DateTime', 'TickVolume', 'Open', 'High', 'Low', 'Close',
            'predicted_low', 'predicted_high', 'pressure', 'pressure_vector'
        ]
        
        assert list(cleaned_df.columns) == expected_columns
        assert not any(col.endswith(',') for col in cleaned_df.columns)
        
    def test_clean_column_names_with_both_tabs_and_commas(self):
        """Test cleaning column names that contain both tabs and trailing commas."""
        # Create DataFrame with both tabs and trailing commas
        df = pd.DataFrame({
            'DateTime': [1, 2, 3],
            '\tTickVolume,': [100, 200, 300],
            '\tOpen,': [1.1, 1.2, 1.3],
            '\tHigh,': [1.2, 1.3, 1.4],
            '\tLow,': [1.0, 1.1, 1.2],
            '\tClose,': [1.1, 1.2, 1.3],
            '\tpredicted_low,': [1.0, 1.1, 1.2],
            'predicted_high,': [1.2, 1.3, 1.4],
            'pressure,': [0.1, 0.2, 0.3],
            'pressure_vector,': [0.01, 0.02, 0.03]
        })
        
        # Clean column names
        cleaned_df = self.data_manager._clean_column_names(df)
        
        # Verify both tabs and trailing commas are removed
        expected_columns = [
            'DateTime', 'TickVolume', 'Open', 'High', 'Low', 'Close',
            'predicted_low', 'predicted_high', 'pressure', 'pressure_vector'
        ]
        
        assert list(cleaned_df.columns) == expected_columns
        assert '\t' not in str(cleaned_df.columns)
        assert not any(col.endswith(',') for col in cleaned_df.columns)
        
    def test_clean_column_names_no_changes_needed(self):
        """Test that clean column names doesn't change already clean names."""
        # Create DataFrame with clean column names
        df = pd.DataFrame({
            'DateTime': [1, 2, 3],
            'TickVolume': [100, 200, 300],
            'Open': [1.1, 1.2, 1.3],
            'High': [1.2, 1.3, 1.4],
            'Low': [1.0, 1.1, 1.2],
            'Close': [1.1, 1.2, 1.3]
        })
        
        original_columns = list(df.columns)
        
        # Clean column names
        cleaned_df = self.data_manager._clean_column_names(df)
        
        # Verify no changes were made
        assert list(cleaned_df.columns) == original_columns
        
    def test_clean_column_names_with_extra_spaces(self):
        """Test cleaning column names that contain extra spaces."""
        # Create DataFrame with extra spaces in column names
        df = pd.DataFrame({
            ' DateTime ': [1, 2, 3],
            '  TickVolume  ': [100, 200, 300],
            '  Open  ': [1.1, 1.2, 1.3],
            '  High  ': [1.2, 1.3, 1.4],
            '  Low  ': [1.0, 1.1, 1.2],
            '  Close  ': [1.1, 1.2, 1.3]
        })
        
        # Clean column names
        cleaned_df = self.data_manager._clean_column_names(df)
        
        # Verify extra spaces are removed
        expected_columns = [
            'DateTime', 'TickVolume', 'Open', 'High', 'Low', 'Close'
        ]
        
        assert list(cleaned_df.columns) == expected_columns
        
    def test_csv_loading_with_dirty_headers(self):
        """Test loading CSV file with dirty headers (tabs and commas)."""
        # Create temporary CSV file with dirty headers
        csv_content = """2025.04.22 12:42	TF = PERIOD_D1	EURUSD
DateTime,	TickVolume,	Open,	High,	Low,	Close,	predicted_low,predicted_high,pressure,pressure_vector,
1971.01.04 00:00,1,0.53690000,0.53690000,0.53690000,0.53690000,0.00000,0.00000,0.00000,0.00000,
1971.01.05 00:00,1,0.53660000,0.53660000,0.53660000,0.53660000,0.00000,0.00000,0.00000,0.00000,"""
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            f.write(csv_content)
            temp_file = f.name
        
        try:
            # Load CSV file
            df = self.data_manager._load_csv_direct(Path(temp_file), ['DateTime'])
            
            # Verify column names are cleaned
            expected_columns = [
                'DateTime', 'TickVolume', 'Open', 'High', 'Low', 'Close',
                'predicted_low', 'predicted_high', 'pressure', 'pressure_vector'
            ]
            
            assert list(df.columns) == expected_columns
            assert '\t' not in str(df.columns)
            assert not any(col.endswith(',') for col in df.columns)
            
        finally:
            # Clean up temporary file
            os.unlink(temp_file)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
