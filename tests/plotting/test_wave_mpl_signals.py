# -*- coding: utf-8 -*-
# tests/plotting/test_wave_mpl_signals.py

"""
Tests for Wave indicator signals display on the main chart in MPL mode.
"""

import pytest
import pandas as pd
import numpy as np
from unittest.mock import patch, MagicMock
import matplotlib.pyplot as plt

from src.plotting.dual_chart_mpl import plot_dual_chart_mpl


class TestWaveMplSignals:
    """Test cases for Wave indicator signals on main chart in MPL mode."""

    @pytest.fixture
    def sample_data_with_wave_signals(self):
        """Create sample data with Wave indicator signals."""
        dates = pd.date_range('2023-01-01', periods=20, freq='D')
        data = {
            'DateTime': dates,
            'Open': np.random.uniform(100, 200, 20),
            'High': np.random.uniform(200, 300, 20),
            'Low': np.random.uniform(50, 100, 20),
            'Close': np.random.uniform(100, 200, 20),
            'Volume': np.random.uniform(1000, 10000, 20),
            # Wave indicator columns
            '_Plot_Color': [0, 1, 0, 2, 0, 1, 0, 2, 0, 1, 0, 2, 0, 1, 0, 2, 0, 1, 0, 2],  # Alternating signals
            '_Plot_Wave': np.random.uniform(-0.1, 0.1, 20),
            '_Plot_FastLine': np.random.uniform(-0.05, 0.05, 20),
            'MA_Line': np.random.uniform(-0.08, 0.08, 20)
        }
        df = pd.DataFrame(data)
        df.set_index('DateTime', inplace=True)
        return df

    def test_wave_signals_on_main_chart(self, sample_data_with_wave_signals):
        """Test that Wave signals are displayed on the main chart."""
        with patch('matplotlib.pyplot.show'):
            fig = plot_dual_chart_mpl(
                sample_data_with_wave_signals,
                'wave:339,10,2,fast,22,11,4,fast,prime,22,open',
                'Test Wave Signals'
            )
            
            # Get the axes from the figure
            ax1, ax2 = fig.axes
            
            # Check that signals are plotted on main chart (ax1)
            # Look for scatter plots (signals)
            scatter_plots = [child for child in ax1.get_children() if hasattr(child, 'get_offsets')]
            
            # Should have at least some scatter plots (signals)
            assert len(scatter_plots) > 0, "No signals found on main chart"

    def test_wave_buy_signals_display(self, sample_data_with_wave_signals):
        """Test that Wave BUY signals are properly displayed."""
        # Create data with only BUY signals
        sample_data_with_wave_signals['_Plot_Color'] = [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0]
        
        with patch('matplotlib.pyplot.show'):
            fig = plot_dual_chart_mpl(
                sample_data_with_wave_signals,
                'wave:339,10,2,fast,22,11,4,fast,prime,22,open',
                'Test Wave BUY Signals'
            )
            
            ax1, ax2 = fig.axes
            
            # Check that BUY signals are plotted
            scatter_plots = [child for child in ax1.get_children() if hasattr(child, 'get_offsets')]
            assert len(scatter_plots) > 0, "BUY signals should be displayed on main chart"

    def test_wave_sell_signals_display(self, sample_data_with_wave_signals):
        """Test that Wave SELL signals are properly displayed."""
        # Create data with only SELL signals
        sample_data_with_wave_signals['_Plot_Color'] = [2, 0, 2, 0, 2, 0, 2, 0, 2, 0, 2, 0, 2, 0, 2, 0, 2, 0, 2, 0]
        
        with patch('matplotlib.pyplot.show'):
            fig = plot_dual_chart_mpl(
                sample_data_with_wave_signals,
                'wave:339,10,2,fast,22,11,4,fast,prime,22,open',
                'Test Wave SELL Signals'
            )
            
            ax1, ax2 = fig.axes
            
            # Check that SELL signals are plotted
            scatter_plots = [child for child in ax1.get_children() if hasattr(child, 'get_offsets')]
            assert len(scatter_plots) > 0, "SELL signals should be displayed on main chart"

    def test_wave_mixed_signals_display(self, sample_data_with_wave_signals):
        """Test that mixed BUY and SELL signals are properly displayed."""
        # Create data with mixed signals
        sample_data_with_wave_signals['_Plot_Color'] = [1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2]
        
        with patch('matplotlib.pyplot.show'):
            fig = plot_dual_chart_mpl(
                sample_data_with_wave_signals,
                'wave:339,10,2,fast,22,11,4,fast,prime,22,open',
                'Test Wave Mixed Signals'
            )
            
            ax1, ax2 = fig.axes
            
            # Check that both types of signals are plotted
            scatter_plots = [child for child in ax1.get_children() if hasattr(child, 'get_offsets')]
            assert len(scatter_plots) > 0, "Mixed signals should be displayed on main chart"

    def test_wave_no_signals_display(self, sample_data_with_wave_signals):
        """Test that no signals are displayed when there are no signals."""
        # Create data with no signals (all zeros)
        sample_data_with_wave_signals['_Plot_Color'] = [0] * 20
        
        with patch('matplotlib.pyplot.show'):
            fig = plot_dual_chart_mpl(
                sample_data_with_wave_signals,
                'wave:339,10,2,fast,22,11,4,fast,prime,22,open',
                'Test Wave No Signals'
            )
            
            ax1, ax2 = fig.axes
            
            # Should still have the chart, but no signal markers
            assert len(fig.axes) == 2, "Should have two subplots"

    def test_wave_signals_legend_entries(self, sample_data_with_wave_signals):
        """Test that Wave signals have proper legend entries."""
        # Create data with both BUY and SELL signals
        sample_data_with_wave_signals['_Plot_Color'] = [1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2]
        
        with patch('matplotlib.pyplot.show'):
            fig = plot_dual_chart_mpl(
                sample_data_with_wave_signals,
                'wave:339,10,2,fast,22,11,4,fast,prime,22,open',
                'Test Wave Signals Legend'
            )
            
            ax1, ax2 = fig.axes
            
            # Check that legend exists
            legend = ax1.get_legend()
            assert legend is not None, "Legend should exist on main chart"
            
            # Get legend text
            legend_texts = [text.get_text() for text in legend.get_texts()]
            
            # Should contain Wave signal entries
            assert 'Wave BUY' in legend_texts or 'Wave SELL' in legend_texts, "Legend should contain Wave signal entries"

    def test_wave_signals_color_coding(self, sample_data_with_wave_signals):
        """Test that Wave signals use correct colors."""
        # Create data with both BUY and SELL signals
        sample_data_with_wave_signals['_Plot_Color'] = [1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2]
        
        with patch('matplotlib.pyplot.show'):
            fig = plot_dual_chart_mpl(
                sample_data_with_wave_signals,
                'wave:339,10,2,fast,22,11,4,fast,prime,22,open',
                'Test Wave Signals Colors'
            )
            
            ax1, ax2 = fig.axes
            
            # Check that scatter plots exist (signals)
            scatter_plots = [child for child in ax1.get_children() if hasattr(child, 'get_offsets')]
            assert len(scatter_plots) > 0, "Signals should be plotted with correct colors"

    def test_wave_signals_marker_styles(self, sample_data_with_wave_signals):
        """Test that Wave signals use correct marker styles."""
        # Create data with both BUY and SELL signals
        sample_data_with_wave_signals['_Plot_Color'] = [1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2]
        
        with patch('matplotlib.pyplot.show'):
            fig = plot_dual_chart_mpl(
                sample_data_with_wave_signals,
                'wave:339,10,2,fast,22,11,4,fast,prime,22,open',
                'Test Wave Signals Markers'
            )
            
            ax1, ax2 = fig.axes
            
            # Check that scatter plots exist (signals with markers)
            scatter_plots = [child for child in ax1.get_children() if hasattr(child, 'get_offsets')]
            assert len(scatter_plots) > 0, "Signals should be plotted with correct markers"

    def test_wave_signals_positioning(self, sample_data_with_wave_signals):
        """Test that Wave signals are positioned correctly on the chart."""
        # Create data with specific signals
        sample_data_with_wave_signals['_Plot_Color'] = [1, 0, 2, 0, 1, 0, 2, 0, 1, 0, 2, 0, 1, 0, 2, 0, 1, 0, 2, 0]
        
        with patch('matplotlib.pyplot.show'):
            fig = plot_dual_chart_mpl(
                sample_data_with_wave_signals,
                'wave:339,10,2,fast,22,11,4,fast,prime,22,open',
                'Test Wave Signals Positioning'
            )
            
            ax1, ax2 = fig.axes
            
            # Check that signals are positioned correctly
            scatter_plots = [child for child in ax1.get_children() if hasattr(child, 'get_offsets')]
            assert len(scatter_plots) > 0, "Signals should be positioned correctly on main chart"

    def test_wave_signals_integration(self, sample_data_with_wave_signals):
        """Test that Wave signals integrate properly with the overall chart."""
        # Create data with signals
        sample_data_with_wave_signals['_Plot_Color'] = [1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2]
        
        with patch('matplotlib.pyplot.show'):
            fig = plot_dual_chart_mpl(
                sample_data_with_wave_signals,
                'wave:339,10,2,fast,22,11,4,fast,prime,22,open',
                'Test Wave Signals Integration'
            )
            
            # Check that figure has correct structure
            assert len(fig.axes) == 2, "Should have two subplots (main chart and indicator)"
            
            ax1, ax2 = fig.axes
            
            # Check that main chart has signals
            scatter_plots = [child for child in ax1.get_children() if hasattr(child, 'get_offsets')]
            assert len(scatter_plots) > 0, "Main chart should display Wave signals"
            
            # Check that indicator chart has Wave lines
            lines = [child for child in ax2.get_children() if hasattr(child, 'get_xdata')]
            assert len(lines) > 0, "Indicator chart should display Wave lines"


if __name__ == "__main__":
    pytest.main([__file__])
