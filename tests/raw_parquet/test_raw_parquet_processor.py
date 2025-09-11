# -*- coding: utf-8 -*-
"""
Unit tests for RawParquetProcessor.

This module contains comprehensive unit tests for the RawParquetProcessor class
to ensure proper functionality of raw parquet data processing and standardization.
"""

import pytest
import pandas as pd
import numpy as np
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import tempfile
import os
import sys

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.interactive.data_management.raw_parquet.raw_parquet_processor import RawParquetProcessor

class TestRawParquetProcessor:
    """Test cases for RawParquetProcessor class."""
    
    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.processor = RawParquetProcessor()
        self.temp_dir = tempfile.mkdtemp()
        self.processor.raw_root = Path(self.temp_dir)
    
    def teardown_method(self):
        """Clean up after each test method."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_init(self):
        """Test processor initialization."""
        assert self.processor.project_root is not None
        assert self.processor.data_root is not None
        assert self.processor.raw_root is not None
        assert self.processor.cleaned_root is not None
        assert len(self.processor.exchange_mappings) > 0
        assert 'binance' in self.processor.exchange_mappings
        assert 'bybit' in self.processor.exchange_mappings
    
    def test_process_raw_data(self):
        """Test processing of raw data."""
        # Create test loaded data
        test_data = pd.DataFrame({
            'open_time': pd.date_range('2023-01-01', periods=100, freq='1min'),
            'open': np.random.rand(100),
            'high': np.random.rand(100),
            'low': np.random.rand(100),
            'close': np.random.rand(100),
            'volume': np.random.rand(100)
        })
        
        loaded_data = {
            'binance_BTCUSDT': {
                'file_path': '/test/path.parquet',
                'source': 'binance',
                'symbol': 'BTCUSDT',
                'timeframe': 'M1',
                'data': test_data,
                'size_mb': 1.0,
                'rows': 100,
                'start_time': '2023-01-01',
                'end_time': '2023-01-01',
                'columns': list(test_data.columns)
            }
        }
        
        result = self.processor.process_raw_data(loaded_data)
        
        assert result["status"] == "success"
        assert len(result["data"]) == 1
        assert "binance_BTCUSDT" in result["data"]
        assert result["metadata"]["total_processed"] == 1
    
    def test_process_raw_data_empty(self):
        """Test processing of empty data."""
        result = self.processor.process_raw_data({})
        
        assert result["status"] == "success"
        assert len(result["data"]) == 0
        assert result["metadata"]["total_processed"] == 0
    
    def test_process_single_data(self):
        """Test processing of single data entry."""
        test_data = pd.DataFrame({
            'open_time': pd.date_range('2023-01-01', periods=100, freq='1min'),
            'open': np.random.rand(100),
            'high': np.random.rand(100),
            'low': np.random.rand(100),
            'close': np.random.rand(100),
            'volume': np.random.rand(100)
        })
        
        data_info = {
            'file_path': '/test/path.parquet',
            'source': 'binance',
            'symbol': 'BTCUSDT',
            'timeframe': 'M1',
            'data': test_data,
            'size_mb': 1.0,
            'rows': 100,
            'start_time': '2023-01-01',
            'end_time': '2023-01-01',
            'columns': list(test_data.columns)
        }
        
        result = self.processor._process_single_data(data_info)
        
        assert result is not None
        assert result['source'] == 'binance'
        assert result['symbol'] == 'BTCUSDT'
        assert 'timestamp' in result['data'].columns
        assert 'open' in result['data'].columns
        assert 'high' in result['data'].columns
        assert 'low' in result['data'].columns
        assert 'close' in result['data'].columns
        assert 'volume' in result['data'].columns
        assert result['data'].index.name == 'timestamp'
    
    def test_standardize_columns_binance(self):
        """Test column standardization for Binance data."""
        test_data = pd.DataFrame({
            'open_time': pd.date_range('2023-01-01', periods=10, freq='1min'),
            'open': np.random.rand(10),
            'high': np.random.rand(10),
            'low': np.random.rand(10),
            'close': np.random.rand(10),
            'volume': np.random.rand(10),
            'close_time': pd.date_range('2023-01-01', periods=10, freq='1min'),
            'quote_asset_volume': np.random.rand(10),
            'number_of_trades': np.random.randint(1, 100, 10),
            'taker_buy_base_asset_volume': np.random.rand(10),
            'taker_buy_quote_asset_volume': np.random.rand(10)
        })
        
        result = self.processor._standardize_columns(test_data, 'binance')
        
        assert 'timestamp' in result.columns
        assert 'open' in result.columns
        assert 'high' in result.columns
        assert 'low' in result.columns
        assert 'close' in result.columns
        assert 'volume' in result.columns
        assert 'close_timestamp' in result.columns
        assert 'quote_volume' in result.columns
        assert 'trades_count' in result.columns
        assert 'taker_buy_volume' in result.columns
        assert 'taker_buy_quote_volume' in result.columns
    
    def test_standardize_columns_bybit(self):
        """Test column standardization for Bybit data."""
        test_data = pd.DataFrame({
            'start_time': pd.date_range('2023-01-01', periods=10, freq='1min'),
            'open': np.random.rand(10),
            'high': np.random.rand(10),
            'low': np.random.rand(10),
            'close': np.random.rand(10),
            'volume': np.random.rand(10),
            'turnover': np.random.rand(10)
        })
        
        result = self.processor._standardize_columns(test_data, 'bybit')
        
        assert 'timestamp' in result.columns
        assert 'open' in result.columns
        assert 'high' in result.columns
        assert 'low' in result.columns
        assert 'close' in result.columns
        assert 'volume' in result.columns
        assert 'quote_volume' in result.columns
    
    def test_standardize_columns_unknown_source(self):
        """Test column standardization for unknown source."""
        test_data = pd.DataFrame({
            'custom_time': pd.date_range('2023-01-01', periods=10, freq='1min'),
            'custom_open': np.random.rand(10),
            'custom_high': np.random.rand(10),
            'custom_low': np.random.rand(10),
            'custom_close': np.random.rand(10),
            'custom_volume': np.random.rand(10)
        })
        
        result = self.processor._standardize_columns(test_data, 'unknown')
        
        # Should not change columns for unknown source
        assert 'custom_time' in result.columns
        assert 'custom_open' in result.columns
        assert 'custom_high' in result.columns
        assert 'custom_low' in result.columns
        assert 'custom_close' in result.columns
        assert 'custom_volume' in result.columns
    
    def test_standardize_data_types(self):
        """Test data type standardization."""
        test_data = pd.DataFrame({
            'timestamp': ['2023-01-01 00:00:00', '2023-01-01 00:01:00', '2023-01-01 00:02:00'],
            'open': ['1.0', '2.0', '3.0'],
            'high': ['1.1', '2.1', '3.1'],
            'low': ['0.9', '1.9', '2.9'],
            'close': ['1.05', '2.05', '3.05'],
            'volume': ['100', '200', '300']
        })
        
        result = self.processor._standardize_data_types(test_data)
        
        assert pd.api.types.is_datetime64_any_dtype(result['timestamp'])
        assert pd.api.types.is_numeric_dtype(result['open'])
        assert pd.api.types.is_numeric_dtype(result['high'])
        assert pd.api.types.is_numeric_dtype(result['low'])
        assert pd.api.types.is_numeric_dtype(result['close'])
        assert pd.api.types.is_numeric_dtype(result['volume'])
    
    def test_clean_data(self):
        """Test data cleaning."""
        # Create test data with issues
        test_data = pd.DataFrame({
            'timestamp': pd.date_range('2023-01-01', periods=10, freq='1min'),
            'open': [1.0, 2.0, np.nan, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0],
            'high': [1.1, 2.1, 3.1, 4.1, 5.1, 6.1, 7.1, 8.1, 9.1, 10.1],
            'low': [0.9, 1.9, 2.9, 3.9, 4.9, 5.9, 6.9, 7.9, 8.9, 9.9],
            'close': [1.05, 2.05, 3.05, 4.05, 5.05, 6.05, 7.05, 8.05, 9.05, 10.05],
            'volume': [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]
        })
        
        # Add some invalid OHLC data
        test_data.loc[5, 'high'] = 5.0  # high < close
        test_data.loc[6, 'low'] = 7.0   # low > close
        
        result = self.processor._clean_data(test_data)
        
        # Should remove rows with NaN in critical columns
        assert len(result) < len(test_data)
        assert not result['open'].isna().any()
        
        # Should remove rows with invalid OHLC data
        assert not (result['high'] < result[['open', 'close']].max(axis=1)).any()
        assert not (result['low'] > result[['open', 'close']].min(axis=1)).any()
        assert not (result['high'] < result['low']).any()
    
    def test_detect_timeframe(self):
        """Test timeframe detection."""
        # Test M1 timeframe
        test_data = pd.DataFrame({
            'timestamp': pd.date_range('2023-01-01', periods=10, freq='1min'),
            'open': np.random.rand(10),
            'high': np.random.rand(10),
            'low': np.random.rand(10),
            'close': np.random.rand(10),
            'volume': np.random.rand(10)
        })
        
        timeframe = self.processor._detect_timeframe(test_data)
        assert timeframe == 'M1'
        
        # Test H1 timeframe
        test_data = pd.DataFrame({
            'timestamp': pd.date_range('2023-01-01', periods=10, freq='1H'),
            'open': np.random.rand(10),
            'high': np.random.rand(10),
            'low': np.random.rand(10),
            'close': np.random.rand(10),
            'volume': np.random.rand(10)
        })
        
        timeframe = self.processor._detect_timeframe(test_data)
        assert timeframe == 'H1'
    
    def test_detect_timeframe_no_timestamp(self):
        """Test timeframe detection with no timestamp column."""
        test_data = pd.DataFrame({
            'open': np.random.rand(10),
            'high': np.random.rand(10),
            'low': np.random.rand(10),
            'close': np.random.rand(10),
            'volume': np.random.rand(10)
        })
        
        timeframe = self.processor._detect_timeframe(test_data)
        assert timeframe is None
    
    def test_set_timestamp_index(self):
        """Test setting timestamp as index."""
        test_data = pd.DataFrame({
            'timestamp': pd.date_range('2023-01-01', periods=10, freq='1min'),
            'open': np.random.rand(10),
            'high': np.random.rand(10),
            'low': np.random.rand(10),
            'close': np.random.rand(10),
            'volume': np.random.rand(10)
        })
        
        result = self.processor._set_timestamp_index(test_data)
        
        assert result.index.name == 'timestamp'
        assert isinstance(result.index, pd.DatetimeIndex)
        assert 'timestamp' not in result.columns
    
    def test_set_timestamp_index_no_timestamp(self):
        """Test setting timestamp index when no timestamp column exists."""
        test_data = pd.DataFrame({
            'open': np.random.rand(10),
            'high': np.random.rand(10),
            'low': np.random.rand(10),
            'close': np.random.rand(10),
            'volume': np.random.rand(10)
        })
        
        result = self.processor._set_timestamp_index(test_data)
        
        # Should return unchanged if no timestamp column
        assert result.index.name is None
        assert 'open' in result.columns
    
    def test_process_symbol_data(self):
        """Test processing of symbol data."""
        test_data = pd.DataFrame({
            'open_time': pd.date_range('2023-01-01', periods=100, freq='1min'),
            'open': np.random.rand(100),
            'high': np.random.rand(100),
            'low': np.random.rand(100),
            'close': np.random.rand(100),
            'volume': np.random.rand(100)
        })
        
        symbol_data = {
            'data': {
                'M1': {
                    'file_path': '/test/path.parquet',
                    'source': 'binance',
                    'symbol': 'BTCUSDT',
                    'timeframe': 'M1',
                    'data': test_data,
                    'size_mb': 1.0,
                    'rows': 100,
                    'start_time': '2023-01-01',
                    'end_time': '2023-01-01',
                    'columns': list(test_data.columns)
                }
            },
            'metadata': {
                'symbol': 'BTCUSDT',
                'source': 'binance',
                'total_files': 1,
                'total_size_mb': 1.0,
                'total_rows': 100
            }
        }
        
        result = self.processor.process_symbol_data(symbol_data)
        
        assert result["status"] == "success"
        assert len(result["data"]) == 1
        assert "M1" in result["data"]
        assert result["metadata"]["symbol"] == "BTCUSDT"
        assert result["metadata"]["processed_count"] == 1
    
    def test_process_symbol_data_empty(self):
        """Test processing of empty symbol data."""
        symbol_data = {
            'data': {},
            'metadata': {
                'symbol': 'BTCUSDT',
                'source': 'binance',
                'total_files': 0,
                'total_size_mb': 0.0,
                'total_rows': 0
            }
        }
        
        result = self.processor.process_symbol_data(symbol_data)
        
        assert result["status"] == "error"
        assert "No data processed" in result["message"]
    
    def test_format_time(self):
        """Test time formatting function."""
        # Test seconds
        assert self.processor._format_time(30.5) == "30.5s"
        
        # Test minutes
        assert self.processor._format_time(90) == "1m 30s"
        
        # Test hours
        assert self.processor._format_time(3661) == "1h 1m"
    
    @patch('src.interactive.data_management.raw_parquet.raw_parquet_processor.print_info')
    def test_show_progress(self, mock_print_info):
        """Test progress display function."""
        self.processor._show_progress("Test message", 0.5, "1m 30s", "2.0 files/s")
        
        # Should call print_info with progress information
        mock_print_info.assert_called()
    
    def test_process_single_data_error(self):
        """Test error handling in single data processing."""
        # Create invalid data info
        data_info = {
            'file_path': '/test/path.parquet',
            'source': 'binance',
            'symbol': 'BTCUSDT',
            'timeframe': 'M1',
            'data': None,  # Invalid data
            'size_mb': 1.0,
            'rows': 100,
            'start_time': '2023-01-01',
            'end_time': '2023-01-01',
            'columns': []
        }
        
        result = self.processor._process_single_data(data_info)
        
        assert result is None
