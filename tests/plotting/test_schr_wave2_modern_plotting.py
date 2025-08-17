# -*- coding: utf-8 -*-
# tests/plotting/test_schr_wave2_modern_plotting.py

"""
Test SCHR Wave2 plotting with buy/sell signals and color-changing wave lines.
Tests the updated add_schr_wave2_indicator function for complete functionality.
"""

import pytest
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from unittest.mock import patch, MagicMock

from src.plotting.dual_chart_fastest import add_schr_wave2_indicator
from src.common.constants import BUY, SELL, NOTRADE


class TestSCHRWave2CompletePlotting:
    """Test class for complete SCHR Wave2 plotting functionality."""
    
    @pytest.fixture
    def sample_data(self):
        """Create sample data for testing."""
        dates = pd.date_range('2024-01-01', periods=100, freq='D')
        np.random.seed(42)
        
        data = {
            'Open': np.random.uniform(1.2000, 1.3000, 100),
            'High': np.random.uniform(1.2100, 1.3100, 100),
            'Low': np.random.uniform(1.1900, 1.2900, 100),
            'Close': np.random.uniform(1.2000, 1.3000, 100),
            'Volume': np.random.randint(1000, 10000, 100),
            'schr_wave2_wave': np.random.uniform(-0.3, 0.3, 100),
            'schr_wave2_fast_line': np.random.uniform(-0.25, 0.25, 100),
            'schr_wave2_ma_line': np.random.uniform(-0.2, 0.2, 100),
            'schr_wave2_direction': np.random.choice([1, 2], 100),
            'schr_wave2_signal': np.random.choice([0, 1, 2], 100)
        }
        
        df = pd.DataFrame(data, index=dates)
        return df
    
    @pytest.fixture
    def mock_figure(self):
        """Create a mock Plotly figure for testing."""
        fig = make_subplots(
            rows=2, cols=1,
            subplot_titles=('Price Chart', 'SCHR Wave2'),
            vertical_spacing=0.1
        )
        return fig
    
    def test_buy_signals_on_upper_chart(self, sample_data, mock_figure):
        """Test that buy signals (green triangles) are added to upper chart."""
        # Add indicator
        add_schr_wave2_indicator(mock_figure, sample_data)
        
        # Check that buy signals were added to row 1 (upper chart)
        upper_chart_traces = [trace for trace in mock_figure.data if trace.yaxis == 'y']
        buy_signals = [trace for trace in upper_chart_traces if 'Buy Signal' in trace.name]
        assert len(buy_signals) > 0, "Buy signals should be added to upper chart"
        
        # Check buy signal properties
        buy_trace = buy_signals[0]
        assert buy_trace.marker.color == 'green', "Buy signals should be green"
        assert buy_trace.marker.symbol == 'triangle-up', "Buy signals should be upward triangles"
    
    def test_sell_signals_on_upper_chart(self, sample_data, mock_figure):
        """Test that sell signals (red triangles) are added to upper chart."""
        # Add indicator
        add_schr_wave2_indicator(mock_figure, sample_data)
        
        # Check that sell signals were added to row 1 (upper chart)
        upper_chart_traces = [trace for trace in mock_figure.data if trace.yaxis == 'y']
        sell_signals = [trace for trace in upper_chart_traces if 'Sell Signal' in trace.name]
        assert len(sell_signals) > 0, "Sell signals should be added to upper chart"
        
        # Check sell signal properties
        sell_trace = sell_signals[0]
        assert sell_trace.marker.color == 'red', "Sell signals should be red"
        assert sell_trace.marker.symbol == 'triangle-down', "Sell signals should be downward triangles"
    
    def test_wave_lines_with_color_changes(self, sample_data, mock_figure):
        """Test that wave lines change color based on positive/negative values."""
        # Add indicator
        add_schr_wave2_indicator(mock_figure, sample_data)
        
        # Check that wave lines are added to lower chart (row 2)
        lower_chart_traces = [trace for trace in mock_figure.data if trace.yaxis == 'y2']
        wave_traces = [trace for trace in lower_chart_traces if 'Wave' in trace.name]
        
        # Should have positive and negative wave traces
        positive_wave = [trace for trace in wave_traces if 'Positive' in trace.name]
        negative_wave = [trace for trace in wave_traces if 'Negative' in trace.name]
        
        assert len(positive_wave) > 0, "Positive wave trace should exist"
        assert len(negative_wave) > 0, "Negative wave trace should exist"
        
        # Check colors
        assert positive_wave[0].line.color == 'blue', "Positive wave should be blue"
        assert negative_wave[0].line.color == 'red', "Negative wave should be red"
    
    def test_fast_line_always_orange(self, sample_data, mock_figure):
        """Test that fast line is always orange."""
        # Add indicator
        add_schr_wave2_indicator(mock_figure, sample_data)
        
        # Check fast line
        lower_chart_traces = [trace for trace in mock_figure.data if trace.yaxis == 'y2']
        fast_line_traces = [trace for trace in lower_chart_traces if 'Fast Line' in trace.name]
        
        assert len(fast_line_traces) > 0, "Fast line should exist"
        assert fast_line_traces[0].line.color == 'orange', "Fast line should always be orange"
    
    def test_ma_line_always_yellow(self, sample_data, mock_figure):
        """Test that MA line is always yellow."""
        # Add indicator
        add_schr_wave2_indicator(mock_figure, sample_data)
        
        # Check MA line
        lower_chart_traces = [trace for trace in mock_figure.data if trace.yaxis == 'y2']
        ma_line_traces = [trace for trace in lower_chart_traces if 'MA Line' in trace.name]
        
        assert len(ma_line_traces) > 0, "MA line should exist"
        assert ma_line_traces[0].line.color == 'yellow', "MA line should always be yellow"
    
    def test_wave_lines_present_on_lower_chart(self, sample_data, mock_figure):
        """Test that wave lines are properly displayed on lower chart."""
        # Add indicator
        add_schr_wave2_indicator(mock_figure, sample_data)
        
        # Check that wave lines are added to lower chart (row 2)
        lower_chart_traces = [trace for trace in mock_figure.data if trace.yaxis == 'y2']
        
        # Should have wave lines + fast line + ma line + zero line
        assert len(lower_chart_traces) >= 4, "Should have at least 4 traces on lower chart"
        
        # Check for specific wave lines
        wave_names = [trace.name for trace in lower_chart_traces]
        assert any('Wave' in name for name in wave_names), "Wave lines should be present"
        assert any('Fast Line' in name for name in wave_names), "Fast line should be present"
        assert any('MA Line' in name for name in wave_names), "MA line should be present"
    
    def test_modern_line_styling(self, sample_data, mock_figure):
        """Test that wave lines use modern styling with spline curves."""
        # Add indicator
        add_schr_wave2_indicator(mock_figure, sample_data)
        
        # Check wave line styling (only actual wave lines, not fast line)
        lower_chart_traces = [trace for trace in mock_figure.data if trace.yaxis == 'y2']
        wave_traces = [trace for trace in lower_chart_traces if 'Wave' in trace.name and 'Fast' not in trace.name and 'MA' not in trace.name]
        
        for trace in wave_traces:
            assert trace.line.shape == 'spline', "Wave lines should use spline curves"
            assert trace.line.width == 3, "Wave lines should have width 3"
        
        # Check fast line styling
        fast_trace = next((trace for trace in lower_chart_traces if 'Fast Line' in trace.name), None)
        assert fast_trace is not None, "Fast line trace should exist"
        assert fast_trace.line.shape == 'spline', "Fast line should use spline curves"
        assert fast_trace.line.width == 2.5, "Fast line should have width 2.5"
        
        # Check MA line styling
        ma_trace = next((trace for trace in lower_chart_traces if 'MA Line' in trace.name), None)
        assert ma_trace is not None, "MA line trace should exist"
        assert ma_trace.line.shape == 'spline', "MA line should use spline curves"
        assert ma_trace.line.width == 2, "MA line should have width 2"
    
    def test_legend_enabled_for_wave_lines(self, sample_data, mock_figure):
        """Test that legend is enabled for wave lines."""
        # Add indicator
        add_schr_wave2_indicator(mock_figure, sample_data)
        
        # Check that wave lines have showlegend=True
        lower_chart_traces = [trace for trace in mock_figure.data if trace.yaxis == 'y2']
        wave_traces = [trace for trace in lower_chart_traces if 'SCHR_Wave2' in trace.name]
        for trace in wave_traces:
            assert trace.showlegend is True, f"Trace {trace.name} should show in legend"
    
    def test_zero_line_styling(self, sample_data, mock_figure):
        """Test that zero line has modern styling."""
        # Add indicator
        add_schr_wave2_indicator(mock_figure, sample_data)
        
        # Check zero line properties
        assert mock_figure.layout.yaxis2.zeroline is True, "Zero line should be enabled"
        assert mock_figure.layout.yaxis2.zerolinecolor == '#636363', "Zero line should use modern gray"
    
    def test_axis_styling(self, sample_data, mock_figure):
        """Test that y-axis has modern styling."""
        # Add indicator
        add_schr_wave2_indicator(mock_figure, sample_data)
        
        # Check y-axis properties
        yaxis = mock_figure.layout.yaxis2
        assert yaxis.title.text == "SCHR Wave2", "Y-axis title should be set"
        assert yaxis.range == (-0.5, 0.5), "Y-axis range should be set"
        assert yaxis.gridcolor == 'rgba(0,0,0,0.08)', "Grid should use subtle color"
        assert yaxis.zerolinecolor == '#636363', "Zero line should use modern gray"
    
    def test_legend_positioning(self, sample_data, mock_figure):
        """Test that legend is positioned correctly."""
        # Add indicator
        add_schr_wave2_indicator(mock_figure, sample_data)
        
        # Check legend properties
        legend = mock_figure.layout.legend
        assert legend.x == 0.02, "Legend should be positioned at x=0.02"
        assert legend.y == 0.98, "Legend should be positioned at y=0.98"
        assert legend.bgcolor == 'rgba(255,255,255,0.9)', "Legend should have semi-transparent white background"
    
    def test_missing_data_handling(self, mock_figure):
        """Test handling of missing SCHR Wave2 data."""
        # Create data without SCHR Wave2 columns
        empty_data = pd.DataFrame({
            'Open': [1.2000, 1.2100],
            'High': [1.2100, 1.2200],
            'Low': [1.1900, 1.2000],
            'Close': [1.2000, 1.2100]
        })
        
        # Should not raise error and should not add any traces
        add_schr_wave2_indicator(mock_figure, empty_data)
        
        # No traces should be added
        assert len(mock_figure.data) == 0, "No traces should be added for missing data"
    
    def test_performance_logging(self, sample_data, mock_figure, caplog):
        """Test that performance logging is working."""
        with patch('src.common.logger.print_info') as mock_logger:
            add_schr_wave2_indicator(mock_figure, sample_data)
            
            # Check that performance logging was called
            assert mock_logger.call_count >= 2, "Should log start and completion"
            
            # Check for specific log messages
            log_calls = [call.args[0] for call in mock_logger.call_args_list]
            assert any('Starting SCHR_Wave2 indicator addition' in call for call in log_calls), "Should log start"
            assert any('SCHR_Wave2 indicator addition completed' in call for call in log_calls), "Should log completion"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
