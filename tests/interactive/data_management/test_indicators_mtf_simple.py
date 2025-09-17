# -*- coding: utf-8 -*-
"""
Simple tests for Indicators MTF Creator functionality.

This module tests the basic functionality of the Indicators MTF Creator.
"""

import pytest
import os
import pandas as pd
import numpy as np
from pathlib import Path
from unittest.mock import Mock, patch
import tempfile
import shutil

# Add project root to path
import sys
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# Skip these tests in Docker due to memory constraints
pytestmark = pytest.mark.skipif(
    os.getenv('DOCKER_CONTAINER') == 'true',
    reason="Skipping data_management tests in Docker due to memory constraints"
)

from src.interactive.data_management.indicators.indicators_mtf_creator import IndicatorsMTFCreator


class TestIndicatorsMTFCreatorSimple:
    """Simple test cases for IndicatorsMTFCreator class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.mtf_creator = IndicatorsMTFCreator()
        
        # Mock the paths to use temp directory
        self.mtf_creator.project_root = Path(self.temp_dir)
        self.mtf_creator.data_root = Path(self.temp_dir) / "data"
        self.mtf_creator.cleaned_root = Path(self.temp_dir) / "data" / "cleaned_data"
        self.mtf_creator.mtf_root = Path(self.temp_dir) / "data" / "cleaned_data" / "mtf_structures"
        self.mtf_creator.indicators_mtf_root = Path(self.temp_dir) / "data" / "cleaned_data" / "mtf_structures" / "indicators"
        
        # Create directories
        self.mtf_creator.indicators_mtf_root.mkdir(parents=True, exist_ok=True)
    
    def teardown_method(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_init(self):
        """Test IndicatorsMTFCreator initialization."""
        creator = IndicatorsMTFCreator()
        assert creator.mtf_structures == {}
        assert creator.cross_timeframe_features == {}
        assert hasattr(creator, 'mtf_root')
    
    def test_extract_symbol_from_data(self):
        """Test symbol extraction from data."""
        # Test filename extraction
        symbol = self.mtf_creator._extract_symbol_from_data(
            'binance_BTCUSDT_M1_RSI.parquet', {}
        )
        assert symbol == 'BTCUSDT'
        
        # Test data extraction
        symbol = self.mtf_creator._extract_symbol_from_data(
            'test.parquet',
            {'symbol': 'ETHUSDT'}
        )
        assert symbol == 'ETHUSDT'
        
        # Test nested data extraction
        symbol = self.mtf_creator._extract_symbol_from_data(
            'test.parquet',
            {'data': {'symbol': 'EURUSD'}}
        )
        assert symbol == 'EURUSD'
    
    def test_group_data_by_symbol(self):
        """Test grouping data by symbol."""
        processed_data = {
            'btcusdt_rsi_m1.parquet': {
                'indicator': 'RSI',
                'timeframe': 'M1',
                'symbol': 'BTCUSDT',
                'data': pd.DataFrame()
            },
            'ethusdt_rsi_m1.parquet': {
                'indicator': 'RSI',
                'timeframe': 'M1',
                'symbol': 'ETHUSDT',
                'data': pd.DataFrame()
            }
        }
        
        grouped = self.mtf_creator._group_data_by_symbol(processed_data)
        
        assert 'BTCUSDT' in grouped
        assert 'ETHUSDT' in grouped
        assert 'M1' in grouped['BTCUSDT']
        assert 'M1' in grouped['ETHUSDT']
    
    def test_validate_mtf_structure(self):
        """Test MTF structure validation."""
        # Valid structure
        valid_mtf = {
            'symbol': 'BTCUSDT',
            'main_timeframe': 'M1',
            'indicators': ['RSI'],
            'timeframes': ['M1'],
            'main_data': pd.DataFrame({'RSI': [50, 60]}),
            'metadata': {
                'created_at': '2023-01-01',
                'total_indicators': 1,
                'total_timeframes': 1
            }
        }
        
        result = self.mtf_creator._validate_mtf_structure(valid_mtf)
        assert result['valid'] == True
        assert len(result['errors']) == 0
        
        # Invalid structure
        invalid_mtf = {
            'symbol': 'BTCUSDT',
            # Missing required fields
        }
        
        result = self.mtf_creator._validate_mtf_structure(invalid_mtf)
        assert result['valid'] == False
        assert len(result['errors']) > 0
    
    def test_calculate_data_quality_metrics(self):
        """Test data quality metrics calculation."""
        # Create sample MTF data
        mtf_data = {
            'main_data': pd.DataFrame({
                'RSI': [50, 60, 70, np.nan, 80],
                'MACD': [0.1, 0.2, 0.3, 0.4, 0.5]
            })
        }
        
        metrics = self.mtf_creator._calculate_data_quality_metrics(mtf_data)
        
        assert 'completeness' in metrics
        assert 'consistency' in metrics
        assert 'validity' in metrics
        assert 'overall_score' in metrics
        assert 0 <= metrics['completeness'] <= 100
        assert 0 <= metrics['consistency'] <= 100
        assert 0 <= metrics['validity'] <= 100
        assert 0 <= metrics['overall_score'] <= 100
    
    def test_save_mtf_structure(self):
        """Test saving MTF structure to disk."""
        # Create sample MTF data
        mtf_data = {
            'symbol': 'BTCUSDT',
            'main_timeframe': 'M1',
            'source': 'indicators',
            'indicators': ['RSI', 'MACD'],
            'timeframes': ['M1'],
            'main_data': pd.DataFrame({
                'RSI': [50, 60, 70],
                'MACD': [0.1, 0.2, 0.3]
            }),
            'metadata': {
                'created_at': '2023-01-01T00:00:00',
                'total_indicators': 2,
                'total_timeframes': 1,
                'total_rows': 3
            }
        }
        
        output_path = self.mtf_creator.indicators_mtf_root / 'test_symbol'
        
        result = self.mtf_creator.save_mtf_structure(mtf_data, output_path)
        
        assert result['status'] == 'success'
        assert output_path.exists()
        assert (output_path / "btcusdt_main_m1.parquet").exists()
        assert (output_path / "mtf_metadata.json").exists()


if __name__ == '__main__':
    pytest.main([__file__])
