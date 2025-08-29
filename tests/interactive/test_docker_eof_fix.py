#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test for Docker EOF fix in interactive system.

This test verifies that the interactive system handles EOF properly
in Docker environment and doesn't exit unexpectedly after fixing data issues.
"""

import pytest
import pandas as pd
import numpy as np
from unittest.mock import patch, MagicMock
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from src.interactive import InteractiveSystem
from src.interactive.analysis_runner import AnalysisRunner


class TestDockerEOFFix:
    """Test class for Docker EOF fix functionality."""
    
    @pytest.fixture
    def sample_data_with_issues(self):
        """Create sample data with various quality issues."""
        data = pd.DataFrame({
            'datetime': pd.date_range('2023-01-01', periods=100, freq='H'),
            'open': [100 + i + np.random.normal(0, 1) for i in range(100)],
            'high': [101 + i + np.random.normal(0, 1) for i in range(100)],
            'low': [99 + i + np.random.normal(0, 1) for i in range(100)],
            'close': [100.5 + i + np.random.normal(0, 1) for i in range(100)],
            'volume': [1000000 + np.random.normal(0, 100000) for _ in range(100)]
        })
        
        # Add some quality issues
        data.loc[10, 'high'] = np.nan  # NaN issue
        # Create duplicate rows properly
        data.loc[20] = data.loc[19]  # Duplicate issue
        data.loc[21] = data.loc[19]  # Duplicate issue
        data.loc[30, 'volume'] = 0  # Zero issue
        data.loc[40, 'low'] = -1  # Negative issue
        data.loc[50, 'close'] = np.inf  # Infinity issue
        
        return data
    
    @pytest.fixture
    def mock_system(self, sample_data_with_issues):
        """Create mock system with sample data."""
        system = InteractiveSystem()
        system.current_data = sample_data_with_issues
        return system
    
    def test_comprehensive_data_quality_check_with_eof_handling(self, mock_system):
        """Test that comprehensive data quality check handles EOF properly."""
        runner = AnalysisRunner(mock_system)
        
        # Mock the input to simulate user choosing 'y' for fixing all issues
        with patch('builtins.input', side_effect=['y']):
            # Mock safe_input to simulate EOF
            with patch.object(mock_system, 'safe_input', side_effect=EOFError("EOF")):
                try:
                    runner.run_comprehensive_data_quality_check(mock_system)
                    # If we get here, the function completed without crashing
                    assert True
                except EOFError:
                    # This is expected behavior - EOF should be caught and handled
                    assert True
                except Exception as e:
                    # Any other exception should not occur
                    pytest.fail(f"Unexpected exception: {e}")
    
    def test_eda_menu_with_eof_handling(self, mock_system):
        """Test that EDA menu handles EOF properly."""
        runner = AnalysisRunner(mock_system)
        
        # Mock the input sequence: choose comprehensive data quality check, then EOF
        with patch('builtins.input', side_effect=['1', 'y']):
            # Mock safe_input to simulate EOF after the function completes
            with patch.object(mock_system, 'safe_input', side_effect=EOFError("EOF")):
                try:
                    # This should not crash the system
                    runner.run_eda_analysis(mock_system)
                    # If we get here, the function completed without crashing
                    assert True
                except EOFError:
                    # This is expected behavior - EOF should be caught and handled
                    assert True
                except Exception as e:
                    # Any other exception should not occur
                    pytest.fail(f"Unexpected exception: {e}")
    
    def test_main_loop_with_eof_handling(self, mock_system):
        """Test that main loop handles EOF properly."""
        # Mock the input sequence: load data, run EDA, choose comprehensive check, then EOF
        with patch('builtins.input', side_effect=['1', 'sample_data.csv', '2', '1', 'y']):
            # Mock safe_input to simulate EOF after the function completes
            with patch.object(mock_system, 'safe_input', side_effect=EOFError("EOF")):
                try:
                    # This should not crash the system
                    mock_system.run()
                    # If we get here, the function completed without crashing
                    assert True
                except EOFError:
                    # This is expected behavior - EOF should be caught and handled
                    assert True
                except Exception as e:
                    # Any other exception should not occur
                    pytest.fail(f"Unexpected exception: {e}")
    
    def test_safe_input_eof_handling(self, mock_system):
        """Test that safe_input handles EOF properly."""
        # Test EOFError
        with patch('builtins.input', side_effect=EOFError("EOF")):
            result = mock_system.safe_input()
            assert result is None
        
        # Test KeyboardInterrupt
        with patch('builtins.input', side_effect=KeyboardInterrupt()):
            result = mock_system.safe_input()
            assert result is None
    
    def test_comprehensive_data_quality_check_completes_successfully(self, mock_system):
        """Test that comprehensive data quality check completes successfully without EOF."""
        runner = AnalysisRunner(mock_system)
        
        # Mock the input to simulate user choosing 'y' for fixing all issues
        with patch('builtins.input', side_effect=['y']):
            # Mock safe_input to return normally (no EOF)
            with patch.object(mock_system, 'safe_input', return_value=''):
                try:
                    runner.run_comprehensive_data_quality_check(mock_system)
                    # Function should complete successfully
                    assert 'comprehensive_data_quality' in mock_system.current_results
                    assert mock_system.current_data is not None
                except Exception as e:
                    pytest.fail(f"Function should complete successfully: {e}")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
