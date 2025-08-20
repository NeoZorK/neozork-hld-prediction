# -*- coding: utf-8 -*-
# tests/plotting/test_wave_mpl_colors.py

"""
Tests for Wave indicator colors in MPL plotting mode.
"""

import pytest
import pandas as pd
import numpy as np
from unittest.mock import patch, MagicMock

from src.plotting.dual_chart_mpl import plot_dual_chart_mpl


class TestWaveMplColors:
    """Test cases for Wave indicator colors in MPL mode."""

    @pytest.fixture
    def sample_wave_data_with_signals(self):
        """Create sample data with Wave indicator signals."""
        dates = pd.date_range('2023-01-01', periods=10, freq='D')
        data = {
            'DateTime': dates,
            'Open': np.random.uniform(100, 200, 10),
            'High': np.random.uniform(200, 300, 10),
            'Low': np.random.uniform(50, 100, 10),
            'Close': np.random.uniform(100, 200, 10),
            'Volume': np.random.uniform(1000, 10000, 10),
            # Wave indicator columns
            '_Plot_Color': [1, 2, 1, 2, 1, 2, 1, 2, 1, 2],  # BUY=1, SELL=2
            '_Signal': [1, 0, 0, 2, 0, 0, 1, 0, 0, 2],  # Only direction changes
            '_Plot_Wave': np.random.uniform(-0.1, 0.1, 10),
            '_Plot_FastLine': np.random.uniform(-0.05, 0.05, 10),
            'MA_Line': np.random.uniform(-0.08, 0.08, 10)
        }
        df = pd.DataFrame(data)
        df.set_index('DateTime', inplace=True)
        return df

    def test_wave_buy_signals_blue_color(self, sample_wave_data_with_signals):
        """Test that BUY signals are displayed in blue color."""
        with patch('matplotlib.pyplot.show'):
            # Mock the scatter method to capture color parameters
            with patch('matplotlib.axes.Axes.scatter') as mock_scatter:
                plot_dual_chart_mpl(
                    sample_wave_data_with_signals,
                    'wave:339,10,2,fast,22,11,4,fast,prime,10,close',
                    'Test Wave Colors - MPL Mode'
                )
                
                # Check that scatter was called for BUY signals
                buy_calls = [call for call in mock_scatter.call_args_list 
                           if call[1].get('color') == '#0066CC' and 'Wave BUY' in str(call[1].get('label', ''))]
                
                assert len(buy_calls) > 0, "BUY signals should be displayed in blue color (#0066CC)"

    def test_wave_sell_signals_red_color(self, sample_wave_data_with_signals):
        """Test that SELL signals are displayed in red color."""
        with patch('matplotlib.pyplot.show'):
            # Mock the scatter method to capture color parameters
            with patch('matplotlib.axes.Axes.scatter') as mock_scatter:
                plot_dual_chart_mpl(
                    sample_wave_data_with_signals,
                    'wave:339,10,2,fast,22,11,4,fast,prime,10,close',
                    'Test Wave Colors - MPL Mode'
                )
                
                # Check that scatter was called for SELL signals
                sell_calls = [call for call in mock_scatter.call_args_list 
                            if call[1].get('color') == '#FF4444' and 'Wave SELL' in str(call[1].get('label', ''))]
                
                assert len(sell_calls) > 0, "SELL signals should be displayed in red color (#FF4444)"

    def test_wave_signal_colors_swapped(self, sample_wave_data_with_signals):
        """Test that BUY and SELL signal colors are correctly swapped."""
        with patch('matplotlib.pyplot.show'):
            # Mock the scatter method to capture color parameters
            with patch('matplotlib.axes.Axes.scatter') as mock_scatter:
                plot_dual_chart_mpl(
                    sample_wave_data_with_signals,
                    'wave:339,10,2,fast,22,11,4,fast,prime,10,close',
                    'Test Wave Colors - MPL Mode'
                )
                
                # Extract all scatter calls with color information
                scatter_calls = []
                for call in mock_scatter.call_args_list:
                    if 'color' in call[1]:
                        color = call[1]['color']
                        label = call[1].get('label', '')
                        if 'Wave BUY' in label or 'Wave SELL' in label:
                            scatter_calls.append((color, label))
                
                # Check that BUY signals are blue and SELL signals are red
                buy_colors = [color for color, label in scatter_calls if 'Wave BUY' in label]
                sell_colors = [color for color, label in scatter_calls if 'Wave SELL' in label]
                
                assert all(color == '#0066CC' for color in buy_colors), "All BUY signals should be blue (#0066CC)"
                assert all(color == '#FF4444' for color in sell_colors), "All SELL signals should be red (#FF4444)"

    def test_wave_legend_colors_match_signals(self, sample_wave_data_with_signals):
        """Test that legend colors match the signal colors."""
        with patch('matplotlib.pyplot.show'):
            # Mock the scatter method to capture color parameters
            with patch('matplotlib.axes.Axes.scatter') as mock_scatter:
                plot_dual_chart_mpl(
                    sample_wave_data_with_signals,
                    'wave:339,10,2,fast,22,11,4,fast,prime,10,close',
                    'Test Wave Colors - MPL Mode'
                )
                
                # Check that legend entries have correct colors
                legend_calls = [call for call in mock_scatter.call_args_list 
                              if 'label' in call[1] and ('Wave BUY' in call[1]['label'] or 'Wave SELL' in call[1]['label'])]
                
                for call in legend_calls:
                    label = call[1]['label']
                    color = call[1]['color']
                    
                    if 'Wave BUY' in label:
                        assert color == '#0066CC', f"BUY signal should be blue, got {color}"
                    elif 'Wave SELL' in label:
                        assert color == '#FF4444', f"SELL signal should be red, got {color}"

    def test_wave_signal_markers_correct(self, sample_wave_data_with_signals):
        """Test that BUY and SELL signals use correct markers."""
        with patch('matplotlib.pyplot.show'):
            # Mock the scatter method to capture marker parameters
            with patch('matplotlib.axes.Axes.scatter') as mock_scatter:
                plot_dual_chart_mpl(
                    sample_wave_data_with_signals,
                    'wave:339,10,2,fast,22,11,4,fast,prime,10,close',
                    'Test Wave Colors - MPL Mode'
                )
                
                # Check marker types
                buy_calls = [call for call in mock_scatter.call_args_list 
                           if 'Wave BUY' in str(call[1].get('label', ''))]
                sell_calls = [call for call in mock_scatter.call_args_list 
                            if 'Wave SELL' in str(call[1].get('label', ''))]
                
                # BUY signals should use upward triangle (^)
                for call in buy_calls:
                    assert call[1].get('marker') == '^', "BUY signals should use upward triangle marker"
                
                # SELL signals should use downward triangle (v)
                for call in sell_calls:
                    assert call[1].get('marker') == 'v', "SELL signals should use downward triangle marker"

    def test_wave_signal_positions_correct(self, sample_wave_data_with_signals):
        """Test that BUY and SELL signals are positioned correctly."""
        with patch('matplotlib.pyplot.show'):
            # Mock the scatter method to capture position parameters
            with patch('matplotlib.axes.Axes.scatter') as mock_scatter:
                plot_dual_chart_mpl(
                    sample_wave_data_with_signals,
                    'wave:339,10,2,fast,22,11,4,fast,prime,10,close',
                    'Test Wave Colors - MPL Mode'
                )
                
                # Check that BUY signals are positioned below Low and SELL signals above High
                for call in mock_scatter.call_args_list:
                    label = call[1].get('label', '')
                    y_pos = call[0][1]  # Second argument is y position
                    
                    if 'Wave BUY' in label:
                        # BUY signals should be below Low (multiplied by 0.995)
                        low_values = sample_wave_data_with_signals['Low']
                        assert all(y <= low * 0.995 for y, low in zip(y_pos, low_values)), "BUY signals should be below Low"
                    
                    elif 'Wave SELL' in label:
                        # SELL signals should be above High (multiplied by 1.005)
                        high_values = sample_wave_data_with_signals['High']
                        assert all(y >= high * 1.005 for y, high in zip(y_pos, high_values)), "SELL signals should be above High"

    def test_wave_colors_consistency(self, sample_wave_data_with_signals):
        """Test that colors are consistent across all signal types."""
        with patch('matplotlib.pyplot.show'):
            with patch('matplotlib.axes.Axes.scatter') as mock_scatter:
                plot_dual_chart_mpl(
                    sample_wave_data_with_signals,
                    'wave:339,10,2,fast,22,11,4,fast,prime,10,close',
                    'Test Wave Colors - MPL Mode'
                )
                
                # Check color consistency
                colors_used = set()
                for call in mock_scatter.call_args_list:
                    if 'color' in call[1]:
                        colors_used.add(call[1]['color'])
                
                # Should only use the two expected colors
                expected_colors = {'#0066CC', '#FF4444'}  # Blue and Red
                assert colors_used.issubset(expected_colors), f"Unexpected colors found: {colors_used - expected_colors}"

    def test_wave_signal_alpha_and_zorder(self, sample_wave_data_with_signals):
        """Test that signals have correct alpha and zorder values."""
        with patch('matplotlib.pyplot.show'):
            with patch('matplotlib.axes.Axes.scatter') as mock_scatter:
                plot_dual_chart_mpl(
                    sample_wave_data_with_signals,
                    'wave:339,10,2,fast,22,11,4,fast,prime,10,close',
                    'Test Wave Colors - MPL Mode'
                )
                
                # Check alpha and zorder for all signal calls
                for call in mock_scatter.call_args_list:
                    if 'Wave BUY' in str(call[1].get('label', '')) or 'Wave SELL' in str(call[1].get('label', '')):
                        assert call[1].get('alpha') == 0.9, "Signals should have alpha=0.9"
                        assert call[1].get('zorder') == 5, "Signals should have zorder=5"
                        assert call[1].get('s') == 100, "Signals should have size=100"


if __name__ == "__main__":
    pytest.main([__file__])
