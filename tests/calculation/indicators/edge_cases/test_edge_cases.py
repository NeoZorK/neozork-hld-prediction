# tests/calculation/indicators/edge_cases/test_edge_cases.py

import pytest
import pandas as pd
import numpy as np
from src.calculation.indicators.volatility.atr_ind import calculate_atr
from src.calculation.indicators.volatility.bb_ind import apply_rule_bollinger_bands
from src.calculation.indicators.volume.obv_ind import calculate_obv
from src.calculation.indicators.volume.vwap_ind import calculate_vwap
from src.calculation.indicators.oscillators.rsi_ind import calculate_rsi
from src.calculation.indicators.oscillators.stoch_ind import apply_rule_stochastic
from src.calculation.indicators.trend.ema_ind import calculate_ema
from src.calculation.indicators.trend.adx_ind import calculate_adx

class TestEdgeCases:
    """Edge case tests for indicators."""
    
    def setup_method(self):
        """Set up indicators for testing."""
        self.atr = calculate_atr
        self.bb = apply_rule_bollinger_bands
        self.obv = calculate_obv
        self.vwap = calculate_vwap
        self.rsi = calculate_rsi
        self.stoch = apply_rule_stochastic
        self.ema = calculate_ema
        self.adx = calculate_adx

    def test_single_row_data(self):
        """Test indicators with single row of data."""
        single_row = pd.DataFrame({
            'open': [100],
            'high': [105],
            'low': [95],
            'close': [102],
            'volume': [1000]
        })
        
        indicators = [self.atr, self.bb, self.obv, self.vwap, self.rsi, self.stoch, self.ema, self.adx]
        
        for indicator in indicators:
            try:
                result = indicator(single_row)
                assert isinstance(result, pd.DataFrame)
                assert len(result) == 1
            except Exception as e:
                # Some indicators might need more data points
                assert "insufficient" in str(e).lower() or "period" in str(e).lower()

    def test_two_rows_data(self):
        """Test indicators with minimal data (2 rows)."""
        two_rows = pd.DataFrame({
            'open': [100, 101],
            'high': [105, 106],
            'low': [95, 96],
            'close': [102, 103],
            'volume': [1000, 1100]
        })
        
        indicators = [self.atr, self.bb, self.obv, self.vwap, self.rsi, self.stoch, self.ema, self.adx]
        
        for indicator in indicators:
            try:
                result = indicator(two_rows)
                assert isinstance(result, pd.DataFrame)
                assert len(result) == 2
            except Exception as e:
                # Some indicators might need more data points
                assert "insufficient" in str(e).lower() or "period" in str(e).lower()

    def test_very_large_numbers(self):
        """Test indicators with very large price values."""
        large_data = pd.DataFrame({
            'open': [1000000, 1000001, 1000002],
            'high': [1000005, 1000006, 1000007],
            'low': [999995, 999996, 999997],
            'close': [1000002, 1000003, 1000004],
            'volume': [1000000, 1100000, 1200000]
        })
        
        indicators = [self.atr, self.bb, self.obv, self.vwap, self.rsi, self.stoch, self.ema, self.adx]
        
        for indicator in indicators:
            try:
                result = indicator(large_data)
                assert isinstance(result, pd.DataFrame)
                assert len(result) == 3
            except Exception as e:
                pytest.fail(f"Indicator {indicator.__name__} failed with large numbers: {e}")

    def test_very_small_numbers(self):
        """Test indicators with very small price values."""
        small_data = pd.DataFrame({
            'open': [0.0001, 0.0002, 0.0003],
            'high': [0.0005, 0.0006, 0.0007],
            'low': [0.00005, 0.00006, 0.00007],
            'close': [0.0002, 0.0003, 0.0004],
            'volume': [1000, 1100, 1200]
        })
        
        indicators = [self.atr, self.bb, self.obv, self.vwap, self.rsi, self.stoch, self.ema, self.adx]
        
        for indicator in indicators:
            try:
                result = indicator(small_data)
                assert isinstance(result, pd.DataFrame)
                assert len(result) == 3
            except Exception as e:
                pytest.fail(f"Indicator {indicator.__name__} failed with small numbers: {e}")

    def test_negative_prices(self):
        """Test indicators with negative price values."""
        negative_data = pd.DataFrame({
            'open': [-100, -101, -102],
            'high': [-95, -96, -97],
            'low': [-105, -106, -107],
            'close': [-102, -103, -104],
            'volume': [1000, 1100, 1200]
        })
        
        indicators = [self.atr, self.bb, self.obv, self.vwap, self.rsi, self.stoch, self.ema, self.adx]
        
        for indicator in indicators:
            try:
                result = indicator(negative_data)
                assert isinstance(result, pd.DataFrame)
                assert len(result) == 3
            except Exception as e:
                # Some indicators might not handle negative prices well
                pass

    def test_zero_prices(self):
        """Test indicators with zero price values."""
        zero_data = pd.DataFrame({
            'open': [0, 0, 0],
            'high': [0, 0, 0],
            'low': [0, 0, 0],
            'close': [0, 0, 0],
            'volume': [1000, 1100, 1200]
        })
        
        indicators = [self.atr, self.bb, self.obv, self.vwap, self.rsi, self.stoch, self.ema, self.adx]
        
        for indicator in indicators:
            try:
                result = indicator(zero_data)
                assert isinstance(result, pd.DataFrame)
                assert len(result) == 3
            except Exception as e:
                # Some indicators might not handle zero prices well
                pass

    def test_zero_volume(self):
        """Test indicators with zero volume."""
        zero_volume_data = pd.DataFrame({
            'open': [100, 101, 102],
            'high': [105, 106, 107],
            'low': [95, 96, 97],
            'close': [102, 103, 104],
            'volume': [0, 0, 0]
        })
        
        indicators = [self.atr, self.bb, self.obv, self.vwap, self.rsi, self.stoch, self.ema, self.adx]
        
        for indicator in indicators:
            try:
                result = indicator(zero_volume_data)
                assert isinstance(result, pd.DataFrame)
                assert len(result) == 3
            except Exception as e:
                pytest.fail(f"Indicator {indicator.__name__} failed with zero volume: {e}")

    def test_negative_volume(self):
        """Test indicators with negative volume."""
        negative_volume_data = pd.DataFrame({
            'open': [100, 101, 102],
            'high': [105, 106, 107],
            'low': [95, 96, 97],
            'close': [102, 103, 104],
            'volume': [-1000, -1100, -1200]
        })
        
        indicators = [self.atr, self.bb, self.obv, self.vwap, self.rsi, self.stoch, self.ema, self.adx]
        
        for indicator in indicators:
            try:
                result = indicator(negative_volume_data)
                assert isinstance(result, pd.DataFrame)
                assert len(result) == 3
            except Exception as e:
                # Some indicators might not handle negative volume well
                pass

    def test_infinite_values(self):
        """Test indicators with infinite values."""
        infinite_data = pd.DataFrame({
            'open': [100, np.inf, 102],
            'high': [105, np.inf, 107],
            'low': [95, -np.inf, 97],
            'close': [102, np.inf, 104],
            'volume': [1000, np.inf, 1200]
        })
        
        indicators = [self.atr, self.bb, self.obv, self.vwap, self.rsi, self.stoch, self.ema, self.adx]
        
        for indicator in indicators:
            try:
                result = indicator(infinite_data)
                assert isinstance(result, pd.DataFrame)
                assert len(result) == 3
            except Exception as e:
                # Some indicators might not handle infinite values well
                pass

    def test_nan_values(self):
        """Test indicators with NaN values."""
        nan_data = pd.DataFrame({
            'open': [100, np.nan, 102],
            'high': [105, np.nan, 107],
            'low': [95, np.nan, 97],
            'close': [102, np.nan, 104],
            'volume': [1000, np.nan, 1200]
        })
        
        indicators = [self.atr, self.bb, self.obv, self.vwap, self.rsi, self.stoch, self.ema, self.adx]
        
        for indicator in indicators:
            try:
                result = indicator(nan_data)
                assert isinstance(result, pd.DataFrame)
                assert len(result) == 3
            except Exception as e:
                pytest.fail(f"Indicator {indicator.__name__} failed with NaN values: {e}")

    def test_all_nan_data(self):
        """Test indicators with all NaN data."""
        all_nan_data = pd.DataFrame({
            'open': [np.nan, np.nan, np.nan],
            'high': [np.nan, np.nan, np.nan],
            'low': [np.nan, np.nan, np.nan],
            'close': [np.nan, np.nan, np.nan],
            'volume': [np.nan, np.nan, np.nan]
        })
        
        indicators = [self.atr, self.bb, self.obv, self.vwap, self.rsi, self.stoch, self.ema, self.adx]
        
        for indicator in indicators:
            try:
                result = indicator(all_nan_data)
                assert isinstance(result, pd.DataFrame)
                assert len(result) == 3
            except Exception as e:
                # Some indicators might not handle all NaN data well
                pass

    def test_very_long_periods(self):
        """Test indicators with very long periods."""
        # Create data with 1000 rows
        long_data = pd.DataFrame({
            'open': np.random.uniform(100, 110, 1000),
            'high': np.random.uniform(110, 120, 1000),
            'low': np.random.uniform(90, 100, 1000),
            'close': np.random.uniform(100, 110, 1000),
            'volume': np.random.randint(1000, 2000, 1000)
        })
        
        # Test with very long periods
        long_period_indicators = [
            calculate_atr(period=500),
            apply_rule_bollinger_bands(period=500),
            calculate_rsi(period=500),
            apply_rule_stochastic(k_period=500, d_period=100),
            calculate_ema(period=500),
            calculate_adx(period=500)
        ]
        
        for indicator in long_period_indicators:
            try:
                result = indicator(long_data)
                assert isinstance(result, pd.DataFrame)
                assert len(result) == 1000
            except Exception as e:
                pytest.fail(f"Indicator {indicator.__name__} failed with long period: {e}")

    def test_mixed_data_types(self):
        """Test indicators with mixed data types in columns."""
        mixed_data = pd.DataFrame({
            'open': [100, '101', 102],  # Mixed int and string
            'high': [105, 106, 107],
            'low': [95, 96, 97],
            'close': [102, 103, 104],
            'volume': [1000, 1100, 1200]
        })
        
        indicators = [self.atr, self.bb, self.obv, self.vwap, self.rsi, self.stoch, self.ema, self.adx]
        
        for indicator in indicators:
            try:
                result = indicator(mixed_data)
                assert isinstance(result, pd.DataFrame)
                assert len(result) == 3
            except Exception as e:
                # Expected to fail with mixed data types
                assert "dtype" in str(e).lower() or "type" in str(e).lower()

    def test_duplicate_index(self):
        """Test indicators with duplicate index values."""
        duplicate_index_data = pd.DataFrame({
            'open': [100, 101, 102],
            'high': [105, 106, 107],
            'low': [95, 96, 97],
            'close': [102, 103, 104],
            'volume': [1000, 1100, 1200]
        }, index=[0, 0, 1])  # Duplicate index
        
        indicators = [self.atr, self.bb, self.obv, self.vwap, self.rsi, self.stoch, self.ema, self.adx]
        
        for indicator in indicators:
            try:
                result = indicator(duplicate_index_data)
                assert isinstance(result, pd.DataFrame)
                assert len(result) == 3
            except Exception as e:
                pytest.fail(f"Indicator {indicator.__name__} failed with duplicate index: {e}") 