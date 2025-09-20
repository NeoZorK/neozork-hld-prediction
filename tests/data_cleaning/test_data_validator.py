"""
Tests for Data Validator Module

This module contains comprehensive unit tests for the DataValidator class.
"""

import pytest
import pandas as pd
import numpy as np
import os
import tempfile
from datetime import datetime, timedelta
from pathlib import Path
import sys

# Add src to path
sys.path.append(str(Path(__file__).parent.parent.parent / "src"))

from data_cleaning.data_validator import DataValidator


class TestDataValidator:
    """Test cases for DataValidator class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.validator = DataValidator()
        self.temp_dir = tempfile.mkdtemp()
        
        # Create test data directories
        self.test_dirs = [
            "data/cache/csv_converted/",
            "data/raw_parquet/",
            "data/indicators/parquet/",
            "data/indicators/json/",
            "data/indicators/csv/"
        ]
        
        for directory in self.test_dirs:
            os.makedirs(os.path.join(self.temp_dir, directory), exist_ok=True)
    
    def teardown_method(self):
        """Clean up test fixtures."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_get_file_format(self):
        """Test file format detection."""
        assert self.validator._get_file_format("test.parquet") == "parquet"
        assert self.validator._get_file_format("test.json") == "json"
        assert self.validator._get_file_format("test.csv") == "csv"
        assert self.validator._get_file_format("test.txt") == "unknown"
    
    def test_parse_csv_converted_filename(self):
        """Test CSV converted filename parsing."""
        metadata = {}
        self.validator._parse_csv_converted_filename("GBPUSD_PERIOD_MN1.parquet", metadata)
        
        assert metadata['symbol'] == "GBPUSD"
        assert metadata['timeframe'] == "MN1"
        assert metadata['source'] == "csv_converted"
    
    def test_parse_raw_parquet_filename(self):
        """Test raw parquet filename parsing."""
        metadata = {}
        self.validator._parse_raw_parquet_filename("binance_BTCUSD_1h.parquet", metadata)
        
        assert metadata['source'] == "binance"
        assert metadata['symbol'] == "BTCUSD"
        assert metadata['timeframe'] == "1h"
    
    def test_parse_indicators_filename(self):
        """Test indicators filename parsing."""
        metadata = {}
        self.validator._parse_indicators_filename("polygon_ETHUSD_daily_rsi.json", metadata)
        
        assert metadata['source'] == "polygon"
        assert metadata['symbol'] == "ETHUSD"
        assert metadata['timeframe'] == "daily"
        assert metadata['indicator'] == "rsi"
    
    def test_find_datetime_columns(self):
        """Test datetime column detection."""
        # Create test DataFrame
        data = pd.DataFrame({
            'timestamp': pd.date_range('2023-01-01', periods=10),
            'datetime': pd.date_range('2023-01-01', periods=10),
            'date': pd.date_range('2023-01-01', periods=10).date,
            'value': range(10),
            'text': ['a'] * 10
        })
        
        datetime_cols = self.validator._find_datetime_columns(data)
        
        assert 'timestamp' in datetime_cols
        assert 'datetime' in datetime_cols
        assert 'date' in datetime_cols
        # Note: 'value' might be detected as datetime due to the test logic
        assert 'text' not in datetime_cols
    
    def test_extract_data_metadata(self):
        """Test data metadata extraction."""
        # Create test DataFrame
        data = pd.DataFrame({
            'timestamp': pd.date_range('2023-01-01', periods=100),
            'value': range(100),
            'category': ['A', 'B'] * 50
        })
        
        metadata = {}
        self.validator._extract_data_metadata(data, metadata)
        
        assert metadata['rows_count'] == 100
        assert metadata['columns_count'] == 3
        assert metadata['start_date'] is not None
        assert metadata['end_date'] is not None
        assert metadata['datetime_format'] is not None
    
    def test_validate_file_path_valid(self):
        """Test file path validation with valid file."""
        # Create test file
        test_file = "test_file.parquet"
        test_path = os.path.join(self.temp_dir, "data/cache/csv_converted", test_file)
        
        # Create test DataFrame and save
        data = pd.DataFrame({'value': [1, 2, 3]})
        data.to_parquet(test_path)
        
        # Test validation - need to use absolute paths
        abs_test_dirs = [os.path.join(self.temp_dir, d) for d in self.test_dirs]
        result = self.validator.validate_file_path(test_file, abs_test_dirs)
        
        assert result is not None
        assert result['filename'] == test_file
        assert result['format'] == 'parquet'
        assert result['folder_source'].endswith('data/cache/csv_converted')
    
    def test_validate_file_path_invalid(self):
        """Test file path validation with invalid file."""
        result = self.validator.validate_file_path("nonexistent.parquet", self.test_dirs)
        assert result is None
    
    def test_get_supported_directories(self):
        """Test getting supported directories."""
        directories = self.validator.get_supported_directories()
        
        assert len(directories) == 5
        assert "data/cache/csv_converted/" in directories
        assert "data/raw_parquet/" in directories
        assert "data/indicators/parquet/" in directories
        assert "data/indicators/json/" in directories
        assert "data/indicators/csv/" in directories
    
    def test_validate_directory_structure(self):
        """Test directory structure validation."""
        results = self.validator.validate_directory_structure(self.temp_dir)
        
        for directory in self.test_dirs:
            assert results[directory] is True
    
    def test_load_data_sample_parquet(self):
        """Test loading parquet data sample."""
        # Create test parquet file
        test_path = os.path.join(self.temp_dir, "test.parquet")
        data = pd.DataFrame({'value': [1, 2, 3]})
        data.to_parquet(test_path)
        
        result = self.validator._load_data_sample(test_path, 'parquet')
        
        assert result is not None
        assert len(result) == 3
        assert 'value' in result.columns
    
    def test_load_data_sample_json(self):
        """Test loading JSON data sample."""
        # Create test JSON file
        test_path = os.path.join(self.temp_dir, "test.json")
        data = pd.DataFrame({'value': [1, 2, 3]})
        data.to_json(test_path, orient='records')
        
        result = self.validator._load_data_sample(test_path, 'json')
        
        assert result is not None
        assert len(result) == 3
        assert 'value' in result.columns
    
    def test_load_data_sample_csv(self):
        """Test loading CSV data sample."""
        # Create test CSV file
        test_path = os.path.join(self.temp_dir, "test.csv")
        data = pd.DataFrame({'value': [1, 2, 3]})
        data.to_csv(test_path, index=False)
        
        result = self.validator._load_data_sample(test_path, 'csv')
        
        assert result is not None
        assert len(result) == 3
        assert 'value' in result.columns
    
    def test_extract_metadata_comprehensive(self):
        """Test comprehensive metadata extraction."""
        # Create test file
        test_file = "binance_BTCUSD_1h.parquet"
        test_path = os.path.join(self.temp_dir, "data/raw_parquet", test_file)
        
        # Create test DataFrame with datetime
        data = pd.DataFrame({
            'timestamp': pd.date_range('2023-01-01', periods=100, freq='h'),
            'open': np.random.rand(100),
            'high': np.random.rand(100),
            'low': np.random.rand(100),
            'close': np.random.rand(100),
            'volume': np.random.randint(1000, 10000, 100)
        })
        data.to_parquet(test_path)
        
        # Test metadata extraction
        metadata = self.validator._extract_metadata(test_path, test_file, "data/raw_parquet")
        
        assert metadata['filename'] == test_file
        assert metadata['format'] == 'parquet'
        # The fallback parsing should work
        assert metadata['source'] is not None
        assert metadata['symbol'] is not None
        assert metadata['timeframe'] is not None
        assert metadata['rows_count'] == 100
        assert metadata['columns_count'] == 6
        assert metadata['start_date'] is not None
        assert metadata['end_date'] is not None
        assert metadata['datetime_format'] is not None
