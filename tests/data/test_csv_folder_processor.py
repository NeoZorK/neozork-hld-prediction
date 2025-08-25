# tests/data/test_csv_folder_processor.py

"""
Tests for CSV folder processing functionality.
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
    """Test cases for CSV folder processing functionality."""

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

    def test_get_csv_files_from_folder_success(self):
        """Test successful CSV file discovery."""
        files = get_csv_files_from_folder(str(self.test_folder))
        
        self.assertEqual(len(files), 3)
        self.assertTrue(all(f.suffix == '.csv' for f in files))
        self.assertTrue(all(f.name in ['test1.csv', 'test2.csv', 'test3.csv'] for f in files))

    def test_get_csv_files_from_folder_not_found(self):
        """Test error when folder doesn't exist."""
        with self.assertRaises(FileNotFoundError):
            get_csv_files_from_folder('/nonexistent/folder')

    def test_get_csv_files_from_folder_not_directory(self):
        """Test error when path is not a directory."""
        # Create a file instead of directory
        file_path = self.test_folder / 'not_a_dir'
        file_path.touch()
        
        with self.assertRaises(ValueError):
            get_csv_files_from_folder(str(file_path))

    def test_get_csv_files_from_folder_no_csv_files(self):
        """Test error when no CSV files found."""
        # Remove all CSV files
        for csv_file in self.test_folder.glob('*.csv'):
            csv_file.unlink()
        
        with self.assertRaises(ValueError):
            get_csv_files_from_folder(str(self.test_folder))

    def test_get_file_info_success(self):
        """Test successful file info retrieval."""
        test_file = self.test_folder / 'test1.csv'
        info = get_file_info(test_file)
        
        self.assertEqual(info['name'], 'test1.csv')
        self.assertEqual(info['path'], test_file)
        self.assertGreater(info['size_bytes'], 0)
        self.assertGreater(info['size_mb'], 0)
        self.assertGreater(info['estimated_time'], 0)

    def test_get_file_info_file_not_found(self):
        """Test file info when file doesn't exist."""
        non_existent_file = self.test_folder / 'nonexistent.csv'
        info = get_file_info(non_existent_file)
        
        self.assertEqual(info['name'], 'nonexistent.csv')
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
            rule='RSI'
        )
        
        self.assertTrue(result['success'])
        self.assertEqual(result['files_processed'], 3)
        self.assertEqual(result['files_failed'], 0)
        self.assertGreater(result['total_time'], 0)
        self.assertEqual(len(result['file_results']), 3)

    @patch('src.data.csv_folder_processor.process_single_csv_file')
    def test_process_csv_folder_with_failures(self, mock_process_single):
        """Test folder processing with some failures."""
        # Mock mixed results
        def mock_process_side_effect(file_path, **kwargs):
            # First file succeeds, others fail
            if 'test1.csv' in str(file_path):
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
            rule='RSI'
        )
        
        self.assertTrue(result['success'])
        self.assertEqual(result['files_processed'], 1)
        self.assertEqual(result['files_failed'], 2)
        self.assertEqual(len(result['failed_files']), 2)

    def test_process_csv_folder_folder_not_found(self):
        """Test folder processing with non-existent folder."""
        result = process_csv_folder(
            folder_path='/nonexistent/folder',
            point_size=0.00001
        )
        
        self.assertFalse(result['success'])
        self.assertEqual(result['files_processed'], 0)
        self.assertEqual(result['files_failed'], 0)
        self.assertIn('error', result)

    @patch('src.workflow.workflow.run_indicator_workflow')
    def test_process_single_csv_file_success(self, mock_workflow):
        """Test successful single file processing."""
        # Mock successful workflow
        mock_workflow.return_value = {
            'success': True,
            'rows_count': 100,
            'columns_count': 5,
            'data_size_mb': 0.1
        }
        
        result = process_single_csv_file(
            file_path=str(self.test_folder / 'test1.csv'),
            point_size=0.00001,
            rule='RSI'
        )
        
        self.assertTrue(result['success'])
        self.assertEqual(result['rows_processed'], 100)
        self.assertEqual(result['columns_count'], 5)
        self.assertEqual(result['data_size_mb'], 0.1)

    @patch('src.workflow.workflow.run_indicator_workflow')
    def test_process_single_csv_file_failure(self, mock_workflow):
        """Test single file processing failure."""
        # Mock failed workflow
        mock_workflow.side_effect = Exception('Test error')
        
        result = process_single_csv_file(
            file_path=str(self.test_folder / 'test1.csv'),
            point_size=0.00001,
            rule='RSI'
        )
        
        self.assertFalse(result['success'])
        self.assertIn('Test error', result['error'])
        self.assertEqual(result['rows_processed'], 0)
        self.assertEqual(result['columns_count'], 0)
        self.assertEqual(result['data_size_mb'], 0)

    def test_process_csv_folder_with_export_formats(self):
        """Test folder processing with export formats."""
        with patch('src.data.csv_folder_processor.process_single_csv_file') as mock_process:
            mock_process.return_value = {
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
                export_formats=['parquet', 'csv']
            )
            
            self.assertTrue(result['success'])
            # Verify that export formats were passed to single file processor
            mock_process.assert_called()
            for call in mock_process.call_args_list:
                self.assertIn('parquet', call[1]['export_formats'])
                self.assertIn('csv', call[1]['export_formats'])


if __name__ == '__main__':
    unittest.main()
