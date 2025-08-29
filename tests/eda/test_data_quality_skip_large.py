#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test skipping data quality checks for extremely large datasets

This module tests the logic for skipping data quality checks when datasets are too large.
"""

import pytest
import pandas as pd
import numpy as np
import os
from unittest.mock import patch, MagicMock

from src.eda import data_quality


class TestDataQualitySkipLarge:
    """Test skipping data quality checks for extremely large datasets."""
    
    def setup_method(self):
        """Set up test environment."""
        # Set environment variables for testing
        os.environ['MAX_MEMORY_MB'] = '1024'
        os.environ['CHUNK_SIZE'] = '10000'
        os.environ['ENABLE_MEMORY_OPTIMIZATION'] = 'true'
    
    def test_skip_nan_check_for_extremely_large_dataset(self):
        """Test that NaN check is skipped for extremely large datasets."""
        # Create an extremely large DataFrame that will trigger skip
        large_df = pd.DataFrame({
            'A': np.random.randn(1000000),  # 1M rows
            'B': np.random.randint(0, 100, 1000000),
            'C': ['test'] * 1000000
        })
        
        nan_summary = []
        
        with patch('builtins.print') as mock_print:
            data_quality.nan_check(large_df, nan_summary, MagicMock(), MagicMock())
            
            # Check that the function runs without errors
            output_calls = [call[0][0] for call in mock_print.call_args_list]
            
            # Should detect extremely large dataset and skip
            assert any("Extremely large dataset detected" in str(call) for call in output_calls)
            assert any("skipping NaN check to prevent memory issues" in str(call) for call in output_calls)
            
            # Should not have processed the data
            assert len(nan_summary) == 0
    
    def test_skip_duplicate_check_for_extremely_large_dataset(self):
        """Test that duplicate check is skipped for extremely large datasets."""
        # Create an extremely large DataFrame that will trigger skip
        large_df = pd.DataFrame({
            'A': np.random.randn(1000000),  # 1M rows
            'B': np.random.randint(0, 100, 1000000),
            'C': ['test'] * 1000000
        })
        
        dupe_summary = []
        
        with patch('builtins.print') as mock_print:
            data_quality.duplicate_check(large_df, dupe_summary, MagicMock(), MagicMock())
            
            # Check that the function runs without errors
            output_calls = [call[0][0] for call in mock_print.call_args_list]
            
            # Should detect extremely large dataset and skip
            assert any("Extremely large dataset detected" in str(call) for call in output_calls)
            assert any("skipping duplicate check to prevent memory issues" in str(call) for call in output_calls)
            
            # Should not have processed the data
            assert len(dupe_summary) == 0
    
    def test_use_sampling_for_very_large_dataset(self):
        """Test that sampling is used for very large datasets."""
        # Create a very large DataFrame that will trigger sampling
        large_df = pd.DataFrame({
            'A': np.random.randn(500000),  # 500k rows
            'B': np.random.randint(0, 100, 500000),
            'C': ['test'] * 500000
        })
        
        # Add some NaN values
        large_df.loc[1000:1100, 'A'] = np.nan
        
        nan_summary = []
        
        with patch('builtins.print') as mock_print:
            data_quality.nan_check(large_df, nan_summary, MagicMock(), MagicMock())
            
            # Check that the function runs without errors
            output_calls = [call[0][0] for call in mock_print.call_args_list]
            
            # Should detect very large dataset and use sampling
            assert any("Very large dataset detected" in str(call) for call in output_calls)
            assert any("sampling approach" in str(call) for call in output_calls)
            
            # Should have processed the data using sampling
            assert isinstance(nan_summary, list)
    
    def test_use_chunked_processing_for_large_dataset(self):
        """Test that chunked processing is used for large datasets."""
        # Create a large DataFrame that will trigger chunked processing
        large_df = pd.DataFrame({
            'A': np.random.randn(100000),  # 100k rows
            'B': np.random.randint(0, 100, 100000),
            'C': ['test'] * 100000
        })
        
        # Add some NaN values
        large_df.loc[1000:1100, 'A'] = np.nan
        
        nan_summary = []
        
        with patch('builtins.print') as mock_print:
            data_quality.nan_check(large_df, nan_summary, MagicMock(), MagicMock())
            
            # Check that the function runs without errors
            output_calls = [call[0][0] for call in mock_print.call_args_list]
            
            # Should detect large dataset and use chunked processing
            assert any("Large dataset detected" in str(call) for call in output_calls)
            assert any("chunked processing" in str(call) for call in output_calls)
            
            # Should have processed the data
            assert isinstance(nan_summary, list)
    
    def test_normal_processing_for_small_dataset(self):
        """Test that normal processing is used for small datasets."""
        # Create a small DataFrame
        small_df = pd.DataFrame({
            'A': np.random.randn(1000),
            'B': np.random.randint(0, 100, 1000),
            'C': ['test'] * 1000
        })
        
        # Add some NaN values
        small_df.loc[100:110, 'A'] = np.nan
        
        nan_summary = []
        
        with patch('builtins.print') as mock_print:
            data_quality.nan_check(small_df, nan_summary, MagicMock(), MagicMock())
            
            # Check that the function runs without errors
            output_calls = [call[0][0] for call in mock_print.call_args_list]
            
            # Should not detect large dataset
            assert not any("Large dataset detected" in str(call) for call in output_calls)
            assert not any("Very large dataset detected" in str(call) for call in output_calls)
            assert not any("Extremely large dataset detected" in str(call) for call in output_calls)
            
            # Should have processed the data normally
            assert isinstance(nan_summary, list)
    
    def test_memory_threshold_calculation(self):
        """Test that memory thresholds are calculated correctly."""
        # Test with different DataFrame sizes
        small_df = pd.DataFrame({'A': np.random.randn(1000)})
        large_df = pd.DataFrame({'A': np.random.randn(100000)})
        very_large_df = pd.DataFrame({'A': np.random.randn(500000)})
        extremely_large_df = pd.DataFrame({'A': np.random.randn(1000000)})
        
        # Calculate memory usage
        small_memory = data_quality._estimate_memory_usage(small_df)
        large_memory = data_quality._estimate_memory_usage(large_df)
        very_large_memory = data_quality._estimate_memory_usage(very_large_df)
        extremely_large_memory = data_quality._estimate_memory_usage(extremely_large_df)
        
        # Verify memory usage increases with DataFrame size
        assert small_memory < large_memory
        assert large_memory < very_large_memory
        assert very_large_memory < extremely_large_memory
        
        # Verify all memory values are positive
        assert small_memory > 0
        assert large_memory > 0
        assert very_large_memory > 0
        assert extremely_large_memory > 0


if __name__ == "__main__":
    pytest.main([__file__])
