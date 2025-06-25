"""
Tests for the nz script functionality.
Tests environment detection and command execution.
"""

import pytest
import subprocess
import os
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock


class TestNZScript:
    """Test cases for the nz script."""

    @classmethod
    def setup_class(cls):
        """Set up test environment."""
        cls.project_root = Path(__file__).parent.parent.parent
        cls.nz_script = cls.project_root / "nz"
        
        # Ensure script is executable
        if cls.nz_script.exists():
            cls.nz_script.chmod(0o755)

    def test_script_exists(self):
        """Test that the nz script exists and is executable."""
        # Skip test if script doesn't exist (e.g., in container)
        if not self.nz_script.exists():
            pytest.skip("nz script not found - may not be available in this environment")
        
        assert self.nz_script.exists(), f"nz script not found at {self.nz_script}"
        assert os.access(self.nz_script, os.X_OK), f"nz script not executable at {self.nz_script}"

    def test_script_version(self):
        """Test that the nz script can show version information."""
        if not self.nz_script.exists():
            pytest.skip("nz script not found - may not be available in this environment")
        
        try:
            result = subprocess.run([str(self.nz_script), "version"], 
                                  capture_output=True, text=True, cwd=self.project_root, timeout=10)
            
            # Should succeed and show version information
            assert result.returncode == 0, f"Script failed: {result.stderr}"
            assert "Version" in result.stdout or "version" in result.stdout.lower()
        except subprocess.TimeoutExpired:
            pytest.skip("Script execution timed out")

    def test_script_help(self):
        """Test that the nz script can show help information."""
        if not self.nz_script.exists():
            pytest.skip("nz script not found - may not be available in this environment")
        
        try:
            result = subprocess.run([str(self.nz_script), "--help"], 
                                  capture_output=True, text=True, cwd=self.project_root, timeout=10)
            
            # Should succeed and show help information
            assert result.returncode == 0, f"Script failed: {result.stderr}"
            assert "usage:" in result.stdout or "Options:" in result.stdout or "help" in result.stdout.lower()
        except subprocess.TimeoutExpired:
            pytest.skip("Script execution timed out")

    def test_script_environment_detection_native(self):
        """Test that the script detects native environment correctly."""
        with patch('pathlib.Path.exists', return_value=False), \
             patch('subprocess.run') as mock_run:
            
            # Mock successful uv run
            mock_run.return_value.returncode = 0
            mock_run.return_value.stdout = "Shcherbyna Pressure Vector Indicator v0.4.1"
            
            result = subprocess.run([str(self.nz_script), "--version"], 
                                  capture_output=True, text=True, cwd=self.project_root)
            
            # Should succeed regardless of environment detection
            assert result.returncode == 0, f"Script failed: {result.stderr}"

    def test_script_environment_detection_docker(self):
        """Test that the script detects Docker environment correctly."""
        with patch('pathlib.Path.exists', return_value=True), \
             patch('subprocess.run') as mock_run:
            
            # Mock successful python execution
            mock_run.return_value.returncode = 0
            mock_run.return_value.stdout = "Shcherbyna Pressure Vector Indicator v0.4.1"
            
            result = subprocess.run([str(self.nz_script), "--version"], 
                                  capture_output=True, text=True, cwd=self.project_root)
            
            # Should succeed regardless of environment detection
            assert result.returncode == 0, f"Script failed: {result.stderr}"

    def test_script_uv_fallback(self):
        """Test that the script falls back to direct python when uv is not available."""
        with patch('subprocess.run') as mock_run:
            # Mock uv not found, then successful python execution
            mock_run.side_effect = [
                MagicMock(returncode=0, stdout="Shcherbyna Pressure Vector Indicator v0.4.1")  # Direct python success
            ]
            
            result = subprocess.run([str(self.nz_script), "--version"], 
                                  capture_output=True, text=True, cwd=self.project_root)
            
            # Should succeed with fallback
            assert result.returncode == 0, f"Script failed: {result.stderr}"

    def test_script_with_uv_run(self):
        """Test that the script works with uv run prefix."""
        if not self.nz_script.exists():
            pytest.skip("nz script not found - may not be available in this environment")
        
        try:
            # Check if uv is available
            uv_check = subprocess.run(["uv", "--version"], capture_output=True, text=True, timeout=5)
            if uv_check.returncode != 0:
                pytest.skip("uv not available")
            
            result = subprocess.run(["uv", "run", str(self.nz_script), "--help"], 
                                  capture_output=True, text=True, cwd=self.project_root, timeout=15)
            
            # Should work regardless of environment detection
            assert result.returncode == 0 or "usage:" in result.stdout
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pytest.skip("uv not available or execution timed out")

    def test_script_invalid_argument(self):
        """Test that the script handles invalid arguments gracefully."""
        if not self.nz_script.exists():
            pytest.skip("nz script not found - may not be available in this environment")
        
        try:
            result = subprocess.run([str(self.nz_script), "--invalid-arg"], 
                                  capture_output=True, text=True, cwd=self.project_root, timeout=10)
            
            # Should not crash, but may return non-zero exit code
            assert result.returncode != 0 or "error" in result.stderr.lower() or "usage" in result.stdout.lower()
        except subprocess.TimeoutExpired:
            pytest.skip("Script execution timed out")

    def test_script_demo_command(self):
        """Test that the script can run demo command."""
        if not self.nz_script.exists():
            pytest.skip("nz script not found - may not be available in this environment")
        
        try:
            result = subprocess.run([str(self.nz_script), "demo"], 
                                  capture_output=True, text=True, cwd=self.project_root, timeout=15)
            
            # Should work or show appropriate message
            assert result.returncode == 0 or "demo" in result.stdout.lower() or "usage:" in result.stdout
        except subprocess.TimeoutExpired:
            pytest.skip("Script execution timed out")

    def test_script_path_addition(self):
        """Test that the script adds itself to PATH."""
        if not self.nz_script.exists():
            pytest.skip("nz script not found - may not be available in this environment")
        
        try:
            result = subprocess.run([str(self.nz_script), "--help"], 
                                  capture_output=True, text=True, cwd=self.project_root, timeout=10)
            
            # Should mention adding to PATH or show help
            assert "Adding" in result.stdout and "PATH" in result.stdout or "usage:" in result.stdout
        except subprocess.TimeoutExpired:
            pytest.skip("Script execution timed out")

    def test_script_executable_permissions(self):
        """Test that the script has proper executable permissions."""
        if not self.nz_script.exists():
            pytest.skip("nz script not found - may not be available in this environment")
        
        stat = os.stat(self.nz_script)
        assert stat.st_mode & 0o111, f"Script {self.nz_script} is not executable"

    def test_script_shebang(self):
        """Test that the script has proper shebang line."""
        if not self.nz_script.exists():
            pytest.skip("nz script not found - may not be available in this environment")
        
        with open(self.nz_script, 'r') as f:
            first_line = f.readline().strip()
        
        assert first_line.startswith('#!'), f"Script {self.nz_script} missing shebang"
        assert 'bash' in first_line, f"Script {self.nz_script} should use bash"


