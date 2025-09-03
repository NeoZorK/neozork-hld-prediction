# -*- coding: utf-8 -*-
"""
Tests for Error Handling Module

This module tests the error handling functionality for different indicator groups.
"""

import pytest
import pandas as pd
import numpy as np
from src.calculation.error_handling import (
    OscillatorErrorHandler,
    TrendErrorHandler,
    MomentumErrorHandler,
    VolumeErrorHandler,
    VolatilityErrorHandler,
    SupportResistanceErrorHandler,
    PredictiveErrorHandler,
    ProbabilityErrorHandler,
    SentimentErrorHandler
)


class TestOscillatorErrorHandler:
    """Test oscillator error handler functionality."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.handler = OscillatorErrorHandler('RSI')
        
        # Create test data with enough rows for validation (minimum 50)
        np.random.seed(42)
        dates = pd.date_range('2023-01-01', periods=60, freq='D')
        self.valid_data = pd.DataFrame({
            'Open': np.random.uniform(1.0, 2.0, 60),
            'High': np.random.uniform(1.1, 2.1, 60),
            'Low': np.random.uniform(0.9, 1.9, 60),
            'Close': np.random.uniform(1.0, 2.0, 60)
        }, index=dates)
    
    def test_validate_parameters_valid(self):
        """Test parameter validation with valid parameters."""
        params = {'period': 14}
        assert self.handler.validate_parameters(params) is True
        assert not self.handler.has_errors()
    
    def test_validate_parameters_invalid_period(self):
        """Test parameter validation with invalid period."""
        params = {'period': 0}
        assert self.handler.validate_parameters(params) is False
        assert self.handler.has_errors()
    
    def test_validate_data_valid(self):
        """Test data validation with valid data."""
        assert self.handler.validate_data(self.valid_data) is True
        assert not self.handler.has_errors()
    
    def test_validate_data_missing_columns(self):
        """Test data validation with missing columns."""
        invalid_data = pd.DataFrame({'Close': [1.0, 1.1, 1.2]})
        assert self.handler.validate_data(invalid_data) is False
        assert self.handler.has_errors()
    
    def test_validate_data_insufficient_length(self):
        """Test data validation with insufficient data length."""
        short_data = pd.DataFrame({
            'Open': [1.0], 'High': [1.1], 'Low': [0.9], 'Close': [1.05]
        })
        assert self.handler.validate_data(short_data) is False
        assert self.handler.has_errors()
    
    def test_handle_calculation_error(self):
        """Test calculation error handling."""
        error = ValueError("Division by zero")
        context = {'period': 14, 'data_length': 100}
        error_info = self.handler.handle_calculation_error(error, context)
        
        assert 'error_type' in error_info
        assert 'error_message' in error_info
        assert 'suggestions' in error_info
        assert self.handler.has_errors()


class TestTrendErrorHandler:
    """Test trend error handler functionality."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.handler = TrendErrorHandler('EMA')
        
        # Create test data with enough rows for validation (minimum 50)
        np.random.seed(42)
        dates = pd.date_range('2023-01-01', periods=60, freq='D')
        self.valid_data = pd.DataFrame({
            'Open': np.random.uniform(1.0, 2.0, 60),
            'High': np.random.uniform(1.1, 2.1, 60),
            'Low': np.random.uniform(0.9, 1.9, 60),
            'Close': np.random.uniform(1.0, 2.0, 60)
        }, index=dates)
    
    def test_validate_parameters_valid(self):
        """Test parameter validation with valid parameters."""
        params = {'period': 20, 'alpha': 0.1}
        assert self.handler.validate_parameters(params) is True
        assert not self.handler.has_errors()
    
    def test_validate_parameters_invalid_alpha(self):
        """Test parameter validation with invalid alpha."""
        params = {'period': 20, 'alpha': 2.0}
        assert self.handler.validate_parameters(params) is False
        assert self.handler.has_errors()
    
    def test_validate_data_valid(self):
        """Test data validation with valid data."""
        assert self.handler.validate_data(self.valid_data) is True
        assert not self.handler.has_errors()


