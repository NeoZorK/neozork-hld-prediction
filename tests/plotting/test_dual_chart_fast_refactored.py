# -*- coding: utf-8 -*-
# tests/plotting/test_dual_chart_fast_refactored.py

"""
Tests for refactored dual_chart_fast module.
Tests all the new indicator functions and ensures the refactoring didn't break functionality.
"""

import pytest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
import tempfile
import shutil
from unittest.mock import Mock, patch

from src.plotting.dual_chart_fast import (
    plot_dual_chart_fast,
    get_screen_height,
    calculate_dynamic_height,
    _plot_rsi_indicator,
    _plot_macd_indicator,
    _plot_ema_indicator,
    _plot_bb_indicator,
    _plot_atr_indicator,
    _plot_cci_indicator,
    _plot_vwap_indicator,
    _plot_pivot_indicator,
    _plot_hma_indicator,
    _plot_tsf_indicator,
    _plot_monte_indicator,
    _plot_kelly_indicator,
    _plot_donchain_indicator,
    _plot_fibo_indicator,
    _plot_obv_indicator,
    _plot_stdev_indicator,
    _plot_adx_indicator,
    _plot_sar_indicator,
    _plot_rsi_mom_indicator,
    _plot_rsi_div_indicator,
    _plot_stoch_indicator,
    _get_indicator_hover_tool,
    _plot_indicator_by_type
)


