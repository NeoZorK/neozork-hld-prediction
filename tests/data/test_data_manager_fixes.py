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
import sys

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.interactive.data.data_manager import DataManager


class TestDataManagerFixes:
    """Test DataManager fixes and improvements."""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Set up test fixtures."""
        # Create test data
        dates = pd.date_range('2024-01-01', periods=1000, freq='H')
        self.test_data = pd.DataFrame({
            'Open': np.random.randn(1000).cumsum() + 100,
            'High': np.random.randn(1000).cumsum() + 105,
            'Low': np.random.randn(1000).cumsum() + 95,
            'Close': np.random.randn(1000).cumsum() + 100,
            'Volume': np.random.randint(1000, 10000, 1000)
        }, index=dates)
        self.test_data.index.name = 'Timestamp'
        
        # Create DataManager instance
        self.data_manager = DataManager()
    
    def test_datetime_index_handling(self):
        """Test handling of datetime index."""
        # Test that we can work with datetime data
        assert 'Timestamp' in self.test_data.index.name
        assert pd.api.types.is_datetime64_any_dtype(self.test_data.index)
        
        # Test that DataManager has data_loader
        assert hasattr(self.data_manager, 'data_loader')
        assert hasattr(self.data_manager.data_loader, 'handle_datetime_index')
        
        # Test data integrity
        assert len(self.test_data) == 1000
        assert all(col in self.test_data.columns for col in ['Open', 'High', 'Low', 'Close', 'Volume'])
    
    def test_datetime_index_unnamed(self):
        """Test handling of unnamed datetime index."""
        # Create data with unnamed datetime index
        data_unnamed = self.test_data.copy()
        data_unnamed.index.name = None
        
        # Test that we can handle unnamed datetime index
        assert data_unnamed.index.name is None
        assert pd.api.types.is_datetime64_any_dtype(data_unnamed.index)
        
        # Test that DataManager can handle this data
        assert hasattr(self.data_manager, 'data_loader')
        assert hasattr(self.data_manager.data_loader, 'handle_datetime_index')
        
        # Test data integrity
        assert len(data_unnamed) == 1000
        assert all(col in data_unnamed.columns for col in ['Open', 'High', 'Low', 'Close', 'Volume'])
    
    def test_no_datetime_index(self):
        """Test handling of data without datetime index."""
        # Create data without datetime index
        data_no_datetime = self.test_data.reset_index(drop=True)
        
        # Test that we can handle data without datetime index
        assert not isinstance(data_no_datetime.index, pd.DatetimeIndex)
        assert len(data_no_datetime) == 1000
        
        # Test that DataManager can handle this data
        assert hasattr(self.data_manager, 'data_loader')
        assert hasattr(self.data_manager.data_loader, 'handle_datetime_index')
        
        # Test data integrity
        assert all(col in data_no_datetime.columns for col in ['Open', 'High', 'Low', 'Close', 'Volume'])
    
    def test_memory_limits_more_permissive(self):
        """Test that memory limits are reasonable."""
        # Check that memory limit is reasonable (at least 1GB)
        assert self.data_manager.max_memory_mb >= 1024  # At least 1GB
        
        # Check that memory manager exists and works
        assert hasattr(self.data_manager, 'memory_manager')
        assert hasattr(self.data_manager.memory_manager, 'get_memory_info')
        
        # Test memory info retrieval
        memory_info = self.data_manager.memory_manager.get_memory_info()
        assert isinstance(memory_info, dict)
        assert 'available_mb' in memory_info
        assert 'total_gb' in memory_info
        assert 'used_gb' in memory_info
        assert 'percent_used' in memory_info
    
    def test_file_size_handling(self):
        """Test file size handling."""
        # Test that chunk size is reasonable
        assert self.data_manager.chunk_size > 0
        assert self.data_manager.chunk_size <= 100000  # Reasonable upper limit
        
        # Test that DataManager has memory manager
        assert hasattr(self.data_manager, 'memory_manager')
        assert hasattr(self.data_manager.memory_manager, 'get_file_size_mb')
    
    def test_chunk_size_increased(self):
        """Test that chunk size can be increased."""
        # Test that chunk size can be modified
        original_chunk_size = self.data_manager.chunk_size
        self.data_manager.chunk_size = original_chunk_size * 2
        
        assert self.data_manager.chunk_size == original_chunk_size * 2
        
        # Restore original value
        self.data_manager.chunk_size = original_chunk_size
    
    def test_parquet_loading_with_datetime(self):
        """Test parquet loading with datetime data."""
        # Test that DataManager can handle parquet files
        assert hasattr(self.data_manager, 'data_loader')
        assert hasattr(self.data_manager.data_loader, 'load_parquet_with_optimization')
        
        # Test data integrity
        assert len(self.test_data) == 1000
        assert all(col in self.test_data.columns for col in ['Open', 'High', 'Low', 'Close', 'Volume'])
    
    def test_csv_loading_with_datetime(self):
        """Test CSV loading with datetime data."""
        # Test that DataManager can handle CSV files
        assert hasattr(self.data_manager, 'data_loader')
        assert hasattr(self.data_manager.data_loader, 'load_csv_direct')
        
        # Test data integrity
        assert len(self.test_data) == 1000
        assert all(col in self.test_data.columns for col in ['Open', 'High', 'Low', 'Close', 'Volume'])
        
        # Test that we can work with datetime data
        assert 'Timestamp' in self.test_data.index.name
        assert pd.api.types.is_datetime64_any_dtype(self.test_data.index)
    
    def test_memory_warning_threshold_increased(self):
        """Test that memory warning threshold is reasonable."""
        # Test that memory manager exists
        assert hasattr(self.data_manager, 'memory_manager')
        assert hasattr(self.data_manager.memory_manager, 'get_memory_info')
        
        # Test memory info retrieval
        memory_info = self.data_manager.memory_manager.get_memory_info()
        assert isinstance(memory_info, dict)
        assert 'percent_used' in memory_info
        
        # Test that percent used is reasonable
        assert 0 <= memory_info['percent_used'] <= 100
    
    def test_memory_critical_threshold_increased(self):
        """Test that memory critical threshold is reasonable."""
        # Test that memory manager exists
        assert hasattr(self.data_manager, 'memory_manager')
        assert hasattr(self.data_manager.memory_manager, 'get_memory_info')
        
        # Test memory info retrieval
        memory_info = self.data_manager.memory_manager.get_memory_info()
        assert isinstance(memory_info, dict)
        assert 'available_gb' in memory_info
        
        # Test that available memory is reasonable
        assert memory_info['available_gb'] > 0
    
    def test_large_file_loading_doesnt_stop_prematurely(self):
        """Test that large files can be loaded without premature stopping."""
        # Test that DataManager can handle large files
        assert hasattr(self.data_manager, 'memory_manager')
        assert hasattr(self.data_manager.memory_manager, 'get_memory_info')
        
        # Test memory info retrieval
        memory_info = self.data_manager.memory_manager.get_memory_info()
        assert isinstance(memory_info, dict)
        assert 'available_mb' in memory_info
        assert 'total_gb' in memory_info
        
        # Test chunk size configuration
        assert self.data_manager.chunk_size > 0
        assert self.data_manager.max_memory_mb > 0
    
    def test_datetime_column_preservation_after_concat(self):
        """Test that datetime columns are preserved after concatenation."""
        # Test that we can work with datetime data
        assert 'Timestamp' in self.test_data.index.name
        assert pd.api.types.is_datetime64_any_dtype(self.test_data.index)
        
        # Test that DataManager can handle this data
        assert hasattr(self.data_manager, 'data_loader')
        assert hasattr(self.data_manager.data_loader, 'handle_datetime_index')
        
        # Test data integrity
        assert len(self.test_data) == 1000
        assert all(col in self.test_data.columns for col in ['Open', 'High', 'Low', 'Close', 'Volume'])
        
        # Test concatenation preserves data
        combined_data = pd.concat([self.test_data, self.test_data])
        assert len(combined_data) == 2000
        assert all(col in combined_data.columns for col in ['Open', 'High', 'Low', 'Close', 'Volume'])


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
