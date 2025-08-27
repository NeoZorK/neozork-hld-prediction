# -*- coding: utf-8 -*-
"""
Tests for time series analysis module.

This module tests the TimeSeriesAnalyzer class and related functions
for comprehensive time series analysis capabilities.
"""

import pytest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path
import tempfile
import shutil
import os

from src.eda.time_series_analysis import TimeSeriesAnalyzer, analyze_time_series


class TestTimeSeriesAnalyzer:
    """Test cases for TimeSeriesAnalyzer class."""
    
    @pytest.fixture
    def sample_data(self):
        """Create sample time series data for testing."""
        # Create a synthetic time series with trend, seasonality, and noise
        np.random.seed(42)
        n_points = 200
        
        # Create datetime index
        dates = pd.date_range(start='2020-01-01', periods=n_points, freq='D')
        
        # Create trend component
        trend = np.linspace(100, 120, n_points)
        
        # Create seasonal component (weekly seasonality)
        seasonal = 5 * np.sin(2 * np.pi * np.arange(n_points) / 7)
        
        # Create noise component
        noise = np.random.normal(0, 2, n_points)
        
        # Combine components
        values = trend + seasonal + noise
        
        # Create DataFrame
        df = pd.DataFrame({
            'date': dates,
            'value': values,
            'price': values + 50,  # Another column for testing
            'volume': np.random.randint(1000, 10000, n_points)
        })
        
        return df
    
    @pytest.fixture
    def analyzer(self, sample_data):
        """Create TimeSeriesAnalyzer instance with sample data."""
        return TimeSeriesAnalyzer(sample_data)
    
    def test_initialization(self):
        """Test TimeSeriesAnalyzer initialization."""
        # Test with data
        data = pd.DataFrame({'value': [1, 2, 3, 4, 5]})
        analyzer = TimeSeriesAnalyzer(data)
        assert analyzer.data is not None
        assert len(analyzer.results) == 0
        
        # Test without data
        analyzer = TimeSeriesAnalyzer()
        assert analyzer.data is None
        assert len(analyzer.results) == 0
        
    def test_set_data(self, analyzer):
        """Test set_data method."""
        new_data = pd.DataFrame({'new_value': [10, 20, 30]})
        analyzer.set_data(new_data)
        assert analyzer.data is not None
        assert 'new_value' in analyzer.data.columns
        
    def test_ensure_plots_directory(self, analyzer):
        """Test plots directory creation."""
        plots_dir = analyzer._ensure_plots_directory()
        assert isinstance(plots_dir, Path)
        assert plots_dir.exists()
        assert plots_dir.is_dir()
        
    def test_ensure_datetime_index(self, analyzer):
        """Test datetime index creation."""
        # Test with existing datetime index
        df = pd.DataFrame({'value': [1, 2, 3]})
        df.index = pd.date_range('2020-01-01', periods=3)
        result = analyzer._ensure_datetime_index(df)
        assert isinstance(result.index, pd.DatetimeIndex)
        
        # Test with date column
        df = pd.DataFrame({
            'date': ['2020-01-01', '2020-01-02', '2020-01-03'],
            'value': [1, 2, 3]
        })
        result = analyzer._ensure_datetime_index(df)
        assert isinstance(result.index, pd.DatetimeIndex)
        
        # Test with no date column
        df = pd.DataFrame({'value': [1, 2, 3]})
        result = analyzer._ensure_datetime_index(df)
        assert isinstance(result.index, pd.DatetimeIndex)
        
    def test_analyze_stationarity(self, analyzer):
        """Test stationarity analysis."""
        # Test with valid data
        result = analyzer.analyze_stationarity('value')
        
        assert 'column' in result
        assert 'length' in result
        assert 'tests' in result
        assert 'plot_path' in result
        
        assert result['column'] == 'value'
        assert result['length'] > 0
        
        # Check if tests were performed
        if 'adf' in result['tests'] and 'error' not in result['tests']['adf']:
            assert 'statistic' in result['tests']['adf']
            assert 'p_value' in result['tests']['adf']
            assert 'is_stationary' in result['tests']['adf']
            
        if 'kpss' in result['tests'] and 'error' not in result['tests']['kpss']:
            assert 'statistic' in result['tests']['kpss']
            assert 'p_value' in result['tests']['kpss']
            assert 'is_stationary' in result['tests']['kpss']
            
        # Test with insufficient data
        small_data = pd.DataFrame({'value': [1, 2, 3, 4, 5]})
        small_analyzer = TimeSeriesAnalyzer(small_data)
        
        with pytest.raises(ValueError, match="Insufficient data"):
            small_analyzer.analyze_stationarity('value')
            
        # Test with no data
        empty_analyzer = TimeSeriesAnalyzer()
        with pytest.raises(ValueError, match="No data provided"):
            empty_analyzer.analyze_stationarity()
            
    def test_analyze_trends(self, analyzer):
        """Test trend analysis."""
        # Test with valid data
        result = analyzer.analyze_trends('value')
        
        assert 'column' in result
        assert 'window' in result
        assert 'trend_analysis' in result
        assert 'plot_path' in result
        
        assert result['column'] == 'value'
        assert result['window'] > 0
        
        # Check trend analysis results
        trend_analysis = result['trend_analysis']
        if 'linear' in trend_analysis:
            assert 'slope' in trend_analysis['linear']
            assert 'intercept' in trend_analysis['linear']
            assert 'r_squared' in trend_analysis['linear']
            assert 'trend_direction' in trend_analysis['linear']
            
        if 'moving_averages' in trend_analysis:
            assert 'short_ma_window' in trend_analysis['moving_averages']
            assert 'long_ma_window' in trend_analysis['moving_averages']
            assert 'trend_strength' in trend_analysis['moving_averages']
            
        # Test with custom window
        result = analyzer.analyze_trends('value', window=10)
        assert result['window'] == 10
        
    def test_analyze_seasonality(self, analyzer):
        """Test seasonality analysis."""
        # Test with valid data
        result = analyzer.analyze_seasonality('value')
        
        assert 'column' in result
        assert 'detected_period' in result
        assert 'seasonality_analysis' in result
        assert 'plot_path' in result
        
        assert result['column'] == 'value'
        assert result['detected_period'] > 0
        
        # Check seasonality analysis results
        seasonality_analysis = result['seasonality_analysis']
        if 'decomposition' in seasonality_analysis and 'error' not in seasonality_analysis['decomposition']:
            decomp = seasonality_analysis['decomposition']
            assert 'trend' in decomp
            assert 'seasonal' in decomp
            assert 'residual' in decomp
            assert 'seasonal_strength' in decomp
            assert 'has_seasonality' in decomp
            
        # Test with custom period
        result = analyzer.analyze_seasonality('value', period=14)
        assert result['detected_period'] == 14
        
        # Test with insufficient data
        small_data = pd.DataFrame({'value': [1] * 50})  # Less than 100 points
        small_analyzer = TimeSeriesAnalyzer(small_data)
        
        with pytest.raises(ValueError, match="Insufficient data"):
            small_analyzer.analyze_seasonality('value')
            
    def test_analyze_volatility(self, analyzer):
        """Test volatility analysis."""
        # Test with valid data - use smaller dataset for faster execution
        result = analyzer.analyze_volatility('value')
        
        assert 'column' in result
        assert 'window' in result
        assert 'volatility_analysis' in result
        assert 'plot_path' in result
        
        assert result['column'] == 'value'
        assert result['window'] > 0
        
        # Check volatility analysis results
        volatility_analysis = result['volatility_analysis']
        assert 'mean_volatility' in volatility_analysis
        assert 'volatility_of_volatility' in volatility_analysis
        assert 'volatility_clustering' in volatility_analysis
        assert 'has_clustering' in volatility_analysis
        assert 'min_volatility' in volatility_analysis
        assert 'max_volatility' in volatility_analysis
        assert 'volatility_percentiles' in volatility_analysis
        
        # Test with custom window
        result = analyzer.analyze_volatility('value', window=15)
        assert result['window'] == 15
        
    def test_analyze_autocorrelation(self, analyzer):
        """Test autocorrelation analysis."""
        # Test with valid data - simplified for faster execution
        result = analyzer.analyze_autocorrelation('value', max_lag=10)  # Reduced max_lag
        
        assert 'column' in result
        assert 'max_lag' in result
        assert 'autocorrelation_analysis' in result
        assert 'plot_path' in result
        
        assert result['column'] == 'value'
        assert result['max_lag'] == 10
        
        # Check autocorrelation analysis results
        autocorr_analysis = result['autocorrelation_analysis']
        if 'error' not in autocorr_analysis:
            assert 'acf_values' in autocorr_analysis
            assert 'pacf_values' in autocorr_analysis
            assert 'confidence_interval' in autocorr_analysis
            assert 'significant_acf_lags' in autocorr_analysis
            assert 'significant_pacf_lags' in autocorr_analysis
            assert 'max_acf_lag' in autocorr_analysis
            assert 'max_pacf_lag' in autocorr_analysis
            
        # Test with custom max_lag
        result = analyzer.analyze_autocorrelation('value', max_lag=20)
        assert result['max_lag'] == 20
        
    def test_forecast_series(self, analyzer):
        """Test forecasting functionality."""
        # Test with valid data - simplified for faster execution
        result = analyzer.forecast_series('value', periods=5)  # Reduced periods
        
        assert 'column' in result
        assert 'periods' in result
        assert 'model_type' in result
        assert 'forecast_results' in result
        assert 'plot_path' in result
        
        assert result['column'] == 'value'
        assert result['periods'] == 5
        
        # Check forecast results
        forecast_results = result['forecast_results']
        if 'forecasts' in forecast_results:
            forecasts = forecast_results['forecasts']
            
            # Check if at least one forecast method worked
            forecast_methods = ['naive', 'seasonal_naive', 'arima']
            working_methods = [method for method in forecast_methods 
                             if method in forecasts and isinstance(forecasts[method], list)]
            
            assert len(working_methods) > 0, "At least one forecast method should work"
            
        # Test with insufficient data
        small_data = pd.DataFrame({'value': [1] * 30})  # Less than 50 points
        small_analyzer = TimeSeriesAnalyzer(small_data)
        
        with pytest.raises(ValueError, match="Insufficient data"):
            small_analyzer.forecast_series('value')

    def test_comprehensive_analysis_basic(self, analyzer):
        """Test comprehensive analysis basic structure."""
        # Test with valid data - simplified version
        result = analyzer.comprehensive_analysis('value')
        
        assert 'timestamp' in result
        assert 'column' in result
        assert 'analyses' in result
        assert 'summary' in result
        assert 'results_file' in result
        
        assert result['column'] == 'value'
        
        # Check that all analyses were attempted
        analyses = result['analyses']
        expected_analyses = ['stationarity', 'trends', 'seasonality', 
                           'volatility', 'autocorrelation', 'forecast']
        
        for analysis in expected_analyses:
            assert analysis in analyses
            
        # Check summary
        summary = result['summary']
        assert 'key_findings' in summary
        assert 'recommendations' in summary
        assert 'data_characteristics' in summary

    def test_comprehensive_analysis_no_data(self, analyzer):
        """Test comprehensive analysis with no data."""
        # Test with no data
        empty_analyzer = TimeSeriesAnalyzer()
        with pytest.raises(ValueError, match="No data provided"):
            empty_analyzer.comprehensive_analysis()

    def test_comprehensive_analysis_small_dataset(self, analyzer):
        """Test comprehensive analysis with smaller dataset for faster execution."""
        # Create smaller dataset for faster testing
        small_data = pd.DataFrame({
            'value': np.random.randn(50) + 100,  # Smaller dataset
            'date': pd.date_range('2020-01-01', periods=50, freq='D')
        })
        small_analyzer = TimeSeriesAnalyzer(small_data)
        
        result = small_analyzer.comprehensive_analysis('value')
        
        assert 'timestamp' in result
        assert 'column' in result
        assert 'analyses' in result
        assert 'summary' in result
        assert result['column'] == 'value'
            
    def test_generate_analysis_summary(self, analyzer):
        """Test analysis summary generation."""
        # Create mock analyses results
        mock_analyses = {
            'stationarity': {
                'tests': {
                    'adf': {'is_stationary': True, 'p_value': 0.01},
                    'kpss': {'is_stationary': True, 'p_value': 0.1}
                }
            },
            'trends': {
                'trend_analysis': {
                    'linear': {
                        'trend_direction': 'increasing',
                        'r_squared': 0.7
                    }
                }
            },
            'seasonality': {
                'seasonality_analysis': {
                    'decomposition': {
                        'seasonal_strength': 0.3,
                        'has_seasonality': True
                    }
                }
            },
            'volatility': {
                'volatility_analysis': {
                    'has_clustering': True
                }
            },
            'autocorrelation': {
                'autocorrelation_analysis': {
                    'max_acf_lag': 5
                }
            }
        }
        
        summary = analyzer._generate_analysis_summary(mock_analyses)
        
        assert 'key_findings' in summary
        assert 'recommendations' in summary
        assert 'data_characteristics' in summary
        
        assert len(summary['key_findings']) > 0
        assert len(summary['recommendations']) > 0
        
    def test_get_results(self, analyzer):
        """Test get_results method."""
        # Initially should be empty
        results = analyzer.get_results()
        assert len(results) == 0
        
        # After running analysis, should have results
        analyzer.analyze_stationarity('value')
        results = analyzer.get_results()
        assert len(results) > 0
        assert 'stationarity' in results
        
    def test_export_results(self, analyzer):
        """Test results export functionality."""
        # Run some analysis first
        analyzer.analyze_stationarity('value')
        
        # Test export with default path
        export_path = analyzer.export_results()
        assert Path(export_path).exists()
        
        # Test export with custom path
        with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as tmp:
            custom_path = tmp.name
            
        try:
            export_path = analyzer.export_results(custom_path)
            assert Path(export_path).exists()
        finally:
            # Clean up
            if Path(custom_path).exists():
                os.unlink(custom_path)
                
    def test_error_handling(self):
        """Test error handling for various edge cases."""
        # Test with empty DataFrame
        empty_df = pd.DataFrame()
        analyzer = TimeSeriesAnalyzer(empty_df)
        
        with pytest.raises(ValueError, match="No numeric columns found"):
            analyzer.analyze_stationarity()
            
        # Test with DataFrame containing only non-numeric columns
        text_df = pd.DataFrame({'text': ['a', 'b', 'c']})
        analyzer = TimeSeriesAnalyzer(text_df)
        
        with pytest.raises(ValueError, match="No numeric columns found"):
            analyzer.analyze_stationarity()
            
        # Test with DataFrame containing all NaN values
        nan_df = pd.DataFrame({'value': [np.nan, np.nan, np.nan]})
        analyzer = TimeSeriesAnalyzer(nan_df)
        
        with pytest.raises(ValueError, match="No numeric columns found"):
            analyzer.analyze_stationarity('value')


