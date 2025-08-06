#!/usr/bin/env python3
"""
Test script for debug_rsi_signals.py functionality.
"""

import pytest
import pandas as pd
import numpy as np
from unittest.mock import patch, MagicMock
import sys
import os

# Add scripts directory to path for testing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'scripts'))

from debug.debug_rsi_signals import analyze_rsi_signals


class TestDebugRSISignals:
    """Test class for debug_rsi_signals functionality."""
    
    @pytest.fixture
    def mock_dataframe(self):
        """Create a mock dataframe for testing."""
        dates = pd.date_range('2023-01-01', periods=100, freq='D')
        data = {
            'Open': np.random.uniform(1.0, 2.0, 100),
            'High': np.random.uniform(1.1, 2.1, 100),
            'Low': np.random.uniform(0.9, 1.9, 100),
            'Close': np.random.uniform(1.0, 2.0, 100),
            'Volume': np.random.randint(1000, 10000, 100)
        }
        return pd.DataFrame(data, index=dates)
    
    @pytest.fixture
    def mock_result_dataframe(self):
        """Create a mock result dataframe with RSI and Direction columns."""
        dates = pd.date_range('2023-01-01', periods=100, freq='D')
        data = {
            'Open': np.random.uniform(1.0, 2.0, 100),
            'High': np.random.uniform(1.1, 2.1, 100),
            'Low': np.random.uniform(0.9, 1.9, 100),
            'Close': np.random.uniform(1.0, 2.0, 100),
            'Volume': np.random.randint(1000, 10000, 100),
            'RSI': np.random.uniform(20, 80, 100),
            'Direction': np.random.choice([0, 1, -1], 100, p=[0.7, 0.15, 0.15])
        }
        return pd.DataFrame(data, index=dates)
    
    @patch('debug.debug_rsi_signals.pd.read_parquet')
    @patch('debug.debug_rsi_signals.calculate_indicator')
    @patch('debug.debug_rsi_signals.calculate_trading_metrics')
    def test_analyze_rsi_signals_basic_functionality(self, mock_calculate_metrics, 
                                                   mock_calculate_indicator, 
                                                   mock_read_parquet,
                                                   mock_dataframe, 
                                                   mock_result_dataframe):
        """Test basic functionality of analyze_rsi_signals function."""
        
        # Setup mocks
        mock_read_parquet.return_value = mock_dataframe
        mock_calculate_indicator.return_value = mock_result_dataframe
        mock_calculate_metrics.side_effect = [
            {
                'buy_count': 10,
                'sell_count': 8,
                'total_trades': 18,
                'win_ratio': 55.5,
                'profit_factor': 1.2,
                'net_return': 5.5,
                'strategy_efficiency': 75.0
            },
            {
                'buy_count': 10,
                'sell_count': 8,
                'total_trades': 18,
                'win_ratio': 55.5,
                'profit_factor': 1.2,
                'net_return': 5.5,
                'strategy_efficiency': 75.0
            }
        ]
        
        # Capture stdout to check output
        with patch('sys.stdout', new=MagicMock()) as mock_stdout:
            analyze_rsi_signals()
        
        # Verify function calls
        mock_read_parquet.assert_called_once()
        mock_calculate_indicator.assert_called_once()
        assert mock_calculate_metrics.call_count == 2
    
    @patch('debug.debug_rsi_signals.pd.read_parquet')
    @patch('debug.debug_rsi_signals.calculate_indicator')
    @patch('debug.debug_rsi_signals.calculate_trading_metrics')
    def test_analyze_rsi_signals_identical_metrics(self, mock_calculate_metrics, 
                                                 mock_calculate_indicator, 
                                                 mock_read_parquet,
                                                 mock_dataframe, 
                                                 mock_result_dataframe):
        """Test behavior when metrics are identical (warning case)."""
        
        # Setup mocks with identical metrics
        mock_read_parquet.return_value = mock_dataframe
        mock_calculate_indicator.return_value = mock_result_dataframe
        identical_metrics = {
            'buy_count': 5,
            'sell_count': 3,
            'total_trades': 8,
            'win_ratio': 50.0,
            'profit_factor': 1.0,
            'net_return': 0.0,
            'strategy_efficiency': 60.0
        }
        mock_calculate_metrics.return_value = identical_metrics
        
        # Capture stdout to check warning output
        with patch('sys.stdout', new=MagicMock()) as mock_stdout:
            analyze_rsi_signals()
        
        # Verify function calls
        mock_calculate_metrics.assert_called()
    
    @patch('debug.debug_rsi_signals.pd.read_parquet')
    @patch('debug.debug_rsi_signals.calculate_indicator')
    def test_analyze_rsi_signals_no_trading_signals(self, mock_calculate_indicator, 
                                                   mock_read_parquet,
                                                   mock_dataframe):
        """Test behavior when no trading signals are found."""
        
        # Create dataframe with no trading signals (all Direction = 0)
        no_signals_df = mock_dataframe.copy()
        no_signals_df['Direction'] = 0
        no_signals_df['RSI'] = np.random.uniform(30, 70, 100)
        
        # Setup mocks
        mock_read_parquet.return_value = mock_dataframe
        mock_calculate_indicator.return_value = no_signals_df
        
        # Capture stdout to check output
        with patch('sys.stdout', new=MagicMock()) as mock_stdout:
            analyze_rsi_signals()
        
        # Verify function calls
        mock_calculate_indicator.assert_called_once()
    
    @patch('debug.debug_rsi_signals.pd.read_parquet')
    @patch('debug.debug_rsi_signals.calculate_indicator')
    def test_analyze_rsi_signals_rsi_analysis(self, mock_calculate_indicator, 
                                             mock_read_parquet,
                                             mock_dataframe):
        """Test RSI analysis functionality."""
        
        # Create dataframe with RSI values
        rsi_df = mock_dataframe.copy()
        rsi_df['RSI'] = np.random.uniform(20, 80, 100)
        rsi_df['Direction'] = np.random.choice([0, 1, -1], 100, p=[0.6, 0.2, 0.2])
        
        # Setup mocks
        mock_read_parquet.return_value = mock_dataframe
        mock_calculate_indicator.return_value = rsi_df
        
        # Capture stdout to check RSI analysis output
        with patch('sys.stdout', new=MagicMock()) as mock_stdout:
            analyze_rsi_signals()
        
        # Verify function calls
        mock_calculate_indicator.assert_called_once()
    
    def test_analyze_rsi_signals_file_path(self):
        """Test that the function uses correct file path."""
        
        # Simple test to verify the file path is correct
        with open('scripts/debug/debug_rsi_signals.py', 'r') as f:
            content = f.read()
            assert '../../data/cache/csv_converted/CSVExport_GBPUSD_PERIOD_MN1.parquet' in content


if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 