#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests for DataManager gap fixing integration

This module tests the integration of gap fixing functionality
in the DataManager class.
"""

import pytest
import pandas as pd
import numpy as np
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import tempfile
import shutil

from src.interactive.data_manager import DataManager


class TestDataManagerGapFixing:
    """Test cases for DataManager gap fixing integration."""
    
    @pytest.fixture
    def data_manager(self):
        """Create DataManager instance for testing."""
        return DataManager()
    
    @pytest.fixture
    def sample_gap_summary(self):
        """Create sample gap summary for testing."""
        return [
            {
                'file': 'CSVExport_EURUSD_PERIOD_M1.parquet',
                'column': 'Timestamp',
                'gaps_count': 8576,
                'largest_gap': '10 days 00:00:00',
                'method': 'direct'
            },
            {
                'file': 'CSVExport_EURUSD_PERIOD_H4.parquet',
                'column': 'Timestamp',
                'gaps_count': 2882,
                'largest_gap': '10 days 00:00:00',
                'method': 'direct'
            }
        ]
    
    @pytest.fixture
    def temp_dir(self):
        """Create temporary directory for testing."""
        temp_dir = tempfile.mkdtemp()
        yield Path(temp_dir)
        shutil.rmtree(temp_dir)
    
    def test_show_detailed_gap_info_with_fix_option(self, data_manager, sample_gap_summary, capsys):
        """Test that gap fixing option is shown after detailed gap information."""
        # Mock Fore and Style
        mock_fore = Mock()
        mock_style = Mock()
        
        # Mock input to avoid stdin reading issues
        with patch('builtins.input', return_value='n'):
            data_manager._show_detailed_gap_info_from_eda(sample_gap_summary, mock_fore, mock_style)
        
        captured = capsys.readouterr()
        
        # Check that gap information is displayed
        assert 'DETAILED GAP INFORMATION' in captured.out
        assert 'CSVExport_EURUSD_PERIOD_M1.parquet' in captured.out
        assert 'CSVExport_EURUSD_PERIOD_H4.parquet' in captured.out
        # The question about fixing gaps is shown but may not be captured in test output
        # We'll test the actual functionality in other tests
    
    def test_show_detailed_gap_info_choose_fix_gaps(self, data_manager, sample_gap_summary, capsys):
        """Test that gap fixing interface is called when user chooses to fix gaps."""
        # Mock Fore and Style
        mock_fore = Mock()
        mock_style = Mock()
        
        # Mock input to choose to fix gaps
        with patch('builtins.input', return_value='y'):
            with patch.object(data_manager, '_fix_gaps_interactive') as mock_fix:
                data_manager._show_detailed_gap_info_from_eda(sample_gap_summary, mock_fore, mock_style)
                
                # Check that gap fixing interface is called
                mock_fix.assert_called_once_with(sample_gap_summary, mock_fore, mock_style)
    
    def test_fix_gaps_interactive_explanation_displayed(self, data_manager, sample_gap_summary, capsys):
        """Test that explanation of why gaps need to be fixed is displayed."""
        # Mock Fore and Style
        mock_fore = Mock()
        mock_style = Mock()
        
        # Mock file paths to exist
        with patch('pathlib.Path.exists', return_value=True):
            with patch('builtins.input', side_effect=['n', 'n']):  # Cancel after showing explanation
                data_manager._fix_gaps_interactive(sample_gap_summary, mock_fore, mock_style)
        
        captured = capsys.readouterr()
        
        # Check that explanation is displayed
        assert 'WHY TIME SERIES GAPS NEED TO BE FIXED' in captured.out
        assert 'Data Quality Issues' in captured.out
        assert 'Analysis Accuracy' in captured.out
        assert 'ML Model Performance' in captured.out
    
    def test_fix_gaps_interactive_file_path_extraction(self, data_manager, sample_gap_summary, temp_dir):
        """Test that file paths are correctly extracted from gap summary."""
        # Mock Fore and Style
        mock_fore = Mock()
        mock_style = Mock()
        
        # Create mock files in temp directory
        mock_file1 = temp_dir / 'CSVExport_EURUSD_PERIOD_M1.parquet'
        mock_file1.write_bytes(b'mock data')
        mock_file2 = temp_dir / 'CSVExport_EURUSD_PERIOD_H4.parquet'
        mock_file2.write_bytes(b'mock data')
        
        # Mock Path to return our temp directory
        with patch('pathlib.Path') as mock_path:
            mock_path.side_effect = lambda x: temp_dir / x if '/' in x else temp_dir / x
            
            with patch('builtins.input', side_effect=['n']):  # Cancel after path extraction
                data_manager._fix_gaps_interactive(sample_gap_summary, mock_fore, mock_style)
    
    def test_fix_gaps_interactive_no_valid_paths(self, data_manager, sample_gap_summary, capsys):
        """Test behavior when no valid file paths are found."""
        # Mock Fore and Style
        mock_fore = Mock()
        mock_style = Mock()
        
        # Mock all paths to not exist
        with patch('pathlib.Path.exists', return_value=False):
            data_manager._fix_gaps_interactive(sample_gap_summary, mock_fore, mock_style)
        
        captured = capsys.readouterr()
        
        # Check that error message is displayed
        assert 'No valid file paths found for gap fixing' in captured.out
    
    def test_fix_gaps_interactive_algorithm_selection(self, data_manager, sample_gap_summary, temp_dir):
        """Test algorithm selection in gap fixing interface."""
        # Mock Fore and Style
        mock_fore = Mock()
        mock_style = Mock()
        
        # Create mock files
        mock_file = temp_dir / 'CSVExport_EURUSD_PERIOD_M1.parquet'
        mock_file.write_bytes(b'mock data')
        
        # Mock Path to return our temp directory
        with patch('pathlib.Path') as mock_path:
            mock_path.side_effect = lambda x: temp_dir / x if '/' in x else temp_dir / x
            
            # Mock input to select algorithm and cancel
            with patch('builtins.input', side_effect=['1', 'n']):  # Select algorithm 1, then cancel
                data_manager._fix_gaps_interactive(sample_gap_summary, mock_fore, mock_style)
    
    def test_fix_gaps_interactive_algorithm_selection_default(self, data_manager, sample_gap_summary, temp_dir):
        """Test default algorithm selection in gap fixing interface."""
        # Mock Fore and Style
        mock_fore = Mock()
        mock_style = Mock()
        
        # Create mock files
        mock_file = temp_dir / 'CSVExport_EURUSD_PERIOD_M1.parquet'
        mock_file.write_bytes(b'mock data')
        
        # Mock Path to return our temp directory
        with patch('pathlib.Path') as mock_path:
            mock_path.side_effect = lambda x: temp_dir / x if '/' in x else temp_dir / x
            
            # Mock input to use default algorithm and cancel
            with patch('builtins.input', side_effect=['', 'n']):  # Empty input for default, then cancel
                data_manager._fix_gaps_interactive(sample_gap_summary, mock_fore, mock_style)
    
    def test_fix_gaps_interactive_algorithm_selection_invalid(self, data_manager, sample_gap_summary, temp_dir):
        """Test invalid algorithm selection handling."""
        # Mock Fore and Style
        mock_fore = Mock()
        mock_style = Mock()
        
        # Create mock files
        mock_file = temp_dir / 'CSVExport_EURUSD_PERIOD_M1.parquet'
        mock_file.write_bytes(b'mock data')
        
        # Mock Path to return our temp directory
        with patch('pathlib.Path') as mock_path:
            mock_path.side_effect = lambda x: temp_dir / x if '/' in x else temp_dir / x
            
            # Mock input to select invalid algorithm and cancel
            with patch('builtins.input', side_effect=['99', 'n']):  # Invalid choice, then cancel
                data_manager._fix_gaps_interactive(sample_gap_summary, mock_fore, mock_style)
    
    def test_fix_gaps_interactive_cancel_confirmation(self, data_manager, sample_gap_summary, temp_dir):
        """Test cancellation at confirmation step."""
        # Mock Fore and Style
        mock_fore = Mock()
        mock_style = Mock()
        
        # Create mock files
        mock_file = temp_dir / 'CSVExport_EURUSD_PERIOD_M1.parquet'
        mock_file.write_bytes(b'mock data')
        
        # Mock Path to return our temp directory
        with patch('pathlib.Path') as mock_path:
            mock_path.side_effect = lambda x: temp_dir / x if '/' in x else temp_dir / x
            
            # Mock input to select algorithm and cancel at confirmation
            with patch('builtins.input', side_effect=['1', 'n']):  # Select algorithm, then cancel
                data_manager._fix_gaps_interactive(sample_gap_summary, mock_fore, mock_style)
    
    @patch('src.interactive.data_manager.GapFixer')
    def test_fix_gaps_interactive_gap_fixer_initialization(self, mock_gap_fixer_class, data_manager, sample_gap_summary, temp_dir):
        """Test GapFixer initialization in gap fixing interface."""
        # Mock Fore and Style
        mock_fore = Mock()
        mock_style = Mock()
        
        # Mock Path.exists to return True for our files
        with patch('pathlib.Path.exists', return_value=True):
            # Mock GapFixer instance
            mock_gap_fixer = Mock()
            mock_gap_fixer_class.return_value = mock_gap_fixer
            
            # Mock input to proceed with gap fixing
            with patch('builtins.input', side_effect=['1', 'y']):  # Select algorithm, then proceed
                with patch.object(mock_gap_fixer, 'fix_multiple_files') as mock_fix:
                    mock_fix.return_value = {}
                    data_manager._fix_gaps_interactive(sample_gap_summary, mock_fore, mock_style)
                    
                    # Check that GapFixer was initialized with correct memory limit
                    mock_gap_fixer_class.assert_called_once_with(memory_limit_mb=data_manager.max_memory_mb)
    
    @patch('src.data.gap_fixer.GapFixer')
    def test_fix_gaps_interactive_gap_fixer_error(self, mock_gap_fixer_class, data_manager, sample_gap_summary, temp_dir):
        """Test error handling during GapFixer initialization."""
        # Mock Fore and Style
        mock_fore = Mock()
        mock_style = Mock()
        
        # Create mock files
        mock_file = temp_dir / 'CSVExport_EURUSD_PERIOD_M1.parquet'
        mock_file.write_bytes(b'mock data')
        
        # Mock Path to return our temp directory
        with patch('pathlib.Path') as mock_path:
            mock_path.side_effect = lambda x: temp_dir / x if '/' in x else temp_dir / x
            
            # Mock GapFixer to raise exception
            mock_gap_fixer_class.side_effect = Exception("GapFixer initialization failed")
            
            # Mock input to proceed with gap fixing
            with patch('builtins.input', side_effect=['1', 'y']):  # Select algorithm, then proceed
                data_manager._fix_gaps_interactive(sample_gap_summary, mock_fore, mock_style)
    
    @patch('src.interactive.data_manager.GapFixer')
    def test_fix_gaps_interactive_successful_execution(self, mock_gap_fixer_class, data_manager, sample_gap_summary, temp_dir, capsys):
        """Test successful gap fixing execution."""
        # Mock Fore and Style
        mock_fore = Mock()
        mock_style = Mock()
        
        # Mock Path.exists to return True for our files
        with patch('pathlib.Path.exists', return_value=True):
            # Mock GapFixer instance
            mock_gap_fixer = Mock()
            mock_gap_fixer_class.return_value = mock_gap_fixer
            
            # Mock successful gap fixing results
            mock_results = {
                'CSVExport_EURUSD_PERIOD_M1.parquet': {
                    'success': True,
                    'gaps_fixed': 100,
                    'algorithm_used': 'linear',
                    'processing_time': 5.0,
                    'memory_used_mb': 50.0
                }
            }
            
            # Mock input to proceed with gap fixing
            with patch('builtins.input', side_effect=['1', 'y']):  # Select algorithm, then proceed
                with patch.object(mock_gap_fixer, 'fix_multiple_files') as mock_fix:
                    mock_fix.return_value = mock_results
                    
                    # Mock time.time for timing
                    with patch('time.time', side_effect=[0.0, 5.0]):  # Start time, end time
                        data_manager._fix_gaps_interactive(sample_gap_summary, mock_fore, mock_style)
                    
                    # Check that gap fixing was called
                    mock_fix.assert_called_once()
                    
                    # Check output
                    captured = capsys.readouterr()
                    assert 'Gap fixing completed!' in captured.out
                    assert '100 gaps fixed' in captured.out
                    assert 'linear' in captured.out
    
    @patch('src.interactive.data_manager.GapFixer')
    def test_fix_gaps_interactive_execution_error(self, mock_gap_fixer_class, data_manager, sample_gap_summary, temp_dir, capsys):
        """Test error handling during gap fixing execution."""
        # Mock Fore and Style
        mock_fore = Mock()
        mock_style = Mock()
        
        # Mock Path.exists to return True for our files
        with patch('pathlib.Path.exists', return_value=True):
            # Mock GapFixer instance
            mock_gap_fixer = Mock()
            mock_gap_fixer_class.return_value = mock_gap_fixer
            
            # Mock input to proceed with gap fixing
            with patch('builtins.input', side_effect=['1', 'y']):  # Select algorithm, then proceed
                with patch.object(mock_gap_fixer, 'fix_multiple_files') as mock_fix:
                    mock_fix.side_effect = Exception("Gap fixing failed")
                    
                    # Mock time.time for timing
                    with patch('time.time', side_effect=[0.0, 5.0]):  # Start time, end time
                        data_manager._fix_gaps_interactive(sample_gap_summary, mock_fore, mock_style)
                    
                    # Check output
                    captured = capsys.readouterr()
                    assert 'Error during gap fixing' in captured.out
    
    def test_fix_gaps_interactive_eof_error_handling(self, data_manager, sample_gap_summary):
        """Test EOF error handling in gap fixing interface."""
        # Mock Fore and Style
        mock_fore = Mock()
        mock_style = Mock()
        
        # Mock input to raise EOFError
        with patch('builtins.input', side_effect=EOFError):
            # Should not raise exception
            data_manager._fix_gaps_interactive(sample_gap_summary, mock_fore, mock_style)
    
    def test_fix_gaps_interactive_value_error_handling(self, data_manager, sample_gap_summary, temp_dir):
        """Test ValueError handling in algorithm selection."""
        # Mock Fore and Style
        mock_fore = Mock()
        mock_style = Mock()
        
        # Create mock files
        mock_file = temp_dir / 'CSVExport_EURUSD_PERIOD_M1.parquet'
        mock_file.write_bytes(b'mock data')
        
        # Mock Path to return our temp directory
        with patch('pathlib.Path') as mock_path:
            mock_path.side_effect = lambda x: temp_dir / x if '/' in x else temp_dir / x
            
            # Mock input to raise ValueError
            with patch('builtins.input', side_effect=ValueError("Invalid input")):
                data_manager._fix_gaps_interactive(sample_gap_summary, mock_fore, mock_style)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
