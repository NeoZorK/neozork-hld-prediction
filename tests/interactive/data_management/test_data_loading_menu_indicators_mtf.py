# -*- coding: utf-8 -*-
"""
Tests for Data Loading Menu Indicators MTF functionality.

This module tests the updated data loading menu with MTF structure creation for indicators.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
import tempfile
import shutil
from pathlib import Path

# Add project root to path
import sys
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.interactive.menu_system.data_loading_menu import DataLoadingMenu


class TestDataLoadingMenuIndicatorsMTF:
    """Test cases for DataLoadingMenu indicators MTF functionality."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.menu = DataLoadingMenu()
    
    def teardown_method(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_save_all_indicators_to_mtf(self):
        """Test saving all indicators to MTF structure."""
        # Mock the required components
        mock_analyzer = Mock()
        mock_loader = Mock()
        mock_processor = Mock()
        mock_mtf_creator = Mock()
        
        # Create sample filtered files
        filtered_files = [
            {
                'filename': 'btcusdt_rsi_m1.parquet',
                'indicator': 'RSI',
                'format': 'parquet',
                'source': 'binance',
                'symbol': 'BTCUSDT'
            },
            {
                'filename': 'btcusdt_macd_m1.parquet',
                'indicator': 'MACD',
                'format': 'parquet',
                'source': 'binance',
                'symbol': 'BTCUSDT'
            }
        ]
        
        # Mock loader responses
        mock_loader.load_specific_file.side_effect = [
            {
                'status': 'success',
                'data': {'indicator': 'RSI', 'values': [50, 60, 70]}
            },
            {
                'status': 'success',
                'data': {'indicator': 'MACD', 'values': [0.1, 0.2, 0.3]}
            }
        ]
        
        # Mock processor responses
        mock_processor.process_indicators_data.return_value = {
            'status': 'success',
            'data': {
                'btcusdt_rsi_m1.parquet': {
                    'indicator': 'RSI',
                    'timeframe': 'M1',
                    'symbol': 'BTCUSDT',
                    'data': 'mock_dataframe',
                    'rows': 100
                },
                'btcusdt_macd_m1.parquet': {
                    'indicator': 'MACD',
                    'timeframe': 'M1',
                    'symbol': 'BTCUSDT',
                    'data': 'mock_dataframe',
                    'rows': 100
                }
            }
        }
        
        # Mock MTF creator response
        mock_mtf_creator.create_mtf_from_processed_data.return_value = {
            'status': 'success',
            'results': {
                'BTCUSDT': {
                    'status': 'success',
                    'save_path': '/mock/path/btcusdt',
                    'metadata': {'total_rows': 200}
                }
            },
            'summary': {
                'total_symbols': 1,
                'successful': 1,
                'failed': 0,
                'success_rate': 100.0
            }
        }
        
        # Mock the progress display method
        with patch.object(self.menu, '_show_indicators_progress'):
            # Call the method
            self.menu._save_all_indicators_to_mtf(
                filtered_files, mock_analyzer, mock_loader, 
                mock_processor, mock_mtf_creator
            )
        
        # Verify that loader was called for each file
        assert mock_loader.load_specific_file.call_count == 2
        
        # Verify that processor was called
        mock_processor.process_indicators_data.assert_called_once()
        
        # Verify that MTF creator was called
        mock_mtf_creator.create_mtf_from_processed_data.assert_called_once()
    
    def test_save_all_indicators_to_mtf_no_data(self):
        """Test saving all indicators to MTF when no data is loaded."""
        # Mock the required components
        mock_analyzer = Mock()
        mock_loader = Mock()
        mock_processor = Mock()
        mock_mtf_creator = Mock()
        
        # Mock loader to return error
        mock_loader.load_specific_file.return_value = {
            'status': 'error',
            'message': 'No data found'
        }
        
        filtered_files = [
            {
                'filename': 'btcusdt_rsi_m1.parquet',
                'indicator': 'RSI',
                'format': 'parquet',
                'source': 'binance',
                'symbol': 'BTCUSDT'
            }
        ]
        
        # Mock the progress display method
        with patch.object(self.menu, '_show_indicators_progress'):
            # Call the method
            self.menu._save_all_indicators_to_mtf(
                filtered_files, mock_analyzer, mock_loader, 
                mock_processor, mock_mtf_creator
            )
        
        # Verify that MTF creator was not called
        mock_mtf_creator.create_mtf_from_all_indicators.assert_not_called()
    
    def test_save_all_indicators_to_mtf_processing_error(self):
        """Test saving all indicators to MTF when processing fails."""
        # Mock the required components
        mock_analyzer = Mock()
        mock_loader = Mock()
        mock_processor = Mock()
        mock_mtf_creator = Mock()
        
        # Mock loader to return success
        mock_loader.load_specific_file.return_value = {
            'status': 'success',
            'data': {'indicator': 'RSI', 'values': [50, 60, 70]}
        }
        
        # Mock processor to return error
        mock_processor.process_indicators_data.return_value = {
            'status': 'error',
            'message': 'Processing failed'
        }
        
        filtered_files = [
            {
                'filename': 'btcusdt_rsi_m1.parquet',
                'indicator': 'RSI',
                'format': 'parquet',
                'source': 'binance',
                'symbol': 'BTCUSDT'
            }
        ]
        
        # Mock the progress display method
        with patch.object(self.menu, '_show_indicators_progress'):
            # Call the method
            self.menu._save_all_indicators_to_mtf(
                filtered_files, mock_analyzer, mock_loader, 
                mock_processor, mock_mtf_creator
            )
        
        # Verify that MTF creator was not called
        mock_mtf_creator.create_mtf_from_all_indicators.assert_not_called()
    
    def test_save_all_indicators_to_mtf_mtf_creation_error(self):
        """Test saving all indicators to MTF when MTF creation fails."""
        # Mock the required components
        mock_analyzer = Mock()
        mock_loader = Mock()
        mock_processor = Mock()
        mock_mtf_creator = Mock()
        
        # Mock successful loading and processing
        mock_loader.load_specific_file.return_value = {
            'status': 'success',
            'data': {'indicator': 'RSI', 'values': [50, 60, 70]}
        }
        
        mock_processor.process_indicators_data.return_value = {
            'status': 'success',
            'data': {
                'btcusdt_rsi_m1.parquet': {
                    'indicator': 'RSI',
                    'timeframe': 'M1',
                    'symbol': 'BTCUSDT',
                    'data': 'mock_dataframe',
                    'rows': 100
                }
            }
        }
        
        # Mock MTF creator to return error
        mock_mtf_creator.create_mtf_from_processed_data.return_value = {
            'status': 'error',
            'message': 'MTF creation failed'
        }
        
        filtered_files = [
            {
                'filename': 'btcusdt_rsi_m1.parquet',
                'indicator': 'RSI',
                'format': 'parquet',
                'source': 'binance',
                'symbol': 'BTCUSDT'
            }
        ]
        
        # Mock the progress display method
        with patch.object(self.menu, '_show_indicators_progress'):
            # Call the method
            self.menu._save_all_indicators_to_mtf(
                filtered_files, mock_analyzer, mock_loader, 
                mock_processor, mock_mtf_creator
            )
        
        # Verify that MTF creator was called
        mock_mtf_creator.create_mtf_from_processed_data.assert_called_once()
    
    @patch('builtins.input')
    def test_load_indicators_menu_choice_1(self, mock_input):
        """Test the indicators menu when user chooses option 1 (save to MTF structure)."""
        # Mock user input to choose option 1 (save to MTF structure)
        mock_input.side_effect = ['1']
        
        # Mock the required components
        mock_analyzer = Mock()
        mock_loader = Mock()
        mock_processor = Mock()
        mock_mtf_creator = Mock()
        
        # Mock analysis result
        analysis_result = {
            'status': 'success',
            'folder_info': {'file_count': 2, 'size_mb': 1.5},
            'indicators': ['RSI', 'MACD'],
            'subfolders_info': {'parquet': {'file_count': 2, 'size_mb': 1.5}},
            'files_info': {
                'btcusdt_rsi_m1.parquet': {
                    'indicator': 'RSI',
                    'format': 'parquet',
                    'source': 'binance'
                }
            }
        }
        
        # Mock data filter
        mock_data_filter = Mock()
        mock_data_filter.interactive_filter_selection.return_value = (None, None, None, None)
        mock_data_filter.filter_files.return_value = [
            {
                'filename': 'btcusdt_rsi_m1.parquet',
                'indicator': 'RSI',
                'format': 'parquet',
                'source': 'binance'
            }
        ]
        mock_data_filter.get_loading_summary.return_value = "2 files ready for loading"
        
        # Mock the save_all_indicators_to_mtf method
        with patch.object(self.menu, '_save_all_indicators_to_mtf') as mock_save:
            with patch('src.interactive.data_management.data_filter.DataFilter', return_value=mock_data_filter):
                with patch.object(mock_analyzer, 'analyze_indicators_folder', return_value=analysis_result):
                    # Call the method
                    self.menu._load_indicators()
        
        # Verify that save_all_indicators_to_mtf was called
        mock_save.assert_called_once()
    
    @patch('builtins.input')
    def test_load_indicators_menu_choice_0(self, mock_input):
        """Test the indicators menu when user chooses option 0 (cancel)."""
        # Mock user input to choose option 0 (cancel)
        mock_input.side_effect = ['0']
        
        # Mock the required components
        mock_analyzer = Mock()
        mock_loader = Mock()
        mock_processor = Mock()
        mock_mtf_creator = Mock()
        
        # Mock analysis result
        analysis_result = {
            'status': 'success',
            'folder_info': {'file_count': 2, 'size_mb': 1.5},
            'indicators': ['RSI', 'MACD'],
            'subfolders_info': {'parquet': {'file_count': 2, 'size_mb': 1.5}},
            'files_info': {
                'btcusdt_rsi_m1.parquet': {
                    'indicator': 'RSI',
                    'format': 'parquet',
                    'source': 'binance'
                }
            }
        }
        
        # Mock data filter
        mock_data_filter = Mock()
        mock_data_filter.interactive_filter_selection.return_value = (None, None, None, None)
        mock_data_filter.filter_files.return_value = [
            {
                'filename': 'btcusdt_rsi_m1.parquet',
                'indicator': 'RSI',
                'format': 'parquet',
                'source': 'binance'
            }
        ]
        mock_data_filter.get_loading_summary.return_value = "2 files ready for loading"
        
        # Mock the save method to ensure it's not called
        with patch.object(self.menu, '_save_all_indicators_to_mtf') as mock_save:
            with patch('src.interactive.data_management.data_filter.DataFilter', return_value=mock_data_filter):
                with patch.object(mock_analyzer, 'analyze_indicators_folder', return_value=analysis_result):
                    # Call the method
                    self.menu._load_indicators()
        
        # Verify that save method was not called
        mock_save.assert_not_called()


if __name__ == '__main__':
    pytest.main([__file__])
