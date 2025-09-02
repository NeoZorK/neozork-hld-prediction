#!/usr/bin/env python3
"""
Test timestamp column case sensitivity fix.
"""

import pytest
import pandas as pd
from pathlib import Path
import tempfile
import os
from src.interactive.data_loader import DataLoader
from src.interactive.memory_manager import MemoryManager


class TestTimestampCaseSensitivity:
    """Test that timestamp columns are detected regardless of case."""
    
    @pytest.fixture
    def data_loader(self):
        """Create DataLoader instance."""
        memory_manager = MemoryManager()
        return DataLoader(memory_manager)
    
    def test_timestamp_column_detection_uppercase(self, data_loader):
        """Test that 'Timestamp' column is detected and converted to index."""
        # Create test data with 'Timestamp' column (uppercase)
        test_data = {
            'Timestamp': ['2023-01-01 10:00:00', '2023-01-01 10:01:00', '2023-01-01 10:02:00'],
            'Open': [100.0, 101.0, 102.0],
            'High': [105.0, 106.0, 107.0],
            'Low': [99.0, 100.0, 101.0],
            'Close': [101.0, 102.0, 103.0],
            'Volume': [1000, 1100, 1200]
        }
        
        df = pd.DataFrame(test_data)
        
        # Process with handle_datetime_index
        result = data_loader.handle_datetime_index(df)
        
        # Check that Timestamp column was converted to index
        assert isinstance(result.index, pd.DatetimeIndex), "Index should be DatetimeIndex"
        assert result.index.name == 'Timestamp', "Index name should be 'Timestamp'"
        assert 'Timestamp' not in result.columns, "Timestamp column should be removed from columns"
        
        # Check that other columns are preserved
        expected_columns = ['Open', 'High', 'Low', 'Close', 'Volume']
        for col in expected_columns:
            assert col in result.columns, f"Column {col} should be preserved"
    
    def test_timestamp_column_detection_lowercase(self, data_loader):
        """Test that 'timestamp' column is detected and converted to index."""
        # Create test data with 'timestamp' column (lowercase)
        test_data = {
            'timestamp': ['2023-01-01 10:00:00', '2023-01-01 10:01:00', '2023-01-01 10:02:00'],
            'Open': [100.0, 101.0, 102.0],
            'High': [105.0, 106.0, 107.0],
            'Low': [99.0, 100.0, 101.0],
            'Close': [101.0, 102.0, 103.0],
            'Volume': [1000, 1100, 1200]
        }
        
        df = pd.DataFrame(test_data)
        
        # Process with handle_datetime_index
        result = data_loader.handle_datetime_index(df)
        
        # Check that timestamp column was converted to index
        assert isinstance(result.index, pd.DatetimeIndex), "Index should be DatetimeIndex"
        assert result.index.name == 'timestamp', "Index name should be 'timestamp'"
        assert 'timestamp' not in result.columns, "timestamp column should be removed from columns"
    
    def test_timestamp_column_detection_mixed_case(self, data_loader):
        """Test that 'TimeStamp' column is detected and converted to index."""
        # Create test data with 'TimeStamp' column (mixed case)
        test_data = {
            'TimeStamp': ['2023-01-01 10:00:00', '2023-01-01 10:01:00', '2023-01-01 10:02:00'],
            'Open': [100.0, 101.0, 102.0],
            'High': [105.0, 106.0, 107.0],
            'Low': [99.0, 100.0, 101.0],
            'Close': [101.0, 102.0, 103.0],
            'Volume': [1000, 1100, 1200]
        }
        
        df = pd.DataFrame(test_data)
        
        # Process with handle_datetime_index
        result = data_loader.handle_datetime_index(df)
        
        # Check that TimeStamp column was converted to index
        assert isinstance(result.index, pd.DatetimeIndex), "Index should be DatetimeIndex"
        assert result.index.name == 'TimeStamp', "Index name should be 'TimeStamp'"
        assert 'TimeStamp' not in result.columns, "TimeStamp column should be removed from columns"
    
    def test_no_timestamp_column_handling(self, data_loader):
        """Test that data without timestamp column is handled correctly."""
        # Create test data without timestamp column
        test_data = {
            'Open': [100.0, 101.0, 102.0],
            'High': [105.0, 106.0, 107.0],
            'Low': [99.0, 100.0, 101.0],
            'Close': [101.0, 102.0, 103.0],
            'Volume': [1000, 1100, 1200]
        }
        
        df = pd.DataFrame(test_data)
        
        # Process with handle_datetime_index
        result = data_loader.handle_datetime_index(df)
        
        # Check that data is returned unchanged
        assert result.equals(df), "Data should be returned unchanged when no timestamp column exists"
        assert not isinstance(result.index, pd.DatetimeIndex), "Index should not be DatetimeIndex"
    
    def test_already_datetime_index(self, data_loader):
        """Test that data with existing DatetimeIndex is returned unchanged."""
        # Create test data with existing DatetimeIndex
        test_data = {
            'Open': [100.0, 101.0, 102.0],
            'High': [105.0, 106.0, 107.0],
            'Low': [99.0, 100.0, 101.0],
            'Close': [101.0, 102.0, 103.0],
            'Volume': [1000, 1100, 1200]
        }
        
        df = pd.DataFrame(test_data)
        df.index = pd.DatetimeIndex(['2023-01-01 10:00:00', '2023-01-01 10:01:00', '2023-01-01 10:02:00'])
        df.index.name = 'Timestamp'
        
        # Process with handle_datetime_index
        result = data_loader.handle_datetime_index(df)
        
        # Check that data is returned unchanged
        assert result.equals(df), "Data with existing DatetimeIndex should be returned unchanged"
        assert isinstance(result.index, pd.DatetimeIndex), "Index should remain DatetimeIndex"
    
    def test_invalid_timestamp_data(self, data_loader):
        """Test that invalid timestamp data is handled gracefully."""
        # Create test data with invalid timestamp values
        test_data = {
            'Timestamp': ['invalid', '2023-01-01 10:01:00', 'also_invalid'],
            'Open': [100.0, 101.0, 102.0],
            'High': [105.0, 106.0, 107.0],
            'Low': [99.0, 100.0, 101.0],
            'Close': [101.0, 102.0, 103.0],
            'Volume': [1000, 1100, 1200]
        }
        
        df = pd.DataFrame(test_data)
        
        # Process with handle_datetime_index
        result = data_loader.handle_datetime_index(df)
        
        # Check that invalid timestamps are converted to NaT
        assert isinstance(result.index, pd.DatetimeIndex), "Index should be DatetimeIndex"
        assert result.index.name == 'Timestamp', "Index name should be 'Timestamp'"
        
        # Check that invalid timestamps are converted to NaT (not filtered out)
        assert len(result) == len(df), "All rows should be preserved"
        assert result.index.isna().sum() == 2, "Should have 2 NaT values for invalid timestamps"
        assert result.index.notna().sum() == 1, "Should have 1 valid timestamp"
