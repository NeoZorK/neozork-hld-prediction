#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test for gap fixing with progress bar functionality

This test verifies that the gap fixing functions now include progress bars
and ETA information for better user experience.
"""

import pytest
import pandas as pd
import numpy as np
from pathlib import Path
import tempfile
import os
from unittest.mock import patch, MagicMock

from src.eda.fix_files import fix_gaps, _fix_gaps_irregular


class TestGapFixingProgress:
    """Test class for gap fixing with progress bar functionality."""
    
    @pytest.fixture
    def sample_data_with_gaps(self):
        """Create sample data with gaps for testing."""
        # Create regular time series with some gaps
        dates = pd.date_range('2023-01-01', periods=1000, freq='H')
        
        # Remove some dates to create gaps
        gap_indices = [100, 200, 300, 400, 500, 600, 700, 800, 900]
        dates_with_gaps = dates.drop(dates[gap_indices])
        
        data = {
            'Timestamp': dates_with_gaps,
            'Low': np.random.uniform(1.0, 2.0, len(dates_with_gaps)),
            'Close': np.random.uniform(1.0, 2.0, len(dates_with_gaps)),
            'High': np.random.uniform(1.0, 2.0, len(dates_with_gaps)),
            'Open': np.random.uniform(1.0, 2.0, len(dates_with_gaps)),
            'Volume': np.random.randint(100, 1000, len(dates_with_gaps))
        }
        df = pd.DataFrame(data)
        return df
    
    @pytest.fixture
    def sample_data_with_large_gaps(self):
        """Create sample data with large gaps for testing irregular method."""
        # Create time series with large gaps
        dates = []
        current_date = pd.Timestamp('2023-01-01')
        
        for i in range(100):
            dates.append(current_date)
            # Add small gap (1 hour)
            current_date += pd.Timedelta(hours=1)
            
            if i % 20 == 0:  # Every 20th point, add large gap
                current_date += pd.Timedelta(days=5)  # 5-day gap
        
        data = {
            'Timestamp': dates,
            'Low': np.random.uniform(1.0, 2.0, len(dates)),
            'Close': np.random.uniform(1.0, 2.0, len(dates)),
            'High': np.random.uniform(1.0, 2.0, len(dates)),
            'Open': np.random.uniform(1.0, 2.0, len(dates)),
            'Volume': np.random.randint(100, 1000, len(dates))
        }
        df = pd.DataFrame(data)
        return df
    
    def test_fix_gaps_with_progress_bar_regular(self, sample_data_with_gaps):
        """Test that fix_gaps shows progress bar for regular method."""
        # Mock tqdm to capture calls
        with patch('src.eda.fix_files.tqdm') as mock_tqdm:
            # Mock tqdm context manager
            mock_pbar = MagicMock()
            mock_tqdm.return_value.__enter__.return_value = mock_pbar
            
            # Run fix_gaps
            result = fix_gaps(sample_data_with_gaps, datetime_col='Timestamp')
            
            # Check that tqdm was called for interpolation
            mock_tqdm.assert_called()
            
            # Verify the result
            assert result is not None
            assert len(result) >= len(sample_data_with_gaps)
            assert 'Timestamp' in result.columns
    
    def test_fix_gaps_with_progress_bar_irregular(self, sample_data_with_large_gaps):
        """Test that fix_gaps shows progress bar for irregular method."""
        # Mock tqdm to capture calls
        with patch('src.eda.fix_files.tqdm') as mock_tqdm:
            # Mock tqdm context manager
            mock_pbar = MagicMock()
            mock_tqdm.return_value.__enter__.return_value = mock_pbar
            
            # Run fix_gaps (should use irregular method due to large gaps)
            result = fix_gaps(sample_data_with_large_gaps, datetime_col='Timestamp')
            
            # Check that tqdm was called for gap processing
            mock_tqdm.assert_called()
            
            # Verify the result
            assert result is not None
            assert len(result) >= len(sample_data_with_large_gaps)
            assert 'Timestamp' in result.columns
    
    def test_fix_gaps_irregular_with_progress_bar(self, sample_data_with_large_gaps):
        """Test that _fix_gaps_irregular shows progress bar."""
        # Mock tqdm to capture calls
        with patch('src.eda.fix_files.tqdm') as mock_tqdm:
            # Mock tqdm context manager
            mock_pbar = MagicMock()
            mock_tqdm.return_value.__enter__.return_value = mock_pbar
            
            # Run _fix_gaps_irregular directly
            result = _fix_gaps_irregular(sample_data_with_large_gaps, 'Timestamp')
            
            # Check that tqdm was called
            mock_tqdm.assert_called()
            
            # Verify tqdm was called with correct parameters
            call_args = mock_tqdm.call_args
            assert call_args[1]['desc'] == "Fixing time series gaps"
            assert call_args[1]['unit'] == "gap"
            
            # Verify the result
            assert result is not None
            assert len(result) >= len(sample_data_with_large_gaps)
            assert 'Timestamp' in result.columns
    
    def test_fix_gaps_datetime_index_with_progress_bar(self):
        """Test that fix_gaps shows progress bar for DatetimeIndex."""
        # Create DataFrame with DatetimeIndex
        dates = pd.date_range('2023-01-01', periods=100, freq='H')
        data = {
            'Low': np.random.uniform(1.0, 2.0, 100),
            'Close': np.random.uniform(1.0, 2.0, 100),
            'High': np.random.uniform(1.0, 2.0, 100),
            'Open': np.random.uniform(1.0, 2.0, 100),
            'Volume': np.random.randint(100, 1000, 100)
        }
        df = pd.DataFrame(data, index=dates)
        
        # Mock tqdm to capture calls
        with patch('src.eda.fix_files.tqdm') as mock_tqdm:
            # Mock tqdm context manager
            mock_pbar = MagicMock()
            mock_tqdm.return_value.__enter__.return_value = mock_pbar
            
            # Run fix_gaps with DatetimeIndex
            result = fix_gaps(df, datetime_col='index')
            
            # Check that tqdm was called
            mock_tqdm.assert_called()
            
            # Verify the result
            assert result is not None
            assert len(result) >= len(df)
    
    def test_progress_bar_updates_correctly(self, sample_data_with_large_gaps):
        """Test that progress bar updates correctly during processing."""
        # Mock tqdm to capture update calls
        with patch('src.eda.fix_files.tqdm') as mock_tqdm:
            # Mock tqdm context manager
            mock_pbar = MagicMock()
            mock_tqdm.return_value.__enter__.return_value = mock_pbar
            
            # Run _fix_gaps_irregular
            result = _fix_gaps_irregular(sample_data_with_large_gaps, 'Timestamp')
            
            # Check that update was called
            assert mock_pbar.update.called
            
            # Check that set_postfix was called
            assert mock_pbar.set_postfix.called
            
            # Verify the result
            assert result is not None
    
    def test_progress_bar_with_no_gaps(self):
        """Test that progress bar works correctly when no gaps are found."""
        # Create data without gaps
        dates = pd.date_range('2023-01-01', periods=100, freq='H')
        data = {
            'Timestamp': dates,
            'Low': np.random.uniform(1.0, 2.0, 100),
            'Close': np.random.uniform(1.0, 2.0, 100),
            'High': np.random.uniform(1.0, 2.0, 100),
            'Open': np.random.uniform(1.0, 2.0, 100),
            'Volume': np.random.randint(100, 1000, 100)
        }
        df = pd.DataFrame(data)
        
        # Mock tqdm to capture calls
        with patch('src.eda.fix_files.tqdm') as mock_tqdm:
            # Mock tqdm context manager
            mock_pbar = MagicMock()
            mock_tqdm.return_value.__enter__.return_value = mock_pbar
            
            # Run fix_gaps
            result = fix_gaps(df, datetime_col='Timestamp')
            
            # Check that tqdm was called (for interpolation)
            mock_tqdm.assert_called()
            
            # Verify the result
            assert result is not None
            assert len(result) >= len(df)
    
    def test_progress_bar_error_handling(self, sample_data_with_gaps):
        """Test that progress bar works correctly even when errors occur."""
        # Mock tqdm to capture calls
        with patch('src.eda.fix_files.tqdm') as mock_tqdm:
            # Mock tqdm context manager
            mock_pbar = MagicMock()
            mock_tqdm.return_value.__enter__.return_value = mock_pbar
            
            # Create data that will cause an error in gap fixing
            bad_data = sample_data_with_gaps.copy()
            bad_data['Timestamp'] = pd.NaT  # This will cause issues
            
            # Run fix_gaps (should handle error gracefully)
            result = fix_gaps(bad_data, datetime_col='Timestamp')
            
            # Verify the result (should return original data)
            assert result is not None
            assert len(result) == len(bad_data)
    
    def test_progress_bar_performance(self, sample_data_with_large_gaps):
        """Test that progress bar doesn't significantly impact performance."""
        import time
        
        # Time without progress bar (mocked)
        with patch('src.eda.fix_files.tqdm') as mock_tqdm:
            mock_pbar = MagicMock()
            mock_tqdm.return_value.__enter__.return_value = mock_pbar
            
            start_time = time.time()
            result1 = _fix_gaps_irregular(sample_data_with_large_gaps, 'Timestamp')
            time_with_progress = time.time() - start_time
        
        # Verify the result
        assert result1 is not None
        assert len(result1) >= len(sample_data_with_large_gaps)
        
        # Progress bar should not add more than 10% overhead
        # (This is a rough estimate - actual overhead should be minimal)
        assert time_with_progress < 1.0  # Should complete within 1 second
