# File: tests/data/test_data_acquisition_refactored.py
# -*- coding: utf-8 -*-

"""
Tests for refactored data acquisition modules.
Ensures all functionality remains working after refactoring.
All comments are in English.
"""

import pytest
import pandas as pd
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime, timedelta

# Import the refactored modules
from src.data.data_acquisition_core import acquire_data
from src.data.data_acquisition_utils import (
    _get_interval_delta, _generate_instrument_parquet_filename,
    _process_csv_folder, _process_csv_single, _process_api_data,
    _validate_dataframe, _clean_dataframe_index, _get_dataframe_summary,
    _update_data_info_metrics
)


class TestDataAcquisitionRefactored:
    """Test class for refactored data acquisition functionality."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.mock_args = Mock()
        self.mock_args.mode = 'yfinance'
        self.mock_args.ticker = 'AAPL'
        self.mock_args.interval = '1h'
        self.mock_args.period = None
        self.mock_args.start = '2024-01-01'
        self.mock_args.end = '2024-01-31'
        self.mock_args.csv_file = None
        self.mock_args.csv_folder = None
    
    def test_get_interval_delta_valid_intervals(self):
        """Test interval delta parsing for valid intervals."""
        # Test common intervals
        assert _get_interval_delta('1h') == pd.Timedelta('1h')
        assert _get_interval_delta('1d') == pd.Timedelta('1d')
        assert _get_interval_delta('1min') == pd.Timedelta('1min')
        
        # Test mapped intervals
        assert _get_interval_delta('H1') == pd.Timedelta('1h')
        assert _get_interval_delta('D1') == pd.Timedelta('1d')
        assert _get_interval_delta('M1') == pd.Timedelta('1min')
        assert _get_interval_delta('W') == pd.Timedelta('7d')
        assert _get_interval_delta('MN1') == pd.Timedelta('30d')
    
    def test_get_interval_delta_invalid_intervals(self):
        """Test interval delta parsing for invalid intervals."""
        # Test invalid intervals
        result = _get_interval_delta('invalid_interval')
        assert result is None
    
    def test_generate_instrument_parquet_filename(self):
        """Test parquet filename generation."""
        # Test yfinance mode
        self.mock_args.mode = 'yf'
        filename = _generate_instrument_parquet_filename(self.mock_args)
        assert filename is not None
        assert 'yfinance_AAPL_1h.parquet' in str(filename)
        
        # Test polygon mode
        self.mock_args.mode = 'polygon'
        filename = _generate_instrument_parquet_filename(self.mock_args)
        assert filename is not None
        assert 'polygon_AAPL_1h.parquet' in str(filename)
        
        # Test binance mode
        self.mock_args.mode = 'binance'
        filename = _generate_instrument_parquet_filename(self.mock_args)
        assert filename is not None
        assert 'binance_AAPL_1h.parquet' in str(filename)
        
        # Test exrate mode
        self.mock_args.mode = 'exrate'
        filename = _generate_instrument_parquet_filename(self.mock_args)
        assert filename is not None
        assert 'exrate_AAPL_1h.parquet' in str(filename)
    
    def test_generate_instrument_parquet_filename_no_ticker(self):
        """Test parquet filename generation without ticker."""
        self.mock_args.ticker = None
        filename = _generate_instrument_parquet_filename(self.mock_args)
        assert filename is None
    
    def test_generate_instrument_parquet_filename_unsupported_mode(self):
        """Test parquet filename generation for unsupported mode."""
        self.mock_args.mode = 'unsupported'
        filename = _generate_instrument_parquet_filename(self.mock_args)
        assert filename is None
    
    @patch('src.data.csv_folder_processor.process_csv_folder')
    def test_process_csv_folder(self, mock_process_csv_folder):
        """Test CSV folder processing."""
        # Mock successful folder processing
        mock_process_csv_folder.return_value = {
            'success': True,
            'files_processed': 5,
            'files_failed': 0,
            'total_time': 10.5,
            'total_size_mb': 25.0
        }
        
        self.mock_args.csv_folder = '/path/to/csv/folder'
        self.mock_args.export_parquet = True
        self.mock_args.export_csv = False
        self.mock_args.export_json = True
        self.mock_args.point = 0.1
        self.mock_args.rule = 'OHLCV'
        self.mock_args.draw = 'candlestick'
        self.mock_args.csv_mask = '*.csv'
        
        data_info = {}
        result = _process_csv_folder(self.mock_args, data_info)
        
        assert result['data_source_label'] == 'CSV Folder: /path/to/csv/folder'
        assert result['folder_processing_results']['success'] is True
        assert result['files_processed'] == 5
        assert result['files_failed'] == 0
        assert result['total_processing_time'] == 10.5
        assert result['total_size_mb'] == 25.0
        assert result['success'] is True
        assert result['ohlcv_df'] is not None
    
    @patch('src.data.csv_folder_processor.process_csv_folder')
    def test_process_csv_folder_failure(self, mock_process_csv_folder):
        """Test CSV folder processing failure."""
        # Mock failed folder processing
        mock_process_csv_folder.return_value = {
            'success': False,
            'error': 'Processing failed'
        }
        
        self.mock_args.csv_folder = '/path/to/csv/folder'
        
        data_info = {}
        
        with pytest.raises(ValueError, match="Failed to process CSV folder"):
            _process_csv_folder(self.mock_args, data_info)
    
    @patch('src.data.fetchers.fetch_csv_data')
    def test_process_csv_single(self, mock_fetch_csv_data):
        """Test single CSV file processing."""
        # Mock successful CSV loading
        mock_df = pd.DataFrame({
            'DateTime,': pd.date_range('2024-01-01', periods=100, freq='1H'),
            'Open,': [100.0] * 100,
            'High,': [110.0] * 100,
            'Low,': [90.0] * 100,
            'Close,': [105.0] * 100,
            'TickVolume,': [1000] * 100
        })
        mock_fetch_csv_data.return_value = mock_df
        
        self.mock_args.csv_file = '/path/to/file.csv'
        
        data_info = {}
        result = _process_csv_single(self.mock_args, data_info)
        
        assert result['data_source_label'] == '/path/to/file.csv'
        assert result['ohlcv_df'] is not None
        assert len(result['ohlcv_df']) == 100
    
    @patch('src.data.fetchers.fetch_csv_data')
    def test_process_csv_single_failure(self, mock_fetch_csv_data):
        """Test single CSV file processing failure."""
        # Mock failed CSV loading
        mock_fetch_csv_data.return_value = None
        
        self.mock_args.csv_file = '/path/to/file.csv'
        
        data_info = {}
        
        with pytest.raises(ValueError, match="Failed to read or process CSV file"):
            _process_csv_single(self.mock_args, data_info)
    
    def test_process_csv_single_file_size(self):
        """Test single CSV file processing with file size calculation."""
        # Create a temporary CSV file for testing
        import tempfile
        import os
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            f.write("DateTime,Open,High,Low,Close,Volume\n")
            f.write("2024-01-01 00:00:00,100,110,90,105,1000\n")
            f.write("2024-01-01 01:00:00,105,115,95,110,1100\n")
            temp_file = f.name
        
        try:
            self.mock_args.csv_file = temp_file
            
            # Mock successful CSV loading
            with patch('src.data.fetchers.fetch_csv_data') as mock_fetch:
                mock_df = pd.DataFrame({
                    'DateTime,': pd.date_range('2024-01-01', periods=2, freq='1H'),
                    'Open,': [100.0, 105.0],
                    'High,': [110.0, 115.0],
                    'Low,': [90.0, 95.0],
                    'Close,': [105.0, 110.0],
                    'TickVolume,': [1000, 1100]
                })
                mock_fetch.return_value = mock_df
                
                data_info = {}
                result = _process_csv_single(self.mock_args, data_info)
                
                assert result['file_size_bytes'] is not None
                assert result['file_size_bytes'] > 0
                
        finally:
            # Clean up temporary file
            if os.path.exists(temp_file):
                os.unlink(temp_file)
    
    def test_validate_dataframe(self):
        """Test DataFrame validation utilities."""
        # Test valid DataFrame
        valid_df = pd.DataFrame({
            'timestamp': pd.date_range('2024-01-01', periods=100, freq='1H'),
            'value': range(100)
        })
        valid_df = valid_df.set_index('timestamp')
        
        assert _validate_dataframe(valid_df, "Test") is True
        
        # Test None DataFrame
        assert _validate_dataframe(None, "Test") is False
        
        # Test empty DataFrame
        empty_df = pd.DataFrame()
        assert _validate_dataframe(empty_df, "Test") is False
        
        # Test DataFrame without DatetimeIndex
        invalid_df = pd.DataFrame({'value': range(100)})
        assert _validate_dataframe(invalid_df, "Test") is False
    
    def test_clean_dataframe_index(self):
        """Test DataFrame index cleaning utilities."""
        # Test DataFrame with timezone info
        df_with_tz = pd.DataFrame({
            'value': range(100)
        })
        df_with_tz.index = pd.date_range('2024-01-01', periods=100, freq='1H', tz='UTC')
        
        cleaned_df = _clean_dataframe_index(df_with_tz)
        assert cleaned_df.index.tz is None
        
        # Test DataFrame without timezone info
        df_without_tz = pd.DataFrame({
            'value': range(100)
        })
        df_without_tz.index = pd.date_range('2024-01-01', periods=100, freq='1H')
        
        cleaned_df = _clean_dataframe_index(df_without_tz)
        assert cleaned_df.index.tz is None
    
    def test_get_dataframe_summary(self):
        """Test DataFrame summary utilities."""
        # Test with valid DataFrame
        test_df = pd.DataFrame({
            'timestamp': pd.date_range('2024-01-01', periods=100, freq='1H'),
            'value1': range(100),
            'value2': [float(x) for x in range(100)]
        })
        test_df = test_df.set_index('timestamp')
        
        summary = _get_dataframe_summary(test_df)
        assert summary['rows'] == 100
        assert summary['columns'] == 2
        assert summary['memory_mb'] > 0
        assert 'value1' in summary['dtypes']
        assert 'value2' in summary['dtypes']
        
        # Test with empty DataFrame
        empty_summary = _get_dataframe_summary(pd.DataFrame())
        assert empty_summary['rows'] == 0
        assert empty_summary['columns'] == 0
        assert empty_summary['memory_mb'] == 0.0
    
    def test_update_data_info_metrics(self):
        """Test data info metrics update utilities."""
        data_info = {
            'parquet_cache_used': False,
            'data_metrics': {}
        }
        
        combined_metrics = {
            'total_latency_sec': 2.5,
            'api_calls': 5,
            'successful_chunks': 3,
            'rows_fetched': 1000,
            'file_size_bytes': 1024
        }
        
        _update_data_info_metrics(data_info, combined_metrics)
        
        assert data_info['api_latency_sec'] == 2.5
        assert data_info['api_calls'] == 5
        assert data_info['successful_chunks'] == 3
        assert data_info['rows_fetched'] == 1000
        assert data_info['file_size_bytes'] == 1024


if __name__ == "__main__":
    pytest.main([__file__])
