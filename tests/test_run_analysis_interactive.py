#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test module for run_analysis.py interactive mode functionality.

This module tests the interactive mode flag handling and workflow execution.
"""

import pytest
import sys
from unittest.mock import patch, MagicMock
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.cli.cli import parse_arguments
from src.workflow.workflow import run_indicator_workflow


class TestRunAnalysisInteractive:
    """Test class for run_analysis.py interactive mode."""
    
    def test_parse_arguments_interactive_flag(self):
        """Test that --interactive flag sets mode to interactive."""
        # Test with --interactive flag
        with patch('sys.argv', ['run_analysis.py', '--interactive']):
            args = parse_arguments()
            assert args.interactive is True
            assert args.mode == 'interactive'
    
    def test_parse_arguments_interactive_with_mode(self):
        """Test that --interactive flag works with explicit mode."""
        # Test with --interactive flag and explicit mode
        with patch('sys.argv', ['run_analysis.py', '--interactive', 'demo']):
            args = parse_arguments()
            assert args.interactive is True
            assert args.mode == 'demo'
    
    def test_parse_arguments_no_interactive(self):
        """Test that mode is required when not using --interactive."""
        # Test without --interactive flag
        with patch('sys.argv', ['run_analysis.py', 'demo']):
            args = parse_arguments()
            assert args.interactive is False
            assert args.mode == 'demo'
    
    def test_workflow_interactive_mode(self):
        """Test that workflow handles interactive mode correctly."""
        # Create mock args with interactive flag
        mock_args = MagicMock()
        mock_args.interactive = True
        mock_args.mode = 'interactive'
        
        # Mock InteractiveSystem
        with patch('src.workflow.workflow.InteractiveSystem') as mock_system_class:
            mock_system = MagicMock()
            mock_system_class.return_value = mock_system
            
            # Run workflow
            result = run_indicator_workflow(mock_args)
            
            # Verify interactive system was created and run
            mock_system_class.assert_called_once()
            mock_system.run.assert_called_once()
            
            # Verify result structure
            assert result['success'] is True
            assert result['effective_mode'] == 'interactive'
            assert result['data_source_label'] == 'Interactive mode'
    
    def test_workflow_interactive_mode_error(self):
        """Test that workflow handles interactive mode errors correctly."""
        # Create mock args with interactive flag
        mock_args = MagicMock()
        mock_args.interactive = True
        mock_args.mode = 'interactive'
        
        # Mock InteractiveSystem to raise an error
        with patch('src.workflow.workflow.InteractiveSystem') as mock_system_class:
            mock_system_class.side_effect = Exception("Test error")
            
            # Run workflow
            result = run_indicator_workflow(mock_args)
            
            # Verify result structure for error case
            assert result['success'] is False
            assert result['effective_mode'] == 'interactive'
            assert result['data_source_label'] == 'Interactive mode'
            assert 'Test error' in result['error_message']
    
    def test_workflow_non_interactive_mode(self):
        """Test that workflow handles non-interactive mode correctly."""
        # Create mock args without interactive flag
        mock_args = MagicMock()
        mock_args.interactive = False
        mock_args.mode = 'demo'
        mock_args.rule = 'EMA'
        
        # Mock acquire_data to return test data
        with patch('src.workflow.workflow.acquire_data') as mock_acquire:
            mock_acquire.return_value = {
                'ohlcv_df': MagicMock(),  # Mock DataFrame
                'data_source_label': 'Test Data',
                'rows_count': 10,
                'columns_count': 5,
                'data_size_mb': 0.001
            }
            
            # Mock other dependencies
            with patch('src.workflow.workflow.get_point_size') as mock_point:
                mock_point.return_value = (0.00001, False)
                
                with patch('src.workflow.workflow.calculate_indicator') as mock_calc:
                    mock_calc.return_value = (MagicMock(), 'EMA')
                    
                    with patch('src.workflow.workflow.generate_plot') as mock_plot:
                        # Run workflow
                        result = run_indicator_workflow(mock_args)
                        
                        # Verify that interactive system was not created
                        assert result['effective_mode'] == 'demo'


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
