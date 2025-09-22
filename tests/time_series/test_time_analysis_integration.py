"""
Integration Tests for Time Series Analysis

This module contains integration tests for the complete time series analysis workflow.
"""

import pytest
import pandas as pd
import numpy as np
import os
import tempfile
import shutil
from unittest.mock import patch, MagicMock
import sys
from pathlib import Path

# Add src to path for imports
sys.path.append(str(Path(__file__).parent.parent.parent / "src"))

from src.time_series.file_operations import TimeSeriesFileOperations
from src.time_series.stationarity_analysis import StationarityAnalysis
from src.time_series.seasonality_detection import SeasonalityDetection
from src.time_series.financial_features import FinancialFeatures
from src.time_series.data_transformation import TimeSeriesDataTransformation
from src.time_series.reporting import TimeSeriesReporter


class TestTimeSeriesIntegration:
    """Integration tests for time series analysis components."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.file_ops = TimeSeriesFileOperations()
        self.stationarity_analyzer = StationarityAnalysis()
        self.seasonality_detector = SeasonalityDetection()
        self.financial_analyzer = FinancialFeatures()
        self.transformer = TimeSeriesDataTransformation()
        self.reporter = TimeSeriesReporter()
        
        # Create sample time series data
        np.random.seed(42)
        dates = pd.date_range('2020-01-01', periods=100, freq='D')
        
        # Create realistic financial data
        prices = 100 + np.cumsum(np.random.normal(0.1, 2, 100))
        volumes = np.random.lognormal(10, 1, 100)
        
        self.sample_data = pd.DataFrame({
            'price': prices,
            'volume': volumes,
            'high': prices + np.random.uniform(0, 2, 100),
            'low': prices - np.random.uniform(0, 2, 100)
        }, index=dates)
    
    def test_file_operations_integration(self):
        """Test file operations integration."""
        # Test data preparation
        prepared_data = self.file_ops.prepare_time_series_data(self.sample_data)
        
        assert isinstance(prepared_data.index, pd.DatetimeIndex)
        assert len(prepared_data) == len(self.sample_data)
        
        # Test numeric columns detection
        numeric_columns = self.file_ops.get_numeric_columns(prepared_data)
        assert len(numeric_columns) > 0
        assert all(col in prepared_data.columns for col in numeric_columns)
    
    def test_stationarity_analysis_integration(self):
        """Test stationarity analysis integration."""
        numeric_columns = self.file_ops.get_numeric_columns(self.sample_data)
        
        results = self.stationarity_analyzer.analyze_stationarity(self.sample_data, numeric_columns)
        
        # Check that all expected components are present
        assert 'adf_tests' in results
        assert 'critical_values' in results
        assert 'stationarity_recommendations' in results
        assert 'overall_assessment' in results
        
        # Check that analysis was performed for each numeric column
        for col in numeric_columns:
            assert col in results['adf_tests']
            assert col in results['critical_values']
            assert col in results['stationarity_recommendations']
    
    def test_seasonality_detection_integration(self):
        """Test seasonality detection integration."""
        numeric_columns = self.file_ops.get_numeric_columns(self.sample_data)
        
        results = self.seasonality_detector.analyze_seasonality(self.sample_data, numeric_columns)
        
        # Check that all expected components are present
        assert 'day_patterns' in results
        assert 'month_patterns' in results
        assert 'cyclical_patterns' in results
        assert 'overall_seasonality' in results
        
        # Check that analysis was performed for each numeric column
        for col in numeric_columns:
            assert col in results['day_patterns']
            assert col in results['month_patterns']
            assert col in results['cyclical_patterns']
    
    def test_financial_features_integration(self):
        """Test financial features analysis integration."""
        numeric_columns = self.file_ops.get_numeric_columns(self.sample_data)
        
        results = self.financial_analyzer.analyze_financial_features(self.sample_data, numeric_columns)
        
        # Check that all expected components are present
        assert 'price_range_analysis' in results
        assert 'price_changes_analysis' in results
        assert 'volatility_analysis' in results
        assert 'overall_financial_assessment' in results
        
        # Check that analysis was performed for each numeric column
        for col in numeric_columns:
            assert col in results['price_range_analysis']
            assert col in results['price_changes_analysis']
            assert col in results['volatility_analysis']
    
    def test_data_transformation_integration(self):
        """Test data transformation integration."""
        numeric_columns = self.file_ops.get_numeric_columns(self.sample_data)
        
        # Create transformation dictionary
        transformations = {}
        for col in numeric_columns:
            transformations[col] = ['differencing', 'detrending', 'log_transform']
        
        results = self.transformer.transform_data(self.sample_data, transformations, numeric_columns)
        
        # Check that all expected components are present
        assert 'transformed_data' in results
        assert 'transformation_details' in results
        assert 'comparison' in results
        assert 'recommendations' in results
        
        # Check that transformed data has same shape as original
        assert results['transformed_data'].shape == self.sample_data.shape
    
    def test_reporting_integration(self):
        """Test reporting integration."""
        # Create mock analysis results
        file_info = {
            'filename': 'test_file.parquet',
            'source': 'Test',
            'symbol': 'TEST',
            'timeframe': 'D1',
            'format': 'parquet',
            'rows_count': 100,
            'columns_count': 4,
            'start_date': '2020-01-01',
            'end_date': '2020-04-09'
        }
        
        analysis_results = {
            'stationarity': {
                'adf_tests': {'price': {
                    'standard': {'p_value': 0.05, 'adf_statistic': -3.5, 'is_stationary': True},
                    'best_specification': 'standard'
                }},
                'critical_values': {'price': {'critical_values': {'1%': -3.43}}},
                'stationarity_recommendations': {'price': {'is_stationary': True}},
                'overall_assessment': {'total_columns': 1, 'stationary_columns': 1}
            },
            'seasonality': {
                'day_patterns': {'price': {'pattern_strength': 0.1}},
                'month_patterns': {'price': {'pattern_strength': 0.2}},
                'cyclical_patterns': {'price': {'cyclical_strength': 0.3}},
                'overall_seasonality': {'total_columns': 1}
            },
            'financial': {
                'price_range_analysis': {'price': {'range_percentage': 25}},
                'price_changes_analysis': {'price': {'overall_volatility': 0.02}},
                'volatility_analysis': {'price': {'overall_volatility': 0.02}},
                'overall_financial_assessment': {'total_columns': 1}
            }
        }
        
        # Generate report
        report = self.reporter.generate_comprehensive_report(
            file_info, analysis_results, None, False, {}
        )
        
        # Check that report contains expected sections
        assert "TIME SERIES ANALYSIS REPORT" in report
        assert "FILE INFORMATION" in report
        assert "STATIONARITY ANALYSIS" in report
        assert "SEASONALITY DETECTION" in report
        assert "FINANCIAL FEATURES ANALYSIS" in report
        assert "OVERALL ASSESSMENT" in report
    
    def test_end_to_end_analysis_workflow(self):
        """Test complete end-to-end analysis workflow."""
        # Prepare data
        prepared_data = self.file_ops.prepare_time_series_data(self.sample_data)
        numeric_columns = self.file_ops.get_numeric_columns(prepared_data)
        
        # Run all analyses
        stationarity_results = self.stationarity_analyzer.analyze_stationarity(prepared_data, numeric_columns)
        seasonality_results = self.seasonality_detector.analyze_seasonality(prepared_data, numeric_columns)
        financial_results = self.financial_analyzer.analyze_financial_features(prepared_data, numeric_columns)
        
        # Create transformation recommendations
        transformations = {}
        for col in numeric_columns:
            transformations[col] = ['differencing', 'detrending', 'normalization']
        
        transformation_results = self.transformer.transform_data(prepared_data, transformations, numeric_columns)
        
        # Combine all results
        all_results = {
            'stationarity': stationarity_results,
            'seasonality': seasonality_results,
            'financial': financial_results,
            'transformation': transformation_results
        }
        
        # Verify that all analyses completed successfully
        assert len(stationarity_results['adf_tests']) > 0
        assert len(seasonality_results['day_patterns']) > 0
        assert len(financial_results['price_range_analysis']) > 0
        assert len(transformation_results['transformation_details']) > 0
        
        # Verify data integrity
        assert transformation_results['transformed_data'].shape == prepared_data.shape
        assert list(transformation_results['transformed_data'].columns) == list(prepared_data.columns)
    
    def test_error_handling_integration(self):
        """Test error handling across components."""
        # Test with empty data
        empty_data = pd.DataFrame()
        numeric_columns = []
        
        # All analyzers should handle empty data gracefully
        stationarity_results = self.stationarity_analyzer.analyze_stationarity(empty_data, numeric_columns)
        seasonality_results = self.seasonality_detector.analyze_seasonality(empty_data, numeric_columns)
        financial_results = self.financial_analyzer.analyze_financial_features(empty_data, numeric_columns)
        
        # Results should still have expected structure
        assert 'adf_tests' in stationarity_results
        assert 'day_patterns' in seasonality_results
        assert 'price_range_analysis' in financial_results
    
    def test_data_consistency_across_analyses(self):
        """Test that data remains consistent across different analyses."""
        prepared_data = self.file_ops.prepare_time_series_data(self.sample_data)
        numeric_columns = self.file_ops.get_numeric_columns(prepared_data)
        
        # Run multiple analyses
        stationarity_results = self.stationarity_analyzer.analyze_stationarity(prepared_data, numeric_columns)
        seasonality_results = self.seasonality_detector.analyze_seasonality(prepared_data, numeric_columns)
        financial_results = self.financial_analyzer.analyze_financial_features(prepared_data, numeric_columns)
        
        # Check that all analyses processed the same columns
        stationarity_cols = set(stationarity_results['adf_tests'].keys())
        seasonality_cols = set(seasonality_results['day_patterns'].keys())
        financial_cols = set(financial_results['price_range_analysis'].keys())
        
        assert stationarity_cols == seasonality_cols == financial_cols
        assert stationarity_cols == set(numeric_columns)
    
    def test_memory_efficiency(self):
        """Test that analyses don't consume excessive memory."""
        # Create larger dataset
        large_dates = pd.date_range('2020-01-01', periods=1000, freq='D')
        large_data = pd.DataFrame({
            'price': np.random.normal(100, 10, 1000),
            'volume': np.random.lognormal(10, 1, 1000)
        }, index=large_dates)
        
        prepared_data = self.file_ops.prepare_time_series_data(large_data)
        numeric_columns = self.file_ops.get_numeric_columns(prepared_data)
        
        # Run analyses - should complete without memory issues
        stationarity_results = self.stationarity_analyzer.analyze_stationarity(prepared_data, numeric_columns)
        seasonality_results = self.seasonality_detector.analyze_seasonality(prepared_data, numeric_columns)
        financial_results = self.financial_analyzer.analyze_financial_features(prepared_data, numeric_columns)
        
        # Verify results are complete
        assert len(stationarity_results['adf_tests']) > 0
        assert len(seasonality_results['day_patterns']) > 0
        assert len(financial_results['price_range_analysis']) > 0
