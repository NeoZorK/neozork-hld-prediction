"""
Tests for Stationarity Analysis Module

This module contains comprehensive tests for the stationarity analysis functionality.
"""

import pytest
import pandas as pd
import numpy as np
from unittest.mock import patch, MagicMock
import sys
from pathlib import Path

# Add src to path for imports
sys.path.append(str(Path(__file__).parent.parent.parent / "src"))

from src.time_series.stationarity_analysis import StationarityAnalysis


class TestStationarityAnalysis:
    """Test cases for StationarityAnalysis class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.analyzer = StationarityAnalysis()
        
        # Create sample time series data
        np.random.seed(42)
        dates = pd.date_range('2020-01-01', periods=100, freq='D')
        
        # Stationary data (white noise)
        self.stationary_data = pd.DataFrame({
            'stationary_col': np.random.normal(0, 1, 100)
        }, index=dates)
        
        # Non-stationary data (with trend)
        trend = np.linspace(0, 10, 100)
        noise = np.random.normal(0, 0.5, 100)
        self.non_stationary_data = pd.DataFrame({
            'trend_col': trend + noise
        }, index=dates)
        
        # Mixed data
        self.mixed_data = pd.DataFrame({
            'stationary_col': np.random.normal(0, 1, 100),
            'trend_col': np.linspace(0, 10, 100) + np.random.normal(0, 0.5, 100)
        }, index=dates)
    
    def test_analyze_stationarity_basic(self):
        """Test basic stationarity analysis functionality."""
        numeric_columns = ['stationary_col']
        results = self.analyzer.analyze_stationarity(self.stationary_data, numeric_columns)
        
        assert 'adf_tests' in results
        assert 'critical_values' in results
        assert 'stationarity_recommendations' in results
        assert 'overall_assessment' in results
        
        # Check that analysis was performed for the column
        assert 'stationary_col' in results['adf_tests']
        assert 'stationary_col' in results['critical_values']
        assert 'stationary_col' in results['stationarity_recommendations']
    
    def test_analyze_stationarity_multiple_columns(self):
        """Test stationarity analysis with multiple columns."""
        numeric_columns = ['stationary_col', 'trend_col']
        results = self.analyzer.analyze_stationarity(self.mixed_data, numeric_columns)
        
        # Check that analysis was performed for both columns
        for col in numeric_columns:
            assert col in results['adf_tests']
            assert col in results['critical_values']
            assert col in results['stationarity_recommendations']
    
    def test_perform_adf_test_stationary_data(self):
        """Test ADF test on stationary data."""
        data = self.stationary_data['stationary_col']
        results = self.analyzer._perform_adf_test(data, 'test_col')
        
        assert 'standard' in results
        assert 'with_trend' in results
        assert 'with_constant' in results
        assert 'best_specification' in results
        
        # Check that results contain expected keys
        for spec in ['standard', 'with_trend', 'with_constant']:
            if results[spec]:
                assert 'adf_statistic' in results[spec]
                assert 'p_value' in results[spec]
                assert 'is_stationary' in results[spec]
    
    def test_perform_adf_test_non_stationary_data(self):
        """Test ADF test on non-stationary data."""
        data = self.non_stationary_data['trend_col']
        results = self.analyzer._perform_adf_test(data, 'test_col')
        
        assert 'standard' in results
        assert 'with_trend' in results
        assert 'with_constant' in results
        assert 'best_specification' in results
    
    def test_get_critical_values(self):
        """Test critical values calculation."""
        data = self.stationary_data['stationary_col']
        results = self.analyzer._get_critical_values(data, 'test_col')
        
        assert 'sample_size' in results
        assert 'critical_values' in results
        assert 'interpretation' in results
        
        if 'critical_values' in results and results['critical_values']:
            assert '1%' in results['critical_values']
            assert '5%' in results['critical_values']
            assert '10%' in results['critical_values']
    
    def test_generate_stationarity_recommendations(self):
        """Test stationarity recommendations generation."""
        # Mock ADF results for stationary data
        adf_results = {
            'standard': {
                'adf_statistic': -3.5,
                'p_value': 0.01,
                'is_stationary': True
            },
            'best_specification': 'standard'
        }
        
        # Mock critical values
        critical_vals = {
            'critical_values': {'1%': -3.43, '5%': -2.86, '10%': -2.57}
        }
        
        data = self.stationary_data['stationary_col']
        results = self.analyzer._generate_stationarity_recommendations(
            adf_results, critical_vals, data, 'test_col'
        )
        
        assert 'is_stationary' in results
        assert 'confidence_level' in results
        assert 'recommended_actions' in results
        assert 'differencing_suggestions' in results
        assert 'transformation_suggestions' in results
    
    def test_has_trend(self):
        """Test trend detection functionality."""
        # Data with clear trend
        trend_data = pd.Series(np.linspace(0, 10, 50))
        assert self.analyzer._has_trend(trend_data) == True
        
        # Data without trend (stationary)
        stationary_data = pd.Series(np.random.normal(0, 1, 50))
        # Note: This might be True or False depending on random data
        # We just test that the method runs without error
        result = self.analyzer._has_trend(stationary_data)
        assert isinstance(result, (bool, np.bool_))
    
    def test_has_seasonality(self):
        """Test seasonality detection functionality."""
        # Create seasonal data
        t = np.arange(100)
        seasonal_data = pd.Series(10 * np.sin(2 * np.pi * t / 12) + np.random.normal(0, 1, 100))
        
        # Test seasonality detection
        result = self.analyzer._has_seasonality(seasonal_data)
        assert isinstance(result, (bool, np.bool_))
    
    def test_has_heteroscedasticity(self):
        """Test heteroscedasticity detection functionality."""
        # Create data with changing variance
        n = 100
        x = np.arange(n)
        y = np.concatenate([
            np.random.normal(0, 1, n//2),
            np.random.normal(0, 3, n//2)
        ])
        hetero_data = pd.Series(y)
        
        result = self.analyzer._has_heteroscedasticity(hetero_data)
        assert isinstance(result, (bool, np.bool_))
    
    def test_generate_overall_assessment(self):
        """Test overall assessment generation."""
        # Mock results
        results = {
            'adf_tests': {
                'col1': {'standard': {'p_value': 0.01}},
                'col2': {'standard': {'p_value': 0.8}}
            },
            'stationarity_recommendations': {
                'col1': {'is_stationary': True},
                'col2': {'is_stationary': False}
            }
        }
        
        assessment = self.analyzer._generate_overall_assessment(results)
        
        assert 'total_columns' in assessment
        assert 'stationary_columns' in assessment
        assert 'non_stationary_columns' in assessment
        assert 'stationarity_rate' in assessment
        assert 'overall_quality' in assessment
        assert 'recommendations' in assessment
    
    def test_analyze_stationarity_empty_data(self):
        """Test stationarity analysis with empty data."""
        empty_data = pd.DataFrame()
        numeric_columns = []
        
        results = self.analyzer.analyze_stationarity(empty_data, numeric_columns)
        
        assert 'adf_tests' in results
        assert 'critical_values' in results
        assert 'stationarity_recommendations' in results
        assert 'overall_assessment' in results
    
    def test_analyze_stationarity_insufficient_data(self):
        """Test stationarity analysis with insufficient data."""
        # Create data with only 5 points (insufficient for ADF test)
        small_data = pd.DataFrame({
            'small_col': np.random.normal(0, 1, 5)
        })
        numeric_columns = ['small_col']
        
        results = self.analyzer.analyze_stationarity(small_data, numeric_columns)
        
        # Should still return results structure but with empty analysis
        assert 'adf_tests' in results
        assert 'critical_values' in results
        assert 'stationarity_recommendations' in results
        assert 'overall_assessment' in results
    
    def test_error_handling(self):
        """Test error handling in various methods."""
        # Test with invalid data
        invalid_data = pd.Series([np.nan, np.nan, np.nan])
        
        # Should handle errors gracefully
        adf_results = self.analyzer._perform_adf_test(invalid_data, 'test_col')
        assert 'error' in adf_results or 'standard' in adf_results
        
        critical_results = self.analyzer._get_critical_values(invalid_data, 'test_col')
        assert 'error' in critical_results or 'sample_size' in critical_results
