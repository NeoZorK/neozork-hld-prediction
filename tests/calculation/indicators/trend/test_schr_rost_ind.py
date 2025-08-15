# -*- coding: utf-8 -*-
# tests/calculation/indicators/trend/test_schr_rost_ind.py

"""
Unit tests for SCHR_ROST indicator.
Tests all functionality including calculations, signals, and parameter handling.
"""

import unittest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import sys
import os

# Import using absolute imports
import src.calculation.indicators.trend.schr_rost_ind as schr_rost_module
from src.common.constants import NOTRADE, BUY, SELL

# Get module components
SpeedEnum = schr_rost_module.SpeedEnum
SPEED_VALUES = schr_rost_module.SPEED_VALUES
SPEED_NAMES = schr_rost_module.SPEED_NAMES
get_speed_period = schr_rost_module.get_speed_period
calculate_schr_rost = schr_rost_module.calculate_schr_rost
calculate_schr_rost_signals = schr_rost_module.calculate_schr_rost_signals
SCHRRostIndicator = schr_rost_module.SCHRRostIndicator
apply_rule_schr_rost = schr_rost_module.apply_rule_schr_rost


class TestSpeedEnum(unittest.TestCase):
    """Test SpeedEnum constants and values."""
    
    def test_speed_enum_values(self):
        """Test that SpeedEnum has correct values."""
        self.assertEqual(SpeedEnum.SNAIL, 0)
        self.assertEqual(SpeedEnum.TURTLE, 1)
        self.assertEqual(SpeedEnum.FROG, 2)
        self.assertEqual(SpeedEnum.MOUSE, 3)
        self.assertEqual(SpeedEnum.CAT, 4)
        self.assertEqual(SpeedEnum.RABBIT, 5)
        self.assertEqual(SpeedEnum.GEPARD, 6)
        self.assertEqual(SpeedEnum.SLOWEST, 7)
        self.assertEqual(SpeedEnum.SLOW, 8)
        self.assertEqual(SpeedEnum.NORMAL, 9)
        self.assertEqual(SpeedEnum.FAST, 10)
        self.assertEqual(SpeedEnum.FUTURE, 11)
    
    def test_speed_values_dict(self):
        """Test that SPEED_VALUES contains all enum values."""
        self.assertEqual(SPEED_VALUES[SpeedEnum.SNAIL], 1000)
        self.assertEqual(SPEED_VALUES[SpeedEnum.TURTLE], 500)
        self.assertEqual(SPEED_VALUES[SpeedEnum.FROG], 200)
        self.assertEqual(SPEED_VALUES[SpeedEnum.MOUSE], 100)
        self.assertEqual(SPEED_VALUES[SpeedEnum.CAT], 50)
        self.assertEqual(SPEED_VALUES[SpeedEnum.RABBIT], 30)
        self.assertEqual(SPEED_VALUES[SpeedEnum.GEPARD], 10)
        self.assertEqual(SPEED_VALUES[SpeedEnum.SLOWEST], 5)
        self.assertEqual(SPEED_VALUES[SpeedEnum.SLOW], 2)
        self.assertEqual(SPEED_VALUES[SpeedEnum.NORMAL], 1.01)
        self.assertEqual(SPEED_VALUES[SpeedEnum.FAST], 0.683)
        self.assertEqual(SPEED_VALUES[SpeedEnum.FUTURE], 0.501)
    
    def test_speed_names_dict(self):
        """Test that SPEED_NAMES contains all enum names."""
        self.assertEqual(SPEED_NAMES[SpeedEnum.SNAIL], "Snail")
        self.assertEqual(SPEED_NAMES[SpeedEnum.TURTLE], "Turtle")
        self.assertEqual(SPEED_NAMES[SpeedEnum.FROG], "Frog")
        self.assertEqual(SPEED_NAMES[SpeedEnum.MOUSE], "Mouse")
        self.assertEqual(SPEED_NAMES[SpeedEnum.CAT], "Cat")
        self.assertEqual(SPEED_NAMES[SpeedEnum.RABBIT], "Rabbit")
        self.assertEqual(SPEED_NAMES[SpeedEnum.GEPARD], "Gepard")
        self.assertEqual(SPEED_NAMES[SpeedEnum.SLOWEST], "Slowest")
        self.assertEqual(SPEED_NAMES[SpeedEnum.SLOW], "Slow")
        self.assertEqual(SPEED_NAMES[SpeedEnum.NORMAL], "Normal")
        self.assertEqual(SPEED_NAMES[SpeedEnum.FAST], "Fast")
        self.assertEqual(SPEED_NAMES[SpeedEnum.FUTURE], "Future")


