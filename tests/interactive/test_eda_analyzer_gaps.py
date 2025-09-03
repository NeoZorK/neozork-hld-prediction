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

from src.interactive.eda_analyzer import EDAAnalyzer


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
            df = self.eda_analyzer._load_file_for_gap_analysis(temp_path)
            
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
            df = self.eda_analyzer._load_file_for_gap_analysis(temp_path)
            
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
            df = self.eda_analyzer._load_file_for_gap_analysis(temp_path)
            
            assert df is None  # Should return None for files without timestamp
            
        finally:
            # Cleanup
            os.unlink(temp_path)
    
    def test_analyze_time_series_gaps_with_gaps(self):
        """Test gap analysis on data with gaps."""
        gap_summary = self.eda_analyzer._analyze_time_series_gaps(self.test_data_with_gaps)
        
        assert len(gap_summary) > 0
        assert gap_summary[0]['column'] == 'timestamp'
        assert gap_summary[0]['gap_count'] > 0
    
    def test_analyze_time_series_gaps_no_gaps(self):
        """Test gap analysis on data without gaps."""
        gap_summary = self.eda_analyzer._analyze_time_series_gaps(self.test_data)
        
        # Should find no gaps in regular hourly data
        assert len(gap_summary) == 0
    
    def test_run_time_series_gaps_analysis_mock_files(self):
        """Test the main gaps analysis method with mocked file system."""
        mock_system = MagicMock()
        
        # Mock Path.glob to return test files
        with patch('pathlib.Path.glob') as mock_glob, \
             patch('pathlib.Path.exists', return_value=True):
            
            # Mock file paths - only non-backup files
            mock_files = [
                Path('data/test1.csv'),
                Path('data/test2.parquet')
            ]
            # Mock both direct glob and recursive glob calls (4 total calls)
            mock_glob.side_effect = [mock_files, mock_files, mock_files, mock_files]
            
            # Mock file loading
            with patch.object(self.eda_analyzer, '_load_file_for_gap_analysis') as mock_load:
                mock_load.return_value = self.test_data_with_gaps
                
                # Run analysis
                result = self.eda_analyzer.run_time_series_gaps_analysis(mock_system)
                
                assert result is True
                # Should call load for each file (2 files * 4 glob calls = 8 total calls)
                assert mock_load.call_count == 8
    
    def test_run_time_series_gaps_analysis_no_data_dir(self):
        """Test gaps analysis when data directory doesn't exist."""
        mock_system = MagicMock()
        
        with patch('pathlib.Path.exists', return_value=False):
            result = self.eda_analyzer.run_time_series_gaps_analysis(mock_system)
            
            assert result is False
    
    def test_run_time_series_gaps_analysis_no_files(self):
        """Test gaps analysis when no data files are found."""
        mock_system = MagicMock()
        
        with patch('pathlib.Path.exists', return_value=True), \
             patch('pathlib.Path.glob', return_value=[]):
            
            result = self.eda_analyzer.run_time_series_gaps_analysis(mock_system)
            
            assert result is False
    
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
            result = self.eda_analyzer._determine_frequency_from_timedelta(td)
            assert result == expected, f"Expected {expected} for {td}, got {result}"
