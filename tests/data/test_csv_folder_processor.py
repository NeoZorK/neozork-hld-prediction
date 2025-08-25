# tests/data/test_csv_folder_processor.py

"""
Tests for CSV folder processing functionality with mask support.
All comments are in English.
"""

import unittest
import tempfile
import os
from pathlib import Path
import pandas as pd
from unittest.mock import patch, MagicMock

from src.data.csv_folder_processor import (
    get_csv_files_from_folder,
    get_file_info,
    process_csv_folder,
    process_single_csv_file
)


class TestCSVFolderProcessor(unittest.TestCase):
    """Test cases for CSV folder processing functionality with mask support."""

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

    def test_get_csv_files_from_folder_no_mask(self):
        """Test getting all CSV files without mask."""
        files = get_csv_files_from_folder(str(self.test_folder))
        self.assertEqual(len(files), 7)
        self.assertTrue(all(f.name.endswith('.csv') for f in files))

    def test_get_csv_files_from_folder_with_mask(self):
        """Test getting CSV files with mask filter."""
        # Test with EURUSD mask
        files = get_csv_files_from_folder(str(self.test_folder), mask="EURUSD")
        self.assertEqual(len(files), 2)
        self.assertTrue(all("EURUSD" in f.name for f in files))
        
        # Test with AAPL mask
        files = get_csv_files_from_folder(str(self.test_folder), mask="AAPL")
        self.assertEqual(len(files), 2)
        self.assertTrue(all("AAPL" in f.name for f in files))
        
        # Test with USD mask (should match all)
        files = get_csv_files_from_folder(str(self.test_folder), mask="USD")
        self.assertEqual(len(files), 5)  # Only 5 files contain "USD"
        self.assertTrue(all("USD" in f.name for f in files))

    def test_get_csv_files_from_folder_with_mask_case_insensitive(self):
        """Test mask filtering is case insensitive."""
        # Test with lowercase mask
        files = get_csv_files_from_folder(str(self.test_folder), mask="eurusd")
        self.assertEqual(len(files), 2)
        self.assertTrue(all("EURUSD" in f.name for f in files))
        
        # Test with mixed case mask
        files = get_csv_files_from_folder(str(self.test_folder), mask="EurUsd")
        self.assertEqual(len(files), 2)
        self.assertTrue(all("EURUSD" in f.name for f in files))

    def test_get_csv_files_from_folder_with_mask_no_matches(self):
        """Test mask filtering when no files match."""
        with self.assertRaises(ValueError) as context:
            get_csv_files_from_folder(str(self.test_folder), mask="NONEXISTENT")
        self.assertIn("No CSV files found in folder", str(context.exception))
        self.assertIn("matching mask 'NONEXISTENT'", str(context.exception))

    def test_get_csv_files_from_folder_with_empty_mask(self):
        """Test with empty mask (should return all files)."""
        files = get_csv_files_from_folder(str(self.test_folder), mask="")
        self.assertEqual(len(files), 7)
        self.assertTrue(all(f.name.endswith('.csv') for f in files))

    def test_get_csv_files_from_folder_with_none_mask(self):
        """Test with None mask (should return all files)."""
        files = get_csv_files_from_folder(str(self.test_folder), mask=None)
        self.assertEqual(len(files), 7)
        self.assertTrue(all(f.name.endswith('.csv') for f in files))

    def test_get_csv_files_from_folder_not_directory(self):
        """Test error when path is not a directory."""
        # Create a file instead of directory
        test_file = self.test_folder / "test.txt"
        test_file.write_text("test")
        
        with self.assertRaises(ValueError) as context:
            get_csv_files_from_folder(str(test_file))
        self.assertIn("Path is not a directory", str(context.exception))

    def test_get_csv_files_from_folder_not_found(self):
        """Test error when folder doesn't exist."""
        with self.assertRaises(FileNotFoundError) as context:
            get_csv_files_from_folder("/nonexistent/folder")
        self.assertIn("Folder not found", str(context.exception))

    def test_get_csv_files_from_folder_no_csv_files(self):
        """Test error when no CSV files found."""
        # Create empty directory
        empty_dir = self.test_folder / "empty"
        empty_dir.mkdir()
        
        with self.assertRaises(ValueError) as context:
            get_csv_files_from_folder(str(empty_dir))
        self.assertIn("No CSV files found in folder", str(context.exception))

    def test_get_file_info_success(self):
        """Test getting file information successfully."""
        test_file = self.test_folder / "CSVExport_AAPL.NAS_PERIOD_D1.csv"
        info = get_file_info(test_file)
        
        self.assertEqual(info['name'], "CSVExport_AAPL.NAS_PERIOD_D1.csv")
        self.assertGreater(info['size_bytes'], 0)
        self.assertGreater(info['size_mb'], 0)
        self.assertGreater(info['estimated_time'], 0)

    def test_get_file_info_file_not_found(self):
        """Test getting file info for non-existent file."""
        test_file = self.test_folder / "nonexistent.csv"
        info = get_file_info(test_file)
        
        self.assertEqual(info['name'], "nonexistent.csv")
        self.assertEqual(info['size_bytes'], 0)
        self.assertEqual(info['size_mb'], 0)
        self.assertEqual(info['estimated_time'], 1.0)

    @patch('src.data.csv_folder_processor.process_single_csv_file')
    def test_process_csv_folder_success(self, mock_process_single):
        """Test successful folder processing."""
        # Mock successful processing
        mock_process_single.return_value = {
            'success': True,
            'error': None,
            'rows_processed': 100,
            'columns_count': 5,
            'data_size_mb': 0.1
        }
        
        result = process_csv_folder(
            folder_path=str(self.test_folder),
            point_size=0.00001,
            rule='RSI',
            draw_mode='fastest'
        )
        
        self.assertTrue(result['success'])
        self.assertEqual(result['files_processed'], 7)
        self.assertEqual(result['files_failed'], 0)
        self.assertGreater(result['total_time'], 0)

    @patch('src.data.csv_folder_processor.process_single_csv_file')
    def test_process_csv_folder_with_mask(self, mock_process_single):
        """Test folder processing with mask filter."""
        # Mock successful processing
        mock_process_single.return_value = {
            'success': True,
            'error': None,
            'rows_processed': 100,
            'columns_count': 5,
            'data_size_mb': 0.1
        }
        
        result = process_csv_folder(
            folder_path=str(self.test_folder),
            point_size=0.00001,
            rule='RSI',
            draw_mode='fastest',
            mask='EURUSD'
        )
        
        self.assertTrue(result['success'])
        self.assertEqual(result['files_processed'], 2)  # Only EURUSD files
        self.assertEqual(result['files_failed'], 0)
        self.assertGreater(result['total_time'], 0)

    @patch('src.data.csv_folder_processor.process_single_csv_file')
    def test_process_csv_folder_with_mask_and_export(self, mock_process_single):
        """Test folder processing with mask and export formats."""
        # Mock successful processing
        mock_process_single.return_value = {
            'success': True,
            'error': None,
            'rows_processed': 100,
            'columns_count': 5,
            'data_size_mb': 0.1
        }
        
        result = process_csv_folder(
            folder_path=str(self.test_folder),
            point_size=0.00001,
            rule='RSI',
            draw_mode='fastest',
            export_formats=['parquet', 'csv'],
            mask='AAPL'
        )
        
        self.assertTrue(result['success'])
        self.assertEqual(result['files_processed'], 2)  # Only AAPL files
        self.assertEqual(result['files_failed'], 0)
        self.assertGreater(result['total_time'], 0)

    @patch('src.data.csv_folder_processor.process_single_csv_file')
    def test_process_csv_folder_with_failures(self, mock_process_single):
        """Test folder processing with some failures."""
        # Mock mixed results
        def mock_process_side_effect(file_path, **kwargs):
            # AAPL files succeed, others fail
            if 'AAPL' in str(file_path):
                return {
                    'success': True,
                    'error': None,
                    'rows_processed': 100,
                    'columns_count': 5,
                    'data_size_mb': 0.1
                }
            else:
                return {
                    'success': False,
                    'error': 'Test error',
                    'rows_processed': 0,
                    'columns_count': 0,
                    'data_size_mb': 0
                }
        
        mock_process_single.side_effect = mock_process_side_effect
        
        result = process_csv_folder(
            folder_path=str(self.test_folder),
            point_size=0.00001,
            rule='RSI',
            draw_mode='fastest',
            mask='AAPL'  # Only AAPL files
        )
        
        self.assertTrue(result['success'])
        self.assertEqual(result['files_processed'], 2)  # 2 AAPL files
        self.assertEqual(result['files_failed'], 0)  # All AAPL files succeed
        self.assertEqual(len(result['failed_files']), 0)

    def test_process_csv_folder_folder_not_found(self):
        """Test folder processing with non-existent folder."""
        result = process_csv_folder(
            folder_path="/nonexistent/folder",
            point_size=0.00001,
            rule='RSI'
        )
        
        self.assertFalse(result['success'])
        self.assertIn("Folder not found", result['error'])
        self.assertEqual(result['files_processed'], 0)
        self.assertEqual(result['files_failed'], 0)

    @patch('src.workflow.workflow.run_indicator_workflow')
    def test_process_single_csv_file_success(self, mock_workflow):
        """Test successful single file processing."""
        test_file = self.test_folder / "CSVExport_AAPL.NAS_PERIOD_D1.csv"
        
        # Mock successful workflow
        mock_workflow.return_value = {
            'success': True,
            'rows_count': 100,
            'columns_count': 5,
            'data_size_mb': 0.1
        }
        
        result = process_single_csv_file(
            file_path=str(test_file),
            point_size=0.00001,
            rule='RSI',
            draw_mode='fastest'
        )
        
        self.assertTrue(result['success'])
        self.assertEqual(result['rows_processed'], 100)
        self.assertEqual(result['columns_count'], 5)
        self.assertEqual(result['data_size_mb'], 0.1)

    @patch('src.workflow.workflow.run_indicator_workflow')
    def test_process_single_csv_file_failure(self, mock_workflow):
        """Test single file processing failure."""
        test_file = self.test_folder / "CSVExport_AAPL.NAS_PERIOD_D1.csv"
        
        # Mock failed workflow
        mock_workflow.side_effect = Exception('Test error')
        
        result = process_single_csv_file(
            file_path=str(test_file),
            point_size=0.00001,
            rule='RSI',
            draw_mode='fastest'
        )
        
        self.assertFalse(result['success'])
        self.assertIn('Test error', result['error'])
        self.assertEqual(result['rows_processed'], 0)
        self.assertEqual(result['columns_count'], 0)
        self.assertEqual(result['data_size_mb'], 0)


if __name__ == '__main__':
    unittest.main()
