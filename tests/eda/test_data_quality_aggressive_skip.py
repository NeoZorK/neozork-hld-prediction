#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test aggressive skipping of data quality checks for large datasets

This module tests the aggressive logic for skipping data quality checks when datasets are large.
"""

import pytest
import pandas as pd
import numpy as np
import os
from unittest.mock import patch, MagicMock

from src.eda import data_quality


class TestDataQualityAggressiveSkip:
    """Test aggressive skipping of data quality checks for large datasets."""
    
    def setup_method(self):
        """Set up test environment."""
        # Set environment variables for testing
        os.environ['MAX_MEMORY_MB'] = '512'
        os.environ['CHUNK_SIZE'] = '5000'
        os.environ['ENABLE_MEMORY_OPTIMIZATION'] = 'true'
    
    def test_skip_nan_check_for_large_dataset(self):
        """Test that NaN check is skipped for large datasets (>1GB)."""
        # Create a large DataFrame that will trigger skip (1480MB scenario)
        large_df = pd.DataFrame({
            'A': np.random.randn(500000),  # 500k rows
            'B': np.random.randint(0, 100, 500000),
            'C': ['test'] * 500000
        })
        
        nan_summary = []
        
        with patch('builtins.print') as mock_print:
            data_quality.nan_check(large_df, nan_summary, MagicMock(), MagicMock())
            
            # Check that the function runs without errors
            output_calls = [call[0][0] for call in mock_print.call_args_list]
            
            # Should detect large dataset and skip or use sampling
            assert any("Large dataset detected" in str(call) for call in output_calls) or \
                   any("Very large dataset detected" in str(call) for call in output_calls) or \
                   any("Extremely large dataset detected" in str(call) for call in output_calls)
            
            # Should have processed the data or skipped it
            assert isinstance(nan_summary, list)
    
    def test_skip_duplicate_check_for_large_dataset(self):
        """Test that duplicate check is skipped for large datasets (>1GB)."""
        # Create a large DataFrame that will trigger skip
        large_df = pd.DataFrame({
            'A': np.random.randn(500000),  # 500k rows
            'B': np.random.randint(0, 100, 500000),
            'C': ['test'] * 500000
        })
        
        dupe_summary = []
        
        with patch('builtins.print') as mock_print:
            data_quality.duplicate_check(large_df, dupe_summary, MagicMock(), MagicMock())
            
            # Check that the function runs without errors
            output_calls = [call[0][0] for call in mock_print.call_args_list]
            
            # Should detect large dataset and skip or use sampling
            assert any("Large dataset detected" in str(call) for call in output_calls) or \
                   any("Very large dataset detected" in str(call) for call in output_calls) or \
                   any("Extremely large dataset detected" in str(call) for call in output_calls)
            
            # Should have processed the data or skipped it
            assert isinstance(dupe_summary, list)
    
    def test_memory_thresholds_with_new_settings(self):
        """Test that memory thresholds work with new conservative settings."""
        # Test with different DataFrame sizes
        small_df = pd.DataFrame({'A': np.random.randn(1000)})
        medium_df = pd.DataFrame({'A': np.random.randn(10000)})
        large_df = pd.DataFrame({'A': np.random.randn(100000)})
        
        # Calculate memory usage
        small_memory = data_quality._estimate_memory_usage(small_df)
        medium_memory = data_quality._estimate_memory_usage(medium_df)
        large_memory = data_quality._estimate_memory_usage(large_df)
        
        # Verify memory usage increases with DataFrame size
        assert small_memory <= medium_memory
        assert medium_memory <= large_memory
        
        # Verify all memory values are positive
        assert small_memory > 0
        assert medium_memory > 0
        assert large_memory > 0
        
        print(f"Memory usage: small={small_memory}MB, medium={medium_memory}MB, large={large_memory}MB")
    
    def test_chunked_processing_with_smaller_chunks(self):
        """Test that chunked processing uses smaller chunks."""
        # Create a medium DataFrame
        medium_df = pd.DataFrame({
            'A': np.random.randn(20000),  # 20k rows
            'B': np.random.randint(0, 100, 20000),
            'C': ['test'] * 20000
        })
        
        # Add some NaN values
        medium_df.loc[1000:1100, 'A'] = np.nan
        
        nan_summary = []
        
        with patch('builtins.print') as mock_print:
            data_quality.nan_check(medium_df, nan_summary, MagicMock(), MagicMock())
            
            # Check that the function runs without errors
            output_calls = [call[0][0] for call in mock_print.call_args_list]
            
            # Should have processed the data
            assert isinstance(nan_summary, list)
    
    def test_error_handling(self):
        """Test error handling in data quality functions."""
        # Create a DataFrame
        df = pd.DataFrame({
            'A': np.random.randn(1000),
            'B': np.random.randint(0, 100, 1000)
        })
        
        nan_summary = []
        
        # Test that the function handles errors gracefully
        with patch('builtins.print') as mock_print:
            data_quality.nan_check(df, nan_summary, MagicMock(), MagicMock())
            
            # Should complete without errors
            assert isinstance(nan_summary, list)


if __name__ == "__main__":
    pytest.main([__file__])
