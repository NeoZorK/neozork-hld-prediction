# -*- coding: utf-8 -*-
"""
Tests for dual_chart_fastest module.
"""

import pytest
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta

from src.plotting.dual_chart_fastest import (
    add_rsi_indicator,
    add_rsi_momentum_indicator,
    add_macd_indicator,
    add_ema_indicator,
    add_bollinger_bands_indicator,
    add_atr_indicator
)


class TestRSIIndicators:
    """Test RSI indicator functions."""
    
    @pytest.fixture
    def sample_data(self):
        """Create sample data for testing."""
        dates = pd.date_range(start='2023-01-01', periods=100, freq='D')
        np.random.seed(42)
        
        # Create sample OHLCV data
        data = {
            'open': np.random.uniform(100, 200, 100),
            'high': np.random.uniform(200, 300, 100),
            'low': np.random.uniform(50, 100, 100),
            'close': np.random.uniform(100, 200, 100),
            'volume': np.random.uniform(1000, 5000, 100),
        }
        
        # Create RSI data
        data['rsi'] = np.random.uniform(0, 100, 100)
        data['rsi_overbought'] = [70] * 100
        data['rsi_oversold'] = [30] * 100
        data['rsi_momentum'] = np.random.uniform(-50, 50, 100)
        
        df = pd.DataFrame(data, index=dates)
        return df
    
    @pytest.fixture
    def sample_figure(self):
        """Create a sample figure for testing."""
        fig = make_subplots(
            rows=2, cols=1,
            subplot_titles=(None, None),
            vertical_spacing=0.04,
            row_heights=[0.62, 0.38],
            specs=[[{"secondary_y": False}],
                   [{"secondary_y": False}]]
        )
        return fig
    
    def test_add_rsi_indicator_basic(self, sample_figure, sample_data):
        """Test basic RSI indicator addition."""
        initial_traces = len(sample_figure.data)
        
        add_rsi_indicator(sample_figure, sample_data)
        
        # Check that traces were added
        assert len(sample_figure.data) > initial_traces
        
        # Check that RSI line was added
        rsi_traces = [trace for trace in sample_figure.data if trace.name == 'RSI']
        assert len(rsi_traces) == 1
        
        # Check that overbought/oversold lines were added
        overbought_traces = [trace for trace in sample_figure.data if 'Overbought' in trace.name]
        oversold_traces = [trace for trace in sample_figure.data if 'Oversold' in trace.name]
        assert len(overbought_traces) == 1
        assert len(oversold_traces) == 1
    
    def test_add_rsi_indicator_missing_data(self, sample_figure):
        """Test RSI indicator with missing RSI data."""
        # Create data without RSI column
        dates = pd.date_range(start='2023-01-01', periods=10, freq='D')
        data = {
            'open': np.random.uniform(100, 200, 10),
            'high': np.random.uniform(200, 300, 10),
            'low': np.random.uniform(50, 100, 10),
            'close': np.random.uniform(100, 200, 10),
        }
        df = pd.DataFrame(data, index=dates)
        
        initial_traces = len(sample_figure.data)
        
        # Should not raise an error
        add_rsi_indicator(sample_figure, df)
        
        # No traces should be added
        assert len(sample_figure.data) == initial_traces
    
    def test_add_rsi_momentum_indicator_basic(self, sample_figure, sample_data):
        """Test basic RSI momentum indicator addition."""
        initial_traces = len(sample_figure.data)
        
        add_rsi_momentum_indicator(sample_figure, sample_data)
        
        # Check that traces were added
        assert len(sample_figure.data) > initial_traces
        
        # Check that RSI line was added
        rsi_traces = [trace for trace in sample_figure.data if trace.name == 'RSI']
        assert len(rsi_traces) == 1
        
        # Check that RSI momentum line was added
        momentum_traces = [trace for trace in sample_figure.data if trace.name == 'RSI Momentum']
        assert len(momentum_traces) == 1
        
        # Check that zero line was added
        zero_traces = [trace for trace in sample_figure.data if trace.name == 'Zero Line']
        assert len(zero_traces) == 1
    
    def test_add_rsi_momentum_indicator_missing_momentum(self, sample_figure, sample_data):
        """Test RSI momentum indicator with missing momentum data."""
        # Remove momentum column
        data_without_momentum = sample_data.drop(columns=['rsi_momentum'])
        
        initial_traces = len(sample_figure.data)
        
        add_rsi_momentum_indicator(sample_figure, data_without_momentum)
        
        # Should still add RSI line but not momentum
        assert len(sample_figure.data) > initial_traces
        
        # Check that RSI line was added
        rsi_traces = [trace for trace in sample_figure.data if trace.name == 'RSI']
        assert len(rsi_traces) == 1
        
        # Check that momentum line was NOT added
        momentum_traces = [trace for trace in sample_figure.data if trace.name == 'RSI Momentum']
        assert len(momentum_traces) == 0
    
    def test_rsi_indicator_colors(self, sample_figure, sample_data):
        """Test that RSI indicator uses correct colors."""
        add_rsi_indicator(sample_figure, sample_data)
        
        # Find RSI trace
        rsi_trace = next((trace for trace in sample_figure.data if trace.name == 'RSI'), None)
        assert rsi_trace is not None
        assert rsi_trace.line.color == 'purple'
        assert rsi_trace.line.width == 3
    
    def test_rsi_momentum_indicator_colors(self, sample_figure, sample_data):
        """Test that RSI momentum indicator uses correct colors."""
        add_rsi_momentum_indicator(sample_figure, sample_data)
        
        # Find momentum trace
        momentum_trace = next((trace for trace in sample_figure.data if trace.name == 'RSI Momentum'), None)
        assert momentum_trace is not None
        assert momentum_trace.line.color == 'orange'
        assert momentum_trace.line.width == 2
    
    def test_rsi_overbought_oversold_values(self, sample_figure, sample_data):
        """Test that overbought/oversold lines use correct values."""
        add_rsi_indicator(sample_figure, sample_data)
        
        # Find overbought trace
        overbought_trace = next((trace for trace in sample_figure.data if 'Overbought' in trace.name), None)
        assert overbought_trace is not None
        assert all(y == 70 for y in overbought_trace.y)
        
        # Find oversold trace
        oversold_trace = next((trace for trace in sample_figure.data if 'Oversold' in trace.name), None)
        assert oversold_trace is not None
        assert all(y == 30 for y in oversold_trace.y)


