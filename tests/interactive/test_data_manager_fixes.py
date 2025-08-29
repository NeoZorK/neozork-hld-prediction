#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test DataManager fixes for datetime index handling and memory optimization.

This test verifies that:
1. Datetime index is properly converted to column
2. Memory limits are more permissive
3. Large files can be loaded without premature stopping
"""

import pytest
import pandas as pd
import numpy as np
from pathlib import Path
import tempfile
import os
from unittest.mock import patch, MagicMock

from src.interactive.data_manager import DataManager


class TestDataManagerFixes:
    """Test DataManager fixes for datetime and memory issues."""
    
    def setup_method(self):
        """Set up test environment."""
        self.data_manager = DataManager()
        
        # Create test data with datetime index
        dates = pd.date_range('2023-01-01', periods=1000, freq='H')
        self.test_data = pd.DataFrame({
            'Open': np.random.randn(1000) + 100,
            'High': np.random.randn(1000) + 101,
            'Low': np.random.randn(1000) + 99,
            'Close': np.random.randn(1000) + 100,
            'Volume': np.random.randint(1000, 10000, 1000)
        }, index=dates)
        self.test_data.index.name = 'Timestamp'
    
    def test_datetime_index_handling(self):
        """Test that datetime index is properly converted to column."""
        # Test with datetime index
        result = self.data_manager._handle_datetime_index(self.test_data)
        
        # Check that index was converted to column
        assert 'Timestamp' in result.columns
        assert not isinstance(result.index, pd.DatetimeIndex)
        assert pd.api.types.is_datetime64_any_dtype(result['Timestamp'])
        
        # Check data integrity
        assert len(result) == len(self.test_data)
        assert all(col in result.columns for col in ['Open', 'High', 'Low', 'Close', 'Volume'])
    
    def test_datetime_index_unnamed(self):
        """Test handling of unnamed datetime index."""
        # Create data with unnamed datetime index
        data_unnamed = self.test_data.copy()
        data_unnamed.index.name = None
        
        result = self.data_manager._handle_datetime_index(data_unnamed)
        
        # Should be renamed to 'datetime'
        assert 'datetime' in result.columns
        assert pd.api.types.is_datetime64_any_dtype(result['datetime'])
    
    def test_no_datetime_index(self):
        """Test handling of data without datetime index."""
        # Create data without datetime index
        data_no_datetime = self.test_data.reset_index(drop=True)
        
        result = self.data_manager._handle_datetime_index(data_no_datetime)
        
        # Should return unchanged
        assert result.equals(data_no_datetime)
    
    def test_memory_limits_more_permissive(self):
        """Test that memory limits are more permissive."""
        # Check that memory limit is increased
        assert self.data_manager.max_memory_mb >= 4096  # At least 4GB
        
        # Check that memory check is more permissive
        with patch.object(self.data_manager, '_get_memory_info') as mock_memory:
            mock_memory.return_value = {
                'total_mb': 8192,
                'available_mb': 1000,  # Low available memory
                'used_mb': 7192,
                'percent': 87.8
            }
            
            # Should still pass with low memory (more permissive)
            assert self.data_manager._check_memory_available()
    
    def test_file_size_threshold_increased(self):
        """Test that file size threshold is increased."""
        assert self.data_manager.max_file_size_mb >= 200  # At least 200MB
    
    def test_chunk_size_increased(self):
        """Test that chunk size is increased."""
        assert self.data_manager.chunk_size >= 50000  # At least 50k rows
    
    def test_parquet_loading_with_datetime(self):
        """Test parquet loading with datetime index."""
        with tempfile.NamedTemporaryFile(suffix='.parquet', delete=False) as tmp_file:
            try:
                # Save test data with datetime index
                self.test_data.to_parquet(tmp_file.name)
                
                # Load with data manager
                result = self.data_manager._load_parquet_with_optimization(Path(tmp_file.name))
                
                # Check that datetime index was converted to column
                assert 'Timestamp' in result.columns
                assert pd.api.types.is_datetime64_any_dtype(result['Timestamp'])
                assert len(result) == len(self.test_data)
                
            finally:
                os.unlink(tmp_file.name)
    
    def test_csv_loading_with_datetime(self):
        """Test CSV loading with datetime columns."""
        with tempfile.NamedTemporaryFile(suffix='.csv', delete=False) as tmp_file:
            try:
                # Save test data as CSV
                self.test_data.to_csv(tmp_file.name)
                
                # Load with data manager
                result = self.data_manager._load_csv_direct(Path(tmp_file.name), ['Timestamp'])
                
                # Check that datetime column is properly parsed
                assert 'Timestamp' in result.columns
                assert pd.api.types.is_datetime64_any_dtype(result['Timestamp'])
                assert len(result) == len(self.test_data)
                
            finally:
                os.unlink(tmp_file.name)
    
    def test_memory_warning_threshold_increased(self):
        """Test that memory warning threshold is increased."""
        assert self.data_manager.memory_warning_threshold >= 0.8  # At least 80%
    
    def test_memory_critical_threshold_increased(self):
        """Test that memory critical threshold is increased."""
        assert self.data_manager.memory_critical_threshold >= 0.95  # At least 95%
    
    def test_large_file_loading_doesnt_stop_prematurely(self):
        """Test that large file loading doesn't stop prematurely."""
        # Mock memory info to simulate high memory usage
        with patch.object(self.data_manager, '_get_memory_info') as mock_memory:
            mock_memory.return_value = {
                'total_mb': 8192,
                'available_mb': 2000,  # High available memory
                'used_mb': 6192,
                'percent': 75.6
            }
            
            # Should allow loading even with high memory usage
            assert self.data_manager._check_memory_available()
            
            # Test with higher memory usage
            mock_memory.return_value['available_mb'] = 1000
            assert self.data_manager._check_memory_available()  # Should still pass
    
    def test_datetime_column_preservation_after_concat(self):
        """Test that datetime columns are preserved after concatenation."""
        # Create two dataframes with datetime index
        df1 = self.test_data.iloc[:500].copy()
        df2 = self.test_data.iloc[500:].copy()
        
        # Process both with datetime handling
        df1_processed = self.data_manager._handle_datetime_index(df1)
        df2_processed = self.data_manager._handle_datetime_index(df2)
        
        # Concatenate
        combined = pd.concat([df1_processed, df2_processed], ignore_index=True)
        
        # Check that datetime column is preserved
        assert 'Timestamp' in combined.columns
        assert pd.api.types.is_datetime64_any_dtype(combined['Timestamp'])
        assert len(combined) == len(df1) + len(df2)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