class TestGetSpeedPeriod(unittest.TestCase):
    """Test get_speed_period function."""
    
    def test_get_speed_period_enum(self):
        """Test get_speed_period with enum values."""
        self.assertEqual(get_speed_period(SpeedEnum.SNAIL), 1000)
        self.assertEqual(get_speed_period(SpeedEnum.FUTURE), 0.501)
        self.assertEqual(get_speed_period(SpeedEnum.NORMAL), 1.01)
    
    def test_get_speed_period_string(self):
        """Test get_speed_period with string names."""
        self.assertEqual(get_speed_period("snail"), 1000)
        self.assertEqual(get_speed_period("FUTURE"), 0.501)
        self.assertEqual(get_speed_period("Normal"), 1.01)
        self.assertEqual(get_speed_period("fast"), 0.683)
    
    def test_get_speed_period_invalid(self):
        """Test get_speed_period with invalid values."""
        # Invalid enum should default to NORMAL
        self.assertEqual(get_speed_period(999), 1.01)
        # Invalid string should default to NORMAL
        self.assertEqual(get_speed_period("invalid"), 1.01)


class TestCalculateSCHRRost(unittest.TestCase):
    """Test calculate_schr_rost function."""
    
    def setUp(self):
        """Set up test data."""
        dates = pd.date_range('2020-01-01', periods=10, freq='D')
        self.df = pd.DataFrame({
            'Open': [1.0, 1.1, 1.05, 1.15, 1.12, 1.18, 1.16, 1.20, 1.17, 1.22],
            'High': [1.12, 1.15, 1.08, 1.18, 1.14, 1.20, 1.18, 1.22, 1.19, 1.24],
            'Low': [0.98, 1.08, 1.02, 1.12, 1.10, 1.16, 1.14, 1.18, 1.15, 1.20],
            'Close': [1.05, 1.12, 1.06, 1.16, 1.13, 1.19, 1.17, 1.21, 1.18, 1.23],
            'Volume': [100, 150, 120, 180, 140, 200, 160, 220, 180, 240]
        }, index=dates)
    
    def test_calculate_schr_rost_basic(self):
        """Test basic SCHR Rost calculation."""
        result = calculate_schr_rost(self.df)
        
        self.assertIsInstance(result, pd.Series)
        self.assertEqual(len(result), len(self.df))
        self.assertEqual(result.index[0], self.df.index[0])
        self.assertEqual(result.index[-1], self.df.index[-1])
        
        # First value should be the first Open price
        self.assertEqual(result.iloc[0], self.df['Open'].iloc[0])
        
        # All values should be finite
        self.assertTrue(np.all(np.isfinite(result)))
    
    def test_calculate_schr_rost_different_speeds(self):
        """Test SCHR Rost calculation with different speed periods."""
        speeds = [SpeedEnum.SNAIL, SpeedEnum.NORMAL, SpeedEnum.FAST, SpeedEnum.FUTURE]
        
        for speed in speeds:
            speed_value = SPEED_VALUES[speed]
            result = calculate_schr_rost(self.df, speed_value)
            
            self.assertIsInstance(result, pd.Series)
            self.assertEqual(len(result), len(self.df))
            self.assertTrue(np.all(np.isfinite(result)))
    
    def test_calculate_schr_rost_insufficient_data(self):
        """Test SCHR Rost calculation with insufficient data."""
        # Single row DataFrame
        single_df = self.df.iloc[:1]
        result = calculate_schr_rost(single_df)
        
        self.assertIsInstance(result, pd.Series)
        self.assertEqual(len(result), 1)
        self.assertTrue(result.isna().all())
    
    def test_calculate_schr_rost_empty_data(self):
        """Test SCHR Rost calculation with empty DataFrame."""
        empty_df = pd.DataFrame(columns=['Open', 'High', 'Low', 'Close', 'Volume'])
        result = calculate_schr_rost(empty_df)
        
        self.assertIsInstance(result, pd.Series)
        self.assertEqual(len(result), 0)


