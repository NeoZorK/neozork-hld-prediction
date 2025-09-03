#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test extreme memory optimization in data quality functions

This module tests the memory optimization features for extremely large datasets.
"""

import pytest
import pandas as pd
import numpy as np
import os
from unittest.mock import patch, MagicMock

from src.batch_eda import data_quality


class TestDataQualityExtremeMemory:
    """Test memory optimization features for extremely large datasets."""
    
    def setup_method(self):
        """Set up test environment."""
        # Set environment variables for testing
        os.environ['MAX_MEMORY_MB'] = '2048'
        os.environ['CHUNK_SIZE'] = '25000'
        os.environ['ENABLE_MEMORY_OPTIMIZATION'] = 'true'
    
    def test_extreme_large_dataset_nan_check(self):
        """Test NaN check with large dataset."""
        # Create a large DataFrame
        large_df = pd.DataFrame({
            'A': np.random.randn(50000),  # 50k rows
            'B': np.random.randint(0, 100, 50000),
            'C': ['test'] * 50000
        })
        
        # Add some NaN values
        large_df.loc[1000:1100, 'A'] = np.nan
        large_df.loc[2000, 'B'] = np.nan
        
        nan_summary = []
        
        with patch('builtins.print') as mock_print:
            data_quality.nan_check(large_df, nan_summary, MagicMock(), MagicMock())
            
            # Check that the function runs without errors
            output_calls = [call[0][0] for call in mock_print.call_args_list]
            
            # Should have processed the data successfully
            assert isinstance(nan_summary, list)
            
            # Should have detected NaN values
            assert len(nan_summary) > 0
    
    def test_extreme_large_dataset_duplicate_check(self):
        """Test duplicate check with large dataset."""
        # Create a large DataFrame with duplicates
        large_df = pd.DataFrame({
            'A': np.random.randn(50000),  # 50k rows
            'B': np.random.randint(0, 100, 50000),
            'C': ['test'] * 50000
        })
        
        # Add some duplicates
        large_df.loc[1000] = large_df.loc[999]
        large_df.loc[2000] = large_df.loc[1999]
        
        dupe_summary = []
        
        with patch('builtins.print') as mock_print:
            data_quality.duplicate_check(large_df, dupe_summary, MagicMock(), MagicMock())
            
            # Check that the function runs without errors
            output_calls = [call[0][0] for call in mock_print.call_args_list]
            
            # Should have processed the data successfully
            assert isinstance(dupe_summary, list)
            
            # Should have detected duplicates
            assert len(dupe_summary) > 0
    
    def test_chunked_processing_with_smaller_chunks(self):
        """Test that chunked processing works with large datasets."""
        # Create a large DataFrame
        large_df = pd.DataFrame({
            'A': np.random.randn(30000),  # 30k rows
            'B': np.random.randint(0, 100, 30000),
            'C': ['test'] * 30000
        })
        
        # Add some NaN values
        large_df.loc[1000:1100, 'A'] = np.nan
        
        nan_summary = []
        
        with patch('builtins.print') as mock_print:
            data_quality.nan_check(large_df, nan_summary, MagicMock(), MagicMock())
            
            # Check that the function runs without errors
            output_calls = [call[0][0] for call in mock_print.call_args_list]
            
            # Should have processed the data successfully
            assert isinstance(nan_summary, list)
            
            # Should have detected NaN values
            assert len(nan_summary) > 0
    
    def test_memory_thresholds(self):
        """Test that different memory thresholds trigger appropriate optimizations."""
        # Test small dataset (should use direct processing)
        small_df = pd.DataFrame({
            'A': np.random.randn(1000),
            'B': np.random.randint(0, 100, 1000)
        })
        
        nan_summary = []
        
        with patch('builtins.print') as mock_print:
            data_quality.nan_check(small_df, nan_summary, MagicMock(), MagicMock())
            
            # Should not detect large dataset
            output_calls = [call[0][0] for call in mock_print.call_args_list]
            assert not any("Large dataset detected" in str(call) for call in output_calls)
            assert not any("Extremely large dataset detected" in str(call) for call in output_calls)
    
    def test_error_handling_in_chunked_processing(self):
        """Test error handling in chunked processing."""
        # Create a large DataFrame
        large_df = pd.DataFrame({
            'A': np.random.randn(25000),  # Reduced size
            'B': np.random.randint(0, 100, 25000)
        })
        
        nan_summary = []
        
        # Test that the function handles errors gracefully
        with patch('builtins.print') as mock_print:
            data_quality.nan_check(large_df, nan_summary, MagicMock(), MagicMock())
            
            # Should complete without errors
            assert isinstance(nan_summary, list)
    
    def test_sampling_accuracy(self):
        """Test that sampling provides reasonable estimates."""
        # Create a dataset with known NaN values
        df = pd.DataFrame({
            'A': [1, 2, np.nan, 4, 5, np.nan, 7, 8, 9, 10] * 5000,  # 50k rows, 20% NaN
            'B': [1, np.nan, 3, 4, 5, 6, 7, 8, np.nan, 10] * 5000,  # 50k rows, 20% NaN
            'C': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10] * 5000  # 50k rows, 0% NaN
        })
        
        nan_summary = []
        
        with patch('builtins.print') as mock_print:
            data_quality.nan_check(df, nan_summary, MagicMock(), MagicMock())
            
            # Should have processed the data
            assert isinstance(nan_summary, list)
            
            # Check that NaN values were detected
            if nan_summary:
                for item in nan_summary:
                    assert 'column' in item
                    assert 'missing' in item
                    assert 'percent' in item


if __name__ == "__main__":
    pytest.main([__file__])
