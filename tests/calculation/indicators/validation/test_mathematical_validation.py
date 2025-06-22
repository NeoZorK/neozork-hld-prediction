# tests/calculation/indicators/validation/test_mathematical_validation.py

import pytest
import pandas as pd
import numpy as np
from src.calculation.indicators.volatility.atr_ind import ATRIndicator
from src.calculation.indicators.volatility.bb_ind import BBIndicator
from src.calculation.indicators.volume.obv_ind import OBVIndicator
from src.calculation.indicators.volume.vwap_ind import VWAPIndicator
from src.calculation.indicators.oscillators.rsi_ind import RsiIndicator
from src.calculation.indicators.oscillators.stoch_ind import StochIndicator
from src.calculation.indicators.trend.ema_ind import EMAIndicator
from src.calculation.indicators.trend.adx_ind import ADXIndicator

class TestMathematicalValidation:
    """Mathematical validation tests for indicators."""
    
    def setup_method(self):
        """Set up indicators for testing."""
        self.atr = ATRIndicator()
        self.bb = BBIndicator()
        self.obv = OBVIndicator()
        self.vwap = VWAPIndicator()
        self.rsi = RsiIndicator()
        self.stoch = StochIndicator()
        self.ema = EMAIndicator()
        self.adx = ADXIndicator()

    def test_rsi_mathematical_properties(self):
        """Test RSI mathematical properties."""
        # Create data with known RSI behavior
        # RSI should be 100 when all price changes are positive
        up_data = pd.DataFrame({
            'close': [100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110],
            'open': [99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109],
            'high': [101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111],
            'low': [98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108],
            'volume': [1000] * 11
        })
        
        result = self.rsi.calculate(up_data)
        rsi_values = result['RSI'].dropna()
        
        if len(rsi_values) > 0:
            # RSI should be high for consistently rising prices
            assert rsi_values.mean() > 70, "RSI should be high for rising prices"
        
        # RSI should be 0 when all price changes are negative
        down_data = pd.DataFrame({
            'close': [110, 109, 108, 107, 106, 105, 104, 103, 102, 101, 100],
            'open': [109, 108, 107, 106, 105, 104, 103, 102, 101, 100, 99],
            'high': [111, 110, 109, 108, 107, 106, 105, 104, 103, 102, 101],
            'low': [108, 107, 106, 105, 104, 103, 102, 101, 100, 99, 98],
            'volume': [1000] * 11
        })
        
        result = self.rsi.calculate(down_data)
        rsi_values = result['RSI'].dropna()
        
        if len(rsi_values) > 0:
            # RSI should be low for consistently falling prices
            assert rsi_values.mean() < 30, "RSI should be low for falling prices"

    def test_stochastic_mathematical_properties(self):
        """Test Stochastic mathematical properties."""
        # Create data where close is at the high (should give 100% K)
        high_close_data = pd.DataFrame({
            'close': [105, 106, 107, 108, 109, 110],
            'open': [100, 101, 102, 103, 104, 105],
            'high': [105, 106, 107, 108, 109, 110],
            'low': [95, 96, 97, 98, 99, 100],
            'volume': [1000] * 6
        })
        
        result = self.stoch.calculate(high_close_data)
        k_values = result['Stoch_K'].dropna()
        
        if len(k_values) > 0:
            # K should be close to 100 when close is at the high
            assert k_values.mean() > 90, "Stochastic K should be high when close is at high"
        
        # Create data where close is at the low (should give 0% K)
        low_close_data = pd.DataFrame({
            'close': [95, 96, 97, 98, 99, 100],
            'open': [100, 101, 102, 103, 104, 105],
            'high': [105, 106, 107, 108, 109, 110],
            'low': [95, 96, 97, 98, 99, 100],
            'volume': [1000] * 6
        })
        
        result = self.stoch.calculate(low_close_data)
        k_values = result['Stoch_K'].dropna()
        
        if len(k_values) > 0:
            # K should be close to 0 when close is at the low
            assert k_values.mean() < 10, "Stochastic K should be low when close is at low"

    def test_bollinger_bands_mathematical_properties(self):
        """Test Bollinger Bands mathematical properties."""
        # Create data with constant values
        constant_data = pd.DataFrame({
            'close': [100] * 20,
            'open': [100] * 20,
            'high': [100] * 20,
            'low': [100] * 20,
            'volume': [1000] * 20
        })
        
        result = self.bb.calculate(constant_data)
        
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
            'close': [100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110],
            'open': [99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109],
            'high': [101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111],
            'low': [98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108],
            'volume': [1000] * 11
        })
        
        result = self.ema.calculate(trend_data)
        ema_values = result['EMA'].dropna()
        
        if len(ema_values) > 1:
            # EMA should follow the trend
            assert ema_values.iloc[-1] > ema_values.iloc[0], "EMA should follow upward trend"

    def test_vwap_mathematical_properties(self):
        """Test VWAP mathematical properties."""
        # Create data with known typical prices and volumes
        data = pd.DataFrame({
            'close': [100, 101, 102],
            'open': [99, 100, 101],
            'high': [101, 102, 103],
            'low': [98, 99, 100],
            'volume': [1000, 2000, 1000]  # Middle period has higher volume
        })
        
        result = self.vwap.calculate(data)
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
            'close': [100, 101, 102],
            'open': [99, 100, 101],
            'high': [105, 106, 107],  # High true range
            'low': [95, 96, 97],      # Low true range
            'volume': [1000, 1100, 1200]
        })
        
        result = self.atr.calculate(data)
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
            'close': [100, 101, 100, 102, 101],  # Up, down, up, down
            'open': [99, 100, 99, 101, 100],
            'high': [101, 102, 101, 103, 102],
            'low': [98, 99, 98, 100, 99],
            'volume': [1000, 1000, 1000, 1000, 1000]
        })
        
        result = self.obv.calculate(data)
        obv_values = result['OBV'].dropna()
        
        if len(obv_values) > 1:
            # OBV should change based on price direction
            # First change: 100->101 (up) -> OBV increases
            # Second change: 101->100 (down) -> OBV decreases
            # Third change: 100->102 (up) -> OBV increases
            # Fourth change: 102->101 (down) -> OBV decreases
            
            # OBV should not be constant
            assert not all(obv_values == obv_values.iloc[0]), "OBV should change with price direction"

    def test_adx_mathematical_properties(self):
        """Test ADX mathematical properties."""
        # Create data with strong trend
        trend_data = pd.DataFrame({
            'close': [100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110],
            'open': [99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109],
            'high': [101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111],
            'low': [98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108],
            'volume': [1000] * 11
        })
        
        result = self.adx.calculate(trend_data)
        adx_values = result['ADX'].dropna()
        
        if len(adx_values) > 0:
            # ADX should be positive
            assert all(adx_values >= 0), "ADX should always be positive"
            
            # ADX should be higher for trending data
            assert adx_values.mean() > 20, "ADX should be higher for trending data"

    def test_indicator_boundaries(self):
        """Test that indicators respect their mathematical boundaries."""
        # Test RSI boundaries (0-100)
        data = pd.DataFrame({
            'close': np.random.uniform(50, 150, 100),
            'open': np.random.uniform(50, 150, 100),
            'high': np.random.uniform(50, 150, 100),
            'low': np.random.uniform(50, 150, 100),
            'volume': np.random.randint(1000, 5000, 100)
        })
        
        rsi_result = self.rsi.calculate(data)
        rsi_values = rsi_result['RSI'].dropna()
        
        if len(rsi_values) > 0:
            assert all(rsi_values >= 0), "RSI should be >= 0"
            assert all(rsi_values <= 100), "RSI should be <= 100"
        
        # Test Stochastic boundaries (0-100)
        stoch_result = self.stoch.calculate(data)
        k_values = stoch_result['Stoch_K'].dropna()
        d_values = stoch_result['Stoch_D'].dropna()
        
        if len(k_values) > 0:
            assert all(k_values >= 0), "Stochastic K should be >= 0"
            assert all(k_values <= 100), "Stochastic K should be <= 100"
        
        if len(d_values) > 0:
            assert all(d_values >= 0), "Stochastic D should be >= 0"
            assert all(d_values <= 100), "Stochastic D should be <= 100"

    def test_indicator_consistency(self):
        """Test that indicators produce consistent results for identical inputs."""
        data = pd.DataFrame({
            'close': [100, 101, 102, 103, 104],
            'open': [99, 100, 101, 102, 103],
            'high': [101, 102, 103, 104, 105],
            'low': [98, 99, 100, 101, 102],
            'volume': [1000, 1100, 1200, 1300, 1400]
        })
        
        indicators = [self.atr, self.bb, self.obv, self.vwap, self.rsi, self.stoch, self.ema, self.adx]
        
        for indicator in indicators:
            result1 = indicator.calculate(data)
            result2 = indicator.calculate(data)
            
            # Results should be identical
            pd.testing.assert_frame_equal(result1, result2, 
                                         check_dtype=False,  # Allow for minor dtype differences
                                         check_index=False)  # Allow for minor index differences 