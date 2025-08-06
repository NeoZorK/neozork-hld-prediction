# -*- coding: utf-8 -*-
# tests/plotting/test_term_chunked_plotters.py

"""
Tests for terminal chunked plotters.
"""

import pytest
import pandas as pd
import numpy as np
from unittest.mock import patch, MagicMock

# Import the functions to test
try:
    from src.plotting.term_chunked_plotters import (
        _get_field_color, _get_field_color_by_index,
        plot_auto_chunks, _plot_single_field_chunk
    )
except ImportError:
    # Fallback for when run as module
    from ..plotting.term_chunked_plotters import (
        _get_field_color, _get_field_color_by_index,
        plot_auto_chunks, _plot_single_field_chunk
    )


class TestFieldColorAssignment:
    """Test field color assignment functionality."""
    
    def test_get_field_color_pressure_indicators(self):
        """Test color assignment for pressure indicators."""
        assert _get_field_color('pressure_high') == 'red+'
        assert _get_field_color('pressure_low') == 'blue+'
        assert _get_field_color('pressure_vector') == 'magenta+'
        assert _get_field_color('pressure') == 'cyan+'
    
    def test_get_field_color_predicted_values(self):
        """Test color assignment for predicted values."""
        assert _get_field_color('predicted_high') == 'bright red'
        assert _get_field_color('predicted_low') == 'bright blue'
        assert _get_field_color('predicted_close') == 'bright green'
        assert _get_field_color('predicted') == 'yellow+'
    
    def test_get_field_color_support_resistance(self):
        """Test color assignment for support/resistance indicators."""
        assert _get_field_color('support') == 'green+'
        assert _get_field_color('resistance') == 'red+'
        assert _get_field_color('support_level') == 'green'
        assert _get_field_color('resistance_level') == 'red'
    
    def test_get_field_color_rsi_variants(self):
        """Test color assignment for RSI variants."""
        assert _get_field_color('rsi') == 'cyan+'
        assert _get_field_color('rsi_signal') == 'yellow+'
        assert _get_field_color('rsi_momentum') == 'magenta+'
        assert _get_field_color('rsi_divergence') == 'bright cyan'
    
    def test_get_field_color_volume_indicators(self):
        """Test color assignment for volume indicators."""
        assert _get_field_color('volume') == 'white+'
        assert _get_field_color('obv') == 'bright white'
        assert _get_field_color('vwap') == 'bright yellow'
    
    def test_get_field_color_macd(self):
        """Test color assignment for MACD indicators."""
        assert _get_field_color('macd') == 'blue+'
        assert _get_field_color('macd_signal') == 'red+'
        assert _get_field_color('macd_histogram') == 'yellow+'
    
    def test_get_field_color_moving_averages(self):
        """Test color assignment for moving averages."""
        assert _get_field_color('sma') == 'green+'
        assert _get_field_color('ema') == 'blue+'
        assert _get_field_color('ma') == 'cyan+'
    
    def test_get_field_color_bollinger_bands(self):
        """Test color assignment for Bollinger Bands."""
        assert _get_field_color('bb_upper') == 'red+'
        assert _get_field_color('bb_lower') == 'blue+'
        assert _get_field_color('bb_middle') == 'yellow+'
    
    def test_get_field_color_by_index(self):
        """Test color assignment by field index."""
        # Test with known field names (should use name-based color)
        assert _get_field_color_by_index('pressure', 0) == 'cyan+'  # pressure is cyan+ in field_colors
        assert _get_field_color_by_index('pressure_vector', 1) == 'magenta+'
        assert _get_field_color_by_index('predicted_high', 2) == 'bright red'
        
        # Test with unknown field names (should use index-based color)
        assert _get_field_color_by_index('unknown_field', 0) == 'green+'
        assert _get_field_color_by_index('custom_indicator', 5) == 'white+'  # index 5 in palette is white+
    
    def test_get_field_color_fallback(self):
        """Test color assignment fallback for unknown fields."""
        # Test fallback to index-based color
        assert _get_field_color('unknown_field', 0) == 'green+'
        assert _get_field_color('custom_indicator', 5) == 'white+'  # index 5 in palette is white+
        
        # Test final fallback
        assert _get_field_color('completely_unknown') == 'green+'


class TestAutoChunksColorAssignment:
    """Test color assignment in AUTO chunks plotting."""
    
    def test_auto_chunks_field_colors(self):
        """Test that AUTO chunks use different colors for different fields."""
        # Create test data with multiple fields
        dates = pd.date_range('2020-01-01', periods=10, freq='D')
        df = pd.DataFrame({
            'Open': [1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9],
            'High': [1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0],
            'Low': [0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8],
            'Close': [1.05, 1.15, 1.25, 1.35, 1.45, 1.55, 1.65, 1.75, 1.85, 1.95],
            'Volume': [100, 110, 120, 130, 140, 150, 160, 170, 180, 190],
            'pressure': [10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
            'pressure_vector': [20, 21, 22, 23, 24, 25, 26, 27, 28, 29],
            'predicted_high': [1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0, 2.1],
            'predicted_low': [0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7]
        }, index=dates)
        
        # Test that different fields get different colors
        pressure_color = _get_field_color('pressure')
        pressure_vector_color = _get_field_color('pressure_vector')
        predicted_high_color = _get_field_color('predicted_high')
        predicted_low_color = _get_field_color('predicted_low')
        
        # Verify that colors are different
        assert pressure_color != pressure_vector_color
        assert pressure_color != predicted_high_color
        assert pressure_color != predicted_low_color
        assert pressure_vector_color != predicted_high_color
        assert pressure_vector_color != predicted_low_color
        assert predicted_high_color != predicted_low_color
        
        # Verify specific color assignments
        assert pressure_color == 'cyan+'
        assert pressure_vector_color == 'magenta+'
        assert predicted_high_color == 'bright red'
        assert predicted_low_color == 'bright blue' 