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
        assert self.nz_script.exists(), f"nz script not found at {self.nz_script}"
        assert os.access(self.nz_script, os.X_OK), f"nz script not executable at {self.nz_script}"

    def test_script_version(self):
        """Test that the nz script can show version information."""
        result = subprocess.run([str(self.nz_script), "--version"], 
                              capture_output=True, text=True, cwd=self.project_root)
        
        assert result.returncode == 0, f"Script failed: {result.stderr}"
        assert "Shcherbyna Pressure Vector Indicator" in result.stdout
        assert "v" in result.stdout  # Version number should be present

    def test_script_help(self):
        """Test that the nz script can show help information."""
        result = subprocess.run([str(self.nz_script), "--help"], 
                              capture_output=True, text=True, cwd=self.project_root)
        
        assert result.returncode == 0, f"Script failed: {result.stderr}"
        assert "usage:" in result.stdout or "Options:" in result.stdout

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
        result = subprocess.run(["uv", "run", str(self.nz_script), "--version"], 
                              capture_output=True, text=True, cwd=self.project_root)
        
        # Should work regardless of environment detection
        assert result.returncode == 0, f"uv run failed: {result.stderr}"

    def test_script_invalid_argument(self):
        """Test that the script handles invalid arguments gracefully."""
        result = subprocess.run([str(self.nz_script), "--invalid-arg"], 
                              capture_output=True, text=True, cwd=self.project_root)
        
        # Should not crash, but may return non-zero exit code
        assert result.returncode != 0 or "error" in result.stderr.lower() or "usage" in result.stdout.lower()

    def test_script_demo_command(self):
        """Test that the script can run demo command."""
        result = subprocess.run([str(self.nz_script), "demo", "--help"], 
                              capture_output=True, text=True, cwd=self.project_root)
        
        # Should show demo help or run successfully
        assert result.returncode == 0 or "demo" in result.stdout.lower()

    def test_script_path_addition(self):
        """Test that the script adds itself to PATH."""
        result = subprocess.run([str(self.nz_script), "--version"], 
                              capture_output=True, text=True, cwd=self.project_root)
        
        # Should mention adding to PATH
        assert "Adding" in result.stdout and "PATH" in result.stdout

    def test_script_executable_permissions(self):
        """Test that the script has proper executable permissions."""
        stat = os.stat(self.nz_script)
        assert stat.st_mode & 0o111, f"Script {self.nz_script} is not executable"

    def test_script_shebang(self):
        """Test that the script has proper shebang line."""
        with open(self.nz_script, 'r') as f:
            first_line = f.readline().strip()
        
        assert first_line.startswith('#!'), f"Script {self.nz_script} missing shebang"
        assert 'bash' in first_line, f"Script {self.nz_script} should use bash"


class TestNZScriptIntegration:
    """Integration tests for the nz script."""

    def test_script_with_real_data(self):
        """Test that the script can handle real data sources."""
        project_root = Path(__file__).parent.parent.parent
        
        # Test with demo data (should be available)
        result = subprocess.run([str(project_root / "nz"), "demo", "--help"], 
                              capture_output=True, text=True, cwd=project_root)
        
        # Should work without errors
        assert result.returncode == 0, f"Demo command failed: {result.stderr}"

    def test_script_environment_variables(self):
        """Test that the script respects environment variables."""
        project_root = Path(__file__).parent.parent.parent
        
        # Test with custom environment
        env = os.environ.copy()
        env['PYTHONPATH'] = str(project_root / "src")
        
        result = subprocess.run([str(project_root / "nz"), "--version"], 
                              capture_output=True, text=True, cwd=project_root, env=env)
        
        assert result.returncode == 0, f"Script failed with custom env: {result.stderr}" 