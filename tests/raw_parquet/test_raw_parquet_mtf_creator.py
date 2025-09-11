# -*- coding: utf-8 -*-
"""
Unit tests for RawParquetMTFCreator.

This module contains comprehensive unit tests for the RawParquetMTFCreator class
to ensure proper functionality of MTF structure creation from raw parquet data.
"""

import pytest
import pandas as pd
import numpy as np
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import tempfile
import os
import sys
import json

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.interactive.data_management.raw_parquet.raw_parquet_mtf_creator import RawParquetMTFCreator

class TestRawParquetMTFCreator:
    """Test cases for RawParquetMTFCreator class."""
    
    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.mtf_creator = RawParquetMTFCreator()
        self.temp_dir = tempfile.mkdtemp()
        self.mtf_creator.cleaned_root = Path(self.temp_dir)
        self.mtf_creator.mtf_root = self.mtf_creator.cleaned_root / "mtf_structures"
    
    def teardown_method(self):
        """Clean up after each test method."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_init(self):
        """Test MTF creator initialization."""
        assert self.mtf_creator.project_root is not None
        assert self.mtf_creator.data_root is not None
        assert self.mtf_creator.cleaned_root is not None
        assert self.mtf_creator.mtf_root is not None
    
    def test_create_mtf_structure(self):
        """Test MTF structure creation."""
        # Create test processed data
        test_data_m1 = pd.DataFrame({
            'timestamp': pd.date_range('2023-01-01', periods=100, freq='1min'),
            'open': np.random.rand(100),
            'high': np.random.rand(100),
            'low': np.random.rand(100),
            'close': np.random.rand(100),
            'volume': np.random.rand(100)
        }).set_index('timestamp')
        
        test_data_h1 = pd.DataFrame({
            'timestamp': pd.date_range('2023-01-01', periods=10, freq='1H'),
            'open': np.random.rand(10),
            'high': np.random.rand(10),
            'low': np.random.rand(10),
            'close': np.random.rand(10),
            'volume': np.random.rand(10)
        }).set_index('timestamp')
        
        processed_data = {
            'M1': {
                'data': test_data_m1,
                'timeframe': 'M1',
                'source': 'binance',
                'symbol': 'BTCUSDT'
            },
            'H1': {
                'data': test_data_h1,
                'timeframe': 'H1',
                'source': 'binance',
                'symbol': 'BTCUSDT'
            }
        }
        
        result = self.mtf_creator.create_mtf_structure(processed_data, 'BTCUSDT', 'M1', 'binance')
        
        assert result["status"] == "success"
        assert result["mtf_data"]["symbol"] == "BTCUSDT"
        assert result["mtf_data"]["source"] == "binance"
        assert result["mtf_data"]["main_timeframe"] == "M1"
        assert len(result["mtf_data"]["timeframes"]) == 2
        assert "M1" in result["mtf_data"]["timeframes"]
        assert "H1" in result["mtf_data"]["timeframes"]
        assert len(result["mtf_data"]["main_data"]) == 100
        assert len(result["mtf_data"]["timeframe_data"]) == 2
        assert "cross_timeframe_features" in result["mtf_data"]
    
    def test_create_mtf_structure_single_timeframe(self):
        """Test MTF structure creation with single timeframe."""
        # Create test processed data
        test_data = pd.DataFrame({
            'timestamp': pd.date_range('2023-01-01', periods=100, freq='1min'),
            'open': np.random.rand(100),
            'high': np.random.rand(100),
            'low': np.random.rand(100),
            'close': np.random.rand(100),
            'volume': np.random.rand(100)
        }).set_index('timestamp')
        
        processed_data = {
            'M1': {
                'data': test_data,
                'timeframe': 'M1',
                'source': 'binance',
                'symbol': 'BTCUSDT'
            }
        }
        
        result = self.mtf_creator.create_mtf_structure(processed_data, 'BTCUSDT', 'M1', 'binance')
        
        assert result["status"] == "success"
        assert result["mtf_data"]["symbol"] == "BTCUSDT"
        assert result["mtf_data"]["main_timeframe"] == "M1"
        assert len(result["mtf_data"]["timeframes"]) == 1
        assert "M1" in result["mtf_data"]["timeframes"]
        assert len(result["mtf_data"]["main_data"]) == 100
        assert "cross_timeframe_features" not in result["mtf_data"]
    
    def test_create_mtf_structure_no_data(self):
        """Test MTF structure creation with no valid data."""
        processed_data = {}
        
        result = self.mtf_creator.create_mtf_structure(processed_data, 'BTCUSDT', 'M1', 'binance')
        
        assert result["status"] == "error"
        assert "No valid timeframe data found" in result["message"]
    
    def test_create_cross_timeframe_features(self):
        """Test cross-timeframe features creation."""
        # Create test dataframes
        main_data = pd.DataFrame({
            'open': np.random.rand(100),
            'high': np.random.rand(100),
            'low': np.random.rand(100),
            'close': np.random.rand(100),
            'volume': np.random.rand(100)
        }, index=pd.date_range('2023-01-01', periods=100, freq='1min'))
        
        h1_data = pd.DataFrame({
            'open': np.random.rand(10),
            'high': np.random.rand(10),
            'low': np.random.rand(10),
            'close': np.random.rand(10),
            'volume': np.random.rand(10)
        }, index=pd.date_range('2023-01-01', periods=10, freq='1H'))
        
        timeframe_data = {
            'M1': main_data,
            'H1': h1_data
        }
        
        result = self.mtf_creator._create_cross_timeframe_features(timeframe_data, 'M1')
        
        assert 'H1' in result
        assert len(result['H1']) == 100  # Should be resampled to main timeframe
        assert all(col.startswith('H1_') for col in result['H1'].columns)
    
    def test_create_cross_timeframe_features_error(self):
        """Test cross-timeframe features creation with error."""
        timeframe_data = {
            'M1': pd.DataFrame(),
            'H1': pd.DataFrame()
        }
        
        result = self.mtf_creator._create_cross_timeframe_features(timeframe_data, 'M1')
        
        assert result == {}
    
    def test_save_mtf_structure(self):
        """Test MTF structure saving."""
        # Create test MTF data
        test_data = pd.DataFrame({
            'open': np.random.rand(100),
            'high': np.random.rand(100),
            'low': np.random.rand(100),
            'close': np.random.rand(100),
            'volume': np.random.rand(100)
        }, index=pd.date_range('2023-01-01', periods=100, freq='1min'))
        
        mtf_data = {
            'symbol': 'BTCUSDT',
            'source': 'binance',
            'main_timeframe': 'M1',
            'timeframes': ['M1'],
            'main_data': test_data,
            'timeframe_data': {'M1': test_data},
            'metadata': {
                'created_at': '2023-01-01T00:00:00',
                'total_rows': 100,
                'timeframe_counts': {'M1': 100},
                'source': 'binance'
            }
        }
        
        self.mtf_creator._save_mtf_structure('BTCUSDT', mtf_data, 'binance')
        
        # Check if files were created
        source_dir = self.mtf_creator.mtf_root / 'binance'
        symbol_dir = source_dir / 'btcusdt'
        
        assert source_dir.exists()
        assert symbol_dir.exists()
        
        # Check main data file
        main_file = symbol_dir / 'btcusdt_main_m1.parquet'
        assert main_file.exists()
        
        # Check metadata file
        metadata_file = symbol_dir / 'mtf_metadata.json'
        assert metadata_file.exists()
        
        # Verify metadata content
        with open(metadata_file, 'r') as f:
            metadata = json.load(f)
        
        assert metadata['symbol'] == 'BTCUSDT'
        assert metadata['source'] == 'binance'
        assert metadata['main_timeframe'] == 'M1'
        assert metadata['timeframes'] == ['M1']
    
    def test_save_mtf_structure_with_cross_features(self):
        """Test MTF structure saving with cross-timeframe features."""
        # Create test MTF data
        test_data = pd.DataFrame({
            'open': np.random.rand(100),
            'high': np.random.rand(100),
            'low': np.random.rand(100),
            'close': np.random.rand(100),
            'volume': np.random.rand(100)
        }, index=pd.date_range('2023-01-01', periods=100, freq='1min'))
        
        cross_data = pd.DataFrame({
            'H1_open': np.random.rand(100),
            'H1_high': np.random.rand(100),
            'H1_low': np.random.rand(100),
            'H1_close': np.random.rand(100),
            'H1_volume': np.random.rand(100)
        }, index=pd.date_range('2023-01-01', periods=100, freq='1min'))
        
        mtf_data = {
            'symbol': 'BTCUSDT',
            'source': 'binance',
            'main_timeframe': 'M1',
            'timeframes': ['M1', 'H1'],
            'main_data': test_data,
            'timeframe_data': {'M1': test_data, 'H1': test_data},
            'cross_timeframe_features': {'H1': cross_data},
            'metadata': {
                'created_at': '2023-01-01T00:00:00',
                'total_rows': 100,
                'timeframe_counts': {'M1': 100, 'H1': 100},
                'source': 'binance'
            }
        }
        
        self.mtf_creator._save_mtf_structure('BTCUSDT', mtf_data, 'binance')
        
        # Check if cross-timeframe directory was created
        source_dir = self.mtf_creator.mtf_root / 'binance'
        symbol_dir = source_dir / 'btcusdt'
        cross_dir = symbol_dir / 'cross_timeframes'
        
        assert cross_dir.exists()
        
        # Check cross-timeframe file
        cross_file = cross_dir / 'btcusdt_h1_cross.parquet'
        assert cross_file.exists()
    
    def test_create_mtf_from_symbol_data(self):
        """Test MTF creation from symbol data."""
        # Create test symbol data
        test_data = pd.DataFrame({
            'timestamp': pd.date_range('2023-01-01', periods=100, freq='1min'),
            'open': np.random.rand(100),
            'high': np.random.rand(100),
            'low': np.random.rand(100),
            'close': np.random.rand(100),
            'volume': np.random.rand(100)
        }).set_index('timestamp')
        
        symbol_data = {
            'data': {
                'M1': {
                    'data': test_data,
                    'timeframe': 'M1',
                    'source': 'binance',
                    'symbol': 'BTCUSDT'
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
        
        result = self.mtf_creator.create_mtf_from_symbol_data(symbol_data, 'M1')
        
        assert result["status"] == "success"
        assert result["mtf_data"]["symbol"] == "BTCUSDT"
        assert result["mtf_data"]["source"] == "binance"
        assert result["mtf_data"]["main_timeframe"] == "M1"
    
    def test_create_mtf_from_symbol_data_error(self):
        """Test MTF creation from symbol data with error."""
        symbol_data = {
            'data': {},
            'metadata': {
                'symbol': 'BTCUSDT',
                'source': 'binance'
            }
        }
        
        result = self.mtf_creator.create_mtf_from_symbol_data(symbol_data, 'M1')
        
        assert result["status"] == "error"
        assert "No valid timeframe data found" in result["message"]
    
    def test_create_mtf_from_processed_data(self):
        """Test MTF creation from processed data."""
        # Create test processed data
        test_data = pd.DataFrame({
            'timestamp': pd.date_range('2023-01-01', periods=100, freq='1min'),
            'open': np.random.rand(100),
            'high': np.random.rand(100),
            'low': np.random.rand(100),
            'close': np.random.rand(100),
            'volume': np.random.rand(100)
        }).set_index('timestamp')
        
        processed_data = {
            'M1': {
                'data': test_data,
                'timeframe': 'M1',
                'source': 'binance',
                'symbol': 'BTCUSDT'
            }
        }
        
        result = self.mtf_creator.create_mtf_from_processed_data(processed_data, 'BTCUSDT', 'M1', 'binance')
        
        assert result["status"] == "success"
        assert result["mtf_data"]["symbol"] == "BTCUSDT"
        assert result["mtf_data"]["source"] == "binance"
        assert result["mtf_data"]["main_timeframe"] == "M1"
    
    def test_create_mtf_from_processed_data_no_data(self):
        """Test MTF creation from processed data with no data."""
        processed_data = {}
        
        result = self.mtf_creator.create_mtf_from_processed_data(processed_data, 'BTCUSDT', 'M1', 'binance')
        
        assert result["status"] == "error"
        assert "No valid timeframe data found" in result["message"]
    
    def test_create_mtf_structure_with_progress(self):
        """Test MTF structure creation with progress tracking."""
        # Create test dataframes
        test_data = pd.DataFrame({
            'open': np.random.rand(100),
            'high': np.random.rand(100),
            'low': np.random.rand(100),
            'close': np.random.rand(100),
            'volume': np.random.rand(100)
        }, index=pd.date_range('2023-01-01', periods=100, freq='1min'))
        
        timeframe_data = {
            'M1': test_data,
            'H1': test_data
        }
        
        result = self.mtf_creator._create_mtf_structure_with_progress(timeframe_data, 'BTCUSDT', 'M1', 'binance')
        
        assert result['symbol'] == 'BTCUSDT'
        assert result['source'] == 'binance'
        assert result['main_timeframe'] == 'M1'
        assert len(result['timeframes']) == 2
        assert 'cross_timeframe_features' in result
    
    def test_create_cross_timeframe_features_with_progress(self):
        """Test cross-timeframe features creation with progress tracking."""
        # Create test dataframes
        main_data = pd.DataFrame({
            'open': np.random.rand(100),
            'high': np.random.rand(100),
            'low': np.random.rand(100),
            'close': np.random.rand(100),
            'volume': np.random.rand(100)
        }, index=pd.date_range('2023-01-01', periods=100, freq='1min'))
        
        h1_data = pd.DataFrame({
            'open': np.random.rand(10),
            'high': np.random.rand(10),
            'low': np.random.rand(10),
            'close': np.random.rand(10),
            'volume': np.random.rand(10)
        }, index=pd.date_range('2023-01-01', periods=10, freq='1H'))
        
        timeframe_data = {
            'M1': main_data,
            'H1': h1_data
        }
        
        result = self.mtf_creator._create_cross_timeframe_features_with_progress(
            timeframe_data, 'M1', 0.0, 1, 3)
        
        assert 'H1' in result
        assert len(result['H1']) == 100
        assert all(col.startswith('H1_') for col in result['H1'].columns)
    
    def test_format_time(self):
        """Test time formatting function."""
        # Test seconds
        assert self.mtf_creator._format_time(30.5) == "30.5s"
        
        # Test minutes
        assert self.mtf_creator._format_time(90) == "1m 30s"
        
        # Test hours
        assert self.mtf_creator._format_time(3661) == "1h 1m"
    
    @patch('builtins.print')
    def test_show_mtf_progress(self, mock_print):
        """Test MTF progress display function."""
        self.mtf_creator._show_mtf_progress("Test message", 0.5, 0.0)
        
        # Should call print with progress information
        mock_print.assert_called()
    
    def test_save_mtf_structure_error(self):
        """Test error handling in MTF structure saving."""
        # Create invalid MTF data
        mtf_data = {
            'symbol': 'BTCUSDT',
            'source': 'binance',
            'main_timeframe': 'M1',
            'timeframes': ['M1'],
            'main_data': None,  # Invalid data
            'timeframe_data': {'M1': None},
            'metadata': {
                'created_at': '2023-01-01T00:00:00',
                'total_rows': 0,
                'timeframe_counts': {'M1': 0},
                'source': 'binance'
            }
        }
        
        # Should not raise exception
        self.mtf_creator._save_mtf_structure('BTCUSDT', mtf_data, 'binance')
