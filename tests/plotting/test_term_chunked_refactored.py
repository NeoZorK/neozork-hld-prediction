# -*- coding: utf-8 -*-
# tests/plotting/test_term_chunked_refactored.py

"""
Tests for refactored terminal chunked plotting modules.
"""

import pytest
import pandas as pd
import numpy as np
from unittest.mock import patch, MagicMock

# Import the modules to test
try:
    from src.plotting.term_chunked_utils import (
        get_terminal_plot_size, calculate_optimal_chunk_size,
        split_dataframe_into_chunks, parse_rsi_rule, draw_ohlc_candles,
        create_time_axis, setup_plot_layout, clear_plot
    )
    from src.plotting.term_chunked_overlays import (
        _add_pv_overlays_to_chunk, _add_sr_overlays_to_chunk,
        _add_phld_overlays_to_chunk, _add_rsi_overlays_to_chunk
    )
    from src.plotting.term_chunked_statistics import (
        _show_chunk_statistics, _show_field_statistics
    )
    from src.plotting.term_chunked_plotters import (
        plot_ohlcv_chunks, plot_auto_chunks, plot_pv_chunks,
        plot_sr_chunks, plot_phld_chunks, plot_rsi_chunks,
        _plot_single_field_chunk
    )
    from src.plotting.term_chunked_plot import plot_chunked_terminal
except ImportError:
    pytest.skip("Could not import refactored modules", allow_module_level=True)


class TestTermChunkedUtils:
    """Test utility functions for terminal chunked plotting."""
    
    def test_get_terminal_plot_size(self):
        """Test terminal plot size calculation."""
        with patch('sys.argv', ['script.py', '-d', 'term']):
            width, height = get_terminal_plot_size()
            assert width == 200
            assert height == 48
        
        with patch('sys.argv', ['script.py']):
            width, height = get_terminal_plot_size()
            assert width == 200
            assert height == 50
    
    def test_calculate_optimal_chunk_size(self):
        """Test optimal chunk size calculation."""
        # Test with small dataset
        chunk_size = calculate_optimal_chunk_size(100)
        assert chunk_size == 50  # Minimum size
        
        # Test with medium dataset
        chunk_size = calculate_optimal_chunk_size(1000)
        assert chunk_size == 100  # Should be around 100
        
        # Test with large dataset
        chunk_size = calculate_optimal_chunk_size(5000)
        assert chunk_size == 200  # Maximum size
        
        # Test with zero rows
        chunk_size = calculate_optimal_chunk_size(0)
        assert chunk_size == 50  # Minimum size
    
    def test_split_dataframe_into_chunks(self):
        """Test DataFrame splitting into chunks."""
        # Create test DataFrame
        df = pd.DataFrame({
            'Open': range(100),
            'High': range(100),
            'Low': range(100),
            'Close': range(100)
        })
        
        chunks = split_dataframe_into_chunks(df, 25)
        assert len(chunks) == 4
        assert len(chunks[0]) == 25
        assert len(chunks[1]) == 25
        assert len(chunks[2]) == 25
        assert len(chunks[3]) == 25
        
        # Test with empty DataFrame
        empty_df = pd.DataFrame()
        chunks = split_dataframe_into_chunks(empty_df, 25)
        assert len(chunks) == 0
    
    def test_parse_rsi_rule(self):
        """Test RSI rule parsing."""
        # Test valid RSI rule
        rule_type, params = parse_rsi_rule('rsi(14,70,30,close)')
        assert rule_type == 'rsi'
        assert params['period'] == 14
        assert params['overbought'] == 70
        assert params['oversold'] == 30
        assert params['price_type'] == 'close'
        
        # Test invalid RSI rule
        rule_type, params = parse_rsi_rule('invalid_rule')
        assert rule_type == 'invalid_rule'
        assert params == {}
    
    @patch('plotext.candlestick')
    def test_draw_ohlc_candles(self, mock_candlestick):
        """Test OHLC candle drawing."""
        # Create test chunk with OHLC data
        chunk = pd.DataFrame({
            'Open': [1.0, 2.0, 3.0],
            'High': [1.1, 2.1, 3.1],
            'Low': [0.9, 1.9, 2.9],
            'Close': [1.05, 2.05, 3.05]
        })
        x_values = [0, 1, 2]
        
        draw_ohlc_candles(chunk, x_values)
        mock_candlestick.assert_called_once()
    
    def test_create_time_axis(self):
        """Test time axis creation."""
        # Test with datetime index
        dates = pd.date_range('2023-01-01', periods=3, freq='D')
        chunk = pd.DataFrame({'Close': [1, 2, 3]}, index=dates)
        
        x_values, x_labels = create_time_axis(chunk)
        assert len(x_values) == 3
        assert len(x_labels) == 3
        assert '2023-01-01' in x_labels[0]
        
        # Test with numeric index
        chunk = pd.DataFrame({'Close': [1, 2, 3]})
        x_values, x_labels = create_time_axis(chunk)
        assert len(x_values) == 3
        assert len(x_labels) == 3
        assert x_labels == ['0', '1', '2']


