#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test chunked processing of large datasets in data quality functions

This module tests the logic for processing large datasets using chunked approach.
"""

import pytest
import pandas as pd
import numpy as np
import os
from unittest.mock import patch, MagicMock

from src.eda import data_quality


class TestDataQualityChunkedProcessing:
    """Test chunked processing of large datasets in data quality functions."""
    
    def setup_method(self):
        """Set up test environment."""
        # Set environment variables for testing
        os.environ['MAX_MEMORY_MB'] = '1024'
        os.environ['CHUNK_SIZE'] = '10000'
        os.environ['ENABLE_MEMORY_OPTIMIZATION'] = 'true'
    
    def test_chunked_processing_for_large_dataset(self):
        """Test that large datasets are processed using chunked approach."""
        # Create a large DataFrame that will trigger chunked processing
        large_df = pd.DataFrame({
            'A': np.random.randn(100000),  # 100k rows
            'B': np.random.randint(0, 100, 100000),
            'C': ['test'] * 100000
        })
        
        # Add some NaN values
        large_df.loc[1000:1100, 'A'] = np.nan
        large_df.loc[2000, 'B'] = np.nan
        
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
            assert len(nan_summary) > 0
    
    def test_sampling_for_very_large_dataset(self):
        """Test that very large datasets use sampling approach."""
        # Create a very large DataFrame that will trigger sampling
        very_large_df = pd.DataFrame({
            'A': np.random.randn(500000),  # 500k rows
            'B': np.random.randint(0, 100, 500000),
            'C': ['test'] * 500000
        })
        
        # Add some NaN values
        very_large_df.loc[1000:1100, 'A'] = np.nan
        
        nan_summary = []
        
        with patch('builtins.print') as mock_print:
            data_quality.nan_check(very_large_df, nan_summary, MagicMock(), MagicMock())
            
            # Check that the function runs without errors
            output_calls = [call[0][0] for call in mock_print.call_args_list]
            
            # Should detect very large dataset and use sampling
            assert any("Very large dataset detected" in str(call) for call in output_calls)
            assert any("sampling approach" in str(call) for call in output_calls)
            
            # Should have processed the data using sampling
            assert isinstance(nan_summary, list)
    
    def test_progress_indicator_for_large_datasets(self):
        """Test that progress is shown for very large datasets."""
        # Create a very large DataFrame
        very_large_df = pd.DataFrame({
            'A': np.random.randn(200000),  # 200k rows
            'B': np.random.randint(0, 100, 200000),
            'C': ['test'] * 200000
        })
        
        nan_summary = []
        
        with patch('builtins.print') as mock_print:
            data_quality.nan_check(very_large_df, nan_summary, MagicMock(), MagicMock())
            
            # Check that the function runs without errors
            output_calls = [call[0][0] for call in mock_print.call_args_list]
            
            # Should show progress for large datasets
            assert any("Processing" in str(call) for call in output_calls) or \
                   any("Progress" in str(call) for call in output_calls)
            
            # Should have processed the data
            assert isinstance(nan_summary, list)
    
    def test_duplicate_check_chunked_processing(self):
        """Test that duplicate check uses chunked processing for large datasets."""
        # Create a large DataFrame with duplicates
        large_df = pd.DataFrame({
            'A': np.random.randn(100000),  # 100k rows
            'B': np.random.randint(0, 100, 100000),
            'C': ['test'] * 100000
        })
        
        # Add some duplicates
        large_df.loc[1000] = large_df.loc[999]
        large_df.loc[2000] = large_df.loc[1999]
        
        dupe_summary = []
        
        with patch('builtins.print') as mock_print:
            data_quality.duplicate_check(large_df, dupe_summary, MagicMock(), MagicMock())
            
            # Check that the function runs without errors
            output_calls = [call[0][0] for call in mock_print.call_args_list]
            
            # Should detect large dataset and use optimized duplicate detection
            assert any("Large dataset detected" in str(call) for call in output_calls)
            assert any("optimized duplicate detection" in str(call) for call in output_calls)
            
            # Should have processed the data
            assert isinstance(dupe_summary, list)
    
    def test_memory_thresholds_with_new_settings(self):
        """Test that memory thresholds work with new settings."""
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
    
    def test_error_handling_in_chunked_processing(self):
        """Test error handling in chunked processing."""
        # Create a large DataFrame
        large_df = pd.DataFrame({
            'A': np.random.randn(50000),  # 50k rows
            'B': np.random.randint(0, 100, 50000),
            'C': ['test'] * 50000
        })
        
        nan_summary = []
        
        # Test that the function handles errors gracefully
        with patch('builtins.print') as mock_print:
            data_quality.nan_check(large_df, nan_summary, MagicMock(), MagicMock())
            
            # Should complete without errors
            assert isinstance(nan_summary, list)
    
    def test_no_skipping_of_large_datasets(self):
        """Test that large datasets are not skipped but processed."""
        # Create a very large DataFrame
        very_large_df = pd.DataFrame({
            'A': np.random.randn(1000000),  # 1M rows
            'B': np.random.randint(0, 100, 1000000),
            'C': ['test'] * 1000000
        })
        
        nan_summary = []
        
        with patch('builtins.print') as mock_print:
            data_quality.nan_check(very_large_df, nan_summary, MagicMock(), MagicMock())
            
            # Check that the function runs without errors
            output_calls = [call[0][0] for call in mock_print.call_args_list]
            
            # Should not skip the dataset
            assert not any("skipping" in str(call).lower() for call in output_calls)
            
            # Should process the dataset using sampling or chunked processing
            assert any("sampling" in str(call).lower() for call in output_calls) or \
                   any("chunked" in str(call).lower() for call in output_calls)
            
            # Should have processed the data
            assert isinstance(nan_summary, list)


if __name__ == "__main__":
    pytest.main([__file__])
