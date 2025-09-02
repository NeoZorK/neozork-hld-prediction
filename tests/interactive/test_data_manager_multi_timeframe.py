#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests for DataManager multi-timeframe functionality.

This module tests the new multi-timeframe data loading strategy
that properly handles different timeframes (M1, M5, H1, D1, MN1) for ML models.
"""

import pytest
import pandas as pd
import numpy as np
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import tempfile
import shutil

from src.interactive.data_manager import DataManager


class TestDataManagerMultiTimeframe:
    """Test multi-timeframe data loading functionality."""
    
    def setup_method(self):
        """Set up test environment."""
        self.data_manager = DataManager()
        self.mock_system = Mock()
        self.mock_system.current_data = None
        self.mock_system.timeframe_info = None
        self.mock_system.cross_timeframe_data = None
        
        # Create temporary test data directory
        self.temp_dir = tempfile.mkdtemp()
        self.test_data_dir = Path(self.temp_dir) / "data"
        self.test_data_dir.mkdir(parents=True)
        
        # Create test files for different timeframes
        self._create_test_timeframe_files()
    
    def teardown_method(self):
        """Clean up test environment."""
        if hasattr(self, 'temp_dir') and Path(self.temp_dir).exists():
            shutil.rmtree(self.temp_dir)
    
    def _create_test_timeframe_files(self):
        """Create test files with different timeframe patterns."""
        # Create sample data for different timeframes
        base_data = {
            'Open': [100.0, 101.0, 102.0, 103.0, 104.0],
            'High': [101.0, 102.0, 103.0, 104.0, 105.0],
            'Low': [99.0, 100.0, 101.0, 102.0, 103.0],
            'Close': [100.5, 101.5, 102.5, 103.5, 104.5],
            'Volume': [1000, 1100, 1200, 1300, 1400]
        }
        
        # Create files with timeframe patterns
        timeframe_files = {
            'M1': 'EURUSD_PERIOD_M1.csv',
            'M5': 'GBPUSD_M5_data.csv',
            'H1': 'BTCUSDT_H1.parquet',
            'D1': 'CSVExport_EURUSD_PERIOD_D1.csv',
            'MN1': 'GBPUSD_PERIOD_MN1.parquet'
        }
        
        for tf, filename in timeframe_files.items():
            file_path = self.test_data_dir / filename
            df = pd.DataFrame(base_data)
            
            if filename.endswith('.csv'):
                df.to_csv(file_path, index=False)
            else:  # parquet
                df.to_parquet(file_path, index=False)
    
    def test_detect_timeframe_from_filename(self):
        """Test timeframe detection from filename patterns."""
        test_cases = [
            ('EURUSD_PERIOD_M1.csv', 'M1'),
            ('GBPUSD_M5_data.csv', 'M5'),
            ('BTCUSDT_H1.parquet', 'H1'),
            ('CSVExport_EURUSD_PERIOD_D1.csv', 'D1'),
            ('GBPUSD_PERIOD_MN1.parquet', 'MN1'),
            ('binance_BTCUSDT_H1.parquet', 'H1'),
            ('yfinance_AAPL_D1.parquet', 'D1'),
            ('unknown_file.csv', 'UNKNOWN')
        ]
        
        for filename, expected_tf in test_cases:
            result = self.data_manager._detect_timeframe_from_filename(filename)
            assert result == expected_tf, f"Expected {expected_tf} for {filename}, got {result}"
    
    @patch('builtins.input')
    @patch('pathlib.Path.cwd')
    def test_load_multi_timeframe_data_success(self, mock_cwd, mock_input):
        """Test successful multi-timeframe data loading."""
        # Mock current working directory to our temp directory
        mock_cwd.return_value = Path(self.temp_dir)
        
        # Mock user inputs: select timeframe 1 (first available), then no cross-timeframe features
        mock_input.side_effect = ['1', 'n']
        
        # Mock file loading
        with patch.object(self.data_manager, 'load_data_from_file') as mock_load:
            # Return test DataFrame
            test_df = pd.DataFrame({
                'Open': [100.0, 101.0],
                'High': [101.0, 102.0],
                'Low': [99.0, 100.0],
                'Close': [100.5, 101.5],
                'Volume': [1000, 1100]
            })
            mock_load.return_value = test_df
            
            result = self.data_manager.load_multi_timeframe_data(self.mock_system)
            
            assert result is True
            assert self.mock_system.current_data is not None
            assert hasattr(self.mock_system, 'timeframe_info')
            assert 'base_timeframe' in self.mock_system.timeframe_info
    
    @patch('builtins.input')
    @patch('pathlib.Path.cwd')
    def test_load_multi_timeframe_data_with_cross_features(self, mock_cwd, mock_input):
        """Test multi-timeframe data loading with cross-timeframe features."""
        # Mock current working directory to our temp directory
        mock_cwd.return_value = Path(self.temp_dir)
        
        # Mock user inputs: select timeframe 1, then yes to cross-timeframe features
        mock_input.side_effect = ['1', 'y']
        
        # Mock file loading
        with patch.object(self.data_manager, 'load_data_from_file') as mock_load:
            test_df = pd.DataFrame({
                'Open': [100.0, 101.0],
                'High': [101.0, 102.0],
                'Low': [99.0, 100.0],
                'Close': [100.5, 101.5],
                'Volume': [1000, 1100]
            })
            mock_load.return_value = test_df
            
            # Mock cross-timeframe feature generation
            with patch('src.ml.feature_engineering.CrossTimeframeFeatureGenerator') as mock_generator:
                mock_gen_instance = Mock()
                mock_gen_instance.generate_features.return_value = test_df
                mock_generator.return_value = mock_gen_instance
                
                result = self.data_manager.load_multi_timeframe_data(self.mock_system)
                
                assert result is True
                assert hasattr(self.mock_system, 'cross_timeframe_data')
    
    @patch('builtins.input')
    def test_load_multi_timeframe_data_user_exit(self, mock_input):
        """Test user exit during multi-timeframe data loading."""
        # Mock EOFError (user exit)
        mock_input.side_effect = EOFError()
        
        result = self.data_manager.load_multi_timeframe_data(self.mock_system)
        assert result is False
    
    @patch('builtins.input')
    @patch('pathlib.Path.cwd')
    def test_load_multi_timeframe_data_invalid_choice(self, mock_cwd, mock_input):
        """Test invalid timeframe choice."""
        # Mock current working directory to our temp directory
        mock_cwd.return_value = Path(self.temp_dir)
        
        # Mock invalid user input
        mock_input.return_value = 'invalid'
        
        result = self.data_manager.load_multi_timeframe_data(self.mock_system)
        assert result is False
    
    def test_detect_timeframe_edge_cases(self):
        """Test edge cases for timeframe detection."""
        edge_cases = [
            ('', 'UNKNOWN'),
            ('file_without_timeframe.csv', 'UNKNOWN'),
            ('EURUSD_1MINUTE_data.csv', 'M1'),
            ('GBPUSD_5MINUTE_data.csv', 'M5'),
            ('BTCUSDT_1HOUR_data.csv', 'H1'),
            ('AAPL_DAILY_data.csv', 'D1'),
            ('SPY_WEEKLY_data.csv', 'W1'),
            ('EURUSD_MONTHLY_data.csv', 'MN1')
        ]
        
        for filename, expected_tf in edge_cases:
            result = self.data_manager._detect_timeframe_from_filename(filename)
            assert result == expected_tf, f"Expected {expected_tf} for {filename}, got {result}"
    
    @patch('builtins.input')
    @patch('pathlib.Path.cwd')
    def test_add_cross_timeframe_features(self, mock_cwd, mock_input):
        """Test adding cross-timeframe features."""
        # Setup mock system with timeframe info
        self.mock_system.timeframe_info = {
            'base_timeframe': 'H1',
            'cross_timeframes': {
                'D1': [Path('test_D1.csv')],
                'M5': [Path('test_M5.csv')]
            }
        }
        
        # Mock file loading
        with patch.object(self.data_manager, 'load_data_from_file') as mock_load:
            test_df = pd.DataFrame({
                'Open': [100.0, 101.0],
                'High': [101.0, 102.0],
                'Low': [99.0, 100.0],
                'Close': [100.5, 101.5],
                'Volume': [1000, 1100]
            })
            mock_load.return_value = test_df
            
            # Mock cross-timeframe feature generation
            with patch('src.ml.feature_engineering.CrossTimeframeFeatureGenerator') as mock_generator:
                mock_gen_instance = Mock()
                mock_gen_instance.generate_features.return_value = test_df
                mock_generator.return_value = mock_gen_instance
                
                result = self.data_manager._add_cross_timeframe_features(self.mock_system)
                
                assert result is True
                assert hasattr(self.mock_system, 'cross_timeframe_data')
    
    def test_memory_optimization_settings(self):
        """Test memory optimization settings for multi-timeframe loading."""
        # Test default settings
        assert self.data_manager.max_memory_mb > 0
        assert self.data_manager.chunk_size > 0
        assert isinstance(self.data_manager.enable_memory_optimization, bool)
        
        # Test memory checking
        memory_available = self.data_manager._check_memory_available(100)  # 100MB
        assert isinstance(memory_available, bool)
    
    @patch('pathlib.Path.exists')
    def test_load_multi_timeframe_data_no_data_folder(self, mock_exists):
        """Test handling when data folder doesn't exist."""
        mock_exists.return_value = False
        
        result = self.data_manager.load_multi_timeframe_data(self.mock_system)
        assert result is False


if __name__ == '__main__':
    pytest.main([__file__])
