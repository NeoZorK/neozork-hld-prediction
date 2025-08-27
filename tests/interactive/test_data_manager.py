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
        system.current_data = pd.DataFrame({
            'Open': [100, 101, 102, 103, 104],
            'High': [105, 106, 107, 108, 109],
            'Low': [95, 96, 97, 98, 99],
            'Close': [102, 103, 104, 105, 106],
            'Volume': [1000, 1100, 1200, 1300, 1400]
        })
        system.current_results = {
            'test_result': {'data': 'test'}
        }
        system.menu_manager = Mock()
        return system
    
    def test_init(self, data_manager):
        """Test DataManager initialization."""
        assert data_manager is not None
    
    def test_load_data_from_file_csv(self, data_manager, tmp_path):
        """Test load_data_from_file with CSV file."""
        # Create test CSV file
        csv_file = tmp_path / "test.csv"
        test_data = pd.DataFrame({'col1': [1, 2, 3], 'col2': [4, 5, 6]})
        test_data.to_csv(csv_file, index=False)
        
        result = data_manager.load_data_from_file(str(csv_file))
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 3
        assert list(result.columns) == ['col1', 'col2']
    
    def test_load_data_from_file_parquet(self, data_manager, tmp_path):
        """Test load_data_from_file with Parquet file."""
        # Create test Parquet file
        parquet_file = tmp_path / "test.parquet"
        test_data = pd.DataFrame({'col1': [1, 2, 3], 'col2': [4, 5, 6]})
        test_data.to_parquet(parquet_file, index=False)
        
        result = data_manager.load_data_from_file(str(parquet_file))
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 3
        assert list(result.columns) == ['col1', 'col2']
    
    def test_load_data_from_file_excel(self, data_manager, tmp_path):
        """Test load_data_from_file with Excel file."""
        # Create test Excel file
        excel_file = tmp_path / "test.xlsx"
        test_data = pd.DataFrame({'col1': [1, 2, 3], 'col2': [4, 5, 6]})
        test_data.to_excel(excel_file, index=False)
        
        result = data_manager.load_data_from_file(str(excel_file))
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 3
        assert list(result.columns) == ['col1', 'col2']
    
    def test_load_data_from_file_unsupported_format(self, data_manager, tmp_path):
        """Test load_data_from_file with unsupported format."""
        # Create test file with unsupported extension
        unsupported_file = tmp_path / "test.txt"
        unsupported_file.write_text("test data")
        
        with pytest.raises(ValueError, match="Unsupported file format"):
            data_manager.load_data_from_file(str(unsupported_file))
    
    def test_load_data_from_file_not_found(self, data_manager):
        """Test load_data_from_file with non-existent file."""
        with pytest.raises(FileNotFoundError):
            data_manager.load_data_from_file("non_existent_file.csv")
    
    def test_load_data_from_folder(self, data_manager, tmp_path):
        """Test load_data_from_folder with data files."""
        # Create test files
        csv_file = tmp_path / "test1.csv"
        parquet_file = tmp_path / "test2.parquet"
        excel_file = tmp_path / "test3.xlsx"
        txt_file = tmp_path / "test4.txt"
        
        pd.DataFrame({'col1': [1, 2]}).to_csv(csv_file, index=False)
        pd.DataFrame({'col2': [3, 4]}).to_parquet(parquet_file, index=False)
        pd.DataFrame({'col3': [5, 6]}).to_excel(excel_file, index=False)
        txt_file.write_text("test data")
        
        result = data_manager.load_data_from_folder(str(tmp_path))
        assert isinstance(result, list)
        assert len(result) == 3  # Should find 3 data files (csv, parquet, excel)
        assert any('test1.csv' in path for path in result)
        assert any('test2.parquet' in path for path in result)
        assert any('test3.xlsx' in path for path in result)
    
    def test_load_data_from_folder_not_found(self, data_manager):
        """Test load_data_from_folder with non-existent folder."""
        with pytest.raises(FileNotFoundError):
            data_manager.load_data_from_folder("non_existent_folder")
    
    def test_load_data_from_folder_not_directory(self, data_manager, tmp_path):
        """Test load_data_from_folder with file instead of directory."""
        file_path = tmp_path / "test.txt"
        file_path.write_text("test")
        
        with pytest.raises(ValueError, match="Path is not a directory"):
            data_manager.load_data_from_folder(str(file_path))
    
    @patch('builtins.input', side_effect=['0'])
    def test_load_data_exit(self, mock_input, data_manager, mock_system):
        """Test load_data with exit option."""
        result = data_manager.load_data(mock_system)
        assert result is False
    
    @patch('builtins.input', side_effect=[''])
    def test_load_data_empty_input(self, mock_input, data_manager, mock_system):
        """Test load_data with empty input."""
        result = data_manager.load_data(mock_system)
        assert result is False
    
    @patch('builtins.input', side_effect=['1', 'y'])
    @patch('pathlib.Path.exists', return_value=True)
    @patch('pathlib.Path.is_dir', return_value=True)
    def test_load_data_folder_number(self, mock_is_dir, mock_exists, mock_input, data_manager, mock_system, tmp_path):
        """Test load_data with folder number selection."""
        # Mock data folder structure
        with patch('pathlib.Path.iterdir') as mock_iterdir:
            mock_iterdir.return_value = [tmp_path / "test.csv"]
            with patch('pathlib.Path.glob') as mock_glob:
                mock_glob.return_value = [tmp_path / "test.csv"]
                with patch.object(data_manager, 'load_data_from_file') as mock_load:
                    mock_load.return_value = pd.DataFrame({'col1': [1, 2, 3]})
                    result = data_manager.load_data(mock_system)
                    assert result is True
    
    @patch('builtins.input', side_effect=['data', 'y'])
    @patch('pathlib.Path.exists', return_value=True)
    @patch('pathlib.Path.is_dir', return_value=True)
    def test_load_data_folder_path(self, mock_is_dir, mock_exists, mock_input, data_manager, mock_system, tmp_path):
        """Test load_data with folder path."""
        with patch('pathlib.Path.glob') as mock_glob:
            mock_glob.return_value = [tmp_path / "test.csv"]
            with patch.object(data_manager, 'load_data_from_file') as mock_load:
                mock_load.return_value = pd.DataFrame({'col1': [1, 2, 3]})
                result = data_manager.load_data(mock_system)
                assert result is True
    
    @patch('builtins.input', side_effect=['data'])
    @patch('pathlib.Path.exists', return_value=False)
    def test_load_data_folder_not_found(self, mock_exists, mock_input, data_manager, mock_system):
        """Test load_data with non-existent folder."""
        result = data_manager.load_data(mock_system)
        assert result is False
    
    @patch('builtins.input', side_effect=['1', 'n', '0', '0', '0', '0'])
    @patch('pathlib.Path.exists', return_value=True)
    @patch('pathlib.Path.is_dir', return_value=True)
    def test_load_data_invalid_folder_number(self, mock_is_dir, mock_exists, mock_input, data_manager, mock_system):
        """Test load_data with invalid folder number."""
        with patch('pathlib.Path.glob') as mock_glob:
            mock_glob.return_value = []
            try:
                result = data_manager.load_data(mock_system)
            except StopIteration:
                result = False  # Expected when input is exhausted
            assert result is False
    
    @patch('builtins.input', side_effect=['data', 'y'])
    @patch('pathlib.Path.exists', return_value=True)
    @patch('pathlib.Path.is_dir', return_value=True)
    def test_load_data_no_files_found(self, mock_is_dir, mock_exists, mock_input, data_manager, mock_system):
        """Test load_data with no data files found."""
        with patch('pathlib.Path.glob') as mock_glob:
            mock_glob.return_value = []
            result = data_manager.load_data(mock_system)
            assert result is False
    
    @patch('builtins.input', side_effect=['data', 'y'])
    @patch('pathlib.Path.exists', return_value=True)
    @patch('pathlib.Path.is_dir', return_value=True)
    def test_load_data_with_mask(self, mock_is_dir, mock_exists, mock_input, data_manager, mock_system, tmp_path):
        """Test load_data with file mask."""
        with patch('pathlib.Path.glob') as mock_glob:
            mock_glob.return_value = [tmp_path / "test_gbpusd.csv"]
            with patch.object(data_manager, 'load_data_from_file') as mock_load:
                mock_load.return_value = pd.DataFrame({'col1': [1, 2, 3]})
                result = data_manager.load_data(mock_system)
                assert result is True
    
    @patch('builtins.input', side_effect=['data', 'y'])
    @patch('pathlib.Path.exists', return_value=True)
    @patch('pathlib.Path.is_dir', return_value=True)
    def test_load_data_load_error(self, mock_is_dir, mock_exists, mock_input, data_manager, mock_system, tmp_path):
        """Test load_data with load error."""
        with patch('pathlib.Path.glob') as mock_glob:
            mock_glob.return_value = [tmp_path / "test.csv"]
            with patch.object(data_manager, 'load_data_from_file') as mock_load:
                mock_load.side_effect = Exception("Load error")
                result = data_manager.load_data(mock_system)
                assert result is False
    
    @patch('builtins.input', side_effect=['data', 'y'])
    @patch('pathlib.Path.exists', return_value=True)
    @patch('pathlib.Path.is_dir', return_value=True)
    def test_load_data_no_files_loaded(self, mock_is_dir, mock_exists, mock_input, data_manager, mock_system):
        """Test load_data with no files successfully loaded."""
        with patch('pathlib.Path.glob') as mock_glob:
            mock_glob.return_value = []
            result = data_manager.load_data(mock_system)
            assert result is False
    
    def test_export_results_no_results(self, data_manager, mock_system):
        """Test export_results with no results."""
        mock_system.current_results = {}
        data_manager.export_results(mock_system)
    
    @patch('pathlib.Path.mkdir')
    @patch('builtins.open', create=True)
    @patch('json.dump')
    def test_export_results_with_results(self, mock_json_dump, mock_open, mock_mkdir, data_manager, mock_system):
        """Test export_results with results."""
        data_manager.export_results(mock_system)
        mock_mkdir.assert_called()
        mock_open.assert_called()
        mock_json_dump.assert_called()
    
    @patch('pathlib.Path.mkdir')
    @patch('builtins.open', create=True)
    @patch('json.dump')
    def test_export_results_with_feature_engineering(self, mock_json_dump, mock_open, mock_mkdir, data_manager, mock_system):
        """Test export_results with feature engineering results."""
        mock_system.current_results['feature_engineering'] = {'test': 'data'}
        data_manager.export_results(mock_system)
        mock_mkdir.assert_called()
        mock_open.assert_called()
        mock_json_dump.assert_called()
    
    @patch('pathlib.Path.mkdir')
    @patch('builtins.open', create=True)
    @patch('json.dump')
    def test_export_results_exception(self, mock_json_dump, mock_open, mock_mkdir, data_manager, mock_system):
        """Test export_results with exception."""
        mock_mkdir.side_effect = Exception("Test error")
        data_manager.export_results(mock_system)
    
    def test_restore_from_backup_no_data(self, data_manager, mock_system):
        """Test restore_from_backup with no data."""
        mock_system.current_data = None
        data_manager.restore_from_backup(mock_system)
    
    @patch('builtins.input', return_value='yes')
    @patch('pathlib.Path.exists', return_value=True)
    def test_restore_from_backup_with_backup_info(self, mock_exists, mock_input, data_manager, mock_system):
        """Test restore_from_backup with backup info."""
        mock_system.current_results['data_fixes'] = {'backup_file': 'backup_test.parquet'}
        with patch('pandas.read_parquet') as mock_read:
            mock_read.return_value = pd.DataFrame({'col1': [1, 2, 3]})
            data_manager.restore_from_backup(mock_system)
            mock_read.assert_called_with('backup_test.parquet')
    
    @patch('builtins.input', side_effect=EOFError)
    @patch('pathlib.Path.exists', return_value=True)
    def test_restore_from_backup_eof(self, mock_exists, mock_input, data_manager, mock_system):
        """Test restore_from_backup with EOFError."""
        mock_system.current_results['data_fixes'] = {'backup_file': 'backup_test.parquet'}
        with patch('pandas.read_parquet') as mock_read:
            mock_read.return_value = pd.DataFrame({'col1': [1, 2, 3]})
            data_manager.restore_from_backup(mock_system)
    
    @patch('pathlib.Path.exists', return_value=True)
    @patch('pathlib.Path.iterdir')
    def test_restore_from_backup_with_backup_files(self, mock_iterdir, mock_exists, data_manager, mock_system):
        """Test restore_from_backup with backup files."""
        mock_backup_file = Mock()
        mock_backup_file.name = "backup_123.parquet"
        mock_backup_file.stat.return_value.st_size = 1024 * 1024  # 1MB
        mock_iterdir.return_value = [mock_backup_file]
        
        with patch('builtins.input', return_value='1'):
            with patch('pandas.read_parquet') as mock_read:
                mock_read.return_value = pd.DataFrame({'col1': [1, 2, 3]})
                data_manager.restore_from_backup(mock_system)
                mock_read.assert_called()
    
    @patch('pathlib.Path.exists', return_value=True)
    @patch('pathlib.Path.iterdir')
    def test_restore_from_backup_invalid_choice(self, mock_iterdir, mock_exists, data_manager, mock_system):
        """Test restore_from_backup with invalid choice."""
        mock_backup_file = Mock()
        mock_backup_file.name = "backup_123.parquet"
        mock_backup_file.stat.return_value.st_size = 1024 * 1024  # 1MB
        mock_iterdir.return_value = [mock_backup_file]
        
        with patch('builtins.input', return_value='999'):
            data_manager.restore_from_backup(mock_system)
    
    @patch('pathlib.Path.exists', return_value=True)
    @patch('pathlib.Path.iterdir')
    def test_restore_from_backup_eof_choice(self, mock_iterdir, mock_exists, data_manager, mock_system):
        """Test restore_from_backup with EOFError during choice."""
        mock_backup_file = Mock()
        mock_backup_file.name = "backup_123.parquet"
        mock_backup_file.stat.return_value.st_size = 1024 * 1024  # 1MB
        mock_iterdir.return_value = [mock_backup_file]
        
        with patch('builtins.input', side_effect=EOFError):
            with patch('pandas.read_parquet') as mock_read:
                mock_read.return_value = pd.DataFrame({'col1': [1, 2, 3]})
                data_manager.restore_from_backup(mock_system)
    
    @patch('pathlib.Path.exists', return_value=True)
    @patch('pathlib.Path.iterdir')
    def test_restore_from_backup_value_error(self, mock_iterdir, mock_exists, data_manager, mock_system):
        """Test restore_from_backup with ValueError during choice."""
        mock_backup_file = Mock()
        mock_backup_file.name = "backup_123.parquet"
        mock_backup_file.stat.return_value.st_size = 1024 * 1024  # 1MB
        mock_iterdir.return_value = [mock_backup_file]
        
        with patch('builtins.input', side_effect=ValueError):
            with patch('pandas.read_parquet') as mock_read:
                mock_read.return_value = pd.DataFrame({'col1': [1, 2, 3]})
                data_manager.restore_from_backup(mock_system)
    
    @patch('pathlib.Path.exists', return_value=False)
    def test_restore_from_backup_no_backup_dir(self, mock_exists, data_manager, mock_system):
        """Test restore_from_backup with no backup directory."""
        data_manager.restore_from_backup(mock_system)
    
    @patch('pathlib.Path.exists', return_value=True)
    @patch('pathlib.Path.iterdir', return_value=[])
    def test_restore_from_backup_no_backup_files(self, mock_iterdir, mock_exists, data_manager, mock_system):
        """Test restore_from_backup with no backup files."""
        data_manager.restore_from_backup(mock_system)
    
    @patch('pathlib.Path.exists', return_value=True)
    @patch('pathlib.Path.iterdir')
    def test_restore_from_backup_exception(self, mock_iterdir, mock_exists, data_manager, mock_system):
        """Test restore_from_backup with exception."""
        mock_iterdir.side_effect = Exception("Test error")
        data_manager.restore_from_backup(mock_system)
