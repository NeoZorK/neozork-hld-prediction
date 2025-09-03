"""
Unit tests for technical indicators in analysis module.

This module tests the technical indicator implementations.
"""

import pytest
import pandas as pd
import numpy as np
from unittest.mock import Mock, patch, MagicMock

from src.analysis.indicators.base import (
    BaseIndicator, 
    TrendIndicator, 
    MomentumIndicator, 
    VolatilityIndicator
)


class MockIndicator(BaseIndicator):
    """Mock indicator for testing."""
    
    def calculate(self, data: pd.DataFrame) -> pd.Series:
        """Mock calculation."""
        return pd.Series([1.0, 2.0, 3.0], index=data.index)
    
    def validate_input(self, data: pd.DataFrame) -> bool:
        """Mock validation."""
        return isinstance(data, pd.DataFrame) and len(data) > 0


class MockTrendIndicator(TrendIndicator):
    """Mock trend indicator for testing."""
    
    def calculate(self, data: pd.DataFrame) -> pd.Series:
        """Mock calculation."""
        return pd.Series([1.0, 2.0, 3.0], index=data.index)
    
    def validate_input(self, data: pd.DataFrame) -> bool:
        """Mock validation."""
        return isinstance(data, pd.DataFrame) and len(data) > 0


class MockMomentumIndicator(MomentumIndicator):
    """Mock momentum indicator for testing."""
    
    def calculate(self, data: pd.DataFrame) -> pd.Series:
        """Mock calculation."""
        return pd.Series([50.0, 60.0, 70.0], index=data.index)
    
    def validate_input(self, data: pd.DataFrame) -> bool:
        """Mock validation."""
        return isinstance(data, pd.DataFrame) and len(data) > 0


class MockVolatilityIndicator(VolatilityIndicator):
    """Mock volatility indicator for testing."""
    
    def calculate(self, data: pd.DataFrame) -> pd.Series:
        """Mock calculation."""
        return pd.Series([0.1, 0.2, 0.3], index=data.index)
    
    def validate_input(self, data: pd.DataFrame) -> bool:
        """Mock validation."""
        return isinstance(data, pd.DataFrame) and len(data) > 0


class TestBaseIndicator:
    """Test cases for BaseIndicator class."""
    
    def test_init(self):
        """Test BaseIndicator initialization."""
        indicator = MockIndicator("test_indicator", {})
        
        assert indicator.name == "test_indicator"
        assert indicator.parameters == {}
        assert indicator.lookback_periods == 14
        assert indicator.min_data_points == 1
    
    def test_init_with_config(self):
        """Test BaseIndicator initialization with config."""
        config = {
            "parameters": {"param1": "value1"},
            "lookback_periods": 20,
            "min_data_points": 5
        }
        indicator = MockIndicator("test_indicator", config)
        
        assert indicator.parameters == {"param1": "value1"}
        assert indicator.lookback_periods == 20
        assert indicator.min_data_points == 5
    
    def test_calculate(self):
        """Test indicator calculation."""
        indicator = MockIndicator("test_indicator", {})
        data = pd.DataFrame({"close": [1.0, 2.0, 3.0]})
        
        result = indicator.calculate(data)
        
        assert isinstance(result, pd.Series)
        assert len(result) == 3
        assert list(result) == [1.0, 2.0, 3.0]
    
    def test_validate_input(self):
        """Test input validation."""
        indicator = MockIndicator("test_indicator", {})
        
        # Valid data
        valid_data = pd.DataFrame({"close": [1.0, 2.0, 3.0]})
        assert indicator.validate_input(valid_data) is True
        
        # Invalid data - not DataFrame
        assert indicator.validate_input("invalid") is False
        
        # Invalid data - empty DataFrame
        empty_data = pd.DataFrame()
        assert indicator.validate_input(empty_data) is False
    
    def test_get_parameters(self):
        """Test parameter retrieval."""
        config = {"parameters": {"param1": "value1", "param2": 42}}
        indicator = MockIndicator("test_indicator", config)
        
        params = indicator.get_parameters()
        
        assert isinstance(params, dict)
        assert params["param1"] == "value1"
        assert params["param2"] == 42
    
    def test_set_parameters(self):
        """Test parameter setting."""
        indicator = MockIndicator("test_indicator", {})
        
        new_params = {
            "param1": "new_value",
            "lookback_periods": 25,
            "min_data_points": 10
        }
        
        indicator.set_parameters(new_params)
        
        assert indicator.parameters["param1"] == "new_value"
        assert indicator.lookback_periods == 25
        assert indicator.min_data_points == 10
    
    def test_get_info(self):
        """Test information retrieval."""
        config = {
            "parameters": {"param1": "value1"},
            "lookback_periods": 20,
            "min_data_points": 5
        }
        indicator = MockIndicator("test_indicator", config)
        
        info = indicator.get_info()
        
        assert isinstance(info, dict)
        assert info["name"] == "test_indicator"
        assert info["class"] == "MockIndicator"
        assert info["parameters"] == {"param1": "value1"}
        assert info["lookback_periods"] == 20
        assert info["min_data_points"] == 5


