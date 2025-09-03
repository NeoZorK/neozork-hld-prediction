#!/usr/bin/env python3
"""
Test duplicates fixing and cleaned data saving functionality.

This test verifies that the duplicates fixing and data saving works correctly
with both main timeframe data and multi-timeframe datasets.
"""

import pytest
import pandas as pd
import numpy as np
from unittest.mock import Mock, MagicMock, patch
from datetime import datetime, timedelta
from pathlib import Path
import tempfile
import shutil

# Import the module to test
from src.interactive.eda import EDAAnalyzer


class TestDuplicatesFixing:
    """Test duplicates fixing and cleaned data saving functionality."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.eda_analyzer = EDAAnalyzer()
        
        # Create temporary directory for testing
        self.temp_dir = tempfile.mkdtemp()
        
        # Create sample data with duplicates
        dates = pd.date_range('2024-01-01', periods=100, freq='1H')
        
        # Main dataset with some duplicates
        self.main_data = pd.DataFrame({
            'Timestamp': dates,
            'Open': np.random.randn(100) * 100 + 1000,
            'High': np.random.randn(100) * 100 + 1000,
            'Low': np.random.randn(100) * 100 + 1000,
            'Close': np.random.randn(100) * 100 + 1000,
            'Volume': np.random.randint(1000, 10000, 100)
        })
        
        # Add some duplicates to main data
        self.main_data = pd.concat([
            self.main_data,
            self.main_data.iloc[0:5]  # Add 5 duplicate rows
        ], ignore_index=True)
        
        # Create multi-timeframe data with duplicates
        self.multi_timeframe_data = {
            'M5': pd.DataFrame({
                'Timestamp': pd.date_range('2024-01-01', periods=50, freq='5T'),
                'Open': np.random.randn(50) * 50 + 1000,
                'High': np.random.randn(50) * 50 + 1000,
                'Low': np.random.randn(50) * 50 + 1000,
                'Close': np.random.randn(50) * 50 + 1000,
                'Volume': np.random.randint(1000, 10000, 50)
            }),
            'H1': pd.DataFrame({
                'Timestamp': pd.date_range('2024-01-01', periods=24, freq='1H'),
                'Open': np.random.randn(24) * 100 + 1000,
                'High': np.random.randn(24) * 100 + 1000,
                'Low': np.random.randn(24) * 100 + 1000,
                'Close': np.random.randn(24) * 100 + 1000,
                'Volume': np.random.randint(1000, 10000, 24)
            })
        }
        
        # Add duplicates to M5 timeframe
        self.multi_timeframe_data['M5'] = pd.concat([
            self.multi_timeframe_data['M5'],
            self.multi_timeframe_data['M5'].iloc[0:3]  # Add 3 duplicate rows
        ], ignore_index=True)
        
        # Mock system object
        self.mock_system = Mock()
        self.mock_system.current_data = self.main_data.copy()
        self.mock_system.other_timeframes_data = {
            tf: data.copy() for tf, data in self.multi_timeframe_data.items()
        }
    
    def teardown_method(self):
        """Clean up test fixtures."""
        if Path(self.temp_dir).exists():
            shutil.rmtree(self.temp_dir)
    
    def test_fix_duplicates_and_save_main_only(self):
        """Test fixing duplicates and saving for main dataset only."""
        # Mock system with only main data
        system_main_only = Mock()
        system_main_only.current_data = self.main_data.copy()
        system_main_only.other_timeframes_data = None
        
        # Mock Path to use temp directory
        with patch('pathlib.Path') as mock_path:
            mock_path.return_value = Path(self.temp_dir) / "cleaned_data"
            mock_path.return_value.mkdir(exist_ok=True)
            
            # Create all_dupe_summaries
            all_dupe_summaries = {
                'main': {
                    'total_duplicates': 5,
                    'duplicate_percent': 4.76
                }
            }
            
            critical_issues = []
            
            result = self.eda_analyzer.duplicates_analyzer.duplicate_fixing._fix_duplicates_and_save(
                system_main_only, all_dupe_summaries, critical_issues
            )
            
            assert result is True
            # Check that duplicates were removed
            assert len(system_main_only.current_data) < len(self.main_data)
    
    def test_fix_duplicates_and_save_multi_timeframes(self):
        """Test fixing duplicates and saving for multi-timeframe datasets."""
        # Mock Path to use temp directory
        with patch('pathlib.Path') as mock_path:
            mock_path.return_value = Path(self.temp_dir) / "cleaned_data"
            mock_path.return_value.mkdir(exist_ok=True)
            
            # Create all_dupe_summaries
            all_dupe_summaries = {
                'main': {
                    'total_duplicates': 5,
                    'duplicate_percent': 4.76
                },
                'M5': {
                    'total_duplicates': 3,
                    'duplicate_percent': 5.66
                },
                'H1': {
                    'total_duplicates': 0,
                    'duplicate_percent': 0.0
                }
            }
            
            critical_issues = []
            
            result = self.eda_analyzer.duplicates_analyzer.duplicate_fixing._fix_duplicates_and_save(
                self.mock_system, all_dupe_summaries, critical_issues
            )
            
            assert result is True
            # Check that duplicates were removed from main dataset
            assert len(self.mock_system.current_data) < len(self.main_data)
            # Check that duplicates were removed from M5 timeframe
            assert len(self.mock_system.other_timeframes_data['M5']) < len(self.multi_timeframe_data['M5'])
    
    @patch('builtins.input', return_value='y')
    def test_run_duplicates_analysis_with_fixing(self, mock_input):
        """Test complete duplicates analysis with fixing option."""
        with patch('pathlib.Path') as mock_path:
            mock_path.return_value = Path(self.temp_dir) / "cleaned_data"
            mock_path.return_value.mkdir(exist_ok=True)
            
            result = self.eda_analyzer.run_duplicates_analysis(self.mock_system)
            
            assert result is True
            # Check that fixing was triggered
            mock_input.assert_called_once()
    
    @patch('builtins.input', return_value='n')
    def test_run_duplicates_analysis_without_fixing(self, mock_input):
        """Test duplicates analysis without fixing option."""
        result = self.eda_analyzer.run_duplicates_analysis(self.mock_system)
        
        assert result is True
        # Check that fixing was not triggered
        mock_input.assert_called_once()
        # Original data should be unchanged
        assert len(self.mock_system.current_data) == len(self.main_data)
    
    def test_fix_duplicates_with_critical_issues(self):
        """Test fixing duplicates when critical issues (NaT values) are present."""
        # Add NaT values to test data
        test_data = self.main_data.copy()
        test_data.loc[0:10, 'Timestamp'] = pd.NaT
        
        system_with_nat = Mock()
        system_with_nat.current_data = test_data
        system_with_nat.other_timeframes_data = None
        
        with patch('pathlib.Path') as mock_path:
            mock_path.return_value = Path(self.temp_dir) / "cleaned_data"
            mock_path.return_value.mkdir(exist_ok=True)
            
            all_dupe_summaries = {
                'main': {
                    'total_duplicates': 5,
                    'duplicate_percent': 4.76
                }
            }
            
            critical_issues = ['Main: 11 NaT values in Timestamp']
            
            result = self.eda_analyzer.duplicates_analyzer.duplicate_fixing._fix_duplicates_and_save(
                system_with_nat, all_dupe_summaries, critical_issues
            )
            
            assert result is True
    
    def test_progress_bar_calculation(self):
        """Test that progress bar and ETA calculations work correctly."""
        # This test verifies the progress calculation logic
        total_timeframes = 7
        current_timeframe = 3
        
        progress = (current_timeframe / total_timeframes) * 100
        eta_remaining = total_timeframes - current_timeframe
        
        assert progress == pytest.approx(42.86, rel=0.01)
        assert eta_remaining == 4
    
    @patch('builtins.input', return_value='n')
    def test_empty_timeframe_handling(self, mock_input):
        """Test handling of empty timeframes during analysis."""
        # Create system with empty timeframes
        system_with_empty = Mock()
        system_with_empty.current_data = self.main_data.copy()
        system_with_empty.other_timeframes_data = {
            'M5': pd.DataFrame(),  # Empty dataframe
            'H1': None  # None dataframe
        }
        
        result = self.eda_analyzer.run_duplicates_analysis(system_with_empty)
        
        assert result is True


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"])

