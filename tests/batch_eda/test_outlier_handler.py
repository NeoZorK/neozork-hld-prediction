#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests for Outlier Handler Module

Comprehensive test suite for outlier detection and treatment functionality.
"""

import pytest
import pandas as pd
import numpy as np
import tempfile
import shutil
from pathlib import Path
from unittest.mock import patch, MagicMock

from src.batch_eda.outlier_handler import OutlierHandler


class TestOutlierHandler:
    """Test cases for OutlierHandler class."""
    
    @pytest.fixture
    def sample_data(self):
        """Create sample data with outliers for testing."""
        np.random.seed(42)
        
        # Create normal data
        normal_data = np.random.normal(100, 10, 1000)
        
        # Add outliers
        outliers_low = np.random.normal(50, 5, 20)  # Low outliers
        outliers_high = np.random.normal(200, 10, 30)  # High outliers
        
        # Combine data
        all_data = np.concatenate([normal_data, outliers_low, outliers_high])
        total_length = len(all_data)
        
        # Create DataFrame with consistent lengths
        df = pd.DataFrame({
            'normal_col': all_data,
            'skewed_col': np.concatenate([
                np.random.normal(10, 2, total_length - 200),
                np.random.normal(50, 5, 200)  # Creates skewness
            ]),
            'categorical_col': ['A', 'B', 'C'] * (total_length // 3) + ['A'] * (total_length % 3),
            'missing_col': np.concatenate([
                np.random.normal(100, 10, total_length - 50),
                [np.nan] * 50
            ])
        })
        
        return df
    
    @pytest.fixture
    def temp_backup_dir(self):
        """Create temporary backup directory."""
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir)
    
    @pytest.fixture
    def outlier_handler(self, sample_data, temp_backup_dir):
        """Create OutlierHandler instance for testing."""
        return OutlierHandler(sample_data, backup_dir=temp_backup_dir)
    
    def test_initialization(self, sample_data, temp_backup_dir):
        """Test OutlierHandler initialization."""
        handler = OutlierHandler(sample_data, backup_dir=temp_backup_dir)
        
        assert handler.original_data.shape == sample_data.shape
        assert handler.current_data.shape == sample_data.shape
        assert handler.backup_dir == Path(temp_backup_dir)
        assert len(handler.treatment_history) == 0
        
        # Check that backup directory was created
        assert Path(temp_backup_dir).exists()
    
    def test_create_backup(self, outlier_handler):
        """Test backup creation functionality."""
        backup_path = outlier_handler.create_backup("_test")
        
        assert Path(backup_path).exists()
        assert backup_path.endswith("_test.parquet")
        
        # Verify backup contains the same data
        backup_data = pd.read_parquet(backup_path)
        pd.testing.assert_frame_equal(outlier_handler.current_data, backup_data)
    
    def test_create_backup_with_error(self, outlier_handler, monkeypatch):
        """Test backup creation with error handling."""
        # Mock to_parquet to raise an exception
        def mock_to_parquet(*args, **kwargs):
            raise Exception("Mock error")
        
        monkeypatch.setattr(outlier_handler.current_data, 'to_parquet', mock_to_parquet)
        
        with pytest.raises(Exception, match="Mock error"):
            outlier_handler.create_backup()
    
    def test_detect_outliers_iqr(self, outlier_handler):
        """Test IQR outlier detection."""
        outlier_mask, stats = outlier_handler.detect_outliers_iqr('normal_col')
        
        assert isinstance(outlier_mask, pd.Series)
        assert len(outlier_mask) == len(outlier_handler.current_data)
        assert isinstance(stats, dict)
        assert 'q1' in stats
        assert 'q3' in stats
        assert 'iqr' in stats
        assert 'lower_bound' in stats
        assert 'upper_bound' in stats
        assert 'outlier_count' in stats
        assert 'outlier_percentage' in stats
        
        # Check that outliers are detected
        assert stats['outlier_count'] > 0
        assert stats['outlier_percentage'] > 0
    
    def test_detect_outliers_iqr_empty_column(self, outlier_handler):
        """Test IQR detection with empty column."""
        # Create empty column
        outlier_handler.current_data['empty_col'] = np.nan
        
        outlier_mask, stats = outlier_handler.detect_outliers_iqr('empty_col')
        
        assert isinstance(outlier_mask, pd.Series)
        assert outlier_mask.sum() == 0
        assert len(stats) == 0
    
    def test_detect_outliers_iqr_custom_multiplier(self, outlier_handler):
        """Test IQR detection with custom multiplier."""
        outlier_mask_15, stats_15 = outlier_handler.detect_outliers_iqr('normal_col', multiplier=1.5)
        outlier_mask_20, stats_20 = outlier_handler.detect_outliers_iqr('normal_col', multiplier=2.0)
        
        # More restrictive multiplier should detect fewer outliers
        assert stats_15['outlier_count'] >= stats_20['outlier_count']
    
    def test_detect_outliers_zscore(self, outlier_handler):
        """Test Z-score outlier detection."""
        outlier_mask, stats = outlier_handler.detect_outliers_zscore('normal_col')
        
        assert isinstance(outlier_mask, pd.Series)
        assert len(outlier_mask) == len(outlier_handler.current_data)
        assert isinstance(stats, dict)
        assert 'mean' in stats
        assert 'std' in stats
        assert 'threshold' in stats
        assert 'outlier_count' in stats
        assert 'outlier_percentage' in stats
        
        # Check that outliers are detected
        assert stats['outlier_count'] > 0
        assert stats['outlier_percentage'] > 0
    
    def test_detect_outliers_zscore_custom_threshold(self, outlier_handler):
        """Test Z-score detection with custom threshold."""
        outlier_mask_3, stats_3 = outlier_handler.detect_outliers_zscore('normal_col', threshold=3.0)
        outlier_mask_2, stats_2 = outlier_handler.detect_outliers_zscore('normal_col', threshold=2.0)
        
        # Lower threshold should detect more outliers
        assert stats_2['outlier_count'] >= stats_3['outlier_count']
    
    def test_detect_outliers_isolation_forest(self, outlier_handler):
        """Test Isolation Forest outlier detection."""
        outlier_mask, stats = outlier_handler.detect_outliers_isolation_forest(['normal_col'])
        
        assert isinstance(outlier_mask, pd.Series)
        assert len(outlier_mask) == len(outlier_handler.current_data)
        assert isinstance(stats, dict)
        assert 'contamination' in stats
        assert 'outlier_count' in stats
        assert 'outlier_percentage' in stats
        assert 'columns_analyzed' in stats
    
    def test_detect_outliers_isolation_forest_no_sklearn(self, outlier_handler, monkeypatch):
        """Test Isolation Forest when scikit-learn is not available."""
        # Mock ImportError
        def mock_import(*args, **kwargs):
            raise ImportError("No module named 'sklearn'")
        
        with patch('builtins.__import__', side_effect=mock_import):
            outlier_mask, stats = outlier_handler.detect_outliers_isolation_forest(['normal_col'])
            
            assert isinstance(outlier_mask, pd.Series)
            assert outlier_mask.sum() == 0
            assert len(stats) == 0
    
    def test_treat_outliers_removal(self, outlier_handler):
        """Test outlier removal treatment."""
        original_shape = outlier_handler.current_data.shape
        
        results = outlier_handler.treat_outliers_removal(['normal_col'], method='iqr')
        
        assert isinstance(results, dict)
        assert results['method'] == 'removal'
        assert results['detection_method'] == 'iqr'
        assert 'normal_col' in results['columns_treated']
        assert 'backup_path' in results
        assert results['rows_removed'] > 0
        
        # Check that data shape changed
        assert outlier_handler.current_data.shape[0] < original_shape[0]
        
        # Check treatment history
        assert len(outlier_handler.treatment_history) == 1
        assert outlier_handler.treatment_history[0] == results
    
    def test_treat_outliers_removal_invalid_method(self, outlier_handler):
        """Test outlier removal with invalid method."""
        results = outlier_handler.treat_outliers_removal(['normal_col'], method='invalid_method')
        
        assert results['rows_removed'] == 0
        assert len(outlier_handler.treatment_history) == 1
    
    def test_treat_outliers_removal_nonexistent_column(self, outlier_handler):
        """Test outlier removal with nonexistent column."""
        results = outlier_handler.treat_outliers_removal(['nonexistent_col'], method='iqr')
        
        assert results['rows_removed'] == 0
        assert len(outlier_handler.treatment_history) == 1
    
    def test_treat_outliers_capping(self, outlier_handler):
        """Test outlier capping treatment."""
        original_data = outlier_handler.current_data['normal_col'].copy()
        
        results = outlier_handler.treat_outliers_capping(['normal_col'], method='iqr', cap_method='percentile')
        
        assert isinstance(results, dict)
        assert results['method'] == 'capping'
        assert results['detection_method'] == 'iqr'
        assert results['cap_method'] == 'percentile'
        assert 'normal_col' in results['columns_treated']
        assert 'backup_path' in results
        assert results['values_capped'] > 0
        
        # Check that data shape didn't change
        assert outlier_handler.current_data.shape == outlier_handler.original_data.shape
        
        # Check that some values were capped
        assert not (outlier_handler.current_data['normal_col'] == original_data).all()
        
        # Check treatment history
        assert len(outlier_handler.treatment_history) == 1
    
    def test_treat_outliers_capping_iqr_method(self, outlier_handler):
        """Test outlier capping with IQR method."""
        results = outlier_handler.treat_outliers_capping(['normal_col'], method='iqr', cap_method='iqr')
        
        assert results['cap_method'] == 'iqr'
        assert results['values_capped'] > 0
    
    def test_treat_outliers_capping_manual_method(self, outlier_handler):
        """Test outlier capping with manual bounds."""
        results = outlier_handler.treat_outliers_capping(
            ['normal_col'], 
            method='iqr', 
            cap_method='manual',
            lower_cap=80,
            upper_cap=120
        )
        
        assert results['cap_method'] == 'manual'
        assert results['values_capped'] > 0
    
    def test_treat_outliers_capping_invalid_method(self, outlier_handler):
        """Test outlier capping with invalid method."""
        results = outlier_handler.treat_outliers_capping(['normal_col'], method='iqr', cap_method='invalid')
        
        assert results['values_capped'] == 0
    
    def test_treat_outliers_winsorization(self, outlier_handler):
        """Test winsorization treatment."""
        original_data = outlier_handler.current_data['normal_col'].copy()
        
        results = outlier_handler.treat_outliers_winsorization(['normal_col'], limits=(0.05, 0.05))
        
        assert isinstance(results, dict)
        assert results['method'] == 'winsorization'
        assert results['limits'] == (0.05, 0.05)
        assert 'normal_col' in results['columns_treated']
        assert 'backup_path' in results
        
        # Check that data shape didn't change
        assert outlier_handler.current_data.shape == outlier_handler.original_data.shape
        
        # Check that some values were changed
        assert not (outlier_handler.current_data['normal_col'] == original_data).all()
        
        # Check treatment history
        assert len(outlier_handler.treatment_history) == 1
    
    def test_validate_treatment(self, outlier_handler):
        """Test treatment validation."""
        validation = outlier_handler.validate_treatment()
        
        assert isinstance(validation, dict)
        assert 'data_integrity' in validation
        assert 'shape_changed' in validation
        assert 'missing_values' in validation
        assert 'infinite_values' in validation
        assert 'warnings' in validation
        
        # Initial validation should be clean
        assert validation['data_integrity'] is True
        assert validation['shape_changed'] is False
        assert isinstance(validation['warnings'], list)
    
    def test_validate_treatment_after_removal(self, outlier_handler):
        """Test validation after outlier removal."""
        # Remove some outliers
        outlier_handler.treat_outliers_removal(['normal_col'], method='iqr')
        
        validation = outlier_handler.validate_treatment()
        
        assert validation['shape_changed'] is True
        assert "Data shape changed" in validation['warnings'][0]
    
    def test_get_treatment_summary(self, outlier_handler):
        """Test treatment summary generation."""
        summary = outlier_handler.get_treatment_summary()
        
        assert isinstance(summary, dict)
        assert 'total_treatments' in summary
        assert 'original_shape' in summary
        assert 'current_shape' in summary
        assert 'treatments' in summary
        assert 'validation' in summary
        
        assert summary['total_treatments'] == 0
        assert summary['original_shape'] == outlier_handler.original_data.shape
        assert summary['current_shape'] == outlier_handler.current_data.shape
    
    def test_get_treatment_summary_after_treatment(self, outlier_handler):
        """Test treatment summary after applying treatments."""
        # Apply multiple treatments
        outlier_handler.treat_outliers_removal(['normal_col'], method='iqr')
        outlier_handler.treat_outliers_capping(['skewed_col'], method='iqr', cap_method='percentile')
        
        summary = outlier_handler.get_treatment_summary()
        
        assert summary['total_treatments'] == 2
        assert len(summary['treatments']) == 2
        assert summary['treatments'][0]['method'] == 'removal'
        assert summary['treatments'][1]['method'] == 'capping'
    
    def test_restore_from_backup(self, outlier_handler):
        """Test backup restoration."""
        # Create a backup
        backup_path = outlier_handler.create_backup("_test_restore")
        
        # Modify data
        original_shape = outlier_handler.current_data.shape
        outlier_handler.treat_outliers_removal(['normal_col'], method='iqr')
        
        # Verify data changed
        assert outlier_handler.current_data.shape[0] < original_shape[0]
        
        # Restore from backup
        success = outlier_handler.restore_from_backup(backup_path)
        
        assert success is True
        assert outlier_handler.current_data.shape == original_shape
    
    def test_restore_from_backup_nonexistent(self, outlier_handler):
        """Test backup restoration with nonexistent file."""
        success = outlier_handler.restore_from_backup("nonexistent_backup.parquet")
        
        assert success is False
    
    def test_get_outlier_report(self, outlier_handler):
        """Test outlier report generation."""
        report = outlier_handler.get_outlier_report()
        
        assert isinstance(report, dict)
        assert 'timestamp' in report
        assert 'columns_analyzed' in report
        assert 'methods' in report
        assert 'results' in report
        
        assert 'normal_col' in report['results']
        assert 'skewed_col' in report['results']
        assert 'iqr' in report['results']['normal_col']
        assert 'zscore' in report['results']['normal_col']
    
    def test_get_outlier_report_specific_columns(self, outlier_handler):
        """Test outlier report with specific columns."""
        report = outlier_handler.get_outlier_report(['normal_col'])
        
        assert 'normal_col' in report['results']
        assert 'skewed_col' not in report['results']
        assert len(report['columns_analyzed']) == 1
    
    def test_get_outlier_report_nonexistent_column(self, outlier_handler):
        """Test outlier report with nonexistent column."""
        report = outlier_handler.get_outlier_report(['nonexistent_col'])
        
        assert 'nonexistent_col' not in report['results']
    
    def test_multiple_treatments(self, outlier_handler):
        """Test applying multiple treatments."""
        # Apply multiple treatments
        results1 = outlier_handler.treat_outliers_removal(['normal_col'], method='iqr')
        results2 = outlier_handler.treat_outliers_capping(['skewed_col'], method='iqr', cap_method='percentile')
        results3 = outlier_handler.treat_outliers_winsorization(['normal_col'], limits=(0.1, 0.1))
        
        assert len(outlier_handler.treatment_history) == 3
        assert outlier_handler.treatment_history[0] == results1
        assert outlier_handler.treatment_history[1] == results2
        assert outlier_handler.treatment_history[2] == results3
        
        summary = outlier_handler.get_treatment_summary()
        assert summary['total_treatments'] == 3
    
    def test_treatment_with_missing_values(self, outlier_handler):
        """Test treatment with columns containing missing values."""
        results = outlier_handler.treat_outliers_removal(['missing_col'], method='iqr')
        
        assert isinstance(results, dict)
        assert 'missing_col' in results['columns_treated']
    
    def test_treatment_with_categorical_data(self, outlier_handler):
        """Test treatment with categorical data."""
        # Categorical data should be ignored in numeric operations
        results = outlier_handler.treat_outliers_removal(['categorical_col'], method='iqr')
        
        assert results['rows_removed'] == 0
    
    def test_backup_directory_creation(self, sample_data):
        """Test that backup directory is created if it doesn't exist."""
        temp_dir = tempfile.mkdtemp()
        backup_dir = Path(temp_dir) / "new_backup_dir"
        
        handler = OutlierHandler(sample_data, backup_dir=str(backup_dir))
        
        assert backup_dir.exists()
        assert backup_dir.is_dir()
        
        shutil.rmtree(temp_dir)
    
    def test_data_integrity_after_treatments(self, outlier_handler):
        """Test data integrity after various treatments."""
        # Apply different treatments
        outlier_handler.treat_outliers_removal(['normal_col'], method='iqr')
        outlier_handler.treat_outliers_capping(['skewed_col'], method='iqr', cap_method='percentile')
        outlier_handler.treat_outliers_winsorization(['normal_col'], limits=(0.05, 0.05))
        
        validation = outlier_handler.validate_treatment()
        
        # Data should still be valid
        assert validation['data_integrity'] is True
        assert not validation['infinite_values']
        
        # Shape may have changed due to removal
        if validation['shape_changed']:
            assert "Data shape changed" in validation['warnings'][0]
    
    def test_edge_case_empty_dataframe(self):
        """Test with empty DataFrame."""
        empty_df = pd.DataFrame()
        temp_dir = tempfile.mkdtemp()
        
        handler = OutlierHandler(empty_df, backup_dir=temp_dir)
        
        # Should handle empty DataFrame gracefully
        # Add a column first to test
        handler.current_data['test_col'] = []
        outlier_mask, stats = handler.detect_outliers_iqr('test_col')
        assert len(outlier_mask) == 0
        assert len(stats) == 0
        
        shutil.rmtree(temp_dir)
    
    def test_edge_case_single_value_column(self, outlier_handler):
        """Test with column containing single value."""
        # Create column with single value
        outlier_handler.current_data['single_value_col'] = 100
        
        outlier_mask, stats = outlier_handler.detect_outliers_iqr('single_value_col')
        
        # No outliers should be detected
        assert outlier_mask.sum() == 0
        assert stats['outlier_count'] == 0
    
    def test_performance_large_dataset(self):
        """Test performance with larger dataset."""
        # Create larger dataset
        large_data = pd.DataFrame({
            'col1': np.random.normal(100, 10, 10000),
            'col2': np.random.normal(50, 5, 10000),
            'col3': np.random.normal(200, 20, 10000)
        })
        
        temp_dir = tempfile.mkdtemp()
        handler = OutlierHandler(large_data, backup_dir=temp_dir)
        
        # Should handle large dataset without errors
        results = handler.treat_outliers_removal(['col1', 'col2', 'col3'], method='iqr')
        
        assert isinstance(results, dict)
        assert len(handler.treatment_history) == 1
        
        shutil.rmtree(temp_dir)


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