class TestMACDIndicator:
    """Test MACD indicator function."""
    
    @pytest.fixture
    def macd_data(self):
        """Create sample MACD data for testing."""
        dates = pd.date_range(start='2023-01-01', periods=100, freq='D')
        np.random.seed(42)
        
        # Create sample OHLCV data
        data = {
            'open': np.random.uniform(100, 200, 100),
            'high': np.random.uniform(200, 300, 100),
            'low': np.random.uniform(50, 100, 100),
            'close': np.random.uniform(100, 200, 100),
            'volume': np.random.uniform(1000, 5000, 100),
        }
        
        # Create MACD data
        data['macd'] = np.random.uniform(-2, 2, 100)
        data['macd_signal'] = np.random.uniform(-1.5, 1.5, 100)
        data['macd_histogram'] = np.random.uniform(-1, 1, 100)
        
        df = pd.DataFrame(data, index=dates)
        return df
    
    @pytest.fixture
    def sample_figure(self):
        """Create a sample figure for testing."""
        fig = make_subplots(
            rows=2, cols=1,
            subplot_titles=(None, None),
            vertical_spacing=0.04,
            row_heights=[0.62, 0.38],
            specs=[[{"secondary_y": False}],
                   [{"secondary_y": False}]]
        )
        return fig
    
    def test_add_macd_indicator_basic(self, sample_figure, macd_data):
        """Test basic MACD indicator addition."""
        initial_traces = len(sample_figure.data)
        
        add_macd_indicator(sample_figure, macd_data)
        
        # Check that traces were added
        assert len(sample_figure.data) > initial_traces
        
        # Check that MACD line was added
        macd_traces = [trace for trace in sample_figure.data if trace.name == 'MACD']
        assert len(macd_traces) == 1
        
        # Check that Signal line was added
        signal_traces = [trace for trace in sample_figure.data if trace.name == 'Signal']
        assert len(signal_traces) == 1
        
        # Check that Histogram was added
        histogram_traces = [trace for trace in sample_figure.data if trace.name == 'Histogram']
        assert len(histogram_traces) == 1
    
    def test_add_macd_indicator_missing_data(self, sample_figure):
        """Test MACD indicator with missing MACD data."""
        # Create data without MACD columns
        dates = pd.date_range(start='2023-01-01', periods=10, freq='D')
        data = {
            'open': np.random.uniform(100, 200, 10),
            'high': np.random.uniform(200, 300, 10),
            'low': np.random.uniform(50, 100, 10),
            'close': np.random.uniform(100, 200, 10),
        }
        df = pd.DataFrame(data, index=dates)
        
        initial_traces = len(sample_figure.data)
        
        # Should not raise an error
        add_macd_indicator(sample_figure, df)
        
        # No traces should be added
        assert len(sample_figure.data) == initial_traces
    
    def test_add_macd_indicator_partial_data(self, sample_figure, macd_data):
        """Test MACD indicator with partial data."""
        # Remove some MACD columns
        partial_data = macd_data.drop(columns=['macd_signal', 'macd_histogram'])
        
        initial_traces = len(sample_figure.data)
        
        add_macd_indicator(sample_figure, partial_data)
        
        # Should add MACD line but not signal or histogram
        assert len(sample_figure.data) > initial_traces
        
        # Check that MACD line was added
        macd_traces = [trace for trace in sample_figure.data if trace.name == 'MACD']
        assert len(macd_traces) == 1
        
        # Check that Signal line was NOT added
        signal_traces = [trace for trace in sample_figure.data if trace.name == 'Signal']
        assert len(signal_traces) == 0
        
        # Check that Histogram was NOT added
        histogram_traces = [trace for trace in sample_figure.data if trace.name == 'Histogram']
        assert len(histogram_traces) == 0
    
    def test_macd_indicator_colors(self, sample_figure, macd_data):
        """Test that MACD indicator uses correct colors."""
        add_macd_indicator(sample_figure, macd_data)
        
        # Find MACD trace
        macd_trace = next((trace for trace in sample_figure.data if trace.name == 'MACD'), None)
        assert macd_trace is not None
        assert macd_trace.line.color == 'blue'
        assert macd_trace.line.width == 3
        
        # Find Signal trace
        signal_trace = next((trace for trace in sample_figure.data if trace.name == 'Signal'), None)
        assert signal_trace is not None
        assert signal_trace.line.color == 'red'
        assert signal_trace.line.width == 2
    
    def test_macd_histogram_colors(self, sample_figure, macd_data):
        """Test that MACD histogram uses correct colors based on values."""
        add_macd_indicator(sample_figure, macd_data)
        
        # Find Histogram trace
        histogram_trace = next((trace for trace in sample_figure.data if trace.name == 'Histogram'), None)
        assert histogram_trace is not None
        assert histogram_trace.opacity == 0.7
        
        # Check that colors are assigned based on values
        colors = histogram_trace.marker.color
        assert len(colors) == len(macd_data)
        
        # Verify color logic: green for >= 0, red for < 0
        for i, val in enumerate(macd_data['macd_histogram']):
            expected_color = 'green' if val >= 0 else 'red'
            assert colors[i] == expected_color 


