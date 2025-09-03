#!/usr/bin/env python3
"""
Test enhanced duplicates analysis functionality.

This test verifies that the enhanced duplicates analysis works correctly
with both main timeframe data and multi-timeframe datasets.
"""

import pytest
import pandas as pd
import numpy as np
from unittest.mock import Mock, MagicMock, patch
from datetime import datetime, timedelta

# Import the module to test
from src.interactive.eda import EDAAnalyzer


class TestEnhancedDuplicatesAnalysis:
    """Test enhanced duplicates analysis functionality."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.eda_analyzer = EDAAnalyzer()
        
        # Create sample data with duplicates
        dates = pd.date_range('2024-01-01', periods=100, freq='1H')
        
        # Main dataset with some duplicates
        self.main_data = pd.DataFrame({
            'timestamp': dates,
            'open': np.random.randn(100) * 100 + 1000,
            'high': np.random.randn(100) * 100 + 1000,
            'low': np.random.randn(100) * 100 + 1000,
            'close': np.random.randn(100) * 100 + 1000,
            'volume': np.random.randint(1000, 10000, 100)
        })
        
        # Add some duplicates to main data
        self.main_data = pd.concat([
            self.main_data,
            self.main_data.iloc[0:5]  # Add 5 duplicate rows
        ], ignore_index=True)
        
        # Create multi-timeframe data
        self.multi_timeframe_data = {
            'M5': pd.DataFrame({
                'timestamp': pd.date_range('2024-01-01', periods=50, freq='5T'),
                'open': np.random.randn(50) * 50 + 1000,
                'high': np.random.randn(50) * 50 + 1000,
                'low': np.random.randn(50) * 50 + 1000,
                'close': np.random.randn(50) * 50 + 1000,
                'volume': np.random.randint(1000, 10000, 50)
            }),
            'H1': pd.DataFrame({
                'timestamp': pd.date_range('2024-01-01', periods=24, freq='1H'),
                'open': np.random.randn(24) * 100 + 1000,
                'high': np.random.randn(24) * 100 + 1000,
                'low': np.random.randn(24) * 100 + 1000,
                'close': np.random.randn(24) * 100 + 1000,
                'volume': np.random.randint(1000, 10000, 24)
            })
        }
        
        # Add duplicates to M5 timeframe
        self.multi_timeframe_data['M5'] = pd.concat([
            self.multi_timeframe_data['M5'],
            self.multi_timeframe_data['M5'].iloc[0:3]  # Add 3 duplicate rows
        ], ignore_index=True)
        
        # Mock system object
        self.mock_system = Mock()
        self.mock_system.current_data = self.main_data
        self.mock_system.other_timeframes_data = self.multi_timeframe_data
    
    def test_analyze_duplicates_enhanced(self):
        """Test enhanced duplicate analysis on a single dataset."""
        result = self.eda_analyzer.duplicates_analyzer.duplicate_detection._analyze_duplicates(self.main_data)
        
        assert isinstance(result, dict)
        assert 'total_duplicates' in result
        assert 'duplicate_percent' in result
        assert 'exact_duplicates' in result
        assert 'timestamp_based_duplicates' in result
        assert 'ohlcv_based_duplicates' in result
        assert 'key_columns' in result
        assert 'ohlcv_duplicates' in result
        
        # Check that duplicates were found
        assert result['total_duplicates'] == 5
        assert result['exact_duplicates'] == 5
        assert result['duplicate_percent'] > 0
    
    @patch('builtins.input', return_value='n')
    def test_run_duplicates_analysis_main_dataset(self, mock_input):
        """Test duplicates analysis on main dataset only."""
        # Test with system that only has main data
        system_main_only = Mock()
        system_main_only.current_data = self.main_data
        system_main_only.other_timeframes_data = None
        
        result = self.eda_analyzer.run_duplicates_analysis(system_main_only)
        
        assert result is True
    
    @patch('builtins.input', return_value='n')
    def test_run_duplicates_analysis_with_multi_timeframes(self, mock_input):
        """Test duplicates analysis with multi-timeframe datasets."""
        result = self.eda_analyzer.run_duplicates_analysis(self.mock_system)
        
        assert result is True
    
    def test_duplicate_detection_types(self):
        """Test different types of duplicate detection."""
        # Test exact duplicates
        result = self.eda_analyzer.duplicates_analyzer.duplicate_detection._analyze_duplicates(self.main_data)
        
        # Should find exact duplicates
        assert result['exact_duplicates'] > 0
        
        # Should have timestamp columns
        assert len([col for col in self.main_data.columns if 'time' in col.lower()]) > 0
        
        # Should have OHLCV columns
        assert len([col for col in self.main_data.columns if col.upper() in ['OPEN', 'HIGH', 'LOW', 'CLOSE', 'VOLUME']]) > 0
    
    def test_empty_dataset(self):
        """Test analysis on empty dataset."""
        empty_df = pd.DataFrame()
        result = self.eda_analyzer.duplicates_analyzer.duplicate_detection._analyze_duplicates(empty_df)
        
        assert result['total_duplicates'] == 0
        assert result['duplicate_percent'] == 0
        assert result['exact_duplicates'] == 0
    
    def test_no_duplicates_dataset(self):
        """Test analysis on dataset with no duplicates."""
        # Create data with no duplicates
        clean_data = pd.DataFrame({
            'timestamp': pd.date_range('2024-01-01', periods=10, freq='1H'),
            'value': range(10)
        })
        
        result = self.eda_analyzer.duplicates_analyzer.duplicate_detection._analyze_duplicates(clean_data)
        
        assert result['total_duplicates'] == 0
        assert result['duplicate_percent'] == 0
        assert result['exact_duplicates'] == 0
    
    def test_timestamp_based_duplicates(self):
        """Test timestamp-based duplicate detection."""
        # Create data with timestamp duplicates
        ts_data = pd.DataFrame({
            'timestamp': ['2024-01-01 10:00:00', '2024-01-01 10:00:00', '2024-01-01 11:00:00'],
            'value': [100, 200, 300]
        })
        
        result = self.eda_analyzer.duplicates_analyzer.duplicate_detection._analyze_duplicates(ts_data)
        
        # Should find timestamp-based duplicates
        assert result['timestamp_based_duplicates'] > 0
        assert len(result['key_columns']) > 0
    
    def test_ohlcv_based_duplicates(self):
        """Test OHLCV-based duplicate detection."""
        # Create data with OHLCV duplicates
        ohlcv_data = pd.DataFrame({
            'timestamp': ['2024-01-01 10:00:00', '2024-01-01 11:00:00', '2024-01-01 12:00:00'],
            'open': [100, 100, 200],  # First two have same open
            'high': [110, 120, 130],
            'low': [90, 95, 100],
            'close': [105, 115, 125],
            'volume': [1000, 2000, 3000]
        })
    
        result = self.eda_analyzer.duplicates_analyzer.duplicate_detection._analyze_duplicates(ohlcv_data)
    
        # Should find OHLCV-based duplicates
        assert result['ohlcv_based_duplicates'] > 0
        assert len(result['ohlcv_duplicates']) > 0
    
    def test_business_logic_duplicates(self):
        """Test business logic duplicate detection (timestamp + OHLCV)."""
        # Create data with business logic duplicates
        bl_data = pd.DataFrame({
            'timestamp': ['2024-01-01 10:00:00', '2024-01-01 10:00:00', '2024-01-01 11:00:00'],
            'open': [100, 100, 200],  # Same timestamp and open for first two
            'high': [110, 120, 130],
            'low': [90, 95, 100],
            'close': [105, 115, 125],
            'volume': [1000, 2000, 3000]
        })
    
        result = self.eda_analyzer.duplicates_analyzer.duplicate_detection._analyze_duplicates(bl_data)
        
        # Should find business logic duplicates
        assert len(result['key_columns']) > 0
        
        # Check if business logic duplicates were found
        business_logic_found = any(
            'type' in col and col['type'] == 'business_logic' 
            for col in result['key_columns']
        )
        assert business_logic_found


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"])