class TestMomentumErrorHandler:
    """Test momentum error handler functionality."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.handler = MomentumErrorHandler('MACD')
        
        # Create test data with enough rows for validation (minimum 50)
        np.random.seed(42)
        dates = pd.date_range('2023-01-01', periods=60, freq='D')
        self.valid_data = pd.DataFrame({
            'Close': np.random.uniform(1.0, 2.0, 60)
        }, index=dates)
    
    def test_validate_parameters_valid(self):
        """Test parameter validation with valid parameters."""
        params = {'fast_period': 12, 'slow_period': 26, 'signal_period': 9}
        assert self.handler.validate_parameters(params) is True
        assert not self.handler.has_errors()
    
    def test_validate_parameters_invalid_periods(self):
        """Test parameter validation with invalid period relationship."""
        params = {'fast_period': 26, 'slow_period': 12, 'signal_period': 9}
        assert self.handler.validate_parameters(params) is False
        assert self.handler.has_errors()
    
    def test_validate_data_valid(self):
        """Test data validation with valid data."""
        assert self.handler.validate_data(self.valid_data) is True
        assert not self.handler.has_errors()


class TestVolumeErrorHandler:
    """Test volume error handler functionality."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.handler = VolumeErrorHandler('OBV')
        
        # Create test data with enough rows for validation (minimum 50)
        np.random.seed(42)
        dates = pd.date_range('2023-01-01', periods=60, freq='D')
        self.valid_data = pd.DataFrame({
            'Close': np.random.uniform(1.0, 2.0, 60),
            'Volume': np.random.uniform(1000, 2000, 60)
        }, index=dates)
    
    def test_validate_data_valid(self):
        """Test data validation with valid data."""
        assert self.handler.validate_data(self.valid_data) is True
        assert not self.handler.has_errors()
    
    def test_validate_data_negative_volume(self):
        """Test data validation with negative volume."""
        invalid_data = pd.DataFrame({
            'Close': [1.0, 1.1, 1.2],
            'Volume': [1000, -100, 1200]
        })
        assert self.handler.validate_data(invalid_data) is False
        assert self.handler.has_errors()


class TestVolatilityErrorHandler:
    """Test volatility error handler functionality."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.handler = VolatilityErrorHandler('ATR')
        
        # Create test data with enough rows for validation (minimum 50)
        np.random.seed(42)
        dates = pd.date_range('2023-01-01', periods=60, freq='D')
        
        # Generate data ensuring High > Low
        base_prices = np.random.uniform(1.0, 2.0, 60)
        spreads = np.random.uniform(0.1, 0.3, 60)
        
        self.valid_data = pd.DataFrame({
            'High': base_prices + spreads/2,
            'Low': base_prices - spreads/2,
            'Close': base_prices
        }, index=dates)
    
    def test_validate_data_valid(self):
        """Test data validation with valid data."""
        assert self.handler.validate_data(self.valid_data) is True
        assert not self.handler.has_errors()
    
    def test_validate_data_invalid_high_low(self):
        """Test data validation with invalid high/low relationship."""
        invalid_data = pd.DataFrame({
            'High': [1.1, 1.0, 1.3],  # High < Low in second row
            'Low': [0.9, 1.1, 1.2],
            'Close': [1.05, 1.15, 1.25]
        })
        assert self.handler.validate_data(invalid_data) is False
        assert self.handler.has_errors()


class TestSupportResistanceErrorHandler:
    """Test support/resistance error handler functionality."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.handler = SupportResistanceErrorHandler('Pivot_Points')
        
        # Create test data with enough rows for validation (minimum 50)
        np.random.seed(42)
        dates = pd.date_range('2023-01-01', periods=60, freq='D')
        self.valid_data = pd.DataFrame({
            'High': np.random.uniform(1.1, 2.1, 60),
            'Low': np.random.uniform(0.9, 1.9, 60),
            'Close': np.random.uniform(1.0, 2.0, 60)
        }, index=dates)
    
    def test_validate_fibonacci_parameters_valid(self):
        """Test Fibonacci parameter validation with valid parameters."""
        handler = SupportResistanceErrorHandler('Fibonacci_Retracement')
        params = {'levels': [0.236, 0.382, 0.5, 0.618, 0.786]}
        assert handler.validate_parameters(params) is True
        assert not handler.has_errors()
    
    def test_validate_fibonacci_parameters_invalid(self):
        """Test Fibonacci parameter validation with invalid parameters."""
        handler = SupportResistanceErrorHandler('Fibonacci_Retracement')
        params = {'levels': [0.236, 1.5, 0.5]}  # 1.5 > 1.0
        assert handler.validate_parameters(params) is False
        assert handler.has_errors()


