# -*- coding: utf-8 -*-
# tests/plotting/test_dual_chart_seaborn.py

"""
Tests for dual chart seaborn plotting functionality.
"""

import pytest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

from src.plotting.dual_chart_seaborn import plot_dual_chart_seaborn


class TestDualChartSeaborn:
    """Test class for dual chart seaborn plotting."""
    
    @pytest.fixture
    def sample_data(self):
        """Create sample OHLCV data with Stochastic indicator."""
        dates = pd.date_range(start='2023-01-01', periods=100, freq='D')
        
        # Create sample OHLCV data
        data = {
            'Open': np.random.uniform(1.0, 2.0, 100),
            'High': np.random.uniform(1.1, 2.1, 100),
            'Low': np.random.uniform(0.9, 1.9, 100),
            'Close': np.random.uniform(1.0, 2.0, 100),
            'Volume': np.random.randint(1000, 10000, 100),
        }
        
        # Ensure High >= Low and High >= Open, Close and Low <= Open, Close
        for i in range(100):
            data['High'][i] = max(data['Open'][i], data['Close'][i], data['High'][i])
            data['Low'][i] = min(data['Open'][i], data['Close'][i], data['Low'][i])
        
        df = pd.DataFrame(data, index=dates)
        
        # Add Stochastic indicator data
        df['stoch_k'] = np.random.uniform(0, 100, 100)
        df['stoch_d'] = np.random.uniform(0, 100, 100)
        df['stoch_overbought'] = 80
        df['stoch_oversold'] = 20
        
        return df
    
    def test_stoch_indicator_processing(self, sample_data, tmp_path):
        """Test that Stochastic indicator is properly processed in seaborn mode."""
        output_path = tmp_path / "test_stoch_seaborn.png"
        
        # Test that the function runs without errors
        try:
            fig = plot_dual_chart_seaborn(
                df=sample_data,
                rule='stoch:14,3,close',
                title='Test Stochastic Indicator',
                output_path=str(output_path),
                width=800,
                height=600
            )
            
            # Check that the figure was created
            assert fig is not None
            
            # Check that the output file was created
            assert output_path.exists()
            
        except Exception as e:
            pytest.fail(f"plot_dual_chart_seaborn failed with error: {e}")
    
    def test_stochoscillator_indicator_processing(self, sample_data, tmp_path):
        """Test that Stochastic Oscillator indicator is properly processed in seaborn mode."""
        output_path = tmp_path / "test_stochoscillator_seaborn.png"
        
        # Add Stochastic Oscillator data
        sample_data['stochosc_k'] = np.random.uniform(0, 100, 100)
        sample_data['stochosc_d'] = np.random.uniform(0, 100, 100)
        sample_data['stochosc_overbought'] = 80
        sample_data['stochosc_oversold'] = 20
        
        # Test that the function runs without errors
        try:
            fig = plot_dual_chart_seaborn(
                df=sample_data,
                rule='stochoscillator:14,3,close',
                title='Test Stochastic Oscillator Indicator',
                output_path=str(output_path),
                width=800,
                height=600
            )
            
            # Check that the figure was created
            assert fig is not None
            
            # Check that the output file was created
            assert output_path.exists()
            
        except Exception as e:
            pytest.fail(f"plot_dual_chart_seaborn failed with error: {e}")
    
    def test_missing_stoch_columns_handling(self, sample_data, tmp_path):
        """Test that missing Stochastic columns are handled gracefully."""
        output_path = tmp_path / "test_missing_stoch_seaborn.png"
        
        # Remove Stochastic columns
        sample_data = sample_data.drop(['stoch_k', 'stoch_d', 'stoch_overbought', 'stoch_oversold'], axis=1)
        
        # Test that the function runs without errors even with missing columns
        try:
            fig = plot_dual_chart_seaborn(
                df=sample_data,
                rule='stoch:14,3,close',
                title='Test Missing Stochastic Columns',
                output_path=str(output_path),
                width=800,
                height=600
            )
            
            # Check that the figure was created
            assert fig is not None
            
        except Exception as e:
            pytest.fail(f"plot_dual_chart_seaborn failed with error: {e}") 