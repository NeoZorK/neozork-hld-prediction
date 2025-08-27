# -*- coding: utf-8 -*-
"""
Tests for data manager module.

This module tests the DataManager class from src/interactive/data_manager.py.
"""

import pytest
import pandas as pd
import numpy as np
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path
import tempfile
import os
import json

# Import the module to test
from src.interactive.data_manager import DataManager


class TestDataManager:
    """Test DataManager class."""
    
    @pytest.fixture
    def data_manager(self):
        """Create DataManager instance for testing."""
        return DataManager()
    
    @pytest.fixture
    def mock_system(self):
        """Create mock system for testing."""
        system = Mock()
        system.current_data = None
        system.current_results = {}
        return system
    
    @pytest.fixture
    def sample_csv_data(self):
        """Create sample CSV data for testing."""
        data = {
            'Date': ['2023-01-01', '2023-01-02', '2023-01-03'],
            'Open': [100.0, 101.0, 102.0],
            'High': [105.0, 106.0, 107.0],
            'Low': [95.0, 96.0, 97.0],
            'Close': [103.0, 104.0, 105.0],
            'Volume': [1000, 1100, 1200]
        }
        return pd.DataFrame(data)
    
    def test_init(self, data_manager):
        """Test DataManager initialization."""
        assert data_manager is not None
    
    def test_load_data_from_file_csv(self, data_manager, sample_csv_data, tmp_path):
        """Test load_data_from_file with CSV file."""
        # Create a temporary CSV file
        csv_file = tmp_path / "test_data.csv"
        sample_csv_data.to_csv(csv_file, index=False)
        
        # Load the data
        result = data_manager.load_data_from_file(str(csv_file))
        
        # Check that data was loaded correctly
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 3
        assert list(result.columns) == ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']
        pd.testing.assert_frame_equal(result, sample_csv_data)
    
    def test_load_data_from_file_parquet(self, data_manager, sample_csv_data, tmp_path):
        """Test load_data_from_file with Parquet file."""
        # Create a temporary Parquet file
        parquet_file = tmp_path / "test_data.parquet"
        sample_csv_data.to_parquet(parquet_file, index=False)
        
        # Load the data
        result = data_manager.load_data_from_file(str(parquet_file))
        
        # Check that data was loaded correctly
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 3
        assert list(result.columns) == ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']
        pd.testing.assert_frame_equal(result, sample_csv_data)
    
    def test_load_data_from_file_excel(self, data_manager, sample_csv_data, tmp_path):
        """Test load_data_from_file with Excel file."""
        # Create a temporary Excel file
        excel_file = tmp_path / "test_data.xlsx"
        sample_csv_data.to_excel(excel_file, index=False)
        
        # Load the data
        result = data_manager.load_data_from_file(str(excel_file))
        
        # Check that data was loaded correctly
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 3
        assert list(result.columns) == ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']
        pd.testing.assert_frame_equal(result, sample_csv_data)
    
    def test_load_data_from_file_not_found(self, data_manager):
        """Test load_data_from_file with non-existent file."""
        with pytest.raises(FileNotFoundError):
            data_manager.load_data_from_file("non_existent_file.csv")
    
    def test_load_data_from_file_unsupported_format(self, data_manager, tmp_path):
        """Test load_data_from_file with unsupported format."""
        # Create a temporary file with unsupported extension
        unsupported_file = tmp_path / "test_data.txt"
        unsupported_file.write_text("some text")
        
        with pytest.raises(ValueError, match="Unsupported file format"):
            data_manager.load_data_from_file(str(unsupported_file))
    
    def test_load_data_from_folder(self, data_manager, sample_csv_data, tmp_path):
        """Test load_data_from_folder."""
        # Create a temporary folder with data files
        folder = tmp_path / "data_folder"
        folder.mkdir()
        
        # Create CSV file
        csv_file = folder / "test1.csv"
        sample_csv_data.to_csv(csv_file, index=False)
        
        # Create Parquet file
        parquet_file = folder / "test2.parquet"
        sample_csv_data.to_parquet(parquet_file, index=False)
        
        # Create text file (should be ignored)
        text_file = folder / "test3.txt"
        text_file.write_text("some text")
        
        # Load data files
        result = data_manager.load_data_from_folder(str(folder))
        
        # Check that only data files were found
        assert len(result) == 2
        assert any("test1.csv" in file for file in result)
        assert any("test2.parquet" in file for file in result)
        assert not any("test3.txt" in file for file in result)
    
    def test_load_data_from_folder_not_found(self, data_manager):
        """Test load_data_from_folder with non-existent folder."""
        with pytest.raises(FileNotFoundError):
            data_manager.load_data_from_folder("non_existent_folder")
    
    def test_load_data_from_folder_not_directory(self, data_manager, tmp_path):
        """Test load_data_from_folder with file instead of directory."""
        # Create a temporary file
        file_path = tmp_path / "not_a_folder.txt"
        file_path.write_text("some text")
        
        with pytest.raises(ValueError, match="Path is not a directory"):
            data_manager.load_data_from_folder(str(file_path))
    
    @patch('builtins.input', return_value='0')
    def test_load_data_exit(self, mock_input, data_manager, mock_system):
        """Test load_data with exit option."""
        result = data_manager.load_data(mock_system)
        assert result is False
    
    @patch('builtins.input', return_value='')
    def test_load_data_no_input(self, mock_input, data_manager, mock_system, capsys):
        """Test load_data with no input."""
        result = data_manager.load_data(mock_system)
        captured = capsys.readouterr()
        assert result is False
        assert "No input provided" in captured.out
    
    @patch('builtins.input', return_value='1')
    @patch('pathlib.Path.exists', return_value=False)
    def test_load_data_no_data_folder(self, mock_exists, mock_input, data_manager, mock_system, capsys):
        """Test load_data with no data folder."""
        result = data_manager.load_data(mock_system)
        captured = capsys.readouterr()
        assert result is False
        assert "Data folder not found" in captured.out
    
    @patch('builtins.input', return_value='1')
    @patch('pathlib.Path.exists', return_value=True)
    @patch('pathlib.Path.is_dir', return_value=True)
    @patch('pathlib.Path.iterdir')
    def test_load_data_no_files_found(self, mock_iterdir, mock_is_dir, mock_exists, mock_input, data_manager, mock_system, capsys):
        """Test load_data with no data files found."""
        # Mock empty directory
        mock_iterdir.return_value = []
        
        result = data_manager.load_data(mock_system)
        captured = capsys.readouterr()
        assert result is False
        assert "No data files found" in captured.out
    
    @patch('builtins.input', return_value='1')
    @patch('pathlib.Path.exists', return_value=True)
    @patch('pathlib.Path.is_dir', return_value=True)
    @patch('pathlib.Path.iterdir')
    def test_load_data_with_files(self, mock_iterdir, mock_is_dir, mock_exists, mock_input, data_manager, mock_system, sample_csv_data, capsys):
        """Test load_data with data files."""
        # Mock directory with CSV file
        mock_file = Mock()
        mock_file.is_file.return_value = True
        mock_file.suffix = '.csv'
        mock_file.name = 'test.csv'
        mock_iterdir.return_value = [mock_file]
        
        # Mock file loading
        with patch.object(data_manager, 'load_data_from_file', return_value=sample_csv_data):
            result = data_manager.load_data(mock_system)
        
        captured = capsys.readouterr()
        assert result is True
        assert "Combined data loaded successfully" in captured.out
        assert mock_system.current_data is not None
        assert len(mock_system.current_data) == 3
    
    def test_export_results_no_results(self, data_manager, mock_system, capsys):
        """Test export_results with no results."""
        data_manager.export_results(mock_system)
        captured = capsys.readouterr()
        assert "No results to export" in captured.out
    
    @patch('pathlib.Path.mkdir')
    @patch('builtins.open', create=True)
    @patch('json.dump')
    def test_export_results_with_results(self, mock_json_dump, mock_open, mock_mkdir, data_manager, mock_system, capsys):
        """Test export_results with results."""
        # Add some results to the system
        mock_system.current_results = {
            'test_result': {'data': 'test'},
            'feature_engineering': {'features': 10}
        }
        
        data_manager.export_results(mock_system)
        
        captured = capsys.readouterr()
        assert "EXPORT RESULTS" in captured.out
        assert "Results exported to" in captured.out
        assert "Summary report exported to" in captured.out
        
        # Check that files were created
        mock_mkdir.assert_called_once()
        assert mock_open.call_count >= 2  # JSON and summary files
        mock_json_dump.assert_called_once()
    
    def test_restore_from_backup_no_data(self, data_manager, mock_system, capsys):
        """Test restore_from_backup with no data."""
        data_manager.restore_from_backup(mock_system)
        captured = capsys.readouterr()
        assert "No data loaded" in captured.out
    
    @patch('builtins.input', return_value='yes')
    @patch('pathlib.Path.exists', return_value=True)
    def test_restore_from_backup_with_backup_info(self, mock_exists, mock_input, data_manager, mock_system, sample_csv_data, capsys):
        """Test restore_from_backup with backup info."""
        mock_system.current_data = sample_csv_data
        mock_system.current_results = {
            'data_fixes': {'backup_file': 'backup_test.parquet'}
        }
        
        # Mock parquet reading
        with patch('pandas.read_parquet', return_value=sample_csv_data):
            data_manager.restore_from_backup(mock_system)
        
        captured = capsys.readouterr()
        assert "RESTORE FROM BACKUP" in captured.out
        assert "Found backup file" in captured.out
        assert "Data restored successfully" in captured.out
        mock_system.menu_manager.mark_menu_as_used.assert_called_once_with('eda', 'restore_from_backup')
    
    @patch('builtins.input', return_value='no')
    @patch('pathlib.Path.exists', return_value=True)
    def test_restore_from_backup_decline_restore(self, mock_exists, mock_input, data_manager, mock_system, sample_csv_data, capsys):
        """Test restore_from_backup when user declines restore."""
        mock_system.current_data = sample_csv_data
        mock_system.current_results = {
            'data_fixes': {'backup_file': 'backup_test.parquet'}
        }
        
        data_manager.restore_from_backup(mock_system)
        
        captured = capsys.readouterr()
        assert "RESTORE FROM BACKUP" in captured.out
        assert "Found backup file" in captured.out
        # Should not call mark_menu_as_used since restore was declined
        mock_system.menu_manager.mark_menu_as_used.assert_not_called()
    
    @patch('pathlib.Path.exists', return_value=True)
    @patch('pathlib.Path.is_dir', return_value=True)
    @patch('pathlib.Path.glob')
    def test_restore_from_backup_with_backup_files(self, mock_glob, mock_is_dir, mock_exists, data_manager, mock_system, sample_csv_data, capsys):
        """Test restore_from_backup with backup files in directory."""
        mock_system.current_data = sample_csv_data
        mock_system.current_results = {}
        
        # Mock backup files
        mock_backup_file = Mock()
        mock_backup_file.name = 'backup_123.parquet'
        mock_backup_file.stat.return_value.st_size = 1024 * 1024  # 1MB
        mock_glob.return_value = [mock_backup_file]
        
        # Mock user input
        with patch('builtins.input', return_value='1'):
            # Mock parquet reading
            with patch('pandas.read_parquet', return_value=sample_csv_data):
                data_manager.restore_from_backup(mock_system)
        
        captured = capsys.readouterr()
        assert "RESTORE FROM BACKUP" in captured.out
        assert "Found 1 backup files" in captured.out
        assert "Data restored successfully" in captured.out
    
    @patch('pathlib.Path.exists', return_value=False)
    def test_restore_from_backup_no_backup_directory(self, mock_exists, data_manager, mock_system, sample_csv_data, capsys):
        """Test restore_from_backup with no backup directory."""
        mock_system.current_data = sample_csv_data
        mock_system.current_results = {}
        
        data_manager.restore_from_backup(mock_system)
        
        captured = capsys.readouterr()
        assert "RESTORE FROM BACKUP" in captured.out
        assert "No backup directory found" in captured.out
    
    @patch('pathlib.Path.exists', return_value=True)
    @patch('pathlib.Path.is_dir', return_value=True)
    @patch('pathlib.Path.glob', return_value=[])
    def test_restore_from_backup_no_backup_files(self, mock_glob, mock_is_dir, mock_exists, data_manager, mock_system, sample_csv_data, capsys):
        """Test restore_from_backup with no backup files."""
        mock_system.current_data = sample_csv_data
        mock_system.current_results = {}
        
        data_manager.restore_from_backup(mock_system)
        
        captured = capsys.readouterr()
        assert "RESTORE FROM BACKUP" in captured.out
        assert "No backup files found" in captured.out
