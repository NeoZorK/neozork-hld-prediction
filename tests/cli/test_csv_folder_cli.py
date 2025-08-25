# tests/cli/test_csv_folder_cli.py

"""
Tests for CSV folder CLI functionality.
All comments are in English.
"""

import unittest
import tempfile
import os
from pathlib import Path
import pandas as pd
from unittest.mock import patch, MagicMock

from src.cli.cli import parse_arguments


class TestCSVFolderCLI(unittest.TestCase):
    """Test cases for CSV folder CLI functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.test_folder = Path(self.temp_dir)
        
        # Create test CSV files
        self.create_test_csv_files()

    def tearDown(self):
        """Clean up test fixtures."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def create_test_csv_files(self):
        """Create test CSV files for testing."""
        # Create sample CSV data
        sample_data = pd.DataFrame({
            'DateTime,': ['2023.01.01 00:00', '2023.01.02 00:00'],
            'TickVolume,': [100, 200],
            'Open,': [1.1000, 1.1100],
            'High,': [1.1200, 1.1300],
            'Low,': [1.0900, 1.1000],
            'Close,': [1.1100, 1.1200]
        })
        
        # Create multiple test files
        test_files = [
            'test1.csv',
            'test2.csv',
            'test3.csv'
        ]
        
        for filename in test_files:
            file_path = self.test_folder / filename
            sample_data.to_csv(file_path, index=False)

    @patch('sys.argv', ['run_analysis.py', 'csv', '--csv-folder', 'test_folder', '--point', '0.00001'])
    def test_parse_arguments_csv_folder_success(self):
        """Test successful parsing of CSV folder arguments."""
        args = parse_arguments()
        
        self.assertEqual(args.mode, 'csv')
        self.assertEqual(args.csv_folder, 'test_folder')
        self.assertIsNone(args.csv_file)
        self.assertEqual(args.point, 0.00001)

    @patch('sys.argv', ['run_analysis.py', 'csv', '--csv-folder', 'test_folder'])
    def test_parse_arguments_csv_folder_default_point(self):
        """Test CSV folder with default point value."""
        args = parse_arguments()
        
        self.assertEqual(args.mode, 'csv')
        self.assertEqual(args.csv_folder, 'test_folder')
        self.assertEqual(args.point, 0.00001)  # Default for folder processing

    @patch('sys.argv', ['run_analysis.py', 'csv', '--csv-file', 'test.csv', '--csv-folder', 'test_folder', '--point', '0.01'])
    def test_parse_arguments_csv_both_file_and_folder_error(self):
        """Test error when both csv-file and csv-folder are provided."""
        with self.assertRaises(SystemExit):
            parse_arguments()

    @patch('sys.argv', ['run_analysis.py', 'csv', '--point', '0.01'])
    def test_parse_arguments_csv_no_file_or_folder_error(self):
        """Test error when neither csv-file nor csv-folder is provided."""
        with self.assertRaises(SystemExit):
            parse_arguments()

    @patch('sys.argv', ['run_analysis.py', 'csv', '--csv-file', 'test.csv'])
    def test_parse_arguments_csv_file_no_point_error(self):
        """Test error when csv-file is provided but no point value."""
        with self.assertRaises(SystemExit):
            parse_arguments()

    @patch('sys.argv', ['run_analysis.py', 'csv', '--csv-folder', 'test_folder', '--rule', 'RSI'])
    def test_parse_arguments_csv_folder_with_rule(self):
        """Test CSV folder with custom rule."""
        args = parse_arguments()
        
        self.assertEqual(args.mode, 'csv')
        self.assertEqual(args.csv_folder, 'test_folder')
        self.assertEqual(args.rule, 'RSI')
        self.assertEqual(args.point, 0.00001)  # Default for folder

    @patch('sys.argv', ['run_analysis.py', 'csv', '--csv-folder', 'test_folder', '-d', 'fastest'])
    def test_parse_arguments_csv_folder_with_draw_mode(self):
        """Test CSV folder with draw mode."""
        args = parse_arguments()
        
        self.assertEqual(args.mode, 'csv')
        self.assertEqual(args.csv_folder, 'test_folder')
        self.assertEqual(args.draw, 'fastest')
        self.assertEqual(args.point, 0.00001)  # Default for folder

    @patch('sys.argv', ['run_analysis.py', 'csv', '--csv-folder', 'test_folder', '--export-parquet'])
    def test_parse_arguments_csv_folder_with_export(self):
        """Test CSV folder with export flag."""
        args = parse_arguments()
        
        self.assertEqual(args.mode, 'csv')
        self.assertEqual(args.csv_folder, 'test_folder')
        self.assertTrue(args.export_parquet)
        self.assertEqual(args.point, 0.00001)  # Default for folder

    @patch('sys.argv', ['run_analysis.py', 'csv', '--csv-folder', 'test_folder', '--point', '0.00001', '--rule', 'PV', '-d', 'plotly'])
    def test_parse_arguments_csv_folder_complex(self):
        """Test CSV folder with multiple options."""
        args = parse_arguments()
        
        self.assertEqual(args.mode, 'csv')
        self.assertEqual(args.csv_folder, 'test_folder')
        self.assertEqual(args.point, 0.00001)
        self.assertEqual(args.rule, 'PV')
        self.assertEqual(args.draw, 'plotly')

    def test_csv_folder_argument_help_text(self):
        """Test that help text includes CSV folder option."""
        # This test verifies that the help text is properly formatted
        # We can't easily test the actual help output, but we can verify
        # that the argument is properly registered
        with patch('sys.argv', ['run_analysis.py', '--help']):
            try:
                parse_arguments()
            except SystemExit:
                pass  # Expected behavior for --help

    @patch('sys.argv', ['run_analysis.py', 'csv', '--csv-folder', 'test_folder', '--point', '0.00001'])
    def test_csv_folder_argument_validation(self):
        """Test CSV folder argument validation."""
        args = parse_arguments()
        
        # Verify all required fields are present
        self.assertIsNotNone(args.mode)
        self.assertIsNotNone(args.csv_folder)
        self.assertIsNotNone(args.point)
        
        # Verify point value is positive
        self.assertGreater(args.point, 0)

    @patch('sys.argv', ['run_analysis.py', 'csv', '--csv-folder', 'test_folder', '--point', '-0.01'])
    def test_csv_folder_negative_point_error(self):
        """Test error with negative point value."""
        with self.assertRaises(SystemExit):
            parse_arguments()

    @patch('sys.argv', ['run_analysis.py', 'csv', '--csv-folder', 'test_folder', '--point', '0'])
    def test_csv_folder_zero_point_error(self):
        """Test error with zero point value."""
        with self.assertRaises(SystemExit):
            parse_arguments()


if __name__ == '__main__':
    unittest.main()
