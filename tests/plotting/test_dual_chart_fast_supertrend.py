"""
Unit tests for modern SuperTrend styling in dual_chart_fast.py

This module tests the enhanced SuperTrend indicator visualization with:
- Modern color scheme (green/red/golden)
- Glow effects and enhanced styling
- BUY/SELL signal markers
- Transparent trend zones
- Proper hover tool functionality
"""

import pytest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
import sys

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

# Import the functions we want to test
try:
    from src.plotting.dual_chart_fast import _plot_supertrend_indicator, _get_indicator_hover_tool
except ImportError:
    # Fallback for different import paths
    try:
        from plotting.dual_chart_fast import _plot_supertrend_indicator, _get_indicator_hover_tool
    except ImportError:
        # Last resort - direct import
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "dual_chart_fast", 
            os.path.join(os.path.dirname(__file__), '..', '..', 'src', 'plotting', 'dual_chart_fast.py')
        )
        dual_chart_fast = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(dual_chart_fast)
        _plot_supertrend_indicator = dual_chart_fast._plot_supertrend_indicator
        _get_indicator_hover_tool = dual_chart_fast._get_indicator_hover_tool


class TestModernSupertrendStyling:
    """Test class for modern SuperTrend styling functionality."""
    
    @pytest.fixture
    def sample_supertrend_data(self):
        """Create sample SuperTrend data for testing."""
        # Create sample datetime index
        dates = pd.date_range(start='2023-01-01', periods=100, freq='D')
        
        # Create sample OHLCV data
        np.random.seed(42)  # For reproducible tests
        base_price = 1.5000
        
        data = {
            'Open': [base_price + np.random.normal(0, 0.01) for _ in range(100)],
            'High': [base_price + np.random.normal(0.005, 0.01) for _ in range(100)],
            'Low': [base_price + np.random.normal(-0.005, 0.01) for _ in range(100)],
            'Close': [base_price + np.random.normal(0, 0.01) for _ in range(100)],
            'Volume': [np.random.randint(1000, 10000) for _ in range(100)],
            'PPrice1': [base_price + np.random.normal(0, 0.02) for _ in range(100)],
            'PPrice2': [base_price + np.random.normal(0, 0.02) for _ in range(100)],
            'Direction': [np.random.choice([0, 1, 2]) for _ in range(100)]
        }
        
        df = pd.DataFrame(data, index=dates)
        df['index'] = df.index
        return df
    
    @pytest.fixture
    def mock_bokeh_figure(self):
        """Create a mock Bokeh figure for testing."""
        class MockFigure:
            def __init__(self):
                self.lines = []
                self.scatters = []
                self.layouts = []
            
            def line(self, x, y, **kwargs):
                self.lines.append({
                    'x': x, 'y': y,
                    'line_color': kwargs.get('line_color'),
                    'line_width': kwargs.get('line_width'),
                    'line_alpha': kwargs.get('line_alpha'),
                    'legend_label': kwargs.get('legend_label')
                })
            
            def scatter(self, x, y, **kwargs):
                self.scatters.append({
                    'x': x, 'y': y,
                    'size': kwargs.get('size'),
                    'color': kwargs.get('color'),
                    'marker': kwargs.get('marker'),
                    'alpha': kwargs.get('alpha'),
                    'legend_label': kwargs.get('legend_label')
                })
            
            def add_layout(self, layout):
                self.layouts.append(layout)
        
        return MockFigure()
    
    def test_supertrend_indicator_creation(self, sample_supertrend_data, mock_bokeh_figure):
        """Test that SuperTrend indicator is created with modern styling."""
        # Call the function
        _plot_supertrend_indicator(mock_bokeh_figure, None, sample_supertrend_data)
        
        # Verify that lines were drawn
        assert len(mock_bokeh_figure.lines) > 0, "No lines were drawn for SuperTrend"
        
        # Verify that at least one line has the SuperTrend legend label
        supertrend_lines = [line for line in mock_bokeh_figure.lines 
                           if line.get('legend_label') == 'SuperTrend']
        assert len(supertrend_lines) > 0, "No SuperTrend line with legend label found"
    
    def test_modern_color_scheme(self, sample_supertrend_data, mock_bokeh_figure):
        """Test that modern color scheme is applied."""
        _plot_supertrend_indicator(mock_bokeh_figure, None, sample_supertrend_data)
        
        # Check for modern colors
        modern_colors = ['#00C851', '#ff4444', '#FFC107']  # Green, Red, Golden
        
        used_colors = set()
        for line in mock_bokeh_figure.lines:
            if line.get('line_color'):
                used_colors.add(line['line_color'])
        
        # At least one modern color should be used
        assert any(color in used_colors for color in modern_colors), \
            f"Modern colors not found. Used colors: {used_colors}"
    
    def test_glow_effect_implementation(self, sample_supertrend_data, mock_bokeh_figure):
        """Test that glow effects are implemented with wide transparent lines."""
        _plot_supertrend_indicator(mock_bokeh_figure, None, sample_supertrend_data)
        
        # Look for glow effect lines (wide, transparent)
        glow_lines = [line for line in mock_bokeh_figure.lines 
                     if line.get('line_width', 0) > 8 and line.get('line_alpha', 1) < 0.3]
        
        assert len(glow_lines) > 0, "Glow effect lines not found"
        
        # Verify glow lines have appropriate properties
        for glow_line in glow_lines:
            assert glow_line['line_width'] >= 10, f"Glow line width too small: {glow_line['line_width']}"
            assert glow_line['line_alpha'] <= 0.2, f"Glow line alpha too high: {glow_line['line_alpha']}"
    
    def test_buy_sell_signals(self, sample_supertrend_data, mock_bokeh_figure):
        """Test that BUY/SELL signals are properly rendered."""
        _plot_supertrend_indicator(mock_bokeh_figure, None, sample_supertrend_data)
        
        # Check for BUY signals (green triangles)
        buy_signals = [scatter for scatter in mock_bokeh_figure.scatters 
                      if scatter.get('legend_label') == 'BUY Signal']
        
        # Check for SELL signals (red inverted triangles)
        sell_signals = [scatter for scatter in mock_bokeh_figure.scatters 
                       if scatter.get('legend_label') == 'SELL Signal']
        
        # At least one type of signal should be present
        assert len(buy_signals) > 0 or len(sell_signals) > 0, "No trading signals found"
        
        # Verify signal properties
        for signal in buy_signals + sell_signals:
            assert signal.get('size') >= 10, f"Signal size too small: {signal.get('size')}"
            assert signal.get('alpha') >= 0.8, f"Signal alpha too low: {signal.get('alpha')}"
    
    def test_trend_zones_creation(self, sample_supertrend_data, mock_bokeh_figure):
        """Test that transparent trend zones are created."""
        _plot_supertrend_indicator(mock_bokeh_figure, None, sample_supertrend_data)
        
        # Check for BoxAnnotation layouts (trend zones)
        assert len(mock_bokeh_figure.layouts) > 0, "No trend zone layouts created"
        
        # Verify trend zones have appropriate properties
        for layout in mock_bokeh_figure.layouts:
            assert hasattr(layout, 'fill_alpha'), "Trend zone missing fill_alpha"
            assert layout.fill_alpha <= 0.1, f"Trend zone alpha too high: {layout.fill_alpha}"
    
    def test_hover_tool_functionality(self, sample_supertrend_data):
        """Test that hover tool is properly configured for SuperTrend."""
        hover_tool = _get_indicator_hover_tool('supertrend', sample_supertrend_data)
        
        # Verify hover tool exists
        assert hover_tool is not None, "Hover tool not created"
        
        # Verify tooltips contain expected fields
        tooltips = hover_tool.tooltips
        tooltip_text = [str(tooltip) for tooltip in tooltips]
        
        # Should contain date and SuperTrend-related fields
        assert any('Date' in str(tooltip) for tooltip in tooltips), "Date tooltip missing"
        assert any('PPrice1' in str(tooltip) or 'SuperTrend' in str(tooltip) 
                  for tooltip in tooltips), "SuperTrend value tooltip missing"
    
    def test_data_fallback_support(self):
        """Test that the function supports both old and new column formats."""
        # Create data with old format (PPrice1, PPrice2, Direction)
        old_format_data = pd.DataFrame({
            'PPrice1': [1.5, 1.51, 1.49],
            'PPrice2': [1.52, 1.53, 1.48],
            'Direction': [1, 0, 2],
            'index': pd.date_range('2023-01-01', periods=3)
        })
        
        # Create data with new format (supertrend, Direction)
        new_format_data = pd.DataFrame({
            'supertrend': [1.5, 1.51, 1.49],
            'Direction': [1, 0, 2],
            'index': pd.date_range('2023-01-01', periods=3)
        })
        
        # Create mock figures directly
        class MockFigure:
            def __init__(self):
                self.lines = []
                self.scatters = []
                self.layouts = []
            
            def line(self, x, y, **kwargs):
                self.lines.append({
                    'x': x, 'y': y,
                    'line_color': kwargs.get('line_color'),
                    'line_width': kwargs.get('line_width'),
                    'line_alpha': kwargs.get('line_alpha'),
                    'legend_label': kwargs.get('legend_label')
                })
            
            def scatter(self, x, y, **kwargs):
                self.scatters.append({
                    'x': x, 'y': y,
                    'size': kwargs.get('size'),
                    'color': kwargs.get('color'),
                    'marker': kwargs.get('marker'),
                    'alpha': kwargs.get('alpha'),
                    'legend_label': kwargs.get('legend_label')
                })
            
            def add_layout(self, layout):
                self.layouts.append(layout)
        
        mock_fig_old = MockFigure()
        mock_fig_new = MockFigure()
        
        # Test old format
        _plot_supertrend_indicator(mock_fig_old, None, old_format_data)
        assert len(mock_fig_old.lines) > 0, "Old format not supported"
        
        # Test new format
        _plot_supertrend_indicator(mock_fig_new, None, new_format_data)
        assert len(mock_fig_new.lines) > 0, "New format not supported"
    
    def test_error_handling_missing_columns(self, mock_bokeh_figure):
        """Test that function handles missing columns gracefully."""
        # Create data without required columns
        incomplete_data = pd.DataFrame({
            'Open': [1.5, 1.51, 1.49],
            'Close': [1.51, 1.52, 1.48],
            'index': pd.date_range('2023-01-01', periods=3)
        })
        
        # Should not raise an error
        try:
            _plot_supertrend_indicator(mock_bokeh_figure, None, incomplete_data)
            # Should not draw any lines
            assert len(mock_bokeh_figure.lines) == 0, "Lines drawn despite missing columns"
        except Exception as e:
            pytest.fail(f"Function raised unexpected error: {e}")
    
    def test_segment_creation_logic(self, sample_supertrend_data, mock_bokeh_figure):
        """Test that segments are created correctly based on direction changes."""
        # Create data with clear direction changes
        test_data = pd.DataFrame({
            'PPrice1': [1.5, 1.51, 1.52, 1.53],
            'PPrice2': [1.49, 1.48, 1.47, 1.46],
            'Direction': [1, 1, 2, 2],  # Clear change from 1 to 2
            'index': pd.date_range('2023-01-01', periods=4)
        })
        
        _plot_supertrend_indicator(mock_bokeh_figure, None, test_data)
        
        # Should create multiple segments due to direction change
        assert len(mock_bokeh_figure.lines) >= 2, "Segments not created for direction changes"
    
    def test_legend_label_consistency(self, sample_supertrend_data, mock_bokeh_figure):
        """Test that legend labels are consistent and meaningful."""
        _plot_supertrend_indicator(mock_bokeh_figure, None, sample_supertrend_data)
        
        # Collect all legend labels
        legend_labels = set()
        for line in mock_bokeh_figure.lines:
            if line.get('legend_label'):
                legend_labels.add(line['legend_label'])
        
        for scatter in mock_bokeh_figure.scatters:
            if scatter.get('legend_label'):
                legend_labels.add(scatter['legend_label'])
        
        # Should have expected legend labels
        expected_labels = {'SuperTrend', 'BUY Signal', 'SELL Signal'}
        found_labels = legend_labels.intersection(expected_labels)
        
        assert len(found_labels) >= 1, f"Expected legend labels not found. Found: {legend_labels}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 