class TestTrendIndicator:
    """Test cases for TrendIndicator class."""
    
    def test_init(self):
        """Test TrendIndicator initialization."""
        indicator = MockTrendIndicator("test_trend", {})
        
        assert indicator.name == "test_trend"
        assert indicator.trend_direction is None
        assert indicator.trend_strength == 0.0
    
    def test_get_trend_info(self):
        """Test trend information retrieval."""
        indicator = MockTrendIndicator("test_trend", {})
        
        info = indicator.get_trend_info()
        
        assert isinstance(info, dict)
        assert info["direction"] is None
        assert info["strength"] == 0.0
        assert info["indicator_name"] == "test_trend"
    
    def test_trend_direction_checks(self):
        """Test trend direction checking methods."""
        indicator = MockTrendIndicator("test_trend", {})
        
        # Test default state
        assert indicator.is_uptrend() is False
        assert indicator.is_downtrend() is False
        assert indicator.is_sideways() is False
        
        # Test uptrend
        indicator.trend_direction = "up"
        assert indicator.is_uptrend() is True
        assert indicator.is_downtrend() is False
        assert indicator.is_sideways() is False
        
        # Test downtrend
        indicator.trend_direction = "down"
        assert indicator.is_uptrend() is False
        assert indicator.is_downtrend() is True
        assert indicator.is_sideways() is False
        
        # Test sideways
        indicator.trend_direction = "sideways"
        assert indicator.is_uptrend() is False
        assert indicator.is_downtrend() is False
        assert indicator.is_sideways() is True


class TestMomentumIndicator:
    """Test cases for MomentumIndicator class."""
    
    def test_init(self):
        """Test MomentumIndicator initialization."""
        indicator = MockMomentumIndicator("test_momentum", {})
        
        assert indicator.name == "test_momentum"
        assert indicator.overbought_threshold == 70
        assert indicator.oversold_threshold == 30
    
    def test_init_with_config(self):
        """Test MomentumIndicator initialization with config."""
        config = {
            "overbought_threshold": 80,
            "oversold_threshold": 20
        }
        indicator = MockMomentumIndicator("test_momentum", config)
        
        assert indicator.overbought_threshold == 80
        assert indicator.oversold_threshold == 20
    
    def test_overbought_detection(self):
        """Test overbought condition detection."""
        indicator = MockMomentumIndicator("test_momentum", {})
        
        # Test overbought values
        assert indicator.is_overbought(75) is True
        assert indicator.is_overbought(80) is True
        assert indicator.is_overbought(90) is True
        
        # Test non-overbought values
        assert indicator.is_overbought(70) is False
        assert indicator.is_overbought(60) is False
        assert indicator.is_overbought(50) is False
    
    def test_oversold_detection(self):
        """Test oversold condition detection."""
        indicator = MockMomentumIndicator("test_momentum", {})
        
        # Test oversold values
        assert indicator.is_oversold(25) is True
        assert indicator.is_oversold(20) is True
        assert indicator.is_oversold(10) is True
        
        # Test non-oversold values
        assert indicator.is_oversold(30) is False
        assert indicator.is_oversold(40) is False
        assert indicator.is_oversold(50) is False
    
    def test_get_momentum_info(self):
        """Test momentum information retrieval."""
        indicator = MockMomentumIndicator("test_momentum", {})
        
        info = indicator.get_momentum_info()
        
        assert isinstance(info, dict)
        assert info["overbought_threshold"] == 70
        assert info["oversold_threshold"] == 30
        assert info["indicator_name"] == "test_momentum"


