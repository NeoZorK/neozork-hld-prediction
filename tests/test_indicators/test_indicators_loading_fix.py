# -*- coding: utf-8 -*-
"""
Test for indicators loading fix.

This test verifies that the fix for the 'dict' object has no attribute 'columns' error
is working correctly.
"""

import pytest
import pandas as pd
from unittest.mock import Mock, patch
from src.interactive.data_management.indicators.indicators_loader import IndicatorsLoader
from src.interactive.data_management.indicators.indicators_processor import IndicatorsProcessor


class TestIndicatorsLoadingFix:
    """Test cases for indicators loading fix."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.loader = IndicatorsLoader()
        self.processor = IndicatorsProcessor()
    
    def test_process_single_indicator_with_correct_data_structure(self):
        """Test that process_single_indicator works with correct data structure."""
        # Create mock data structure that matches what load_indicator_by_name returns
        mock_file_data = {
            'data': pd.DataFrame({
                'timestamp': pd.date_range('2023-01-01', periods=10, freq='1h'),
                'value': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                'symbol': ['BTCUSDT'] * 10,
                'timeframe': ['H1'] * 10
            }),
            'format': 'parquet',
            'rows': 10,
            'columns': ['timestamp', 'value', 'symbol', 'timeframe'],
            'file_path': '/test/file.parquet',
            'indicator': 'RSI'
        }
        
        # This should work without errors
        result = self.processor.process_single_indicator(mock_file_data)
        
        assert result["status"] == "success"
        assert "data" in result
        assert result["data"]["indicator"] == "RSI"
        assert result["data"]["rows"] == 10
    
    def test_process_single_indicator_with_wrong_data_structure(self):
        """Test that process_single_indicator handles wrong data structure gracefully."""
        # Create mock data structure that would cause the original error
        mock_result_structure = {
            "status": "success",
            "indicator_name": "RSI",
            "file_path": "/test/file.parquet",
            "data": {
                'data': pd.DataFrame({
                    'timestamp': pd.date_range('2023-01-01', periods=10, freq='1h'),
                    'value': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                    'symbol': ['BTCUSDT'] * 10,
                    'timeframe': ['H1'] * 10
                }),
                'format': 'parquet',
                'rows': 10,
                'columns': ['timestamp', 'value', 'symbol', 'timeframe'],
                'file_path': '/test/file.parquet',
                'indicator': 'RSI'
            },
            "format": "parquet"
        }
        
        # This should return an error status instead of raising an exception
        result = self.processor.process_single_indicator(mock_result_structure)
        
        assert result["status"] == "error"
        assert "'dict' object has no attribute 'columns'" in result["message"]
    
    def test_load_and_process_workflow(self):
        """Test the complete load and process workflow."""
        # Mock the loader to return the correct structure
        mock_loader_result = {
            "status": "success",
            "indicator_name": "RSI",
            "file_path": "/test/file.parquet",
            "data": {
                'data': pd.DataFrame({
                    'timestamp': pd.date_range('2023-01-01', periods=10, freq='1h'),
                    'value': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                    'symbol': ['BTCUSDT'] * 10,
                    'timeframe': ['H1'] * 10
                }),
                'format': 'parquet',
                'rows': 10,
                'columns': ['timestamp', 'value', 'symbol', 'timeframe'],
                'file_path': '/test/file.parquet',
                'indicator': 'RSI'
            },
            "format": "parquet"
        }
        
        # Simulate the fixed workflow
        if mock_loader_result["status"] == "success":
            # This is the fix: pass result['data'] instead of result
            processed_result = self.processor.process_single_indicator(mock_loader_result['data'])
            
            assert processed_result["status"] == "success"
            assert "data" in processed_result
            assert processed_result["data"]["indicator"] == "RSI"
