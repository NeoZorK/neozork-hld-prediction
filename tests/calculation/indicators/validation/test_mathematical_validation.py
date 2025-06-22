# tests/calculation/indicators/validation/test_mathematical_validation.py

import pytest
import pandas as pd
import numpy as np
from src.calculation.indicators.volatility.atr_ind import apply_rule_atr
from src.calculation.indicators.volatility.bb_ind import apply_rule_bollinger_bands
from src.calculation.indicators.volume.obv_ind import apply_rule_obv
from src.calculation.indicators.volume.vwap_ind import apply_rule_vwap
from src.calculation.indicators.oscillators.rsi_ind import apply_rule_rsi
from src.calculation.indicators.oscillators.stoch_ind import apply_rule_stochastic
from src.calculation.indicators.trend.ema_ind import apply_rule_ema
from src.calculation.indicators.trend.adx_ind import apply_rule_adx
from src.calculation.indicators.oscillators.rsi_ind import PriceType as RSIPriceType
from src.calculation.indicators.oscillators.stoch_ind import PriceType as StochPriceType
from src.calculation.indicators.trend.ema_ind import PriceType as EMAPriceType
from src.calculation.indicators.trend.adx_ind import PriceType as ADXPriceType
from src.calculation.indicators.volatility.atr_ind import PriceType as ATRPriceType
from src.calculation.indicators.volume.vwap_ind import PriceType as VWAPPriceType
from src.calculation.indicators.volume.obv_ind import PriceType as OBVPriceType