class TestCalculateSCHRRostSignals(unittest.TestCase):
    """Test calculate_schr_rost_signals function."""
    
    def setUp(self):
        """Set up test data."""
        dates = pd.date_range('2020-01-01', periods=10, freq='D')
        self.rost_values = pd.Series([1.0, 1.1, 1.05, 1.15, 1.12, 1.18, 1.16, 1.20, 1.17, 1.22], index=dates)
    
    def test_calculate_signals_basic(self):
        """Test basic signal calculation."""
        prediction, direction, signal = calculate_schr_rost_signals(self.rost_values)
        
        self.assertIsInstance(prediction, pd.Series)
        self.assertIsInstance(direction, pd.Series)
        self.assertIsInstance(signal, pd.Series)
        
        self.assertEqual(len(prediction), len(self.rost_values))
        self.assertEqual(len(direction), len(self.rost_values))
        self.assertEqual(len(signal), len(self.rost_values))
        
        # First values should be 0/NOTRADE
        self.assertEqual(prediction.iloc[0], 0)
        self.assertEqual(direction.iloc[0], NOTRADE)
        self.assertEqual(signal.iloc[0], NOTRADE)
    
    def test_calculate_signals_faster_reverse(self):
        """Test signal calculation with faster reverse enabled."""
        # Create values that stay the same for faster reverse test
        same_values = pd.Series([1.0, 1.0, 1.1, 1.1, 1.05, 1.05, 1.15, 1.15], 
                               index=pd.date_range('2020-01-01', periods=8, freq='D'))
        
        prediction, direction, signal = calculate_schr_rost_signals(same_values, faster_reverse=True)
        
        # Check that signals are generated
        self.assertTrue(any(signal != NOTRADE))
    
    def test_calculate_signals_no_faster_reverse(self):
        """Test signal calculation without faster reverse."""
        same_values = pd.Series([1.0, 1.0, 1.1, 1.1, 1.05, 1.05, 1.15, 1.15], 
                               index=pd.date_range('2020-01-01', periods=8, freq='D'))
        
        prediction, direction, signal = calculate_schr_rost_signals(same_values, faster_reverse=False)
        
        # Should have fewer signals without faster reverse
        self.assertTrue(len([s for s in signal if s != NOTRADE]) <= 
                       len([s for s in calculate_schr_rost_signals(same_values, True)[2] if s != NOTRADE]))


class TestSCHRRostIndicator(unittest.TestCase):
    """Test SCHRRostIndicator class."""
    
    def setUp(self):
        """Set up test data."""
        dates = pd.date_range('2020-01-01', periods=10, freq='D')
        self.df = pd.DataFrame({
            'Open': [1.0, 1.1, 1.05, 1.15, 1.12, 1.18, 1.16, 1.20, 1.17, 1.22],
            'High': [1.12, 1.15, 1.08, 1.18, 1.14, 1.20, 1.18, 1.22, 1.19, 1.24],
            'Low': [0.98, 1.08, 1.02, 1.12, 1.10, 1.16, 1.14, 1.18, 1.15, 1.20],
            'Close': [1.05, 1.12, 1.06, 1.16, 1.13, 1.19, 1.17, 1.21, 1.18, 1.23],
            'Volume': [100, 150, 120, 180, 140, 200, 160, 220, 180, 240]
        }, index=dates)
    
    def test_indicator_initialization(self):
        """Test indicator initialization."""
        indicator = SCHRRostIndicator()
        
        self.assertEqual(indicator.speed_period, SPEED_VALUES[SpeedEnum.FUTURE])
        self.assertFalse(indicator.faster_reverse)
        self.assertEqual(indicator.price_type.value, 'open')
    
    def test_indicator_initialization_custom_params(self):
        """Test indicator initialization with custom parameters."""
        indicator = SCHRRostIndicator(
            speed_period=SpeedEnum.NORMAL,
            faster_reverse=True,
            price_type='close'
        )
        
        self.assertEqual(indicator.speed_period, SPEED_VALUES[SpeedEnum.NORMAL])
        self.assertTrue(indicator.faster_reverse)
        self.assertEqual(indicator.price_type.value, 'close')
    
    def test_calculate_method(self):
        """Test calculate method."""
        indicator = SCHRRostIndicator()
        result = indicator.calculate(self.df)
        
        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(len(result), len(self.df))
        
        # Check that required columns are added
        required_cols = ['schr_rost', 'schr_rost_prediction', 'schr_rost_direction', 'schr_rost_signal']
        for col in required_cols:
            self.assertIn(col, result.columns)
        
        # Check that original columns are preserved
        original_cols = ['Open', 'High', 'Low', 'Close', 'Volume']
        for col in original_cols:
            self.assertIn(col, result.columns)
    
    def test_apply_rule_method(self):
        """Test apply_rule method."""
        indicator = SCHRRostIndicator()
        result = indicator.apply_rule(self.df, point=0.00001)
        
        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(len(result), len(self.df))
        
        # Check that rule output columns are present
        rule_cols = ['PPrice1', 'PColor1', 'PPrice2', 'PColor2', 'Direction', 'Diff']
        for col in rule_cols:
            self.assertIn(col, result.columns)
        
        # Check that indicator columns are present
        indicator_cols = ['schr_rost', 'schr_rost_prediction', 'schr_rost_direction', 'schr_rost_signal']
        for col in indicator_cols:
            self.assertIn(col, result.columns)
    
    def test_validate_data(self):
        """Test data validation."""
        indicator = SCHRRostIndicator()
        
        # Valid data
        self.assertTrue(indicator.validate_data(self.df, min_periods=2))
        
        # Invalid data - missing columns
        invalid_df = self.df.drop(columns=['Open'])
        self.assertFalse(indicator.validate_data(invalid_df, min_periods=2))
        
        # Invalid data - insufficient periods
        short_df = self.df.iloc[:1]
        self.assertFalse(indicator.validate_data(short_df, min_periods=2))


