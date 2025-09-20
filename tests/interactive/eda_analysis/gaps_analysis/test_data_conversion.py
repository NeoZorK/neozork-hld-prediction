# -*- coding: utf-8 -*-
"""
Test data conversion for gaps analysis.

This module tests the data conversion functionality for gaps analysis.
"""

import pytest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

from src.interactive.menu_system.eda_menu import EDAMenu


class TestDataConversion:
    """Test cases for data conversion functionality."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.eda_menu = EDAMenu()
        
        # Create sample data structure as returned by data_state_manager
        dates = pd.date_range('2023-01-01', periods=100, freq='1h')
        self.sample_data = pd.DataFrame({
            'Open': np.random.randn(len(dates)) * 100 + 1000,
            'High': np.random.randn(len(dates)) * 100 + 1000,
            'Low': np.random.randn(len(dates)) * 100 + 1000,
            'Close': np.random.randn(len(dates)) * 100 + 1000,
            'Volume': np.random.randint(1000, 10000, len(dates))
        }, index=dates)
        
        # Create cross timeframes data
        self.cross_data = {
            'M5': self.sample_data.resample('5T').first(),
            'M15': self.sample_data.resample('15T').first(),
            'H1': self.sample_data.resample('1H').first()
        }
        
        # Create metadata
        self.metadata = {
            'symbol': 'EURUSD',
            'source': 'csv',
            'main_timeframe': 'M1',
            'timeframes': ['M1', 'M5', 'M15', 'H1'],
            'total_rows': 100,
            'main_data_shape': (100, 5),
            'cross_timeframes': ['M5', 'M15', 'H1'],
            'created_at': '2023-01-01T00:00:00',
            'size_mb': 1.0,
            'file_count': 1,
            'folder_path': '/test/path'
        }
    
    def test_convert_data_for_gaps_analysis(self):
        """Test data conversion for gaps analysis."""
        # Create data structure as returned by data_state_manager
        raw_data = {
            'status': 'success',
            'main_data': self.sample_data,
            'cross_timeframes': ['M5', 'M15', 'H1'],
            'M5': self.cross_data['M5'],
            'M15': self.cross_data['M15'],
            'H1': self.cross_data['H1'],
            'memory_used': 100.0,
            'loading_time': 1.0,
            'metadata': self.metadata
        }
        
        # Convert data
        converted_data = self.eda_menu._convert_data_for_gaps_analysis(raw_data)
        
        # Check structure
        assert isinstance(converted_data, dict)
        assert 'M1' in converted_data  # Main timeframe
        assert 'M5' in converted_data  # Cross timeframe
        assert 'M15' in converted_data  # Cross timeframe
        assert 'H1' in converted_data  # Cross timeframe
        assert '_metadata' in converted_data
        assert '_symbol' in converted_data
        
        # Check data types
        assert isinstance(converted_data['M1'], pd.DataFrame)
        assert isinstance(converted_data['M5'], pd.DataFrame)
        assert isinstance(converted_data['M15'], pd.DataFrame)
        assert isinstance(converted_data['H1'], pd.DataFrame)
        
        # Check metadata
        assert converted_data['_symbol'] == 'EURUSD'
        assert converted_data['_metadata']['symbol'] == 'EURUSD'
        
        # Check data shapes (should have reasonable sizes)
        assert converted_data['M1'].shape[0] == 100
        assert converted_data['M5'].shape[0] > 0
        assert converted_data['M15'].shape[0] > 0
        assert converted_data['H1'].shape[0] > 0
    
    def test_convert_data_missing_main_data(self):
        """Test data conversion with missing main_data."""
        raw_data = {
            'status': 'success',
            'cross_timeframes': ['M5', 'M15'],
            'metadata': self.metadata
        }
        
        # Should return original data if main_data is missing
        converted_data = self.eda_menu._convert_data_for_gaps_analysis(raw_data)
        assert converted_data == raw_data
    
    def test_convert_data_missing_metadata(self):
        """Test data conversion with missing metadata."""
        raw_data = {
            'status': 'success',
            'main_data': self.sample_data,
            'cross_timeframes': ['M5', 'M15']
        }
        
        converted_data = self.eda_menu._convert_data_for_gaps_analysis(raw_data)
        
        # Should still work but with default values
        assert '_symbol' in converted_data
        assert converted_data['_symbol'] == 'UNKNOWN'
    
    def test_convert_data_empty_cross_timeframes(self):
        """Test data conversion with empty cross timeframes."""
        # Create metadata with empty cross_timeframes
        empty_metadata = self.metadata.copy()
        empty_metadata['cross_timeframes'] = []
        
        raw_data = {
            'status': 'success',
            'main_data': self.sample_data,
            'cross_timeframes': [],
            'metadata': empty_metadata
        }
        
        converted_data = self.eda_menu._convert_data_for_gaps_analysis(raw_data)
        
        # Should only have main timeframe
        assert 'M1' in converted_data
        assert len([k for k in converted_data.keys() if not k.startswith('_')]) == 1
    
    def test_convert_data_with_cross_timeframe_data(self):
        """Test data conversion with actual cross timeframe data."""
        raw_data = {
            'status': 'success',
            'main_data': self.sample_data,
            'cross_timeframes': ['M5', 'M15', 'H1'],
            'M5': self.cross_data['M5'],
            'M15': self.cross_data['M15'],
            'H1': self.cross_data['H1'],
            'metadata': self.metadata
        }
        
        converted_data = self.eda_menu._convert_data_for_gaps_analysis(raw_data)
        
        # Should have all timeframes
        assert 'M1' in converted_data
        assert 'M5' in converted_data
        assert 'M15' in converted_data
        assert 'H1' in converted_data
        
        # Check that cross timeframe data is preserved
        assert converted_data['M5'].equals(self.cross_data['M5'])
        assert converted_data['M15'].equals(self.cross_data['M15'])
        assert converted_data['H1'].equals(self.cross_data['H1'])


if __name__ == '__main__':
    pytest.main([__file__])
