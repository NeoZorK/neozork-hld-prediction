# -*- coding: utf-8 -*-
# tests/plotting/test_mplfinance_supertrend.py
import pytest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

from src.plotting.mplfinance_plot import plot_indicator_results_mplfinance
from src.common.constants import TradingRule


class TestMplfinanceSupertrend:
    """Test enhanced SuperTrend plotting in mplfinance mode."""
    
    @pytest.fixture
    def sample_data(self):
        """Create sample OHLCV data with SuperTrend indicators."""
        dates = pd.date_range('2023-01-01', periods=100, freq='D')
        
        # Create realistic price data
        np.random.seed(42)
        base_price = 1.5000
        price_changes = np.random.normal(0, 0.01, 100)
        prices = [base_price]
        
        for change in price_changes[1:]:
            new_price = prices[-1] * (1 + change)
            prices.append(new_price)
        
        # Create OHLCV data
        data = {
            'Open': prices,
            'High': [p * (1 + abs(np.random.normal(0, 0.005))) for p in prices],
            'Low': [p * (1 - abs(np.random.normal(0, 0.005))) for p in prices],
            'Close': prices,
            'Volume': np.random.randint(1000, 10000, 100)
        }
        
        df = pd.DataFrame(data, index=dates)
        
        # Add SuperTrend data (PPrice1, PPrice2, Direction)
        # Simulate SuperTrend values that change based on trend
        supertrend_values = []
        direction_values = []
        
        for i in range(len(df)):
            if i < 10:  # First 10 points - no trend
                supertrend_values.append(np.nan)
                direction_values.append(0)
            else:
                # Simple SuperTrend simulation
                if i % 20 < 10:  # Uptrend
                    supertrend_values.append(df['Close'].iloc[i] * 0.995)
                    direction_values.append(1)
                else:  # Downtrend
                    supertrend_values.append(df['Close'].iloc[i] * 1.005)
                    direction_values.append(2)
        
        df['PPrice1'] = supertrend_values
        df['PPrice2'] = supertrend_values
        df['Direction'] = direction_values
        df['PColor1'] = 1
        df['PColor2'] = 2
        df['Diff'] = df['Close'] - df['PPrice1']
        
        return df
    
    def test_supertrend_enhanced_plotting(self, sample_data):
        """Test that enhanced SuperTrend plotting works correctly."""
        # This test verifies that the plotting function doesn't raise errors
        # and handles the enhanced SuperTrend logic properly
        
        try:
            # Call the plotting function
            plot_indicator_results_mplfinance(
                df_results=sample_data,
                rule=TradingRule.SuperTrend,
                title="Test SuperTrend Enhanced Plotting"
            )
            # If no exception is raised, the test passes
            assert True
        except Exception as e:
            pytest.fail(f"Enhanced SuperTrend plotting failed: {e}")
    
    def test_supertrend_trend_detection(self, sample_data):
        """Test that trend detection logic works correctly."""
        # Extract the trend detection logic from the plotting function
        has_pprice = 'PPrice1' in sample_data.columns and 'PPrice2' in sample_data.columns
        has_direction = 'Direction' in sample_data.columns
        
        assert has_pprice, "PPrice1 and PPrice2 columns should be present"
        assert has_direction, "Direction column should be present"
        
        # Test trend calculation logic
        p1 = sample_data['PPrice1']
        p2 = sample_data['PPrice2']
        direction = sample_data['Direction']
        
        # Handle NaN values properly
        valid_mask = ~(pd.isna(p1) | pd.isna(p2))
        supertrend_values = np.full(len(direction), np.nan)
        supertrend_values[valid_mask] = np.where(direction[valid_mask] > 0, p1[valid_mask], p2[valid_mask])
        
        # Determine trend direction
        price_series = sample_data['Close']
        trend = np.where(price_series > supertrend_values, 1, -1)
        trend = pd.Series(trend, index=sample_data.index)
        
        # Verify trend calculation
        assert len(trend) == len(sample_data), "Trend series should have same length as data"
        assert all(trend.isin([1, -1])), "Trend values should be 1 or -1"
    
    def test_supertrend_signal_detection(self, sample_data):
        """Test that signal change detection works correctly."""
        # Test signal change detection logic
        p1 = sample_data['PPrice1']
        p2 = sample_data['PPrice2']
        direction = sample_data['Direction']
        
        valid_mask = ~(pd.isna(p1) | pd.isna(p2))
        supertrend_values = np.full(len(direction), np.nan)
        supertrend_values[valid_mask] = np.where(direction[valid_mask] > 0, p1[valid_mask], p2[valid_mask])
        
        price_series = sample_data['Close']
        trend = np.where(price_series > supertrend_values, 1, -1)
        trend = pd.Series(trend, index=sample_data.index)
        
        # Detect signal change points
        buy_signals = (trend == 1) & (trend.shift(1) == -1)
        sell_signals = (trend == -1) & (trend.shift(1) == 1)
        signal_changes = buy_signals | sell_signals
        
        # Verify signal detection
        assert len(buy_signals) == len(sample_data), "Buy signals should have same length as data"
        assert len(sell_signals) == len(sample_data), "Sell signals should have same length as data"
        assert len(signal_changes) == len(sample_data), "Signal changes should have same length as data"
    
    def test_supertrend_segmentation(self, sample_data):
        """Test that SuperTrend segmentation works correctly."""
        # Test segmentation logic
        p1 = sample_data['PPrice1']
        p2 = sample_data['PPrice2']
        direction = sample_data['Direction']
        
        valid_mask = ~(pd.isna(p1) | pd.isna(p2))
        supertrend_values = np.full(len(direction), np.nan)
        supertrend_values[valid_mask] = np.where(direction[valid_mask] > 0, p1[valid_mask], p2[valid_mask])
        
        price_series = sample_data['Close']
        trend = np.where(price_series > supertrend_values, 1, -1)
        trend = pd.Series(trend, index=sample_data.index)
        
        # Colors like in fastest mode
        uptrend_color = '#00C851'  # Green
        downtrend_color = '#FF4444'  # Red
        signal_change_color = '#FFC107'  # Golden
        
        # Detect signal change points
        buy_signals = (trend == 1) & (trend.shift(1) == -1)
        sell_signals = (trend == -1) & (trend.shift(1) == 1)
        signal_changes = buy_signals | sell_signals
        
        # Create color array with signal change highlighting
        color_arr = np.where(trend == 1, uptrend_color, downtrend_color)
        
        # Enhanced segmentation with signal change detection
        segments = []
        last_color = color_arr[0]
        seg_x, seg_y = [sample_data.index[0]], [supertrend_values[0]]
        
        for i in range(1, len(sample_data.index)):
            current_color = color_arr[i]
            
            # Check if this is a signal change point
            if signal_changes.iloc[i]:
                # Add previous segment
                if len(seg_x) > 1:
                    segments.append((seg_x.copy(), seg_y.copy(), last_color))
                
                # Add signal change point with golden color
                segments.append(([sample_data.index[i-1], sample_data.index[i]], 
                              [supertrend_values[i-1], supertrend_values[i]], 
                              signal_change_color))
                
                # Start new segment
                seg_x, seg_y = [sample_data.index[i]], [supertrend_values[i]]
                last_color = current_color
            elif current_color != last_color:
                # Regular trend change (not a signal)
                segments.append((seg_x.copy(), seg_y.copy(), last_color))
                seg_x, seg_y = [sample_data.index[i-1]], [supertrend_values[i-1]]
                last_color = current_color
            
            seg_x.append(sample_data.index[i])
            seg_y.append(supertrend_values[i])
        
        # Add final segment
        if len(seg_x) > 0:
            segments.append((seg_x, seg_y, last_color))
        
        # Verify segmentation
        assert len(segments) > 0, "Should have at least one segment"
        for seg_x, seg_y, seg_color in segments:
            assert len(seg_x) > 0, "Segment should have x coordinates"
            assert len(seg_y) > 0, "Segment should have y coordinates"
            assert seg_color in [uptrend_color, downtrend_color, signal_change_color], "Invalid color"
    
    def test_supertrend_fallback_columns(self):
        """Test that SuperTrend works with different column names."""
        # Create data with different SuperTrend column names
        dates = pd.date_range('2023-01-01', periods=50, freq='D')
        
        # Test with 'supertrend' column
        data_supertrend = pd.DataFrame({
            'Open': np.random.uniform(1.4, 1.6, 50),
            'High': np.random.uniform(1.5, 1.7, 50),
            'Low': np.random.uniform(1.3, 1.5, 50),
            'Close': np.random.uniform(1.4, 1.6, 50),
            'Volume': np.random.randint(1000, 10000, 50),
            'supertrend': np.random.uniform(1.3, 1.7, 50),
            'Direction': np.random.choice([0, 1, 2], 50)
        }, index=dates)
        
        # Test with 'SuperTrend' column
        data_SuperTrend = pd.DataFrame({
            'Open': np.random.uniform(1.4, 1.6, 50),
            'High': np.random.uniform(1.5, 1.7, 50),
            'Low': np.random.uniform(1.3, 1.5, 50),
            'Close': np.random.uniform(1.4, 1.6, 50),
            'Volume': np.random.randint(1000, 10000, 50),
            'SuperTrend': np.random.uniform(1.3, 1.7, 50),
            'Direction': np.random.choice([0, 1, 2], 50)
        }, index=dates)
        
        # Both should work without errors
        try:
            plot_indicator_results_mplfinance(
                df_results=data_supertrend,
                rule=TradingRule.SuperTrend,
                title="Test SuperTrend Column"
            )
            assert True
        except Exception as e:
            pytest.fail(f"Failed with 'supertrend' column: {e}")
        
        try:
            plot_indicator_results_mplfinance(
                df_results=data_SuperTrend,
                rule=TradingRule.SuperTrend,
                title="Test SuperTrend Column"
            )
            assert True
        except Exception as e:
            pytest.fail(f"Failed with 'SuperTrend' column: {e}")
    
    def test_supertrend_no_data_handling(self):
        """Test that SuperTrend handles missing data gracefully."""
        # Create data without SuperTrend columns
        dates = pd.date_range('2023-01-01', periods=50, freq='D')
        data_no_supertrend = pd.DataFrame({
            'Open': np.random.uniform(1.4, 1.6, 50),
            'High': np.random.uniform(1.5, 1.7, 50),
            'Low': np.random.uniform(1.3, 1.5, 50),
            'Close': np.random.uniform(1.4, 1.6, 50),
            'Volume': np.random.randint(1000, 10000, 50)
        }, index=dates)
        
        # Should not raise an error, just skip SuperTrend plotting
        try:
            plot_indicator_results_mplfinance(
                df_results=data_no_supertrend,
                rule=TradingRule.SuperTrend,
                title="Test No SuperTrend Data"
            )
            assert True
        except Exception as e:
            pytest.fail(f"Failed with no SuperTrend data: {e}")


if __name__ == "__main__":
    pytest.main([__file__]) 