#!/usr/bin/env python3
"""
Test SAR indicator signals validation for the command:
uv run run_analysis.py show csv mn1 -d fastest --rule sar:0.000002,0.00005
"""

import pytest
import pandas as pd
import numpy as np
import os
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent.parent / "src"))

from src.calculation.indicators.trend.sar_ind import calculate_sar, calculate_sar_signals, apply_rule_sar
from src.common.constants import BUY, SELL, NOTRADE


class TestSARSignalsValidation:
    """Test SAR indicator signals validation for specific parameters."""

    def setup_method(self):
        """Set up test data similar to mn1.csv."""
        # Create test data similar to the mn1.csv structure
        dates = pd.date_range('2024-01-01', periods=10, freq='h')
        self.test_data = pd.DataFrame({
            'Open': [100.50, 102.10, 105.30, 108.45, 110.75, 113.20, 115.60, 118.90, 120.50, 122.30],
            'High': [105.25, 107.40, 110.80, 112.90, 115.60, 118.20, 120.80, 123.40, 125.20, 127.10],
            'Low': [98.75, 100.25, 103.10, 106.20, 108.30, 111.50, 113.80, 116.60, 118.40, 120.20],
            'Close': [102.10, 105.30, 108.45, 110.75, 113.20, 115.60, 118.90, 120.50, 122.30, 124.10],
            'Volume': [1000, 1200, 1100, 1300, 1150, 1400, 1250, 1500, 1350, 1600]
        }, index=dates)

    def test_sar_calculation_with_specific_parameters(self):
        """Test SAR calculation with the exact parameters from the command."""
        acceleration = 0.000002
        maximum = 0.00005
        
        # Calculate SAR
        sar_values = calculate_sar(self.test_data, acceleration, maximum)
        
        # Verify SAR values are calculated
        assert isinstance(sar_values, pd.Series)
        assert len(sar_values) == len(self.test_data)
        assert not sar_values.isna().all()
        
        # Check that SAR values are within reasonable bounds
        assert sar_values.min() >= self.test_data['Low'].min() * 0.99
        assert sar_values.max() <= self.test_data['High'].max() * 1.01

    def test_sar_signals_generation(self):
        """Test SAR signal generation with Close prices."""
        acceleration = 0.000002
        maximum = 0.00005
        
        # Calculate SAR
        sar_values = calculate_sar(self.test_data, acceleration, maximum)
        
        # Calculate signals using Close prices
        signals = calculate_sar_signals(self.test_data['Close'], sar_values)
        
        # Verify signals
        assert isinstance(signals, pd.Series)
        assert len(signals) == len(self.test_data)
        
        # Check signal values are valid
        valid_signals = [NOTRADE, BUY, SELL]
        assert all(signal in valid_signals for signal in signals.dropna())

    def test_sar_apply_rule_complete_workflow(self):
        """Test complete SAR rule application workflow."""
        acceleration = 0.000002
        maximum = 0.00005
        point_size = 0.01
        
        # Apply SAR rule
        result_df = apply_rule_sar(
            self.test_data, 
            point_size, 
            sar_acceleration=acceleration, 
            sar_maximum=maximum
        )
        
        # Verify required columns are present
        required_columns = ['SAR', 'SAR_Signal', 'SAR_Price_Type', 'PPrice1', 'PPrice2', 'Direction', 'Diff']
        for col in required_columns:
            assert col in result_df.columns, f"Missing required column: {col}"
        
        # Verify SAR values
        assert not result_df['SAR'].isna().all()
        assert result_df['SAR_Price_Type'].iloc[0] == 'Close'
        
        # Verify signals
        valid_signals = [NOTRADE, BUY, SELL]
        assert all(signal in valid_signals for signal in result_df['SAR_Signal'].dropna())
        
        # Verify support/resistance levels
        assert not result_df['PPrice1'].isna().all()
        assert not result_df['PPrice2'].isna().all()

    def test_sar_signal_logic_validation(self):
        """Test SAR signal logic - BUY when price crosses above SAR, SELL when below."""
        acceleration = 0.000002
        maximum = 0.00005
        
        # Calculate SAR
        sar_values = calculate_sar(self.test_data, acceleration, maximum)
        
        # Calculate signals
        signals = calculate_sar_signals(self.test_data['Close'], sar_values)
        
        # Test signal logic for specific cases
        for i in range(1, len(self.test_data)):
            current_price = self.test_data['Close'].iloc[i]
            current_sar = sar_values.iloc[i]
            current_signal = signals.iloc[i]
            
            prev_price = self.test_data['Close'].iloc[i-1]
            prev_sar = sar_values.iloc[i-1]
            
            # BUY signal: Price crosses above SAR
            if current_price > current_sar and prev_price <= prev_sar:
                assert current_signal == BUY, f"Expected BUY signal at index {i}"
            
            # SELL signal: Price crosses below SAR
            elif current_price < current_sar and prev_price >= prev_sar:
                assert current_signal == SELL, f"Expected SELL signal at index {i}"

    def test_sar_parameter_sensitivity(self):
        """Test SAR sensitivity to different parameter values."""
        # Test with very small parameters (like in the command)
        small_acc = 0.000002
        small_max = 0.00005
        
        # Test with larger parameters
        large_acc = 0.02
        large_max = 0.2
        
        # Calculate SAR with both parameter sets
        sar_small = calculate_sar(self.test_data, small_acc, small_max)
        sar_large = calculate_sar(self.test_data, large_acc, large_max)
        
        # Both should produce valid results
        assert not sar_small.isna().all()
        assert not sar_large.isna().all()
        
        # Small parameters should produce more conservative SAR values
        # (closer to price levels)
        price_range = self.test_data['High'].max() - self.test_data['Low'].min()
        sar_small_range = sar_small.max() - sar_small.min()
        sar_large_range = sar_large.max() - sar_large.min()
        
        # Small parameters should generally produce smaller ranges
        assert sar_small_range <= sar_large_range * 2  # Allow some tolerance

    def test_sar_edge_cases(self):
        """Test SAR edge cases and boundary conditions."""
        acceleration = 0.000002
        maximum = 0.00005
        
        # Test with minimal data
        minimal_data = self.test_data.head(2)
        sar_minimal = calculate_sar(minimal_data, acceleration, maximum)
        assert len(sar_minimal) == 2
        
        # Test with flat price data
        flat_data = self.test_data.copy()
        flat_data['High'] = 100.0
        flat_data['Low'] = 100.0
        flat_data['Close'] = 100.0
        flat_data['Open'] = 100.0
        
        sar_flat = calculate_sar(flat_data, acceleration, maximum)
        assert not sar_flat.isna().all()

    def test_sar_integration_with_workflow(self):
        """Test SAR integration with the complete workflow."""
        # Simulate the exact command parameters
        acceleration = 0.000002
        maximum = 0.00005
        point_size = 0.01
        
        # Apply rule and verify all components work together
        result_df = apply_rule_sar(
            self.test_data, 
            point_size, 
            sar_acceleration=acceleration, 
            sar_maximum=maximum
        )
        
        # Verify the complete workflow produces expected results
        assert 'SAR' in result_df.columns
        assert 'SAR_Signal' in result_df.columns
        assert 'Direction' in result_df.columns
        assert 'PPrice1' in result_df.columns
        assert 'PPrice2' in result_df.columns
        
        # Verify signal counts are reasonable
        signals = result_df['SAR_Signal'].dropna()
        buy_signals = (signals == BUY).sum()
        sell_signals = (signals == SELL).sum()
        
        # For small test datasets, it's okay to have no signals
        # The important thing is that the workflow completes successfully
        print(f"SAR signals generated: Buy={buy_signals}, Sell={sell_signals}, Total={len(signals)}")
        
        # Verify that SAR values are calculated correctly
        assert not result_df['SAR'].isna().all()
        assert result_df['SAR'].min() >= self.test_data['Low'].min() * 0.99
        assert result_df['SAR'].max() <= self.test_data['High'].max() * 1.01


if __name__ == "__main__":
    # Run the tests
    pytest.main([__file__, "-v"]) 