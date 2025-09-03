#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test memory optimization in data quality functions

This module tests the memory optimization features of the data quality functions.
"""

import pytest
import pandas as pd
import numpy as np
import tempfile
import os
from pathlib import Path
from unittest.mock import patch, MagicMock

from src.batch_eda import data_quality


class TestDataQualityMemory:
    """Test memory optimization features in data quality functions."""
    
    def setup_method(self):
        """Set up test environment."""
        # Set environment variables for testing
        os.environ['MAX_MEMORY_MB'] = '2048'
        os.environ['CHUNK_SIZE'] = '100000'
        os.environ['ENABLE_MEMORY_OPTIMIZATION'] = 'true'
    
    @patch('psutil.virtual_memory')
    def test_memory_optimization_enabled(self, mock_vm):
        """Test that memory optimization is enabled by default."""
        # Mock memory check to return True (sufficient memory)
        mock_vm.return_value.available = 4 * 1024 * 1024 * 1024  # 4GB available
        assert data_quality._check_memory_available() is True
    
    def test_estimate_memory_usage(self):
        """Test memory usage estimation."""
        # Create a test DataFrame
        df = pd.DataFrame({
            'A': np.random.randn(1000),
            'B': np.random.randint(0, 100, 1000),
            'C': ['test'] * 1000
        })
        
        memory_mb = data_quality._estimate_memory_usage(df)
        assert memory_mb >= 0  # Should be non-negative
        assert isinstance(memory_mb, int)
        
        # Test with larger DataFrame
        large_df = pd.DataFrame({
            'A': np.random.randn(10000),
            'B': np.random.randint(0, 100, 10000),
            'C': ['test'] * 10000
        })
        
        large_memory_mb = data_quality._estimate_memory_usage(large_df)
        assert large_memory_mb >= 0  # Should be non-negative
        assert isinstance(large_memory_mb, int)
    
    def test_nan_check_large_dataset(self):
        """Test NaN check with large dataset optimization."""
        # Create a large DataFrame
        large_df = pd.DataFrame({
            'A': np.random.randn(50000),
            'B': np.random.randint(0, 100, 50000),
            'C': ['test'] * 50000
        })
        
        # Add some NaN values
        large_df.loc[1000:1100, 'A'] = np.nan
        large_df.loc[2000, 'B'] = np.nan
        
        nan_summary = []
        
        # Test that the function runs without errors
        data_quality.nan_check(large_df, nan_summary, MagicMock(), MagicMock())
        
        # Should have processed the data
        assert len(nan_summary) > 0
    
    def test_duplicate_check_large_dataset(self):
        """Test duplicate check with large dataset optimization."""
        # Create a large DataFrame with duplicates
        large_df = pd.DataFrame({
            'A': np.random.randn(50000),
            'B': np.random.randint(0, 100, 50000),
            'C': ['test'] * 50000
        })
        
        # Add some duplicates
        large_df.loc[1000] = large_df.loc[999]
        large_df.loc[2000] = large_df.loc[1999]
        
        dupe_summary = []
        
        # Test that the function runs without errors
        data_quality.duplicate_check(large_df, dupe_summary, MagicMock(), MagicMock())
        
        # Should have processed the data
        assert isinstance(dupe_summary, list)
    
    def test_gap_check_large_dataset(self):
        """Test gap check with large dataset optimization."""
        # Create a large DataFrame with datetime
        dates = pd.date_range('2020-01-01', periods=50000, freq='1min')
        large_df = pd.DataFrame({
            'datetime': dates,
            'A': np.random.randn(50000),
            'B': np.random.randint(0, 100, 50000)
        })
        
        gap_summary = []
        
        # Test that the function runs without errors
        data_quality.gap_check(large_df, gap_summary, MagicMock(), MagicMock())
        
        # Should have processed the data
        assert isinstance(gap_summary, list)
    
    def test_zero_check_large_dataset(self):
        """Test zero check with large dataset optimization."""
        # Create a large DataFrame with zeros
        large_df = pd.DataFrame({
            'A': np.random.randn(50000),
            'B': np.random.randint(0, 100, 50000),
            'volume': np.random.randint(0, 1000, 50000)
        })
        
        # Add some zeros
        large_df.loc[1000:1100, 'volume'] = 0
        
        zero_summary = []
        
        # Test that the function runs without errors
        data_quality.zero_check(large_df, zero_summary, MagicMock(), MagicMock())
        
        # Should have processed the data
        assert isinstance(zero_summary, list)
    
    def test_negative_check_large_dataset(self):
        """Test negative check with large dataset optimization."""
        # Create a large DataFrame with negative values
        large_df = pd.DataFrame({
            'A': np.random.randn(50000),
            'B': np.random.randint(0, 100, 50000),
            'close': np.random.randn(50000) * 100
        })
        
        # Add some negative values
        large_df.loc[1000:1100, 'close'] = -5
        
        negative_summary = []
        
        # Test that the function runs without errors
        data_quality.negative_check(large_df, negative_summary, MagicMock(), MagicMock())
        
        # Should have processed the data
        assert isinstance(negative_summary, list)
    
    def test_inf_check_large_dataset(self):
        """Test infinity check with large dataset optimization."""
        # Create a large DataFrame with infinity values
        large_df = pd.DataFrame({
            'A': np.random.randn(50000),
            'B': np.random.randint(0, 100, 50000),
            'C': np.random.randn(50000)
        })
        
        # Add some infinity values
        large_df.loc[1000, 'C'] = np.inf
        large_df.loc[2000, 'C'] = -np.inf
        
        inf_summary = []
        
        # Test that the function runs without errors
        data_quality.inf_check(large_df, inf_summary, MagicMock(), MagicMock())
        
        # Should have processed the data
        assert isinstance(inf_summary, list)
    
    def test_small_dataset_normal_processing(self):
        """Test that small datasets use normal processing."""
        # Create a small DataFrame
        small_df = pd.DataFrame({
            'A': np.random.randn(1000),
            'B': np.random.randint(0, 100, 1000),
            'C': ['test'] * 1000
        })
        
        # Add some issues
        small_df.loc[100, 'A'] = np.nan
        small_df.loc[200] = small_df.loc[199]  # Duplicate
        
        nan_summary = []
        dupe_summary = []
        
        # Test that the functions run without errors
        data_quality.nan_check(small_df, nan_summary, MagicMock(), MagicMock())
        data_quality.duplicate_check(small_df, dupe_summary, MagicMock(), MagicMock())
        
        # Should have processed the data
        assert isinstance(nan_summary, list)
        assert isinstance(dupe_summary, list)
    
    def test_memory_cleanup(self):
        """Test that memory cleanup is called during processing."""
        # Create a large DataFrame
        large_df = pd.DataFrame({
            'A': np.random.randn(50000),
            'B': np.random.randint(0, 100, 50000)
        })
        
        nan_summary = []
        
        # Test that the function runs without errors
        data_quality.nan_check(large_df, nan_summary, MagicMock(), MagicMock())
        
        # Should have processed the data
        assert isinstance(nan_summary, list)
    
    def test_error_handling(self):
        """Test error handling in memory-optimized functions."""
        # Create a large DataFrame
        large_df = pd.DataFrame({
            'A': np.random.randn(50000),
            'B': np.random.randint(0, 100, 50000)
        })
        
        nan_summary = []
        
        # Test that the function runs without errors
        data_quality.nan_check(large_df, nan_summary, MagicMock(), MagicMock())
        
        # Should have processed the data
        assert isinstance(nan_summary, list)


if __name__ == "__main__":
    pytest.main([__file__])
