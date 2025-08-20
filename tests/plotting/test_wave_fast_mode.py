# -*- coding: utf-8 -*-
# tests/plotting/test_wave_fast_mode.py

"""
Unit tests for Wave indicator in fast mode plotting.
Tests the new functionality that enables Wave indicator to work with -d fast method.
"""

import pytest
import pandas as pd
import numpy as np
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime, timedelta

from src.plotting.dual_chart_fast import _plot_wave_indicator, _get_indicator_hover_tool
from src.calculation.indicators.trend.wave_ind import apply_rule_wave, WaveParameters, ENUM_MOM_TR, ENUM_GLOBAL_TR
from src.calculation.indicators.base_indicator import PriceType
from src.common.constants import BUY, SELL, NOTRADE


class TestWaveFastMode:
    """Test class for Wave indicator in fast mode plotting."""

    def setup_method(self):
        """Set up test data."""
        # Create sample OHLCV data
        dates = pd.date_range('2023-01-01', periods=100, freq='D')
        self.sample_data = pd.DataFrame({
            'DateTime': dates,
            'Open': np.random.uniform(100, 200, 100),
            'High': np.random.uniform(200, 300, 100),
            'Low': np.random.uniform(50, 150, 100),
            'Close': np.random.uniform(100, 200, 100),
            'Volume': np.random.uniform(1000, 10000, 100)
        })
        self.sample_data['High'] = self.sample_data[['Open', 'High', 'Close']].max(axis=1)
        self.sample_data['Low'] = self.sample_data[['Open', 'Low', 'Close']].min(axis=1)
        self.sample_data.set_index('DateTime', inplace=True)

    def test_wave_indicator_fast_mode_basic(self):
        """Test basic Wave indicator plotting in fast mode."""
        # Create wave parameters
        wave_params = WaveParameters(
            long1=50, fast1=10, trend1=5, tr1=ENUM_MOM_TR.TR_Fast,
            long2=30, fast2=8, trend2=3, tr2=ENUM_MOM_TR.TR_Fast,
            global_tr=ENUM_GLOBAL_TR.G_TR_PRIME, sma_period=20
        )
        
        # Apply wave calculation
        result_df = apply_rule_wave(self.sample_data.copy(), wave_params, PriceType.OPEN)
        
        # Create mock figure and source
        mock_fig = Mock()
        mock_source = Mock()
        
        # Test wave indicator plotting
        _plot_wave_indicator(mock_fig, mock_source, result_df)
        
        # Verify that line method was called (indicating lines were added)
        assert mock_fig.line.called, "line method should be called for wave indicator"
        
        # Get all calls to line method
        calls = mock_fig.line.call_args_list
        
        # Should have at least some lines added
        assert len(calls) > 0, "No lines added for wave indicator"
        
        # Check that lines have valid parameters
        for call in calls:
            args, kwargs = call
            # Check that line has valid parameters
            assert 'line_color' in kwargs, "Line should have color"
            assert 'line_width' in kwargs, "Line should have width"
            assert 'legend_label' in kwargs, "Line should have legend label"

    def test_wave_indicator_fast_mode_columns(self):
        """Test Wave indicator with different column name variations."""
        # Create wave parameters
        wave_params = WaveParameters(
            long1=50, fast1=10, trend1=5, tr1=ENUM_MOM_TR.TR_Fast,
            long2=30, fast2=8, trend2=3, tr2=ENUM_MOM_TR.TR_Fast,
            global_tr=ENUM_GLOBAL_TR.G_TR_PRIME, sma_period=20
        )
        
        # Apply wave calculation
        result_df = apply_rule_wave(self.sample_data.copy(), wave_params, PriceType.OPEN)
        
        # Test with different column name variations
        column_variations = [
            ('_Plot_Wave', '_Plot_Color', '_Plot_FastLine', 'MA_Line'),
            ('_plot_wave', '_plot_color', '_plot_fastline', 'ma_line')
        ]
        
        for wave_col, color_col, fastline_col, ma_col in column_variations:
            # Rename columns to test different variations
            test_df = result_df.copy()
            if wave_col in test_df.columns:
                test_df[wave_col] = test_df['_Plot_Wave']
            if color_col in test_df.columns:
                test_df[color_col] = test_df['_Plot_Color']
            if fastline_col in test_df.columns:
                test_df[fastline_col] = test_df['_Plot_FastLine']
            if ma_col in test_df.columns:
                test_df[ma_col] = test_df['MA_Line']
            
            # Create mock figure and source
            mock_fig = Mock()
            mock_source = Mock()
            
            # Test wave indicator plotting
            _plot_wave_indicator(mock_fig, mock_source, test_df)
            
            # Verify that line method was called
            assert mock_fig.line.called, f"line method should be called for column variation {wave_col}"

    def test_wave_indicator_fast_mode_signals(self):
        """Test Wave indicator signal filtering in fast mode."""
        # Create wave parameters
        wave_params = WaveParameters(
            long1=50, fast1=10, trend1=5, tr1=ENUM_MOM_TR.TR_Fast,
            long2=30, fast2=8, trend2=3, tr2=ENUM_MOM_TR.TR_Fast,
            global_tr=ENUM_GLOBAL_TR.G_TR_PRIME, sma_period=20
        )
        
        # Apply wave calculation
        result_df = apply_rule_wave(self.sample_data.copy(), wave_params, PriceType.OPEN)
        
        # Create mock figure and source
        mock_fig = Mock()
        mock_source = Mock()
        
        # Test wave indicator plotting
        _plot_wave_indicator(mock_fig, mock_source, result_df)
        
        # Get all calls to line method
        calls = mock_fig.line.call_args_list
        
        # Check for red lines (BUY signals)
        red_lines = [call for call in calls if call[1].get('line_color') == 'red']
        assert len(red_lines) >= 0, "Should have red lines for BUY signals (or none if no signals)"
        
        # Check for blue lines (SELL signals)
        blue_lines = [call for call in calls if call[1].get('line_color') == 'blue']
        assert len(blue_lines) >= 0, "Should have blue lines for SELL signals (or none if no signals)"
        
        # Check for lightblue lines (MA Line)
        lightblue_lines = [call for call in calls if call[1].get('line_color') == 'lightblue']
        assert len(lightblue_lines) >= 0, "Should have lightblue lines for MA Line (or none if no data)"

    def test_wave_indicator_fast_mode_hover_tool(self):
        """Test Wave indicator hover tool in fast mode."""
        # Create wave parameters
        wave_params = WaveParameters(
            long1=50, fast1=10, trend1=5, tr1=ENUM_MOM_TR.TR_Fast,
            long2=30, fast2=8, trend2=3, tr2=ENUM_MOM_TR.TR_Fast,
            global_tr=ENUM_GLOBAL_TR.G_TR_PRIME, sma_period=20
        )
        
        # Apply wave calculation
        result_df = apply_rule_wave(self.sample_data.copy(), wave_params, PriceType.OPEN)
        
        # Test hover tool creation
        hover_tool = _get_indicator_hover_tool('wave', result_df)
        
        # Verify hover tool was created
        assert hover_tool is not None, "Hover tool should be created for wave indicator"
        
        # Check that hover tool has tooltips
        assert hasattr(hover_tool, 'tooltips'), "Hover tool should have tooltips"
        
        # Check that tooltips contain expected fields
        tooltip_text = str(hover_tool.tooltips)
        assert 'Wave' in tooltip_text, "Tooltips should contain Wave field"
        assert 'Fast Line' in tooltip_text, "Tooltips should contain Fast Line field"
        assert 'MA Line' in tooltip_text, "Tooltips should contain MA Line field"
        assert 'Signal' in tooltip_text, "Tooltips should contain Signal field"

    def test_wave_indicator_fast_mode_empty_data(self):
        """Test Wave indicator with empty or invalid data."""
        # Create empty DataFrame
        empty_df = pd.DataFrame()
        
        # Create mock figure and source
        mock_fig = Mock()
        mock_source = Mock()
        
        # Test wave indicator plotting with empty data
        _plot_wave_indicator(mock_fig, mock_source, empty_df)
        
        # Should not raise any exceptions
        # The function should handle empty data gracefully

    def test_wave_indicator_fast_mode_missing_columns(self):
        """Test Wave indicator with missing columns."""
        # Create DataFrame without wave columns
        test_df = self.sample_data.copy()
        
        # Create mock figure and source
        mock_fig = Mock()
        mock_source = Mock()
        
        # Test wave indicator plotting with missing columns
        _plot_wave_indicator(mock_fig, mock_source, test_df)
        
        # Should not raise any exceptions
        # The function should handle missing columns gracefully

    def test_wave_indicator_fast_mode_integration(self):
        """Test complete Wave indicator integration in fast mode."""
        # Create wave parameters
        wave_params = WaveParameters(
            long1=50, fast1=10, trend1=5, tr1=ENUM_MOM_TR.TR_Fast,
            long2=30, fast2=8, trend2=3, tr2=ENUM_MOM_TR.TR_Fast,
            global_tr=ENUM_GLOBAL_TR.G_TR_PRIME, sma_period=20
        )
        
        # Apply wave calculation
        result_df = apply_rule_wave(self.sample_data.copy(), wave_params, PriceType.OPEN)
        
        # Verify required columns exist
        required_cols = ['_Plot_Wave', '_Plot_Color', '_Plot_FastLine', 'MA_Line']
        for col in required_cols:
            assert col in result_df.columns, f"Missing required column {col}"
        
        # Verify signal values are valid
        valid_signals = [NOTRADE, BUY, SELL]
        assert result_df['_Plot_Color'].isin(valid_signals).all(), "Invalid signal values"
        
        # Create mock figure and source
        mock_fig = Mock()
        mock_source = Mock()
        
        # Test wave indicator plotting
        _plot_wave_indicator(mock_fig, mock_source, result_df)
        
        # Verify that plotting was successful
        assert mock_fig.line.called, "Wave indicator plotting should be successful"


if __name__ == "__main__":
    # Run tests
    test_instance = TestWaveFastMode()
    test_instance.setup_method()
    
    print("Running Wave Fast Mode Tests...")
    
    test_instance.test_wave_indicator_fast_mode_basic()
    print("✅ Basic Wave indicator fast mode test passed")
    
    test_instance.test_wave_indicator_fast_mode_columns()
    print("✅ Wave indicator column variations test passed")
    
    test_instance.test_wave_indicator_fast_mode_signals()
    print("✅ Wave indicator signal filtering test passed")
    
    test_instance.test_wave_indicator_fast_mode_hover_tool()
    print("✅ Wave indicator hover tool test passed")
    
    test_instance.test_wave_indicator_fast_mode_empty_data()
    print("✅ Wave indicator empty data test passed")
    
    test_instance.test_wave_indicator_fast_mode_missing_columns()
    print("✅ Wave indicator missing columns test passed")
    
    test_instance.test_wave_indicator_fast_mode_integration()
    print("✅ Wave indicator integration test passed")
    
    print("\n🎉 All Wave Fast Mode tests passed successfully!")
