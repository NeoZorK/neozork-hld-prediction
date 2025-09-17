# -*- coding: utf-8 -*-
"""
Test data structure flexibility for gaps analysis.

This module tests how the gaps analysis handles different data structures.
"""

import pytest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

from src.interactive.eda_analysis.gaps_analysis import GapsDetector


class TestDataStructureFlexibility:
    """Test cases for data structure flexibility."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.detector = GapsDetector()
        
        # Create sample data with gaps
        dates = pd.date_range('2023-01-01', periods=10, freq='1h')
        indices_to_keep = [i for i in range(10) if i not in [3, 4, 7]]
        dates = dates[indices_to_keep]
        
        self.sample_data = pd.DataFrame({
            'Open': [100 + i for i in range(len(dates))],
            'High': [101 + i for i in range(len(dates))],
            'Low': [99 + i for i in range(len(dates))],
            'Close': [100.5 + i for i in range(len(dates))],
            'Volume': [1000 + i * 100 for i in range(len(dates))]
        }, index=dates)
    
    def test_standard_mtf_structure(self):
        """Test with standard MTF structure (loaded_data key)."""
        mtf_data = {
            'loaded_data': {
                'H1': self.sample_data,
                'D1': self.sample_data.resample('D').first()
            },
            'symbol': 'BTCUSD',
            'metadata': {}
        }
        
        result = self.detector.detect_gaps_in_mtf_data(mtf_data)
        
        assert result['status'] == 'success'
        assert 'timeframe_gaps' in result
        assert 'H1' in result['timeframe_gaps']
        assert 'D1' in result['timeframe_gaps']
    
    def test_direct_timeframe_structure(self):
        """Test with direct timeframe structure (no loaded_data key)."""
        mtf_data = {
            'H1': self.sample_data,
            'D1': self.sample_data.resample('D').first(),
            'symbol': 'BTCUSD',
            'metadata': {}
        }
        
        result = self.detector.detect_gaps_in_mtf_data(mtf_data)
        
        assert result['status'] == 'success'
        assert 'timeframe_gaps' in result
        assert 'H1' in result['timeframe_gaps']
        assert 'D1' in result['timeframe_gaps']
    
    def test_mixed_structure(self):
        """Test with mixed structure (some timeframes, some metadata)."""
        mtf_data = {
            'H1': self.sample_data,
            'D1': self.sample_data.resample('D').first(),
            '_metadata': {'symbol': 'BTCUSD'},
            '_other_info': 'test'
        }
        
        result = self.detector.detect_gaps_in_mtf_data(mtf_data)
        
        assert result['status'] == 'success'
        assert 'timeframe_gaps' in result
        assert 'H1' in result['timeframe_gaps']
        assert 'D1' in result['timeframe_gaps']
    
    def test_empty_data(self):
        """Test with empty data."""
        result = self.detector.detect_gaps_in_mtf_data(None)
        
        assert result['status'] == 'error'
        assert 'No MTF data provided' in result['message']
    
    def test_no_timeframe_data(self):
        """Test with data that has no timeframe information."""
        mtf_data = {
            'symbol': 'BTCUSD',
            'metadata': {},
            'other_info': 'test'
        }
        
        result = self.detector.detect_gaps_in_mtf_data(mtf_data)
        
        assert result['status'] == 'error'
        assert 'No valid timeframe data found' in result['message']
    
    def test_single_timeframe(self):
        """Test with single timeframe."""
        mtf_data = {
            'H1': self.sample_data
        }
        
        result = self.detector.detect_gaps_in_mtf_data(mtf_data)
        
        assert result['status'] == 'success'
        assert 'timeframe_gaps' in result
        assert 'H1' in result['timeframe_gaps']


if __name__ == '__main__':
    pytest.main([__file__])
