"""
Test enhanced shell functionality for native container
Tests automatic venv activation and UV setup
"""

import pytest
import subprocess
import os
import tempfile
import shutil
from pathlib import Path


class TestEnhancedShell:
    """Test enhanced shell functionality"""
    
    def test_enhanced_shell_script_exists(self):
        """Test that enhanced shell script is created correctly"""
        exec_script_path = Path("scripts/native-container/exec.sh")
        assert exec_script_path.exists(), "exec.sh script should exist"
        
        # Read script content
        with open(exec_script_path, 'r') as f:
            script_content = f.read()
        
        # Verify script contains expected components
        assert "#!/bin/bash" in script_content
        assert "create_enhanced_shell_command" in script_content
        assert "execute_enhanced_shell" in script_content
        assert "source /app/.venv/bin/activate" in script_content
        assert "uv pip install" in script_content
        assert "alias nz=" in script_content
        assert "alias eda=" in script_content
        assert "alias uv-install=" in script_content
        assert "alias uv-update=" in script_content
        assert "alias uv-test=" in script_content
        assert "alias uv-pytest=" in script_content
    
    def test_enhanced_shell_function_exists(self):
        """Test that enhanced shell function exists in exec.sh"""
        exec_script_path = Path("scripts/native-container/exec.sh")
        
        with open(exec_script_path, 'r') as f:
            script_content = f.read()
        
        # Verify function exists
        assert "execute_enhanced_shell()" in script_content
        assert "create_enhanced_shell_command()" in script_content
    
    def test_shell_mode_uses_enhanced_shell(self):
        """Test that shell mode uses enhanced shell instead of basic bash"""
        exec_script_path = Path("scripts/native-container/exec.sh")
        
        with open(exec_script_path, 'r') as f:
            script_content = f.read()
        
        # Verify that shell mode calls execute_enhanced_shell
        assert "if [ \"$SHELL_MODE\" = true ]; then" in script_content
        assert "execute_enhanced_shell" in script_content
        assert "# Use enhanced shell with automatic venv activation and UV setup" in script_content
    
    def test_enhanced_shell_script_structure(self):
        """Test the structure of the enhanced shell script"""
        exec_script_path = Path("scripts/native-container/exec.sh")
        
        with open(exec_script_path, 'r') as f:
            script_content = f.read()
        
        # Find the create_enhanced_shell_command function
        start_marker = "create_enhanced_shell_command() {"
        end_marker = "}"
        
        start_idx = script_content.find(start_marker)
        assert start_idx != -1, "create_enhanced_shell_command function not found"
        
        # Extract function content (simplified approach)
        function_content = script_content[start_idx:]
        
        # Verify script structure
        assert 'echo "=== NeoZork HLD Prediction Container Shell ==="' in function_content
        assert 'if [ ! -f "/app/requirements.txt" ]' in function_content
        assert 'if ! command -v uv >/dev/null 2>&1' in function_content
        assert 'if [ ! -d "/app/.venv" ]' in function_content
        assert 'source /app/.venv/bin/activate' in function_content
        assert 'uv pip install -r /app/requirements.txt' in function_content
        assert 'export PYTHONPATH="/app:$PYTHONPATH"' in function_content
        assert 'alias nz=' in function_content
        assert 'alias eda=' in function_content
        assert 'alias uv-install=' in function_content
        assert 'alias uv-update=' in function_content
        assert 'alias uv-test=' in function_content
        assert 'alias uv-pytest=' in function_content
        assert 'exec bash' in function_content
    
    def test_help_text_includes_enhanced_features(self):
        """Test that help text includes enhanced shell features"""
        exec_script_path = Path("scripts/native-container/exec.sh")
        
        with open(exec_script_path, 'r') as f:
            script_content = f.read()
        
        # Find the show_available_commands function
        start_marker = "show_available_commands() {"
        end_marker = "}"
        
        start_idx = script_content.find(start_marker)
        assert start_idx != -1, "show_available_commands function not found"
        
        # Extract function content (simplified approach)
        function_content = script_content[start_idx:]
        
        # Verify enhanced features are mentioned
        assert "Enhanced Shell Features" in function_content
        assert "Automatic virtual environment activation" in function_content
        assert "Automatic UV dependency installation" in function_content
        assert "Pre-configured aliases" in function_content
        assert "Environment variables setup" in function_content
        assert "Dependency update checking" in function_content
        assert "uv-pytest" in function_content
        assert "enhanced bash shell" in function_content
    
    def test_usage_includes_enhanced_shell(self):
        """Test that usage text includes enhanced shell description"""
        exec_script_path = Path("scripts/native-container/exec.sh")
        
        with open(exec_script_path, 'r') as f:
            script_content = f.read()
        
        # Find the show_usage function
        start_marker = "show_usage() {"
        end_marker = "}"
        
        start_idx = script_content.find(start_marker)
        assert start_idx != -1, "show_usage function not found"
        
        # Extract function content (simplified approach)
        function_content = script_content[start_idx:]
        
        # Verify enhanced shell is mentioned
        assert "enhanced interactive shell" in function_content
        assert "with venv + UV setup" in function_content
        assert "Enhanced Shell Features" in function_content
        assert "Automatic virtual environment activation" in function_content
        assert "Automatic UV dependency installation and updates" in function_content
        assert "Pre-configured aliases and environment variables" in function_content
        assert "Dependency health checking" in function_content
    
    def test_native_container_script_updated(self):
        """Test that native-container.sh has been updated with enhanced shell info"""
        native_script_path = Path("scripts/native-container/native-container.sh")
        
        with open(native_script_path, 'r') as f:
            script_content = f.read()
        
        # Verify enhanced shell features are mentioned
        assert "enhanced interactive shell" in script_content
        assert "Automatic virtual environment activation" in script_content
        assert "source .venv/bin/activate" in script_content
        assert "Pre-configured aliases" in script_content
        assert "Environment variables setup" in script_content
        assert "Dependency health checking" in script_content
    
    def test_exec_script_syntax_valid(self):
        """Test that exec.sh has valid bash syntax"""
        exec_script_path = Path("scripts/native-container/exec.sh")
        
        # Check if script has executable permissions
        assert os.access(exec_script_path, os.X_OK), "exec.sh should be executable"
        
        # Test bash syntax
        result = subprocess.run(
            ["bash", "-n", str(exec_script_path)],
            capture_output=True,
            text=True
        )
        
        assert result.returncode == 0, f"Bash syntax error in exec.sh: {result.stderr}"
    
    def test_native_container_script_syntax_valid(self):
        """Test that native-container.sh has valid bash syntax"""
        native_script_path = Path("scripts/native-container/native-container.sh")
        
        # Check if script has executable permissions
        assert os.access(native_script_path, os.X_OK), "native-container.sh should be executable"
        
        # Test bash syntax
        result = subprocess.run(
            ["bash", "-n", str(native_script_path)],
            capture_output=True,
            text=True
        )
        
        assert result.returncode == 0, f"Bash syntax error in native-container.sh: {result.stderr}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 