class TestAnalyzeTimeSeriesFunction:
    """Test cases for the convenience function."""
    
    def test_analyze_time_series_function(self):
        """Test the convenience function."""
        # Create sample data
        data = pd.DataFrame({
            'value': np.random.randn(100).cumsum() + 100,
            'date': pd.date_range('2020-01-01', periods=100, freq='D')
        })
        
        # Test function
        result = analyze_time_series(data, 'value')
        
        assert 'timestamp' in result
        assert 'column' in result
        assert 'analyses' in result
        assert 'summary' in result
        
        assert result['column'] == 'value'
        
    def test_analyze_time_series_without_column(self):
        """Test convenience function without specifying column."""
        # Create sample data
        data = pd.DataFrame({
            'price': np.random.randn(100).cumsum() + 100,
            'volume': np.random.randint(1000, 10000, 100)
        })
        
        # Test function without specifying column (should use first numeric column)
        result = analyze_time_series(data)
        
        assert 'column' in result
        # Should use 'price' as it's the first numeric column
        assert result['column'] == 'price'


class TestIntegration:
    """Integration tests for the time series analysis module."""
    
    def test_full_workflow(self):
        """Test the complete workflow from data loading to results export."""
        # Create comprehensive test data
        np.random.seed(42)
        n_points = 300
        
        # Create datetime index
        dates = pd.date_range(start='2020-01-01', periods=n_points, freq='D')
        
        # Create complex time series with multiple components
        trend = np.linspace(100, 150, n_points)
        seasonal = 10 * np.sin(2 * np.pi * np.arange(n_points) / 30)  # Monthly seasonality
        cyclical = 5 * np.sin(2 * np.pi * np.arange(n_points) / 7)   # Weekly cycles
        noise = np.random.normal(0, 3, n_points)
        
        values = trend + seasonal + cyclical + noise
        
        # Create DataFrame
        df = pd.DataFrame({
            'date': dates,
            'close': values,
            'volume': np.random.randint(1000, 10000, n_points)
        })
        
        # Initialize analyzer
        analyzer = TimeSeriesAnalyzer(df)
        
        # Run comprehensive analysis
        result = analyzer.comprehensive_analysis('close')
        
        # Verify results structure
        assert 'timestamp' in result
        assert 'column' in result
        assert 'analyses' in result
        assert 'summary' in result
        assert 'results_file' in result
        
        # Verify all analyses were performed
        analyses = result['analyses']
        expected_analyses = ['stationarity', 'trends', 'seasonality', 
                           'volatility', 'autocorrelation', 'forecast']
        
        for analysis in expected_analyses:
            assert analysis in analyses
            
        # Verify summary contains insights
        summary = result['summary']
        assert len(summary['key_findings']) > 0
        assert len(summary['recommendations']) > 0
        
        # Test results export
        export_path = analyzer.export_results()
        assert Path(export_path).exists()
        
        # Verify exported file contains data
        with open(export_path, 'r') as f:
            exported_data = f.read()
            assert len(exported_data) > 0
            
    def test_multiple_columns_analysis(self):
        """Test analysis of multiple columns."""
        # Create test data with multiple columns
        np.random.seed(42)
        n_points = 200
        
        dates = pd.date_range(start='2020-01-01', periods=n_points, freq='D')
        
        df = pd.DataFrame({
            'date': dates,
            'price': np.random.randn(n_points).cumsum() + 100,
            'volume': np.random.randint(1000, 10000, n_points),
            'returns': np.random.randn(n_points) * 0.02
        })
        
        analyzer = TimeSeriesAnalyzer(df)
        
        # Analyze different columns
        price_result = analyzer.analyze_stationarity('price')
        volume_result = analyzer.analyze_trends('volume')
        returns_result = analyzer.analyze_volatility('returns')
        
        # Verify results
        assert price_result['column'] == 'price'
        assert volume_result['column'] == 'volume'
        assert returns_result['column'] == 'returns'
        
        # Verify all results are stored
        all_results = analyzer.get_results()
        assert 'stationarity' in all_results
        assert 'trends' in all_results
        assert 'volatility' in all_results


if __name__ == "__main__":
    pytest.main([__file__])
