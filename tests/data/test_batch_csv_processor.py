# File: tests/data/test_batch_csv_processor.py
# -*- coding: utf-8 -*-

"""
Tests for batch CSV processing functionality.
All comments are in English.
"""
import pytest
import tempfile
import os
from pathlib import Path
from unittest.mock import patch, MagicMock

from src.data.batch_csv_processor import find_csv_files_in_folder, process_csv_folder


class TestBatchCSVProcessor:
    """Test cases for batch CSV processing functionality."""

    def test_find_csv_files_in_folder_success(self):
        """Test finding CSV files in a folder successfully."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create test CSV files
            csv_files = [
                "test1.csv",
                "test2.CSV",
                "test3.csv"
            ]
            
            for csv_file in csv_files:
                (Path(temp_dir) / csv_file).touch()
            
            # Create a non-CSV file (should be ignored)
            (Path(temp_dir) / "test.txt").touch()
            
            # Test finding CSV files
            found_files = find_csv_files_in_folder(temp_dir)
            
            # Should find all CSV files (case insensitive)
            assert len(found_files) == 3
            assert all(Path(f).suffix.lower() == '.csv' for f in found_files)
            assert all(Path(f).name in csv_files for f in found_files)

    def test_find_csv_files_in_folder_empty(self):
        """Test finding CSV files in an empty folder."""
        with tempfile.TemporaryDirectory() as temp_dir:
            found_files = find_csv_files_in_folder(temp_dir)
            assert len(found_files) == 0

    def test_find_csv_files_in_folder_nonexistent(self):
        """Test finding CSV files in a non-existent folder."""
        found_files = find_csv_files_in_folder("/nonexistent/folder")
        assert len(found_files) == 0

    def test_find_csv_files_in_folder_not_directory(self):
        """Test finding CSV files when path is not a directory."""
        with tempfile.NamedTemporaryFile(suffix='.csv', delete=False) as temp_file:
            temp_file.write(b"test")
            temp_file_path = temp_file.name
        
        try:
            found_files = find_csv_files_in_folder(temp_file_path)
            assert len(found_files) == 0
        finally:
            os.unlink(temp_file_path)

    def test_find_csv_files_in_folder_sorted(self):
        """Test that CSV files are returned in sorted order."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create CSV files in non-alphabetical order
            csv_files = ["z_test.csv", "a_test.csv", "m_test.csv"]
            
            for csv_file in csv_files:
                (Path(temp_dir) / csv_file).touch()
            
            found_files = find_csv_files_in_folder(temp_dir)
            
            # Should be sorted alphabetically
            assert len(found_files) == 3
            file_names = [Path(f).name for f in found_files]
            assert file_names == sorted(file_names)

    @patch('src.data.batch_csv_processor.fetch_csv_data')
    def test_process_csv_folder_success(self, mock_fetch_csv):
        """Test successful batch processing of CSV folder."""
        # Mock successful CSV processing
        mock_df = MagicMock()
        mock_df.empty = False
        mock_df.__len__ = MagicMock(return_value=100)
        mock_fetch_csv.return_value = mock_df
        
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create test CSV files
            csv_files = ["test1.csv", "test2.csv"]
            for csv_file in csv_files:
                (Path(temp_dir) / csv_file).touch()
            
            # Create mock args
            args = MagicMock()
            args.csv_folder = temp_dir
            args.point = 0.00001
            
            # Test processing
            results = process_csv_folder(args)
            
            # Verify results
            assert results["success"] is True
            assert results["total_files"] == 2
            assert results["processed_files"] == 2
            assert results["successful_conversions"] == 2
            assert results["failed_conversions"] == 0
            assert len(results["converted_files"]) == 2
            assert len(results["failed_files"]) == 0
            assert len(results["error_messages"]) == 0

    @patch('src.data.batch_csv_processor.fetch_csv_data')
    def test_process_csv_folder_with_failures(self, mock_fetch_csv):
        """Test batch processing with some file failures."""
        # Mock mixed results: first file succeeds, second fails
        def mock_fetch_side_effect(*args, **kwargs):
            file_path = args[0] if args else kwargs.get('file_path', '')
            if 'test1.csv' in file_path:
                mock_df = MagicMock()
                mock_df.empty = False
                mock_df.__len__ = MagicMock(return_value=100)
                return mock_df
            else:
                return None
        
        mock_fetch_csv.side_effect = mock_fetch_side_effect
        
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create test CSV files
            csv_files = ["test1.csv", "test2.csv"]
            for csv_file in csv_files:
                (Path(temp_dir) / csv_file).touch()
            
            # Create mock args
            args = MagicMock()
            args.csv_folder = temp_dir
            args.point = 0.00001
            
            # Test processing
            results = process_csv_folder(args)
            
            # Verify results
            assert results["success"] is True  # Should still be successful if any files processed
            assert results["total_files"] == 2
            assert results["processed_files"] == 2
            assert results["successful_conversions"] == 1
            assert results["failed_conversions"] == 1
            assert len(results["converted_files"]) == 1
            assert len(results["failed_files"]) == 1
            assert len(results["error_messages"]) == 1

    @patch('src.data.batch_csv_processor.fetch_csv_data')
    def test_process_csv_folder_all_failures(self, mock_fetch_csv):
        """Test batch processing when all files fail."""
        # Mock all files failing
        mock_fetch_csv.return_value = None
        
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create test CSV files
            csv_files = ["test1.csv", "test2.csv"]
            for csv_file in csv_files:
                (Path(temp_dir) / csv_file).touch()
            
            # Create mock args
            args = MagicMock()
            args.csv_folder = temp_dir
            args.point = 0.00001
            
            # Test processing
            results = process_csv_folder(args)
            
            # Verify results
            assert results["success"] is False  # Should fail if no files processed successfully
            assert results["total_files"] == 2
            assert results["processed_files"] == 2
            assert results["successful_conversions"] == 0
            assert results["failed_conversions"] == 2
            assert len(results["converted_files"]) == 0
            assert len(results["failed_files"]) == 2
            assert len(results["error_messages"]) == 2

    def test_process_csv_folder_no_files(self):
        """Test batch processing when no CSV files are found."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create mock args
            args = MagicMock()
            args.csv_folder = temp_dir
            args.point = 0.00001
            
            # Test processing
            results = process_csv_folder(args)
            
            # Verify results
            assert results["success"] is False
            assert results["total_files"] == 0
            assert results["processed_files"] == 0
            assert results["successful_conversions"] == 0
            assert results["failed_conversions"] == 0
            assert len(results["converted_files"]) == 0
            assert len(results["failed_files"]) == 0
            assert len(results["error_messages"]) == 1
            assert "No CSV files found" in results["error_messages"][0]

    @patch('src.data.batch_csv_processor.fetch_csv_data')
    def test_process_csv_folder_exception_handling(self, mock_fetch_csv):
        """Test batch processing with exception handling."""
        # Mock exception during processing
        mock_fetch_csv.side_effect = Exception("Test exception")
        
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create test CSV file
            (Path(temp_dir) / "test.csv").touch()
            
            # Create mock args
            args = MagicMock()
            args.csv_folder = temp_dir
            args.point = 0.00001
            
            # Test processing
            results = process_csv_folder(args)
            
            # Verify results
            assert results["success"] is False
            assert results["total_files"] == 1
            assert results["processed_files"] == 1
            assert results["successful_conversions"] == 0
            assert results["failed_conversions"] == 1
            assert len(results["converted_files"]) == 0
            assert len(results["failed_files"]) == 1
            assert len(results["error_messages"]) == 1
            assert "Test exception" in results["error_messages"][0]

    def test_process_csv_folder_nonexistent_folder(self):
        """Test batch processing with non-existent folder."""
        # Create mock args
        args = MagicMock()
        args.csv_folder = "/nonexistent/folder"
        args.point = 0.00001
        
        # Test processing
        results = process_csv_folder(args)
        
        # Verify results
        assert results["success"] is False
        assert results["total_files"] == 0
        assert results["processed_files"] == 0
        assert results["successful_conversions"] == 0
        assert results["failed_conversions"] == 0
        assert len(results["converted_files"]) == 0
        assert len(results["failed_files"]) == 0
        assert len(results["error_messages"]) == 1
        assert "No CSV files found" in results["error_messages"][0]
