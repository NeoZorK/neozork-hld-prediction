#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Menu Exit Commands

This test verifies that exit commands ("Exit", "00", "0") work correctly
in all menus of the interactive system.
"""

import pytest
import sys
from unittest.mock import patch, MagicMock
from io import StringIO
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent.parent))

from src.interactive import InteractiveSystem


class TestMenuExitCommands:
    """Test class for menu exit commands functionality."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.system = InteractiveSystem()
    
    @patch('builtins.input')
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_menu_exit_commands(self, mock_stdout, mock_input):
        """Test exit commands in main menu."""
        # Test "0" command
        mock_input.side_effect = ['0']
        
        with patch('src.interactive.core.InteractiveSystem.safe_input') as mock_safe_input:
            mock_safe_input.return_value = None
            self.system.run()
        
        output = mock_stdout.getvalue()
        assert "👋 Thank you for using NeoZorK HLD Prediction Interactive System!" in output
        assert "Goodbye!" in output
    
    @patch('builtins.input')
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_menu_exit_text_commands(self, mock_stdout, mock_input):
        """Test text exit commands in main menu."""
        # Test "exit" command
        mock_input.side_effect = ['exit']
        
        with patch('src.interactive.core.InteractiveSystem.safe_input') as mock_safe_input:
            mock_safe_input.return_value = None
            self.system.run()
        
        output = mock_stdout.getvalue()
        assert "👋 Thank you for using NeoZorK HLD Prediction Interactive System!" in output
        assert "Goodbye!" in output
    
    @patch('builtins.input')
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_menu_00_command(self, mock_stdout, mock_input):
        """Test "00" command in main menu."""
        # Test "00" command
        mock_input.side_effect = ['00']
        
        with patch('src.interactive.core.InteractiveSystem.safe_input') as mock_safe_input:
            mock_safe_input.return_value = None
            self.system.run()
        
        output = mock_stdout.getvalue()
        assert "👋 Thank you for using NeoZorK HLD Prediction Interactive System!" in output
        assert "Goodbye!" in output
    
    @patch('builtins.input')
    @patch('sys.stdout', new_callable=StringIO)
    def test_eda_menu_exit_commands(self, mock_stdout, mock_input):
        """Test exit commands in EDA menu."""
        # Navigate to EDA menu and then exit
        mock_input.side_effect = ['2', '0']  # Enter EDA menu, then exit
        
        with patch('src.interactive.core.InteractiveSystem.safe_input') as mock_safe_input:
            mock_safe_input.return_value = None
            self.system.run()
        
        output = mock_stdout.getvalue()
        assert "EDA ANALYSIS MENU" in output
    
    @patch('builtins.input')
    @patch('sys.stdout', new_callable=StringIO)
    def test_eda_menu_00_command(self, mock_stdout, mock_input):
        """Test "00" command in EDA menu."""
        # Navigate to EDA menu and then exit with "00"
        mock_input.side_effect = ['2', '00']  # Enter EDA menu, then exit with "00"
        
        with patch('src.interactive.core.InteractiveSystem.safe_input') as mock_safe_input:
            mock_safe_input.return_value = None
            self.system.run()
        
        output = mock_stdout.getvalue()
        assert "EDA ANALYSIS MENU" in output
    
    @patch('builtins.input')
    @patch('sys.stdout', new_callable=StringIO)
    def test_eda_menu_exit_text_commands(self, mock_stdout, mock_input):
        """Test text exit commands in EDA menu."""
        # Navigate to EDA menu and then exit with "exit"
        mock_input.side_effect = ['2', 'exit']  # Enter EDA menu, then exit with "exit"
        
        with patch('src.interactive.core.InteractiveSystem.safe_input') as mock_safe_input:
            mock_safe_input.return_value = None
            self.system.run()
        
        output = mock_stdout.getvalue()
        assert "👋 Thank you for using NeoZorK HLD Prediction Interactive System!" in output
        assert "Goodbye!" in output
    
    @patch('builtins.input')
    @patch('sys.stdout', new_callable=StringIO)
    def test_feature_engineering_menu_exit_commands(self, mock_stdout, mock_input):
        """Test exit commands in Feature Engineering menu."""
        # Navigate to Feature Engineering menu and then exit
        mock_input.side_effect = ['3', '0']  # Enter Feature Engineering menu, then exit
        
        with patch('src.interactive.core.InteractiveSystem.safe_input') as mock_safe_input:
            mock_safe_input.return_value = None
            self.system.run()
        
        output = mock_stdout.getvalue()
        assert "FEATURE ENGINEERING MENU" in output
    
    @patch('builtins.input')
    @patch('sys.stdout', new_callable=StringIO)
    def test_feature_engineering_menu_00_command(self, mock_stdout, mock_input):
        """Test "00" command in Feature Engineering menu."""
        # Navigate to Feature Engineering menu and then exit with "00"
        mock_input.side_effect = ['3', '00']  # Enter Feature Engineering menu, then exit with "00"
        
        with patch('src.interactive.core.InteractiveSystem.safe_input') as mock_safe_input:
            mock_safe_input.return_value = None
            self.system.run()
        
        output = mock_stdout.getvalue()
        assert "FEATURE ENGINEERING MENU" in output
    
    @patch('builtins.input')
    @patch('sys.stdout', new_callable=StringIO)
    def test_visualization_menu_exit_commands(self, mock_stdout, mock_input):
        """Test exit commands in Visualization menu."""
        # Navigate to Visualization menu and then exit
        mock_input.side_effect = ['4', '0']  # Enter Visualization menu, then exit
        
        with patch('src.interactive.core.InteractiveSystem.safe_input') as mock_safe_input:
            mock_safe_input.return_value = None
            self.system.run()
        
        output = mock_stdout.getvalue()
        assert "DATA VISUALIZATION MENU" in output
    
    @patch('builtins.input')
    @patch('sys.stdout', new_callable=StringIO)
    def test_visualization_menu_00_command(self, mock_stdout, mock_input):
        """Test "00" command in Visualization menu."""
        # Navigate to Visualization menu and then exit with "00"
        mock_input.side_effect = ['4', '00']  # Enter Visualization menu, then exit with "00"
        
        with patch('src.interactive.core.InteractiveSystem.safe_input') as mock_safe_input:
            mock_safe_input.return_value = None
            self.system.run()
        
        output = mock_stdout.getvalue()
        assert "DATA VISUALIZATION MENU" in output
    
    @patch('builtins.input')
    @patch('sys.stdout', new_callable=StringIO)
    def test_model_development_menu_exit_commands(self, mock_stdout, mock_input):
        """Test exit commands in Model Development menu."""
        # Navigate to Model Development menu and then exit
        mock_input.side_effect = ['5', '0']  # Enter Model Development menu, then exit
        
        with patch('src.interactive.core.InteractiveSystem.safe_input') as mock_safe_input:
            mock_safe_input.return_value = None
            self.system.run()
        
        output = mock_stdout.getvalue()
        assert "MODEL DEVELOPMENT MENU" in output
    
    @patch('builtins.input')
    @patch('sys.stdout', new_callable=StringIO)
    def test_model_development_menu_00_command(self, mock_stdout, mock_input):
        """Test "00" command in Model Development menu."""
        # Navigate to Model Development menu and then exit with "00"
        mock_input.side_effect = ['5', '00']  # Enter Model Development menu, then exit with "00"
        
        with patch('src.interactive.core.InteractiveSystem.safe_input') as mock_safe_input:
            mock_safe_input.return_value = None
            self.system.run()
        
        output = mock_stdout.getvalue()
        assert "MODEL DEVELOPMENT MENU" in output
    
    @patch('builtins.input')
    @patch('sys.stdout', new_callable=StringIO)
    def test_all_menus_exit_text_commands(self, mock_stdout, mock_input):
        """Test text exit commands in all menus."""
        # Test "exit" command in different menus
        test_cases = [
            ('2', 'exit'),  # EDA menu
            ('3', 'exit'),  # Feature Engineering menu
            ('4', 'exit'),  # Visualization menu
            ('5', 'exit'),  # Model Development menu
        ]
        
        for menu_choice, exit_command in test_cases:
            mock_input.side_effect = [menu_choice, exit_command]
            
            with patch('src.interactive.core.InteractiveSystem.safe_input') as mock_safe_input:
                mock_safe_input.return_value = None
                self.system.run()
            
            output = mock_stdout.getvalue()
            assert "👋 Thank you for using NeoZorK HLD Prediction Interactive System!" in output
            assert "Goodbye!" in output
            
            # Reset for next test
            mock_stdout.truncate(0)
            mock_stdout.seek(0)
    
    @patch('builtins.input')
    @patch('sys.stdout', new_callable=StringIO)
    def test_all_menus_quit_commands(self, mock_stdout, mock_input):
        """Test "quit" command in all menus."""
        # Test "quit" command in different menus
        test_cases = [
            ('2', 'quit'),  # EDA menu
            ('3', 'quit'),  # Feature Engineering menu
            ('4', 'quit'),  # Visualization menu
            ('5', 'quit'),  # Model Development menu
        ]
        
        for menu_choice, exit_command in test_cases:
            mock_input.side_effect = [menu_choice, exit_command]
            
            with patch('src.interactive.core.InteractiveSystem.safe_input') as mock_safe_input:
                mock_safe_input.return_value = None
                self.system.run()
            
            output = mock_stdout.getvalue()
            assert "👋 Thank you for using NeoZorK HLD Prediction Interactive System!" in output
            assert "Goodbye!" in output
            
            # Reset for next test
            mock_stdout.truncate(0)
            mock_stdout.seek(0)
    
    @patch('builtins.input')
    @patch('sys.stdout', new_callable=StringIO)
    def test_all_menus_q_commands(self, mock_stdout, mock_input):
        """Test "q" command in all menus."""
        # Test "q" command in different menus
        test_cases = [
            ('2', 'q'),  # EDA menu
            ('3', 'q'),  # Feature Engineering menu
            ('4', 'q'),  # Visualization menu
            ('5', 'q'),  # Model Development menu
        ]
        
        for menu_choice, exit_command in test_cases:
            mock_input.side_effect = [menu_choice, exit_command]
            
            with patch('src.interactive.core.InteractiveSystem.safe_input') as mock_safe_input:
                mock_safe_input.return_value = None
                self.system.run()
            
            output = mock_stdout.getvalue()
            assert "👋 Thank you for using NeoZorK HLD Prediction Interactive System!" in output
            assert "Goodbye!" in output
            
            # Reset for next test
            mock_stdout.truncate(0)
            mock_stdout.seek(0)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
