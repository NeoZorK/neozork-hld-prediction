#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests for enhanced Time Series Gaps Analysis functionality.

This module tests the updated run_time_series_gaps_analysis method
that analyzes multiple timeframe files.
"""

import pytest
import pandas as pd
import numpy as np
from pathlib import Path
import tempfile
import os
from unittest.mock import patch, MagicMock

from src.interactive.eda import EDAAnalyzer


class TestEDAAnalyzerGaps:
    """Test enhanced Time Series Gaps Analysis functionality."""
    
    def setup_method(self):
        """Set up test environment."""
        self.eda_analyzer = EDAAnalyzer()
        
        # Create test data with timestamps
        dates = pd.date_range('2023-01-01', periods=100, freq='H')
        self.test_data = pd.DataFrame({
            'timestamp': dates,
            'Open': np.random.uniform(100, 110, 100),
            'High': np.random.uniform(110, 120, 100),
            'Low': np.random.uniform(90, 100, 100),
            'Close': np.random.uniform(100, 110, 100),
            'Volume': np.random.randint(1000, 10000, 100)
        })
        
        # Create gaps in timestamps
        self.test_data_with_gaps = self.test_data.copy()
        # Remove some rows to create gaps
        self.test_data_with_gaps = self.test_data_with_gaps.drop([10, 20, 30, 40, 50])
    
    def test_load_file_for_gap_analysis_csv(self):
        """Test loading CSV file for gap analysis."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            # Write test data to CSV
            self.test_data.to_csv(f.name, index=False)
            temp_path = Path(f.name)
        
        try:
            # Test loading
            df = self.eda_analyzer.time_series_analyzer.gaps_analyzer._load_file_for_gap_analysis(temp_path)
            
            assert df is not None
            assert len(df) > 0
            assert 'timestamp' in df.columns
            assert len(df.columns) == 6  # timestamp + OHLCV
            
        finally:
            # Cleanup
            os.unlink(temp_path)
    
    def test_load_file_for_gap_analysis_parquet(self):
        """Test loading parquet file for gap analysis."""
        with tempfile.NamedTemporaryFile(suffix='.parquet', delete=False) as f:
            # Write test data to parquet
            self.test_data.to_parquet(f.name, index=False)
            temp_path = Path(f.name)
        
        try:
            # Test loading
            df = self.eda_analyzer.time_series_analyzer.gaps_analyzer._load_file_for_gap_analysis(temp_path)
            
            assert df is not None
            assert len(df) > 0
            assert 'timestamp' in df.columns
            assert len(df.columns) == 6  # timestamp + OHLCV
            
        finally:
            # Cleanup
            os.unlink(temp_path)
    
    def test_load_file_for_gap_analysis_no_timestamp(self):
        """Test loading file without timestamp columns."""
        # Create data without timestamp
        data_no_ts = pd.DataFrame({
            'Open': np.random.uniform(100, 110, 100),
            'High': np.random.uniform(110, 120, 100),
            'Low': np.random.uniform(90, 100, 100),
            'Close': np.random.uniform(100, 110, 100)
        })
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            data_no_ts.to_csv(f.name, index=False)
            temp_path = Path(f.name)
        
        try:
            # Test loading
            df = self.eda_analyzer.time_series_analyzer.gaps_analyzer._load_file_for_gap_analysis(temp_path)
            
            assert df is None  # Should return None for files without timestamp
            
        finally:
            # Cleanup
            os.unlink(temp_path)
    
    def test_analyze_time_series_gaps_with_gaps(self):
        """Test gap analysis on data with gaps."""
        gap_summary = self.eda_analyzer.time_series_analyzer.gaps_analyzer._analyze_time_series_gaps(self.test_data_with_gaps)
        
        assert len(gap_summary) > 0
        assert gap_summary[0]['column'] == 'timestamp'
        assert gap_summary[0]['gap_count'] > 0
    
    def test_analyze_time_series_gaps_no_gaps(self):
        """Test gap analysis on data without gaps."""
        gap_summary = self.eda_analyzer.time_series_analyzer.gaps_analyzer._analyze_time_series_gaps(self.test_data)
        
        # Should find no gaps in regular hourly data
        assert len(gap_summary) > 0  # Returns info about timestamp columns
        assert gap_summary[0]['gap_count'] == 0  # But no actual gaps
    
    def test_run_time_series_gaps_analysis_mock_files(self):
        """Test the main gaps analysis method with preloaded data."""
        mock_system = MagicMock()
        
        # Mock current_data
        mock_system.current_data = self.test_data_with_gaps
        
        # Mock other_timeframes_data with actual DataFrames
        mock_system.other_timeframes_data = {
            'M5': self.test_data_with_gaps,
            'H1': self.test_data_with_gaps
        }
        
        # Mock timeframe_info
        mock_system.timeframe_info = {
            'cross_timeframes': {
                'M5': ['loaded_M5_dataframe'],
                'H1': ['loaded_H1_dataframe']
            }
        }
        
        # Mock the time_series_analyzer to return True
        mock_system.time_series_analyzer.run_time_series_gaps_analysis.return_value = True
        
        # Run analysis
        result = self.eda_analyzer.run_time_series_gaps_analysis(mock_system)
        
        assert result is True
    
    def test_run_time_series_gaps_analysis_no_data_loaded(self):
        """Test gaps analysis when no data is loaded."""
        mock_system = MagicMock()
        mock_system.current_data = None
        
        # Mock the time_series_analyzer to return False
        mock_system.time_series_analyzer.run_time_series_gaps_analysis.return_value = False
        
        result = self.eda_analyzer.run_time_series_gaps_analysis(mock_system)
        
        assert result is False
    
    def test_run_time_series_gaps_analysis_no_timeframe_info(self):
        """Test gaps analysis when no timeframe info is available."""
        mock_system = MagicMock()
        mock_system.current_data = self.test_data_with_gaps
        mock_system.timeframe_info = None
        
        # Mock the time_series_analyzer to return True
        mock_system.time_series_analyzer.run_time_series_gaps_analysis.return_value = True
        
        # Run analysis
        result = self.eda_analyzer.run_time_series_gaps_analysis(mock_system)
        
        assert result is True
    
    def test_run_time_series_gaps_analysis_empty_timeframe_info(self):
        """Test gaps analysis when timeframe info is empty."""
        mock_system = MagicMock()
        mock_system.current_data = self.test_data_with_gaps
        mock_system.timeframe_info = {'cross_timeframes': {}}
        
        # Mock the time_series_analyzer to return True
        mock_system.time_series_analyzer.run_time_series_gaps_analysis.return_value = True
        
        # Run analysis
        result = self.eda_analyzer.run_time_series_gaps_analysis(mock_system)
        
        assert result is True
    
    def test_run_time_series_gaps_analysis_with_cross_timeframes(self):
        """Test gaps analysis with cross-timeframe data."""
        mock_system = MagicMock()
        mock_system.current_data = self.test_data_with_gaps
        
        # Mock other_timeframes_data with actual DataFrames
        mock_system.other_timeframes_data = {
            'M5': self.test_data_with_gaps,
            'H1': self.test_data_with_gaps
        }
        
        # Mock timeframe_info with cross-timeframes
        mock_system.timeframe_info = {
            'cross_timeframes': {
                'M5': ['loaded_M5_dataframe'],
                'H1': ['loaded_H1_dataframe']
            }
        }
        
        # Mock the time_series_analyzer to return True
        mock_system.time_series_analyzer.run_time_series_gaps_analysis.return_value = True
        
        # Run analysis
        result = self.eda_analyzer.run_time_series_gaps_analysis(mock_system)
        
        assert result is True
    
    def test_run_time_series_gaps_analysis_no_other_timeframes_data(self):
        """Test gaps analysis when other_timeframes_data is not available."""
        mock_system = MagicMock()
        mock_system.current_data = self.test_data_with_gaps
        
        # Mock timeframe_info with cross-timeframes but no other_timeframes_data
        mock_system.timeframe_info = {
            'cross_timeframes': {
                'M5': ['loaded_M5_dataframe'],
                'H1': ['loaded_H1_dataframe']
            }
        }
        
        # Don't set other_timeframes_data
        
        # Mock the time_series_analyzer to return True
        mock_system.time_series_analyzer.run_time_series_gaps_analysis.return_value = True
        
        # Run analysis
        result = self.eda_analyzer.run_time_series_gaps_analysis(mock_system)
        
        assert result is True
    
    def test_determine_frequency_from_timedelta(self):
        """Test frequency determination from timedelta."""
        # Test different time intervals
        test_cases = [
            (pd.Timedelta(minutes=30), '30T'),
            (pd.Timedelta(hours=1), '1H'),
            (pd.Timedelta(hours=4), '4H'),
            (pd.Timedelta(days=1), '1D'),
            (pd.Timedelta(weeks=1), '1W'),
            (pd.Timedelta(days=30), '1M'),
            (pd.Timedelta(days=365), '1Y')
        ]
    
        for td, expected in test_cases:
            result = self.eda_analyzer.time_series_analyzer.gaps_analyzer._determine_frequency_from_timedelta(td)
            assert result == expected, f"Expected {expected} for {td}, got {result}"