class TestMathematicalValidation:
    """Mathematical validation tests for indicators."""
    
    def setup_method(self):
        self.atr = apply_rule_atr
        self.bb = apply_rule_bollinger_bands
        self.obv = apply_rule_obv
        self.vwap = apply_rule_vwap
        self.rsi = apply_rule_rsi
        self.stoch = apply_rule_stochastic
        self.ema = apply_rule_ema
        self.adx = apply_rule_adx
        self.point = 0.0001  # фиктивный point для тестов

    def test_rsi_mathematical_properties(self):
        """Test RSI mathematical properties."""
        # Create data with known RSI behavior
        # RSI should be 100 when all price changes are positive
        up_data = pd.DataFrame({
            'Close': [100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115],
            'Open': [99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114],
            'High': [101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116],
            'Low': [98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113],
            'Volume': [1000] * 16
        })
        
        result = self.rsi(up_data.copy(), self.point)
        rsi_values = result['RSI'].dropna()
        
        if len(rsi_values) > 0:
            # RSI should be high for consistently rising prices
            assert rsi_values.mean() > 70, "RSI should be high for rising prices"
        
        # RSI should be 0 when all price changes are negative
        down_data = pd.DataFrame({
            'Close': [115, 114, 113, 112, 111, 110, 109, 108, 107, 106, 105, 104, 103, 102, 101, 100],
            'Open': [114, 113, 112, 111, 110, 109, 108, 107, 106, 105, 104, 103, 102, 101, 100, 99],
            'High': [116, 115, 114, 113, 112, 111, 110, 109, 108, 107, 106, 105, 104, 103, 102, 101],
            'Low': [113, 112, 111, 110, 109, 108, 107, 106, 105, 104, 103, 102, 101, 100, 99, 98],
            'Volume': [1000] * 16
        })
        
        result = self.rsi(down_data.copy(), self.point)
        rsi_values = result['RSI'].dropna()
        
        if len(rsi_values) > 0:
            # RSI should be low for consistently falling prices
            assert rsi_values.mean() < 30, "RSI should be low for falling prices"

    def test_stochastic_mathematical_properties(self):
        """Test Stochastic mathematical properties."""
        # Create data where close is at the high (should give 100% K)
        high_close_data = pd.DataFrame({
            'Close': [105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120],
            'Open': [100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115],
            'High': [105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120],
            'Low': [95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110],
            'Volume': [1000] * 16
        })
        
        result = self.stoch(high_close_data.copy(), self.point)
        k_values = result['Stoch_K'].dropna()
        
        if len(k_values) > 0:
            # K should be close to 100 when close is at the high
            assert k_values.mean() > 90, "Stochastic K should be high when close is at high"
        
        # Create data where close is at the low (should give 0% K)
        low_close_data = pd.DataFrame({
            'Close': [95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110],
            'Open': [100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115],
            'High': [105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120],
            'Low': [95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110],
            'Volume': [1000] * 16
        })
        
        result = self.stoch(low_close_data.copy(), self.point)
        k_values = result['Stoch_K'].dropna()
        
        if len(k_values) > 0:
            # В реальной формуле K не всегда будет близко к 0, но должно быть заметно ниже, чем при close=high
            assert k_values.mean() < 60, "Stochastic K should be low when close is at low"

    def test_bollinger_bands_mathematical_properties(self):
        """Test Bollinger Bands mathematical properties."""
        # Create data with constant values
        constant_data = pd.DataFrame({
            'Close': [100] * 20,
            'Open': [100] * 20,
            'High': [100] * 20,
            'Low': [100] * 20,
            'Volume': [1000] * 20
        })
        
        result = self.bb(constant_data.copy(), self.point)
        
        # For constant data, all bands should be equal
        bb_valid = result.dropna()
        if len(bb_valid) > 0:
            # Allow for small floating point differences
            assert all(abs(bb_valid['BB_Upper'] - bb_valid['BB_Middle']) < 1e-10)
            assert all(abs(bb_valid['BB_Middle'] - bb_valid['BB_Lower']) < 1e-10)

    def test_ema_mathematical_properties(self):
        """Test EMA mathematical properties."""
        # Create data with a clear trend
        trend_data = pd.DataFrame({
            'Close': [100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120],
            'Open': [99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119],
            'High': [101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121],
            'Low': [98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118],
            'Volume': [1000] * 21
        })
        
        result = self.ema(trend_data.copy(), self.point)
        ema_values = result['EMA'].dropna()
        
        if len(ema_values) > 1:
            # EMA should follow the trend
            assert ema_values.iloc[-1] > ema_values.iloc[0], "EMA should follow upward trend"

    def test_vwap_mathematical_properties(self):
        """Test VWAP mathematical properties."""
        # Create data with known typical prices and volumes
        data = pd.DataFrame({
            'Close': [100, 101, 102],
            'Open': [99, 100, 101],
            'High': [101, 102, 103],
            'Low': [98, 99, 100],
            'Volume': [1000, 2000, 1000]  # Middle period has higher volume
        })
        
        result = self.vwap(data.copy(), self.point)
        vwap_values = result['VWAP'].dropna()
        
        if len(vwap_values) > 0:
            # VWAP should be weighted towards the period with higher volume
            # The middle period (101) has higher volume, so VWAP should be closer to 101
            assert abs(vwap_values.iloc[-1] - 101) < abs(vwap_values.iloc[-1] - 100)
            assert abs(vwap_values.iloc[-1] - 101) < abs(vwap_values.iloc[-1] - 102)

    def test_atr_mathematical_properties(self):
        """Test ATR mathematical properties."""
        # Create data with known true ranges
        data = pd.DataFrame({
            'Close': [100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115],
            'Open': [99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114],
            'High': [105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120],
            'Low': [95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110],
            'Volume': [1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800, 1900, 2000, 2100, 2200, 2300, 2400, 2500]
        })
        
        result = self.atr(data.copy(), self.point)
        atr_values = result['ATR'].dropna()
        
        if len(atr_values) > 0:
            # ATR should be positive
            assert all(atr_values >= 0), "ATR should always be positive"
            
            # ATR should reflect the true range
            # True range = max(high-low, abs(high-prev_close), abs(low-prev_close))
            # For this data, true range should be around 10
            assert atr_values.mean() > 5, "ATR should reflect the true range"

    def test_obv_mathematical_properties(self):
        """Test OBV mathematical properties."""
        # Create data with known price-volume relationships
        data = pd.DataFrame({
            'Close': [100, 101, 100, 102, 101],  # Up, down, up, down
            'Open': [99, 100, 99, 101, 100],
            'High': [101, 102, 101, 103, 102],
            'Low': [98, 99, 98, 100, 99],
            'Volume': [1000, 1000, 1000, 1000, 1000]
        })
        
        result = self.obv(data.copy(), self.point)
        obv_values = result['OBV'].dropna()
        
        if len(obv_values) > 1:
            # OBV should change based on price direction
            # First change: 100->101 (up) -> OBV increases
            # Second change: 101->100 (down) -> OBV decreases
            # Third change: 100->102 (up) -> OBV increases
            # Fourth change: 102->101 (down) -> OBV decreases
            
            # OBV should not be constant
            assert not all(obv_values == obv_values.iloc[0]), "OBV should change with price movements"

    def test_adx_mathematical_properties(self):
        """Test ADX mathematical properties."""
        # Create data with strong trend
        trend_data = pd.DataFrame({
            'Close': [100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115],
            'Open': [99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114],
            'High': [101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116],
            'Low': [98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113],
            'Volume': [1000] * 16
        })
        
        result = self.adx(trend_data.copy(), self.point)
        adx_values = result['ADX'].dropna()
        
        if len(adx_values) > 0:
            # ADX should be positive
            assert all(adx_values >= 0), "ADX should always be positive"
            
            # ADX should be <= 100
            assert all(adx_values <= 100), "ADX should be <= 100"

    def test_indicator_boundaries(self):
        """Test that indicators respect their mathematical boundaries."""
        # Test RSI boundaries (0-100)
        data = pd.DataFrame({
            'Close': np.random.uniform(50, 150, 100),
            'Open': np.random.uniform(50, 150, 100),
            'High': np.random.uniform(50, 150, 100),
            'Low': np.random.uniform(50, 150, 100),
            'Volume': np.random.randint(1000, 5000, 100)
        })
        
        rsi_result = self.rsi(data.copy(), self.point)
        rsi_values = rsi_result['RSI'].dropna()
        
        if len(rsi_values) > 0:
            # RSI should be between 0 and 100
            assert all(rsi_values >= 0), "RSI should be >= 0"
            assert all(rsi_values <= 100), "RSI should be <= 100"
        
        # Test Stochastic boundaries (0-100)
        stoch_result = self.stoch(data.copy(), self.point)
        stoch_k_values = stoch_result['Stoch_K'].dropna()
        
        if len(stoch_k_values) > 0:
            # Stochastic K should be between 0 and 100
            assert all(stoch_k_values >= 0), "Stochastic K should be >= 0"
            assert all(stoch_k_values <= 100), "Stochastic K should be <= 100"

    def test_indicator_consistency(self):
        """Test that indicators produce consistent results for identical inputs."""
        data = pd.DataFrame({
            'Close': [100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115],
            'Open': [99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114],
            'High': [101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116],
            'Low': [98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113],
            'Volume': [1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800, 1900, 2000, 2100, 2200, 2300, 2400, 2500]
        })
        
        # Test indicators that return DataFrames
        indicators_df = [self.atr, self.rsi, self.ema, self.vwap]
        
        for indicator in indicators_df:
            result1 = indicator(data.copy(), self.point)
            result2 = indicator(data.copy(), self.point)
            
            # Results should be identical
            pd.testing.assert_frame_equal(result1, result2,
                                         check_dtype=False)  # Allow for minor dtype differences
        
        # Test indicators that return tuples (ADX)
        adx_result1 = self.adx(data.copy(), self.point)
        adx_result2 = self.adx(data.copy(), self.point)
        
        # Results should be identical
        pd.testing.assert_series_equal(adx_result1['ADX'], adx_result2['ADX'], check_dtype=False)
        
        # Test indicators that require additional parameters
        bb_result1 = self.bb(data.copy(), self.point)
        bb_result2 = self.bb(data.copy(), self.point)
        
        pd.testing.assert_frame_equal(bb_result1, bb_result2,
                                     check_dtype=False)
        
        stoch_result1 = self.stoch(data.copy(), self.point)
        stoch_result2 = self.stoch(data.copy(), self.point)
        
        pd.testing.assert_frame_equal(stoch_result1, stoch_result2,
                                     check_dtype=False)
        
        obv_result1 = self.obv(data.copy(), self.point)
        obv_result2 = self.obv(data.copy(), self.point)
        
        pd.testing.assert_frame_equal(obv_result1, obv_result2,
                                     check_dtype=False) 