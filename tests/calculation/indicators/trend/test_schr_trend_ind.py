# -*- coding: utf-8 -*-
# tests/calculation/indicators/trend/test_schr_trend_ind.py

"""
Tests for SCHR_Trend indicator implementation.
"""

import pytest
import pandas as pd
import numpy as np
from src.calculation.indicators.trend.schr_trend_ind import (
    SCHRTrendIndicator, TradingRuleMode, calculate_schr_trend,
    calculate_rsi, apply_rule_schr_trend
)
from src.calculation.indicators.oscillators.rsi_ind_calc import PriceType
from src.common.constants import NOTRADE, BUY, SELL, DBL_BUY, DBL_SELL


class TestSCHRTrendIndicator:
    """Test class for SCHR_Trend indicator."""
    
    def setup_method(self):
        """Set up test data."""
        # Create sample OHLCV data
        dates = pd.date_range('2024-01-01', periods=100, freq='D')
        np.random.seed(42)  # For reproducible tests
        
        # Generate realistic price data
        base_price = 100.0
        returns = np.random.normal(0, 0.02, 100)  # 2% daily volatility
        prices = [base_price]
        
        for ret in returns[1:]:
            prices.append(prices[-1] * (1 + ret))
        
        self.df = pd.DataFrame({
            'Open': prices,
            'High': [p * (1 + abs(np.random.normal(0, 0.01))) for p in prices],
            'Low': [p * (1 - abs(np.random.normal(0, 0.01))) for p in prices],
            'Close': [p * (1 + np.random.normal(0, 0.005)) for p in prices],
            'Volume': np.random.randint(1000, 10000, 100)
        }, index=dates)
        
        # Ensure High >= Low
        self.df['High'] = np.maximum(self.df['High'], self.df['Low'])
        self.df['High'] = np.maximum(self.df['High'], self.df['Open'])
        self.df['High'] = np.maximum(self.df['High'], self.df['Close'])
        self.df['Low'] = np.minimum(self.df['Low'], self.df['Open'])
        self.df['Low'] = np.minimum(self.df['Low'], self.df['Close'])
    
    def test_indicator_initialization(self):
        """Test indicator initialization with default parameters."""
        indicator = SCHRTrendIndicator()
        
        assert indicator.period == 2
        assert indicator.tr_mode == TradingRuleMode.TR_Zone
        assert indicator.extreme_up == 95
        assert indicator.extreme_down == 5
        assert indicator.price_type.value == PriceType.OPEN.value
    
    def test_indicator_initialization_custom(self):
        """Test indicator initialization with custom parameters."""
        indicator = SCHRTrendIndicator(
            period=5,
            tr_mode='firstclassic',
            extreme_up=90,
            extreme_down=10,
            price_type=PriceType.CLOSE
        )
        
        assert indicator.period == 5
        assert indicator.tr_mode == TradingRuleMode.TR_FirstClassic
        assert indicator.extreme_up == 90
        assert indicator.extreme_down == 10
        assert indicator.price_type == PriceType.CLOSE
    
    def test_tr_mode_parsing(self):
        """Test trading rule mode parsing from strings."""
        indicator = SCHRTrendIndicator()
        
        # Test valid modes
        assert indicator._parse_tr_mode('firstclassic') == TradingRuleMode.TR_FirstClassic
        assert indicator._parse_tr_mode('firsttrend') == TradingRuleMode.TR_FirstTrend
        assert indicator._parse_tr_mode('trend') == TradingRuleMode.TR_Trend
        assert indicator._parse_tr_mode('zone') == TradingRuleMode.TR_Zone
        assert indicator._parse_tr_mode('firstzone') == TradingRuleMode.TR_FirstZone
        assert indicator._parse_tr_mode('firststrongzone') == TradingRuleMode.TR_FirstStrongZone
        assert indicator._parse_tr_mode('purchasepower') == TradingRuleMode.TR_PurchasePower
        assert indicator._parse_tr_mode('purchasepower_bycount') == TradingRuleMode.TR_PurchasePower_byCount
        assert indicator._parse_tr_mode('purchasepower_extreme') == TradingRuleMode.TR_PurchasePower_Extreme
        assert indicator._parse_tr_mode('purchasepower_weak') == TradingRuleMode.TR_PurchasePower_Weak
        
        # Test invalid mode (should default to zone)
        assert indicator._parse_tr_mode('invalid') == TradingRuleMode.TR_Zone
        
        # Test integer mode
        assert indicator._parse_tr_mode(0) == TradingRuleMode.TR_FirstClassic
        assert indicator._parse_tr_mode(3) == TradingRuleMode.TR_Zone
    
    def test_rsi_calculation(self):
        """Test RSI calculation function."""
        rsi_values = calculate_rsi(self.df, period=14, price_type=PriceType.OPEN)
        
        assert len(rsi_values) == len(self.df)
        assert not rsi_values.isna().all()  # Should have some valid values
        assert all(0 <= val <= 100 for val in rsi_values.dropna())  # RSI should be 0-100
        
        # Test with different period
        rsi_values_5 = calculate_rsi(self.df, period=5, price_type=PriceType.CLOSE)
        assert len(rsi_values_5) == len(self.df)
        assert not rsi_values_5.isna().all()
    
    def test_rsi_calculation_insufficient_data(self):
        """Test RSI calculation with insufficient data."""
        small_df = self.df.head(5)  # Less than period + 1
        rsi_values = calculate_rsi(small_df, period=10, price_type=PriceType.OPEN)
        
        assert len(rsi_values) == len(small_df)
        assert rsi_values.isna().all()  # Should all be NaN
    
    def test_schr_trend_calculation_basic(self):
        """Test basic SCHR trend calculation."""
        origin, trend, direction, signal, color, purchase_power = calculate_schr_trend(
            self.df, period=2, tr_mode=TradingRuleMode.TR_Zone,
            extreme_up=95, extreme_down=5, price_type=PriceType.OPEN
        )
        
        assert len(origin) == len(self.df)
        assert len(trend) == len(self.df)
        assert len(color) == len(self.df)
        assert len(direction) == len(self.df)
        assert len(signal) == len(self.df)
        assert len(purchase_power) == len(self.df)
        
        # Check that first bar has no signal
        assert signal.iloc[0] == NOTRADE
        
        # Check that trend line equals open prices
        assert all(abs(trend.iloc[i] - self.df['Open'].iloc[i]) < 1e-10 for i in range(len(self.df)))
    
    def test_schr_trend_calculation_insufficient_data(self):
        """Test SCHR trend calculation with insufficient data."""
        small_df = self.df.head(1)  # Less than period + 1
        origin, trend, color, direction, signal, purchase_power = calculate_schr_trend(
            small_df, period=2, tr_mode=TradingRuleMode.TR_Zone,
            extreme_up=95, extreme_down=5, price_type=PriceType.OPEN
        )
        
        assert len(origin) == len(small_df)
        assert len(trend) == len(small_df)
        assert len(color) == len(small_df)
        assert len(direction) == len(small_df)
        assert len(signal) == len(small_df)
        assert len(purchase_power) == len(small_df)
        assert all(pd.isna(val) for val in origin)
        assert all(pd.isna(val) for val in trend)
        assert all(pd.isna(val) for val in color)
        assert all(pd.isna(val) for val in direction)
        assert all(pd.isna(val) for val in signal)
        assert all(pd.isna(val) for val in purchase_power)
    
    def test_trading_rule_modes(self):
        """Test different trading rule modes."""
        # Test Zone mode (default)
        _, _, direction_zone, signal_zone, color_zone, _ = calculate_schr_trend(
            self.df, period=2, tr_mode=TradingRuleMode.TR_Zone,
            extreme_up=95, extreme_down=5, price_type=PriceType.OPEN
        )
        
        # Test First Classic mode
        _, _, direction_fc, signal_fc, color_fc, _ = calculate_schr_trend(
            self.df, period=2, tr_mode=TradingRuleMode.TR_FirstClassic,
            extreme_up=95, extreme_down=5, price_type=PriceType.OPEN
        )
        
        # Test First Trend mode
        _, _, direction_ft, signal_ft, color_ft, _ = calculate_schr_trend(
            self.df, period=2, tr_mode=TradingRuleMode.TR_FirstTrend,
            extreme_up=95, extreme_down=5, price_type=PriceType.OPEN
        )
        
        # All should have same length
        assert len(color_zone) == len(color_fc) == len(color_ft)
        assert len(direction_zone) == len(direction_fc) == len(direction_ft)
        assert len(signal_zone) == len(signal_fc) == len(signal_ft)
    
    def test_purchase_power_modes(self):
        """Test purchase power trading rule modes."""
        # Test Purchase Power mode
        _, _, direction_pp, signal_pp, color_pp, _ = calculate_schr_trend(
            self.df, period=2, tr_mode=TradingRuleMode.TR_PurchasePower,
            extreme_up=95, extreme_down=5, price_type=PriceType.OPEN
        )
        
        # Test Purchase Power by Count mode
        _, _, direction_ppc, signal_ppc, color_ppc, _ = calculate_schr_trend(
            self.df, period=2, tr_mode=TradingRuleMode.TR_PurchasePower_byCount,
            extreme_up=95, extreme_down=5, price_type=PriceType.OPEN
        )
        
        # Test Purchase Power Extreme mode
        _, _, direction_ppe, signal_ppe, color_ppe, _ = calculate_schr_trend(
            self.df, period=2, tr_mode=TradingRuleMode.TR_PurchasePower_Extreme,
            extreme_up=95, extreme_down=5, price_type=PriceType.OPEN
        )
        
        # Test Purchase Power Weak mode
        _, _, direction_ppw, signal_ppw, color_ppw, _ = calculate_schr_trend(
            self.df, period=2, tr_mode=TradingRuleMode.TR_PurchasePower_Weak,
            extreme_up=95, extreme_down=5, price_type=PriceType.OPEN
        )
        
        # All should have same length
        assert len(color_pp) == len(color_ppc) == len(color_ppe) == len(color_ppw)
        assert len(direction_pp) == len(direction_ppc) == len(direction_ppe) == len(direction_ppw)
        assert len(signal_pp) == len(signal_ppc) == len(signal_ppe) == len(signal_ppw)
    
    def test_indicator_calculate_method(self):
        """Test indicator calculate method."""
        indicator = SCHRTrendIndicator(
            period=3,
            tr_mode='zone',
            extreme_up=90,
            extreme_down=10
        )
        
        result = indicator.calculate(self.df)
        
        assert 'schr_trend' in result.columns
        assert 'schr_trend_color' in result.columns
        assert 'schr_trend_direction' in result.columns
        assert 'schr_trend_signal' in result.columns
        
        # Check that original data is preserved
        assert all(col in result.columns for col in self.df.columns)
    
    def test_indicator_apply_rule_method(self):
        """Test indicator apply_rule method."""
        indicator = SCHRTrendIndicator(
            period=2,
            tr_mode='firstclassic',
            extreme_up=95,
            extreme_down=5
        )
        
        result = indicator.apply_rule(self.df, point=0.0001)
        
        # Check output columns for rule system compatibility
        assert 'PPrice1' in result.columns
        assert 'PColor1' in result.columns
        assert 'PPrice2' in result.columns
        assert 'PColor2' in result.columns
        assert 'Direction' in result.columns
        assert 'Diff' in result.columns
        
        # Check that PPrice1 equals Open prices
        assert all(abs(result['PPrice1'].iloc[i] - self.df['Open'].iloc[i]) < 1e-10 for i in range(len(self.df)))
    
    def test_apply_rule_schr_trend_function(self):
        """Test apply_rule_schr_trend function."""
        result = apply_rule_schr_trend(
            self.df, point=0.0001,
            period=4,
            tr_mode='trend',
            extreme_up=85,
            extreme_down=15,
            price_type='open'
        )
        
        # Check output columns
        assert 'PPrice1' in result.columns
        assert 'PColor1' in result.columns
        assert 'PPrice2' in result.columns
        assert 'PColor2' in result.columns
        assert 'Direction' in result.columns
        assert 'Diff' in result.columns
        
        # Check that PPrice1 equals Open prices
        assert all(abs(result['PPrice1'].iloc[i] - self.df['Open'].iloc[i]) < 1e-10 for i in range(len(self.df)))
    
    def test_signal_values_range(self):
        """Test that signal values are within expected range."""
        _, _, _, signal, _, _ = calculate_schr_trend(
            self.df, period=2, tr_mode=TradingRuleMode.TR_Zone,
            extreme_up=95, extreme_down=5, price_type=PriceType.OPEN
        )
        
        # Signal values should be within expected range
        valid_signals = [NOTRADE, BUY, SELL, DBL_BUY, DBL_SELL]
        assert all(signal.iloc[i] in valid_signals for i in range(len(signal)))
    
    def test_direction_values_range(self):
        """Test that direction values are within expected range."""
        _, _, direction, _, _, _ = calculate_schr_trend(
            self.df, period=2, tr_mode=TradingRuleMode.TR_Zone,
            extreme_up=95, extreme_down=5, price_type=PriceType.OPEN
        )
        
        # Direction values should be within expected range
        valid_directions = [NOTRADE, BUY, SELL, DBL_BUY, DBL_SELL]
        assert all(direction.iloc[i] in valid_directions for i in range(len(direction)))
    
    def test_color_values_range(self):
        """Test that color values are within expected range."""
        _, _, _, _, color, _ = calculate_schr_trend(
            self.df, period=2, tr_mode=TradingRuleMode.TR_Zone,
            extreme_up=95, extreme_down=5, price_type=PriceType.OPEN
        )
        
        # Color values should be within expected range
        valid_colors = [NOTRADE, BUY, SELL, DBL_BUY, DBL_SELL]
        assert all(color.iloc[i] in valid_colors for i in range(len(color)))
    
    def test_extreme_points_effect(self):
        """Test that extreme points affect signal generation."""
        # Test with high extreme points
        _, _, _, signal_high, _, _ = calculate_schr_trend(
            self.df, period=2, tr_mode=TradingRuleMode.TR_Zone,
            extreme_up=99, extreme_down=1, price_type=PriceType.OPEN
        )
        
        # Test with low extreme points
        _, _, _, signal_low, _, _ = calculate_schr_trend(
            self.df, period=2, tr_mode=TradingRuleMode.TR_Zone,
            extreme_up=80, extreme_down=20, price_type=PriceType.OPEN
        )
        
        # Both should generate some signals
        high_signals = sum(1 for s in signal_high if s != NOTRADE)
        low_signals = sum(1 for s in signal_low if s != NOTRADE)
        
        # Both extreme point settings should generate signals
        assert high_signals > 0
        assert low_signals > 0
        
        # Check that signals are valid
        valid_signals = [NOTRADE, BUY, SELL, DBL_BUY, DBL_SELL]
        assert all(signal_high.iloc[i] in valid_signals for i in range(len(signal_high)))
        assert all(signal_low.iloc[i] in valid_signals for i in range(len(signal_low)))
    
    def test_period_effect(self):
        """Test that period affects calculation."""
        # Test with short period
        _, _, _, signal_short, _, _ = calculate_schr_trend(
            self.df, period=1, tr_mode=TradingRuleMode.TR_Zone,
            extreme_up=95, extreme_down=5, price_type=PriceType.OPEN
        )
        
        # Test with long period
        _, _, _, signal_long, _, _ = calculate_schr_trend(
            self.df, period=5, tr_mode=TradingRuleMode.TR_Zone,
            extreme_up=95, extreme_down=5, price_type=PriceType.OPEN
        )
        
        # Shorter period should generate more signals (more sensitive)
        short_signals = sum(1 for s in signal_short if s != NOTRADE)
        long_signals = sum(1 for s in signal_long if s != NOTRADE)
        
        assert short_signals >= long_signals
    
    def test_price_type_effect(self):
        """Test that price type affects calculation."""
        # Test with Open prices
        _, _, _, signal_open, _, _ = calculate_schr_trend(
            self.df, period=2, tr_mode=TradingRuleMode.TR_Zone,
            extreme_up=95, extreme_down=5, price_type=PriceType.OPEN
        )
        
        # Test with Close prices
        _, _, _, signal_close, _, _ = calculate_schr_trend(
            self.df, period=2, tr_mode=TradingRuleMode.TR_Zone,
            extreme_up=95, extreme_down=5, price_type=PriceType.CLOSE
        )
        
        # Open and Close should generate different signals
        open_signals = sum(1 for s in signal_open if s != NOTRADE)
        close_signals = sum(1 for s in signal_close if s != NOTRADE)
        
        # Both should generate some signals
        assert open_signals > 0
        assert close_signals > 0


if __name__ == '__main__':
    pytest.main([__file__])
