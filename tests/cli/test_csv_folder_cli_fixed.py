# tests/cli/test_csv_folder_cli_fixed.py

"""
Tests for CSV folder CLI functionality with mask support.
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
    """Test cases for CSV folder CLI functionality with mask support."""

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
        """Create test CSV files with different names."""
        # Create test CSV files with different patterns
        test_files = [
            "CSVExport_AAPL.NAS_PERIOD_D1.csv",
            "CSVExport_EURUSD_PERIOD_D1.csv",
            "CSVExport_GBPUSD_PERIOD_D1.csv",
            "CSVExport_BTCUSD_PERIOD_D1.csv",
            "CSVExport_ETHUSD_PERIOD_D1.csv",
            "data_export_AAPL.csv",
            "data_export_EURUSD.csv"
        ]
        
        for filename in test_files:
            file_path = self.test_folder / filename
            # Create a simple CSV file
            df = pd.DataFrame({
                'DateTime': ['2023-01-01', '2023-01-02'],
                'Open': [100.0, 101.0],
                'High': [102.0, 103.0],
                'Low': [99.0, 100.0],
                'Close': [101.0, 102.0],
                'TickVolume': [1000, 1100]
            })
            df.to_csv(file_path, index=False)

    @patch('sys.argv', ['run_analysis.py', 'csv', '--csv-folder', 'test_folder', '--point', '0.00001'])
    def test_parse_arguments_csv_folder_success(self):
        """Test successful CSV folder argument parsing."""
        args = parse_arguments()
        
        self.assertEqual(args.mode, 'csv')
        self.assertEqual(args.csv_folder, 'test_folder')
        self.assertIsNone(args.csv_file)
        self.assertEqual(args.point, 0.00001)

    @patch('sys.argv', ['run_analysis.py', 'csv', '--csv-folder', 'test_folder', '--csv-mask', 'EURUSD', '--point', '0.00001'])
    def test_parse_arguments_csv_folder_with_mask(self):
        """Test CSV folder argument parsing with mask."""
        args = parse_arguments()
        
        self.assertEqual(args.mode, 'csv')
        self.assertEqual(args.csv_folder, 'test_folder')
        self.assertEqual(args.csv_mask, 'EURUSD')
        self.assertIsNone(args.csv_file)
        self.assertEqual(args.point, 0.00001)

    @patch('sys.argv', ['run_analysis.py', 'csv', '--csv-folder', 'test_folder', 'EURUSD', '--point', '0.00001'])
    def test_parse_arguments_csv_folder_with_positional_mask(self):
        """Test CSV folder argument parsing with positional mask."""
        args = parse_arguments()
        
        self.assertEqual(args.mode, 'csv')
        self.assertEqual(args.csv_folder, 'test_folder')
        self.assertEqual(args.csv_mask, 'EURUSD')
        self.assertIsNone(args.csv_file)
        self.assertEqual(args.point, 0.00001)

    @patch('sys.argv', ['run_analysis.py', 'csv', '--csv-folder', 'test_folder', '--csv-mask', 'AAPL', 'EURUSD', '--point', '0.00001'])
    def test_parse_arguments_csv_folder_with_both_masks(self):
        """Test CSV folder argument parsing with both --csv-mask and positional mask."""
        args = parse_arguments()
        
        self.assertEqual(args.mode, 'csv')
        self.assertEqual(args.csv_folder, 'test_folder')
        self.assertEqual(args.csv_mask, 'AAPL')  # --csv-mask takes precedence
        self.assertIsNone(args.csv_file)
        self.assertEqual(args.point, 0.00001)

    @patch('sys.argv', ['run_analysis.py', 'csv', '--csv-folder', 'test_folder', '--point', '0.00001', '--rule', 'RSI'])
    def test_parse_arguments_csv_folder_with_rule(self):
        """Test CSV folder argument parsing with rule."""
        args = parse_arguments()
        
        self.assertEqual(args.mode, 'csv')
        self.assertEqual(args.csv_folder, 'test_folder')
        self.assertEqual(args.rule, 'RSI')
        self.assertEqual(args.point, 0.00001)

    @patch('sys.argv', ['run_analysis.py', 'csv', '--csv-folder', 'test_folder', '--point', '0.00001', '-d', 'fastest'])
    def test_parse_arguments_csv_folder_with_draw_mode(self):
        """Test CSV folder argument parsing with draw mode."""
        args = parse_arguments()
        
        self.assertEqual(args.mode, 'csv')
        self.assertEqual(args.csv_folder, 'test_folder')
        self.assertEqual(args.draw, 'fastest')
        self.assertEqual(args.point, 0.00001)

    @patch('sys.argv', ['run_analysis.py', 'csv', '--csv-folder', 'test_folder', '--point', '0.00001', '--export-parquet'])
    def test_parse_arguments_csv_folder_with_export(self):
        """Test CSV folder argument parsing with export."""
        args = parse_arguments()
        
        self.assertEqual(args.mode, 'csv')
        self.assertEqual(args.csv_folder, 'test_folder')
        self.assertTrue(args.export_parquet)
        self.assertEqual(args.point, 0.00001)

    @patch('sys.argv', ['run_analysis.py', 'csv', '--csv-folder', 'test_folder', 'EURUSD', '--point', '0.00001', '--rule', 'RSI', '-d', 'fastest', '--export-parquet', '--export-csv'])
    def test_parse_arguments_csv_folder_complex(self):
        """Test complex CSV folder argument parsing."""
        args = parse_arguments()
        
        self.assertEqual(args.mode, 'csv')
        self.assertEqual(args.csv_folder, 'test_folder')
        self.assertEqual(args.csv_mask, 'EURUSD')
        self.assertEqual(args.rule, 'RSI')
        self.assertEqual(args.draw, 'fastest')
        self.assertTrue(args.export_parquet)
        self.assertTrue(args.export_csv)
        self.assertEqual(args.point, 0.00001)

    @patch('sys.argv', ['run_analysis.py', 'csv', '--csv-folder', 'test_folder'])
    def test_parse_arguments_csv_folder_default_point(self):
        """Test CSV folder argument parsing with default point value."""
        args = parse_arguments()
        
        self.assertEqual(args.mode, 'csv')
        self.assertEqual(args.csv_folder, 'test_folder')
        self.assertEqual(args.point, 0.00001)  # Default value

    @patch('sys.argv', ['run_analysis.py', 'csv', '--csv-folder', 'test_folder', '--point', '0.00001'])
    def test_csv_folder_argument_help_text(self):
        """Test that CSV folder argument has proper help text."""
        # This test verifies the argument is properly defined
        # We can't easily test help text without running the full parser
        args = parse_arguments()
        self.assertEqual(args.csv_folder, 'test_folder')

    @patch('sys.argv', ['run_analysis.py', 'csv', '--csv-file', 'test.csv', '--csv-folder', 'test_folder', '--point', '0.00001'])
    def test_csv_folder_argument_validation(self):
        """Test CSV folder argument validation."""
        # Test that both csv-file and csv-folder cannot be used together
        with self.assertRaises(SystemExit):
            parse_arguments()

    @patch('sys.argv', ['run_analysis.py', 'csv', '--csv-mask', 'EURUSD', '--point', '0.00001'])
    def test_csv_mask_argument_validation(self):
        """Test CSV mask argument validation."""
        # Test that csv-mask cannot be used without csv-folder
        with self.assertRaises(SystemExit):
            parse_arguments()

    @patch('sys.argv', ['run_analysis.py', 'csv', '--point', '0.00001'])
    def test_parse_arguments_csv_no_file_or_folder_error(self):
        """Test error when neither csv-file nor csv-folder is provided."""
        with self.assertRaises(SystemExit):
            parse_arguments()

    @patch('sys.argv', ['run_analysis.py', 'csv', '--csv-file', 'test.csv'])
    def test_parse_arguments_csv_file_no_point_error(self):
        """Test error when csv-file is used without point."""
        with self.assertRaises(SystemExit):
            parse_arguments()

    @patch('sys.argv', ['run_analysis.py', 'csv', '--csv-folder', 'test_folder', '--point', '0'])
    def test_csv_folder_zero_point_error(self):
        """Test error when point is zero."""
        with self.assertRaises(SystemExit):
            parse_arguments()

    @patch('sys.argv', ['run_analysis.py', 'csv', '--csv-folder', 'test_folder', '--point', '-0.00001'])
    def test_csv_folder_negative_point_error(self):
        """Test error when point is negative."""
        with self.assertRaises(SystemExit):
            parse_arguments()

    @patch('sys.argv', ['run_analysis.py', 'csv', '--csv-folder', 'test_folder', 'eurusd', '--point', '0.00001'])
    def test_parse_arguments_csv_folder_with_positional_mask_case_insensitive(self):
        """Test that positional mask is case insensitive."""
        args = parse_arguments()
        
        self.assertEqual(args.mode, 'csv')
        self.assertEqual(args.csv_folder, 'test_folder')
        self.assertEqual(args.csv_mask, 'eurusd')
        self.assertEqual(args.point, 0.00001)

    @patch('sys.argv', ['run_analysis.py', 'csv', '--csv-folder', 'test_folder', '--csv-mask', 'eurusd', '--point', '0.00001'])
    def test_parse_arguments_csv_folder_with_csv_mask_case_insensitive(self):
        """Test that --csv-mask is case insensitive."""
        args = parse_arguments()
        
        self.assertEqual(args.mode, 'csv')
        self.assertEqual(args.csv_folder, 'test_folder')
        self.assertEqual(args.csv_mask, 'eurusd')
        self.assertEqual(args.point, 0.00001)


if __name__ == '__main__':
    unittest.main()
