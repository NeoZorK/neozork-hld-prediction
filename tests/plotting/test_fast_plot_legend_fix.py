# -*- coding: utf-8 -*-
"""
Test for legend_label fix in fast_plot.py

This test verifies that the legendlabel error is fixed in the fast plotting mode.
"""

import pytest
import pandas as pd
import numpy as np
from unittest.mock import Mock, patch
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from src.plotting.fast_plot import plot_indicator_results_fast


class TestFastPlotLegendFix:
    """Test class for fast plot legend label fix."""
    
    @pytest.fixture
    def sample_data(self):
        """Create sample data for testing."""
        dates = pd.date_range('2020-01-01', periods=100, freq='D')
        data = {
            'Open': [1.0 + i * 0.001 for i in range(100)],
            'High': [1.1 + i * 0.001 for i in range(100)],
            'Low': [0.9 + i * 0.001 for i in range(100)],
            'Close': [1.05 + i * 0.001 for i in range(100)],
            'Volume': [1000 + i * 10 for i in range(100)],
            'supertrend': [1.0 + i * 0.001 for i in range(100)],
            'Direction': [1 if i % 2 == 0 else -1 for i in range(100)]
        }
        df = pd.DataFrame(data, index=dates)
        return df
    
    @pytest.fixture
    def mock_rule(self):
        """Create a mock rule object."""
        rule = Mock()
        rule.name = 'PHLD'
        rule.original_rule_with_params = 'PHLD'
        return rule
    
    def test_supertrend_legend_label_fix(self, sample_data, mock_rule):
        """Test that SuperTrend legend labels are properly handled."""
        # Mock the necessary Bokeh components
        with patch('src.plotting.fast_plot.figure') as mock_figure, \
             patch('src.plotting.fast_plot.output_file') as mock_output_file, \
             patch('src.plotting.fast_plot.save') as mock_save, \
             patch('src.plotting.fast_plot.webbrowser') as mock_webbrowser, \
             patch('src.plotting.fast_plot.os.makedirs') as mock_os_makedirs, \
             patch('src.plotting.fast_plot.column') as mock_column:
            
            # Mock figure objects
            mock_main_fig = Mock()
            mock_volume_fig = Mock()
            mock_hl_fig = Mock()
            mock_pressure_fig = Mock()
            mock_pv_fig = Mock()
            mock_supertrend_fig = Mock()
            
            mock_figure.side_effect = [
                mock_main_fig,  # Main figure
                mock_volume_fig,  # Volume figure
                mock_hl_fig,  # HL figure
                mock_pressure_fig,  # Pressure figure
                mock_pv_fig,  # PV figure
                mock_supertrend_fig  # SuperTrend figure
            ]
            
            # Mock line and scatter methods
            mock_main_fig.line = Mock()
            mock_main_fig.scatter = Mock()
            mock_supertrend_fig.line = Mock()
            mock_supertrend_fig.scatter = Mock()
            
            # Mock column layout
            mock_layout = Mock()
            mock_column.return_value = mock_layout
            
            # Mock ColumnDataSource
            with patch('src.plotting.fast_plot.ColumnDataSource') as mock_cds:
                mock_source = Mock()
                mock_cds.return_value = mock_source
                
                # Call the function
                result = plot_indicator_results_fast(
                    sample_data,
                    mock_rule,
                    title='Test Plot',
                    output_path='test_output.html'
                )
                
                # Verify that the function completed without legend_label errors
                assert result is not None
                
                # Verify that SuperTrend line calls don't have None legend_label
                supertrend_line_calls = mock_supertrend_fig.line.call_args_list
                
                # Check that no line calls have legend_label=None
                for call in supertrend_line_calls:
                    kwargs = call[1] if len(call) > 1 else {}

                    # If legend_label is present, it should be a string
                    if 'legend_label' in kwargs:
                        assert isinstance(kwargs['legend_label'], str), \
                            f"Legend label should be string, got {type(kwargs['legend_label'])}"
                        assert kwargs['legend_label'] != '', \
                            "Legend label should not be empty string"
    
    def test_legend_label_string_validation(self, sample_data, mock_rule):
        """Test that all legend_label values are strings."""
        with patch('src.plotting.fast_plot.figure') as mock_figure, \
             patch('src.plotting.fast_plot.output_file'), \
             patch('src.plotting.fast_plot.save'), \
             patch('src.plotting.fast_plot.webbrowser'), \
             patch('src.plotting.fast_plot.os.makedirs'):
            
            # Mock figure objects
            mock_figs = [Mock() for _ in range(6)]
            mock_figure.side_effect = mock_figs
            
            # Track all line and scatter calls
            all_calls = []
            
            def track_calls(method_name):
                def wrapper(*args, **kwargs):
                    all_calls.append((method_name, (args, kwargs)))
                    return Mock()
                return wrapper
            
            for fig in mock_figs:
                fig.line = track_calls('line')
                fig.scatter = track_calls('scatter')
            
            with patch('src.plotting.fast_plot.ColumnDataSource'):
                # Call the function
                plot_indicator_results_fast(
                    sample_data,
                    mock_rule,
                    title='Test Plot',
                    output_path='test_output.html'
                )
                
                # Check all calls for proper legend_label values
                for method_name, call_args in all_calls:
                    if len(call_args) > 1:  # Has kwargs
                        kwargs = call_args[1]
                        if 'legend_label' in kwargs:
                            legend_label = kwargs['legend_label']
                            assert isinstance(legend_label, str), \
                                f"Legend label in {method_name} should be string, got {type(legend_label)}"
                            assert legend_label != '', \
                                f"Legend label in {method_name} should not be empty"
                            assert legend_label is not None, \
                                f"Legend label in {method_name} should not be None"


if __name__ == '__main__':
    pytest.main([__file__, '-v']) 