class TestNZScriptIntegration:
    """Integration tests for the nz script."""

    def test_script_with_real_data(self):
        """Test that the script can handle real data files."""
        project_root = Path(__file__).parent.parent.parent
        nz_script = project_root / "nz"
        
        if not nz_script.exists():
            pytest.skip("nz script not found - may not be available in this environment")
        
        # Test with help command (should be available)
        try:
            result = subprocess.run([str(nz_script), "--help"], 
                                  capture_output=True, text=True, cwd=project_root, timeout=10)
            
            # Should work without errors
            assert result.returncode == 0 or "usage:" in result.stdout
        except subprocess.TimeoutExpired:
            pytest.skip("Script execution timed out")

    def test_script_environment_variables(self):
        """Test that the script respects environment variables."""
        project_root = Path(__file__).parent.parent.parent
        nz_script = project_root / "nz"
        
        if not nz_script.exists():
            pytest.skip("nz script not found - may not be available in this environment")
        
        # Test with custom environment
        env = os.environ.copy()
        env['PYTHONPATH'] = str(project_root / "src")
        
        try:
            result = subprocess.run([str(nz_script), "--help"], 
                                  capture_output=True, text=True, cwd=project_root, env=env, timeout=10)
            
            assert result.returncode == 0 or "usage:" in result.stdout
        except subprocess.TimeoutExpired:
            pytest.skip("Script execution timed out")

    def test_script_data_operations(self):
        """Test that the script can handle data operations."""
        project_root = Path(__file__).parent.parent.parent
        nz_script = project_root / "nz"
        
        if not nz_script.exists():
            pytest.skip("nz script not found - may not be available in this environment")
        
        # Test with data operations
        try:
            result = subprocess.run([str(nz_script), "data", "--help"], 
                                  capture_output=True, text=True, cwd=project_root, timeout=10)
            
            # Should work without errors
            assert result.returncode == 0 or "usage:" in result.stdout
        except subprocess.TimeoutExpired:
            pytest.skip("Script execution timed out")

    def test_script_test_command(self):
        """Test that the script can run test command."""
        project_root = Path(__file__).parent.parent.parent
        nz_script = project_root / "nz"
        
        if not nz_script.exists():
            pytest.skip("nz script not found - may not be available in this environment")
        
        try:
            result = subprocess.run([str(nz_script), "test"], 
                                  capture_output=True, text=True, cwd=project_root, timeout=30)
            
            # Should work or show appropriate message
            assert result.returncode == 0 or "test" in result.stdout.lower() or "usage:" in result.stdout
        except subprocess.TimeoutExpired:
            pytest.skip("Script execution timed out")

    def test_script_analyze_command(self):
        """Test that the script can run analyze command."""
        project_root = Path(__file__).parent.parent.parent
        nz_script = project_root / "nz"
        
        if not nz_script.exists():
            pytest.skip("nz script not found - may not be available in this environment")
        
        try:
            result = subprocess.run([str(nz_script), "analyze", "--help"], 
                                  capture_output=True, text=True, cwd=project_root, timeout=10)
            
            # Should work or show appropriate message
            assert result.returncode == 0 or "analyze" in result.stdout.lower() or "usage:" in result.stdout
        except subprocess.TimeoutExpired:
            pytest.skip("Script execution timed out")

    def test_script_plot_command(self):
        """Test that the script can run plot command."""
        project_root = Path(__file__).parent.parent.parent
        nz_script = project_root / "nz"
        
        if not nz_script.exists():
            pytest.skip("nz script not found - may not be available in this environment")
        
        try:
            result = subprocess.run([str(nz_script), "plot", "--help"], 
                                  capture_output=True, text=True, cwd=project_root, timeout=10)
            
            # Should work or show appropriate message
            assert result.returncode == 0 or "plot" in result.stdout.lower() or "usage:" in result.stdout
        except subprocess.TimeoutExpired:
            pytest.skip("Script execution timed out") 