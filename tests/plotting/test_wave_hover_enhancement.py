# -*- coding: utf-8 -*-
# tests/plotting/test_wave_hover_enhancement.py

"""
Test Wave indicator hover enhancement for fastest mode.
Tests that Wave Values show correct color information on hover.
"""

import pytest
import pandas as pd
import numpy as np
from unittest.mock import Mock, patch
import plotly.graph_objects as go

from src.plotting.dual_chart_fastest import add_wave_indicator, create_discontinuous_line_traces


class TestWaveHoverEnhancement:
    """Test Wave indicator hover enhancement functionality."""
    
    def setup_method(self):
        """Set up test data."""
        # Create sample data with Wave indicator values
        dates = pd.date_range('2024-01-01', periods=100, freq='h')
        
        # Create Wave values with different colors
        wave_values = np.random.uniform(-2, 2, 100)
        color_values = np.random.choice([0, 1, 2], 100)  # 0=NOTRADE, 1=BUY, 2=SELL
        fastline_values = np.random.uniform(-1, 1, 100)
        ma_values = np.random.uniform(-0.5, 0.5, 100)
        
        self.test_df = pd.DataFrame({
            '_Plot_Wave': wave_values,
            '_Plot_Color': color_values,
            '_Plot_FastLine': fastline_values,
            'MA_Line': ma_values
        }, index=dates)
    
    def test_create_discontinuous_line_traces_hover_template(self):
        """Test that create_discontinuous_line_traces includes color information in hover template."""
        # Create test data
        x_data = self.test_df.index
        y_data = self.test_df['_Plot_Wave']
        mask = self.test_df['_Plot_Color'] == 1  # BUY signals
        
        # Call the function
        traces = create_discontinuous_line_traces(
            x_data, y_data, mask, 'Wave', 'red', width=2, showlegend=True
        )
        
        # Check that traces were created
        assert len(traces) > 0
        
        # Check that first trace has correct hover template
        first_trace = traces[0]
        assert isinstance(first_trace, go.Scatter)
        assert 'Color: Red (BUY)' in first_trace.hovertemplate
        assert 'Value: %{y:.6f}' in first_trace.hovertemplate
    
    def test_wave_indicator_hover_templates(self):
        """Test that Wave indicator creates traces with enhanced hover templates."""
        # Create mock figure
        mock_fig = Mock()
        
        # Call add_wave_indicator
        add_wave_indicator(mock_fig, self.test_df)
        
        # Check that add_trace was called for Wave segments
        add_trace_calls = [call for call in mock_fig.add_trace.call_args_list 
                          if call[0][0].name == 'Wave']
        
        # Should have calls for red and blue segments
        assert len(add_trace_calls) > 0
        
        # Check that at least one trace has enhanced hover template
        has_enhanced_hover = False
        for call in add_trace_calls:
            trace = call[0][0]
            if hasattr(trace, 'hovertemplate') and trace.hovertemplate:
                if 'Color:' in trace.hovertemplate:
                    has_enhanced_hover = True
                    break
        
        assert has_enhanced_hover, "No enhanced hover template found"
    
    def test_fast_line_hover_template(self):
        """Test that Fast Line has enhanced hover template."""
        # Create mock figure
        mock_fig = Mock()
        
        # Call add_wave_indicator
        add_wave_indicator(mock_fig, self.test_df)
        
        # Check that add_trace was called for Fast Line
        add_trace_calls = [call for call in mock_fig.add_trace.call_args_list 
                          if call[0][0].name == 'Fast Line']
        
        if add_trace_calls:  # If Fast Line traces were created
            fast_line_trace = add_trace_calls[0][0][0]
            assert 'Color: Red (Signal)' in fast_line_trace.hovertemplate
    
    def test_ma_line_hover_template(self):
        """Test that MA Line has enhanced hover template."""
        # Create mock figure
        mock_fig = Mock()
        
        # Call add_wave_indicator
        add_wave_indicator(mock_fig, self.test_df)
        
        # Check that add_trace was called for MA Line
        add_trace_calls = [call for call in mock_fig.add_trace.call_args_list 
                          if call[0][0].name == 'MA Line']
        
        if add_trace_calls:  # If MA Line traces were created
            ma_line_trace = add_trace_calls[0][0][0]
            assert 'Color: Light Blue (MA)' in ma_line_trace.hovertemplate
    
    def test_third_wave_hover_trace(self):
        """Test that third hover trace named 'wave' is created for red/blue segments only."""
        # Create mock figure
        mock_fig = Mock()
        
        # Call add_wave_indicator
        add_wave_indicator(mock_fig, self.test_df)
        
        # Check that add_trace was called for the third wave hover trace
        add_trace_calls = [call for call in mock_fig.add_trace.call_args_list 
                          if call[0][0].name == 'wave']
        
        # Should have exactly one wave hover trace
        assert len(add_trace_calls) == 1
        
        # Check the wave hover trace properties
        wave_trace = add_trace_calls[0][0][0]
        assert wave_trace.mode == 'markers'
        assert wave_trace.showlegend == False
        assert wave_trace.hoverinfo == 'y+name'
        assert '<b>wave</b><br>Value: %{y:.6f}<extra></extra>' in wave_trace.hovertemplate
        
        # Check that markers are invisible
        assert wave_trace.marker.size == 0
        assert wave_trace.marker.color == 'rgba(0,0,0,0)'
    
    def test_third_wave_hover_only_red_blue_data(self):
        """Test that third wave hover trace only includes red/blue segment data."""
        # Create test data with specific color values
        dates = pd.date_range('2024-01-01', periods=10, freq='h')
        test_df = pd.DataFrame({
            '_Plot_Wave': [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0],
            '_Plot_Color': [1, 2, 0, 1, 2, 0, 1, 2, 0, 1],  # Red, Blue, Black, Red, Blue, Black, Red, Blue, Black, Red
            '_Plot_FastLine': [0.5] * 10,
            'MA_Line': [0.3] * 10
        }, index=dates)
        
        # Create mock figure
        mock_fig = Mock()
        
        # Call add_wave_indicator
        add_wave_indicator(mock_fig, test_df)
        
        # Check that add_trace was called for the wave hover trace
        add_trace_calls = [call for call in mock_fig.add_trace.call_args_list 
                          if call[0][0].name == 'wave']
        
        assert len(add_trace_calls) == 1
        
        # Check that only red/blue data points are included (indices 0,1,3,4,6,7,9)
        wave_trace = add_trace_calls[0][0][0]
        expected_indices = [0, 1, 3, 4, 6, 7, 9]  # Red and Blue indices
        actual_indices = [i for i, x in enumerate(wave_trace.x) if x in test_df.index[expected_indices]]
        
        # Should have 7 data points (only red and blue)
        assert len(wave_trace.x) == 7
        assert len(wave_trace.y) == 7
    
    def test_color_mapping_correctness(self):
        """Test that color mapping is correct for different signal types."""
        # Test red color mapping
        traces_red = create_discontinuous_line_traces(
            self.test_df.index, 
            self.test_df['_Plot_Wave'], 
            self.test_df['_Plot_Color'] == 1, 
            'Wave', 'red', width=2, showlegend=True
        )
        
        if traces_red:
            assert 'Color: Red (BUY)' in traces_red[0].hovertemplate
        
        # Test blue color mapping
        traces_blue = create_discontinuous_line_traces(
            self.test_df.index, 
            self.test_df['_Plot_Wave'], 
            self.test_df['_Plot_Color'] == 2, 
            'Wave', 'blue', width=2, showlegend=True
        )
        
        if traces_blue:
            assert 'Color: Blue (SELL)' in traces_blue[0].hovertemplate
        
        # Test black color mapping (should not be visible but template should exist)
        traces_black = create_discontinuous_line_traces(
            self.test_df.index, 
            self.test_df['_Plot_Wave'], 
            self.test_df['_Plot_Color'] == 0, 
            'Wave', 'black', width=2, showlegend=True
        )
        
        if traces_black:
            assert 'Color: Black (NOTRADE)' in traces_black[0].hovertemplate


def test_wave_hover_enhancement_integration():
    """Integration test for Wave hover enhancement."""
    print("🎯 Testing Wave hover enhancement...")
    
    # Create test instance
    test_instance = TestWaveHoverEnhancement()
    test_instance.setup_method()
    
    # Run tests
    test_instance.test_create_discontinuous_line_traces_hover_template()
    print("✅ create_discontinuous_line_traces hover template test passed")
    
    test_instance.test_wave_indicator_hover_templates()
    print("✅ Wave indicator hover templates test passed")
    
    test_instance.test_fast_line_hover_template()
    print("✅ Fast Line hover template test passed")
    
    test_instance.test_ma_line_hover_template()
    print("✅ MA Line hover template test passed")
    
    test_instance.test_third_wave_hover_trace()
    print("✅ Third wave hover trace test passed")
    
    test_instance.test_third_wave_hover_only_red_blue_data()
    print("✅ Third wave hover only red/blue data test passed")
    
    test_instance.test_color_mapping_correctness()
    print("✅ Color mapping correctness test passed")
    
    print("🎉 All Wave hover enhancement tests passed!")


if __name__ == "__main__":
    test_wave_hover_enhancement_integration()