class TestEMAIndicator:
    """Test EMA indicator function."""
    
    @pytest.fixture
    def ema_data(self):
        """Create sample EMA data for testing."""
        dates = pd.date_range(start='2023-01-01', periods=100, freq='D')
        np.random.seed(42)
        
        # Create sample OHLCV data
        data = {
            'open': np.random.uniform(100, 200, 100),
            'high': np.random.uniform(200, 300, 100),
            'low': np.random.uniform(50, 100, 100),
            'close': np.random.uniform(100, 200, 100),
            'volume': np.random.uniform(1000, 5000, 100),
        }
        
        # Create EMA data
        data['ema'] = np.random.uniform(120, 180, 100)
        
        df = pd.DataFrame(data, index=dates)
        return df
    
    @pytest.fixture
    def sample_figure(self):
        """Create a sample figure for testing."""
        fig = make_subplots(
            rows=2, cols=1,
            subplot_titles=(None, None),
            vertical_spacing=0.04,
            row_heights=[0.62, 0.38],
            specs=[[{"secondary_y": False}],
                   [{"secondary_y": False}]]
        )
        return fig
    
    def test_add_ema_indicator_basic(self, sample_figure, ema_data):
        """Test basic EMA indicator addition."""
        initial_traces = len(sample_figure.data)
        
        add_ema_indicator(sample_figure, ema_data)
        
        # Check that traces were added
        assert len(sample_figure.data) > initial_traces
        
        # Check that EMA line was added
        ema_traces = [trace for trace in sample_figure.data if trace.name == 'EMA']
        assert len(ema_traces) == 1
    
    def test_add_ema_indicator_missing_data(self, sample_figure):
        """Test EMA indicator with missing EMA data."""
        # Create data without EMA column
        dates = pd.date_range(start='2023-01-01', periods=10, freq='D')
        data = {
            'open': np.random.uniform(100, 200, 10),
            'high': np.random.uniform(200, 300, 10),
            'low': np.random.uniform(50, 100, 10),
            'close': np.random.uniform(100, 200, 10),
        }
        df = pd.DataFrame(data, index=dates)
        
        initial_traces = len(sample_figure.data)
        
        # Should not raise an error
        add_ema_indicator(sample_figure, df)
        
        # No traces should be added
        assert len(sample_figure.data) == initial_traces
    
    def test_ema_indicator_colors(self, sample_figure, ema_data):
        """Test that EMA indicator uses correct colors."""
        add_ema_indicator(sample_figure, ema_data)
        
        # Find EMA trace
        ema_trace = next((trace for trace in sample_figure.data if trace.name == 'EMA'), None)
        assert ema_trace is not None
        assert ema_trace.line.color == 'orange'
        assert ema_trace.line.width == 3
    
    def test_ema_indicator_data_values(self, sample_figure, ema_data):
        """Test that EMA indicator uses correct data values."""
        add_ema_indicator(sample_figure, ema_data)
        
        # Find EMA trace
        ema_trace = next((trace for trace in sample_figure.data if trace.name == 'EMA'), None)
        assert ema_trace is not None
        
        # Check that the trace uses the correct data
        assert len(ema_trace.x) == len(ema_data)
        assert len(ema_trace.y) == len(ema_data)
        
        # Check that y values match EMA data
        assert all(ema_trace.y == ema_data['ema'].values) 


