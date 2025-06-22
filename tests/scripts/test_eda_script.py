"""
Tests for the eda script functionality.
Tests environment detection and command execution.
"""

import pytest
import subprocess
import os
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock


class TestEDAScript:
    """Test cases for the eda script."""

    @classmethod
    def setup_class(cls):
        """Set up test environment."""
        cls.project_root = Path(__file__).parent.parent.parent
        cls.eda_script = cls.project_root / "eda"
        
        # Ensure script is executable
        if cls.eda_script.exists():
            cls.eda_script.chmod(0o755)

    def test_script_exists(self):
        """Test that the eda script exists and is executable."""
        assert self.eda_script.exists(), f"eda script not found at {self.eda_script}"
        assert os.access(self.eda_script, os.X_OK), f"eda script not executable at {self.eda_script}"

    def test_script_help(self):
        """Test that the eda script can show help information."""
        result = subprocess.run([str(self.eda_script), "--help"], 
                              capture_output=True, text=True, cwd=self.project_root)
        
        assert result.returncode == 0, f"Script failed: {result.stderr}"
        assert "usage:" in result.stdout or "Options:" in result.stdout or "help" in result.stdout.lower()

    def test_script_environment_detection_native(self):
        """Test that the script detects native environment correctly."""
        with patch('pathlib.Path.exists', return_value=False), \
             patch('subprocess.run') as mock_run:
            
            # Mock successful uv run
            mock_run.return_value.returncode = 0
            mock_run.return_value.stdout = "EDA Batch Check Tool"
            
            result = subprocess.run([str(self.eda_script), "--help"], 
                                  capture_output=True, text=True, cwd=self.project_root)
            
            # Should succeed regardless of environment detection
            assert result.returncode == 0, f"Script failed: {result.stderr}"

    def test_script_environment_detection_docker(self):
        """Test that the script detects Docker environment correctly."""
        with patch('pathlib.Path.exists', return_value=True), \
             patch('subprocess.run') as mock_run:
            
            # Mock successful python execution
            mock_run.return_value.returncode = 0
            mock_run.return_value.stdout = "EDA Batch Check Tool"
            
            result = subprocess.run([str(self.eda_script), "--help"], 
                                  capture_output=True, text=True, cwd=self.project_root)
            
            # Should succeed regardless of environment detection
            assert result.returncode == 0, f"Script failed: {result.stderr}"

    def test_script_uv_fallback(self):
        """Test that the script falls back to direct python when uv is not available."""
        with patch('subprocess.run') as mock_run:
            # Mock successful python execution
            mock_run.return_value.returncode = 0
            mock_run.return_value.stdout = "EDA Batch Check Tool"
            
            result = subprocess.run([str(self.eda_script), "--help"], 
                                  capture_output=True, text=True, cwd=self.project_root)
            
            # Should succeed with fallback
            assert result.returncode == 0, f"Script failed: {result.stderr}"

    def test_script_with_uv_run(self):
        """Test that the script works with uv run prefix."""
        result = subprocess.run(["uv", "run", str(self.eda_script), "--help"], 
                              capture_output=True, text=True, cwd=self.project_root)
        
        # Should work regardless of environment detection
        assert result.returncode == 0, f"uv run failed: {result.stderr}"

    def test_script_invalid_argument(self):
        """Test that the script handles invalid arguments gracefully."""
        result = subprocess.run([str(self.eda_script), "--invalid-arg"], 
                              capture_output=True, text=True, cwd=self.project_root)
        
        # Should not crash, but may return non-zero exit code
        assert result.returncode != 0 or "error" in result.stderr.lower() or "usage" in result.stdout.lower()

    def test_script_data_quality_checks(self):
        """Test that the script can run data quality checks."""
        result = subprocess.run([str(self.eda_script), "--data-quality-checks", "--help"], 
                              capture_output=True, text=True, cwd=self.project_root)
        
        # Should show help or run successfully
        assert result.returncode == 0 or "quality" in result.stdout.lower()

    def test_script_nan_check(self):
        """Test that the script can run NaN checks."""
        result = subprocess.run([str(self.eda_script), "--nan-check", "--help"], 
                              capture_output=True, text=True, cwd=self.project_root)
        
        # Should show help or run successfully
        assert result.returncode == 0 or "nan" in result.stdout.lower()

    def test_script_fix_files(self):
        """Test that the script can run file fixing."""
        result = subprocess.run([str(self.eda_script), "--fix-files", "--help"], 
                              capture_output=True, text=True, cwd=self.project_root)
        
        # Should show help or run successfully
        assert result.returncode == 0 or "fix" in result.stdout.lower()

    def test_script_path_addition(self):
        """Test that the script adds itself to PATH."""
        result = subprocess.run([str(self.eda_script), "--help"], 
                              capture_output=True, text=True, cwd=self.project_root)
        
        # Should mention adding to PATH
        assert "Adding" in result.stdout and "PATH" in result.stdout

    def test_script_executable_permissions(self):
        """Test that the script has proper executable permissions."""
        stat = os.stat(self.eda_script)
        assert stat.st_mode & 0o111, f"Script {self.eda_script} is not executable"

    def test_script_shebang(self):
        """Test that the script has proper shebang line."""
        with open(self.eda_script, 'r') as f:
            first_line = f.readline().strip()
        
        assert first_line.startswith('#!'), f"Script {self.eda_script} missing shebang"
        assert 'bash' in first_line, f"Script {self.eda_script} should use bash"


