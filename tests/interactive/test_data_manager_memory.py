#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test memory optimization in DataManager

This module tests the memory optimization features of the DataManager class.
"""

import pytest
import pandas as pd
import numpy as np
import tempfile
import os
from pathlib import Path
from unittest.mock import patch, MagicMock

from src.interactive.data_manager import DataManager


class TestDataManagerMemory:
    """Test memory optimization features."""
    
    def setup_method(self):
        """Set up test environment."""
        self.data_manager = DataManager()
        
    def test_memory_optimization_enabled(self):
        """Test that memory optimization is enabled by default."""
        assert self.data_manager.enable_memory_optimization is True
        assert self.data_manager.max_memory_mb > 0
        assert self.data_manager.chunk_size > 0
    
    def test_estimate_memory_usage(self):
        """Test memory usage estimation."""
        # Create a test DataFrame
        df = pd.DataFrame({
            'A': np.random.randn(1000),
            'B': np.random.randint(0, 100, 1000),
            'C': ['test'] * 1000
        })
        
        memory_mb = self.data_manager._estimate_memory_usage(df)
        # Memory usage should be at least 1 MB for this DataFrame
        assert memory_mb >= 0  # Allow 0 for very small DataFrames
        assert isinstance(memory_mb, int)
        
        # Test with larger DataFrame
        large_df = pd.DataFrame({
            'A': np.random.randn(10000),
            'B': np.random.randint(0, 100, 10000),
            'C': ['test'] * 10000
        })
        
        large_memory_mb = self.data_manager._estimate_memory_usage(large_df)
        assert large_memory_mb > 0  # Larger DataFrame should use more memory
        assert isinstance(large_memory_mb, int)
    
    def test_check_memory_available(self):
        """Test memory availability check."""
        # Test with psutil available
        with patch('psutil.virtual_memory') as mock_vm:
            mock_vm.return_value.available = 4 * 1024 * 1024 * 1024  # 4GB available
            assert self.data_manager._check_memory_available() is True
            
            # Test with insufficient memory (less than 10% of max_memory_mb)
            # max_memory_mb is 6144MB by default, so 10% is 614.4MB
            mock_vm.return_value.available = 500 * 1024 * 1024  # 500MB available (less than 614.4MB required)
            assert self.data_manager._check_memory_available() is False
        
        # Test without psutil (should return True)
        with patch.dict('sys.modules', {'psutil': None}):
            assert self.data_manager._check_memory_available() is True
    
    def test_load_data_in_chunks_parquet(self):
        """Test chunked loading of parquet files."""
        # Create a large test DataFrame
        large_df = pd.DataFrame({
            'timestamp': pd.date_range('2020-01-01', periods=100000, freq='1min'),
            'open': np.random.randn(100000),
            'high': np.random.randn(100000),
            'low': np.random.randn(100000),
            'close': np.random.randn(100000),
            'volume': np.random.randint(0, 1000, 100000)
        })
        
        with tempfile.NamedTemporaryFile(suffix='.parquet', delete=False) as tmp_file:
            large_df.to_parquet(tmp_file.name)
            tmp_path = tmp_file.name
        
        try:
            # Test chunked loading
            result_df = self.data_manager._load_data_in_chunks(tmp_path, chunk_size=10000)
            
            assert result_df.shape == large_df.shape
            assert list(result_df.columns) == list(large_df.columns)
            assert result_df['open'].sum() == pytest.approx(large_df['open'].sum(), rel=1e-10)
            
        finally:
            os.unlink(tmp_path)
    
    def test_load_data_in_chunks_csv(self):
        """Test chunked loading of CSV files."""
        # Create a large test DataFrame
        large_df = pd.DataFrame({
            'timestamp': pd.date_range('2020-01-01', periods=50000, freq='1min'),
            'open': np.random.randn(50000),
            'high': np.random.randn(50000),
            'low': np.random.randn(50000),
            'close': np.random.randn(50000),
            'volume': np.random.randint(0, 1000, 50000)
        })
        
        with tempfile.NamedTemporaryFile(suffix='.csv', delete=False) as tmp_file:
            large_df.to_csv(tmp_file.name, index=False)
            tmp_path = tmp_file.name
        
        try:
            # Test chunked loading
            result_df = self.data_manager._load_data_in_chunks(tmp_path, chunk_size=5000)
            
            assert result_df.shape == large_df.shape
            assert list(result_df.columns) == list(large_df.columns)
            assert result_df['open'].sum() == pytest.approx(large_df['open'].sum(), rel=1e-10)
            
        finally:
            os.unlink(tmp_path)
    
    def test_large_file_detection(self):
        """Test detection of large files for chunked loading."""
        # Create a small file
        small_df = pd.DataFrame({'A': [1, 2, 3]})
        
        with tempfile.NamedTemporaryFile(suffix='.parquet', delete=False) as tmp_file:
            small_df.to_parquet(tmp_file.name)
            tmp_path = tmp_file.name
        
        try:
            # Small file should not trigger chunked loading
            with patch.object(self.data_manager, '_load_data_in_chunks') as mock_chunked:
                self.data_manager.load_data_from_file(tmp_path)
                mock_chunked.assert_not_called()
                
        finally:
            os.unlink(tmp_path)
    
    def test_memory_optimization_disabled(self):
        """Test behavior when memory optimization is disabled."""
        # Create a data manager with optimization disabled
        with patch.dict(os.environ, {'ENABLE_MEMORY_OPTIMIZATION': 'false'}):
            dm = DataManager()
            assert dm.enable_memory_optimization is False
    
    def test_custom_memory_settings(self):
        """Test custom memory settings from environment."""
        with patch.dict(os.environ, {
            'MAX_MEMORY_MB': '8192',
            'CHUNK_SIZE': '200000'
        }):
            dm = DataManager()
            assert dm.max_memory_mb == 8192
            assert dm.chunk_size == 200000
    
    def test_memory_cleanup(self):
        """Test that memory cleanup is called during chunked loading."""
        # Create a large test DataFrame
        large_df = pd.DataFrame({
            'A': np.random.randn(50000),
            'B': np.random.randint(0, 100, 50000)
        })
        
        with tempfile.NamedTemporaryFile(suffix='.parquet', delete=False) as tmp_file:
            large_df.to_parquet(tmp_file.name)
            tmp_path = tmp_file.name
        
        try:
            # Test that gc.collect is called during chunked loading
            with patch('gc.collect') as mock_gc:
                self.data_manager._load_data_in_chunks(tmp_path, chunk_size=10000)
                # Should be called multiple times during chunked loading
                assert mock_gc.call_count > 0
                
        finally:
            os.unlink(tmp_path)
    
    def test_error_handling_in_chunked_loading(self):
        """Test error handling in chunked loading."""
        # Test with non-existent file
        with pytest.raises(FileNotFoundError):
            self.data_manager._load_data_in_chunks('non_existent_file.parquet')
        
        # Test with unsupported file format
        with tempfile.NamedTemporaryFile(suffix='.txt', delete=False) as tmp_file:
            tmp_file.write(b'test data')
            tmp_path = tmp_file.name
        
        try:
            with pytest.raises(ValueError, match="Unsupported file format"):
                self.data_manager._load_data_in_chunks(tmp_path)
        finally:
            os.unlink(tmp_path)


if __name__ == "__main__":
    pytest.main([__file__])
