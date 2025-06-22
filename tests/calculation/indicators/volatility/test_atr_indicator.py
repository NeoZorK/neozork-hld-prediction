# tests/calculation/indicators/volatility/test_atr_indicator.py

import pytest
import pandas as pd
import numpy as np
from unittest.mock import patch, MagicMock
from src.calculation.indicators.volatility.atr_ind import calculate_atr, apply_rule_atr


class TestATRIndicator:
    """Test cases for ATR (Average True Range) indicator."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.atr = calculate_atr
        
        # Create sample data
        dates = pd.date_range('2023-01-01', periods=30, freq='D')
        self.sample_data = pd.DataFrame({
            'Open': [100 + i * 0.1 for i in range(30)],
            'High': [102 + i * 0.1 for i in range(30)],
            'Low': [98 + i * 0.1 for i in range(30)],
            'Close': [101 + i * 0.1 for i in range(30)],
            'Volume': [1000 + i * 10 for i in range(30)]
        }, index=dates)
        
        # Add some volatility
        self.sample_data.loc[10:15, 'High'] += 5
        self.sample_data.loc[10:15, 'Low'] -= 3
        
    def test_atr_calculation_basic(self):
        """Test basic ATR calculation."""
        result = self.atr(self.sample_data)
        
        assert 'ATR' in result
        assert len(result['ATR']) == len(self.sample_data)
        assert not result['ATR'].isna().all()
        
        # ATR should be positive
        atr_values = result['ATR'].dropna()
        assert (atr_values > 0).all()
        
    def test_atr_calculation_with_custom_period(self):
        """Test ATR calculation with custom period."""
        result = self.atr(self.sample_data, period=10)
        
        assert 'ATR' in result
        # First 9 values should be NaN (period - 1)
        assert result['ATR'].iloc[:9].isna().all()
        assert not result['ATR'].iloc[9:].isna().all()
        
    def test_atr_with_invalid_period(self):
        """Test ATR with invalid period."""
        with pytest.raises(ValueError, match="Period must be positive"):
            self.atr(self.sample_data, period=0)
            
        with pytest.raises(ValueError, match="Period must be positive"):
            self.atr(self.sample_data, period=-1)
            
    def test_atr_empty_dataframe(self):
        """Test ATR with empty DataFrame."""
        empty_df = pd.DataFrame(columns=['Open', 'High', 'Low', 'Close', 'Volume'])
        result = self.atr(empty_df)
        
        assert 'ATR' in result
        assert len(result['ATR']) == 0
        
    def test_atr_insufficient_data(self):
        """Test ATR with insufficient data."""
        small_df = self.sample_data.head(5)  # Less than period
        result = self.atr(small_df, period=14)
        
        assert 'ATR' in result
        # All values should be NaN for insufficient data
        assert result['ATR'].isna().all()
        
    def test_atr_parameter_validation(self):
        """Test ATR parameter validation."""
        # Test with valid parameters
        result = self.atr(self.sample_data, period=20)
        assert 'ATR' in result
        
        # Test with float period (should be converted to int)
        result = self.atr(self.sample_data, period=20.5)
        assert 'ATR' in result
        
    def test_atr_period_impact(self):
        """Test the impact of period on ATR calculation."""
        result_short = self.atr(self.sample_data, period=5)
        result_long = self.atr(self.sample_data, period=20)
        
        # Longer period should result in smoother ATR
        atr_short = result_short['ATR'].dropna()
        atr_long = result_long['ATR'].dropna()
        
        # Longer period ATR should be less volatile
        assert atr_long.std() <= atr_short.std()
        
    def test_atr_with_constant_data(self):
        """Test ATR with constant price data."""
        constant_data = self.sample_data.copy()
        constant_data['High'] = 100
        constant_data['Low'] = 100
        constant_data['Close'] = 100
        constant_data['Open'] = 100
        
        result = self.atr(constant_data)
        atr_values = result['ATR'].dropna()
        
        # ATR should be very small for constant data
        assert (atr_values <= 0.01).all()
        
    def test_atr_with_extreme_volatility(self):
        """Test ATR with extreme volatility."""
        volatile_data = self.sample_data.copy()
        volatile_data.loc[10:15, 'High'] += 50
        volatile_data.loc[10:15, 'Low'] -= 30
        
        result = self.atr(volatile_data)
        atr_values = result['ATR'].dropna()
        
        # ATR should be higher for volatile data
        assert atr_values.max() > 10
        
    def test_atr_edge_cases(self):
        """Test ATR edge cases."""
        # Test with NaN values
        data_with_nan = self.sample_data.copy()
        data_with_nan.loc[5, 'High'] = np.nan
        
        result = self.atr(data_with_nan)
        assert 'ATR' in result
        
        # Test with zero values
        data_with_zero = self.sample_data.copy()
        data_with_zero.loc[5, 'Low'] = 0
        
        result = self.atr(data_with_zero)
        assert 'ATR' in result
        
    def test_atr_apply_rule(self):
        """Test ATR apply_rule function."""
        result = apply_rule_atr(self.sample_data, point=0.01)
        
        assert 'ATR' in result
        assert 'ATR_Signal' in result
        assert 'Direction' in result
        assert 'Diff' in result
        
        # Check signal values
        signals = result['ATR_Signal'].dropna()
        assert signals.isin(['BUY', 'SELL', 'NOTRADE']).all()
        
    def test_atr_performance(self):
        """Test ATR calculation performance."""
        large_data = pd.DataFrame({
            'Open': np.random.uniform(100, 200, 10000),
            'High': np.random.uniform(200, 300, 10000),
            'Low': np.random.uniform(50, 100, 10000),
            'Close': np.random.uniform(100, 200, 10000),
            'Volume': np.random.uniform(1000, 5000, 10000)
        })
        
        import time
        start_time = time.time()
        result = self.atr(large_data)
        end_time = time.time()
        
        # Should complete within reasonable time (less than 1 second)
        assert end_time - start_time < 1.0
        assert 'ATR' in result 