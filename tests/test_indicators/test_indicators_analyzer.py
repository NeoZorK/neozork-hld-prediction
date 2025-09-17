# -*- coding: utf-8 -*-
"""
Tests for IndicatorsAnalyzer class.
"""

import pytest
import pandas as pd
import numpy as np
from pathlib import Path
import tempfile
import shutil
import json
from unittest.mock import patch, MagicMock

from src.interactive.data_management.indicators.indicators_analyzer import IndicatorsAnalyzer


class TestIndicatorsAnalyzer:
    """Test cases for IndicatorsAnalyzer."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.analyzer = IndicatorsAnalyzer()
        self.analyzer.indicators_path = Path(self.temp_dir)
        
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
        parquet_data.to_parquet(parquet_dir / "binance_rsi_btcusdt_h1.parquet")
        
        # Create additional parquet files for more indicators
        macd_data = pd.DataFrame({
            'timestamp': pd.date_range('2023-01-01', periods=50, freq='1h'),
            'value': np.random.randn(50),
            'symbol': ['ETHUSDT'] * 50,
            'timeframe': ['H1'] * 50
        })
        macd_data.to_parquet(parquet_dir / "binance_macd_ethusdt_h1.parquet")
        
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
        with open(json_dir / "binance_macd_ethusdt_m1.json", 'w') as f:
            json.dump(json_data, f)
        
        # Create sample CSV file
        csv_data = pd.DataFrame({
            'time': pd.date_range('2023-01-01', periods=50, freq='1D'),
            'price': np.random.randn(50),
            'pair': ['EURUSD'] * 50,
            'period': ['D1'] * 50
        })
        csv_data.to_csv(csv_dir / "csvexport_sma_eurusd_d1.csv", index=False)
    
    def test_analyze_indicators_folder_success(self):
        """Test successful folder analysis."""
        result = self.analyzer.analyze_indicators_folder()
        
        assert result["status"] == "success"
        assert "folder_info" in result
        assert "indicators" in result
        assert "subfolders_info" in result
        assert "files_info" in result
        
        # Check indicators found
        assert len(result["indicators"]) > 0
        # The indicators are extracted from filenames, so they will be the full filename without extension
        assert any("rsi" in indicator.lower() for indicator in result["indicators"])
        assert any("macd" in indicator.lower() for indicator in result["indicators"])
        assert any("sma" in indicator.lower() for indicator in result["indicators"])
        
        # Check subfolders
        assert "parquet" in result["subfolders_info"]
        assert "json" in result["subfolders_info"]
        assert "csv" in result["subfolders_info"]
    
    def test_analyze_indicators_folder_not_found(self):
        """Test analysis when folder doesn't exist."""
        self.analyzer.indicators_path = Path("/nonexistent/path")
        
        result = self.analyzer.analyze_indicators_folder()
        
        assert result["status"] == "error"
        assert "not found" in result["message"]
    
    def test_analyze_folder_structure(self):
        """Test folder structure analysis."""
        folder_info = self.analyzer._analyze_folder_structure(Path(self.temp_dir))
        
        assert "path" in folder_info
        assert "file_count" in folder_info
        assert "size_mb" in folder_info
        assert "modified" in folder_info
        assert folder_info["file_count"] > 0
        assert folder_info["size_mb"] > 0
    
    def test_find_indicators_files(self):
        """Test finding indicators files."""
        files = self.analyzer._find_indicators_files()
        
        assert len(files) == 4  # Two parquet files, one json, one csv
        assert any("binance_rsi_btcusdt_h1.parquet" in str(f) for f in files)
        assert any("binance_macd_ethusdt_h1.parquet" in str(f) for f in files)
        assert any("binance_macd_ethusdt_m1.json" in str(f) for f in files)
        assert any("csvexport_sma_eurusd_d1.csv" in str(f) for f in files)
    
    def test_analyze_single_file_parquet(self):
        """Test analyzing single parquet file."""
        parquet_file = Path(self.temp_dir) / "parquet" / "binance_rsi_btcusdt_h1.parquet"
        file_info = self.analyzer._analyze_single_file(parquet_file)
        
        assert file_info is not None
        assert file_info["format"] == ".parquet"
        assert file_info["indicator"] == "RSI"
        assert file_info["rows"] == 100
        assert "value" in file_info["columns"]
        assert file_info["size_mb"] >= 0
    
    def test_analyze_single_file_json(self):
        """Test analyzing single JSON file."""
        json_file = Path(self.temp_dir) / "json" / "binance_macd_ethusdt_m1.json"
        file_info = self.analyzer._analyze_single_file(json_file)
        
        assert file_info is not None
        assert file_info["format"] == ".json"
        assert file_info["indicator"] == "MACD"
        assert file_info["rows"] == 2
        assert "value" in file_info["columns"]
    
    def test_analyze_single_file_csv(self):
        """Test analyzing single CSV file."""
        csv_file = Path(self.temp_dir) / "csv" / "csvexport_sma_eurusd_d1.csv"
        file_info = self.analyzer._analyze_single_file(csv_file)
        
        assert file_info is not None
        assert file_info["format"] == ".csv"
        assert file_info["indicator"] == "SMA"
        assert file_info["rows"] == 50
        assert "price" in file_info["columns"]
    
    def test_extract_indicator_name(self):
        """Test extracting indicator name from filename."""
        # Test common patterns
        assert self.analyzer._extract_indicator_name("rsi_btcusdt.parquet") == "RSI"
        assert self.analyzer._extract_indicator_name("macd_ethusdt.json") == "MACD"
        assert self.analyzer._extract_indicator_name("sma_eurusd.csv") == "SMA"
        
        # Test fallback
        assert self.analyzer._extract_indicator_name("unknown_file.parquet") == "UNKNOWN_FILE"
    
    def test_get_parquet_data_info(self):
        """Test getting data info from parquet file."""
        parquet_file = Path(self.temp_dir) / "parquet" / "binance_rsi_btcusdt_h1.parquet"
        data_info = self.analyzer._get_parquet_data_info(parquet_file)
        
        assert data_info["rows"] == 100
        assert "timestamp" in data_info["columns"]
        assert "value" in data_info["columns"]
        assert data_info["start_date"] != "No time data"
        assert data_info["end_date"] != "No time data"
        assert "BTCUSDT" in data_info["symbols"]
    
    def test_get_json_data_info(self):
        """Test getting data info from JSON file."""
        json_file = Path(self.temp_dir) / "json" / "binance_macd_ethusdt_m1.json"
        data_info = self.analyzer._get_json_data_info(json_file)
        
        assert data_info["rows"] == 2
        assert "timestamp" in data_info["columns"]
        assert "value" in data_info["columns"]
        assert data_info["start_date"] != "No time data"
        assert data_info["end_date"] != "No time data"
        assert "ETHUSDT" in data_info["symbols"]
    
    def test_get_csv_data_info(self):
        """Test getting data info from CSV file."""
        csv_file = Path(self.temp_dir) / "csv" / "csvexport_sma_eurusd_d1.csv"
        data_info = self.analyzer._get_csv_data_info(csv_file)
        
        assert data_info["rows"] == 50
        assert "time" in data_info["columns"]
        assert "price" in data_info["columns"]
        assert data_info["start_date"] != "No time data"
        assert data_info["end_date"] != "No time data"
        assert "EURUSD" in data_info["symbols"]
    
    def test_analyze_subfolders(self):
        """Test analyzing subfolders."""
        subfolders_info = self.analyzer._analyze_subfolders()
        
        assert "parquet" in subfolders_info
        assert "json" in subfolders_info
        assert "csv" in subfolders_info
        
        # Check each subfolder has files_info
        for subfolder in subfolders_info.values():
            assert "files_info" in subfolder
            assert subfolder["file_count"] > 0
            assert subfolder["size_mb"] >= 0
    
    def test_extract_indicators_metadata(self):
        """Test extracting indicators metadata."""
        files = self.analyzer._find_indicators_files()
        metadata = self.analyzer._extract_indicators_metadata(files)
        
        assert len(metadata) == 4
        assert any("binance_rsi_btcusdt_h1.parquet" in filename for filename in metadata.keys())
        assert any("binance_macd_ethusdt_h1.parquet" in filename for filename in metadata.keys())
        assert any("binance_macd_ethusdt_m1.json" in filename for filename in metadata.keys())
        assert any("csvexport_sma_eurusd_d1.csv" in filename for filename in metadata.keys())
        
        # Check each file has required metadata
        for file_info in metadata.values():
            assert "file_path" in file_info
            assert "size_mb" in file_info
            assert "format" in file_info
            assert "indicator" in file_info
            assert "rows" in file_info
            assert "columns" in file_info
