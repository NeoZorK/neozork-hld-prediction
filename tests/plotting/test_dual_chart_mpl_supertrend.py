# -*- coding: utf-8 -*-
# tests/plotting/test_dual_chart_mpl_supertrend.py

"""
Test SuperTrend indicator display in dual_chart_mpl.py
"""

import pytest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock

from src.plotting.dual_chart_mpl import plot_dual_chart_mpl


class TestDualChartMplSuperTrend:
    """Test SuperTrend indicator display in dual_chart_mpl.py"""
    
    @pytest.fixture
    def sample_data(self):
        """Create sample data with SuperTrend indicators"""
        dates = pd.date_range('2023-01-01', periods=100, freq='D')
        
        # Create sample OHLCV data
        data = {
            'Open': np.random.uniform(1.0, 2.0, 100),
            'High': np.random.uniform(1.1, 2.1, 100),
            'Low': np.random.uniform(0.9, 1.9, 100),
            'Close': np.random.uniform(1.0, 2.0, 100),
            'Volume': np.random.randint(1000, 10000, 100),
            'SuperTrend': np.random.uniform(1.0, 2.0, 100),
            'SuperTrend_Direction': np.random.choice([1, -1], 100),
            'SuperTrend_Signal': np.random.choice([0, 1, 2], 100),
            'PPrice1': np.random.uniform(1.0, 2.0, 100),
            'PPrice2': np.random.uniform(1.0, 2.0, 100),
            'Direction': np.random.choice([0, 1, 2], 100),
            'PColor1': np.ones(100),
            'PColor2': np.full(100, 2)
        }
        
        df = pd.DataFrame(data, index=dates)
        return df
    
    def test_supertrend_with_supertrend_columns(self, sample_data):
        """Test SuperTrend display when SuperTrend columns are available"""
        with patch('matplotlib.pyplot.show') as mock_show:
            with patch('matplotlib.pyplot.savefig') as mock_save:
                # Test with SuperTrend columns
                result = plot_dual_chart_mpl(
                    df=sample_data,
                    rule='supertrend:10,3,open',
                    title='Test SuperTrend'
                )
                
                # Verify that the function executed without errors
                assert result is not None
                mock_show.assert_called_once()
    
    def test_supertrend_with_pprice_columns(self, sample_data):
        """Test SuperTrend display when only PPrice1/PPrice2 columns are available"""
        # Remove SuperTrend columns to test fallback
        test_data = sample_data.drop(['SuperTrend', 'SuperTrend_Direction', 'SuperTrend_Signal'], axis=1)
        
        with patch('matplotlib.pyplot.show') as mock_show:
            with patch('matplotlib.pyplot.savefig') as mock_save:
                # Test with PPrice1/PPrice2 fallback
                result = plot_dual_chart_mpl(
                    df=test_data,
                    rule='supertrend:10,3,open',
                    title='Test SuperTrend Fallback'
                )
                
                # Verify that the function executed without errors
                assert result is not None
                mock_show.assert_called_once()
    
    def test_supertrend_signal_points(self, sample_data):
        """Test that SuperTrend signal points are displayed correctly"""
        # Create data with specific signals
        test_data = sample_data.copy()
        test_data['SuperTrend_Signal'] = 0  # No signals initially
        test_data.loc[test_data.index[10], 'SuperTrend_Signal'] = 1  # Buy signal
        test_data.loc[test_data.index[20], 'SuperTrend_Signal'] = 2  # Sell signal
        
        with patch('matplotlib.pyplot.show') as mock_show:
            with patch('matplotlib.pyplot.savefig') as mock_save:
                result = plot_dual_chart_mpl(
                    df=test_data,
                    rule='supertrend:10,3,open',
                    title='Test SuperTrend Signals'
                )
                
                # Verify that the function executed without errors
                assert result is not None
                mock_show.assert_called_once()
    
    def test_supertrend_trend_direction(self, sample_data):
        """Test SuperTrend trend direction visualization"""
        # Create data with clear trend direction
        test_data = sample_data.copy()
        test_data['SuperTrend_Direction'] = 1  # All uptrend
        test_data.loc[test_data.index[50:], 'SuperTrend_Direction'] = -1  # Downtrend after midpoint
        
        with patch('matplotlib.pyplot.show') as mock_show:
            with patch('matplotlib.pyplot.savefig') as mock_save:
                result = plot_dual_chart_mpl(
                    df=test_data,
                    rule='supertrend:10,3,open',
                    title='Test SuperTrend Trend Direction'
                )
                
                # Verify that the function executed without errors
                assert result is not None
                mock_show.assert_called_once()
    
    def test_supertrend_parameter_parsing(self, sample_data):
        """Test that SuperTrend parameters are parsed correctly"""
        with patch('matplotlib.pyplot.show') as mock_show:
            with patch('matplotlib.pyplot.savefig') as mock_save:
                # Test different parameter combinations
                result1 = plot_dual_chart_mpl(
                    df=sample_data,
                    rule='supertrend:10,3,open',
                    title='Test SuperTrend Open Price'
                )
                
                result2 = plot_dual_chart_mpl(
                    df=sample_data,
                    rule='supertrend:14,2.5,close',
                    title='Test SuperTrend Close Price'
                )
                
                # Verify that both function calls executed without errors
                assert result1 is not None
                assert result2 is not None
                assert mock_show.call_count == 2
    
    def test_supertrend_error_handling(self):
        """Test SuperTrend error handling with invalid data"""
        # Create minimal data without required columns
        dates = pd.date_range('2023-01-01', periods=10, freq='D')
        minimal_data = pd.DataFrame({
            'Open': np.random.uniform(1.0, 2.0, 10),
            'High': np.random.uniform(1.1, 2.1, 10),
            'Low': np.random.uniform(0.9, 1.9, 10),
            'Close': np.random.uniform(1.0, 2.0, 10),
            'Volume': np.random.randint(1000, 10000, 10)
        }, index=dates)
        
        with patch('matplotlib.pyplot.show') as mock_show:
            with patch('matplotlib.pyplot.savefig') as mock_save:
                # Should handle missing SuperTrend columns gracefully
                result = plot_dual_chart_mpl(
                    df=minimal_data,
                    rule='supertrend:10,3,open',
                    title='Test SuperTrend Minimal Data'
                )
                
                # Verify that the function executed without errors
                assert result is not None
                mock_show.assert_called_once()


if __name__ == '__main__':
    pytest.main([__file__]) 