# -*- coding: utf-8 -*-
# tests/calculation/test_rsi_integration.py

"""
Integration tests for RSI indicator with main indicator module.
"""

import pytest
import pandas as pd
import numpy as np
from src.calculation.indicator import calculate_pressure_vector
from src.common.constants import TradingRule


class TestRSIIntegration:
    """Integration tests for RSI indicator."""
    
    def setup_method(self):
        """Set up test data."""
        # Create sample price data
        dates = pd.date_range('2023-01-01', periods=50, freq='D')
        np.random.seed(42)  # For reproducible tests
        
        # Generate realistic price data
        base_price = 100.0
        returns = np.random.normal(0, 0.02, 50)  # 2% daily volatility
        prices = [base_price]
        for ret in returns[1:]:
            prices.append(prices[-1] * (1 + ret))
        
        self.test_data = pd.DataFrame({
            'Open': prices,
            'High': [p * 1.01 for p in prices],  # 1% higher
            'Low': [p * 0.99 for p in prices],   # 1% lower
            'Close': prices,
            'TickVolume': np.random.randint(1000, 10000, 50)
        }, index=dates)
    
    def test_rsi_basic_integration(self):
        """Test basic RSI integration with main indicator module."""
        df = self.test_data.copy()
        point = 0.01
        
        result = calculate_pressure_vector(df, point, TradingRule.RSI)
        
        # Check that RSI-specific columns are present
        assert 'RSI' in result.columns
        assert 'RSI_Signal' in result.columns
        
        # Check that standard output columns are present
        assert 'PPrice1' in result.columns
        assert 'PColor1' in result.columns
        assert 'PPrice2' in result.columns
        assert 'PColor2' in result.columns
        assert 'Direction' in result.columns
        assert 'Diff' in result.columns
        
        # Check that RSI values are calculated
        assert not result['RSI'].isna().all()
        
        # Check that RSI values are between 0 and 100
        valid_rsi = result['RSI'].dropna()
        if len(valid_rsi) > 0:
            assert valid_rsi.min() >= 0
            assert valid_rsi.max() <= 100
    
    def test_rsi_momentum_integration(self):
        """Test RSI momentum integration with main indicator module."""
        df = self.test_data.copy()
        point = 0.01
        
        result = calculate_pressure_vector(df, point, TradingRule.RSI_Momentum)
        
        # Check that RSI momentum-specific columns are present
        assert 'RSI' in result.columns
        assert 'RSI_Momentum' in result.columns
        assert 'RSI_Signal' in result.columns
        
        # Check that momentum is calculated
        assert not result['RSI_Momentum'].isna().all()
    
    def test_rsi_divergence_integration(self):
        """Test RSI divergence integration with main indicator module."""
        df = self.test_data.copy()
        point = 0.01
        
        result = calculate_pressure_vector(df, point, TradingRule.RSI_Divergence)
        
        # Check that RSI divergence-specific columns are present
        assert 'RSI' in result.columns
        assert 'RSI_Signal' in result.columns
        
        # Check that divergence strength is calculated
        assert not result['Diff'].isna().all()
    
    def test_rsi_vs_traditional_indicators(self):
        """Test that RSI rules don't interfere with traditional indicators."""
        df = self.test_data.copy()
        point = 0.01
        
        # Test traditional indicator
        traditional_result = calculate_pressure_vector(df, point, TradingRule.PV_HighLow)
        
        # Test RSI indicator
        rsi_result = calculate_pressure_vector(df, point, TradingRule.RSI)
        
        # Both should have the same basic structure
        assert 'Open' in traditional_result.columns
        assert 'Open' in rsi_result.columns
        assert 'High' in traditional_result.columns
        assert 'High' in rsi_result.columns
        assert 'Low' in traditional_result.columns
        assert 'Low' in rsi_result.columns
        assert 'Close' in traditional_result.columns
        assert 'Close' in rsi_result.columns
        assert 'Volume' in traditional_result.columns
        assert 'Volume' in rsi_result.columns
        
        # Traditional should have HL, Pressure, PV
        assert 'HL' in traditional_result.columns
        assert 'Pressure' in traditional_result.columns
        assert 'PV' in traditional_result.columns
        
        # RSI should have RSI-specific columns
        assert 'RSI' in rsi_result.columns
        assert 'RSI_Signal' in rsi_result.columns
        
        # RSI should NOT have HL, Pressure, PV (they're not calculated for RSI rules)
        assert 'HL' not in rsi_result.columns
        assert 'Pressure' not in rsi_result.columns
        assert 'PV' not in rsi_result.columns
    
    def test_rsi_all_variants_comparison(self):
        """Test comparison between all RSI variants."""
        df = self.test_data.copy()
        point = 0.01
        
        # Calculate all RSI variants
        rsi_basic = calculate_pressure_vector(df, point, TradingRule.RSI)
        rsi_momentum = calculate_pressure_vector(df, point, TradingRule.RSI_Momentum)
        rsi_divergence = calculate_pressure_vector(df, point, TradingRule.RSI_Divergence)
        
        # All should have basic RSI column
        assert 'RSI' in rsi_basic.columns
        assert 'RSI' in rsi_momentum.columns
        assert 'RSI' in rsi_divergence.columns
        
        # RSI values should be the same across all variants
        rsi_basic_values = rsi_basic['RSI'].dropna()
        rsi_momentum_values = rsi_momentum['RSI'].dropna()
        rsi_divergence_values = rsi_divergence['RSI'].dropna()
        
        # Should have same number of valid values
        assert len(rsi_basic_values) == len(rsi_momentum_values)
        assert len(rsi_basic_values) == len(rsi_divergence_values)
        
        # RSI values should be identical
        np.testing.assert_array_almost_equal(rsi_basic_values.values, rsi_momentum_values.values)
        np.testing.assert_array_almost_equal(rsi_basic_values.values, rsi_divergence_values.values)
        
        # Each should have unique additional columns
        assert 'RSI_Momentum' in rsi_momentum.columns
        assert 'RSI_Momentum' not in rsi_basic.columns
        assert 'RSI_Momentum' not in rsi_divergence.columns
    
    def test_rsi_with_different_point_sizes(self):
        """Test RSI calculation with different point sizes."""
        df = self.test_data.copy()
        
        # Test with different point sizes
        point_sizes = [0.00001, 0.001, 0.01, 0.1, 1.0]
        
        for point in point_sizes:
            result = calculate_pressure_vector(df, point, TradingRule.RSI)
            
            # RSI calculation should not depend on point size
            assert 'RSI' in result.columns
            assert not result['RSI'].isna().all()
            
            # RSI values should be the same regardless of point size
            if point == point_sizes[0]:
                reference_rsi = result['RSI'].dropna()
            else:
                current_rsi = result['RSI'].dropna()
                np.testing.assert_array_almost_equal(reference_rsi.values, current_rsi.values)
    
    def test_rsi_with_duplicate_indices(self):
        """Test RSI calculation with duplicate indices."""
        df = self.test_data.copy()
        
        # Create duplicate indices
        df.index = pd.DatetimeIndex(['2023-01-01'] * 25 + ['2023-01-02'] * 25)
        
        point = 0.01
        
        # Should handle duplicate indices gracefully
        result = calculate_pressure_vector(df, point, TradingRule.RSI)
        
        assert 'RSI' in result.columns
        assert len(result) <= len(df)  # Should remove duplicates
    
    def test_rsi_with_missing_data(self):
        """Test RSI calculation with missing data."""
        df = self.test_data.copy()
        
        # Add some missing values
        df.loc[df.index[10:15], 'Close'] = np.nan
        df.loc[df.index[20:25], 'High'] = np.nan
        
        point = 0.01
        
        # Should handle missing data gracefully
        result = calculate_pressure_vector(df, point, TradingRule.RSI)
        
        assert 'RSI' in result.columns
        # Should still have some valid RSI values
        assert not result['RSI'].isna().all()
    
    def test_rsi_signal_distribution(self):
        """Test RSI signal distribution across different rules."""
        df = self.test_data.copy()
        point = 0.01
        
        # Test all RSI variants
        rsi_basic = calculate_pressure_vector(df, point, TradingRule.RSI)
        rsi_momentum = calculate_pressure_vector(df, point, TradingRule.RSI_Momentum)
        rsi_divergence = calculate_pressure_vector(df, point, TradingRule.RSI_Divergence)
        
        # Check signal distributions
        for result, name in [(rsi_basic, 'Basic'), (rsi_momentum, 'Momentum'), (rsi_divergence, 'Divergence')]:
            signals = result['Direction'].dropna()
            assert len(signals) > 0, f"No signals generated for {name} RSI"
            
            # Should have valid signal values
            valid_signals = [0.0, 1.0, 2.0]  # NOTRADE, BUY, SELL
            assert signals.isin(valid_signals).all(), f"Invalid signals in {name} RSI"
    
    def test_rsi_output_consistency(self):
        """Test that RSI output is consistent across multiple runs."""
        df = self.test_data.copy()
        point = 0.01
        
        # Run RSI calculation multiple times
        results = []
        for _ in range(3):
            result = calculate_pressure_vector(df, point, TradingRule.RSI)
            results.append(result['RSI'].dropna())
        
        # All results should be identical
        for i in range(1, len(results)):
            np.testing.assert_array_almost_equal(results[0].values, results[i].values)
    
    def test_rsi_with_extreme_volatility(self):
        """Test RSI calculation with extreme volatility data."""
        # Create data with extreme volatility
        dates = pd.date_range('2023-01-01', periods=30, freq='D')
        extreme_prices = []
        current_price = 100.0
        
        for i in range(30):
            # Extreme price movements
            if i % 3 == 0:
                current_price *= 1.5  # 50% increase
            elif i % 3 == 1:
                current_price *= 0.5  # 50% decrease
            else:
                current_price *= 1.1  # 10% increase
            extreme_prices.append(current_price)
        
        extreme_data = pd.DataFrame({
            'Open': extreme_prices,
            'High': [p * 1.02 for p in extreme_prices],
            'Low': [p * 0.98 for p in extreme_prices],
            'Close': extreme_prices,
            'TickVolume': [1000] * 30
        }, index=dates)
        
        point = 0.01
        
        # Should handle extreme volatility
        result = calculate_pressure_vector(extreme_data, point, TradingRule.RSI)
        
        assert 'RSI' in result.columns
        rsi_values = result['RSI'].dropna()
        
        if len(rsi_values) > 0:
            # RSI should still be within valid range
            assert rsi_values.min() >= 0
            assert rsi_values.max() <= 100
    
    def test_rsi_column_renaming(self):
        """Test that TickVolume is properly renamed to Volume."""
        df = self.test_data.copy()
        point = 0.01
        
        result = calculate_pressure_vector(df, point, TradingRule.RSI)
        
        # Should have Volume column (renamed from TickVolume)
        assert 'Volume' in result.columns
        assert 'TickVolume' not in result.columns
        
        # Original data should still have TickVolume
        assert 'TickVolume' in df.columns 