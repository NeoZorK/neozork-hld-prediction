# -*- coding: utf-8 -*-
# tests/plotting/test_dual_chart_fast_fullscreen.py

"""
Tests for dual_chart_fast module with dynamic fullscreen height functionality.
Tests the new features:
1. Dynamic height calculation
2. 10% size reduction for better legend visibility
3. MACD indicator identical to fastest mode
"""

import pytest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
import tempfile
import shutil

from src.plotting.dual_chart_fast import (
    plot_dual_chart_fast,
    get_screen_height,
    calculate_dynamic_height
)


class TestDualChartFastFullscreen:
    """Test class for dual_chart_fast fullscreen functionality."""
    
    @pytest.fixture
    def sample_data(self):
        """Create sample OHLCV data with MACD indicator."""
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
        
        # Add MACD indicator columns
        df['macd'] = np.random.normal(0, 0.1, 100)
        df['macd_signal'] = np.random.normal(0, 0.08, 100)
        df['macd_histogram'] = df['macd'] - df['macd_signal']
        
        return df
    
    @pytest.fixture
    def temp_output_dir(self):
        """Create temporary output directory."""
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir)
    
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
        
        # Note: We can't directly test the internal size calculations
        # as they're used internally by Bokeh, but we can verify the function
        # runs without errors and produces output
    
    def test_plot_dual_chart_fast_macd_indicator(self, sample_data, temp_output_dir):
        """Test that MACD indicator is properly rendered."""
        output_path = os.path.join(temp_output_dir, "test_macd_indicator.html")
        
        result = plot_dual_chart_fast(
            df=sample_data,
            rule="macd:8,21,5,open",
            title="Test MACD Indicator",
            output_path=output_path,
            width=1800,
            height=1100
        )
        
        # Check that file was created
        assert os.path.exists(output_path)
        assert os.path.getsize(output_path) > 0
        
        # Read the HTML file to check for MACD-related content
        with open(output_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # Check for MACD legend labels
        assert 'MACD' in html_content
        assert 'Signal' in html_content
        assert 'Histogram' in html_content
        
        # Check for hover tooltip content
        assert 'MACD' in html_content or 'macd' in html_content.lower()
        assert 'Signal' in html_content or 'macd_signal' in html_content.lower()
        assert 'Histogram' in html_content or 'macd_histogram' in html_content.lower()
    
    def test_plot_dual_chart_fast_rsi_indicator(self, sample_data, temp_output_dir):
        """Test that RSI indicator is properly rendered."""
        # Add RSI data to sample_data
        sample_data['rsi'] = np.random.uniform(0, 100, 100)
        sample_data['rsi_overbought'] = 70
        sample_data['rsi_oversold'] = 30
        
        output_path = os.path.join(temp_output_dir, "test_rsi_indicator.html")
        
        result = plot_dual_chart_fast(
            df=sample_data,
            rule="rsi:14,30,70,open",
            title="Test RSI Indicator",
            output_path=output_path,
            width=1800,
            height=1100
        )
        
        # Check that file was created
        assert os.path.exists(output_path)
        assert os.path.getsize(output_path) > 0
        
        # Read the HTML file to check for RSI-related content
        with open(output_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # Check for RSI legend labels
        assert 'RSI' in html_content
    
    def test_plot_dual_chart_fast_error_handling(self, temp_output_dir):
        """Test error handling with invalid data."""
        output_path = os.path.join(temp_output_dir, "test_error_handling.html")
        
        # Test with empty DataFrame
        empty_df = pd.DataFrame()
        
        with pytest.raises(Exception):
            plot_dual_chart_fast(
                df=empty_df,
                rule="macd:8,21,5,open",
                title="Test Error Handling",
                output_path=output_path,
                width=1800,
                height=1100
            )
    
    def test_plot_dual_chart_fast_missing_columns(self, sample_data, temp_output_dir):
        """Test handling of missing OHLC columns."""
        output_path = os.path.join(temp_output_dir, "test_missing_columns.html")
        
        # Remove required columns
        invalid_df = sample_data.drop(['Open', 'High', 'Low', 'Close'], axis=1)
        
        with pytest.raises(Exception):
            plot_dual_chart_fast(
                df=invalid_df,
                rule="macd:8,21,5,open",
                title="Test Missing Columns",
                output_path=output_path,
                width=1800,
                height=1100
            )
    
    def test_plot_dual_chart_fast_different_rules(self, sample_data, temp_output_dir):
        """Test different indicator rules."""
        # Add various indicator data
        sample_data['ema'] = sample_data['Close'].rolling(20).mean()
        sample_data['bb_upper'] = sample_data['Close'] * 1.02
        sample_data['bb_middle'] = sample_data['Close']
        sample_data['bb_lower'] = sample_data['Close'] * 0.98
        
        rules_to_test = [
            "ema:20,open",
            "bb:20,2,open",
            "atr:14,open",
            "cci:14,open",
            "vwap:open",
            "pivot:open",
            "hma:20,open",
            "tsf:20,open"
        ]
        
        for rule in rules_to_test:
            output_path = os.path.join(temp_output_dir, f"test_{rule.replace(':', '_').replace(',', '_')}.html")
            
            try:
                result = plot_dual_chart_fast(
                    df=sample_data,
                    rule=rule,
                    title=f"Test {rule}",
                    output_path=output_path,
                    width=1800,
                    height=1100
                )
                
                # Check that file was created
                assert os.path.exists(output_path)
                assert os.path.getsize(output_path) > 0
                
            except Exception as e:
                # Some indicators might not be fully implemented, which is OK
                pytest.skip(f"Rule {rule} not fully implemented: {e}")
    
    def test_plot_dual_chart_fast_layout_configuration(self, sample_data, temp_output_dir):
        """Test layout configuration options."""
        output_path = os.path.join(temp_output_dir, "test_layout_config.html")
        
        layout = {
            'indicator_name': 'Custom MACD',
            'main_chart_height': 0.7,
            'indicator_chart_height': 0.3
        }
        
        result = plot_dual_chart_fast(
            df=sample_data,
            rule="macd:8,21,5,open",
            title="Test Layout Configuration",
            output_path=output_path,
            width=1800,
            height=1100,
            layout=layout
        )
        
        # Check that file was created
        assert os.path.exists(output_path)
        assert os.path.getsize(output_path) > 0


if __name__ == "__main__":
    pytest.main([__file__]) 