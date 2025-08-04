"""
Test for Docker terminal mode enforcement in show commands.
"""

import pytest
import os
import sys
from unittest.mock import patch, MagicMock
from src.cli.cli_show_mode import _force_terminal_mode_in_docker


class TestDockerTerminalMode:
    """Test cases for Docker terminal mode enforcement."""

    def test_force_terminal_mode_in_docker_detected(self):
        """Test that terminal mode is forced when Docker is detected."""
        # Mock args object
        args = MagicMock()
        args.draw = 'fastest'
        
        # Mock Docker environment
        with patch.dict(os.environ, {'DOCKER_CONTAINER': 'true'}):
            result = _force_terminal_mode_in_docker(args)
            
            # Should force terminal mode
            assert result is True
            assert args.draw == 'term'

    def test_force_terminal_mode_in_docker_dockerenv(self):
        """Test that terminal mode is forced when /.dockerenv exists."""
        # Mock args object
        args = MagicMock()
        args.draw = 'plotly'
        
        # Mock /.dockerenv file
        with patch('os.path.exists', return_value=True):
            result = _force_terminal_mode_in_docker(args)
            
            # Should force terminal mode
            assert result is True
            assert args.draw == 'term'

    def test_force_terminal_mode_in_docker_already_term(self):
        """Test that terminal mode is not changed when already set to 'term'."""
        # Mock args object
        args = MagicMock()
        args.draw = 'term'
        
        # Mock Docker environment
        with patch.dict(os.environ, {'DOCKER_CONTAINER': 'true'}):
            result = _force_terminal_mode_in_docker(args)
            
            # Should not change the mode
            assert result is True
            assert args.draw == 'term'

    def test_force_terminal_mode_not_in_docker(self):
        """Test that terminal mode is not forced when not in Docker."""
        # Mock args object
        args = MagicMock()
        args.draw = 'fastest'
        
        # Mock non-Docker environment
        with patch.dict(os.environ, {}, clear=True), patch('os.path.exists', return_value=False):
            result = _force_terminal_mode_in_docker(args)
            
            # Should not change the mode
            assert result is False
            assert args.draw == 'fastest'

    def test_force_terminal_mode_docker_detection_disabled(self):
        """Test that terminal mode is not forced when Docker detection is disabled."""
        # Mock args object
        args = MagicMock()
        args.draw = 'fastest'
        
        # Mock Docker environment with disabled detection
        with patch.dict(os.environ, {'DOCKER_CONTAINER': 'true', 'DISABLE_DOCKER_DETECTION': 'true'}):
            result = _force_terminal_mode_in_docker(args)
            
            # Should not change the mode
            assert result is False
            assert args.draw == 'fastest'

    def test_force_terminal_mode_no_draw_attribute(self):
        """Test that terminal mode is forced when no draw attribute exists."""
        # Mock args object without draw attribute
        args = MagicMock()
        del args.draw
        
        # Mock Docker environment
        with patch.dict(os.environ, {'DOCKER_CONTAINER': 'true'}):
            result = _force_terminal_mode_in_docker(args)
            
            # Should force terminal mode
            assert result is True
            assert args.draw == 'term'

    def test_force_terminal_mode_different_modes(self):
        """Test that different draw modes are forced to 'term' in Docker."""
        test_modes = ['fast', 'plotly', 'mpl', 'seaborn', 'sb', 'fastest']
        
        for mode in test_modes:
            # Mock args object
            args = MagicMock()
            args.draw = mode
            
            # Mock Docker environment
            with patch.dict(os.environ, {'DOCKER_CONTAINER': 'true'}):
                result = _force_terminal_mode_in_docker(args)
                
                # Should force terminal mode
                assert result is True
                assert args.draw == 'term', f"Mode {mode} should be forced to 'term'"


if __name__ == "__main__":
    pytest.main([__file__]) 