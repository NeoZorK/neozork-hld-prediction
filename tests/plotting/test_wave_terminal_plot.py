# -*- coding: utf-8 -*-
# tests/plotting/test_wave_terminal_plot.py

"""
Test cases for Wave indicator terminal plotting support.
"""

import pytest
import pandas as pd
import numpy as np
from unittest.mock import patch, MagicMock

from src.plotting.term_chunked_plot import _add_wave_indicator_to_subplot


class TestWaveTerminalPlot:
    """Test cases for Wave indicator terminal plotting."""

    def test_add_wave_indicator_to_subplot_basic(self):
        """Test basic wave indicator plotting functionality."""
        # Create sample data
        dates = pd.date_range('2023-01-01', periods=50, freq='D')
        chunk = pd.DataFrame({
            'Open': np.random.uniform(1.0, 2.0, 50),
            'High': np.random.uniform(1.0, 2.0, 50),
            'Low': np.random.uniform(1.0, 2.0, 50),
            'Close': np.random.uniform(1.0, 2.0, 50),
            '_Plot_Wave': np.random.uniform(-0.1, 0.1, 50),
            '_Plot_Color': np.random.choice([0, 1, 2], 50),
            '_Plot_FastLine': np.random.uniform(-0.05, 0.05, 50),
            'MA_Line': np.random.uniform(-0.02, 0.02, 50)
        }, index=dates)
        
        x_values = list(range(len(chunk)))
        
        # Mock plotext
        with patch('src.plotting.term_chunked_plot.plt') as mock_plt:
            _add_wave_indicator_to_subplot(chunk, x_values)
            
            # Verify that plot was called
            assert mock_plt.plot.called

    def test_add_wave_indicator_to_subplot_with_buy_signals(self):
        """Test wave indicator plotting with BUY signals."""
        dates = pd.date_range('2023-01-01', periods=20, freq='D')
        chunk = pd.DataFrame({
            'Open': np.random.uniform(1.0, 2.0, 20),
            'High': np.random.uniform(1.0, 2.0, 20),
            'Low': np.random.uniform(1.0, 2.0, 20),
            'Close': np.random.uniform(1.0, 2.0, 20),
            '_Plot_Wave': np.random.uniform(0.01, 0.1, 20),  # Positive values
            '_Plot_Color': [1] * 20,  # All BUY signals
            '_Plot_FastLine': np.random.uniform(-0.05, 0.05, 20),
            'MA_Line': np.random.uniform(-0.02, 0.02, 20)
        }, index=dates)
        
        x_values = list(range(len(chunk)))
        
        with patch('src.plotting.term_chunked_plot.plt') as mock_plt:
            _add_wave_indicator_to_subplot(chunk, x_values)
            
            # Check that plot was called for BUY signals
            plot_calls = mock_plt.plot.call_args_list
            buy_plot_calls = [call for call in plot_calls if 'Wave (BUY)' in str(call)]
            assert len(buy_plot_calls) > 0

    def test_add_wave_indicator_to_subplot_with_sell_signals(self):
        """Test wave indicator plotting with SELL signals."""
        dates = pd.date_range('2023-01-01', periods=20, freq='D')
        chunk = pd.DataFrame({
            'Open': np.random.uniform(1.0, 2.0, 20),
            'High': np.random.uniform(1.0, 2.0, 20),
            'Low': np.random.uniform(1.0, 2.0, 20),
            'Close': np.random.uniform(1.0, 2.0, 20),
            '_Plot_Wave': np.random.uniform(-0.1, -0.01, 20),  # Negative values
            '_Plot_Color': [2] * 20,  # All SELL signals
            '_Plot_FastLine': np.random.uniform(-0.05, 0.05, 20),
            'MA_Line': np.random.uniform(-0.02, 0.02, 20)
        }, index=dates)
        
        x_values = list(range(len(chunk)))
        
        with patch('src.plotting.term_chunked_plot.plt') as mock_plt:
            _add_wave_indicator_to_subplot(chunk, x_values)
            
            # Check that plot was called for SELL signals
            plot_calls = mock_plt.plot.call_args_list
            sell_plot_calls = [call for call in plot_calls if 'Wave (SELL)' in str(call)]
            assert len(sell_plot_calls) > 0

    def test_add_wave_indicator_to_subplot_missing_columns(self):
        """Test wave indicator plotting with missing columns."""
        dates = pd.date_range('2023-01-01', periods=10, freq='D')
        chunk = pd.DataFrame({
            'Open': np.random.uniform(1.0, 2.0, 10),
            'High': np.random.uniform(1.0, 2.0, 10),
            'Low': np.random.uniform(1.0, 2.0, 10),
            'Close': np.random.uniform(1.0, 2.0, 10)
            # Missing wave columns
        }, index=dates)
        
        x_values = list(range(len(chunk)))
        
        with patch('src.plotting.term_chunked_plot.plt') as mock_plt:
            _add_wave_indicator_to_subplot(chunk, x_values)
            
            # Should still work without errors
            assert True

    def test_add_wave_indicator_to_subplot_different_column_names(self):
        """Test wave indicator plotting with different column naming conventions."""
        dates = pd.date_range('2023-01-01', periods=15, freq='D')
        chunk = pd.DataFrame({
            'Open': np.random.uniform(1.0, 2.0, 15),
            'High': np.random.uniform(1.0, 2.0, 15),
            'Low': np.random.uniform(1.0, 2.0, 15),
            'Close': np.random.uniform(1.0, 2.0, 15),
            '_plot_wave': np.random.uniform(-0.1, 0.1, 15),  # Lowercase
            '_plot_color': np.random.choice([0, 1, 2], 15),  # Lowercase
            '_plot_fastline': np.random.uniform(-0.05, 0.05, 15),  # Lowercase
        }, index=dates)
        
        x_values = list(range(len(chunk)))
        
        with patch('src.plotting.term_chunked_plot.plt') as mock_plt:
            _add_wave_indicator_to_subplot(chunk, x_values)
            
            # Should work with lowercase column names
            assert mock_plt.plot.called

    def test_add_wave_indicator_to_subplot_zero_values(self):
        """Test wave indicator plotting with zero values."""
        dates = pd.date_range('2023-01-01', periods=10, freq='D')
        chunk = pd.DataFrame({
            'Open': np.random.uniform(1.0, 2.0, 10),
            'High': np.random.uniform(1.0, 2.0, 10),
            'Low': np.random.uniform(1.0, 2.0, 10),
            'Close': np.random.uniform(1.0, 2.0, 10),
            '_Plot_Wave': [0.0] * 10,  # All zeros
            '_Plot_Color': [0] * 10,   # No trade signals
            '_Plot_FastLine': [0.0] * 10,
            'MA_Line': [0.0] * 10
        }, index=dates)
        
        x_values = list(range(len(chunk)))
        
        with patch('src.plotting.term_chunked_plot.plt') as mock_plt:
            _add_wave_indicator_to_subplot(chunk, x_values)
            
            # Should still work with zero values
            assert True

    def test_add_wave_indicator_to_subplot_mixed_signals(self):
        """Test wave indicator plotting with mixed BUY/SELL signals."""
        dates = pd.date_range('2023-01-01', periods=30, freq='D')
        chunk = pd.DataFrame({
            'Open': np.random.uniform(1.0, 2.0, 30),
            'High': np.random.uniform(1.0, 2.0, 30),
            'Low': np.random.uniform(1.0, 2.0, 30),
            'Close': np.random.uniform(1.0, 2.0, 30),
            '_Plot_Wave': np.random.uniform(-0.1, 0.1, 30),
            '_Plot_Color': [1, 2, 0, 1, 2, 0, 1, 2, 0, 1, 2, 0, 1, 2, 0, 1, 2, 0, 1, 2, 0, 1, 2, 0, 1, 2, 0, 1, 2, 0],  # Mixed signals
            '_Plot_FastLine': np.random.uniform(-0.05, 0.05, 30),
            'MA_Line': np.random.uniform(-0.02, 0.02, 30)
        }, index=dates)
        
        x_values = list(range(len(chunk)))
        
        with patch('src.plotting.term_chunked_plot.plt') as mock_plt:
            _add_wave_indicator_to_subplot(chunk, x_values)
            
            # Should handle mixed signals correctly
            assert mock_plt.plot.called