class TestTermChunkedOverlays:
    """Test overlay functions for terminal chunked plotting."""
    
    @patch('src.plotting.term_chunked_overlays._add_trading_signals_to_chunk')
    def test_add_pv_overlays_to_chunk(self, mock_add_signals):
        """Test PV overlays addition."""
        chunk = pd.DataFrame({'Direction': ['BUY', 'SELL', 'NO_TRADE']})
        x_values = [0, 1, 2]
        
        _add_pv_overlays_to_chunk(chunk, x_values)
        mock_add_signals.assert_called_once_with(chunk, x_values)
    
    @patch('plotext.plot')
    def test_add_sr_overlays_to_chunk(self, mock_plot):
        """Test SR overlays addition."""
        chunk = pd.DataFrame({
            'PPrice1': [1.0, 2.0, 3.0],  # Support
            'PPrice2': [1.1, 2.1, 3.1]   # Resistance
        })
        x_values = [0, 1, 2]
        
        _add_sr_overlays_to_chunk(chunk, x_values)
        assert mock_plot.call_count == 2  # Two lines should be plotted
    
    @patch('plotext.plot')
    @patch('src.plotting.term_chunked_overlays._add_trading_signals_to_chunk')
    def test_add_phld_overlays_to_chunk(self, mock_add_signals, mock_plot):
        """Test PHLD overlays addition."""
        chunk = pd.DataFrame({
            'PPrice1': [1.0, 2.0, 3.0],  # Support channel
            'PPrice2': [1.1, 2.1, 3.1],  # Resistance channel
            'Direction': ['BUY', 'SELL', 'NO_TRADE']
        })
        x_values = [0, 1, 2]
        
        _add_phld_overlays_to_chunk(chunk, x_values)
        assert mock_plot.call_count == 2  # Two channels should be plotted
        mock_add_signals.assert_called_once_with(chunk, x_values)
    
    @patch('src.plotting.term_chunked_overlays._add_trading_signals_to_chunk')
    def test_add_rsi_overlays_to_chunk(self, mock_add_signals):
        """Test RSI overlays addition."""
        chunk = pd.DataFrame({'Direction': ['BUY', 'SELL', 'NO_TRADE']})
        x_values = [0, 1, 2]
        rule_type = 'rsi'
        params = {'period': 14, 'overbought': 70, 'oversold': 30, 'price_type': 'close'}
        
        _add_rsi_overlays_to_chunk(chunk, x_values, rule_type, params)
        mock_add_signals.assert_called_once_with(chunk, x_values)


