# -*- coding: utf-8 -*-
"""
Tests for IndicatorsProcessor class.
"""

import pytest
import pandas as pd
import numpy as np
from pathlib import Path
import tempfile
import shutil
from unittest.mock import patch, MagicMock

from src.interactive.data_management.indicators.indicators_processor import IndicatorsProcessor


class TestIndicatorsProcessor:
    """Test cases for IndicatorsProcessor."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.processor = IndicatorsProcessor()
    
    def test_process_indicators_data_success(self):
        """Test successful processing of indicators data."""
        # Create sample loaded data
        loaded_data = {
            "file1.parquet": {
                "data": pd.DataFrame({
                    "timestamp": pd.date_range('2023-01-01', periods=10, freq='1H'),
                    "value": np.random.randn(10),
                    "symbol": ['BTCUSDT'] * 10,
                    "timeframe": ['H1'] * 10
                }),
                "indicator": "RSI",
                "format": "parquet",
                "file_path": "/test/file1.parquet"
            },
            "file2.json": {
                "data": pd.DataFrame({
                    "timestamp": pd.date_range('2023-01-01', periods=5, freq='1D'),
                    "value": np.random.randn(5),
                    "symbol": ['ETHUSDT'] * 5,
                    "timeframe": ['D1'] * 5
                }),
                "indicator": "MACD",
                "format": "json",
                "file_path": "/test/file2.json"
            }
        }
        
        result = self.processor.process_indicators_data(loaded_data)
        
        assert result["status"] == "success"
        assert "data" in result
        assert "metadata" in result
        
        # Check processing stats
        stats = result["metadata"]["processing_stats"]
        assert stats["total_files"] == 2
        assert stats["successful_files"] == 2
        assert stats["failed_files"] == 0
        assert stats["total_rows"] > 0
    
    def test_process_single_indicator_success(self):
        """Test successful processing of single indicator."""
        file_data = {
            "data": pd.DataFrame({
                "timestamp": pd.date_range('2023-01-01', periods=10, freq='1H'),
                "value": np.random.randn(10),
                "symbol": ['BTCUSDT'] * 10,
                "timeframe": ['H1'] * 10
            }),
            "indicator": "RSI",
            "format": "parquet",
            "file_path": "/test/file1.parquet"
        }
        
        result = self.processor.process_single_indicator(file_data)
        
        assert result["status"] == "success"
        assert "data" in result
        assert result["data"]["indicator"] == "RSI"
        assert result["data"]["rows"] == 10
        assert "processed_at" in result["data"]["data"].columns
    
    def test_standardize_columns(self):
        """Test column standardization."""
        df = pd.DataFrame({
            "time": pd.date_range('2023-01-01', periods=5, freq='1H'),
            "val": [1, 2, 3, 4, 5],
            "pair": ['BTCUSDT'] * 5,
            "tf": ['H1'] * 5
        })
        
        standardized_df = self.processor._standardize_columns(df)
        
        assert "timestamp" in standardized_df.columns
        assert "value" in standardized_df.columns
        assert "symbol" in standardized_df.columns
        assert "timeframe" in standardized_df.columns
    
    def test_validate_required_columns_success(self):
        """Test successful validation of required columns."""
        df = pd.DataFrame({
            "value": [1, 2, 3, 4, 5],
            "timestamp": pd.date_range('2023-01-01', periods=5, freq='1H')
        })
        
        result = self.processor._validate_required_columns(df)
        
        assert result["valid"] is True
        assert result["missing"] == []
    
    def test_validate_required_columns_missing(self):
        """Test validation with missing required columns."""
        df = pd.DataFrame({
            "timestamp": pd.date_range('2023-01-01', periods=5, freq='1H'),
            "other_column": [1, 2, 3, 4, 5]
        })
        
        result = self.processor._validate_required_columns(df)
        
        assert result["valid"] is False
        assert "value" in result["missing"]
    
    def test_clean_data(self):
        """Test data cleaning."""
        df = pd.DataFrame({
            "timestamp": pd.date_range('2023-01-01', periods=10, freq='1H'),
            "value": [1, 2, np.nan, 4, 5, 6, 7, 8, 9, 10],
            "symbol": ['BTCUSDT'] * 10,
            "timeframe": ['H1'] * 10
        })
        
        cleaned_df = self.processor._clean_data(df)
        
        # Should remove NaN values
        assert cleaned_df["value"].isna().sum() == 0
        # Should be sorted by timestamp
        assert cleaned_df.index.name == "timestamp"
        # Should have no duplicates
        assert not cleaned_df.duplicated().any()
    
    def test_add_metadata_columns(self):
        """Test adding metadata columns."""
        df = pd.DataFrame({
            "value": [1, 2, 3, 4, 5],
            "timestamp": pd.date_range('2023-01-01', periods=5, freq='1H')
        })
        
        file_data = {
            "indicator": "RSI",
            "format": "parquet"
        }
        
        result_df = self.processor._add_metadata_columns(df, file_data)
        
        assert "indicator" in result_df.columns
        assert "symbol" in result_df.columns
        assert "timeframe" in result_df.columns
        assert "processed_at" in result_df.columns
        assert (result_df["indicator"] == "RSI").all()
    
    def test_sort_by_timestamp(self):
        """Test sorting by timestamp."""
        df = pd.DataFrame({
            "value": [3, 1, 2],
            "timestamp": pd.to_datetime(['2023-01-03', '2023-01-01', '2023-01-02'])
        })
        
        sorted_df = self.processor._sort_by_timestamp(df)
        
        assert sorted_df["timestamp"].is_monotonic_increasing
    
    def test_final_validation_success(self):
        """Test successful final validation."""
        df = pd.DataFrame({
            "value": [1, 2, 3, 4, 5],
            "timestamp": pd.date_range('2023-01-01', periods=5, freq='1H')
        })
        
        result = self.processor._final_validation(df)
        
        assert result["valid"] is True
        assert result["errors"] == []
    
    def test_final_validation_empty_dataframe(self):
        """Test final validation with empty dataframe."""
        df = pd.DataFrame()
        
        result = self.processor._final_validation(df)
        
        assert result["valid"] is False
        assert "empty" in result["errors"][0].lower()
    
    def test_final_validation_missing_required_columns(self):
        """Test final validation with missing required columns."""
        df = pd.DataFrame({
            "other_column": [1, 2, 3, 4, 5]
        })
        
        result = self.processor._final_validation(df)
        
        assert result["valid"] is False
        assert any("required" in error.lower() for error in result["errors"])
    
    def test_final_validation_invalid_value_column(self):
        """Test final validation with invalid value column."""
        df = pd.DataFrame({
            "value": ["a", "b", "c", "d", "e"],  # Non-numeric
            "timestamp": pd.date_range('2023-01-01', periods=5, freq='1H')
        })
        
        result = self.processor._final_validation(df)
        
        assert result["valid"] is False
        assert any("non-numeric" in error.lower() for error in result["errors"])
    
    def test_final_validation_no_variation(self):
        """Test final validation with no value variation."""
        df = pd.DataFrame({
            "value": [1, 1, 1, 1, 1],  # All same values
            "timestamp": pd.date_range('2023-01-01', periods=5, freq='1H')
        })
        
        result = self.processor._final_validation(df)
        
        assert result["valid"] is False
        assert any("variation" in error.lower() for error in result["errors"])
    
    def test_get_processing_summary(self):
        """Test getting processing summary."""
        processed_data = {
            "file1": {
                "data": pd.DataFrame({
                    "value": [1, 2, 3],
                    "symbol": ['BTCUSDT'] * 3,
                    "timeframe": ['H1'] * 3,
                    "timestamp": pd.date_range('2023-01-01', periods=3, freq='1H')
                }),
                "indicator": "RSI",
                "format": "parquet"
            },
            "file2": {
                "data": pd.DataFrame({
                    "value": [4, 5],
                    "symbol": ['ETHUSDT'] * 2,
                    "timeframe": ['D1'] * 2,
                    "timestamp": pd.date_range('2023-01-01', periods=2, freq='1D')
                }),
                "indicator": "MACD",
                "format": "json"
            }
        }
        
        summary = self.processor.get_processing_summary(processed_data)
        
        assert summary["total_files"] == 2
        assert summary["total_rows"] == 5
        assert "RSI" in summary["indicators"]
        assert "MACD" in summary["indicators"]
        assert "parquet" in summary["formats"]
        assert "json" in summary["formats"]
        assert "BTCUSDT" in summary["symbols"]
        assert "ETHUSDT" in summary["symbols"]
        assert "H1" in summary["timeframes"]
        assert "D1" in summary["timeframes"]
    
    def test_process_indicators_data_with_errors(self):
        """Test processing with some files failing."""
        # Create data with one file that will fail validation
        loaded_data = {
            "file1.parquet": {
                "data": pd.DataFrame({
                    "timestamp": pd.date_range('2023-01-01', periods=10, freq='1H'),
                    "value": np.random.randn(10),
                    "symbol": ['BTCUSDT'] * 10,
                    "timeframe": ['H1'] * 10
                }),
                "indicator": "RSI",
                "format": "parquet",
                "file_path": "/test/file1.parquet"
            },
            "file2.json": {
                "data": pd.DataFrame(),  # Empty dataframe will fail validation
                "indicator": "MACD",
                "format": "json",
                "file_path": "/test/file2.json"
            }
        }
        
        result = self.processor.process_indicators_data(loaded_data)
        
        assert result["status"] == "success"
        stats = result["metadata"]["processing_stats"]
        assert stats["total_files"] == 2
        assert stats["successful_files"] == 1
        assert stats["failed_files"] == 1
        assert len(stats["validation_errors"]) == 1
    
    def test_process_single_indicator_error_handling(self):
        """Test error handling in process_single_indicator."""
        # Test with invalid file data
        file_data = {
            "data": "invalid_data",  # Not a DataFrame
            "indicator": "RSI",
            "format": "parquet"
        }
        
        result = self.processor.process_single_indicator(file_data)
        
        assert result["status"] == "error"
        assert "message" in result
