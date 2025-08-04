# -*- coding: utf-8 -*-
"""
Test for SR lines addition in fast_plot.py

This test verifies that support and resistance lines are properly added to the main chart
in fast mode for SR rule.
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


class TestSRLinesAddition:
    """Test class for SR lines addition in fast mode."""
    
    @pytest.fixture
    def sample_data(self):
        """Create sample data with PPrice1 and PPrice2 columns."""
        dates = pd.date_range('2020-01-01', periods=100, freq='D')
        data = {
            'Open': [1.0 + i * 0.001 for i in range(100)],
            'High': [1.1 + i * 0.001 for i in range(100)],
            'Low': [0.9 + i * 0.001 for i in range(100)],
            'Close': [1.05 + i * 0.001 for i in range(100)],
            'Volume': [1000 + i * 10 for i in range(100)],
            'PPrice1': [0.95 + i * 0.001 for i in range(100)],  # Support line
            'PPrice2': [1.15 + i * 0.001 for i in range(100)],  # Resistance line
            'Direction': [0] * 100  # No signals
        }
        return pd.DataFrame(data, index=dates)
    
    @pytest.fixture
    def mock_rule(self):
        """Create a mock rule object."""
        rule = Mock()
        rule.name = "SR"
        rule.original_rule_with_params = "SR"
        return rule
    
    def test_sr_lines_addition(self, sample_data, mock_rule):
        """Test that support and resistance lines are properly added."""
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
            
            mock_figure.side_effect = [
                mock_main_fig,  # Main figure
                mock_volume_fig,  # Volume figure
                mock_hl_fig,  # HL figure
                mock_pressure_fig,  # Pressure figure
                mock_pv_fig  # PV figure
            ]
            
            # Mock layout functions
            mock_column.return_value = Mock()
            
            # Track calls to main_fig.line
            line_calls = []
            def track_line_calls(*args, **kwargs):
                line_calls.append(kwargs)
                return Mock()
            
            mock_main_fig.line.side_effect = track_line_calls
            
            # Call the function
            result = plot_indicator_results_fast(sample_data, mock_rule)
            
            # Verify that line calls were made for support and resistance
            assert len(line_calls) >= 2, "Should have at least 2 line calls for support and resistance"
            
            # Check for support line (PPrice1)
            support_calls = [call for call in line_calls if 'PPrice1' in str(call)]
            assert len(support_calls) > 0, "Support line (PPrice1) should be added"
            
            # Check for resistance line (PPrice2)
            resistance_calls = [call for call in line_calls if 'PPrice2' in str(call)]
            assert len(resistance_calls) > 0, "Resistance line (PPrice2) should be added"
            
            # Verify line properties
            for call in line_calls:
                if 'PPrice1' in str(call):
                    assert call.get('line_color') == 'blue', "Support line should be blue"
                    assert call.get('legend_label') == 'Support', "Support line should have correct legend"
                elif 'PPrice2' in str(call):
                    assert call.get('line_color') == 'red', "Resistance line should be red"
                    assert call.get('legend_label') == 'Resistance', "Resistance line should have correct legend"
    
    def test_sr_lines_without_columns(self, sample_data, mock_rule):
        """Test that no errors occur when PPrice1/PPrice2 columns are missing."""
        # Remove PPrice1 and PPrice2 columns
        sample_data_no_sr = sample_data.drop(['PPrice1', 'PPrice2'], axis=1)
        
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
            
            mock_figure.side_effect = [
                mock_main_fig,  # Main figure
                mock_volume_fig,  # Volume figure
                mock_hl_fig,  # HL figure
                mock_pressure_fig,  # Pressure figure
                mock_pv_fig  # PV figure
            ]
            
            # Mock layout functions
            mock_column.return_value = Mock()
            
            # Call the function - should not raise any errors
            result = plot_indicator_results_fast(sample_data_no_sr, mock_rule)
            
            # Verify that the function completes successfully
            assert result is not None, "Function should complete successfully even without SR columns"


if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 