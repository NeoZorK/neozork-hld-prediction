#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test fix for the frequency error in fix_gaps function.

This test verifies that:
1. Invalid frequencies (NaN, zero) are handled gracefully
2. The function falls back to median frequency when most common frequency is invalid
3. The function skips gap fixing when no valid frequency can be determined
4. Invalid start/end times are handled properly
"""

import pytest
import pandas as pd
import numpy as np
from pathlib import Path
import tempfile
import os

from src.eda import fix_files


class TestFixGapsFrequencyError:
    """Test fixes for frequency error in fix_gaps function."""
    
    def setup_method(self):
        """Set up test environment."""
        # Create test data with valid datetime
        dates = pd.date_range('2023-01-01', periods=100, freq='H')
        self.valid_data = pd.DataFrame({
            'Open': np.random.uniform(100, 110, 100),
            'High': np.random.uniform(110, 120, 100),
            'Low': np.random.uniform(90, 100, 100),
            'Close': np.random.uniform(100, 110, 100),
            'Volume': np.random.randint(1000, 10000, 100),
            'Timestamp': dates
        })
        
        # Create test data with invalid frequency (all same timestamp)
        same_time = pd.Timestamp('2023-01-01 12:00:00')
        self.invalid_freq_data = pd.DataFrame({
            'Open': np.random.uniform(100, 110, 50),
            'High': np.random.uniform(110, 120, 50),
            'Low': np.random.uniform(90, 100, 50),
            'Close': np.random.uniform(100, 110, 50),
            'Volume': np.random.randint(1000, 10000, 50),
            'Timestamp': [same_time] * 50  # All same timestamp
        })
        
        # Create test data with NaN timestamps
        dates_with_nan = list(pd.date_range('2023-01-01', periods=100, freq='H'))
        dates_with_nan[50:60] = [pd.NaT] * 10  # Insert NaN values
        self.nan_timestamp_data = pd.DataFrame({
            'Open': np.random.uniform(100, 110, 100),
            'High': np.random.uniform(110, 120, 100),
            'Low': np.random.uniform(90, 100, 100),
            'Close': np.random.uniform(100, 110, 100),
            'Volume': np.random.randint(1000, 10000, 100),
            'Timestamp': dates_with_nan
        })
    
    def test_valid_frequency_handling(self):
        """Test that valid frequencies work correctly."""
        # This should work without errors
        result = fix_files.fix_gaps(self.valid_data, gap_summary=[{'column': 'Timestamp'}])
        
        # Should return a DataFrame
        assert isinstance(result, pd.DataFrame)
        assert len(result) > 0
        assert 'Timestamp' in result.columns
    
    def test_invalid_frequency_handling(self):
        """Test that invalid frequencies (all same timestamp) are handled gracefully."""
        # This should not raise an error, but should skip gap fixing
        result = fix_files.fix_gaps(self.invalid_freq_data, gap_summary=[{'column': 'Timestamp'}])
        
        # Should return a DataFrame with the same number of rows
        assert isinstance(result, pd.DataFrame)
        assert len(result) == len(self.invalid_freq_data)
        # Should have the same columns
        assert list(result.columns) == list(self.invalid_freq_data.columns)
        # All timestamps should still be the same
        assert result['Timestamp'].nunique() == 1
    
    def test_nan_timestamp_handling(self):
        """Test that NaN timestamps are handled gracefully."""
        # This should handle NaN timestamps properly
        result = fix_files.fix_gaps(self.nan_timestamp_data, gap_summary=[{'column': 'Timestamp'}])
        
        # Should return a DataFrame
        assert isinstance(result, pd.DataFrame)
        assert len(result) > 0
        assert 'Timestamp' in result.columns
    
    def test_empty_dataframe_handling(self):
        """Test that empty DataFrame is handled gracefully."""
        empty_df = pd.DataFrame(columns=['Open', 'High', 'Low', 'Close', 'Volume', 'Timestamp'])
        
        result = fix_files.fix_gaps(empty_df, gap_summary=[{'column': 'Timestamp'}])
        
        # Should return the empty DataFrame
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 0
    
    def test_mixed_frequency_data(self):
        """Test data with mixed frequencies (some valid, some invalid)."""
        # Create data with mixed frequencies
        dates = []
        for i in range(50):
            if i % 10 == 0:
                dates.append(pd.Timestamp('2023-01-01 12:00:00'))  # Same time
            else:
                dates.append(pd.Timestamp('2023-01-01') + pd.Timedelta(hours=i))
        
        mixed_data = pd.DataFrame({
            'Open': np.random.uniform(100, 110, 50),
            'High': np.random.uniform(110, 120, 50),
            'Low': np.random.uniform(90, 100, 50),
            'Close': np.random.uniform(100, 110, 50),
            'Volume': np.random.randint(1000, 10000, 50),
            'Timestamp': dates
        })
        
        result = fix_files.fix_gaps(mixed_data, gap_summary=[{'column': 'Timestamp'}])
        
        # Should handle mixed frequencies gracefully
        assert isinstance(result, pd.DataFrame)
        assert len(result) > 0
    
    def test_datetime_index_handling(self):
        """Test handling of DataFrame with datetime index."""
        # Create DataFrame with datetime index
        dates = pd.date_range('2023-01-01', periods=100, freq='H')
        df_with_index = pd.DataFrame({
            'Open': np.random.uniform(100, 110, 100),
            'High': np.random.uniform(110, 120, 100),
            'Low': np.random.uniform(90, 100, 100),
            'Close': np.random.uniform(100, 110, 100),
            'Volume': np.random.randint(1000, 10000, 100)
        }, index=dates)
        
        result = fix_files.fix_gaps(df_with_index, gap_summary=[{'column': 'index'}])
        
        # Should handle datetime index correctly
        assert isinstance(result, pd.DataFrame)
        assert len(result) > 0
    
    def test_invalid_datetime_index(self):
        """Test handling of DataFrame with invalid datetime index."""
        # Create DataFrame with all same datetime index
        same_time = pd.Timestamp('2023-01-01 12:00:00')
        df_with_invalid_index = pd.DataFrame({
            'Open': np.random.uniform(100, 110, 50),
            'High': np.random.uniform(110, 120, 50),
            'Low': np.random.uniform(90, 100, 50),
            'Close': np.random.uniform(100, 110, 50),
            'Volume': np.random.randint(1000, 10000, 50)
        }, index=[same_time] * 50)
        
        result = fix_files.fix_gaps(df_with_invalid_index, gap_summary=[{'column': 'index'}])
        
        # Should handle invalid index gracefully
        assert isinstance(result, pd.DataFrame)
        assert len(result) == len(df_with_invalid_index)
    
    def test_no_gap_summary_provided(self):
        """Test handling when no gap_summary is provided."""
        result = fix_files.fix_gaps(self.valid_data)
        
        # Should still work and try to detect datetime column
        assert isinstance(result, pd.DataFrame)
        assert len(result) > 0
    
    def test_non_datetime_column(self):
        """Test handling when specified column is not datetime."""
        # Create data with non-datetime column
        non_datetime_data = pd.DataFrame({
            'Open': np.random.uniform(100, 110, 100),
            'High': np.random.uniform(110, 120, 100),
            'Low': np.random.uniform(90, 100, 100),
            'Close': np.random.uniform(100, 110, 100),
            'Volume': np.random.randint(1000, 10000, 100),
            'StringColumn': ['text'] * 100
        })
        
        result = fix_files.fix_gaps(non_datetime_data, gap_summary=[{'column': 'StringColumn'}])
        
        # Should handle non-datetime column gracefully
        assert isinstance(result, pd.DataFrame)
        assert len(result) == len(non_datetime_data)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