class TestApplyRuleSCHRRost(unittest.TestCase):
    """Test apply_rule_schr_rost function."""
    
    def setUp(self):
        """Set up test data."""
        dates = pd.date_range('2020-01-01', periods=10, freq='D')
        self.df = pd.DataFrame({
            'Open': [1.0, 1.1, 1.05, 1.15, 1.12, 1.18, 1.16, 1.20, 1.17, 1.22],
            'High': [1.12, 1.15, 1.08, 1.18, 1.14, 1.20, 1.18, 1.22, 1.19, 1.24],
            'Low': [0.98, 1.08, 1.02, 1.12, 1.10, 1.16, 1.14, 1.18, 1.15, 1.20],
            'Close': [1.05, 1.12, 1.06, 1.16, 1.13, 1.19, 1.17, 1.21, 1.18, 1.23],
            'Volume': [100, 150, 120, 180, 140, 200, 160, 220, 180, 240]
        }, index=dates)
    
    def test_apply_rule_basic(self):
        """Test basic rule application."""
        result = apply_rule_schr_rost(self.df, point=0.00001)
        
        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(len(result), len(self.df))
        
        # Check that all required columns are present
        required_cols = ['PPrice1', 'PColor1', 'PPrice2', 'PColor2', 'Direction', 'Diff']
        for col in required_cols:
            self.assertIn(col, result.columns)
    
    def test_apply_rule_with_parameters(self):
        """Test rule application with different parameters."""
        # Test with different speed periods
        for speed in [SpeedEnum.SNAIL, SpeedEnum.NORMAL, SpeedEnum.FAST]:
            result = apply_rule_schr_rost(self.df, point=0.00001, speed_period=speed)
            self.assertIsInstance(result, pd.DataFrame)
            self.assertEqual(len(result), len(self.df))
        
        # Test with faster reverse
        result = apply_rule_schr_rost(self.df, point=0.00001, faster_reverse=True)
        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(len(result), len(self.df))
        
        # Test with different price type
        result = apply_rule_schr_rost(self.df, point=0.00001, price_type='close')
        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(len(result), len(self.df))
    
    def test_apply_rule_large_dataset(self):
        """Test rule application with large dataset."""
        # Create larger dataset
        dates = pd.date_range('2020-01-01', periods=1000, freq='H')
        large_df = pd.DataFrame({
            'Open': np.random.uniform(1.0, 1.5, 1000),
            'High': np.random.uniform(1.1, 1.6, 1000),
            'Low': np.random.uniform(0.9, 1.4, 1000),
            'Close': np.random.uniform(1.0, 1.5, 1000),
            'Volume': np.random.randint(100, 1000, 1000)
        }, index=dates)
        
        result = apply_rule_schr_rost(large_df, point=0.00001)
        
        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(len(result), len(large_df))
        
        # Check that calculations completed successfully
        self.assertTrue(np.all(np.isfinite(result['schr_rost'].dropna())))


if __name__ == '__main__':
    unittest.main()