class TestTermChunkedStatistics:
    """Test statistics functions for terminal chunked plotting."""
    
    @patch('builtins.print')
    def test_show_chunk_statistics(self, mock_print):
        """Test chunk statistics display."""
        chunk = pd.DataFrame({
            'Open': [1.0, 2.0, 3.0],
            'High': [1.1, 2.1, 3.1],
            'Low': [0.9, 1.9, 2.9],
            'Close': [1.05, 2.05, 3.05],
            'Volume': [100, 200, 300],
            'Direction': ['BUY', 'SELL', 'NO_TRADE']
        })
        
        _show_chunk_statistics(chunk, "Test Chunk", 0, 3)
        assert mock_print.called
    
    @patch('builtins.print')
    def test_show_field_statistics(self, mock_print):
        """Test field statistics display."""
        field_series = pd.Series([1.0, 2.0, 3.0, 4.0, 5.0])
        
        _show_field_statistics(field_series, "TestField")
        assert mock_print.called


class TestTermChunkedPlotters:
    """Test plotter functions for terminal chunked plotting."""
    
    @patch('src.plotting.term_chunked_plotters.calculate_optimal_chunk_size')
    @patch('src.plotting.term_chunked_plotters.split_dataframe_into_chunks')
    @patch('src.plotting.term_chunked_plotters.clear_plot')
    @patch('src.plotting.term_chunked_plotters.setup_plot_layout')
    @patch('src.plotting.term_chunked_plotters.create_time_axis')
    @patch('src.plotting.term_chunked_plotters.draw_ohlc_candles')
    @patch('plotext.show')
    @patch('plotext.title')
    @patch('plotext.xlabel')
    @patch('plotext.ylabel')
    @patch('plotext.xticks')
    def test_plot_ohlcv_chunks(self, mock_xticks, mock_ylabel, mock_xlabel, mock_title, 
                               mock_show, mock_draw_candles, mock_create_axis,
                               mock_setup_layout, mock_clear_plot, mock_split_chunks,
                               mock_calculate_size):
        """Test OHLCV chunks plotting."""
        # Setup mocks
        mock_calculate_size.return_value = 50
        mock_split_chunks.return_value = [pd.DataFrame({'Open': [1], 'High': [1], 'Low': [1], 'Close': [1]})]
        mock_create_axis.return_value = ([0], ['2023-01-01'])
        
        # Create test DataFrame
        df = pd.DataFrame({
            'Open': [1.0, 2.0, 3.0],
            'High': [1.1, 2.1, 3.1],
            'Low': [0.9, 1.9, 2.9],
            'Close': [1.05, 2.05, 3.05]
        })
        
        plot_ohlcv_chunks(df, "Test OHLC", "matrix", False)
        
        # Verify mocks were called
        mock_calculate_size.assert_called_once()
        mock_split_chunks.assert_called_once()
        mock_clear_plot.assert_called()
        mock_setup_layout.assert_called()
        mock_create_axis.assert_called()
        mock_draw_candles.assert_called()
        mock_show.assert_called()
    
    @patch('src.plotting.term_chunked_plotters.clear_plot')
    @patch('src.plotting.term_chunked_plotters.setup_plot_layout')
    @patch('src.plotting.term_chunked_plotters.create_time_axis')
    @patch('plotext.plot')
    @patch('plotext.show')
    @patch('plotext.title')
    @patch('plotext.xlabel')
    @patch('plotext.ylabel')
    @patch('plotext.xticks')
    def test_plot_single_field_chunk(self, mock_xticks, mock_ylabel, mock_xlabel, mock_title, 
                                    mock_show, mock_plot, mock_create_axis,
                                    mock_setup_layout, mock_clear_plot):
        """Test single field chunk plotting."""
        # Setup mocks
        mock_create_axis.return_value = ([0, 1, 2], ['2023-01-01', '2023-01-02', '2023-01-03'])
        
        # Create test chunk
        chunk = pd.DataFrame({
            'TestField': [1.0, 2.0, 3.0]
        }, index=pd.date_range('2023-01-01', periods=3))
        
        _plot_single_field_chunk(chunk, 'TestField', 'Test Title', 'matrix')
        
        # Verify mocks were called
        mock_clear_plot.assert_called()
        mock_setup_layout.assert_called()
        mock_create_axis.assert_called()
        mock_plot.assert_called()
        mock_show.assert_called()


