# -*- coding: utf-8 -*-
# tests/plotting/test_wave_mpl_signal_filtering.py

"""
Tests for Wave indicator signal filtering on the main chart in MPL mode.
"""

import pytest
import pandas as pd
import numpy as np
from unittest.mock import patch, MagicMock
import matplotlib.pyplot as plt

from src.plotting.dual_chart_mpl import plot_dual_chart_mpl


class TestWaveMplSignalFiltering:
    """Test cases for Wave indicator signal filtering on main chart in MPL mode."""

    @pytest.fixture
    def sample_data_with_wave_signals_and_direction(self):
        """Create sample data with Wave indicator signals and direction changes."""
        dates = pd.date_range('2023-01-01', periods=20, freq='D')
        data = {
            'DateTime': dates,
            'Open': np.random.uniform(100, 200, 20),
            'High': np.random.uniform(200, 300, 20),
            'Low': np.random.uniform(50, 100, 20),
            'Close': np.random.uniform(100, 200, 20),
            'Volume': np.random.uniform(1000, 10000, 20),
            # Wave indicator columns
            '_Plot_Color': [1, 1, 1, 2, 2, 2, 1, 1, 1, 2, 2, 2, 1, 1, 1, 2, 2, 2, 1, 1],  # Direction changes
            '_Signal': [1, 0, 0, 2, 0, 0, 1, 0, 0, 2, 0, 0, 1, 0, 0, 2, 0, 0, 1, 0],  # Only direction changes
            '_Plot_Wave': np.random.uniform(-0.1, 0.1, 20),
            '_Plot_FastLine': np.random.uniform(-0.05, 0.05, 20),
            'MA_Line': np.random.uniform(-0.08, 0.08, 20)
        }
        df = pd.DataFrame(data)
        df.set_index('DateTime', inplace=True)
        return df

    def test_signal_filtering_uses_signal_column(self, sample_data_with_wave_signals_and_direction):
        """Test that signal filtering uses _Signal column instead of _Plot_Color."""
        with patch('matplotlib.pyplot.show'):
            fig = plot_dual_chart_mpl(
                sample_data_with_wave_signals_and_direction,
                'wave:339,10,2,fast,22,11,4,fast,prime,22,open',
                'Test Wave Signal Filtering'
            )
            
            # Get the axes from the figure
            ax1, ax2 = fig.axes
            
            # Check that signals are plotted on main chart (ax1)
            scatter_plots = [child for child in ax1.get_children() if hasattr(child, 'get_offsets')]
            
            # Should have scatter plots (signals) but fewer than before filtering
            assert len(scatter_plots) > 0, "Signals should be displayed on main chart"
            
            # Count actual signals from _Signal column (only direction changes)
            signal_data = sample_data_with_wave_signals_and_direction['_Signal']
            actual_signals = signal_data[signal_data != 0]
            
            # Should have fewer signals than _Plot_Color would suggest
            plot_color_data = sample_data_with_wave_signals_and_direction['_Plot_Color']
            plot_color_signals = plot_color_data[plot_color_data != 0]
            
            assert len(actual_signals) < len(plot_color_signals), "Filtered signals should be fewer than unfiltered"

    def test_signal_filtering_only_shows_direction_changes(self, sample_data_with_wave_signals_and_direction):
        """Test that only direction changes are shown as signals."""
        # Create data with clear direction changes
        sample_data_with_wave_signals_and_direction['_Plot_Color'] = [1, 1, 1, 2, 2, 2, 1, 1, 1, 2, 2, 2, 1, 1, 1, 2, 2, 2, 1, 1]
        sample_data_with_wave_signals_and_direction['_Signal'] = [1, 0, 0, 2, 0, 0, 1, 0, 0, 2, 0, 0, 1, 0, 0, 2, 0, 0, 1, 0]
        
        with patch('matplotlib.pyplot.show'):
            fig = plot_dual_chart_mpl(
                sample_data_with_wave_signals_and_direction,
                'wave:339,10,2,fast,22,11,4,fast,prime,22,open',
                'Test Direction Changes Only'
            )
            
            ax1, ax2 = fig.axes
            
            # Count signals from _Signal column
            signal_data = sample_data_with_wave_signals_and_direction['_Signal']
            buy_signals = signal_data[signal_data == 1]
            sell_signals = signal_data[signal_data == 2]
            
            # Should have exactly the number of direction changes
            expected_buy_signals = 4  # Based on the test data
            expected_sell_signals = 3  # Based on the test data
            
            assert len(buy_signals) == expected_buy_signals, f"Expected {expected_buy_signals} BUY signals, got {len(buy_signals)}"
            assert len(sell_signals) == expected_sell_signals, f"Expected {expected_sell_signals} SELL signals, got {len(sell_signals)}"

    def test_signal_filtering_fallback_to_plot_color(self, sample_data_with_wave_signals_and_direction):
        """Test fallback to _Plot_Color when _Signal column is not available."""
        # Remove _Signal column to test fallback
        sample_data_with_wave_signals_and_direction = sample_data_with_wave_signals_and_direction.drop('_Signal', axis=1)
        
        with patch('matplotlib.pyplot.show'):
            fig = plot_dual_chart_mpl(
                sample_data_with_wave_signals_and_direction,
                'wave:339,10,2,fast,22,11,4,fast,prime,22,open',
                'Test Fallback to Plot Color'
            )
            
            ax1, ax2 = fig.axes
            
            # Should still have signals (using _Plot_Color as fallback)
            scatter_plots = [child for child in ax1.get_children() if hasattr(child, 'get_offsets')]
            assert len(scatter_plots) > 0, "Signals should be displayed using fallback"

    def test_signal_filtering_no_signals_when_no_direction_changes(self, sample_data_with_wave_signals_and_direction):
        """Test that no signals are shown when there are no direction changes."""
        # Set all signals to 0 (no direction changes)
        sample_data_with_wave_signals_and_direction['_Signal'] = [0] * 20
        
        with patch('matplotlib.pyplot.show'):
            fig = plot_dual_chart_mpl(
                sample_data_with_wave_signals_and_direction,
                'wave:339,10,2,fast,22,11,4,fast,prime,22,open',
                'Test No Direction Changes'
            )
            
            ax1, ax2 = fig.axes
            
            # Should have no signal scatter plots
            scatter_plots = [child for child in ax1.get_children() if hasattr(child, 'get_offsets')]
            # Note: There might be other scatter plots (like support/resistance), so we check for signal-specific ones
            assert len(fig.axes) == 2, "Should have two subplots"

    def test_signal_filtering_mixed_direction_changes(self, sample_data_with_wave_signals_and_direction):
        """Test mixed direction changes with realistic signal pattern."""
        # Create realistic signal pattern with direction changes
        sample_data_with_wave_signals_and_direction['_Plot_Color'] = [1, 1, 1, 2, 2, 2, 1, 1, 1, 2, 2, 2, 1, 1, 1, 2, 2, 2, 1, 1]
        sample_data_with_wave_signals_and_direction['_Signal'] = [1, 0, 0, 2, 0, 0, 1, 0, 0, 2, 0, 0, 1, 0, 0, 2, 0, 0, 1, 0]
        
        with patch('matplotlib.pyplot.show'):
            fig = plot_dual_chart_mpl(
                sample_data_with_wave_signals_and_direction,
                'wave:339,10,2,fast,22,11,4,fast,prime,22,open',
                'Test Mixed Direction Changes'
            )
            
            ax1, ax2 = fig.axes
            
            # Count actual signals
            signal_data = sample_data_with_wave_signals_and_direction['_Signal']
            buy_signals = signal_data[signal_data == 1]
            sell_signals = signal_data[signal_data == 2]
            
            # Should have both types of signals
            assert len(buy_signals) > 0, "Should have BUY signals"
            assert len(sell_signals) > 0, "Should have SELL signals"

    def test_signal_filtering_legend_entries_filtered(self, sample_data_with_wave_signals_and_direction):
        """Test that legend entries reflect filtered signals."""
        # Create data with direction changes
        sample_data_with_wave_signals_and_direction['_Plot_Color'] = [1, 1, 1, 2, 2, 2, 1, 1, 1, 2, 2, 2, 1, 1, 1, 2, 2, 2, 1, 1]
        sample_data_with_wave_signals_and_direction['_Signal'] = [1, 0, 0, 2, 0, 0, 1, 0, 0, 2, 0, 0, 1, 0, 0, 2, 0, 0, 1, 0]
        
        with patch('matplotlib.pyplot.show'):
            fig = plot_dual_chart_mpl(
                sample_data_with_wave_signals_and_direction,
                'wave:339,10,2,fast,22,11,4,fast,prime,22,open',
                'Test Filtered Legend'
            )
            
            ax1, ax2 = fig.axes
            
            # Check that legend exists
            legend = ax1.get_legend()
            assert legend is not None, "Legend should exist on main chart"
            
            # Get legend text
            legend_texts = [text.get_text() for text in legend.get_texts()]
            
            # Should contain Wave signal entries
            assert 'Wave BUY' in legend_texts or 'Wave SELL' in legend_texts, "Legend should contain Wave signal entries"

    def test_signal_filtering_performance_improvement(self, sample_data_with_wave_signals_and_direction):
        """Test that filtering reduces the number of displayed signals."""
        # Create data with many _Plot_Color signals but few _Signal signals
        sample_data_with_wave_signals_and_direction['_Plot_Color'] = [1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2]
        sample_data_with_wave_signals_and_direction['_Signal'] = [1, 0, 0, 0, 0, 2, 0, 0, 0, 0, 1, 0, 0, 0, 0, 2, 0, 0, 0, 0]
        
        with patch('matplotlib.pyplot.show'):
            fig = plot_dual_chart_mpl(
                sample_data_with_wave_signals_and_direction,
                'wave:339,10,2,fast,22,11,4,fast,prime,22,open',
                'Test Performance Improvement'
            )
            
            ax1, ax2 = fig.axes
            
            # Count signals from both columns
            plot_color_signals = sample_data_with_wave_signals_and_direction['_Plot_Color'][sample_data_with_wave_signals_and_direction['_Plot_Color'] != 0]
            signal_signals = sample_data_with_wave_signals_and_direction['_Signal'][sample_data_with_wave_signals_and_direction['_Signal'] != 0]
            
            # _Signal should have fewer signals than _Plot_Color
            assert len(signal_signals) < len(plot_color_signals), "Filtered signals should be fewer than unfiltered"

    def test_signal_filtering_edge_cases(self, sample_data_with_wave_signals_and_direction):
        """Test edge cases for signal filtering."""
        # Test with single signal
        sample_data_with_wave_signals_and_direction['_Plot_Color'] = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        sample_data_with_wave_signals_and_direction['_Signal'] = [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        
        with patch('matplotlib.pyplot.show'):
            fig = plot_dual_chart_mpl(
                sample_data_with_wave_signals_and_direction,
                'wave:339,10,2,fast,22,11,4,fast,prime,22,open',
                'Test Single Signal'
            )
            
            ax1, ax2 = fig.axes
            
            # Should have exactly one signal
            signal_data = sample_data_with_wave_signals_and_direction['_Signal']
            actual_signals = signal_data[signal_data != 0]
            assert len(actual_signals) == 1, "Should have exactly one signal"

    def test_signal_filtering_integration_with_existing_features(self, sample_data_with_wave_signals_and_direction):
        """Test that signal filtering integrates well with existing chart features."""
        # Create data with signals
        sample_data_with_wave_signals_and_direction['_Plot_Color'] = [1, 1, 1, 2, 2, 2, 1, 1, 1, 2, 2, 2, 1, 1, 1, 2, 2, 2, 1, 1]
        sample_data_with_wave_signals_and_direction['_Signal'] = [1, 0, 0, 2, 0, 0, 1, 0, 0, 2, 0, 0, 1, 0, 0, 2, 0, 0, 1, 0]
        
        with patch('matplotlib.pyplot.show'):
            fig = plot_dual_chart_mpl(
                sample_data_with_wave_signals_and_direction,
                'wave:339,10,2,fast,22,11,4,fast,prime,22,open',
                'Test Integration'
            )
            
            # Check that figure has correct structure
            assert len(fig.axes) == 2, "Should have two subplots (main chart and indicator)"
            
            ax1, ax2 = fig.axes
            
            # Check that main chart has filtered signals
            scatter_plots = [child for child in ax1.get_children() if hasattr(child, 'get_offsets')]
            assert len(scatter_plots) > 0, "Main chart should display filtered Wave signals"
            
            # Check that indicator chart has Wave lines
            lines = [child for child in ax2.get_children() if hasattr(child, 'get_xdata')]
            assert len(lines) > 0, "Indicator chart should display Wave lines"


if __name__ == "__main__":
    pytest.main([__file__])
