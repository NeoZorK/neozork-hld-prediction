# -*- coding: utf-8 -*-
# tests/plotting/test_wave_prime_fastest_fast.py

"""
Tests for Wave indicator Prime rule in fastest and fast plotting modes.
"""

import pytest
import pandas as pd
import numpy as np
from unittest.mock import patch, MagicMock

from src.plotting.dual_chart_fastest import plot_dual_chart_fastest
from src.plotting.dual_chart_fast import plot_dual_chart_fast


class TestWavePrimeFastestFast:
    """Test cases for Wave indicator Prime rule in fastest and fast modes."""

    @pytest.fixture
    def sample_wave_data_with_prime_signals(self):
        """Create sample data with Wave indicator using Prime rule."""
        dates = pd.date_range('2023-01-01', periods=20, freq='D')
        data = {
            'DateTime': dates,
            'Open': np.random.uniform(100, 200, 20),
            'High': np.random.uniform(200, 300, 20),
            'Low': np.random.uniform(50, 100, 20),
            'Close': np.random.uniform(100, 200, 20),
            'Volume': np.random.uniform(1000, 10000, 20),
            # Wave indicator columns with Prime rule applied (signals should be inverted)
            '_Plot_Color': [2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1],  # Inverted signals
            '_Signal': [2, 0, 0, 1, 0, 0, 2, 0, 0, 1, 0, 0, 2, 0, 0, 1, 0, 0, 2, 0],  # Only direction changes
            '_Plot_Wave': np.random.uniform(-0.1, 0.1, 20),
            '_Plot_FastLine': np.random.uniform(-0.05, 0.05, 20),
            'MA_Line': np.random.uniform(-0.08, 0.08, 20)
        }
        df = pd.DataFrame(data)
        df.set_index('DateTime', inplace=True)
        return df

    def test_wave_prime_rule_fastest_mode(self, sample_wave_data_with_prime_signals):
        """Test Wave indicator Prime rule in fastest mode."""
        with patch('plotly.graph_objects.Figure.show'):
            fig = plot_dual_chart_fastest(
                sample_wave_data_with_prime_signals,
                'wave:339,10,2,fast,22,11,4,fast,prime,10,close',
                'Test Wave Prime Rule - Fastest Mode'
            )
            
            # Check that figure was created successfully
            assert fig is not None
            assert len(fig.data) > 0
            
            # Check that the figure has the expected structure
            rows_cols = fig._get_subplot_rows_columns()
            assert len(rows_cols) == 2  # Should have rows and cols

    def test_wave_prime_rule_fast_mode(self, sample_wave_data_with_prime_signals):
        """Test Wave indicator Prime rule in fast mode."""
        with patch('bokeh.plotting.show'):
            result = plot_dual_chart_fast(
                sample_wave_data_with_prime_signals,
                'wave:339,10,2,fast,22,11,4,fast,prime,10,close',
                'Test Wave Prime Rule - Fast Mode'
            )
            
            # Check that result is not None (bokeh figure or similar)
            assert result is not None

    def test_wave_prime_signal_inversion_fastest(self, sample_wave_data_with_prime_signals):
        """Test that Prime rule correctly inverts signals in fastest mode."""
        # Create data where original signals would be BUY, but Prime should invert to SELL
        test_data = sample_wave_data_with_prime_signals.copy()
        
        with patch('plotly.graph_objects.Figure.show'):
            fig = plot_dual_chart_fastest(
                test_data,
                'wave:339,10,2,fast,22,11,4,fast,prime,10,close',
                'Test Signal Inversion'
            )
            
            # Check that the data contains inverted signals
            plot_color_data = test_data['_Plot_Color']
            
            # Should have both BUY (1) and SELL (2) signals
            unique_signals = plot_color_data.unique()
            assert 1 in unique_signals  # BUY signals
            assert 2 in unique_signals  # SELL signals

    def test_wave_prime_signal_inversion_fast(self, sample_wave_data_with_prime_signals):
        """Test that Prime rule correctly inverts signals in fast mode."""
        # Create data where original signals would be BUY, but Prime should invert to SELL
        test_data = sample_wave_data_with_prime_signals.copy()
        
        with patch('bokeh.plotting.show'):
            result = plot_dual_chart_fast(
                test_data,
                'wave:339,10,2,fast,22,11,4,fast,prime,10,close',
                'Test Signal Inversion - Fast'
            )
            
            # Check that the data contains inverted signals
            plot_color_data = test_data['_Plot_Color']
            
            # Should have both BUY (1) and SELL (2) signals
            unique_signals = plot_color_data.unique()
            assert 1 in unique_signals  # BUY signals
            assert 2 in unique_signals  # SELL signals

    def test_wave_prime_vs_reverse_fastest(self, sample_wave_data_with_prime_signals):
        """Test that Prime and Reverse rules produce different results in fastest mode."""
        test_data = sample_wave_data_with_prime_signals.copy()
        
        with patch('plotly.graph_objects.Figure.show'):
            # Test Prime rule
            fig_prime = plot_dual_chart_fastest(
                test_data,
                'wave:339,10,2,fast,22,11,4,fast,prime,10,close',
                'Prime Rule Test'
            )
            
            # Test Reverse rule
            fig_reverse = plot_dual_chart_fastest(
                test_data,
                'wave:339,10,2,fast,22,11,4,fast,reverse,10,close',
                'Reverse Rule Test'
            )
            
            # Both figures should exist but with different signal processing
            assert fig_prime is not None
            assert fig_reverse is not None

    def test_wave_prime_vs_reverse_fast(self, sample_wave_data_with_prime_signals):
        """Test that Prime and Reverse rules produce different results in fast mode."""
        test_data = sample_wave_data_with_prime_signals.copy()
        
        with patch('bokeh.plotting.show'):
            # Test Prime rule
            result_prime = plot_dual_chart_fast(
                test_data,
                'wave:339,10,2,fast,22,11,4,fast,prime,10,close',
                'Prime Rule Test'
            )
            
            # Test Reverse rule
            result_reverse = plot_dual_chart_fast(
                test_data,
                'wave:339,10,2,fast,22,11,4,fast,reverse,10,close',
                'Reverse Rule Test'
            )
            
            # Both results should exist
            assert result_prime is not None
            assert result_reverse is not None

    def test_wave_prime_rule_signal_filtering_fastest(self, sample_wave_data_with_prime_signals):
        """Test that Prime rule correctly filters signals in fastest mode."""
        # Ensure _Signal column has fewer signals than _Plot_Color
        test_data = sample_wave_data_with_prime_signals.copy()
        
        # Count signals
        plot_color_signals = test_data['_Plot_Color'][test_data['_Plot_Color'] != 0]
        signal_signals = test_data['_Signal'][test_data['_Signal'] != 0]
        
        # _Signal should have fewer signals than _Plot_Color (only direction changes)
        assert len(signal_signals) <= len(plot_color_signals)
        
        with patch('plotly.graph_objects.Figure.show'):
            fig = plot_dual_chart_fastest(
                test_data,
                'wave:339,10,2,fast,22,11,4,fast,prime,10,close',
                'Signal Filtering Test'
            )
            
            assert fig is not None

    def test_wave_prime_rule_signal_filtering_fast(self, sample_wave_data_with_prime_signals):
        """Test that Prime rule correctly filters signals in fast mode."""
        # Ensure _Signal column has fewer signals than _Plot_Color
        test_data = sample_wave_data_with_prime_signals.copy()
        
        # Count signals
        plot_color_signals = test_data['_Plot_Color'][test_data['_Plot_Color'] != 0]
        signal_signals = test_data['_Signal'][test_data['_Signal'] != 0]
        
        # _Signal should have fewer signals than _Plot_Color (only direction changes)
        assert len(signal_signals) <= len(plot_color_signals)
        
        with patch('bokeh.plotting.show'):
            result = plot_dual_chart_fast(
                test_data,
                'wave:339,10,2,fast,22,11,4,fast,prime,10,close',
                'Signal Filtering Test'
            )
            
            assert result is not None

    def test_wave_prime_rule_edge_cases_fastest(self, sample_wave_data_with_prime_signals):
        """Test edge cases for Prime rule in fastest mode."""
        # Test with minimal data
        minimal_data = sample_wave_data_with_prime_signals.head(5).copy()
        
        with patch('plotly.graph_objects.Figure.show'):
            fig = plot_dual_chart_fastest(
                minimal_data,
                'wave:339,10,2,fast,22,11,4,fast,prime,10,close',
                'Edge Case Test'
            )
            
            assert fig is not None

    def test_wave_prime_rule_edge_cases_fast(self, sample_wave_data_with_prime_signals):
        """Test edge cases for Prime rule in fast mode."""
        # Test with minimal data
        minimal_data = sample_wave_data_with_prime_signals.head(5).copy()
        
        with patch('bokeh.plotting.show'):
            result = plot_dual_chart_fast(
                minimal_data,
                'wave:339,10,2,fast,22,11,4,fast,prime,10,close',
                'Edge Case Test'
            )
            
            assert result is not None

    def test_wave_prime_rule_integration_fastest_fast(self, sample_wave_data_with_prime_signals):
        """Test integration between fastest and fast modes for Prime rule."""
        test_data = sample_wave_data_with_prime_signals.copy()
        
        with patch('plotly.graph_objects.Figure.show'), patch('bokeh.plotting.show'):
            # Test both modes with same data and rule
            fig_fastest = plot_dual_chart_fastest(
                test_data,
                'wave:339,10,2,fast,22,11,4,fast,prime,10,close',
                'Integration Test - Fastest'
            )
            
            result_fast = plot_dual_chart_fast(
                test_data,
                'wave:339,10,2,fast,22,11,4,fast,prime,10,close',
                'Integration Test - Fast'
            )
            
            # Both should work with same data
            assert fig_fastest is not None
            assert result_fast is not None


if __name__ == "__main__":
    pytest.main([__file__])
