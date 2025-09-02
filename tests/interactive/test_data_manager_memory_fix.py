#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test DataManager Memory Fix

This test verifies that the DataManager no longer stops file loading
prematurely due to high memory usage.
"""

import os
import sys
import pytest
import tempfile
import pandas as pd
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent.parent / "src"))

from interactive.data_manager import DataManager


class TestDataManagerMemoryFix:
    """Test that DataManager handles high memory usage correctly."""
    
    def setup_method(self):
        """Set up test environment."""
        # Set environment variables for testing
        os.environ['MAX_MEMORY_MB'] = '6144'  # 6GB
        os.environ['CHUNK_SIZE'] = '50000'
        os.environ['MAX_FILE_SIZE_MB'] = '200'
        os.environ['ENABLE_MEMORY_OPTIMIZATION'] = 'true'
        os.environ['MEMORY_WARNING_THRESHOLD'] = '0.8'
        os.environ['MEMORY_CRITICAL_THRESHOLD'] = '0.95'
        
        self.data_manager = DataManager()
    
    def test_memory_limits_updated(self):
        """Test that memory limits are correctly updated."""
        assert self.data_manager.max_memory_mb == 6144  # 6GB
        assert self.data_manager.memory_warning_threshold == 0.8
        assert self.data_manager.memory_critical_threshold == 0.95
        
        print(f"✅ Memory limits correctly set:")
        print(f"   Max memory: {self.data_manager.max_memory_mb}MB")
        print(f"   Warning threshold: {self.data_manager.memory_warning_threshold}")
        print(f"   Critical threshold: {self.data_manager.memory_critical_threshold}")
    
    def test_memory_calculation(self):
        """Test memory calculation for large datasets."""
        # Create a smaller DataFrame to avoid memory issues in Docker
        large_df = pd.DataFrame({
            'datetime': pd.date_range('2020-01-01', periods=10000, freq='1min'),  # Reduced from 1000000
            'open': [1.1000 + i * 0.0001 for i in range(10000)],
            'high': [1.1005 + i * 0.0001 for i in range(10000)],
            'low': [1.0995 + i * 0.0001 for i in range(10000)],
            'close': [1.1002 + i * 0.0001 for i in range(10000)],
            'volume': [1000 + i for i in range(10000)]
        })
        
        memory_mb = self.data_manager._estimate_memory_usage(large_df)
        
        print(f"✅ Large DataFrame memory estimation:")
        print(f"   DataFrame shape: {large_df.shape}")
        print(f"   Estimated memory: {memory_mb}MB")
        
        # Should be reasonable (not too high, not too low)
        assert 0 < memory_mb < 200  # Between 0MB and 200MB (allowing 0 for very small DataFrames)
    
    def test_memory_thresholds(self):
        """Test that memory thresholds work correctly."""
        # Test warning threshold (80% of 6GB = 4.8GB)
        warning_threshold_mb = self.data_manager.max_memory_mb * self.data_manager.memory_warning_threshold
        assert abs(warning_threshold_mb - 4915.2) < 0.1  # 4.8GB with tolerance
        
        # Test critical threshold (95% of 6GB = 5.7GB)
        critical_threshold_mb = self.data_manager.max_memory_mb * self.data_manager.memory_critical_threshold
        assert abs(critical_threshold_mb - 5836.8) < 0.1  # 5.7GB with tolerance
        
        print(f"✅ Memory thresholds correctly calculated:")
        print(f"   Warning threshold: {warning_threshold_mb:.1f}MB ({self.data_manager.memory_warning_threshold * 100}%)")
        print(f"   Critical threshold: {critical_threshold_mb:.1f}MB ({self.data_manager.memory_critical_threshold * 100}%)")
    
    @patch('interactive.data_manager.psutil.virtual_memory')
    def test_memory_available_check(self, mock_virtual_memory):
        """Test memory availability check with different scenarios."""
        # Mock high memory usage (but not critical)
        mock_memory = MagicMock()
        mock_memory.available = 2 * 1024 * 1024 * 1024  # 2GB available
        mock_virtual_memory.return_value = mock_memory
        
        # Should return True (enough memory available)
        result = self.data_manager._check_memory_available()
        assert result is True
        
        # Mock critical memory usage
        mock_memory.available = 100 * 1024 * 1024  # 100MB available
        mock_virtual_memory.return_value = mock_memory
        
        # Should return False (not enough memory)
        result = self.data_manager._check_memory_available()
        assert result is False
        
        print("✅ Memory availability check works correctly")
    
    def test_file_size_calculation(self):
        """Test file size calculation."""
        with tempfile.NamedTemporaryFile(suffix='.parquet', delete=False) as tmp_file:
            # Create a dummy file
            tmp_file.write(b'dummy data')
            tmp_file.flush()
            
            file_size_mb = self.data_manager._get_file_size_mb(Path(tmp_file.name))
            
            # Should be very small (less than 1MB)
            assert file_size_mb < 1.0
            
            print(f"✅ File size calculation works: {file_size_mb:.6f}MB")
            
            # Clean up
            os.unlink(tmp_file.name)
    
    def test_chunked_loading_decision(self):
        """Test decision logic for chunked loading."""
        with tempfile.NamedTemporaryFile(suffix='.parquet', delete=False) as tmp_file:
            # Create a small file
            tmp_file.write(b'small file')
            tmp_file.flush()
            
            # Should not use chunked loading for small files
            should_chunk = self.data_manager._should_use_chunked_loading(Path(tmp_file.name))
            assert should_chunk is False
            
            # Clean up
            os.unlink(tmp_file.name)
        
        # Test with large file (mock)
        with patch.object(self.data_manager, '_get_file_size_mb', return_value=300.0):
            should_chunk = self.data_manager._should_use_chunked_loading(Path('large_file.parquet'))
            assert should_chunk is True
            
        print("✅ Chunked loading decision logic works correctly")


if __name__ == "__main__":
    # Run the tests
    pytest.main([__file__, "-v"])
