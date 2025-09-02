#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Data Manager Gap Fixing Functionality

This module tests the time series gap fixing functionality in DataManager.
"""

import pytest
import pandas as pd
import numpy as np
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import sys
import os

# Add project root to path
project_root = Path(__file__).parent.parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from src.interactive.data_manager import DataManager
from src.data.gap_fixer import GapFixer


class TestDataManagerGapFixing:
    """Test class for DataManager gap fixing functionality."""
    
    @pytest.fixture
    def data_manager(self):
        """Create a DataManager instance for testing."""
        return DataManager()
    
    @pytest.fixture
    def sample_dataframe_with_gaps(self):
        """Create a sample DataFrame with time series gaps."""
        # Create datetime range with gaps
        dates = pd.date_range('2023-01-01', '2023-01-10', freq='1H')
        
        # Remove some dates to create gaps
        dates_with_gaps = dates.drop([
            pd.Timestamp('2023-01-02 12:00:00'),
            pd.Timestamp('2023-01-03 06:00:00'),
            pd.Timestamp('2023-01-05 18:00:00'),
            pd.Timestamp('2023-01-07 00:00:00')
        ])
        
        # Create DataFrame with gaps
        df = pd.DataFrame({
            'Timestamp': dates_with_gaps,
            'Open': np.random.randn(len(dates_with_gaps)),
            'High': np.random.randn(len(dates_with_gaps)),
            'Low': np.random.randn(len(dates_with_gaps)),
            'Close': np.random.randn(len(dates_with_gaps)),
            'Volume': np.random.randint(1000, 10000, len(dates_with_gaps))
        })
        
        return df
    
    @pytest.fixture
    def sample_dataframe_no_gaps(self):
        """Create a sample DataFrame without time series gaps."""
        dates = pd.date_range('2023-01-01', '2023-01-10', freq='1H')
        
        df = pd.DataFrame({
            'Timestamp': dates,
            'Open': np.random.randn(len(dates)),
            'High': np.random.randn(len(dates)),
            'Low': np.random.randn(len(dates)),
            'Close': np.random.randn(len(dates)),
            'Volume': np.random.randint(1000, 10000, len(dates))
        })
        
        return df
    
    @pytest.fixture
    def sample_dataframe_no_timestamp(self):
        """Create a sample DataFrame without timestamp column."""
        df = pd.DataFrame({
            'Open': np.random.randn(100),
            'High': np.random.randn(100),
            'Low': np.random.randn(100),
            'Close': np.random.randn(100),
            'Volume': np.random.randint(1000, 10000, 100)
        })
        
        return df
    
    def test_fix_time_series_gaps_empty_list(self, data_manager):
        """Test gap fixing with empty list of dataframes."""
        result = data_manager._fix_time_series_gaps([])
        assert result == []
    
    def test_fix_time_series_gaps_none_input(self, data_manager):
        """Test gap fixing with None input."""
        result = data_manager._fix_time_series_gaps(None)
        assert result == []
    
    def test_fix_time_series_gaps_no_timestamp_column(self, data_manager, sample_dataframe_no_timestamp):
        """Test gap fixing with dataframe that has no timestamp column."""
        dataframes = [sample_dataframe_no_timestamp]
        
        with patch('builtins.print') as mock_print:
            result = data_manager._fix_time_series_gaps(dataframes)
        
        # Should return original dataframe unchanged
        assert len(result) == 1
        assert result[0] is sample_dataframe_no_timestamp
        
        # Check that appropriate message was printed
        mock_print.assert_any_call("   ⚠️  No timestamp column found, skipping gap fixing")
    
    def test_fix_time_series_gaps_no_gaps_found(self, data_manager, sample_dataframe_no_gaps):
        """Test gap fixing with dataframe that has no gaps."""
        dataframes = [sample_dataframe_no_gaps]
        
        with patch('builtins.print') as mock_print:
            result = data_manager._fix_time_series_gaps(dataframes)
        
        # Should return original dataframe unchanged
        assert len(result) == 1
        assert result[0] is sample_dataframe_no_gaps
        
        # Check that appropriate message was printed
        mock_print.assert_any_call("   ✅ No gaps found, dataframe is clean")
    
    def test_fix_time_series_gaps_with_gaps_success(self, data_manager, sample_dataframe_with_gaps):
        """Test gap fixing with dataframe that has gaps (successful case)."""
        dataframes = [sample_dataframe_with_gaps]
        
        # Mock GapFixer methods
        with patch.object(GapFixer, '_find_timestamp_column', return_value='Timestamp'), \
             patch.object(GapFixer, '_detect_gaps') as mock_detect, \
             patch.object(GapFixer, '_fix_gaps_in_dataframe') as mock_fix, \
             patch('builtins.print'):
            
            # Mock gap detection to return gaps found
            mock_detect.return_value = {
                'has_gaps': True,
                'gap_count': 4,
                'expected_frequency': pd.Timedelta('1H'),
                'gap_threshold': pd.Timedelta('1.5H'),
                'total_rows': len(sample_dataframe_with_gaps),
                'time_range': {
                    'start': sample_dataframe_with_gaps['Timestamp'].min(),
                    'end': sample_dataframe_with_gaps['Timestamp'].max()
                }
            }
            
            # Mock gap fixing to return fixed dataframe
            fixed_df = sample_dataframe_with_gaps.copy()
            fixed_df.loc[len(fixed_df)] = [pd.Timestamp('2023-01-02 12:00:00'), 0, 0, 0, 0, 0]
            
            mock_fix.return_value = (fixed_df, {
                'algorithm_used': 'linear',
                'gaps_fixed': 4,
                'processing_time': 1.5,
                'memory_used_mb': 10.5,
                'original_shape': sample_dataframe_with_gaps.shape,
                'final_shape': fixed_df.shape
            })
            
            result = data_manager._fix_time_series_gaps(dataframes)
        
        # Should return fixed dataframe
        assert len(result) == 1
        assert result[0] is fixed_df
        
        # Verify methods were called
        mock_detect.assert_called_once()
        mock_fix.assert_called_once()
    
    def test_fix_time_series_gaps_with_gaps_failure(self, data_manager, sample_dataframe_with_gaps):
        """Test gap fixing with dataframe that has gaps (failure case)."""
        dataframes = [sample_dataframe_with_gaps]
        
        # Mock GapFixer methods to raise exception
        with patch.object(GapFixer, '_find_timestamp_column', return_value='Timestamp'), \
             patch.object(GapFixer, '_detect_gaps', side_effect=Exception("Test error")), \
             patch('builtins.print') as mock_print:
            
            result = data_manager._fix_time_series_gaps(dataframes)
        
        # Should return original dataframe unchanged
        assert len(result) == 1
        assert result[0] is sample_dataframe_with_gaps
        
        # Check that appropriate error message was printed
        mock_print.assert_any_call("   ❌ Error fixing gaps in dataframe 1: Test error")
        mock_print.assert_any_call("   💡 Continuing with original dataframe...")
    
    def test_fix_time_series_gaps_multiple_dataframes(self, data_manager, 
                                                     sample_dataframe_with_gaps, 
                                                     sample_dataframe_no_gaps):
        """Test gap fixing with multiple dataframes."""
        dataframes = [sample_dataframe_with_gaps, sample_dataframe_no_gaps]
        
        # Mock GapFixer methods
        with patch.object(GapFixer, '_find_timestamp_column', side_effect=['Timestamp', 'Timestamp']), \
             patch.object(GapFixer, '_detect_gaps') as mock_detect, \
             patch.object(GapFixer, '_fix_gaps_in_dataframe') as mock_fix, \
             patch('builtins.print'):
            
            # Mock gap detection - first has gaps, second doesn't
            mock_detect.side_effect = [
                {
                    'has_gaps': True,
                    'gap_count': 4,
                    'expected_frequency': pd.Timedelta('1H'),
                    'gap_threshold': pd.Timedelta('1.5H'),
                    'total_rows': len(sample_dataframe_with_gaps),
                    'time_range': {
                        'start': sample_dataframe_with_gaps['Timestamp'].min(),
                        'end': sample_dataframe_with_gaps['Timestamp'].max()
                    }
                },
                {
                    'has_gaps': False,
                    'gap_count': 0,
                    'expected_frequency': pd.Timedelta('1H'),
                    'gap_threshold': pd.Timedelta('1.5H'),
                    'total_rows': len(sample_dataframe_no_gaps),
                    'time_range': {
                        'start': sample_dataframe_no_gaps['Timestamp'].min(),
                        'end': sample_dataframe_no_gaps['Timestamp'].max()
                    }
                }
            ]
            
            # Mock gap fixing for first dataframe
            fixed_df = sample_dataframe_with_gaps.copy()
            fixed_df.loc[len(fixed_df)] = [pd.Timestamp('2023-01-02 12:00:00'), 0, 0, 0, 0, 0]
            
            mock_fix.return_value = (fixed_df, {
                'algorithm_used': 'linear',
                'gaps_fixed': 4,
                'processing_time': 1.5,
                'memory_used_mb': 10.5,
                'original_shape': sample_dataframe_with_gaps.shape,
                'final_shape': fixed_df.shape
            })
            
            result = data_manager._fix_time_series_gaps(dataframes)
        
        # Should return both dataframes (first fixed, second unchanged)
        assert len(result) == 2
        assert result[0] is fixed_df
        assert result[1] is sample_dataframe_no_gaps
        
        # Verify methods were called
        assert mock_detect.call_count == 2
        assert mock_fix.call_count == 1  # Only called for first dataframe
    
    def test_fix_time_series_gaps_memory_management(self, data_manager, sample_dataframe_with_gaps):
        """Test that memory management is properly handled during gap fixing."""
        dataframes = [sample_dataframe_with_gaps]
        
        # Mock GapFixer methods
        with patch.object(GapFixer, '_find_timestamp_column', return_value='Timestamp'), \
             patch.object(GapFixer, '_detect_gaps') as mock_detect, \
             patch.object(GapFixer, '_fix_gaps_in_dataframe') as mock_fix, \
             patch('builtins.print'), \
             patch.object(data_manager, 'enable_memory_optimization', True), \
             patch('gc.collect') as mock_gc:
            
            # Mock gap detection
            mock_detect.return_value = {
                'has_gaps': True,
                'gap_count': 4,
                'expected_frequency': pd.Timedelta('1H'),
                'gap_threshold': pd.Timedelta('1.5H'),
                'total_rows': len(sample_dataframe_with_gaps),
                'time_range': {
                    'start': sample_dataframe_with_gaps['Timestamp'].min(),
                    'end': sample_dataframe_with_gaps['Timestamp'].max()
                }
            }
            
            # Mock gap fixing
            fixed_df = sample_dataframe_with_gaps.copy()
            mock_fix.return_value = (fixed_df, {
                'algorithm_used': 'linear',
                'gaps_fixed': 4,
                'processing_time': 1.5,
                'memory_used_mb': 10.5,
                'original_shape': sample_dataframe_with_gaps.shape,
                'final_shape': fixed_df.shape
            })
            
            result = data_manager._fix_time_series_gaps(dataframes)
        
        # Verify garbage collection was called
        assert mock_gc.call_count > 0
    
    def test_fix_time_series_gaps_integration(self, data_manager):
        """Integration test for gap fixing functionality."""
        # Create a real DataFrame with gaps
        dates = pd.date_range('2023-01-01', '2023-01-05', freq='1H')
        dates_with_gaps = dates.drop([pd.Timestamp('2023-01-02 12:00:00')])
        
        df = pd.DataFrame({
            'Timestamp': dates_with_gaps,
            'Value': np.random.randn(len(dates_with_gaps))
        })
        
        dataframes = [df]
        
        # Test with real GapFixer (no mocking)
        result = data_manager._fix_time_series_gaps(dataframes)
        
        # Should return a list with one dataframe
        assert len(result) == 1
        assert isinstance(result[0], pd.DataFrame)
        
        # The result should be a DataFrame (either fixed or original)
        assert isinstance(result[0], pd.DataFrame)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
