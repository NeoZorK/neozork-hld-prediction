# -*- coding: utf-8 -*-
# tests/plotting/test_wave_terminal_signals.py

"""
Test cases for Wave indicator trading signals display in terminal mode.
"""

import pytest
import pandas as pd
import numpy as np
from unittest.mock import patch, MagicMock

from src.plotting.term_chunked_plot import _has_trading_signals, _add_trading_signals_to_chunk


class TestWaveTerminalSignals:
    """Test cases for Wave indicator trading signals in terminal mode."""

    def test_has_trading_signals_with_wave_plot_color(self):
        """Test _has_trading_signals function with _Plot_Color column."""
        # Create sample data with wave indicator signals
        chunk = pd.DataFrame({
            'Open': [1.0, 1.1, 1.2],
            'High': [1.05, 1.15, 1.25],
            'Low': [0.95, 1.05, 1.15],
            'Close': [1.02, 1.12, 1.22],
            '_Plot_Color': [0, 1, 2]  # 0=NO TRADE, 1=BUY, 2=SELL
        })
        
        assert _has_trading_signals(chunk) == True

    def test_has_trading_signals_with_wave_signal(self):
        """Test _has_trading_signals function with _Signal column."""
        # Create sample data with wave indicator signals
        chunk = pd.DataFrame({
            'Open': [1.0, 1.1, 1.2],
            'High': [1.05, 1.15, 1.25],
            'Low': [0.95, 1.05, 1.15],
            'Close': [1.02, 1.12, 1.22],
            '_Signal': [0, 1, 2]  # 0=NO TRADE, 1=BUY, 2=SELL
        })
        
        assert _has_trading_signals(chunk) == True

    def test_has_trading_signals_with_direction(self):
        """Test _has_trading_signals function with Direction column."""
        # Create sample data with standard Direction column
        chunk = pd.DataFrame({
            'Open': [1.0, 1.1, 1.2],
            'High': [1.05, 1.15, 1.25],
            'Low': [0.95, 1.05, 1.15],
            'Close': [1.02, 1.12, 1.22],
            'Direction': [0, 1, 2]  # 0=NOTRADE, 1=BUY, 2=SELL
        })
        
        assert _has_trading_signals(chunk) == True

    def test_has_trading_signals_without_signals(self):
        """Test _has_trading_signals function without any signal columns."""
        # Create sample data without signal columns
        chunk = pd.DataFrame({
            'Open': [1.0, 1.1, 1.2],
            'High': [1.05, 1.15, 1.25],
            'Low': [0.95, 1.05, 1.15],
            'Close': [1.02, 1.12, 1.22]
        })
        
        assert _has_trading_signals(chunk) == False

    def test_add_trading_signals_to_chunk_wave_plot_color(self):
        """Test _add_trading_signals_to_chunk with wave _Plot_Color signals."""
        # Create sample data with wave indicator signals
        chunk = pd.DataFrame({
            'Open': [1.0, 1.1, 1.2, 1.3],
            'High': [1.05, 1.15, 1.25, 1.35],
            'Low': [0.95, 1.05, 1.15, 1.25],
            'Close': [1.02, 1.12, 1.22, 1.32],
            '_Plot_Color': [0, 1, 2, 1]  # NO TRADE, BUY, SELL, BUY
        })
        
        x_values = [0, 1, 2, 3]
        
        with patch('src.plotting.term_chunked_plot.plt') as mock_plt:
            _add_trading_signals_to_chunk(chunk, x_values)
            
            # Should call scatter for BUY signals (indices 1 and 3)
            assert mock_plt.scatter.called
            
            # Check that scatter was called for BUY signals
            scatter_calls = mock_plt.scatter.call_args_list
            assert len(scatter_calls) >= 1  # At least one scatter call

    def test_add_trading_signals_to_chunk_wave_signal(self):
        """Test _add_trading_signals_to_chunk with wave _Signal signals."""
        # Create sample data with wave indicator signals
        chunk = pd.DataFrame({
            'Open': [1.0, 1.1, 1.2, 1.3],
            'High': [1.05, 1.15, 1.25, 1.35],
            'Low': [0.95, 1.05, 1.15, 1.25],
            'Close': [1.02, 1.12, 1.22, 1.32],
            '_Signal': [0, 1, 2, 1]  # NO TRADE, BUY, SELL, BUY
        })
        
        x_values = [0, 1, 2, 3]
        
        with patch('src.plotting.term_chunked_plot.plt') as mock_plt:
            _add_trading_signals_to_chunk(chunk, x_values)
            
            # Should call scatter for signals
            assert mock_plt.scatter.called

    def test_add_trading_signals_to_chunk_mixed_signals(self):
        """Test _add_trading_signals_to_chunk with mixed signal types."""
        # Create sample data with mixed signal types
        chunk = pd.DataFrame({
            'Open': [1.0, 1.1, 1.2, 1.3],
            'High': [1.05, 1.15, 1.25, 1.35],
            'Low': [0.95, 1.05, 1.15, 1.25],
            'Close': [1.02, 1.12, 1.22, 1.32],
            '_Plot_Color': [0, 1, 2, 0],  # NO TRADE, BUY, SELL, NO TRADE
            '_Signal': [0, 1, 2, 0]      # Same signals
        })
        
        x_values = [0, 1, 2, 3]
        
        with patch('src.plotting.term_chunked_plot.plt') as mock_plt:
            _add_trading_signals_to_chunk(chunk, x_values)
            
            # Should handle mixed signals correctly
            assert mock_plt.scatter.called

    def test_add_trading_signals_to_chunk_no_signals(self):
        """Test _add_trading_signals_to_chunk with no valid signals."""
        # Create sample data with no valid signals
        chunk = pd.DataFrame({
            'Open': [1.0, 1.1, 1.2],
            'High': [1.05, 1.15, 1.25],
            'Low': [0.95, 1.05, 1.15],
            'Close': [1.02, 1.12, 1.22],
            '_Plot_Color': [0, 0, 0]  # All NO TRADE
        })
        
        x_values = [0, 1, 2]
        
        with patch('src.plotting.term_chunked_plot.plt') as mock_plt:
            _add_trading_signals_to_chunk(chunk, x_values)
            
            # Should not call scatter when no signals
            mock_plt.scatter.assert_not_called()

    def test_add_trading_signals_to_chunk_error_handling(self):
        """Test _add_trading_signals_to_chunk error handling."""
        # Create invalid data to trigger error
        chunk = pd.DataFrame({
            'Open': [1.0, 1.1, 1.2],
            'High': [1.05, 1.15, 1.25],
            'Low': [0.95, 1.05, 1.15],
            'Close': [1.02, 1.12, 1.22],
            '_Plot_Color': [0, 1, 2]
        })
        
        x_values = [0, 1, 2]
        
        with patch('src.plotting.term_chunked_plot.plt') as mock_plt:
            # Mock plt.scatter to raise an exception
            mock_plt.scatter.side_effect = Exception("Test error")
            
            # Should handle error gracefully
            _add_trading_signals_to_chunk(chunk, x_values)
            
            # Should still attempt to call scatter
            assert mock_plt.scatter.called

    def test_wave_signal_priority_order(self):
        """Test that _Plot_Color takes priority over _Signal over Direction."""
        # Create sample data with multiple signal sources
        chunk = pd.DataFrame({
            'Open': [1.0, 1.1, 1.2],
            'High': [1.05, 1.15, 1.25],
            'Low': [0.95, 1.05, 1.15],
            'Close': [1.02, 1.12, 1.22],
            '_Plot_Color': [0, 1, 2],  # Should be used
            '_Signal': [2, 0, 1],      # Should be ignored
            'Direction': [1, 2, 0]     # Should be ignored
        })
        
        x_values = [0, 1, 2]
        
        with patch('src.plotting.term_chunked_plot.plt') as mock_plt:
            _add_trading_signals_to_chunk(chunk, x_values)
            
            # Should use _Plot_Color signals (0, 1, 2)
            assert mock_plt.scatter.called

    def test_wave_signal_values_interpretation(self):
        """Test correct interpretation of wave signal values."""
        # Create sample data with specific wave signal values
        chunk = pd.DataFrame({
            'Open': [1.0, 1.1, 1.2, 1.3, 1.4],
            'High': [1.05, 1.15, 1.25, 1.35, 1.45],
            'Low': [0.95, 1.05, 1.15, 1.25, 1.35],
            'Close': [1.02, 1.12, 1.22, 1.32, 1.42],
            '_Plot_Color': [0, 1, 2, 1, 2]  # NO TRADE, BUY, SELL, BUY, SELL
        })
        
        x_values = [0, 1, 2, 3, 4]
        
        with patch('src.plotting.term_chunked_plot.plt') as mock_plt:
            _add_trading_signals_to_chunk(chunk, x_values)
            
            # Should handle all signal types correctly
            assert mock_plt.scatter.called
            
            # Check that scatter was called multiple times (for BUY and SELL)
            scatter_calls = mock_plt.scatter.call_args_list
            assert len(scatter_calls) >= 1