class TestBollingerBandsIndicator:
    """Test Bollinger Bands indicator function."""
    
    @pytest.fixture
    def bb_data(self):
        """Create sample Bollinger Bands data for testing."""
        dates = pd.date_range(start='2023-01-01', periods=100, freq='D')
        np.random.seed(42)
        
        # Create sample OHLCV data
        data = {
            'open': np.random.uniform(100, 200, 100),
            'high': np.random.uniform(200, 300, 100),
            'low': np.random.uniform(50, 100, 100),
            'close': np.random.uniform(100, 200, 100),
            'volume': np.random.uniform(1000, 5000, 100),
        }
        
        # Create Bollinger Bands data
        base_price = 150
        data['bb_upper'] = base_price + np.random.uniform(5, 15, 100)
        data['bb_middle'] = base_price + np.random.uniform(-5, 5, 100)
        data['bb_lower'] = base_price - np.random.uniform(5, 15, 100)
        
        df = pd.DataFrame(data, index=dates)
        return df
    
    @pytest.fixture
    def sample_figure(self):
        """Create a sample figure for testing."""
        fig = make_subplots(
            rows=2, cols=1,
            subplot_titles=(None, None),
            vertical_spacing=0.04,
            row_heights=[0.62, 0.38],
            specs=[[{"secondary_y": False}],
                   [{"secondary_y": False}]]
        )
        return fig
    
    def test_add_bollinger_bands_indicator_basic(self, sample_figure, bb_data):
        """Test basic Bollinger Bands indicator addition."""
        initial_traces = len(sample_figure.data)
        
        add_bollinger_bands_indicator(sample_figure, bb_data)
        
        # Check that traces were added
        assert len(sample_figure.data) > initial_traces
        
        # Check that all three bands were added
        upper_traces = [trace for trace in sample_figure.data if trace.name == 'Upper Band']
        middle_traces = [trace for trace in sample_figure.data if trace.name == 'Middle Band']
        lower_traces = [trace for trace in sample_figure.data if trace.name == 'Lower Band']
        
        assert len(upper_traces) == 1
        assert len(middle_traces) == 1
        assert len(lower_traces) == 1
    
    def test_add_bollinger_bands_indicator_missing_data(self, sample_figure):
        """Test Bollinger Bands indicator with missing data."""
        # Create data without BB columns
        dates = pd.date_range(start='2023-01-01', periods=10, freq='D')
        data = {
            'open': np.random.uniform(100, 200, 10),
            'high': np.random.uniform(200, 300, 10),
            'low': np.random.uniform(50, 100, 10),
            'close': np.random.uniform(100, 200, 10),
        }
        df = pd.DataFrame(data, index=dates)
        
        initial_traces = len(sample_figure.data)
        
        # Should not raise an error
        add_bollinger_bands_indicator(sample_figure, df)
        
        # No traces should be added
        assert len(sample_figure.data) == initial_traces
    
    def test_add_bollinger_bands_indicator_partial_data(self, sample_figure, bb_data):
        """Test Bollinger Bands indicator with partial data."""
        # Remove some BB columns
        partial_data = bb_data.drop(columns=['bb_middle', 'bb_lower'])
        
        initial_traces = len(sample_figure.data)
        
        add_bollinger_bands_indicator(sample_figure, partial_data)
        
        # Should add upper band but not middle or lower
        assert len(sample_figure.data) > initial_traces
        
        # Check that upper band was added
        upper_traces = [trace for trace in sample_figure.data if trace.name == 'Upper Band']
        assert len(upper_traces) == 1
        
        # Check that middle and lower bands were NOT added
        middle_traces = [trace for trace in sample_figure.data if trace.name == 'Middle Band']
        lower_traces = [trace for trace in sample_figure.data if trace.name == 'Lower Band']
        assert len(middle_traces) == 0
        assert len(lower_traces) == 0
    
    def test_bollinger_bands_indicator_colors(self, sample_figure, bb_data):
        """Test that Bollinger Bands indicator uses correct colors."""
        add_bollinger_bands_indicator(sample_figure, bb_data)
        
        # Find upper band trace
        upper_trace = next((trace for trace in sample_figure.data if trace.name == 'Upper Band'), None)
        assert upper_trace is not None
        assert upper_trace.line.color == 'blue'
        assert upper_trace.line.width == 2
        
        # Find middle band trace
        middle_trace = next((trace for trace in sample_figure.data if trace.name == 'Middle Band'), None)
        assert middle_trace is not None
        assert middle_trace.line.color == 'gray'
        assert middle_trace.line.width == 2
        
        # Find lower band trace
        lower_trace = next((trace for trace in sample_figure.data if trace.name == 'Lower Band'), None)
        assert lower_trace is not None
        assert lower_trace.line.color == 'blue'
        assert lower_trace.line.width == 2
    
    def test_bollinger_bands_indicator_data_values(self, sample_figure, bb_data):
        """Test that Bollinger Bands indicator uses correct data values."""
        add_bollinger_bands_indicator(sample_figure, bb_data)
        
        # Find upper band trace
        upper_trace = next((trace for trace in sample_figure.data if trace.name == 'Upper Band'), None)
        assert upper_trace is not None
        assert all(upper_trace.y == bb_data['bb_upper'].values)
        
        # Find middle band trace
        middle_trace = next((trace for trace in sample_figure.data if trace.name == 'Middle Band'), None)
        assert middle_trace is not None
        assert all(middle_trace.y == bb_data['bb_middle'].values)
        
        # Find lower band trace
        lower_trace = next((trace for trace in sample_figure.data if trace.name == 'Lower Band'), None)
        assert lower_trace is not None
        assert all(lower_trace.y == bb_data['bb_lower'].values) 