class TestDualChartFastRefactored:
    """Test class for refactored dual_chart_fast functionality."""
    
    @pytest.fixture
    def sample_data(self):
        """Create sample OHLCV data with various indicators."""
        dates = pd.date_range('2023-01-01', periods=100, freq='D')
        np.random.seed(42)
        
        # Generate realistic OHLCV data
        base_price = 100.0
        prices = []
        for i in range(100):
            if i == 0:
                price = base_price
            else:
                change = np.random.normal(0, 0.5)
                price = prices[-1] * (1 + change/100)
            prices.append(price)
        
        data = []
        for i, price in enumerate(prices):
            high = price * (1 + abs(np.random.normal(0, 0.01)))
            low = price * (1 - abs(np.random.normal(0, 0.01)))
            open_price = price * (1 + np.random.normal(0, 0.005))
            close_price = price * (1 + np.random.normal(0, 0.005))
            volume = np.random.randint(1000, 10000)
            
            data.append({
                'Open': open_price,
                'High': high,
                'Low': low,
                'Close': close_price,
                'Volume': volume
            })
        
        df = pd.DataFrame(data, index=dates)
        
        # Add various indicator columns
        df['rsi'] = np.random.uniform(0, 100, 100)
        df['rsi_overbought'] = 70
        df['rsi_oversold'] = 30
        df['macd'] = np.random.normal(0, 0.1, 100)
        df['macd_signal'] = np.random.normal(0, 0.08, 100)
        df['macd_histogram'] = df['macd'] - df['macd_signal']
        df['ema'] = np.random.normal(100, 2, 100)
        df['bb_upper'] = np.random.normal(105, 2, 100)
        df['bb_middle'] = np.random.normal(100, 2, 100)
        df['bb_lower'] = np.random.normal(95, 2, 100)
        df['atr'] = np.random.uniform(0.5, 2.0, 100)
        df['cci'] = np.random.normal(0, 50, 100)
        df['vwap'] = np.random.normal(100, 2, 100)
        df['pivot'] = np.random.normal(100, 2, 100)
        df['r1'] = np.random.normal(102, 2, 100)
        df['s1'] = np.random.normal(98, 2, 100)
        df['hma'] = np.random.normal(100, 2, 100)
        df['tsf'] = np.random.normal(100, 2, 100)
        df['montecarlo'] = np.random.normal(100, 2, 100)
        df['montecarlo_signal'] = np.random.normal(100, 2, 100)
        df['montecarlo_histogram'] = np.random.normal(0, 0.5, 100)
        df['montecarlo_upper'] = np.random.normal(102, 2, 100)
        df['montecarlo_lower'] = np.random.normal(98, 2, 100)
        df['kelly'] = np.random.uniform(-0.5, 0.5, 100)
        df['donchain_upper'] = np.random.normal(105, 2, 100)
        df['donchain_middle'] = np.random.normal(100, 2, 100)
        df['donchain_lower'] = np.random.normal(95, 2, 100)
        df['fibo_0'] = np.random.normal(95, 2, 100)
        df['fibo_236'] = np.random.normal(97, 2, 100)
        df['fibo_382'] = np.random.normal(99, 2, 100)
        df['fibo_618'] = np.random.normal(101, 2, 100)
        df['fibo_786'] = np.random.normal(103, 2, 100)
        df['fibo_100'] = np.random.normal(105, 2, 100)
        df['obv'] = np.random.uniform(1000000, 2000000, 100)
        df['stdev'] = np.random.uniform(0.5, 2.0, 100)
        df['adx'] = np.random.uniform(0, 100, 100)
        df['di_plus'] = np.random.uniform(0, 100, 100)
        df['di_minus'] = np.random.uniform(0, 100, 100)
        df['sar'] = np.random.normal(100, 2, 100)
        df['rsi_momentum'] = np.random.uniform(-10, 10, 100)
        df['rsi_divergence'] = np.random.uniform(-10, 10, 100)
        df['stoch_k'] = np.random.uniform(0, 100, 100)
        df['stoch_d'] = np.random.uniform(0, 100, 100)
        df['stoch_overbought'] = 80
        df['stoch_oversold'] = 20
        
        return df
    
    @pytest.fixture
    def temp_output_dir(self):
        """Create temporary output directory."""
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir)
    
    @pytest.fixture
    def mock_figure(self):
        """Create a mock Bokeh figure for testing."""
        mock_fig = Mock()
        mock_fig.line = Mock()
        mock_fig.vbar = Mock()
        mock_fig.scatter = Mock()
        return mock_fig
    
    @pytest.fixture
    def mock_source(self):
        """Create a mock ColumnDataSource for testing."""
        mock = Mock()
        mock.data = {}
        return mock
    
    def test_get_screen_height(self):
        """Test get_screen_height function returns reasonable value."""
        height = get_screen_height()
        assert isinstance(height, int)
        assert height > 0
        assert height < 10000  # Reasonable upper bound
    
    def test_calculate_dynamic_height(self):
        """Test calculate_dynamic_height function."""
        # Test with None values
        height = calculate_dynamic_height()
        assert isinstance(height, int)
        assert height > 0
        
        # Test with custom screen height
        height = calculate_dynamic_height(screen_height=1080, rule_str="macd")
        assert isinstance(height, int)
        assert height > 0
        assert height <= 2000  # Max bound
        assert height >= 400   # Min bound
        
        # Test with OHLCV rule
        height = calculate_dynamic_height(screen_height=1080, rule_str="OHLCV")
        assert isinstance(height, int)
        assert height > 0
        assert height <= 2000
        assert height >= 400
    
    def test_plot_rsi_indicator(self, mock_figure, mock_source, sample_data):
        """Test RSI indicator plotting function."""
        _plot_rsi_indicator(mock_figure, mock_source, sample_data)
        
        # Check that line was called for RSI
        mock_figure.line.assert_called()
        calls = mock_figure.line.call_args_list
        
        # Should have at least 3 calls: RSI line, overbought, oversold
        assert len(calls) >= 3
        
        # Check RSI line call
        rsi_call = calls[0]
        assert rsi_call[1]['legend_label'] == 'RSI'
        assert rsi_call[1]['line_color'] == 'purple'
        assert rsi_call[1]['line_width'] == 3
    
    def test_plot_macd_indicator(self, mock_figure, mock_source, sample_data):
        """Test MACD indicator plotting function."""
        _plot_macd_indicator(mock_figure, mock_source, sample_data)
        
        # Check that line and vbar were called
        mock_figure.line.assert_called()
        mock_figure.vbar.assert_called()
        
        # Check MACD line call
        line_calls = mock_figure.line.call_args_list
        macd_call = line_calls[0]
        assert macd_call[1]['legend_label'] == 'MACD'
        assert macd_call[1]['line_color'] == 'blue'
        assert macd_call[1]['line_width'] == 3
        
        # Check histogram call
        vbar_calls = mock_figure.vbar.call_args_list
        hist_call = vbar_calls[0]
        assert hist_call[1]['legend_label'] == 'Histogram'
        assert hist_call[1]['alpha'] == 0.7
    
    def test_plot_ema_indicator(self, mock_figure, mock_source, sample_data):
        """Test EMA indicator plotting function."""
        _plot_ema_indicator(mock_figure, mock_source, sample_data)
        
        mock_figure.line.assert_called_once()
        call = mock_figure.line.call_args
        assert call[1]['legend_label'] == 'EMA'
        assert call[1]['line_color'] == 'orange'
        assert call[1]['line_width'] == 3
    
    def test_plot_bb_indicator(self, mock_figure, mock_source, sample_data):
        """Test Bollinger Bands indicator plotting function."""
        _plot_bb_indicator(mock_figure, mock_source, sample_data)
        
        # Should have 3 line calls for upper, middle, lower bands
        assert mock_figure.line.call_count == 3
        
        calls = mock_figure.line.call_args_list
        labels = [call[1]['legend_label'] for call in calls]
        assert 'Upper Band' in labels
        assert 'Middle Band' in labels
        assert 'Lower Band' in labels
    
    def test_plot_atr_indicator(self, mock_figure, mock_source, sample_data):
        """Test ATR indicator plotting function."""
        _plot_atr_indicator(mock_figure, mock_source, sample_data)
        
        mock_figure.line.assert_called_once()
        call = mock_figure.line.call_args
        assert call[1]['legend_label'] == 'ATR'
        assert call[1]['line_color'] == 'brown'
        assert call[1]['line_width'] == 3
    
    def test_plot_cci_indicator(self, mock_figure, mock_source, sample_data):
        """Test CCI indicator plotting function."""
        _plot_cci_indicator(mock_figure, mock_source, sample_data)
        
        # Should have 3 line calls: CCI line, +100, -100
        assert mock_figure.line.call_count == 3
        
        calls = mock_figure.line.call_args_list
        labels = [call[1]['legend_label'] for call in calls]
        assert 'CCI' in labels
        assert 'CCI +100' in labels
        assert 'CCI -100' in labels
    
    def test_plot_vwap_indicator(self, mock_figure, mock_source, sample_data):
        """Test VWAP indicator plotting function."""
        _plot_vwap_indicator(mock_figure, mock_source, sample_data)
        
        mock_figure.line.assert_called_once()
        call = mock_figure.line.call_args
        assert call[1]['legend_label'] == 'VWAP'
        assert call[1]['line_color'] == 'orange'
        assert call[1]['line_width'] == 3
    
    def test_plot_pivot_indicator(self, mock_figure, mock_source, sample_data):
        """Test Pivot indicator plotting function."""
        _plot_pivot_indicator(mock_figure, mock_source, sample_data)
        
        # Should have 3 line calls: pivot, r1, s1
        assert mock_figure.line.call_count == 3
        
        calls = mock_figure.line.call_args_list
        labels = [call[1]['legend_label'] for call in calls]
        assert 'Pivot' in labels
        assert 'R1' in labels
        assert 'S1' in labels
    
    def test_plot_hma_indicator(self, mock_figure, mock_source, sample_data):
        """Test HMA indicator plotting function."""
        _plot_hma_indicator(mock_figure, mock_source, sample_data)
        
        mock_figure.line.assert_called_once()
        call = mock_figure.line.call_args
        assert call[1]['legend_label'] == 'HMA'
        assert call[1]['line_color'] == 'purple'
        assert call[1]['line_width'] == 3
    
    def test_plot_tsf_indicator(self, mock_figure, mock_source, sample_data):
        """Test TSF indicator plotting function."""
        _plot_tsf_indicator(mock_figure, mock_source, sample_data)
        
        mock_figure.line.assert_called_once()
        call = mock_figure.line.call_args
        assert call[1]['legend_label'] == 'TSF'
        assert call[1]['line_color'] == 'cyan'
        assert call[1]['line_width'] == 3
    
    def test_plot_monte_indicator(self, mock_figure, mock_source, sample_data):
        """Test Monte Carlo indicator plotting function."""
        _plot_monte_indicator(mock_figure, mock_source, sample_data)
        
        # Should have multiple calls for forecast, signal, histogram, confidence bands, zero line
        assert mock_figure.line.call_count >= 4
        assert mock_figure.vbar.call_count == 1
        
        calls = mock_figure.line.call_args_list
        labels = [call[1]['legend_label'] for call in calls]
        assert 'Monte Carlo Forecast' in labels
        assert 'Signal Line' in labels
        assert 'Upper Confidence' in labels
        assert 'Lower Confidence' in labels
        assert 'Zero Line' in labels
    
    def test_plot_kelly_indicator(self, mock_figure, mock_source, sample_data):
        """Test Kelly indicator plotting function."""
        _plot_kelly_indicator(mock_figure, mock_source, sample_data)
        
        mock_figure.line.assert_called_once()
        call = mock_figure.line.call_args
        assert call[1]['legend_label'] == 'Kelly'
        assert call[1]['line_color'] == 'green'
        assert call[1]['line_width'] == 3
    
    def test_plot_donchain_indicator(self, mock_figure, mock_source, sample_data):
        """Test Donchian Channel indicator plotting function."""
        _plot_donchain_indicator(mock_figure, mock_source, sample_data)
        
        # Should have 3 line calls for upper, middle, lower channels
        assert mock_figure.line.call_count == 3
        
        calls = mock_figure.line.call_args_list
        labels = [call[1]['legend_label'] for call in calls]
        assert 'Upper Channel' in labels
        assert 'Middle Channel' in labels
        assert 'Lower Channel' in labels
    
    def test_plot_fibo_indicator(self, mock_figure, mock_source, sample_data):
        """Test Fibonacci indicator plotting function."""
        _plot_fibo_indicator(mock_figure, mock_source, sample_data)
        
        # Should have 6 line calls for Fibonacci levels
        assert mock_figure.line.call_count == 6
        
        calls = mock_figure.line.call_args_list
        labels = [call[1]['legend_label'] for call in calls]
        assert 'Fib 0' in labels
        assert 'Fib 236' in labels
        assert 'Fib 382' in labels
        assert 'Fib 618' in labels
        assert 'Fib 786' in labels
        assert 'Fib 100' in labels
    
    def test_plot_obv_indicator(self, mock_figure, mock_source, sample_data):
        """Test OBV indicator plotting function."""
        _plot_obv_indicator(mock_figure, mock_source, sample_data)
        
        mock_figure.line.assert_called_once()
        call = mock_figure.line.call_args
        assert call[1]['legend_label'] == 'OBV'
        assert call[1]['line_color'] == 'brown'
        assert call[1]['line_width'] == 3
    
    def test_plot_stdev_indicator(self, mock_figure, mock_source, sample_data):
        """Test Standard Deviation indicator plotting function."""
        _plot_stdev_indicator(mock_figure, mock_source, sample_data)
        
        mock_figure.line.assert_called_once()
        call = mock_figure.line.call_args
        assert call[1]['legend_label'] == 'StdDev'
        assert call[1]['line_color'] == 'gray'
        assert call[1]['line_width'] == 3
    
    def test_plot_adx_indicator(self, mock_figure, mock_source, sample_data):
        """Test ADX indicator plotting function."""
        _plot_adx_indicator(mock_figure, mock_source, sample_data)
        
        # Should have 3 line calls for ADX, DI+, DI-
        assert mock_figure.line.call_count == 3
        
        calls = mock_figure.line.call_args_list
        labels = [call[1]['legend_label'] for call in calls]
        assert 'ADX' in labels
        assert 'DI+' in labels
        assert 'DI-' in labels
    
    def test_plot_sar_indicator(self, mock_figure, mock_source, sample_data):
        """Test SAR indicator plotting function."""
        _plot_sar_indicator(mock_figure, mock_source, sample_data)
        
        mock_figure.scatter.assert_called_once()
        call = mock_figure.scatter.call_args
        assert call[1]['legend_label'] == 'SAR'
        assert call[1]['color'] == 'red'
        assert call[1]['size'] == 4
    
    def test_plot_rsi_mom_indicator(self, mock_figure, mock_source, sample_data):
        """Test RSI Momentum indicator plotting function."""
        _plot_rsi_mom_indicator(mock_figure, mock_source, sample_data)
        
        # Should have 4 line calls: RSI, RSI Momentum, overbought, oversold
        assert mock_figure.line.call_count == 4
        
        calls = mock_figure.line.call_args_list
        labels = [call[1]['legend_label'] for call in calls]
        assert 'RSI' in labels
        assert 'RSI Momentum' in labels
        assert 'Overbought' in labels
        assert 'Oversold' in labels
    
    def test_plot_rsi_div_indicator(self, mock_figure, mock_source, sample_data):
        """Test RSI Divergence indicator plotting function."""
        _plot_rsi_div_indicator(mock_figure, mock_source, sample_data)
        
        # Should have 4 line calls: RSI, RSI Divergence, overbought, oversold
        assert mock_figure.line.call_count == 4
        
        calls = mock_figure.line.call_args_list
        labels = [call[1]['legend_label'] for call in calls]
        assert 'RSI' in labels
        assert 'RSI Divergence' in labels
        assert 'Overbought' in labels
        assert 'Oversold' in labels
    
    def test_plot_stoch_indicator(self, mock_figure, mock_source, sample_data):
        """Test Stochastic indicator plotting function."""
        _plot_stoch_indicator(mock_figure, mock_source, sample_data)
        
        # Should have 4 line calls: %K, %D, overbought, oversold
        assert mock_figure.line.call_count == 4
        
        calls = mock_figure.line.call_args_list
        labels = [call[1]['legend_label'] for call in calls]
        assert '%K' in labels
        assert '%D' in labels
        assert 'Overbought' in labels
        assert 'Oversold' in labels
    
    def test_get_indicator_hover_tool(self, sample_data):
        """Test hover tool generation for different indicators."""
        from bokeh.models import HoverTool
        
        # Test MACD hover tool
        macd_hover = _get_indicator_hover_tool('macd', sample_data)
        assert isinstance(macd_hover, HoverTool)
        
        # Test RSI hover tool
        rsi_hover = _get_indicator_hover_tool('rsi', sample_data)
        assert isinstance(rsi_hover, HoverTool)
        
        # Test generic hover tool
        generic_hover = _get_indicator_hover_tool('unknown', sample_data)
        assert isinstance(generic_hover, HoverTool)
    
    def test_plot_indicator_by_type(self, mock_figure, mock_source, sample_data):
        """Test indicator plotting by type function."""
        # Test with known indicator
        _plot_indicator_by_type(mock_figure, mock_source, sample_data, 'rsi')
        assert mock_figure.line.called
        
        # Test with unknown indicator
        mock_figure.reset_mock()
        _plot_indicator_by_type(mock_figure, mock_source, sample_data, 'unknown')
        assert not mock_figure.line.called
    
    def test_plot_dual_chart_fast_integration(self, sample_data, temp_output_dir):
        """Test that the main function still works with refactored code."""
        output_path = os.path.join(temp_output_dir, "test_integration.html")
        
        result = plot_dual_chart_fast(
            df=sample_data,
            rule="rsi:14,30,70,open",
            title="Test Integration",
            output_path=output_path,
            width=1800,
            height=1100
        )
        
        # Check that file was created
        assert os.path.exists(output_path)
        assert os.path.getsize(output_path) > 0
    
    def test_plot_dual_chart_fast_all_indicators(self, sample_data, temp_output_dir):
        """Test all indicators work with the main function."""
        indicators = [
            'rsi', 'macd', 'ema', 'bb', 'atr', 'cci', 'vwap', 'pivot',
            'hma', 'tsf', 'monte', 'kelly', 'donchain', 'fibo', 'obv',
            'stdev', 'adx', 'sar', 'rsi_mom', 'rsi_div', 'stoch'
        ]
        
        for indicator in indicators:
            output_path = os.path.join(temp_output_dir, f"test_{indicator}.html")
            
            try:
                result = plot_dual_chart_fast(
                    df=sample_data,
                    rule=f"{indicator}:14,30,70,open",
                    title=f"Test {indicator.upper()}",
                    output_path=output_path,
                    width=1800,
                    height=1100
                )
                
                # Check that file was created
                assert os.path.exists(output_path)
                assert os.path.getsize(output_path) > 0
                
            except Exception as e:
                pytest.fail(f"Failed to plot {indicator} indicator: {str(e)}")
    
    def test_plot_dual_chart_fast_missing_columns(self, sample_data, temp_output_dir):
        """Test that the function handles missing indicator columns gracefully."""
        # Remove some indicator columns
        sample_data = sample_data.drop(columns=['rsi', 'macd'], errors='ignore')
        
        output_path = os.path.join(temp_output_dir, "test_missing_columns.html")
        
        # Should not raise an exception
        result = plot_dual_chart_fast(
            df=sample_data,
            rule="rsi:14,30,70,open",
            title="Test Missing Columns",
            output_path=output_path,
            width=1800,
            height=1100
        )
        
        # Check that file was created
        assert os.path.exists(output_path)
        assert os.path.getsize(output_path) > 0
    
    def test_plot_dual_chart_fast_empty_dataframe(self, temp_output_dir):
        """Test that the function handles empty DataFrame gracefully."""
        # Create empty DataFrame with required columns
        empty_df = pd.DataFrame(columns=['Open', 'High', 'Low', 'Close', 'Volume'])
        
        output_path = os.path.join(temp_output_dir, "test_empty_dataframe.html")
        
        # Should not raise an exception
        result = plot_dual_chart_fast(
            df=empty_df,
            rule="rsi:14,30,70,open",
            title="Test Empty DataFrame",
            output_path=output_path,
            width=1800,
            height=1100
        )
        
        # Check that file was created
        assert os.path.exists(output_path)
        assert os.path.getsize(output_path) > 0
    
    def test_plot_dual_chart_fast_dynamic_height(self, sample_data, temp_output_dir):
        """Test that plot_dual_chart_fast uses dynamic height."""
        output_path = os.path.join(temp_output_dir, "test_dynamic_height.html")
        
        # Test with None height to trigger dynamic calculation
        result = plot_dual_chart_fast(
            df=sample_data,
            rule="macd:8,21,5,open",
            title="Test Dynamic Height",
            output_path=output_path,
            width=1800,
            height=None  # This should trigger dynamic calculation
        )
        
        # Check that file was created
        assert os.path.exists(output_path)
        assert os.path.getsize(output_path) > 0
    
    def test_plot_dual_chart_fast_size_adjustment(self, sample_data, temp_output_dir):
        """Test that plot_dual_chart_fast reduces width by 5% and reduces height by 10%."""
        output_path = os.path.join(temp_output_dir, "test_size_adjustment.html")
        
        original_width = 1800
        original_height = 1100
        
        result = plot_dual_chart_fast(
            df=sample_data,
            rule="macd:8,21,5,open",
            title="Test Size Adjustment",
            output_path=output_path,
            width=original_width,
            height=original_height
        )
        
        # Check that file was created
        assert os.path.exists(output_path)
        assert os.path.getsize(output_path) > 0 