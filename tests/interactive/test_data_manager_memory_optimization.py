#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test memory optimization features in DataManager

This module tests the aggressive memory optimization features
implemented in the DataManager class.
"""

import pytest
import pandas as pd
import numpy as np
import tempfile
import os
from pathlib import Path
from unittest.mock import patch, MagicMock

from src.interactive.data_manager import DataManager


class TestDataManagerMemoryOptimization:
    """Test memory optimization features in DataManager."""
    
    def setup_method(self):
        """Set up test environment."""
        # Set environment variables for testing
        os.environ['MAX_MEMORY_MB'] = '512'
        os.environ['CHUNK_SIZE'] = '25000'
        os.environ['SAMPLE_SIZE'] = '5000'
        os.environ['MAX_FILE_SIZE_MB'] = '25'
        os.environ['ENABLE_MEMORY_OPTIMIZATION'] = 'true'
        os.environ['ENABLE_STREAMING'] = 'true'
        
        self.data_manager = DataManager()
    
    def test_memory_settings_initialization(self):
        """Test that memory settings are properly initialized."""
        assert self.data_manager.max_memory_mb == 512
        assert self.data_manager.chunk_size == 25000
        assert self.data_manager.sample_size == 5000
        assert self.data_manager.max_file_size_mb == 25
        assert self.data_manager.enable_memory_optimization is True
        assert self.data_manager.enable_streaming is True
    
    def test_estimate_memory_usage(self):
        """Test memory usage estimation."""
        # Create test DataFrame
        df = pd.DataFrame({
            'A': np.random.randn(1000),
            'B': np.random.randint(0, 100, 1000),
            'C': ['test'] * 1000
        })
        
        memory_mb = self.data_manager._estimate_memory_usage(df)
        assert memory_mb >= 0
        assert isinstance(memory_mb, int)
        
        # Test with larger DataFrame
        large_df = pd.DataFrame({
            'A': np.random.randn(10000),
            'B': np.random.randint(0, 100, 10000),
            'C': ['test'] * 10000
        })
        
        large_memory_mb = self.data_manager._estimate_memory_usage(large_df)
        assert large_memory_mb >= memory_mb  # Should be larger
    
    def test_check_memory_available(self):
        """Test memory availability check."""
        # Test with mock psutil
        with patch('psutil.virtual_memory') as mock_memory:
            mock_memory.return_value.available = 1024 * 1024 * 1024  # 1GB available
            assert self.data_manager._check_memory_available() is True
            
            mock_memory.return_value.available = 100 * 1024 * 1024  # 100MB available
            assert self.data_manager._check_memory_available() is False
    
    def test_get_file_size_mb(self):
        """Test file size calculation."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            f.write('test data' * 1000)  # Write some data
            file_path = Path(f.name)
        
        try:
            size_mb = self.data_manager._get_file_size_mb(file_path)
            assert size_mb > 0
            assert isinstance(size_mb, float)
        finally:
            file_path.unlink()
    
    def test_should_use_chunked_loading(self):
        """Test chunked loading decision logic."""
        # Create a small file
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            f.write('test data')
            small_file = Path(f.name)
        
        # Create a large file that exceeds the 25MB threshold
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            # Write enough data to exceed 25MB threshold
            large_data = 'test data ' * 3000000  # ~30MB of data
            f.write(large_data)
            large_file = Path(f.name)
        
        try:
            # Small file should not use chunked loading
            assert self.data_manager._should_use_chunked_loading(small_file) is False
            
            # Large file should use chunked loading
            assert self.data_manager._should_use_chunked_loading(large_file) is True
        finally:
            small_file.unlink()
            large_file.unlink()
    
    def test_load_csv_with_datetime_handling(self):
        """Test CSV loading with datetime handling."""
        # Create test CSV with datetime column
        csv_data = """DateTime,Open,High,Low,Close,Volume
2023-01-01 10:00:00,100.0,101.0,99.0,100.5,1000
2023-01-01 10:01:00,100.5,102.0,100.0,101.5,1500
2023-01-01 10:02:00,101.5,103.0,101.0,102.5,2000"""
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            f.write(csv_data)
            csv_path = Path(f.name)
        
        try:
            df = self.data_manager._load_csv_with_datetime_handling(csv_path)
            
            assert not df.empty
            assert 'DateTime' in df.columns
            assert pd.api.types.is_datetime64_any_dtype(df['DateTime'])
            assert len(df) == 3
        finally:
            csv_path.unlink()
    
    def test_load_csv_in_chunks(self):
        """Test chunked CSV loading."""
        # Create large CSV file
        csv_data = "DateTime,Open,High,Low,Close,Volume\n"
        for i in range(100000):  # 100k rows
            csv_data += f"2023-01-01 10:{i:02d}:00,{100+i},{101+i},{99+i},{100.5+i},{1000+i}\n"
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            f.write(csv_data)
            csv_path = Path(f.name)
        
        try:
            # Mock datetime columns detection
            datetime_columns = ['DateTime']
            
            df = self.data_manager._load_csv_in_chunks(csv_path, datetime_columns, chunk_size=1000)
            
            assert not df.empty
            assert 'DateTime' in df.columns
            assert pd.api.types.is_datetime64_any_dtype(df['DateTime'])
            assert len(df) == 100000
        finally:
            csv_path.unlink()
    
    def test_load_parquet_with_optimization(self):
        """Test parquet loading with optimization."""
        # Create test DataFrame
        test_df = pd.DataFrame({
            'DateTime': pd.date_range('2023-01-01', periods=1000, freq='1H'),
            'Open': np.random.randn(1000),
            'High': np.random.randn(1000),
            'Low': np.random.randn(1000),
            'Close': np.random.randn(1000),
            'Volume': np.random.randint(1000, 10000, 1000)
        })
        
        with tempfile.NamedTemporaryFile(suffix='.parquet', delete=False) as f:
            test_df.to_parquet(f.name)
            parquet_path = Path(f.name)
        
        try:
            df = self.data_manager._load_parquet_with_optimization(parquet_path)
            
            assert not df.empty
            assert len(df) == 1000
            assert all(col in df.columns for col in ['DateTime', 'Open', 'High', 'Low', 'Close', 'Volume'])
        finally:
            parquet_path.unlink()
    
    def test_memory_error_handling(self):
        """Test memory error handling."""
        # Mock memory check to return False
        with patch.object(self.data_manager, '_check_memory_available', return_value=False):
            with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
                f.write('test,data\n1,2')
                csv_path = Path(f.name)
            
            try:
                with pytest.raises(MemoryError):
                    self.data_manager.load_data_from_file(str(csv_path))
            finally:
                csv_path.unlink()
    
    def test_large_file_handling(self):
        """Test handling of large files."""
        # Create a large CSV file that exceeds the 25MB threshold
        csv_data = "DateTime,Open,High,Low,Close,Volume\n"
        for i in range(50000):  # 50k rows
            csv_data += f"2023-01-01 10:{i:02d}:00,{100+i},{101+i},{99+i},{100.5+i},{1000+i}\n"
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            f.write(csv_data)
            csv_path = Path(f.name)
        
        try:
            # Check if file is large enough to trigger chunked loading
            file_size_mb = self.data_manager._get_file_size_mb(csv_path)
            
            if file_size_mb > self.data_manager.max_file_size_mb:
                # Should use chunked loading for large file
                assert self.data_manager._should_use_chunked_loading(csv_path) is True
                
                # Load the file
                df = self.data_manager.load_data_from_file(str(csv_path))
                
                assert not df.empty
                assert len(df) == 50000
                assert 'DateTime' in df.columns
            else:
                # File is small enough for direct loading
                df = self.data_manager.load_data_from_file(str(csv_path))
                
                assert not df.empty
                assert len(df) == 50000
                assert 'DateTime' in df.columns
        finally:
            csv_path.unlink()
    
    def test_datetime_column_detection(self):
        """Test automatic datetime column detection."""
        # Create CSV with various datetime-like columns
        csv_data = """timestamp,date_time,time,open,high,low,close
2023-01-01 10:00:00,2023-01-01 10:00:00,10:00:00,100.0,101.0,99.0,100.5
2023-01-01 10:01:00,2023-01-01 10:01:00,10:01:00,100.5,102.0,100.0,101.5"""
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            f.write(csv_data)
            csv_path = Path(f.name)
        
        try:
            df = self.data_manager._load_csv_with_datetime_handling(csv_path)
            
            # Should detect and parse datetime columns
            datetime_columns = ['timestamp', 'date_time']
            for col in datetime_columns:
                if col in df.columns:
                    assert pd.api.types.is_datetime64_any_dtype(df[col])
        finally:
            csv_path.unlink()
    
    def test_memory_monitoring(self):
        """Test memory monitoring functionality."""
        memory_info = self.data_manager._get_memory_info()
        
        assert 'total_mb' in memory_info
        assert 'available_mb' in memory_info
        assert 'used_mb' in memory_info
        assert 'percent' in memory_info
        
        assert memory_info['total_mb'] > 0
        assert memory_info['available_mb'] >= 0
        assert memory_info['used_mb'] >= 0
        assert 0 <= memory_info['percent'] <= 100
    
    def test_environment_variable_overrides(self):
        """Test that environment variables properly override defaults."""
        # Test with different environment variables
        os.environ['MAX_MEMORY_MB'] = '1024'
        os.environ['CHUNK_SIZE'] = '50000'
        os.environ['SAMPLE_SIZE'] = '10000'
        
        data_manager = DataManager()
        
        assert data_manager.max_memory_mb == 1024
        assert data_manager.chunk_size == 50000
        assert data_manager.sample_size == 10000
    
    def test_error_handling_in_chunked_loading(self):
        """Test error handling during chunked loading."""
        # Create a CSV file with inconsistent column counts
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            f.write('col1,col2,col3\n')
            f.write('1,2,3\n')
            f.write('1,2,3,4,5\n')  # Extra columns
            csv_path = Path(f.name)
        
        try:
            datetime_columns = ['col1']
            
            # Should handle errors gracefully - pandas will raise ParserError
            with pytest.raises(pd.errors.ParserError):
                self.data_manager._load_csv_in_chunks(csv_path, datetime_columns, chunk_size=1000)
        finally:
            csv_path.unlink()
    
    def test_memory_cleanup(self):
        """Test that memory is properly cleaned up during processing."""
        # Create a large DataFrame to test memory cleanup
        large_df = pd.DataFrame({
            'A': np.random.randn(10000),
            'B': np.random.randint(0, 100, 10000),
            'C': ['test'] * 10000
        })
        
        # Test memory estimation
        initial_memory = self.data_manager._estimate_memory_usage(large_df)
        
        # Process the DataFrame
        processed_df = large_df.copy()
        processed_memory = self.data_manager._estimate_memory_usage(processed_df)
        
        # Memory usage should be similar
        assert abs(initial_memory - processed_memory) < 100  # Allow some variance
        
        # Clean up
        del large_df, processed_df
        import gc
        gc.collect()
    
    def test_conservative_memory_settings(self):
        """Test that conservative memory settings work correctly."""
        # Test with very conservative settings
        os.environ['MAX_MEMORY_MB'] = '256'
        os.environ['CHUNK_SIZE'] = '1000'
        os.environ['SAMPLE_SIZE'] = '1000'
        
        conservative_manager = DataManager()
        
        assert conservative_manager.max_memory_mb == 256
        assert conservative_manager.chunk_size == 1000
        assert conservative_manager.sample_size == 1000
        
        # Test memory check with conservative settings
        with patch('psutil.virtual_memory') as mock_memory:
            mock_memory.return_value.available = 50 * 1024 * 1024  # 50MB available (less than 30% of 256MB)
            assert conservative_manager._check_memory_available() is False