class TestVolatilityIndicator:
    """Test cases for VolatilityIndicator class."""
    
    def test_init(self):
        """Test VolatilityIndicator initialization."""
        indicator = MockVolatilityIndicator("test_volatility", {})
        
        assert indicator.name == "test_volatility"
        assert indicator.volatility_period == 20
        assert indicator.volatility_multiplier == 2.0
    
    def test_init_with_config(self):
        """Test VolatilityIndicator initialization with config."""
        config = {
            "volatility_period": 30,
            "volatility_multiplier": 1.5
        }
        indicator = MockVolatilityIndicator("test_volatility", config)
        
        assert indicator.volatility_period == 30
        assert indicator.volatility_multiplier == 1.5
    
    def test_get_volatility_info(self):
        """Test volatility information retrieval."""
        indicator = MockVolatilityIndicator("test_volatility", {})
        
        info = indicator.get_volatility_info()
        
        assert isinstance(info, dict)
        assert info["volatility_period"] == 20
        assert info["volatility_multiplier"] == 2.0
        assert info["indicator_name"] == "test_volatility"
    
    def test_calculate_bands(self):
        """Test volatility band calculation."""
        indicator = MockVolatilityIndicator("test_volatility", {})
        
        # Create test data
        data = pd.Series([1.0, 2.0, 3.0, 4.0, 5.0])
        
        upper_band, lower_band = indicator.calculate_bands(data)
        
        assert isinstance(upper_band, pd.Series)
        assert isinstance(lower_band, pd.Series)
        assert len(upper_band) == len(data)
        assert len(lower_band) == len(data)
        
        # Check that upper band is above lower band
        assert all(upper_band >= lower_band)


class TestIndicatorIntegration:
    """Test cases for indicator integration."""
    
    def test_indicator_hierarchy(self):
        """Test that indicators properly inherit from base classes."""
        # Check inheritance
        assert issubclass(TrendIndicator, BaseIndicator)
        assert issubclass(MomentumIndicator, BaseIndicator)
        assert issubclass(VolatilityIndicator, BaseIndicator)
        
        # Check that they can be instantiated
        trend_ind = MockTrendIndicator("test", {})
        momentum_ind = MockMomentumIndicator("test", {})
        volatility_ind = MockVolatilityIndicator("test", {})
        
        assert isinstance(trend_ind, BaseIndicator)
        assert isinstance(momentum_ind, BaseIndicator)
        assert isinstance(volatility_ind, BaseIndicator)
    
    def test_indicator_calculation_flow(self):
        """Test complete indicator calculation flow."""
        indicator = MockTrendIndicator("test", {
            "parameters": {"sensitivity": 0.8},
            "lookback_periods": 20,
            "min_data_points": 10
        })
        
        # Create test data
        data = pd.DataFrame({
            "close": np.random.randn(100),
            "volume": np.random.randint(1000, 10000, 100)
        })
        
        # Validate input
        assert indicator.validate_input(data) is True
        
        # Calculate indicator
        result = indicator.calculate(data)
        
        # Check result
        assert isinstance(result, pd.Series)
        assert len(result) == 100
        
        # Check parameters
        params = indicator.get_parameters()
        assert params["sensitivity"] == 0.8
        
        # Check info
        info = indicator.get_info()
        assert info["lookback_periods"] == 20
        assert info["min_data_points"] == 10
    
    def test_indicator_parameter_management(self):
        """Test indicator parameter management."""
        indicator = MockIndicator("test", {})
        
        # Set initial parameters
        initial_params = {"param1": "value1", "param2": 42}
        indicator.set_parameters(initial_params)
        
        # Verify parameters
        assert indicator.get_parameters() == initial_params
        
        # Update parameters
        update_params = {"param1": "new_value", "param3": 100}
        indicator.set_parameters(update_params)
        
        # Verify updated parameters
        expected_params = {"param1": "new_value", "param2": 42, "param3": 100}
        assert indicator.get_parameters() == expected_params
    
    def test_indicator_validation(self):
        """Test indicator input validation."""
        indicator = MockIndicator("test", {})
        
        # Valid data
        valid_data = pd.DataFrame({"close": [1.0, 2.0, 3.0]})
        assert indicator.validate_input(valid_data) is True
        
        # Invalid data types
        assert indicator.validate_input(None) is False
        assert indicator.validate_input("string") is False
        assert indicator.validate_input(123) is False
        
        # Invalid data structures
        empty_df = pd.DataFrame()
        assert indicator.validate_input(empty_df) is False
        
        # Test with minimum data points requirement
        indicator.min_data_points = 5
        small_data = pd.DataFrame({"close": [1.0, 2.0, 3.0]})
        assert indicator.validate_input(small_data) is False
        
        large_data = pd.DataFrame({"close": [1.0, 2.0, 3.0, 4.0, 5.0, 6.0]})
        assert indicator.validate_input(large_data) is True
