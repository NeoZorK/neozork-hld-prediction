# -*- coding: utf-8 -*-
# tests/plotting/test_dual_chart_plot.py

"""
Unit tests for dual chart plotting functionality.
Tests the new feature that creates a secondary chart below the main chart
when user specifies --rule parameter with indicator parameters.
"""

import pytest
import pandas as pd
import numpy as np
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime, timedelta

from src.plotting.dual_chart_plot import (
    plot_dual_chart_results,
    is_dual_chart_rule,
    get_supported_indicators,
    calculate_additional_indicator,
    create_dual_chart_layout
)


class TestDualChartPlot:
    """Test class for dual chart plotting functionality."""

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

    def test_is_dual_chart_rule_valid_indicators(self):
        """Test that valid indicators return True for dual chart."""
        valid_rules = [
            'rsi:14,30,70,open',
            'macd:12,26,9,close',
            'ema:20,close',
            'bb:20,2.0,close',
            'atr:14',
            'cci:20,close',
            'vwap:close',
            'pivot:close',
            'hma:20,close',
            'tsf:20,5,close',
            'monte:1000,252',
            'kelly:20',
            'donchain:20',
            'fibo:0.236,0.382,0.5,0.618,0.786',
            'obv',
            'stdev:20,close',
            'adx:14',
            'sar:0.02,0.2'
        ]
        
        for rule in valid_rules:
            assert is_dual_chart_rule(rule), f"Rule {rule} should be valid for dual chart"

    def test_is_dual_chart_rule_excluded_indicators(self):
        """Test that excluded indicators return False for dual chart."""
        excluded_rules = [
            'OHLCV',
            'AUTO',
            'PV',
            'SR',
            'PHLD',
            'PRESSURE_VECTOR',
            'SUPPORT_RESISTANTS',
            'PREDICT_HIGH_LOW_DIRECTION'
        ]
        
        for rule in excluded_rules:
            assert not is_dual_chart_rule(rule), f"Rule {rule} should be excluded from dual chart"

    def test_is_dual_chart_rule_invalid_format(self):
        """Test that invalid rule formats return False."""
        invalid_rules = [
            'invalid:indicator',
            'rsi:invalid,params',
            'macd:12,26',  # Missing parameters
            'ema:20,invalid_price_type',
            'bb:20,2.0,invalid_price_type'
        ]
        
        for rule in invalid_rules:
            assert not is_dual_chart_rule(rule), f"Rule {rule} should be invalid"

    def test_get_supported_indicators(self):
        """Test that all supported indicators are returned."""
        supported = get_supported_indicators()
        
        expected_indicators = [
            'rsi', 'rsi_mom', 'rsi_div', 'macd', 'stoch', 'ema', 'bb', 'atr',
            'cci', 'vwap', 'pivot', 'hma', 'tsf', 'monte', 'kelly', 'donchain',
            'fibo', 'obv', 'stdev', 'adx', 'sar'
        ]
        
        for indicator in expected_indicators:
            assert indicator in supported, f"Indicator {indicator} should be supported"

    def test_get_supported_indicators_excludes_forbidden(self):
        """Test that forbidden indicators are not included."""
        supported = get_supported_indicators()
        
        forbidden_indicators = ['ohlcv', 'auto', 'pv', 'sr', 'phld']
        
        for indicator in forbidden_indicators:
            assert indicator not in supported, f"Indicator {indicator} should not be supported"

    @patch('src.plotting.dual_chart_plot.calculate_rsi')
    def test_calculate_additional_indicator_rsi(self, mock_calculate_rsi):
        """Test calculation of RSI indicator."""
        mock_calculate_rsi.return_value = pd.Series([50.0] * 100, index=self.sample_data.index)
        
        result = calculate_additional_indicator(self.sample_data, 'rsi:14,30,70,open')
        
        assert 'rsi' in result.columns
        assert len(result) == len(self.sample_data)
        mock_calculate_rsi.assert_called_once()

    @patch('src.plotting.dual_chart_plot.calculate_macd')
    def test_calculate_additional_indicator_macd(self, mock_calculate_macd):
        """Test calculation of MACD indicator."""
        mock_calculate_macd.return_value = pd.DataFrame({
            'macd': [0.1] * 100,
            'signal': [0.05] * 100,
            'histogram': [0.05] * 100
        }, index=self.sample_data.index)
        
        result = calculate_additional_indicator(self.sample_data, 'macd:12,26,9,close')
        
        assert 'macd' in result.columns
        assert 'signal' in result.columns
        assert 'histogram' in result.columns
        assert len(result) == len(self.sample_data)

    @patch('src.plotting.dual_chart_plot.calculate_ema')
    def test_calculate_additional_indicator_ema(self, mock_calculate_ema):
        """Test calculation of EMA indicator."""
        mock_calculate_ema.return_value = pd.Series([150.0] * 100, index=self.sample_data.index)
        
        result = calculate_additional_indicator(self.sample_data, 'ema:20,close')
        
        assert 'ema' in result.columns
        assert len(result) == len(self.sample_data)

    def test_calculate_additional_indicator_invalid(self):
        """Test calculation with invalid indicator."""
        with pytest.raises(ValueError, match="Unsupported indicator"):
            calculate_additional_indicator(self.sample_data, 'invalid:param')

    def test_create_dual_chart_layout_fastest(self):
        """Test creation of dual chart layout for fastest mode."""
        layout = create_dual_chart_layout('fastest', 'rsi:14,30,70,open')
        
        assert layout['mode'] == 'fastest'
        assert layout['main_chart_height'] == 0.6
        assert layout['indicator_chart_height'] == 0.4
        assert layout['indicator_name'] == 'RSI'
        assert layout['show_volume'] == False

    def test_create_dual_chart_layout_fast(self):
        """Test creation of dual chart layout for fast mode."""
        layout = create_dual_chart_layout('fast', 'macd:12,26,9,close')
        
        assert layout['mode'] == 'fast'
        assert layout['main_chart_height'] == 0.6
        assert layout['indicator_chart_height'] == 0.4
        assert layout['indicator_name'] == 'MACD'
        assert layout['show_volume'] == False

    def test_create_dual_chart_layout_mpl(self):
        """Test creation of dual chart layout for mpl mode."""
        layout = create_dual_chart_layout('mpl', 'ema:20,close')
        
        assert layout['mode'] == 'mpl'
        assert layout['main_chart_height'] == 0.6
        assert layout['indicator_chart_height'] == 0.4
        assert layout['indicator_name'] == 'EMA'
        assert layout['show_volume'] == False

    def test_create_dual_chart_layout_seaborn(self):
        """Test creation of dual chart layout for seaborn mode."""
        layout = create_dual_chart_layout('sb', 'bb:20,2.0,close')
        
        assert layout['mode'] == 'sb'
        assert layout['main_chart_height'] == 0.6
        assert layout['indicator_chart_height'] == 0.4
        assert layout['indicator_name'] == 'Bollinger Bands'
        assert layout['show_volume'] == False

    def test_create_dual_chart_layout_terminal(self):
        """Test creation of dual chart layout for terminal mode."""
        layout = create_dual_chart_layout('term', 'atr:14')
        
        assert layout['mode'] == 'term'
        assert layout['main_chart_height'] == 0.6
        assert layout['indicator_chart_height'] == 0.4
        assert layout['indicator_name'] == 'ATR'
        assert layout['show_volume'] == False

    @patch('src.plotting.dual_chart_plot.plot_dual_chart_fastest')
    def test_plot_dual_chart_results_fastest(self, mock_plot_fastest):
        """Test dual chart plotting for fastest mode."""
        mock_plot_fastest.return_value = Mock()
        
        result = plot_dual_chart_results(
            self.sample_data,
            'rsi:14,30,70,open',
            'Test Title',
            mode='fastest'
        )
        
        assert result is not None
        mock_plot_fastest.assert_called_once()

    @patch('src.plotting.dual_chart_plot.plot_dual_chart_fast')
    def test_plot_dual_chart_results_fast(self, mock_plot_fast):
        """Test dual chart plotting for fast mode."""
        mock_plot_fast.return_value = Mock()
        
        result = plot_dual_chart_results(
            self.sample_data,
            'macd:12,26,9,close',
            'Test Title',
            mode='fast'
        )
        
        assert result is not None
        mock_plot_fast.assert_called_once()

    @patch('src.plotting.dual_chart_plot.plot_dual_chart_mpl')
    def test_plot_dual_chart_results_mpl(self, mock_plot_mpl):
        """Test dual chart plotting for mpl mode."""
        mock_plot_mpl.return_value = Mock()
        
        result = plot_dual_chart_results(
            self.sample_data,
            'ema:20,close',
            'Test Title',
            mode='mpl'
        )
        
        assert result is not None
        mock_plot_mpl.assert_called_once()

    @patch('src.plotting.dual_chart_plot.plot_dual_chart_seaborn')
    def test_plot_dual_chart_results_seaborn(self, mock_plot_seaborn):
        """Test dual chart plotting for seaborn mode."""
        mock_plot_seaborn.return_value = Mock()
        
        result = plot_dual_chart_results(
            self.sample_data,
            'bb:20,2.0,close',
            'Test Title',
            mode='sb'
        )
        
        assert result is not None
        mock_plot_seaborn.assert_called_once()

    @patch('src.plotting.dual_chart_plot.plot_dual_chart_terminal')
    def test_plot_dual_chart_results_terminal(self, mock_plot_terminal):
        """Test dual chart plotting for terminal mode."""
        mock_plot_terminal.return_value = Mock()
        
        result = plot_dual_chart_results(
            self.sample_data,
            'atr:14',
            'Test Title',
            mode='term'
        )
        
        assert result is not None
        mock_plot_terminal.assert_called_once()

    def test_plot_dual_chart_results_invalid_mode(self):
        """Test dual chart plotting with invalid mode."""
        with pytest.raises(ValueError, match="Unsupported plotting mode"):
            plot_dual_chart_results(
                self.sample_data,
                'rsi:14,30,70,open',
                'Test Title',
                mode='invalid_mode'
            )

    def test_plot_dual_chart_results_invalid_rule(self):
        """Test dual chart plotting with invalid rule."""
        with pytest.raises(ValueError, match="Invalid rule for dual chart"):
            plot_dual_chart_results(
                self.sample_data,
                'OHLCV',  # Excluded rule
                'Test Title',
                mode='fastest'
            )

    def test_plot_dual_chart_results_empty_data(self):
        """Test dual chart plotting with empty data."""
        empty_data = pd.DataFrame()
        
        with pytest.raises(ValueError, match="DataFrame is empty"):
            plot_dual_chart_results(
                empty_data,
                'rsi:14,30,70,open',
                'Test Title',
                mode='fastest'
            )

    def test_plot_dual_chart_results_missing_columns(self):
        """Test dual chart plotting with missing required columns."""
        incomplete_data = pd.DataFrame({
            'Open': [100, 101, 102],
            'Close': [101, 102, 103]
            # Missing High, Low, Volume
        })
        
        with pytest.raises(ValueError, match="Missing required columns"):
            plot_dual_chart_results(
                incomplete_data,
                'rsi:14,30,70,open',
                'Test Title',
                mode='fastest'
            )

    @patch('src.plotting.dual_chart_plot.calculate_additional_indicator')
    @patch('src.plotting.dual_chart_plot.plot_dual_chart_fastest')
    def test_plot_dual_chart_results_with_indicator_calculation(self, mock_plot, mock_calc):
        """Test that indicator calculation is called before plotting."""
        mock_calc.return_value = self.sample_data.copy()
        mock_plot.return_value = Mock()
        
        plot_dual_chart_results(
            self.sample_data,
            'rsi:14,30,70,open',
            'Test Title',
            mode='fastest'
        )
        
        mock_calc.assert_called_once_with(self.sample_data, 'rsi:14,30,70,open')
        mock_plot.assert_called_once()

    def test_plot_dual_chart_results_default_parameters(self):
        """Test dual chart plotting with default parameters."""
        with patch('src.plotting.dual_chart_plot.plot_dual_chart_fastest') as mock_plot:
            mock_plot.return_value = Mock()
            
            result = plot_dual_chart_results(
                self.sample_data,
                'rsi:14,30,70,open'
            )
            
            assert result is not None
            # Check that default mode is 'fastest'
            mock_plot.assert_called_once()

    def test_plot_dual_chart_results_custom_output_path(self):
        """Test dual chart plotting with custom output path."""
        with patch('src.plotting.dual_chart_plot.plot_dual_chart_fastest') as mock_plot:
            mock_plot.return_value = Mock()
            
            result = plot_dual_chart_results(
                self.sample_data,
                'rsi:14,30,70,open',
                output_path='custom/path/plot.html'
            )
            
            assert result is not None
            # Check that output_path is passed to plotting function
            call_args = mock_plot.call_args
            assert 'output_path' in call_args[1]
            assert call_args[1]['output_path'] == 'custom/path/plot.html'