class TestATRIndicator:
    """Test ATR indicator function."""
    
    @pytest.fixture
    def atr_data(self):
        """Create sample ATR data for testing."""
        dates = pd.date_range(start='2023-01-01', periods=100, freq='D')
        np.random.seed(42)
        
        # Create sample OHLCV data
        data = {
            'open': np.random.uniform(100, 200, 100),
            'high': np.random.uniform(200, 300, 100),
            'low': np.random.uniform(50, 100, 100),
            'close': np.random.uniform(100, 200, 100),
            'volume': np.random.uniform(1000, 5000, 100),
        }
        
        # Create ATR data
        data['atr'] = np.random.uniform(1, 10, 100)
        
        df = pd.DataFrame(data, index=dates)
        return df
    
    @pytest.fixture
    def sample_figure(self):
        """Create a sample figure for testing."""
        fig = make_subplots(
            rows=2, cols=1,
            subplot_titles=(None, None),
            vertical_spacing=0.04,
            row_heights=[0.62, 0.38],
            specs=[[{"secondary_y": False}],
                   [{"secondary_y": False}]]
        )
        return fig
    
    def test_add_atr_indicator_basic(self, sample_figure, atr_data):
        """Test basic ATR indicator addition."""
        initial_traces = len(sample_figure.data)
        
        add_atr_indicator(sample_figure, atr_data)
        
        # Check that traces were added
        assert len(sample_figure.data) > initial_traces
        
        # Check that ATR line was added
        atr_traces = [trace for trace in sample_figure.data if trace.name == 'ATR']
        assert len(atr_traces) == 1
    
    def test_add_atr_indicator_missing_data(self, sample_figure):
        """Test ATR indicator with missing ATR data."""
        # Create data without ATR column
        dates = pd.date_range(start='2023-01-01', periods=10, freq='D')
        data = {
            'open': np.random.uniform(100, 200, 10),
            'high': np.random.uniform(200, 300, 10),
            'low': np.random.uniform(50, 100, 10),
            'close': np.random.uniform(100, 200, 10),
        }
        df = pd.DataFrame(data, index=dates)
        
        initial_traces = len(sample_figure.data)
        
        # Should not raise an error
        add_atr_indicator(sample_figure, df)
        
        # No traces should be added
        assert len(sample_figure.data) == initial_traces
    
    def test_atr_indicator_colors(self, sample_figure, atr_data):
        """Test that ATR indicator uses correct colors."""
        add_atr_indicator(sample_figure, atr_data)
        
        # Find ATR trace
        atr_trace = next((trace for trace in sample_figure.data if trace.name == 'ATR'), None)
        assert atr_trace is not None
        assert atr_trace.line.color == 'brown'
        assert atr_trace.line.width == 3
    
    def test_atr_indicator_data_values(self, sample_figure, atr_data):
        """Test that ATR indicator uses correct data values."""
        add_atr_indicator(sample_figure, atr_data)
        
        # Find ATR trace
        atr_trace = next((trace for trace in sample_figure.data if trace.name == 'ATR'), None)
        assert atr_trace is not None
        
        # Check that the trace uses the correct data
        assert len(atr_trace.x) == len(atr_data)
        assert len(atr_trace.y) == len(atr_data)
        
        # Check that y values match ATR data
        assert all(atr_trace.y == atr_data['atr'].values) 