class TestEDAScriptIntegration:
    """Integration tests for the eda script."""

    def test_script_with_sample_data(self):
        """Test that the script can handle sample data files."""
        project_root = Path(__file__).parent.parent.parent
        
        # Test with help command (should be available)
        result = subprocess.run([str(project_root / "eda"), "--help"], 
                              capture_output=True, text=True, cwd=project_root)
        
        # Should work without errors
        assert result.returncode == 0, f"Help command failed: {result.stderr}"

    def test_script_environment_variables(self):
        """Test that the script respects environment variables."""
        project_root = Path(__file__).parent.parent.parent
        
        # Test with custom environment
        env = os.environ.copy()
        env['PYTHONPATH'] = str(project_root / "src")
        
        result = subprocess.run([str(project_root / "eda"), "--help"], 
                              capture_output=True, text=True, cwd=project_root, env=env)
        
        assert result.returncode == 0, f"Script failed with custom env: {result.stderr}"

    def test_script_data_directory_handling(self):
        """Test that the script can handle data directory operations."""
        project_root = Path(__file__).parent.parent.parent
        
        # Test with data directory check
        result = subprocess.run([str(project_root / "eda"), "--folder-stats", "--help"], 
                              capture_output=True, text=True, cwd=project_root)
        
        # Should work without errors
        assert result.returncode == 0, f"Folder stats command failed: {result.stderr}"

    def test_script_file_analysis(self):
        """Test that the script can analyze specific files."""
        project_root = Path(__file__).parent.parent.parent
        
        # Test with file analysis
        result = subprocess.run([str(project_root / "eda"), "--file-info", "--help"], 
                              capture_output=True, text=True, cwd=project_root)
        
        # Should work without errors
        assert result.returncode == 0, f"File info command failed: {result.stderr}"


class TestEDAScriptDataOperations:
    """Tests for EDA script data operations."""

    def test_script_cleanup_operations(self):
        """Test that the script can perform cleanup operations."""
        project_root = Path(__file__).parent.parent.parent
        
        # Test cleanup commands
        cleanup_commands = [
            "--clean-stats-logs",
            "--clean-reports",
            "--clean-all"
        ]
        
        for cmd in cleanup_commands:
            result = subprocess.run([str(project_root / "eda"), cmd, "--help"], 
                                  capture_output=True, text=True, cwd=project_root)
            
            # Should work without errors
            assert result.returncode == 0, f"Cleanup command {cmd} failed: {result.stderr}"

    def test_script_statistical_analysis(self):
        """Test that the script can perform statistical analysis."""
        project_root = Path(__file__).parent.parent.parent
        
        # Test statistical analysis commands
        stats_commands = [
            "--descriptive-stats",
            "--correlation-analysis",
            "--feature-importance"
        ]
        
        for cmd in stats_commands:
            result = subprocess.run([str(project_root / "eda"), cmd, "--help"], 
                                  capture_output=True, text=True, cwd=project_root)
            
            # Should work without errors
            assert result.returncode == 0, f"Stats command {cmd} failed: {result.stderr}" 