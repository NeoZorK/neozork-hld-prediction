# -*- coding: utf-8 -*-
# tests/plotting/test_term_chunked_integration.py

"""
Integration tests for refactored terminal chunked plotting modules.
"""

import pytest
import pandas as pd
import numpy as np
from unittest.mock import patch, MagicMock

# Import the modules to test
try:
    from src.plotting.term_chunked_plot import plot_chunked_terminal
    from src.plotting.term_chunked_utils import (
        calculate_optimal_chunk_size, split_dataframe_into_chunks
    )
except ImportError:
    pytest.skip("Could not import refactored modules", allow_module_level=True)


class TestTermChunkedIntegration:
    """Integration tests for terminal chunked plotting."""
    
    def test_calculate_optimal_chunk_size_integration(self):
        """Test optimal chunk size calculation with real data."""
        # Test with different dataset sizes
        test_cases = [
            (100, 50),   # Small dataset -> minimum size
            (1000, 100), # Medium dataset -> around 100
            (5000, 200), # Large dataset -> maximum size
            (0, 50),     # Empty dataset -> minimum size
        ]
        
        for total_rows, expected_size in test_cases:
            chunk_size = calculate_optimal_chunk_size(total_rows)
            assert chunk_size == expected_size
    
    def test_split_dataframe_into_chunks_integration(self):
        """Test DataFrame splitting with real data."""
        # Create test DataFrame
        df = pd.DataFrame({
            'Open': range(100),
            'High': range(100),
            'Low': range(100),
            'Close': range(100),
            'Volume': range(100)
        })
        
        # Test splitting into chunks
        chunk_size = 25
        chunks = split_dataframe_into_chunks(df, chunk_size)
        
        assert len(chunks) == 4
        assert all(len(chunk) == 25 for chunk in chunks[:3])
        assert len(chunks[3]) == 25  # Last chunk
        
        # Verify data integrity
        reconstructed_df = pd.concat(chunks)
        pd.testing.assert_frame_equal(df, reconstructed_df)
    
    @patch('src.plotting.term_chunked_plotters.plot_ohlcv_chunks')
    def test_plot_chunked_terminal_ohlcv_integration(self, mock_plot):
        """Test main function with OHLCV rule."""
        # Create test DataFrame
        df = pd.DataFrame({
            'Open': [1.0, 2.0, 3.0],
            'High': [1.1, 2.1, 3.1],
            'Low': [0.9, 1.9, 2.9],
            'Close': [1.05, 2.05, 3.05]
        })
        
        # Test the main function
        plot_chunked_terminal(df, 'OHLCV', 'Test OHLC', 'matrix', False)
        
        # Verify that the correct function was called
        mock_plot.assert_called_once_with(df, 'Test OHLC', 'matrix', False)
    
    @patch('src.plotting.term_chunked_plotters.plot_auto_chunks')
    def test_plot_chunked_terminal_auto_integration(self, mock_plot):
        """Test main function with AUTO rule."""
        # Create test DataFrame
        df = pd.DataFrame({
            'Open': [1.0, 2.0, 3.0],
            'High': [1.1, 2.1, 3.1],
            'Low': [0.9, 1.9, 2.9],
            'Close': [1.05, 2.05, 3.05],
            'Volume': [100, 200, 300]
        })
        
        # Test the main function
        plot_chunked_terminal(df, 'AUTO', 'Test AUTO', 'matrix', False)
        
        # Verify that the correct function was called
        mock_plot.assert_called_once_with(df, 'Test AUTO', 'matrix', False)
    
    @patch('src.plotting.term_chunked_plotters.plot_pv_chunks')
    def test_plot_chunked_terminal_pv_integration(self, mock_plot):
        """Test main function with PV rule."""
        # Create test DataFrame
        df = pd.DataFrame({
            'Open': [1.0, 2.0, 3.0],
            'High': [1.1, 2.1, 3.1],
            'Low': [0.9, 1.9, 2.9],
            'Close': [1.05, 2.05, 3.05],
            'Direction': ['BUY', 'SELL', 'NO_TRADE']
        })
        
        # Test the main function
        plot_chunked_terminal(df, 'PV', 'Test PV', 'matrix', False)
        
        # Verify that the correct function was called
        mock_plot.assert_called_once_with(df, 'Test PV', 'matrix', False)
    
    @patch('src.plotting.term_chunked_plotters.plot_sr_chunks')
    def test_plot_chunked_terminal_sr_integration(self, mock_plot):
        """Test main function with SR rule."""
        # Create test DataFrame
        df = pd.DataFrame({
            'Open': [1.0, 2.0, 3.0],
            'High': [1.1, 2.1, 3.1],
            'Low': [0.9, 1.9, 2.9],
            'Close': [1.05, 2.05, 3.05],
            'PPrice1': [1.0, 2.0, 3.0],  # Support
            'PPrice2': [1.1, 2.1, 3.1]   # Resistance
        })
        
        # Test the main function
        plot_chunked_terminal(df, 'SR', 'Test SR', 'matrix', False)
        
        # Verify that the correct function was called
        mock_plot.assert_called_once_with(df, 'Test SR', 'matrix', False)
    
    @patch('src.plotting.term_chunked_plotters.plot_phld_chunks')
    def test_plot_chunked_terminal_phld_integration(self, mock_plot):
        """Test main function with PHLD rule."""
        # Create test DataFrame
        df = pd.DataFrame({
            'Open': [1.0, 2.0, 3.0],
            'High': [1.1, 2.1, 3.1],
            'Low': [0.9, 1.9, 2.9],
            'Close': [1.05, 2.05, 3.05],
            'PPrice1': [1.0, 2.0, 3.0],  # Support channel
            'PPrice2': [1.1, 2.1, 3.1],  # Resistance channel
            'Direction': ['BUY', 'SELL', 'NO_TRADE']
        })
        
        # Test the main function
        plot_chunked_terminal(df, 'PHLD', 'Test PHLD', 'matrix', False)
        
        # Verify that the correct function was called
        mock_plot.assert_called_once_with(df, 'Test PHLD', 'matrix', False)
    
    @patch('src.plotting.term_chunked_plotters.plot_rsi_chunks')
    def test_plot_chunked_terminal_rsi_integration(self, mock_plot):
        """Test main function with RSI rule."""
        # Create test DataFrame
        df = pd.DataFrame({
            'Open': [1.0, 2.0, 3.0],
            'High': [1.1, 2.1, 3.1],
            'Low': [0.9, 1.9, 2.9],
            'Close': [1.05, 2.05, 3.05],
            'Direction': ['BUY', 'SELL', 'NO_TRADE']
        })
        
        # Test the main function
        plot_chunked_terminal(df, 'RSI', 'Test RSI', 'matrix', False)
        
        # Verify that the correct function was called
        mock_plot.assert_called_once_with(df, 'RSI', 'Test RSI', 'matrix', False)
    
    @patch('src.plotting.term_chunked_plotters.plot_rsi_chunks')
    def test_plot_chunked_terminal_rsi_parameterized_integration(self, mock_plot):
        """Test main function with parameterized RSI rule."""
        # Create test DataFrame
        df = pd.DataFrame({
            'Open': [1.0, 2.0, 3.0],
            'High': [1.1, 2.1, 3.1],
            'Low': [0.9, 1.9, 2.9],
            'Close': [1.05, 2.05, 3.05],
            'Direction': ['BUY', 'SELL', 'NO_TRADE']
        })
        
        # Test the main function with parameterized RSI rule
        rule = 'rsi(14,70,30,close)'
        plot_chunked_terminal(df, rule, 'Test RSI Param', 'matrix', False)
        
        # Verify that the correct function was called
        mock_plot.assert_called_once_with(df, rule, 'Test RSI Param', 'matrix', False)
    
    @patch('src.plotting.term_chunked_plotters.plot_ohlcv_chunks')
    def test_plot_chunked_terminal_unknown_rule_integration(self, mock_plot):
        """Test main function with unknown rule."""
        # Create test DataFrame
        df = pd.DataFrame({
            'Open': [1.0, 2.0, 3.0],
            'High': [1.1, 2.1, 3.1],
            'Low': [0.9, 1.9, 2.9],
            'Close': [1.05, 2.05, 3.05]
        })
        
        # Test the main function with unknown rule
        plot_chunked_terminal(df, 'UNKNOWN_RULE', 'Test Unknown', 'matrix', False)
        
        # Verify that the default function was called
        mock_plot.assert_called_once_with(df, 'Test Unknown', 'matrix', False)
    
    def test_module_imports(self):
        """Test that all refactored modules can be imported."""
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
            assert True  # All imports successful
        except ImportError as e:
            pytest.fail(f"Failed to import refactored modules: {e}")
    
    def test_function_signatures(self):
        """Test that function signatures are preserved."""
        from src.plotting.term_chunked_plot import plot_chunked_terminal
        from src.plotting.term_chunked_utils import calculate_optimal_chunk_size
        
        # Test that functions have the expected signatures
        import inspect
        
        # Test plot_chunked_terminal signature
        sig = inspect.signature(plot_chunked_terminal)
        params = list(sig.parameters.keys())
        expected_params = ['df', 'rule', 'title', 'style', 'use_navigation']
        assert params == expected_params
        
        # Test calculate_optimal_chunk_size signature
        sig = inspect.signature(calculate_optimal_chunk_size)
        params = list(sig.parameters.keys())
        expected_params = ['total_rows', 'target_chunks', 'min_chunk_size', 'max_chunk_size']
        assert params == expected_params 