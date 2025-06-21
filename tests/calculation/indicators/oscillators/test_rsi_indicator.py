# -*- coding: utf-8 -*-
# tests/calculation/indicators/oscillators/test_rsi_indicator.py

import pytest
import pandas as pd
import numpy as np
from unittest.mock import patch, MagicMock
from src.calculation.indicators.oscillators.rsi_ind import (
    calculate_rsi, 
    calculate_rsi_signals, 
    apply_rule_rsi, 
    PriceType
)
from src.common.constants import NOTRADE, BUY, SELL


class TestRSIIndicator:
    """Test cases for RSI (Relative Strength Index) indicator."""

    def setup_method(self):
        """Set up test data."""
        self.sample_data = pd.DataFrame({
            'Open': [100, 101, 102, 103, 104, 105, 106, 107, 108, 109],
            'High': [102, 103, 104, 105, 106, 107, 108, 109, 110, 111],
            'Low': [99, 100, 101, 102, 103, 104, 105, 106, 107, 108],
            'Close': [101, 102, 103, 104, 105, 106, 107, 108, 109, 110],
            'Volume': [1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800, 1900]
        })

    def test_calculate_rsi_basic(self):
        """Test basic RSI calculation."""
        price_series = self.sample_data['Close']
        result = calculate_rsi(price_series, period=14)
        
        assert isinstance(result, pd.Series)
        assert len(result) == len(price_series)
        assert not result.isna().all()  # Should have some valid values

    def test_calculate_rsi_different_periods(self):
        """Test RSI calculation with different periods."""
        price_series = self.sample_data['Close']
        periods = [5, 10, 14, 20]
        
        for period in periods:
            result = calculate_rsi(price_series, period=period)
            assert isinstance(result, pd.Series)
            assert len(result) == len(price_series)

    def test_calculate_rsi_invalid_period(self):
        """Test RSI calculation with invalid period."""
        price_series = self.sample_data['Close']
        
        with pytest.raises(ValueError):
            calculate_rsi(price_series, period=0)
        
        with pytest.raises(ValueError):
            calculate_rsi(price_series, period=-1)

    def test_calculate_rsi_insufficient_data(self):
        """Test RSI calculation with insufficient data."""
        short_data = pd.Series([100, 101, 102])  # Only 3 points
        
        with patch('src.calculation.indicators.oscillators.rsi_ind.logger') as mock_logger:
            result = calculate_rsi(short_data, period=14)
            assert isinstance(result, pd.Series)
            assert len(result) == len(short_data)
            mock_logger.print_warning.assert_called()

    def test_calculate_rsi_with_nan_values(self):
        """Test RSI calculation with NaN values."""
        data_with_nan = self.sample_data['Close'].copy()
        data_with_nan.loc[2] = np.nan
        
        result = calculate_rsi(data_with_nan, period=14)
        assert isinstance(result, pd.Series)
        assert len(result) == len(data_with_nan)

    def test_calculate_rsi_signals_basic(self):
        """Test basic RSI signal calculation."""
        rsi_values = pd.Series([20, 30, 50, 70, 80])
        result = calculate_rsi_signals(rsi_values)
        
        assert isinstance(result, pd.Series)
        assert len(result) == len(rsi_values)
        assert result.iloc[0] == BUY  # 20 <= 30 (oversold)
        assert result.iloc[1] == BUY  # 30 <= 30 (oversold)
        assert result.iloc[2] == NOTRADE  # 50 between levels
        assert result.iloc[3] == SELL  # 70 >= 70 (overbought)
        assert result.iloc[4] == SELL  # 80 >= 70 (overbought)

    def test_calculate_rsi_signals_custom_levels(self):
        """Test RSI signal calculation with custom levels."""
        rsi_values = pd.Series([15, 25, 50, 75, 85])
        result = calculate_rsi_signals(rsi_values, overbought=80, oversold=20)
        
        assert isinstance(result, pd.Series)
        assert len(result) == len(rsi_values)
        assert result.iloc[0] == BUY  # 15 <= 20 (oversold)
        assert result.iloc[1] == NOTRADE  # 25 between levels
        assert result.iloc[2] == NOTRADE  # 50 between levels
        assert result.iloc[3] == NOTRADE  # 75 between levels
        assert result.iloc[4] == SELL  # 85 >= 80 (overbought)

    def test_calculate_rsi_signals_empty_series(self):
        """Test RSI signal calculation with empty series."""
        empty_series = pd.Series(dtype=float)
        result = calculate_rsi_signals(empty_series)
        
        assert isinstance(result, pd.Series)
        assert len(result) == 0

    def test_apply_rule_rsi_basic(self):
        """Test basic RSI rule application."""
        result = apply_rule_rsi(
            self.sample_data, 
            point=0.01,
            rsi_period=14,
            overbought=70,
            oversold=30,
            price_type=PriceType.CLOSE
        )
        
        assert 'RSI' in result.columns
        assert 'RSI_Signal' in result.columns
        assert 'RSI_Price_Type' in result.columns
        assert 'PPrice1' in result.columns
        assert 'PPrice2' in result.columns
        assert 'PColor1' in result.columns
        assert 'PColor2' in result.columns
        assert 'Direction' in result.columns
        assert 'Diff' in result.columns
        assert len(result) == len(self.sample_data)

    def test_apply_rule_rsi_with_open_price(self):
        """Test RSI rule application using open price."""
        result = apply_rule_rsi(
            self.sample_data, 
            point=0.01,
            rsi_period=14,
            overbought=70,
            oversold=30,
            price_type=PriceType.OPEN
        )
        
        assert 'RSI' in result.columns
        assert 'RSI_Price_Type' in result.columns
        assert result['RSI_Price_Type'].iloc[0] == 'Open'

    def test_apply_rule_rsi_with_close_price(self):
        """Test RSI rule application using close price."""
        result = apply_rule_rsi(
            self.sample_data, 
            point=0.01,
            rsi_period=14,
            overbought=70,
            oversold=30,
            price_type=PriceType.CLOSE
        )
        
        assert 'RSI' in result.columns
        assert 'RSI_Price_Type' in result.columns
        assert result['RSI_Price_Type'].iloc[0] == 'Close'

    def test_apply_rule_rsi_different_parameters(self):
        """Test RSI rule application with different parameters."""
        periods = [5, 10, 14]
        overbought_levels = [60, 70, 80]
        oversold_levels = [20, 30, 40]
        
        for period in periods:
            for overbought in overbought_levels:
                for oversold in oversold_levels:
                    if oversold < overbought:  # Valid combination
                        result = apply_rule_rsi(
                            self.sample_data, 
                            point=0.01,
                            rsi_period=period,
                            overbought=overbought,
                            oversold=oversold,
                            price_type=PriceType.CLOSE
                        )
                        
                        assert 'RSI' in result.columns
                        assert 'RSI_Signal' in result.columns
                        assert len(result) == len(self.sample_data)

    def test_apply_rule_rsi_support_resistance_calculation(self):
        """Test RSI support and resistance level calculation."""
        result = apply_rule_rsi(
            self.sample_data, 
            point=0.01,
            rsi_period=14,
            overbought=70,
            oversold=30,
            price_type=PriceType.CLOSE
        )
        
        # Check support levels (PPrice1)
        assert 'PPrice1' in result.columns
        assert 'PColor1' in result.columns
        assert all(result['PColor1'] == BUY)
        
        # Check resistance levels (PPrice2)
        assert 'PPrice2' in result.columns
        assert 'PColor2' in result.columns
        assert all(result['PColor2'] == SELL)

    def test_apply_rule_rsi_direction_and_diff(self):
        """Test RSI direction and difference calculation."""
        result = apply_rule_rsi(
            self.sample_data, 
            point=0.01,
            rsi_period=14,
            overbought=70,
            oversold=30,
            price_type=PriceType.CLOSE
        )
        
        assert 'Direction' in result.columns
        assert 'Diff' in result.columns
        
        # Direction should contain trading signals
        valid_signals = [NOTRADE, BUY, SELL]
        assert all(signal in valid_signals for signal in result['Direction'].dropna())
        
        # Diff should contain RSI values
        assert 'Diff' in result.columns
        rsi_values = result['Diff'].dropna()
        assert len(rsi_values) > 0

    def test_apply_rule_rsi_empty_dataframe(self):
        """Test RSI rule application with empty dataframe."""
        empty_df = pd.DataFrame()
        
        with pytest.raises(KeyError):  # Missing required columns
            apply_rule_rsi(
                empty_df, 
                point=0.01,
                rsi_period=14,
                overbought=70,
                oversold=30,
                price_type=PriceType.CLOSE
            )

    def test_apply_rule_rsi_missing_columns(self):
        """Test RSI rule application with missing required columns."""
        incomplete_df = self.sample_data.drop(columns=['Close'])
        
        with pytest.raises(KeyError):  # Missing Close column
            apply_rule_rsi(
                incomplete_df, 
                point=0.01,
                rsi_period=14,
                overbought=70,
                oversold=30,
                price_type=PriceType.CLOSE
            )

    def test_apply_rule_rsi_with_nan_values(self):
        """Test RSI rule application with NaN values in data."""
        data_with_nan = self.sample_data.copy()
        data_with_nan.loc[2, 'Close'] = np.nan
        
        result = apply_rule_rsi(
            data_with_nan, 
            point=0.01,
            rsi_period=14,
            overbought=70,
            oversold=30,
            price_type=PriceType.CLOSE
        )
        
        assert 'RSI' in result.columns
        assert len(result) == len(data_with_nan)

    def test_apply_rule_rsi_volatility_factor(self):
        """Test RSI volatility factor in support/resistance calculation."""
        result = apply_rule_rsi(
            self.sample_data, 
            point=0.01,
            rsi_period=14,
            overbought=70,
            oversold=30,
            price_type=PriceType.CLOSE
        )
        
        # Support levels should be lower than open prices (2% volatility factor)
        support_levels = result['PPrice1']
        open_prices = self.sample_data['Open']
        
        # Check that support levels are approximately 2% below open prices
        for i in range(len(support_levels)):
            if not pd.isna(support_levels.iloc[i]) and not pd.isna(open_prices.iloc[i]):
                expected_support = open_prices.iloc[i] * 0.98  # 1 - 0.02
                assert abs(support_levels.iloc[i] - expected_support) < 0.01

    def test_apply_rule_rsi_edge_cases(self):
        """Test RSI rule application with edge cases."""
        # Test with very small dataset
        small_data = self.sample_data.head(3)
        
        with patch('src.calculation.indicators.oscillators.rsi_ind.logger') as mock_logger:
            result = apply_rule_rsi(
                small_data, 
                point=0.01,
                rsi_period=14,
                overbought=70,
                oversold=30,
                price_type=PriceType.CLOSE
            )
            
            assert 'RSI' in result.columns
            assert len(result) == len(small_data)

    def test_apply_rule_rsi_consistency(self):
        """Test RSI rule application consistency."""
        # Run multiple times with same parameters
        results = []
        for _ in range(3):
            result = apply_rule_rsi(
                self.sample_data, 
                point=0.01,
                rsi_period=14,
                overbought=70,
                oversold=30,
                price_type=PriceType.CLOSE
            )
            results.append(result)
        
        # All results should be identical
        for i in range(1, len(results)):
            pd.testing.assert_frame_equal(results[0], results[i])

    def test_apply_rule_rsi_performance(self):
        """Test RSI rule application performance."""
        import time
        
        # Create larger dataset
        large_data = pd.DataFrame({
            'Open': np.random.uniform(100, 200, 1000),
            'High': np.random.uniform(200, 300, 1000),
            'Low': np.random.uniform(50, 100, 1000),
            'Close': np.random.uniform(100, 200, 1000),
            'Volume': np.random.uniform(1000, 10000, 1000)
        })
        
        start_time = time.time()
        result = apply_rule_rsi(
            large_data, 
            point=0.01,
            rsi_period=14,
            overbought=70,
            oversold=30,
            price_type=PriceType.CLOSE
        )
        end_time = time.time()
        
        assert 'RSI' in result.columns
        assert len(result) == len(large_data)
        assert (end_time - start_time) < 1.0  # Should complete within 1 second

    def test_price_type_enum(self):
        """Test PriceType enum functionality."""
        assert PriceType.OPEN.value == "open"
        assert PriceType.CLOSE.value == "close"
        assert PriceType.OPEN != PriceType.CLOSE

    def test_rsi_mathematical_properties(self):
        """Test RSI mathematical properties."""
        # Create data with known pattern
        increasing_data = pd.Series([100, 101, 102, 103, 104, 105, 106, 107, 108, 109])
        rsi_increasing = calculate_rsi(increasing_data, period=5)
        
        # RSI should be between 0 and 100
        valid_rsi = rsi_increasing.dropna()
        assert all(0 <= rsi <= 100 for rsi in valid_rsi if not pd.isna(rsi))
        
        # Create decreasing data
        decreasing_data = pd.Series([109, 108, 107, 106, 105, 104, 103, 102, 101, 100])
        rsi_decreasing = calculate_rsi(decreasing_data, period=5)
        
        # RSI should be between 0 and 100
        valid_rsi = rsi_decreasing.dropna()
        assert all(0 <= rsi <= 100 for rsi in valid_rsi if not pd.isna(rsi))

    def test_rsi_signal_logic(self):
        """Test RSI signal logic thoroughly."""
        # Test exact boundary conditions
        rsi_values = pd.Series([29.9, 30.0, 30.1, 69.9, 70.0, 70.1])
        signals = calculate_rsi_signals(rsi_values, overbought=70, oversold=30)
        
        assert signals.iloc[0] == BUY    # 29.9 <= 30
        assert signals.iloc[1] == BUY    # 30.0 <= 30
        assert signals.iloc[2] == NOTRADE  # 30.1 > 30
        assert signals.iloc[3] == NOTRADE  # 69.9 < 70
        assert signals.iloc[4] == SELL   # 70.0 >= 70
        assert signals.iloc[5] == SELL   # 70.1 >= 70 