class TestDualChartPlotIntegration:
    """Integration tests for dual chart plotting."""

    def setup_method(self):
        """Set up test data for integration tests."""
        dates = pd.date_range('2023-01-01', periods=50, freq='D')
        self.test_data = pd.DataFrame({
            'DateTime': dates,
            'Open': np.linspace(100, 200, 50),
            'High': np.linspace(200, 300, 50),
            'Low': np.linspace(50, 150, 50),
            'Close': np.linspace(110, 190, 50),
            'Volume': np.random.uniform(1000, 10000, 50)
        })
        self.test_data.set_index('DateTime', inplace=True)

    def test_full_dual_chart_workflow_rsi(self):
        """Test complete dual chart workflow with RSI."""
        # This test would require actual plotting libraries
        # For now, we'll test the workflow without actual plotting
        with patch('src.plotting.dual_chart_plot.plot_dual_chart_fastest') as mock_plot:
            mock_plot.return_value = Mock()
            
            result = plot_dual_chart_results(
                self.test_data,
                'rsi:14,30,70,open',
                'RSI Dual Chart Test',
                mode='fastest'
            )
            
            assert result is not None
            mock_plot.assert_called_once()

    def test_full_dual_chart_workflow_macd(self):
        """Test complete dual chart workflow with MACD."""
        with patch('src.plotting.dual_chart_plot.plot_dual_chart_fastest') as mock_plot:
            mock_plot.return_value = Mock()
            
            result = plot_dual_chart_results(
                self.test_data,
                'macd:12,26,9,close',
                'MACD Dual Chart Test',
                mode='fastest'
            )
            
            assert result is not None
            mock_plot.assert_called_once()

    def test_full_dual_chart_workflow_ema(self):
        """Test complete dual chart workflow with EMA."""
        with patch('src.plotting.dual_chart_plot.plot_dual_chart_fastest') as mock_plot:
            mock_plot.return_value = Mock()
            
            result = plot_dual_chart_results(
                self.test_data,
                'ema:20,close',
                'EMA Dual Chart Test',
                mode='fastest'
            )
            
            assert result is not None
            mock_plot.assert_called_once()


if __name__ == '__main__':
    pytest.main([__file__]) 