class TestPredictiveErrorHandler:
    """Test predictive error handler functionality."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.handler = PredictiveErrorHandler('HMA')
        self.valid_data = pd.DataFrame({
            'Close': [1.0] * 100  # Need at least 100 rows
        })
    
    def test_validate_parameters_valid(self):
        """Test parameter validation with valid parameters."""
        params = {'period': 20, 'forecast_periods': 10}
        assert self.handler.validate_parameters(params) is True
        assert not self.handler.has_errors()
    
    def test_validate_data_valid(self):
        """Test data validation with valid data."""
        assert self.handler.validate_data(self.valid_data) is True
        assert not self.handler.has_errors()


class TestProbabilityErrorHandler:
    """Test probability error handler functionality."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.handler = ProbabilityErrorHandler('MonteCarlo')
        self.valid_data = pd.DataFrame({
            'Close': [1.0] * 100  # Need at least 100 rows
        })
    
    def test_validate_monte_carlo_parameters_valid(self):
        """Test Monte Carlo parameter validation with valid parameters."""
        params = {'simulations': 1000, 'time_steps': 100, 'volatility': 0.2}
        assert self.handler.validate_parameters(params) is True
        assert not self.handler.has_errors()
    
    def test_validate_kelly_parameters_valid(self):
        """Test Kelly Criterion parameter validation with valid parameters."""
        handler = ProbabilityErrorHandler('Kelly')
        params = {'win_rate': 0.6, 'avg_win': 100, 'avg_loss': 50}
        assert handler.validate_parameters(params) is True
        assert not handler.has_errors()


class TestSentimentErrorHandler:
    """Test sentiment error handler functionality."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.handler = SentimentErrorHandler('FearGreed')
        self.valid_data = pd.DataFrame({
            'Close': [1.0] * 50  # Need at least 50 rows
        })
    
    def test_validate_cot_data_valid(self):
        """Test COT data validation with valid data."""
        handler = SentimentErrorHandler('COT')
        
        # Create test data with enough rows for validation (minimum 50)
        np.random.seed(42)
        dates = pd.date_range('2023-01-01', periods=60, freq='D')
        valid_cot_data = pd.DataFrame({
            'Open_Interest': np.random.uniform(1000, 2000, 60),
            'Long_Positions': np.random.uniform(500, 1000, 60),
            'Short_Positions': np.random.uniform(300, 800, 60)
        }, index=dates)
        
        assert handler.validate_data(valid_cot_data) is True
        assert not handler.has_errors()
    
    def test_validate_cot_data_negative_positions(self):
        """Test COT data validation with negative positions."""
        handler = SentimentErrorHandler('COT')
        invalid_cot_data = pd.DataFrame({
            'Open_Interest': [1000, 1100, 1200],
            'Long_Positions': [500, -50, 600],  # Negative position
            'Short_Positions': [300, 350, 400]
        })
        assert handler.validate_data(invalid_cot_data) is False
        assert handler.has_errors()


class TestBaseErrorHandlerMethods:
    """Test base error handler utility methods."""
    
    def test_validate_numeric_range_valid(self):
        """Test numeric range validation with valid values."""
        handler = OscillatorErrorHandler('RSI')
        assert handler.validate_numeric_range(50, 0, 100, 'test_param') is True
        assert not handler.has_errors()
    
    def test_validate_numeric_range_invalid(self):
        """Test numeric range validation with invalid values."""
        handler = OscillatorErrorHandler('RSI')
        assert handler.validate_numeric_range(150, 0, 100, 'test_param') is False
        assert handler.has_errors()
    
    def test_validate_positive_value_valid(self):
        """Test positive value validation with valid values."""
        handler = OscillatorErrorHandler('RSI')
        assert handler.validate_positive_value(50, 'test_param') is True
        assert not handler.has_errors()
    
    def test_validate_positive_value_invalid(self):
        """Test positive value validation with invalid values."""
        handler = OscillatorErrorHandler('RSI')
        assert handler.validate_positive_value(-5, 'test_param') is False
        assert handler.has_errors()
    
    def test_get_error_summary(self):
        """Test error summary generation."""
        handler = OscillatorErrorHandler('RSI')
        handler.add_error("Test error")
        handler.add_warning("Test warning")
        
        summary = handler.get_error_summary()
        assert summary['indicator'] == 'RSI'
        assert summary['total_errors'] == 1
        assert summary['total_warnings'] == 1
        assert len(summary['errors']) == 1
        assert len(summary['warnings']) == 1
    
    def test_clear_errors(self):
        """Test error clearing functionality."""
        handler = OscillatorErrorHandler('RSI')
        handler.add_error("Test error")
        handler.add_warning("Test warning")
        
        assert handler.has_errors()
        assert handler.has_warnings()
        
        handler.clear_errors()
        assert not handler.has_errors()
        assert not handler.has_warnings()


if __name__ == "__main__":
    pytest.main([__file__])
