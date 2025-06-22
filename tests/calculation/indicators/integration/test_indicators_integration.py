# tests/calculation/indicators/integration/test_indicators_integration.py

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

class TestIndicatorsIntegration:
    """Integration tests for multiple indicators working together."""
    
    def setup_method(self):
        """Set up test data with realistic market conditions."""
        # Create realistic market data with trends and volatility
        np.random.seed(42)  # For reproducible tests
        
        # Generate 100 days of realistic price data
        dates = pd.date_range('2023-01-01', periods=100, freq='D')
        
        # Create trending data with some volatility
        base_price = 100
        trend = np.linspace(0, 20, 100)  # Upward trend
        noise = np.random.normal(0, 2, 100)  # Random noise
        prices = base_price + trend + noise
        
        self.market_data = pd.DataFrame({
            'Open': prices + np.random.normal(0, 0.5, 100),
            'High': prices + np.abs(np.random.normal(1, 0.5, 100)),
            'Low': prices - np.abs(np.random.normal(1, 0.5, 100)),
            'Close': prices,
            'Volume': np.random.randint(1000, 5000, 100)
        }, index=dates)
        
        # Set point value for indicators
        self.point = 0.0001
        
        # Initialize indicators with apply_rule functions
        self.atr = apply_rule_atr
        self.bb = apply_rule_bollinger_bands
        self.obv = apply_rule_obv
        self.vwap = apply_rule_vwap
        self.rsi = apply_rule_rsi
        self.stoch = apply_rule_stochastic
        self.ema = apply_rule_ema
        self.adx = apply_rule_adx

    def test_multiple_volatility_indicators(self):
        """Test that volatility indicators work together."""
        # Calculate ATR and Bollinger Bands
        atr_result = self.atr(self.market_data.copy(), self.point)
        bb_result = self.bb(self.market_data.copy(), self.point)
        
        # Both should have valid results
        assert 'ATR' in atr_result.columns
        assert 'BB_Upper' in bb_result.columns
        assert 'BB_Middle' in bb_result.columns
        assert 'BB_Lower' in bb_result.columns
        
        # ATR should be positive
        assert all(atr_result['ATR'].dropna() >= 0)
        
        # Bollinger Bands should maintain proper relationships
        bb_valid = bb_result.dropna()
        if len(bb_valid) > 0:
            assert all(bb_valid['BB_Upper'] >= bb_valid['BB_Middle'])
            assert all(bb_valid['BB_Middle'] >= bb_valid['BB_Lower'])

    def test_volume_and_price_indicators(self):
        """Test volume indicators with price-based indicators."""
        # Calculate OBV and VWAP
        obv_result = self.obv(self.market_data.copy(), self.point)
        vwap_result = self.vwap(self.market_data.copy(), self.point)
        
        # Both should have valid results
        assert 'OBV' in obv_result.columns
        assert 'VWAP' in vwap_result.columns
        
        # VWAP should be within price range
        vwap_values = vwap_result['VWAP'].dropna()
        if len(vwap_values) > 0:
            assert all(vwap_values >= self.market_data['Low'].min())
            assert all(vwap_values <= self.market_data['High'].max())

    def test_oscillator_combinations(self):
        """Test multiple oscillators together."""
        # Calculate RSI and Stochastic
        rsi_result = self.rsi(self.market_data.copy(), self.point)
        stoch_result = self.stoch(self.market_data.copy(), self.point)
        
        # Both should have valid results
        assert 'RSI' in rsi_result.columns
        assert 'Stoch_K' in stoch_result.columns
        assert 'Stoch_D' in stoch_result.columns
        
        # RSI should be between 0 and 100
        rsi_values = rsi_result['RSI'].dropna()
        if len(rsi_values) > 0:
            assert all(rsi_values >= 0)
            assert all(rsi_values <= 100)
        
        # Stochastic should be between 0 and 100
        stoch_k_values = stoch_result['Stoch_K'].dropna()
        stoch_d_values = stoch_result['Stoch_D'].dropna()
        if len(stoch_k_values) > 0:
            assert all(stoch_k_values >= 0)
            assert all(stoch_k_values <= 100)
        if len(stoch_d_values) > 0:
            assert all(stoch_d_values >= 0)
            assert all(stoch_d_values <= 100)

    def test_trend_indicators(self):
        """Test trend indicators together."""
        # Calculate EMA and ADX
        ema_result = self.ema(self.market_data.copy(), self.point)
        adx_result = self.adx(self.market_data.copy(), self.point)
        
        # Both should have valid results
        assert 'EMA' in ema_result.columns
        assert 'ADX' in adx_result.columns
        
        # ADX should be positive (measures trend strength)
        adx_values = adx_result['ADX'].dropna()
        if len(adx_values) > 0:
            assert all(adx_values >= 0)

    def test_all_indicators_together(self):
        """Test all indicators calculated on the same dataset."""
        # Calculate all indicators
        results = {}
        indicators = [
            ('ATR', self.atr),
            ('BB', self.bb),
            ('OBV', self.obv),
            ('VWAP', self.vwap),
            ('RSI', self.rsi),
            ('Stoch', self.stoch),
            ('EMA', self.ema),
            ('ADX', self.adx)
        ]
        
        for name, indicator in indicators:
            try:
                results[name] = indicator(self.market_data.copy(), self.point)
            except Exception as e:
                pytest.fail(f"Indicator {name} failed: {e}")
        
        # All results should have the same length as input data
        for name, result in results.items():
            assert len(result) == len(self.market_data), f"Length mismatch for {name}"

    def test_indicators_with_extreme_data(self):
        """Test indicators with extreme market conditions."""
        # Create extreme data (very volatile)
        extreme_data = self.market_data.copy()
        extreme_data['High'] = extreme_data['Close'] * 1.5  # 50% higher
        extreme_data['Low'] = extreme_data['Close'] * 0.5   # 50% lower
        extreme_data['Volume'] = extreme_data['Volume'] * 10  # 10x volume
        
        # Test that indicators handle extreme data gracefully
        indicators = [self.atr, self.bb, self.obv, self.vwap, self.rsi, self.stoch, self.ema, self.adx]
        
        for indicator in indicators:
            try:
                result = indicator(extreme_data.copy(), self.point)
                assert isinstance(result, pd.DataFrame)
                assert len(result) == len(extreme_data)
            except Exception as e:
                pytest.fail(f"Indicator {indicator.__name__} failed with extreme data: {e}")

    def test_indicators_with_constant_data(self):
        """Test indicators with constant (no movement) data."""
        # Create constant data
        constant_data = self.market_data.copy()
        constant_data['Open'] = 100
        constant_data['High'] = 100
        constant_data['Low'] = 100
        constant_data['Close'] = 100
        constant_data['Volume'] = 1000
        
        # Test that indicators handle constant data gracefully
        indicators = [self.atr, self.bb, self.obv, self.vwap, self.rsi, self.stoch, self.ema, self.adx]
        
        for indicator in indicators:
            try:
                result = indicator(constant_data.copy(), self.point)
                assert isinstance(result, pd.DataFrame)
                assert len(result) == len(constant_data)
            except Exception as e:
                pytest.fail(f"Indicator {indicator.__name__} failed with constant data: {e}")

    def test_indicators_with_missing_data(self):
        """Test indicators with missing data points."""
        # Create data with some missing values
        missing_data = self.market_data.copy()
        missing_data.iloc[10:15, missing_data.columns.get_loc('Close')] = np.nan
        missing_data.iloc[20:25, missing_data.columns.get_loc('Volume')] = np.nan
        
        # Test that indicators handle missing data gracefully
        indicators = [self.atr, self.bb, self.obv, self.vwap, self.rsi, self.stoch, self.ema, self.adx]
        
        for indicator in indicators:
            try:
                result = indicator(missing_data.copy(), self.point)
                assert isinstance(result, pd.DataFrame)
                assert len(result) == len(missing_data)
            except Exception as e:
                pytest.fail(f"Indicator {indicator.__name__} failed with missing data: {e}")

    def test_indicators_performance(self):
        """Test that indicators perform reasonably fast."""
        import time
        
        # Test performance with larger dataset
        large_data = self.market_data.copy()
        # Duplicate data to make it larger
        large_data = pd.concat([large_data] * 5, ignore_index=True)
        
        indicators = [self.atr, self.bb, self.obv, self.vwap, self.rsi, self.stoch, self.ema, self.adx]
        
        for indicator in indicators:
            start_time = time.time()
            result = indicator(large_data.copy(), self.point)
            end_time = time.time()
            
            # Should complete within reasonable time (5 seconds)
            assert end_time - start_time < 5.0, f"Indicator {indicator.__name__} took too long"
            assert isinstance(result, pd.DataFrame)
            assert len(result) == len(large_data) 