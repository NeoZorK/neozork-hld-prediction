import pytest
import pandas as pd
import tempfile
import os
from pathlib import Path
from unittest.mock import patch, MagicMock
from src.interactive.core import InteractiveSystem


class TestRestoreBackup:
    """Test restore from backup functionality."""
    
    @pytest.fixture
    def system(self):
        """Create a test system."""
        return InteractiveSystem()
    
    def test_restore_from_backup_no_data(self, system):
        """Test restore from backup when no data is loaded."""
        with patch('builtins.print') as mock_print:
            system.data_manager.restore_from_backup(system)
            
            # Check that error message is shown
            output_calls = [call[0][0] for call in mock_print.call_args_list]
            assert any("No data loaded" in str(call) for call in output_calls)
    
    def test_restore_from_backup_no_backup_files(self, system):
        """Test restore from backup when no backup files exist."""
        # Create test data
        system.current_data = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
        
        # Mock the glob function to return no files
        with patch('pathlib.Path.glob') as mock_glob:
            mock_glob.return_value = []  # No backup files found
            
            with patch('builtins.input', return_value='q'):  # User quits if asked
                with patch('builtins.print') as mock_print:
                    result = system.data_manager.restore_from_backup(system)
                    
                    # Check that function returns False (quit)
                    assert result is False
                    
                    # Check that backup files search was attempted
                    mock_glob.assert_called()
    
    def test_restore_from_backup_with_data_backup_files(self, system):
        """Test restore from backup with data_backup_*.parquet files."""
        # Create test data
        test_data = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
        system.current_data = test_data.copy()
        
        # Create temporary backup directory and files
        with tempfile.TemporaryDirectory() as temp_dir:
            backup_dir = Path(temp_dir) / "data" / "backups"
            backup_dir.mkdir(parents=True, exist_ok=True)
            
            # Create backup files
            backup_file1 = backup_dir / "data_backup_1234567890.parquet"
            backup_file2 = backup_dir / "data_fixed_1234567891.parquet"
            
            # Create different test data for backups
            backup_data1 = pd.DataFrame({'X': [10, 20, 30], 'Y': [40, 50, 60]})
            backup_data2 = pd.DataFrame({'Z': [100, 200, 300], 'W': [400, 500, 600]})
            
            backup_data1.to_parquet(backup_file1)
            backup_data2.to_parquet(backup_file2)
            
            # Mock the backup directory path
            with patch('pathlib.Path') as mock_path:
                # Mock the backup directory to return our temp directory
                mock_backup_dir = MagicMock()
                mock_backup_dir.exists.return_value = True
                mock_backup_dir.glob.side_effect = lambda pattern: {
                    "backup_*.parquet": [],
                    "data_backup_*.parquet": [backup_file1],
                    "data_fixed_*.parquet": [backup_file2]
                }[pattern]
                
                mock_path.return_value = mock_backup_dir
                
                # Mock user input to select first backup
                with patch('builtins.input', return_value='1'):
                    with patch('builtins.print') as mock_print:
                        system.data_manager.restore_from_backup(system)
                        
                        # Check that backup files were found
                        output_calls = [call[0][0] for call in mock_print.call_args_list]
                        assert any("Found 2 backup files" in str(call) for call in output_calls)
                        
                        # Check that data was restored
                        assert any("Data restored successfully" in str(call) for call in output_calls)
                        
                        # Check that menu was marked as used
                        assert system.menu_manager.used_menus['eda']['restore_from_backup']
    
    def test_restore_from_backup_with_regular_backup_files(self, system):
        """Test restore from backup with backup_*.parquet files."""
        # Create test data
        test_data = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
        system.current_data = test_data.copy()
        
        # Create temporary backup directory and files
        with tempfile.TemporaryDirectory() as temp_dir:
            backup_dir = Path(temp_dir) / "data" / "backups"
            backup_dir.mkdir(parents=True, exist_ok=True)
            
            # Create backup file
            backup_file = backup_dir / "backup_1234567890.parquet"
            
            # Create different test data for backup
            backup_data = pd.DataFrame({'X': [10, 20, 30], 'Y': [40, 50, 60]})
            backup_data.to_parquet(backup_file)
            
            # Mock the backup directory path
            with patch('pathlib.Path') as mock_path:
                # Mock the backup directory to return our temp directory
                mock_backup_dir = MagicMock()
                mock_backup_dir.exists.return_value = True
                mock_backup_dir.glob.side_effect = lambda pattern: {
                    "backup_*.parquet": [backup_file],
                    "data_backup_*.parquet": [],
                    "data_fixed_*.parquet": []
                }[pattern]
                
                mock_path.return_value = mock_backup_dir
                
                # Mock user input to select first backup
                with patch('builtins.input', return_value='1'):
                    with patch('builtins.print') as mock_print:
                        system.data_manager.restore_from_backup(system)
                        
                        # Check that backup files were found
                        output_calls = [call[0][0] for call in mock_print.call_args_list]
                        assert any("Found 1 backup files" in str(call) for call in output_calls)
                        
                        # Check that data was restored
                        assert any("Data restored successfully" in str(call) for call in output_calls)
    
    def test_restore_from_backup_invalid_choice(self, system):
        """Test restore from backup with invalid choice."""
        # Create test data
        test_data = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
        system.current_data = test_data.copy()
        
        # Create temporary backup directory and files
        with tempfile.TemporaryDirectory() as temp_dir:
            backup_dir = Path(temp_dir) / "data" / "backups"
            backup_dir.mkdir(parents=True, exist_ok=True)
            
            # Create backup file
            backup_file = backup_dir / "data_backup_1234567890.parquet"
            backup_data = pd.DataFrame({'X': [10, 20, 30], 'Y': [40, 50, 60]})
            backup_data.to_parquet(backup_file)
            
            # Mock the backup directory path
            with patch('pathlib.Path') as mock_path:
                # Mock the backup directory to return our temp directory
                mock_backup_dir = MagicMock()
                mock_backup_dir.exists.return_value = True
                mock_backup_dir.glob.side_effect = lambda pattern: {
                    "backup_*.parquet": [],
                    "data_backup_*.parquet": [backup_file],
                    "data_fixed_*.parquet": []
                }[pattern]
                
                mock_path.return_value = mock_backup_dir
                
                # Mock user input to select invalid choice
                with patch('builtins.input', return_value='999'):
                    with patch('builtins.print') as mock_print:
                        system.data_manager.restore_from_backup(system)
                        
                        # Check that invalid choice message is shown
                        output_calls = [call[0][0] for call in mock_print.call_args_list]
                        assert any("Invalid choice" in str(call) for call in output_calls)
    
    def test_restore_from_backup_test_mode(self, system):
        """Test restore from backup in test mode (no user input available)."""
        # Create test data
        test_data = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
        system.current_data = test_data.copy()
        
        # Create temporary backup directory and files
        with tempfile.TemporaryDirectory() as temp_dir:
            backup_dir = Path(temp_dir) / "data" / "backups"
            backup_dir.mkdir(parents=True, exist_ok=True)
            
            # Create backup file
            backup_file = backup_dir / "data_backup_1234567890.parquet"
            backup_data = pd.DataFrame({'X': [10, 20, 30], 'Y': [40, 50, 60]})
            backup_data.to_parquet(backup_file)
            
            # Mock the backup directory path
            with patch('pathlib.Path') as mock_path:
                # Mock the backup directory to return our temp directory
                mock_backup_dir = MagicMock()
                mock_backup_dir.exists.return_value = True
                mock_backup_dir.glob.side_effect = lambda pattern: {
                    "backup_*.parquet": [],
                    "data_backup_*.parquet": [backup_file],
                    "data_fixed_*.parquet": []
                }[pattern]
                
                mock_path.return_value = mock_backup_dir
                
                # Mock user input to raise EOFError (test mode)
                with patch('builtins.input', side_effect=EOFError):
                    with patch('builtins.print') as mock_print:
                        system.data_manager.restore_from_backup(system)
                        
                        # Check that test mode message is shown
                        output_calls = [call[0][0] for call in mock_print.call_args_list]
                        assert any("test mode" in str(call) for call in output_calls)
                        
                        # Check that data was restored
                        assert any("Data restored successfully" in str(call) for call in output_calls)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
