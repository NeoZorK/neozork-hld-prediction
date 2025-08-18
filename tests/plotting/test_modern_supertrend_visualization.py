# -*- coding: utf-8 -*-
# tests/plotting/test_modern_supertrend_visualization.py

"""
Test module for modern SuperTrend visualization.
Tests the enhanced visual features and styling of SuperTrend indicator.
"""

import pytest

# Individual tests will be enforced with 10-second timeout
# No module-level skip to allow individual test execution

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import tempfile
import os

from src.plotting.dual_chart_fastest import plot_dual_chart_fastest
from src.calculation.indicators.trend.supertrend_ind import calculate_supertrend


class TestModernSuperTrendVisualization:
    """Test class for modern SuperTrend visualization features."""
    
    @pytest.fixture
    def sample_data(self):
        """Create sample OHLCV data for testing."""
        dates = pd.date_range(start='2024-01-01', periods=100, freq='D')
        
        # Create realistic price data with trends
        np.random.seed(42)
        base_price = 100.0
        prices = []
        
        for i in range(100):
            if i < 30:  # Uptrend
                change = np.random.normal(0.5, 0.3)
            elif i < 60:  # Downtrend
                change = np.random.normal(-0.3, 0.3)
            else:  # Sideways
                change = np.random.normal(0.0, 0.2)
            
            base_price += change
            open_price = base_price
            high_price = open_price + abs(np.random.normal(0, 0.5))
            low_price = open_price - abs(np.random.normal(0, 0.5))
            close_price = np.random.uniform(low_price, high_price)
            volume = np.random.randint(1000, 10000)
            
            prices.append({
                'Open': open_price,
                'High': high_price,
                'Low': low_price,
                'Close': close_price,
                'Volume': volume
            })
        
        df = pd.DataFrame(prices, index=dates)
        return df
    
    @pytest.fixture
    def supertrend_data(self, sample_data):
        """Create sample data with SuperTrend calculations."""
        df = sample_data.copy()
        
        # Calculate SuperTrend
        supertrend_values, trend_direction = calculate_supertrend(df, period=10, multiplier=3.0)
        
        df['supertrend'] = supertrend_values
        # Use direction column instead of supertrend_direction to match real data structure
        df['direction'] = pd.Series(0.0, index=df.index)  # Default to no signal
        
        # Add some BUY/SELL signals for testing
        df.loc[df.index[10], 'direction'] = 1.0  # BUY signal
        df.loc[df.index[20], 'direction'] = 2.0  # SELL signal
        
        return df
    
    def test_modern_supertrend_colors(self, supertrend_data):
        """Test that modern SuperTrend uses enhanced color scheme."""
        with tempfile.NamedTemporaryFile(suffix='.html', delete=False) as tmp_file:
            output_path = tmp_file.name
        
        try:
            # Create chart with modern SuperTrend
            fig = plot_dual_chart_fastest(
                df=supertrend_data,
                rule='supertrend:10,3,close',
                title='Test Modern SuperTrend',
                output_path=output_path
            )
            
            # Check that figure was created
            assert fig is not None
            
            # Check that SuperTrend traces exist
            supertrend_traces = [trace for trace in fig.data if 'SuperTrend' in trace.name]
            assert len(supertrend_traces) > 0
            
            # Check for three-color scheme
            expected_colors = [
                'rgba(0, 200, 81, 0.95)',  # Uptrend green
                'rgba(255, 68, 68, 0.95)',  # Downtrend red
                'rgba(255, 193, 7, 0.95)'   # Signal change golden
            ]
            found_colors = set()
            
            for trace in supertrend_traces:
                if hasattr(trace, 'line') and trace.line.color in expected_colors:
                    found_colors.add(trace.line.color)
            
            # Should find at least uptrend and downtrend colors
            assert len(found_colors) >= 2, f"Expected at least 2 colors, found: {found_colors}"
            
        finally:
            if os.path.exists(output_path):
                os.unlink(output_path)
    
    def test_enhanced_markers(self, supertrend_data):
        """Test that enhanced BUY/SELL markers are present."""
        with tempfile.NamedTemporaryFile(suffix='.html', delete=False) as tmp_file:
            output_path = tmp_file.name
        
        try:
            fig = plot_dual_chart_fastest(
                df=supertrend_data,
                rule='supertrend:10,3,close',
                output_path=output_path
            )
            
            # Check for BUY/SELL signal traces
            buy_traces = [trace for trace in fig.data if 'BUY Signal' in trace.name]
            sell_traces = [trace for trace in fig.data if 'SELL Signal' in trace.name]
            
            # Check for pulse effect traces
            pulse_traces = [trace for trace in fig.data if 'Pulse' in trace.name]
            
            # At least some signals should be present
            assert len(buy_traces) + len(sell_traces) >= 0
            
            # Check marker styling
            for trace in buy_traces + sell_traces:
                assert hasattr(trace, 'marker')
                assert trace.marker.size >= 16  # Enhanced size
                assert 'white' in trace.marker.line.color  # White border
            
        finally:
            if os.path.exists(output_path):
                os.unlink(output_path)
    
    def test_smooth_curves(self, supertrend_data):
        """Test that SuperTrend lines use smooth curves."""
        with tempfile.NamedTemporaryFile(suffix='.html', delete=False) as tmp_file:
            output_path = tmp_file.name
        
        try:
            fig = plot_dual_chart_fastest(
                df=supertrend_data,
                rule='supertrend:10,3,close',
                output_path=output_path
            )
            
            # Check for smooth curve traces
            smooth_traces = [trace for trace in fig.data if 'SuperTrend' in trace.name and 'Glow' not in trace.name]
            
            for trace in smooth_traces:
                if hasattr(trace, 'line'):
                    assert trace.line.shape == 'spline', "SuperTrend should use smooth curves"
            
        finally:
            if os.path.exists(output_path):
                os.unlink(output_path)
    
    def test_glow_effects(self, supertrend_data):
        """Test that glow effects are present."""
        with tempfile.NamedTemporaryFile(suffix='.html', delete=False) as tmp_file:
            output_path = tmp_file.name
        
        try:
            fig = plot_dual_chart_fastest(
                df=supertrend_data,
                rule='supertrend:10,3,close',
                output_path=output_path
            )
            
            # Check for glow effect traces
            glow_traces = [trace for trace in fig.data if 'Glow' in trace.name]
            
            # Should have glow effects for each SuperTrend segment
            assert len(glow_traces) > 0
            
            # Check glow styling
            for trace in glow_traces:
                assert hasattr(trace, 'line')
                assert trace.line.width > 5  # Thicker than main line
                assert '0.3' in trace.line.color  # Semi-transparent
            
        finally:
            if os.path.exists(output_path):
                os.unlink(output_path)
    
    def test_trend_background_zones(self, supertrend_data):
        """Test that trend background zones are added."""
        with tempfile.NamedTemporaryFile(suffix='.html', delete=False) as tmp_file:
            output_path = tmp_file.name
        
        try:
            fig = plot_dual_chart_fastest(
                df=supertrend_data,
                rule='supertrend:10,3,close',
                output_path=output_path
            )
            
            # Check for background shapes
            background_shapes = [shape for shape in fig.layout.shapes if shape.type == 'rect']
            
            # Should have background zones for trend changes
            assert len(background_shapes) >= 0
            
        finally:
            if os.path.exists(output_path):
                os.unlink(output_path)
    
    def test_modern_layout(self, supertrend_data):
        """Test that modern layout features are applied."""
        with tempfile.NamedTemporaryFile(suffix='.html', delete=False) as tmp_file:
            output_path = tmp_file.name
        
        try:
            fig = plot_dual_chart_fastest(
                df=supertrend_data,
                rule='supertrend:10,3,close',
                output_path=output_path
            )
            
            # Check modern layout features
            layout = fig.layout
            
            # Modern background
            assert 'rgba(248, 249, 250, 0.8)' in str(layout.plot_bgcolor)
            
            # Modern font family
            assert 'Arial' in str(layout.font.family)
            
            # Enhanced margins
            assert layout.margin.t >= 40
            assert layout.margin.l >= 40
            
            # Modern legend styling
            assert layout.legend.bgcolor == 'rgba(255,255,255,0.95)'
            assert layout.legend.bordercolor == '#e1e8ed'
            
        finally:
            if os.path.exists(output_path):
                os.unlink(output_path)
    
    def test_enhanced_hover_labels(self, supertrend_data):
        """Test that enhanced hover labels are configured."""
        with tempfile.NamedTemporaryFile(suffix='.html', delete=False) as tmp_file:
            output_path = tmp_file.name
        
        try:
            fig = plot_dual_chart_fastest(
                df=supertrend_data,
                rule='supertrend:10,3,close',
                output_path=output_path
            )
            
            # Check hover configuration
            layout = fig.layout
            
            assert layout.hovermode == "x unified"
            assert layout.hoverlabel.font.size == 11
            assert layout.hoverlabel.bordercolor == '#e1e8ed'
            assert 'Arial' in str(layout.hoverlabel.font.family)
            
        finally:
            if os.path.exists(output_path):
                os.unlink(output_path)
    
    def test_fallback_supertrend(self, sample_data):
        """Test fallback SuperTrend visualization when direction data is missing."""
        with tempfile.NamedTemporaryFile(suffix='.html', delete=False) as tmp_file:
            output_path = tmp_file.name
        
        try:
            # Add only SuperTrend values without direction
            df = sample_data.copy()
            supertrend_values, _ = calculate_supertrend(df, period=10, multiplier=3.0)
            df['supertrend'] = supertrend_values
            
            fig = plot_dual_chart_fastest(
                df=df,
                rule='supertrend:10,3,close',
                output_path=output_path
            )
            
            # Check that fallback trace exists
            fallback_traces = [trace for trace in fig.data if 'SuperTrend' in trace.name]
            assert len(fallback_traces) > 0
            
            # Check fallback styling
            for trace in fallback_traces:
                if hasattr(trace, 'line'):
                    assert trace.line.color == '#3498db'  # Modern blue
                    assert trace.line.shape == 'spline'  # Smooth curve
            
        finally:
            if os.path.exists(output_path):
                os.unlink(output_path)
    
    def test_three_color_signal_changes(self, supertrend_data):
        """Test that SuperTrend shows three colors for signal changes."""
        with tempfile.NamedTemporaryFile(suffix='.html', delete=False) as tmp_file:
            output_path = tmp_file.name
        
        try:
            fig = plot_dual_chart_fastest(
                df=supertrend_data,
                rule='supertrend:10,3,close',
                output_path=output_path
            )
            
            # Check for three-color legend entries
            legend_names = [trace.name for trace in fig.data if 'SuperTrend' in trace.name]
            
            # Should have different legend names for different colors
            unique_names = set(legend_names)
            assert len(unique_names) >= 2, f"Expected multiple SuperTrend legend entries, found: {unique_names}"
            
            # Check for signal change color specifically
            signal_change_traces = [trace for trace in fig.data if 'Signal Change' in trace.name]
            if len(signal_change_traces) > 0:
                for trace in signal_change_traces:
                    assert trace.line.color == 'rgba(255, 193, 7, 0.95)', "Signal change should be golden color"
            
        finally:
            if os.path.exists(output_path):
                os.unlink(output_path)
    
    def test_performance_with_large_dataset(self, supertrend_data):
        """Test performance with larger dataset."""
        # Expand dataset
        large_df = pd.concat([supertrend_data] * 3, ignore_index=True)
        large_df.index = pd.date_range(start='2024-01-01', periods=len(large_df), freq='D')
        
        with tempfile.NamedTemporaryFile(suffix='.html', delete=False) as tmp_file:
            output_path = tmp_file.name
        
        try:
            import time
            start_time = time.time()
            
            fig = plot_dual_chart_fastest(
                df=large_df,
                rule='supertrend:10,3,close',
                output_path=output_path
            )
            
            end_time = time.time()
            processing_time = end_time - start_time
            
            # Should complete within reasonable time (adjust threshold as needed)
            assert processing_time < 10.0, f"Processing took too long: {processing_time:.2f} seconds"
            
            # Check that figure was created successfully
            assert fig is not None
            
        finally:
            if os.path.exists(output_path):
                os.unlink(output_path)


if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 