class TestTermChunkedPlot:
    """Test main plot function for terminal chunked plotting."""
    
    def test_plot_chunked_terminal_ohlcv(self):
        """Test main function with OHLCV rule."""
        df = pd.DataFrame({'Open': [1], 'High': [1], 'Low': [1], 'Close': [1]})
        
        # Mock the actual function calls to avoid real execution
        with patch('src.plotting.term_chunked_plot.plot_ohlcv_chunks') as mock_plot:
            plot_chunked_terminal(df, 'OHLCV', 'Test', 'matrix', False)
            mock_plot.assert_called_once_with(df, 'Test', 'matrix', False)
    
    def test_plot_chunked_terminal_auto(self):
        """Test main function with AUTO rule."""
        df = pd.DataFrame({'Open': [1], 'High': [1], 'Low': [1], 'Close': [1]})
        
        with patch('src.plotting.term_chunked_plot.plot_auto_chunks') as mock_plot:
            plot_chunked_terminal(df, 'AUTO', 'Test', 'matrix', False)
            mock_plot.assert_called_once_with(df, 'Test', 'matrix', False)
    
    def test_plot_chunked_terminal_pv(self):
        """Test main function with PV rule."""
        df = pd.DataFrame({'Open': [1], 'High': [1], 'Low': [1], 'Close': [1]})
        
        with patch('src.plotting.term_chunked_plot.plot_pv_chunks') as mock_plot:
            plot_chunked_terminal(df, 'PV', 'Test', 'matrix', False)
            mock_plot.assert_called_once_with(df, 'Test', 'matrix', False)
    
    def test_plot_chunked_terminal_sr(self):
        """Test main function with SR rule."""
        df = pd.DataFrame({'Open': [1], 'High': [1], 'Low': [1], 'Close': [1]})
        
        with patch('src.plotting.term_chunked_plot.plot_sr_chunks') as mock_plot:
            plot_chunked_terminal(df, 'SR', 'Test', 'matrix', False)
            mock_plot.assert_called_once_with(df, 'Test', 'matrix', False)
    
    def test_plot_chunked_terminal_phld(self):
        """Test main function with PHLD rule."""
        df = pd.DataFrame({'Open': [1], 'High': [1], 'Low': [1], 'Close': [1]})
        
        with patch('src.plotting.term_chunked_plot.plot_phld_chunks') as mock_plot:
            plot_chunked_terminal(df, 'PHLD', 'Test', 'matrix', False)
            mock_plot.assert_called_once_with(df, 'Test', 'matrix', False)
    
    def test_plot_chunked_terminal_rsi(self):
        """Test main function with RSI rule."""
        df = pd.DataFrame({'Open': [1], 'High': [1], 'Low': [1], 'Close': [1]})
        
        with patch('src.plotting.term_chunked_plot.plot_rsi_chunks') as mock_plot:
            plot_chunked_terminal(df, 'RSI', 'Test', 'matrix', False)
            mock_plot.assert_called_once_with(df, 'rsi(14,70,30,close)', 'Test', 'matrix', False)
    
    def test_plot_chunked_terminal_rsi_parameterized(self):
        """Test main function with parameterized RSI rule."""
        df = pd.DataFrame({'Open': [1], 'High': [1], 'Low': [1], 'Close': [1]})
        
        with patch('src.plotting.term_chunked_plot.plot_rsi_chunks') as mock_plot:
            plot_chunked_terminal(df, 'rsi(14,70,30,close)', 'Test', 'matrix', False)
            mock_plot.assert_called_once_with(df, 'rsi(14,70,30,close)', 'Test', 'matrix', False)
    
    def test_plot_chunked_terminal_unknown_rule(self):
        """Test main function with unknown rule."""
        df = pd.DataFrame({'Open': [1], 'High': [1], 'Low': [1], 'Close': [1]})
        
        with patch('src.plotting.term_chunked_plot.plot_ohlcv_chunks') as mock_plot:
            plot_chunked_terminal(df, 'UNKNOWN_RULE', 'Test', 'matrix', False)
            mock_plot.assert_called_once_with(df, 'Test', 'matrix', False) 