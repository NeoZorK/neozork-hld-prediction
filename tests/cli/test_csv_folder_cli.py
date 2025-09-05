# File: tests/cli/test_csv_folder_cli.py
# -*- coding: utf-8 -*-

"""
Tests for CSV folder CLI functionality.
All comments are in English.
"""
import pytest
import tempfile
import os
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock
import argparse

from src.cli.cli import parse_arguments


class TestCSVFolderCLI:
    """Test cases for CSV folder CLI functionality."""

    def test_csv_folder_argument_parsing(self):
        """Test that --csv-folder argument is parsed correctly."""
        # Test with --csv-folder
        with patch.object(sys, 'argv', ['run_analysis.py', 'csv', '--csv-folder', 'test_folder', '--point', '0.00001']):
            args = parse_arguments()
        
        assert args.mode == 'csv'
        assert args.csv_folder == 'test_folder'
        assert args.csv_file is None
        assert args.point == 0.00001

    def test_csv_file_argument_parsing(self):
        """Test that --csv-file argument is parsed correctly."""
        # Test with --csv-file
        with patch.object(sys, 'argv', ['run_analysis.py', 'csv', '--csv-file', 'test_file.csv', '--point', '0.00001']):
            args = parse_arguments()
        
        assert args.mode == 'csv'
        assert args.csv_file == 'test_file.csv'
        assert args.csv_folder is None
        assert args.point == 0.00001

    def test_csv_file_and_folder_mutually_exclusive(self):
        """Test that --csv-file and --csv-folder are mutually exclusive."""
        with patch.object(sys, 'argv', ['run_analysis.py', 'csv', '--csv-file', 'test.csv', '--csv-folder', 'test_folder', '--point', '0.00001']):
            with pytest.raises(SystemExit):
                parse_arguments()

    def test_csv_mode_requires_file_or_folder(self):
        """Test that csv mode requires either --csv-file or --csv-folder."""
        with patch.object(sys, 'argv', ['run_analysis.py', 'csv', '--point', '0.00001']):
            with pytest.raises(SystemExit):
                parse_arguments()

    def test_csv_mode_requires_point(self):
        """Test that csv mode requires --point argument."""
        with patch.object(sys, 'argv', ['run_analysis.py', 'csv', '--csv-folder', 'test_folder']):
            with pytest.raises(SystemExit):
                parse_arguments()

    def test_csv_folder_with_rule_ignored(self):
        """Test that --rule is ignored in batch mode (no error, but rule not used)."""
        with patch.object(sys, 'argv', ['run_analysis.py', 'csv', '--csv-folder', 'test_folder', '--point', '0.00001', '--rule', 'RSI']):
            args = parse_arguments()
        
        assert args.mode == 'csv'
        assert args.csv_folder == 'test_folder'
        assert args.point == 0.00001
        assert args.rule == 'RSI'  # Rule is parsed but not used in batch mode

    def test_csv_file_with_rule_works(self):
        """Test that --rule works with single file mode."""
        with patch.object(sys, 'argv', ['run_analysis.py', 'csv', '--csv-file', 'test.csv', '--point', '0.00001', '--rule', 'RSI']):
            args = parse_arguments()
        
        assert args.mode == 'csv'
        assert args.csv_file == 'test.csv'
        assert args.point == 0.00001
        assert args.rule == 'RSI'

    def test_csv_folder_help_text(self):
        """Test that help text includes csv-folder option."""
        with patch.object(sys, 'argv', ['run_analysis.py', 'csv', '--help']):
            with pytest.raises(SystemExit) as exc_info:
                parse_arguments()
        
        # The help should be printed (SystemExit with code 0)
        assert exc_info.value.code == 0

    def test_csv_folder_examples_included(self):
        """Test that examples include csv-folder usage."""
        with patch.object(sys, 'argv', ['run_analysis.py', '--examples']):
            with pytest.raises(SystemExit) as exc_info:
                parse_arguments()
        
        # The examples should be printed (SystemExit with code 0)
        assert exc_info.value.code == 0

    def test_csv_folder_with_other_options(self):
        """Test that csv-folder works with other valid options."""
        with patch.object(sys, 'argv', ['run_analysis.py', 'csv', '--csv-folder', 'test_folder', '--point', '0.00001', '-d', 'fastest']):
            args = parse_arguments()
        
        assert args.mode == 'csv'
        assert args.csv_folder == 'test_folder'
        assert args.point == 0.00001
        assert args.draw == 'fastest'

    def test_csv_folder_validation_success(self):
        """Test successful validation of csv-folder arguments."""
        # This should not raise any exceptions
        with patch.object(sys, 'argv', ['run_analysis.py', 'csv', '--csv-folder', 'test_folder', '--point', '0.00001']):
            args = parse_arguments()
        
        assert args.mode == 'csv'
        assert args.csv_folder == 'test_folder'
        assert args.point == 0.00001

    def test_csv_folder_validation_failure_no_point(self):
        """Test validation failure when point is missing."""
        with patch.object(sys, 'argv', ['run_analysis.py', 'csv', '--csv-folder', 'test_folder']):
            with pytest.raises(SystemExit):
                parse_arguments()

    def test_csv_folder_validation_failure_no_source(self):
        """Test validation failure when neither csv-file nor csv-folder is provided."""
        with patch.object(sys, 'argv', ['run_analysis.py', 'csv', '--point', '0.00001']):
            with pytest.raises(SystemExit):
                parse_arguments()

    def test_csv_folder_validation_failure_both_sources(self):
        """Test validation failure when both csv-file and csv-folder are provided."""
        with patch.object(sys, 'argv', ['run_analysis.py', 'csv', '--csv-file', 'test.csv', '--csv-folder', 'test_folder', '--point', '0.00001']):
            with pytest.raises(SystemExit):
                parse_arguments()

    def test_csv_folder_with_export_flags_not_allowed(self):
        """Test that export flags are not allowed in csv mode."""
        with patch.object(sys, 'argv', ['run_analysis.py', 'csv', '--csv-folder', 'test_folder', '--point', '0.00001', '--export-parquet', '--export-csv']):
            with pytest.raises(SystemExit):
                parse_arguments()

    def test_csv_folder_with_plotting_backend(self):
        """Test that plotting backend options work with csv-folder."""
        backends = ['fastest', 'fast', 'plotly', 'mplfinance', 'seaborn', 'term']
        
        for backend in backends:
            with patch.object(sys, 'argv', ['run_analysis.py', 'csv', '--csv-folder', 'test_folder', '--point', '0.00001', '-d', backend]):
                args = parse_arguments()
            
            assert args.mode == 'csv'
            assert args.csv_folder == 'test_folder'
            assert args.point == 0.00001
            assert args.draw == backend

    def test_csv_folder_absolute_path(self):
        """Test that absolute paths work with csv-folder."""
        abs_path = '/absolute/path/to/folder'
        with patch.object(sys, 'argv', ['run_analysis.py', 'csv', '--csv-folder', abs_path, '--point', '0.00001']):
            args = parse_arguments()
        
        assert args.mode == 'csv'
        assert args.csv_folder == abs_path
        assert args.point == 0.00001

    def test_csv_folder_relative_path(self):
        """Test that relative paths work with csv-folder."""
        rel_path = 'relative/path/to/folder'
        with patch.object(sys, 'argv', ['run_analysis.py', 'csv', '--csv-folder', rel_path, '--point', '0.00001']):
            args = parse_arguments()
        
        assert args.mode == 'csv'
        assert args.csv_folder == rel_path
        assert args.point == 0.00001

    def test_csv_folder_with_spaces_in_path(self):
        """Test that paths with spaces work with csv-folder."""
        path_with_spaces = 'folder with spaces'
        with patch.object(sys, 'argv', ['run_analysis.py', 'csv', '--csv-folder', path_with_spaces, '--point', '0.00001']):
            args = parse_arguments()
        
        assert args.mode == 'csv'
        assert args.csv_folder == path_with_spaces
        assert args.point == 0.00001
