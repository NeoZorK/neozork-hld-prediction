# -*- coding: utf-8 -*-
"""
Tests for IndicatorsMTFCreator class.
"""

import pytest
import pandas as pd
import numpy as np
from pathlib import Path
import tempfile
import shutil
import json
from unittest.mock import patch, MagicMock

from src.interactive.data_management.indicators.indicators_mtf_creator import IndicatorsMTFCreator


class TestIndicatorsMTFCreator:
    """Test cases for IndicatorsMTFCreator."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.mtf_creator = IndicatorsMTFCreator()
        self.temp_dir = tempfile.mkdtemp()
    
    def teardown_method(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.temp_dir)
    
    def test_create_mtf_from_processed_data_success(self):
        """Test successful MTF creation from processed data."""
        # Create sample processed data
        processed_data = {
            "file1.parquet": {
                "data": pd.DataFrame({
                    "timestamp": pd.date_range('2023-01-01', periods=10, freq='1h'),
                    "value": np.random.randn(10),
                    "symbol": ['BTCUSDT'] * 10,
                    "timeframe": ['H1'] * 10
                }),
                "indicator": "RSI",
                "timeframe": "H1",
                "format": "parquet",
                "file_path": "/test/rsi.parquet"
            },
            "file2.parquet": {
                "data": pd.DataFrame({
                    "timestamp": pd.date_range('2023-01-01', periods=10, freq='1h'),
                    "value": np.random.randn(10),
                    "symbol": ['BTCUSDT'] * 10,
                    "timeframe": ['H1'] * 10
                }),
                "indicator": "MACD",
                "timeframe": "H1",
                "format": "parquet",
                "file_path": "/test/macd.parquet"
            }
        }
        
        result = self.mtf_creator.create_mtf_from_processed_data(
            processed_data, "BTCUSDT", "H1", "indicators"
        )
        
        assert result["status"] == "success"
        assert "mtf_data" in result
        assert "creation_time" in result
        assert "metadata" in result
        
        mtf_data = result["mtf_data"]
        assert mtf_data["symbol"] == "BTCUSDT"
        assert mtf_data["main_timeframe"] == "H1"
        assert mtf_data["source"] == "indicators"
        assert "RSI" in mtf_data["indicators"]
        assert "MACD" in mtf_data["indicators"]
        assert "H1" in mtf_data["timeframes"]
        assert not mtf_data["main_data"].empty
    
    def test_create_mtf_from_single_indicator_success(self):
        """Test successful MTF creation from single indicator."""
        indicator_data = {
            "data": pd.DataFrame({
                "timestamp": pd.date_range('2023-01-01', periods=10, freq='1h'),
                "value": np.random.randn(10),
                "symbol": ['BTCUSDT'] * 10,
                "timeframe": ['H1'] * 10
            }),
            "indicator": "RSI",
            "timeframe": "H1",
            "format": "parquet",
            "file_path": "/test/rsi.parquet"
        }
        
        result = self.mtf_creator.create_mtf_from_single_indicator(
            indicator_data, "BTCUSDT", "H1"
        )
        
        assert result["status"] == "success"
        assert "mtf_data" in result
        
        mtf_data = result["mtf_data"]
        assert mtf_data["symbol"] == "BTCUSDT"
        assert mtf_data["main_timeframe"] == "H1"
        assert "RSI" in mtf_data["indicators"]
    
    def test_organize_data_by_indicator_and_timeframe(self):
        """Test organizing data by indicator and timeframe."""
        processed_data = {
            "file1.parquet": {
                "data": pd.DataFrame({"value": [1, 2, 3]}),
                "indicator": "RSI",
                "timeframe": "H1"
            },
            "file2.json": {
                "data": pd.DataFrame({"value": [4, 5]}),
                "indicator": "MACD",
                "timeframe": "H1"
            }
        }
        
        organized = self.mtf_creator._organize_data_by_indicator_and_timeframe(processed_data)
        
        assert "RSI" in organized
        assert "MACD" in organized
        assert "H1" in organized["RSI"]  # timeframe is extracted from data
        assert "H1" in organized["MACD"]
    
    def test_create_main_mtf_structure(self):
        """Test creating main MTF structure."""
        organized_data = {
            "RSI": {
                "H1": {
                    "data": pd.DataFrame({
                        "timestamp": pd.date_range('2023-01-01', periods=5, freq='1h'),
                        "value": [1, 2, 3, 4, 5],
                        "symbol": ['BTCUSDT'] * 5,
                        "timeframe": ['H1'] * 5
                    }),
                    "indicator": "RSI"
                }
            }
        }
        
        mtf_data = self.mtf_creator._create_main_mtf_structure(
            organized_data, "BTCUSDT", "H1", "indicators"
        )
        
        assert mtf_data["symbol"] == "BTCUSDT"
        assert mtf_data["main_timeframe"] == "H1"
        assert mtf_data["source"] == "indicators"
        assert "RSI" in mtf_data["indicators"]
        assert "H1" in mtf_data["timeframes"]
        assert not mtf_data["main_data"].empty
        assert "metadata" in mtf_data
    
    def test_create_cross_timeframe_features(self):
        """Test creating cross-timeframe features."""
        organized_data = {
            "RSI": {
                "H1": {
                    "data": pd.DataFrame({
                        "timestamp": pd.date_range('2023-01-01', periods=5, freq='1h'),
                        "value": [1, 2, 3, 4, 5],
                        "symbol": ['BTCUSDT'] * 5,
                        "timeframe": ['H1'] * 5
                    }),
                    "indicator": "RSI"
                },
                "D1": {
                    "data": pd.DataFrame({
                        "timestamp": pd.date_range('2023-01-01', periods=3, freq='1D'),
                        "value": [10, 20, 30],
                        "symbol": ['BTCUSDT'] * 3,
                        "timeframe": ['D1'] * 3
                    }),
                    "indicator": "RSI"
                }
            }
        }
        
        cross_features = self.mtf_creator._create_cross_timeframe_features(
            organized_data, "H1"
        )
        
        assert "D1" in cross_features
        assert "RSI" in cross_features["D1"]
        assert not cross_features["D1"]["RSI"].empty
    
    def test_add_mtf_metadata(self):
        """Test adding MTF metadata."""
        mtf_data = {
            "symbol": "BTCUSDT",
            "main_timeframe": "H1",
            "indicators": ["RSI"],
            "timeframes": ["H1"],
            "main_data": pd.DataFrame({"value": [1, 2, 3]}),
            "metadata": {
                "total_rows": 3,
                "total_indicators": 1,
                "total_timeframes": 1
            }
        }
        
        processed_data = {"file1.parquet": {"data": pd.DataFrame()}}
        start_time = 1000.0
        
        with patch('time.time', return_value=1002.0):
            result = self.mtf_creator._add_mtf_metadata(mtf_data, processed_data, start_time)
        
        assert "creation_time" in result["metadata"]
        assert "data_quality" in result["metadata"]
        assert "indicators_list" in result["metadata"]
        assert "timeframes_list" in result["metadata"]
        assert "main_data_shape" in result["metadata"]
        assert result["metadata"]["creation_time"] == 2.0
    
    def test_calculate_data_quality_metrics(self):
        """Test calculating data quality metrics."""
        mtf_data = {
            "main_data": pd.DataFrame({
                "RSI": [1, 2, 3, 4, 5],
                "MACD": [0.1, 0.2, 0.3, 0.4, 0.5],
                "other": ["a", "b", "c", "d", "e"]
            })
        }
        
        metrics = self.mtf_creator._calculate_data_quality_metrics(mtf_data)
        
        assert "completeness" in metrics
        assert "consistency" in metrics
        assert "validity" in metrics
        assert "overall_score" in metrics
        assert 0 <= metrics["completeness"] <= 100
        assert 0 <= metrics["consistency"] <= 100
        assert 0 <= metrics["validity"] <= 100
        assert 0 <= metrics["overall_score"] <= 100
    
    def test_validate_mtf_structure_success(self):
        """Test successful MTF structure validation."""
        mtf_data = {
            "symbol": "BTCUSDT",
            "main_timeframe": "H1",
            "indicators": ["RSI"],
            "timeframes": ["H1"],
            "main_data": pd.DataFrame({"value": [1, 2, 3]}),
            "metadata": {
                "created_at": "2023-01-01T00:00:00Z",
                "total_indicators": 1,
                "total_timeframes": 1
            }
        }
        
        result = self.mtf_creator._validate_mtf_structure(mtf_data)
        
        assert result["valid"] is True
        assert result["errors"] == []
    
    def test_validate_mtf_structure_missing_fields(self):
        """Test MTF structure validation with missing fields."""
        mtf_data = {
            "symbol": "BTCUSDT",
            # Missing required fields
        }
        
        result = self.mtf_creator._validate_mtf_structure(mtf_data)
        
        assert result["valid"] is False
        assert len(result["errors"]) > 0
        assert any("Missing required field" in error for error in result["errors"])
    
    def test_validate_mtf_structure_empty_data(self):
        """Test MTF structure validation with empty main data."""
        mtf_data = {
            "symbol": "BTCUSDT",
            "main_timeframe": "H1",
            "indicators": ["RSI"],
            "timeframes": ["H1"],
            "main_data": pd.DataFrame(),  # Empty
            "metadata": {
                "created_at": "2023-01-01T00:00:00Z",
                "total_indicators": 1,
                "total_timeframes": 1
            }
        }
        
        result = self.mtf_creator._validate_mtf_structure(mtf_data)
        
        assert result["valid"] is False
        assert any("empty" in error.lower() for error in result["errors"])
    
    def test_save_mtf_structure_success(self):
        """Test successful MTF structure saving."""
        mtf_data = {
            "symbol": "BTCUSDT",
            "main_timeframe": "H1",
            "indicators": ["RSI"],
            "timeframes": ["H1"],
            "main_data": pd.DataFrame({
                "RSI": [1, 2, 3],
                "timestamp": pd.date_range('2023-01-01', periods=3, freq='1h')
            }),
            "cross_timeframe_features": {
                "D1": {
                    "RSI": pd.DataFrame({
                        "value": [10, 20, 30],
                        "timestamp": pd.date_range('2023-01-01', periods=3, freq='1D')
                    })
                }
            },
            "metadata": {
                "created_at": "2023-01-01T00:00:00Z",
                "total_indicators": 1,
                "total_timeframes": 1
            }
        }
        
        output_path = Path(self.temp_dir) / "test_mtf"
        result = self.mtf_creator.save_mtf_structure(mtf_data, output_path)
        
        assert result["status"] == "success"
        assert "output_path" in result
        assert "files_created" in result
        assert output_path.exists()
        assert (output_path / "mtf_metadata.json").exists()
    
    def test_save_mtf_structure_error_handling(self):
        """Test error handling in save_mtf_structure."""
        mtf_data = {
            "symbol": "BTCUSDT",
            "main_timeframe": "H1",
            "indicators": ["RSI"],
            "timeframes": ["H1"],
            "main_data": pd.DataFrame({"value": [1, 2, 3]}),
            "metadata": {}
        }
        
        # Use invalid path to trigger error
        invalid_path = Path("/invalid/path/that/does/not/exist")
        
        # Mock the mkdir method to raise an exception
        with patch.object(Path, 'mkdir', side_effect=OSError("Permission denied")):
            result = self.mtf_creator.save_mtf_structure(mtf_data, invalid_path)
        
        assert result["status"] == "error"
        assert "message" in result
    
    def test_create_mtf_from_processed_data_no_data(self):
        """Test MTF creation with no valid data."""
        processed_data = {}
        
        result = self.mtf_creator.create_mtf_from_processed_data(
            processed_data, "BTCUSDT", "H1", "indicators"
        )
        
        assert result["status"] == "error"
        assert "No valid data found" in result["message"]
    
    def test_create_mtf_from_processed_data_validation_failure(self):
        """Test MTF creation with validation failure."""
        # Create invalid MTF data that will fail validation
        processed_data = {
            "RSI": {
                "H1": {
                    "data": pd.DataFrame(),  # Empty dataframe
                    "indicator": "RSI"
                }
            }
        }
        
        with patch.object(self.mtf_creator, '_validate_mtf_structure', 
                         return_value={"valid": False, "errors": ["Test error"]}):
            result = self.mtf_creator.create_mtf_from_processed_data(
                processed_data, "BTCUSDT", "H1", "indicators"
            )
        
        assert result["status"] == "error"
        assert "validation failed" in result["message"]
    
    def test_create_cross_timeframe_features_no_other_timeframes(self):
        """Test cross-timeframe features creation with no other timeframes."""
        organized_data = {
            "RSI": {
                "H1": {
                    "data": pd.DataFrame({"value": [1, 2, 3]}),
                    "indicator": "RSI"
                }
            }
        }
        
        cross_features = self.mtf_creator._create_cross_timeframe_features(
            organized_data, "H1"
        )
        
        assert cross_features == {}
    
    def test_calculate_data_quality_metrics_empty_dataframe(self):
        """Test data quality metrics calculation with empty dataframe."""
        mtf_data = {
            "main_data": pd.DataFrame()
        }
        
        metrics = self.mtf_creator._calculate_data_quality_metrics(mtf_data)
        
        assert metrics["completeness"] == 0
        assert metrics["consistency"] == 0
        assert metrics["validity"] == 0
        assert metrics["overall_score"] == 0
