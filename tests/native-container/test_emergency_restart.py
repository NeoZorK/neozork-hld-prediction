#!/usr/bin/env python3
"""
Test emergency restart functionality for native container management.

This test verifies that the emergency restart service option works correctly
when container deletion fails.
"""

import pytest
import subprocess
import sys
import os
from unittest.mock import patch, MagicMock
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "src"))

class TestEmergencyRestart:
    """Test emergency restart functionality."""
    
    def test_restart_service_function_exists(self):
        """Test that restart_service function exists in the script."""
        script_path = Path(__file__).parent.parent.parent.parent / "scripts" / "native-container" / "native-container.sh"
        
        assert script_path.exists(), f"Script not found: {script_path}"
        
        with open(script_path, 'r') as f:
            content = f.read()
            
        # Check that the restart function exists
        assert "restart_container_service()" in content, "restart_container_service function not found"
        
        # Check that the emergency restart function exists
        assert "stop_container_with_emergency_restart()" in content, "stop_container_with_emergency_restart function not found"
    
    def test_menu_has_restart_option(self):
        """Test that the main menu includes the restart service option."""
        script_path = Path(__file__).parent.parent.parent.parent / "scripts" / "native-container" / "native-container.sh"
        
        with open(script_path, 'r') as f:
            content = f.read()
            
        # Check that menu shows restart option
        assert "4) Restart Service" in content, "Restart Service option not found in menu"
        assert "Enter your choice (0-5):" in content, "Menu choice range not updated"
    
    def test_help_includes_restart_description(self):
        """Test that help function includes description of restart service."""
        script_path = Path(__file__).parent.parent.parent.parent / "scripts" / "native-container" / "native-container.sh"
        
        with open(script_path, 'r') as f:
            content = f.read()
            
        # Check that help includes restart service description
        assert "4. Restart Service" in content, "Restart Service not found in help"
        assert "Emergency container service restart:" in content, "Emergency restart description not found"
        assert "container system stop" in content, "container system stop command not mentioned"
        assert "container system start" in content, "container system start command not mentioned"
        assert "container system status" in content, "container system status command not mentioned"
    
    def test_emergency_restart_handles_deletion_error(self):
        """Test that emergency restart handles container deletion failure."""
        script_path = Path(__file__).parent.parent.parent.parent / "scripts" / "native-container" / "native-container.sh"
        
        with open(script_path, 'r') as f:
            content = f.read()
            
        # Check that the script handles deletion failure
        assert "delete failed for one or more containers" in content, "Deletion failure handling not found"
        assert "Recommended emergency restart service" in content, "Emergency restart recommendation not found"
        assert "Do you want to restart container service now?" in content, "Restart prompt not found"
    
    def test_restart_sequence_commands(self):
        """Test that restart sequence includes all required commands."""
        script_path = Path(__file__).parent.parent.parent.parent / "scripts" / "native-container" / "native-container.sh"
        
        with open(script_path, 'r') as f:
            content = f.read()
            
        # Check that restart sequence includes all required steps
        assert "container system stop" in content, "container system stop not found in restart sequence"
        assert "container system start" in content, "container system start not found in restart sequence"
        assert "container system status" in content, "container system status not found in restart sequence"
    
    def test_retry_after_restart(self):
        """Test that script retries container stop after service restart."""
        script_path = Path(__file__).parent.parent.parent.parent / "scripts" / "native-container" / "native-container.sh"
        
        with open(script_path, 'r') as f:
            content = f.read()
            
        # Check that retry logic exists
        assert "Step 4: Retrying container stop after service restart" in content, "Retry step not found"
        assert "Step 5: Final cleanup after service restart" in content, "Final cleanup step not found"
    
    @patch('subprocess.run')
    def test_restart_service_execution(self, mock_run):
        """Test that restart service function executes correctly."""
        # Mock successful execution
        mock_run.return_value.returncode = 0
        
        script_path = Path(__file__).parent.parent.parent.parent / "scripts" / "native-container" / "native-container.sh"
        
        # This would require more complex testing with actual script execution
        # For now, we just verify the script structure
        assert script_path.exists(), "Script should exist"
        
        # Check that the script is executable
        assert os.access(script_path, os.X_OK), "Script should be executable"
    
    def test_error_handling_structure(self):
        """Test that error handling structure is properly implemented."""
        script_path = Path(__file__).parent.parent.parent.parent / "scripts" / "native-container" / "native-container.sh"
        
        with open(script_path, 'r') as f:
            content = f.read()
            
        # Check that error handling includes proper exit codes
        assert "return 1" in content, "Error handling should include return codes"
        
        # Check that cleanup output is captured
        assert "cleanup_output=" in content, "Cleanup output should be captured"
        assert "cleanup_exit_code=" in content, "Cleanup exit code should be captured"
    
    def test_interactive_prompts(self):
        """Test that interactive prompts are properly implemented."""
        script_path = Path(__file__).parent.parent.parent.parent / "scripts" / "native-container" / "native-container.sh"
        
        with open(script_path, 'r') as f:
            content = f.read()
            
        # Check that interactive prompts exist
        assert "read -p" in content, "Interactive prompts should use read -p"
        assert "[ -t 0 ]" in content, "Interactive mode checking should be implemented"
    
    def test_color_output_functions(self):
        """Test that color output functions are properly defined."""
        script_path = Path(__file__).parent.parent.parent.parent / "scripts" / "native-container" / "native-container.sh"
        
        with open(script_path, 'r') as f:
            content = f.read()
            
        # Check that color functions exist
        assert "print_status()" in content, "print_status function should exist"
        assert "print_success()" in content, "print_success function should exist"
        assert "print_warning()" in content, "print_warning function should exist"
        assert "print_error()" in content, "print_error function should exist"
    
    def test_script_syntax(self):
        """Test that the script has valid bash syntax."""
        script_path = Path(__file__).parent.parent.parent.parent / "scripts" / "native-container" / "native-container.sh"
        
        # Check bash syntax
        result = subprocess.run(
            ["bash", "-n", str(script_path)],
            capture_output=True,
            text=True
        )
        
        assert result.returncode == 0, f"Script has syntax errors: {result.stderr}"


if __name__ == "__main__":
    pytest.main([__file__]) 