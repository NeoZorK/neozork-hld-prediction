# tests/calculation/indicators/volatility/test_bb_indicator.py

import pytest
import pandas as pd
import numpy as np
from unittest.mock import patch, MagicMock
from src.calculation.indicators.volatility.bb_ind import BBIndicator


class TestBBIndicator:
    """Test cases for Bollinger Bands indicator."""

    def setup_method(self):
        """Set up test fixtures."""
        self.bb = BBIndicator()
        
        # Create sample data
        self.sample_data = pd.DataFrame({
            'open': [100, 101, 102, 103, 104],
            'high': [105, 106, 107, 108, 109],
            'low': [99, 100, 101, 102, 103],
            'close': [101, 102, 103, 104, 105],
            'volume': [1000, 1100, 1200, 1300, 1400]
        })

    def test_bb_initialization(self):
        """Test Bollinger Bands indicator initialization."""
        assert self.bb.name == "Bollinger_Bands"
        assert self.bb.category == "volatility"
        assert "Bollinger" in self.bb.description

    def test_bb_calculation_basic(self):
        """Test basic Bollinger Bands calculation."""
        result = self.bb.calculate(self.sample_data)
        
        assert isinstance(result, pd.DataFrame)
        assert 'BB_Upper' in result.columns
        assert 'BB_Middle' in result.columns
        assert 'BB_Lower' in result.columns
        assert len(result) == len(self.sample_data)

    def test_bb_calculation_with_custom_parameters(self):
        """Test Bollinger Bands calculation with custom parameters."""
        bb_custom = BBIndicator(period=10, std_dev=2.0)
        result = bb_custom.calculate(self.sample_data)
        
        assert isinstance(result, pd.DataFrame)
        assert 'BB_Upper' in result.columns
        assert 'BB_Middle' in result.columns
        assert 'BB_Lower' in result.columns

    def test_bb_invalid_parameters(self):
        """Test Bollinger Bands with invalid parameters."""
        with pytest.raises(ValueError, match="Period must be positive"):
            BBIndicator(period=0)
        
        with pytest.raises(ValueError, match="Period must be positive"):
            BBIndicator(period=-1)
        
        with pytest.raises(ValueError, match="Standard deviation must be positive"):
            BBIndicator(std_dev=0)
        
        with pytest.raises(ValueError, match="Standard deviation must be positive"):
            BBIndicator(std_dev=-1)

    def test_bb_empty_dataframe(self):
        """Test Bollinger Bands with empty dataframe."""
        empty_df = pd.DataFrame()
        result = self.bb.calculate(empty_df)
        
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 0

    def test_bb_missing_columns(self):
        """Test Bollinger Bands with missing required columns."""
        incomplete_data = self.sample_data.drop(columns=['close'])
        
        with pytest.raises(ValueError, match="Missing required columns"):
            self.bb.calculate(incomplete_data)

    def test_bb_parameter_validation(self):
        """Test Bollinger Bands parameter validation."""
        # Test with valid parameters
        bb_valid = BBIndicator(period=20, std_dev=2.0)
        assert bb_valid.period == 20
        assert bb_valid.std_dev == 2.0
        
        # Test with float parameters (should be converted appropriately)
        bb_float = BBIndicator(period=20.5, std_dev=2.5)
        assert bb_float.period == 20
        assert bb_float.std_dev == 2.5

    def test_bb_value_relationships(self):
        """Test Bollinger Bands value relationships."""
        result = self.bb.calculate(self.sample_data)
        
        # Upper band should be greater than or equal to middle band
        assert all(result['BB_Upper'].dropna() >= result['BB_Middle'].dropna())
        
        # Middle band should be greater than or equal to lower band
        assert all(result['BB_Middle'].dropna() >= result['BB_Lower'].dropna())
        
        # Upper band should be greater than lower band
        assert all(result['BB_Upper'].dropna() > result['BB_Lower'].dropna())

    def test_bb_with_nan_values(self):
        """Test Bollinger Bands calculation with NaN values."""
        data_with_nan = self.sample_data.copy()
        data_with_nan.loc[2, 'close'] = np.nan
        
        result = self.bb.calculate(data_with_nan)
        
        assert isinstance(result, pd.DataFrame)
        assert 'BB_Upper' in result.columns
        assert 'BB_Middle' in result.columns
        assert 'BB_Lower' in result.columns

    def test_bb_docstring_info(self):
        """Test Bollinger Bands docstring information."""
        assert "Bollinger" in self.bb.name
        assert "volatility" in self.bb.category.lower()
        assert len(self.bb.description) > 0

    def test_bb_cli_integration(self):
        """Test Bollinger Bands CLI integration."""
        # Test that the indicator can be used in CLI context
        assert hasattr(self.bb, 'calculate')
        assert callable(self.bb.calculate)

    def test_bb_performance(self):
        """Test Bollinger Bands performance with larger dataset."""
        # Create larger dataset
        large_data = pd.DataFrame({
            'open': np.random.uniform(100, 110, 1000),
            'high': np.random.uniform(110, 120, 1000),
            'low': np.random.uniform(90, 100, 1000),
            'close': np.random.uniform(100, 110, 1000),
            'volume': np.random.randint(1000, 2000, 1000)
        })
        
        result = self.bb.calculate(large_data)
        
        assert isinstance(result, pd.DataFrame)
        assert len(result) == len(large_data)
        assert 'BB_Upper' in result.columns
        assert 'BB_Middle' in result.columns
        assert 'BB_Lower' in result.columns

    def test_bb_edge_cases(self):
        """Test Bollinger Bands edge cases."""
        # Test with all same values
        same_values = pd.DataFrame({
            'open': [100] * 10,
            'high': [100] * 10,
            'low': [100] * 10,
            'close': [100] * 10,
            'volume': [1000] * 10
        })
        
        result = self.bb.calculate(same_values)
        assert isinstance(result, pd.DataFrame)
        assert 'BB_Upper' in result.columns
        assert 'BB_Middle' in result.columns
        assert 'BB_Lower' in result.columns

    def test_bb_consistency(self):
        """Test Bollinger Bands calculation consistency."""
        result1 = self.bb.calculate(self.sample_data)
        result2 = self.bb.calculate(self.sample_data)
        
        pd.testing.assert_frame_equal(result1, result2)

    def test_bb_volatility_measurement(self):
        """Test that Bollinger Bands properly measure volatility."""
        # Create data with different volatility levels
        low_vol_data = pd.DataFrame({
            'open': [100, 100.1, 100.2, 100.1, 100.3],
            'high': [100.2, 100.3, 100.4, 100.3, 100.5],
            'low': [99.9, 100.0, 100.1, 100.0, 100.2],
            'close': [100.1, 100.2, 100.3, 100.2, 100.4],
            'volume': [1000, 1100, 1200, 1300, 1400]
        })
        
        high_vol_data = pd.DataFrame({
            'open': [100, 105, 95, 110, 90],
            'high': [110, 115, 105, 120, 100],
            'low': [90, 95, 85, 100, 80],
            'close': [105, 95, 110, 90, 105],
            'volume': [1000, 1100, 1200, 1300, 1400]
        })
        
        low_vol_result = self.bb.calculate(low_vol_data)
        high_vol_result = self.bb.calculate(high_vol_data)
        
        # High volatility data should have wider bands
        low_vol_width = (low_vol_result['BB_Upper'] - low_vol_result['BB_Lower']).mean()
        high_vol_width = (high_vol_result['BB_Upper'] - high_vol_result['BB_Lower']).mean()
        
        assert high_vol_width > low_vol_width

    def test_bb_std_dev_impact(self):
        """Test the impact of standard deviation on band width."""
        bb_narrow = BBIndicator(std_dev=1.0)
        bb_wide = BBIndicator(std_dev=3.0)
        
        result_narrow = bb_narrow.calculate(self.sample_data)
        result_wide = bb_wide.calculate(self.sample_data)
        
        narrow_width = (result_narrow['BB_Upper'] - result_narrow['BB_Lower']).mean()
        wide_width = (result_wide['BB_Upper'] - result_wide['BB_Lower']).mean()
        
        assert wide_width > narrow_width 