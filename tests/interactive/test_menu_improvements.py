import pytest
import pandas as pd
import numpy as np
import tempfile
import os
from pathlib import Path
from unittest.mock import patch, MagicMock
from src.interactive.core import InteractiveSystem


class TestMenuImprovements:
    """Test menu improvements including 00 option, clear backup, and individual fixes."""
    
    @pytest.fixture
    def system(self):
        """Create a test system."""
        return InteractiveSystem()
    
    def test_menu_00_option_support(self, system):
        """Test that '00' option works for returning to main menu."""
        with patch('builtins.input', return_value='00'):
            with patch('builtins.print') as mock_print:
                system.analysis_runner.run_eda_analysis(system)
                output_calls = [call[0][0] for call in mock_print.call_args_list]
                assert any("00. 🏠 Main Menu" in str(call) for call in output_calls)
    
    def test_clear_data_backup_no_files(self, system):
        """Test clear data backup when no backup files exist."""
        system.current_data = pd.DataFrame({'A': [1, 2, 3]})
        
        # Mock the backup directory path to return empty results
        with patch('pathlib.Path') as mock_path:
            # Mock the backup directory to return empty results
            mock_backup_dir = MagicMock()
            mock_backup_dir.exists.return_value = True
            mock_backup_dir.glob.side_effect = lambda pattern: []
            
            mock_path.return_value = mock_backup_dir
            
            with patch('builtins.print') as mock_print:
                system.data_manager.clear_data_backup(system)
                output_calls = [call[0][0] for call in mock_print.call_args_list]
                assert any("No backup files found to clear" in str(call) for call in output_calls)
    
    def test_individual_fix_menu_display(self, system):
        """Test that individual fix menu displays correctly."""
        system.current_data = pd.DataFrame({
            'A': [1, 2, np.nan, 4, 5],
            'B': [1, 1, 2, 2, 3]
        })
        
        nan_summary = [{'column': 'A', 'count': 1}]
        dupe_summary = [{'column': 'B', 'count': 1}]
        
        with patch('builtins.input', return_value='0'):
            with patch('builtins.print') as mock_print:
                system.analysis_runner.show_individual_fix_menu(
                    system, nan_summary, dupe_summary, [], [], [], []
                )
                output_calls = [call[0][0] for call in mock_print.call_args_list]
                assert any("INDIVIDUAL FIX OPTIONS" in str(call) for call in output_calls)
                assert any("Fix NaN values" in str(call) for call in output_calls)
                assert any("Fix Duplicates" in str(call) for call in output_calls)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
