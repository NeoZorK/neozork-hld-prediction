# -*- coding: utf-8 -*-
"""
Tests for data loading functionality.

This module provides tests for the universal data loader.
"""

import pytest
import pandas as pd
import numpy as np
from pathlib import Path
import tempfile
import json
import os

from ..data import UniversalDataLoader, GluonPreprocessor


class TestDataLoading:
    """Test data loading functionality."""
    
    @pytest.fixture
    def sample_data(self):
        """Create sample data for testing."""
        np.random.seed(42)
        n_samples = 100
        
        data = pd.DataFrame({
            'feature_1': np.random.randn(n_samples),
            'feature_2': np.random.randn(n_samples),
            'feature_3': np.random.randn(n_samples),
            'target': np.random.randn(n_samples)
        })
        
        # Add datetime index
        data.index = pd.date_range('2023-01-01', periods=n_samples, freq='D')
        
        return data
    
    @pytest.fixture
    def temp_data_dir(self, sample_data):
        """Create temporary data directory with sample files."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create parquet file
            parquet_path = Path(temp_dir) / "test_data.parquet"
            sample_data.to_parquet(parquet_path)
            
            # Create CSV file
            csv_path = Path(temp_dir) / "test_data.csv"
            sample_data.to_csv(csv_path)
            
            # Create JSON file
            json_path = Path(temp_dir) / "test_data.json"
            sample_data.to_json(json_path, orient='records')
            
            # Create Excel file
            excel_path = Path(temp_dir) / "test_data.xlsx"
            sample_data.to_excel(excel_path)
            
            yield temp_dir
    
    def test_universal_loader_initialization(self):
        """Test UniversalDataLoader initialization."""
        loader = UniversalDataLoader("test_path", recursive=True)
        
        assert loader.data_path == Path("test_path")
        assert loader.recursive is True
        assert len(loader.supported_formats) > 0
    
    def test_file_discovery(self, temp_data_dir):
        """Test file discovery functionality."""
        loader = UniversalDataLoader(temp_data_dir, recursive=True)
        files = loader.discover_data_files()
        
        assert len(files) >= 4  # At least parquet, CSV, JSON, Excel
        assert any('test_data.parquet' in str(f) for f in files)
        assert any('test_data.csv' in str(f) for f in files)
        assert any('test_data.json' in str(f) for f in files)
        assert any('test_data.xlsx' in str(f) for f in files)
    
    def test_parquet_loading(self, temp_data_dir, sample_data):
        """Test parquet file loading."""
        loader = UniversalDataLoader(temp_data_dir)
        parquet_path = Path(temp_data_dir) / "test_data.parquet"
        
        loaded_data = loader.load_parquet(parquet_path)
        
        assert not loaded_data.empty
        assert len(loaded_data) == len(sample_data)
        assert list(loaded_data.columns) == list(sample_data.columns)
    
    def test_csv_loading(self, temp_data_dir, sample_data):
        """Test CSV file loading."""
        loader = UniversalDataLoader(temp_data_dir)
        csv_path = Path(temp_data_dir) / "test_data.csv"
        
        loaded_data = loader.load_csv(csv_path)
        
        assert not loaded_data.empty
        assert len(loaded_data) == len(sample_data)
        assert list(loaded_data.columns) == list(sample_data.columns)
    
    def test_json_loading(self, temp_data_dir, sample_data):
        """Test JSON file loading."""
        loader = UniversalDataLoader(temp_data_dir)
        json_path = Path(temp_data_dir) / "test_data.json"
        
        loaded_data = loader.load_json(json_path)
        
        assert not loaded_data.empty
        assert len(loaded_data) == len(sample_data)
        assert list(loaded_data.columns) == list(sample_data.columns)
    
    def test_excel_loading(self, temp_data_dir, sample_data):
        """Test Excel file loading."""
        loader = UniversalDataLoader(temp_data_dir)
        excel_path = Path(temp_data_dir) / "test_data.xlsx"
        
        loaded_data = loader.load_excel(excel_path)
        
        assert not loaded_data.empty
        assert len(loaded_data) == len(sample_data)
        assert list(loaded_data.columns) == list(sample_data.columns)
    
    def test_auto_format_detection(self, temp_data_dir, sample_data):
        """Test automatic format detection."""
        loader = UniversalDataLoader(temp_data_dir)
        
        # Test parquet
        parquet_path = Path(temp_data_dir) / "test_data.parquet"
        loaded_data = loader.load_file(parquet_path)
        assert not loaded_data.empty
        
        # Test CSV
        csv_path = Path(temp_data_dir) / "test_data.csv"
        loaded_data = loader.load_file(csv_path)
        assert not loaded_data.empty
        
        # Test JSON
        json_path = Path(temp_data_dir) / "test_data.json"
        loaded_data = loader.load_file(json_path)
        assert not loaded_data.empty
    
    def test_multiple_file_loading(self, temp_data_dir):
        """Test loading multiple files."""
        loader = UniversalDataLoader(temp_data_dir)
        
        # Get all files
        files = loader.discover_data_files()
        
        # Load multiple files
        loaded_data = loader.load_multiple_files(files[:2])  # Load first 2 files
        
        assert not loaded_data.empty
        assert len(loaded_data) > 0
    
    def test_file_info(self, temp_data_dir):
        """Test file information retrieval."""
        loader = UniversalDataLoader(temp_data_dir)
        parquet_path = Path(temp_data_dir) / "test_data.parquet"
        
        file_info = loader.get_file_info(parquet_path)
        
        assert 'file_path' in file_info
        assert 'file_size' in file_info
        assert 'extension' in file_info
        assert 'rows' in file_info
        assert 'columns' in file_info
    
    def test_data_validation(self, sample_data):
        """Test data validation."""
        loader = UniversalDataLoader()
        
        # Test valid data
        validation_results = loader.validate_dataframe(sample_data)
        assert validation_results['is_valid'] is True
        
        # Test empty data
        empty_data = pd.DataFrame()
        validation_results = loader.validate_dataframe(empty_data)
        assert validation_results['is_valid'] is False
    
    def test_preprocessor_initialization(self):
        """Test GluonPreprocessor initialization."""
        preprocessor = GluonPreprocessor()
        
        assert preprocessor.config is not None
        assert preprocessor.preprocessing_steps == []
    
    def test_data_preparation(self, sample_data):
        """Test data preparation for AutoGluon."""
        preprocessor = GluonPreprocessor()
        
        prepared_data = preprocessor.prepare_for_gluon(sample_data, 'target')
        
        assert not prepared_data.empty
        assert len(prepared_data) == len(sample_data)
        assert list(prepared_data.columns) == list(sample_data.columns)
    
    def test_time_series_split(self, sample_data):
        """Test time series splitting."""
        preprocessor = GluonPreprocessor()
        
        train, val, test = preprocessor.create_time_series_split(sample_data)
        
        # Check split ratios
        total_len = len(sample_data)
        assert len(train) == int(total_len * 0.6)
        assert len(val) == int(total_len * 0.2)
        assert len(test) == int(total_len * 0.2)
        
        # Check chronological order
        assert train.index.max() <= val.index.min()
        assert val.index.max() <= test.index.min()
    
    def test_sequential_split(self, sample_data):
        """Test sequential splitting for non-datetime data."""
        preprocessor = GluonPreprocessor()
        
        # Remove datetime index
        sample_data_no_dt = sample_data.copy()
        sample_data_no_dt.index = range(len(sample_data_no_dt))
        
        train, val, test = preprocessor.create_time_series_split(sample_data_no_dt)
        
        # Check split ratios
        total_len = len(sample_data_no_dt)
        assert len(train) == int(total_len * 0.6)
        assert len(val) == int(total_len * 0.2)
        assert len(test) == int(total_len * 0.2)
    
    def test_data_summary(self, sample_data):
        """Test data summary generation."""
        preprocessor = GluonPreprocessor()
        
        summary = preprocessor.get_data_summary(sample_data)
        
        assert 'shape' in summary
        assert 'columns' in summary
        assert 'dtypes' in summary
        assert 'missing_values' in summary
        assert 'memory_usage' in summary
        assert 'numeric_columns' in summary
        assert 'categorical_columns' in summary
    
    def test_quality_issue_detection(self, sample_data):
        """Test data quality issue detection."""
        preprocessor = GluonPreprocessor()
        
        # Test with good data
        issues = preprocessor.detect_data_quality_issues(sample_data)
        assert len(issues) == 0
        
        # Test with problematic data
        bad_data = sample_data.copy()
        bad_data['empty_col'] = np.nan  # Empty column
        bad_data['constant_col'] = 1  # Constant column
        
        issues = preprocessor.detect_data_quality_issues(bad_data)
        assert len(issues) > 0
        assert any('Empty columns' in issue for issue in issues)
        assert any('Constant columns' in issue for issue in issues)
    
    def test_error_handling(self):
        """Test error handling in data loading."""
        loader = UniversalDataLoader()
        
        # Test with non-existent file
        non_existent_path = Path("/nonexistent/file.parquet")
        loaded_data = loader.load_file(non_existent_path)
        assert loaded_data.empty
        
        # Test with unsupported format
        unsupported_path = Path("test.txt")
        loaded_data = loader.load_file(unsupported_path)
        assert loaded_data.empty
    
    def test_memory_optimization(self, sample_data):
        """Test memory optimization features."""
        loader = UniversalDataLoader()
        
        # Test with large dataset
        large_data = pd.concat([sample_data] * 10)  # 10x larger
        
        # Should handle large datasets gracefully
        validation_results = loader.validate_dataframe(large_data)
        assert validation_results['is_valid'] is True
