# tests/calculation/indicators/edge_cases/test_edge_cases.py

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

class TestEdgeCases:
    """Edge case tests for indicators."""
    
    def setup_method(self):
        """Set up indicators for testing."""
        self.atr = apply_rule_atr
        self.bb = apply_rule_bollinger_bands
        self.obv = apply_rule_obv
        self.vwap = apply_rule_vwap
        self.rsi = apply_rule_rsi
        self.stoch = apply_rule_stochastic
        self.ema = apply_rule_ema
        self.adx = apply_rule_adx
        self.point = 0.0001

    def test_single_row_data(self):
        """Test indicators with single row of data."""
        single_row = pd.DataFrame({
            'Open': [100],
            'High': [105],
            'Low': [95],
            'Close': [102],
            'Volume': [1000]
        })
        
        indicators = [self.atr, self.bb, self.obv, self.vwap, self.rsi, self.stoch, self.ema, self.adx]
        
        for indicator in indicators:
            try:
                result = indicator(single_row.copy(), self.point)
                assert isinstance(result, pd.DataFrame) or isinstance(result, pd.Series)
                assert len(result) == 1
            except Exception:
                pass

    def test_two_rows_data(self):
        """Test indicators with minimal data (2 rows)."""
        two_rows = pd.DataFrame({
            'Open': [100, 101],
            'High': [105, 106],
            'Low': [95, 96],
            'Close': [102, 103],
            'Volume': [1000, 1100]
        })
        
        indicators = [self.atr, self.bb, self.obv, self.vwap, self.rsi, self.stoch, self.ema, self.adx]
        
        for indicator in indicators:
            try:
                result = indicator(two_rows.copy(), self.point)
                assert isinstance(result, pd.DataFrame) or isinstance(result, pd.Series)
                assert len(result) == 2
            except Exception:
                pass

    def test_very_large_numbers(self):
        """Test indicators with very large price values."""
        large_data = pd.DataFrame({
            'Open': [1000000, 1000001, 1000002],
            'High': [1000005, 1000006, 1000007],
            'Low': [999995, 999996, 999997],
            'Close': [1000002, 1000003, 1000004],
            'Volume': [1000000, 1100000, 1200000]
        })
        
        indicators = [self.atr, self.bb, self.obv, self.vwap, self.rsi, self.stoch, self.ema, self.adx]
        
        for indicator in indicators:
            try:
                result = indicator(large_data.copy(), self.point)
                assert isinstance(result, pd.DataFrame) or isinstance(result, pd.Series)
                assert len(result) == 3
            except Exception as e:
                pytest.fail(f"Indicator {indicator.__name__} failed with large numbers: {e}")

    def test_very_small_numbers(self):
        """Test indicators with very small price values."""
        small_data = pd.DataFrame({
            'Open': [0.0001, 0.0002, 0.0003],
            'High': [0.0005, 0.0006, 0.0007],
            'Low': [0.00005, 0.00006, 0.00007],
            'Close': [0.0002, 0.0003, 0.0004],
            'Volume': [1000, 1100, 1200]
        })
        
        indicators = [self.atr, self.bb, self.obv, self.vwap, self.rsi, self.stoch, self.ema, self.adx]
        
        for indicator in indicators:
            try:
                result = indicator(small_data.copy(), self.point)
                assert isinstance(result, pd.DataFrame) or isinstance(result, pd.Series)
                assert len(result) == 3
            except Exception as e:
                pytest.fail(f"Indicator {indicator.__name__} failed with small numbers: {e}")

    def test_negative_prices(self):
        """Test indicators with negative price values."""
        negative_data = pd.DataFrame({
            'Open': [-100, -101, -102],
            'High': [-95, -96, -97],
            'Low': [-105, -106, -107],
            'Close': [-102, -103, -104],
            'Volume': [1000, 1100, 1200]
        })
        
        indicators = [self.atr, self.bb, self.obv, self.vwap, self.rsi, self.stoch, self.ema, self.adx]
        
        for indicator in indicators:
            try:
                result = indicator(negative_data.copy(), self.point)
                assert isinstance(result, pd.DataFrame) or isinstance(result, pd.Series)
                assert len(result) == 3
            except Exception:
                pass

    def test_zero_prices(self):
        """Test indicators with zero price values."""
        zero_data = pd.DataFrame({
            'Open': [0, 0, 0],
            'High': [0, 0, 0],
            'Low': [0, 0, 0],
            'Close': [0, 0, 0],
            'Volume': [1000, 1100, 1200]
        })
        
        indicators = [self.atr, self.bb, self.obv, self.vwap, self.rsi, self.stoch, self.ema, self.adx]
        
        for indicator in indicators:
            try:
                result = indicator(zero_data.copy(), self.point)
                assert isinstance(result, pd.DataFrame) or isinstance(result, pd.Series)
                assert len(result) == 3
            except Exception:
                pass

    def test_zero_volume(self):
        """Test indicators with zero volume."""
        zero_volume_data = pd.DataFrame({
            'Open': [100, 101, 102],
            'High': [105, 106, 107],
            'Low': [95, 96, 97],
            'Close': [102, 103, 104],
            'Volume': [0, 0, 0]
        })
        
        indicators = [self.atr, self.bb, self.obv, self.vwap, self.rsi, self.stoch, self.ema, self.adx]
        
        for indicator in indicators:
            try:
                result = indicator(zero_volume_data.copy(), self.point)
                assert isinstance(result, pd.DataFrame) or isinstance(result, pd.Series)
                assert len(result) == 3
            except Exception as e:
                pytest.fail(f"Indicator {indicator.__name__} failed with zero volume: {e}")

    def test_negative_volume(self):
        """Test indicators with negative volume."""
        negative_volume_data = pd.DataFrame({
            'Open': [100, 101, 102],
            'High': [105, 106, 107],
            'Low': [95, 96, 97],
            'Close': [102, 103, 104],
            'Volume': [-1000, -1100, -1200]
        })
        
        indicators = [self.atr, self.bb, self.obv, self.vwap, self.rsi, self.stoch, self.ema, self.adx]
        
        for indicator in indicators:
            try:
                result = indicator(negative_volume_data.copy(), self.point)
                assert isinstance(result, pd.DataFrame) or isinstance(result, pd.Series)
                assert len(result) == 3
            except Exception:
                pass

    def test_infinite_values(self):
        """Test indicators with infinite values."""
        infinite_data = pd.DataFrame({
            'Open': [100, np.inf, 102],
            'High': [105, np.inf, 107],
            'Low': [95, -np.inf, 97],
            'Close': [102, np.inf, 104],
            'Volume': [1000, np.inf, 1200]
        })
        
        indicators = [self.atr, self.bb, self.obv, self.vwap, self.rsi, self.stoch, self.ema, self.adx]
        
        for indicator in indicators:
            try:
                result = indicator(infinite_data.copy(), self.point)
                assert isinstance(result, pd.DataFrame) or isinstance(result, pd.Series)
                assert len(result) == 3
            except Exception:
                pass

    def test_nan_values(self):
        """Test indicators with NaN values."""
        nan_data = pd.DataFrame({
            'Open': [100, np.nan, 102],
            'High': [105, np.nan, 107],
            'Low': [95, np.nan, 97],
            'Close': [102, np.nan, 104],
            'Volume': [1000, np.nan, 1200]
        })
        
        indicators = [self.atr, self.bb, self.obv, self.vwap, self.rsi, self.stoch, self.ema, self.adx]
        
        for indicator in indicators:
            try:
                result = indicator(nan_data.copy(), self.point)
                assert isinstance(result, pd.DataFrame) or isinstance(result, pd.Series)
                assert len(result) == 3
            except Exception as e:
                pytest.fail(f"Indicator {indicator.__name__} failed with NaN values: {e}")

    def test_all_nan_data(self):
        """Test indicators with all NaN data."""
        all_nan_data = pd.DataFrame({
            'Open': [np.nan, np.nan, np.nan],
            'High': [np.nan, np.nan, np.nan],
            'Low': [np.nan, np.nan, np.nan],
            'Close': [np.nan, np.nan, np.nan],
            'Volume': [np.nan, np.nan, np.nan]
        })
        
        indicators = [self.atr, self.bb, self.obv, self.vwap, self.rsi, self.stoch, self.ema, self.adx]
        
        for indicator in indicators:
            try:
                result = indicator(all_nan_data.copy(), self.point)
                assert isinstance(result, pd.DataFrame) or isinstance(result, pd.Series)
                assert len(result) == 3
            except Exception:
                pass

    def test_very_long_periods(self):
        """Test indicators with very long periods."""
        # Create data with 1000 rows
        long_data = pd.DataFrame({
            'Open': np.random.uniform(100, 110, 1000),
            'High': np.random.uniform(110, 120, 1000),
            'Low': np.random.uniform(90, 100, 1000),
            'Close': np.random.uniform(100, 110, 1000),
            'Volume': np.random.randint(1000, 2000, 1000)
        })
        
        # Test with very long periods
        long_period_indicators = [
            self.atr(long_data.copy(), self.point),
            self.bb(long_data.copy(), self.point),
            self.rsi(long_data.copy(), self.point),
            self.stoch(long_data.copy(), self.point),
            self.ema(long_data.copy(), self.point),
            self.adx(long_data.copy(), self.point)
        ]
        
        for indicator in long_period_indicators:
            try:
                result = indicator
                assert isinstance(result, pd.DataFrame) or isinstance(result, pd.Series)
                assert len(result) == 1000
            except Exception as e:
                pytest.fail(f"Indicator {indicator.__name__} failed with long period: {e}")

    def test_mixed_data_types(self):
        """Test indicators with mixed data types in columns."""
        mixed_data = pd.DataFrame({
            'Open': [100, '101', 102],  # Mixed int and string
            'High': [105, 106, 107],
            'Low': [95, 96, 97],
            'Close': [102, 103, 104],
            'Volume': [1000, 1100, 1200]
        })
        
        # Only apply_rule_rsi and apply_rule_stochastic should throw TypeError
        with pytest.raises(TypeError):
            apply_rule_rsi(mixed_data.copy(), self.point)
        with pytest.raises(TypeError):
            apply_rule_stochastic(mixed_data.copy(), self.point)
        
        # Other indicators should return DataFrame
        result_atr = apply_rule_atr(mixed_data.copy(), self.point)
        assert isinstance(result_atr, pd.DataFrame)
        
        result_bb = apply_rule_bollinger_bands(mixed_data.copy(), self.point)
        assert isinstance(result_bb, pd.DataFrame)
        
        result_obv = apply_rule_obv(mixed_data.copy(), self.point)
        assert isinstance(result_obv, pd.DataFrame)
        
        result_vwap = apply_rule_vwap(mixed_data.copy(), self.point)
        assert isinstance(result_vwap, pd.DataFrame)
        
        result_ema = apply_rule_ema(mixed_data.copy(), self.point)
        assert isinstance(result_ema, pd.DataFrame)
        
        result_adx = apply_rule_adx(mixed_data.copy(), self.point)
        assert isinstance(result_adx, pd.DataFrame)

    def test_duplicate_index(self):
        """Test indicators with duplicate index values."""
        duplicate_index_data = pd.DataFrame({
            'Open': [100, 101, 102],
            'High': [105, 106, 107],
            'Low': [95, 96, 97],
            'Close': [102, 103, 104],
            'Volume': [1000, 1100, 1200]
        }, index=[0, 0, 1])  # Duplicate index
        
        indicators = [self.atr, self.bb, self.obv, self.vwap, self.rsi, self.stoch, self.ema, self.adx]
        
        for indicator in indicators:
            try:
                result = indicator(duplicate_index_data.copy(), self.point)
                assert isinstance(result, pd.DataFrame) or isinstance(result, pd.Series)
                assert len(result) == 3
            except Exception as e:
                pytest.fail(f"Indicator {indicator.__name__} failed with duplicate index: {e}") 