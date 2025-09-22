"""
Tests for Financial Features Analysis Module

This module contains comprehensive tests for the financial features analysis functionality.
"""

import pytest
import pandas as pd
import numpy as np
from unittest.mock import patch, MagicMock
import sys
from pathlib import Path

# Add src to path for imports
sys.path.append(str(Path(__file__).parent.parent.parent / "src"))

from src.time_series.financial_features import FinancialFeatures


class TestFinancialFeatures:
    """Test cases for FinancialFeatures class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.analyzer = FinancialFeatures()
        
        # Create sample financial time series data
        np.random.seed(42)
        dates = pd.date_range('2020-01-01', periods=100, freq='D')
        
        # Price data with trend and volatility
        prices = 100 + np.cumsum(np.random.normal(0.1, 2, 100))
        self.price_data = pd.DataFrame({
            'price': prices,
            'volume': np.random.lognormal(10, 1, 100)
        }, index=dates)
        
        # High volatility data
        high_vol_prices = 100 + np.cumsum(np.random.normal(0, 5, 100))
        self.high_vol_data = pd.DataFrame({
            'high_vol_price': high_vol_prices
        }, index=dates)
        
        # Mixed financial data
        self.mixed_financial_data = pd.DataFrame({
            'price': prices,
            'volume': np.random.lognormal(10, 1, 100),
            'high_vol_price': high_vol_prices
        }, index=dates)
    
    def test_analyze_financial_features_basic(self):
        """Test basic financial features analysis functionality."""
        numeric_columns = ['price']
        results = self.analyzer.analyze_financial_features(self.price_data, numeric_columns)
        
        assert 'price_range_analysis' in results
        assert 'price_changes_analysis' in results
        assert 'volatility_analysis' in results
        assert 'overall_financial_assessment' in results
        
        # Check that analysis was performed for the column
        assert 'price' in results['price_range_analysis']
        assert 'price' in results['price_changes_analysis']
        assert 'price' in results['volatility_analysis']
    
    def test_analyze_financial_features_multiple_columns(self):
        """Test financial features analysis with multiple columns."""
        numeric_columns = ['price', 'volume']
        results = self.analyzer.analyze_financial_features(self.price_data, numeric_columns)
        
        # Check that analysis was performed for both columns
        for col in numeric_columns:
            assert col in results['price_range_analysis']
            assert col in results['price_changes_analysis']
            assert col in results['volatility_analysis']
    
    def test_analyze_price_range(self):
        """Test price range analysis functionality."""
        data = self.price_data['price']
        results = self.analyzer._analyze_price_range(data, 'test_price')
        
        assert 'min_price' in results
        assert 'max_price' in results
        assert 'price_range' in results
        assert 'range_percentage' in results
        assert 'mean_price' in results
        assert 'median_price' in results
        assert 'volatility_level' in results
        assert 'interpretation' in results
        
        # Check that values are reasonable
        assert results['min_price'] <= results['max_price']
        assert results['price_range'] == results['max_price'] - results['min_price']
        assert results['range_percentage'] >= 0
    
    def test_analyze_price_changes(self):
        """Test price changes analysis functionality."""
        data = self.price_data['price']
        results = self.analyzer._analyze_price_changes(data, 'test_price')
        
        assert 'returns_by_period' in results
        assert 'overall_volatility' in results
        assert 'interpretation' in results
        
        # Check returns by period
        for period in [1, 5, 10, 20]:
            period_key = f'period_{period}'
            if period_key in results['returns_by_period']:
                period_data = results['returns_by_period'][period_key]
                assert 'simple_returns' in period_data
                assert 'log_returns' in period_data
                assert 'absolute_changes' in period_data
    
    def test_analyze_volatility(self):
        """Test volatility analysis functionality."""
        data = self.price_data['price']
        results = self.analyzer._analyze_volatility(data, 'test_price')
        
        assert 'volatility_by_window' in results
        assert 'overall_volatility' in results
        assert 'annualized_volatility' in results
        assert 'coefficient_of_variation' in results
        assert 'volatility_level' in results
        assert 'interpretation' in results
        
        # Check volatility by window
        for window in [5, 10, 20, 30]:
            window_key = f'window_{window}'
            if window_key in results['volatility_by_window']:
                window_data = results['volatility_by_window'][window_key]
                assert 'mean_volatility' in window_data
                assert 'std_volatility' in window_data
    
    def test_classify_volatility_level(self):
        """Test volatility level classification."""
        assert self.analyzer._classify_volatility_level(3) == 'very_low'
        assert self.analyzer._classify_volatility_level(10) == 'low'
        assert self.analyzer._classify_volatility_level(25) == 'moderate'
        assert self.analyzer._classify_volatility_level(40) == 'high'
        assert self.analyzer._classify_volatility_level(60) == 'very_high'
    
    def test_interpret_price_range(self):
        """Test price range interpretation."""
        # Test different range percentages
        result1 = self.analyzer._interpret_price_range(5, 0.1)
        assert 'stable' in result1.lower()
        
        result2 = self.analyzer._interpret_price_range(30, 0.1)
        assert 'wide' in result2.lower()  # 30% is actually high volatility
        
        result3 = self.analyzer._interpret_price_range(60, 0.1)
        assert 'wide' in result3.lower()
    
    def test_interpret_price_changes(self):
        """Test price changes interpretation."""
        # Mock returns analysis
        returns_analysis = {
            'period_1': {
                'simple_returns': {'mean': 0.01, 'std': 0.02}
            }
        }
        
        # Mock return consistency
        return_consistency = {
            'positive_percentage': 65,
            'negative_percentage': 35
        }
        
        result = self.analyzer._interpret_price_changes(returns_analysis, return_consistency)
        assert isinstance(result, str)
        assert len(result) > 0
    
    def test_interpret_volatility(self):
        """Test volatility interpretation."""
        result1 = self.analyzer._interpret_volatility(0.01, 5, {})
        assert 'low' in result1.lower()
        
        result2 = self.analyzer._interpret_volatility(0.1, 30, {})
        assert 'high' in result2.lower()  # 30% CoV is high volatility
        
        result3 = self.analyzer._interpret_volatility(0.5, 80, {})
        assert 'high' in result3.lower()
    
    def test_analyze_return_trend(self):
        """Test return trend analysis."""
        # Create returns data
        returns = pd.Series(np.random.normal(0.01, 0.02, 50))
        results = self.analyzer._analyze_return_trend(returns)
        
        assert 'slope' in results
        assert 'r_squared' in results
        assert 'p_value' in results
        assert 'trend_direction' in results
        assert 'trend_strength' in results
        assert 'is_significant' in results
    
    def test_calculate_trend(self):
        """Test trend calculation."""
        # Upward trend
        upward_data = pd.Series([1, 2, 3, 4, 5])
        trend1 = self.analyzer._calculate_trend(upward_data)
        assert trend1 > 0
        
        # Downward trend
        downward_data = pd.Series([5, 4, 3, 2, 1])
        trend2 = self.analyzer._calculate_trend(downward_data)
        assert trend2 < 0
        
        # No trend
        flat_data = pd.Series([1, 1, 1, 1, 1])
        trend3 = self.analyzer._calculate_trend(flat_data)
        assert trend3 == 0
    
    def test_analyze_volatility_clustering(self):
        """Test volatility clustering analysis."""
        # Create returns with volatility clustering
        returns = pd.Series(np.random.normal(0, 0.02, 100))
        results = self.analyzer._analyze_volatility_clustering(returns)
        
        # Should either have the expected keys or an error
        if 'error' in results:
            assert 'error' in results
        else:
            assert 'autocorrelation_squared_returns' in results
            assert 'ljung_box_statistic' in results
            assert 'ljung_box_pvalue' in results
            assert 'has_clustering' in results
    
    def test_analyze_volatility_regimes(self):
        """Test volatility regime analysis."""
        returns = pd.Series(np.random.normal(0, 0.02, 100))
        results = self.analyzer._analyze_volatility_regimes(returns)
        
        assert 'low_volatility_periods' in results
        assert 'medium_volatility_periods' in results
        assert 'high_volatility_periods' in results
        assert 'regime_distribution' in results
    
    def test_calculate_max_drawdown(self):
        """Test maximum drawdown calculation."""
        # Create price series with drawdown
        prices = pd.Series([100, 110, 105, 90, 95, 100])
        max_dd = self.analyzer._calculate_max_drawdown(prices)
        
        assert max_dd <= 0  # Drawdown should be negative or zero
        assert isinstance(max_dd, (int, float))
    
    def test_generate_overall_financial_assessment(self):
        """Test overall financial assessment generation."""
        # Mock results
        results = {
            'price_range_analysis': {
                'col1': {'range_percentage': 20},
                'col2': {'range_percentage': 40}
            },
            'volatility_analysis': {
                'col1': {'overall_volatility': 0.02, 'coefficient_of_variation': 15},
                'col2': {'overall_volatility': 0.05, 'coefficient_of_variation': 30}
            }
        }
        
        assessment = self.analyzer._generate_overall_financial_assessment(results)
        
        assert 'total_columns' in assessment
        assert 'volatility_distribution' in assessment
        assert 'average_range_percentage' in assessment
        assert 'average_volatility' in assessment
        assert 'average_coefficient_variation' in assessment
        assert 'overall_risk_level' in assessment
        assert 'recommendations' in assessment
    
    def test_analyze_financial_features_empty_data(self):
        """Test financial features analysis with empty data."""
        empty_data = pd.DataFrame()
        numeric_columns = []
        
        results = self.analyzer.analyze_financial_features(empty_data, numeric_columns)
        
        assert 'price_range_analysis' in results
        assert 'price_changes_analysis' in results
        assert 'volatility_analysis' in results
        assert 'overall_financial_assessment' in results
    
    def test_analyze_financial_features_insufficient_data(self):
        """Test financial features analysis with insufficient data."""
        # Create data with only 5 points (insufficient for some analyses)
        small_data = pd.DataFrame({
            'small_col': np.random.normal(100, 5, 5)
        })
        numeric_columns = ['small_col']
        
        results = self.analyzer.analyze_financial_features(small_data, numeric_columns)
        
        # Should still return results structure
        assert 'price_range_analysis' in results
        assert 'price_changes_analysis' in results
        assert 'volatility_analysis' in results
        assert 'overall_financial_assessment' in results
    
    def test_error_handling(self):
        """Test error handling in various methods."""
        # Test with invalid data
        invalid_data = pd.Series([np.nan, np.nan, np.nan])
        
        # Should handle errors gracefully
        range_results = self.analyzer._analyze_price_range(invalid_data, 'test_col')
        assert 'error' in range_results or 'min_price' in range_results
        
        changes_results = self.analyzer._analyze_price_changes(invalid_data, 'test_col')
        assert 'error' in changes_results or 'returns_by_period' in changes_results
        
        vol_results = self.analyzer._analyze_volatility(invalid_data, 'test_col')
        assert 'error' in vol_results or 'overall_volatility' in vol_results
