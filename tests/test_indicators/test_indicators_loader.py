# -*- coding: utf-8 -*-
"""
Tests for IndicatorsLoader class.
"""

import pytest
import pandas as pd
import numpy as np
from pathlib import Path
import tempfile
import shutil
import json
from unittest.mock import patch, MagicMock

from src.interactive.data_management.indicators.indicators_loader import IndicatorsLoader


class TestIndicatorsLoader:
    """Test cases for IndicatorsLoader."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.loader = IndicatorsLoader()
        self.loader.indicators_path = Path(self.temp_dir)
        
        # Create test directory structure
        self._create_test_structure()
    
    def teardown_method(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.temp_dir)
    
    def _create_test_structure(self):
        """Create test directory structure with sample files."""
        # Create subdirectories
        parquet_dir = Path(self.temp_dir) / "parquet"
        json_dir = Path(self.temp_dir) / "json"
        csv_dir = Path(self.temp_dir) / "csv"
        
        parquet_dir.mkdir(parents=True)
        json_dir.mkdir(parents=True)
        csv_dir.mkdir(parents=True)
        
        # Create sample parquet file
        parquet_data = pd.DataFrame({
            'timestamp': pd.date_range('2023-01-01', periods=100, freq='1h'),
            'value': np.random.randn(100),
            'symbol': ['BTCUSDT'] * 100,
            'timeframe': ['H1'] * 100
        })
        parquet_data.to_parquet(parquet_dir / "rsi_btcusdt_h1.parquet")
        
        # Create sample JSON file
        json_data = [
            {
                'timestamp': '2023-01-01T00:00:00Z',
                'value': 0.5,
                'symbol': 'ETHUSDT',
                'timeframe': 'M1'
            },
            {
                'timestamp': '2023-01-01T01:00:00Z',
                'value': 0.6,
                'symbol': 'ETHUSDT',
                'timeframe': 'M1'
            }
        ]
        with open(json_dir / "macd_ethusdt_m1.json", 'w') as f:
            json.dump(json_data, f)
        
        # Create sample CSV file
        csv_data = pd.DataFrame({
            'time': pd.date_range('2023-01-01', periods=50, freq='1D'),
            'price': np.random.randn(50),
            'pair': ['EURUSD'] * 50,
            'period': ['D1'] * 50
        })
        csv_data.to_csv(csv_dir / "sma_eurusd_d1.csv", index=False)
    
    def test_load_indicators_data_success(self):
        """Test successful loading of indicators data."""
        result = self.loader.load_indicators_data()
        
        assert result["status"] == "success"
        assert "data" in result
        assert "metadata" in result
        assert "memory_used" in result
        assert "loading_time" in result
        
        # Check that all files were loaded
        assert len(result["data"]) == 3
        
        # Check metadata
        metadata = result["metadata"]
        assert metadata["total_files"] == 3
        assert metadata["total_rows"] > 0
        assert len(metadata["indicators"]) > 0
        assert len(metadata["formats"]) > 0
    
    def test_load_indicators_data_with_filters(self):
        """Test loading with indicator and format filters."""
        # Test with indicator filter
        result = self.loader.load_indicators_data(indicator_filter="RSI")
        
        assert result["status"] == "success"
        assert len(result["data"]) == 1
        assert "rsi_btcusdt_h1.parquet" in result["data"]
        
        # Test with format filter
        result = self.loader.load_indicators_data(format_filter="parquet")
        
        assert result["status"] == "success"
        assert len(result["data"]) == 1
        assert "rsi_btcusdt_h1.parquet" in result["data"]
    
    def test_load_indicator_by_name_success(self):
        """Test loading specific indicator by name."""
        result = self.loader.load_indicator_by_name("RSI", "parquet")
        
        assert result["status"] == "success"
        assert result["indicator_name"] == "RSI"
        assert result["format"] == "parquet"
        assert "data" in result
        assert result["data"]["indicator"] == "RSI"
    
    def test_load_indicator_by_name_not_found(self):
        """Test loading non-existent indicator."""
        result = self.loader.load_indicator_by_name("NONEXISTENT", "parquet")
        
        assert result["status"] == "error"
        assert "No files found" in result["message"]
    
    def test_load_indicators_by_format_success(self):
        """Test loading all indicators from specific format."""
        result = self.loader.load_indicators_by_format("parquet")
        
        assert result["status"] == "success"
        assert len(result["data"]) == 1
        assert "rsi_btcusdt_h1.parquet" in result["data"]
    
    def test_load_indicators_by_format_not_found(self):
        """Test loading from non-existent format."""
        result = self.loader.load_indicators_by_format("nonexistent")
        
        assert result["status"] == "error"
        assert "No nonexistent files found" in result["message"]
    
    def test_find_files_to_load(self):
        """Test finding files to load with filters."""
        # Test without filters
        files = self.loader._find_files_to_load()
        assert len(files) == 3
        
        # Test with indicator filter
        files = self.loader._find_files_to_load(indicator_filter="RSI")
        assert len(files) == 1
        assert "rsi_btcusdt_h1.parquet" in str(files[0])
        
        # Test with format filter
        files = self.loader._find_files_to_load(format_filter="parquet")
        assert len(files) == 1
        assert "rsi_btcusdt_h1.parquet" in str(files[0])
    
    def test_find_indicator_files(self):
        """Test finding files for specific indicator."""
        files = self.loader._find_indicator_files("RSI")
        assert len(files) == 1
        assert "rsi_btcusdt_h1.parquet" in str(files[0])
        
        files = self.loader._find_indicator_files("NONEXISTENT")
        assert len(files) == 0
    
    def test_find_files_by_format(self):
        """Test finding files by format."""
        files = self.loader._find_files_by_format("parquet")
        assert len(files) == 1
        assert "rsi_btcusdt_h1.parquet" in str(files[0])
        
        files = self.loader._find_files_by_format("nonexistent")
        assert len(files) == 0
    
    def test_load_parquet_file(self):
        """Test loading parquet file."""
        parquet_file = Path(self.temp_dir) / "parquet" / "rsi_btcusdt_h1.parquet"
        result = self.loader._load_parquet_file(parquet_file)
        
        assert result is not None
        assert result["format"] == "parquet"
        assert result["indicator"] == "RSI"
        assert result["rows"] == 100
        assert "value" in result["columns"]
        assert isinstance(result["data"], pd.DataFrame)
    
    def test_load_json_file(self):
        """Test loading JSON file."""
        json_file = Path(self.temp_dir) / "json" / "macd_ethusdt_m1.json"
        result = self.loader._load_json_file(json_file)
        
        assert result is not None
        assert result["format"] == "json"
        assert result["indicator"] == "MACD"
        assert result["rows"] == 2
        assert "value" in result["columns"]
        assert isinstance(result["data"], pd.DataFrame)
        assert "raw_data" in result
    
    def test_load_csv_file(self):
        """Test loading CSV file."""
        csv_file = Path(self.temp_dir) / "csv" / "sma_eurusd_d1.csv"
        result = self.loader._load_csv_file(csv_file)
        
        assert result is not None
        assert result["format"] == "csv"
        assert result["indicator"] == "SMA"
        assert result["rows"] == 50
        assert "price" in result["columns"]
        assert isinstance(result["data"], pd.DataFrame)
    
    def test_load_single_file_unsupported_format(self):
        """Test loading unsupported file format."""
        # Create a file with unsupported extension
        unsupported_file = Path(self.temp_dir) / "test.txt"
        unsupported_file.write_text("test data")
        
        result = self.loader._load_single_file(unsupported_file)
        assert result is None
    
    def test_extract_indicator_name(self):
        """Test extracting indicator name from filename."""
        assert self.loader._extract_indicator_name("rsi_btcusdt.parquet") == "RSI"
        assert self.loader._extract_indicator_name("macd_ethusdt.json") == "MACD"
        assert self.loader._extract_indicator_name("sma_eurusd.csv") == "SMA"
        assert self.loader._extract_indicator_name("unknown_file.parquet") == "UNKNOWN_FILE"
    
    def test_create_metadata(self):
        """Test creating metadata for loaded data."""
        # Create sample loaded data
        loaded_data = {
            "file1.parquet": {
                "data": pd.DataFrame({"value": [1, 2, 3]}),
                "rows": 3,
                "indicator": "RSI",
                "format": "parquet",
                "file_path": str(Path(self.temp_dir) / "file1.parquet")
            },
            "file2.json": {
                "data": pd.DataFrame({"value": [4, 5]}),
                "rows": 2,
                "indicator": "MACD",
                "format": "json",
                "file_path": str(Path(self.temp_dir) / "file2.json")
            }
        }
        
        metadata = self.loader._create_metadata(loaded_data, 10.5, 2.3)
        
        assert metadata["total_files"] == 2
        assert metadata["total_rows"] == 5
        assert "RSI" in metadata["indicators"]
        assert "MACD" in metadata["indicators"]
        assert "parquet" in metadata["formats"]
        assert "json" in metadata["formats"]
        assert metadata["memory_used_mb"] == 10.5
        assert metadata["loading_time_seconds"] == 2.3
    
    def test_format_time(self):
        """Test time formatting."""
        assert self.loader._format_time(30.5) == "30.5s"
        assert self.loader._format_time(90) == "1m 30s"
        assert self.loader._format_time(3661) == "1h 1m"
    
    @patch('src.interactive.data_management.indicators.indicators_loader.print')
    def test_show_loading_progress(self, mock_print):
        """Test loading progress display."""
        self.loader._show_loading_progress("Test message", 0.5, 1000.0)
        
        # Check that print was called
        assert mock_print.called
    
    def test_load_indicators_data_error_handling(self):
        """Test error handling in load_indicators_data."""
        # Test with non-existent directory
        self.loader.indicators_path = Path("/nonexistent/path")
        
        result = self.loader.load_indicators_data()
        
        assert result["status"] == "error"
        assert "message" in result
