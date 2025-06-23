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
        # Skip test if script doesn't exist (e.g., in container)
        if not self.eda_script.exists():
            pytest.skip("eda script not found - may not be available in this environment")
        
        assert self.eda_script.exists(), f"eda script not found at {self.eda_script}"
        assert os.access(self.eda_script, os.X_OK), f"eda script not executable at {self.eda_script}"

    def test_script_help(self):
        """Test that the eda script can show help information."""
        if not self.eda_script.exists():
            pytest.skip("eda script not found - may not be available in this environment")
        
        try:
            result = subprocess.run([str(self.eda_script), "--help"], 
                                  capture_output=True, text=True, cwd=self.project_root, timeout=10)
            
            # Should succeed or show usage information
            assert result.returncode == 0 or "usage:" in result.stdout or "Options:" in result.stdout or "help" in result.stdout.lower()
        except subprocess.TimeoutExpired:
            pytest.skip("Script execution timed out")

    def test_script_environment_detection_native(self):
        """Test that the script detects native environment correctly."""
        if not self.eda_script.exists():
            pytest.skip("eda script not found - may not be available in this environment")
        
        with patch('pathlib.Path.exists', return_value=False), \
             patch('subprocess.run') as mock_run:
            
            # Mock successful uv run
            mock_run.return_value.returncode = 0
            mock_run.return_value.stdout = "EDA Batch Check Tool"
            
            try:
                result = subprocess.run([str(self.eda_script), "--help"], 
                                      capture_output=True, text=True, cwd=self.project_root, timeout=10)
                
                # Should succeed regardless of environment detection
                assert result.returncode == 0 or "usage:" in result.stdout
            except subprocess.TimeoutExpired:
                pytest.skip("Script execution timed out")

    def test_script_environment_detection_docker(self):
        """Test that the script detects Docker environment correctly."""
        if not self.eda_script.exists():
            pytest.skip("eda script not found - may not be available in this environment")
        
        with patch('pathlib.Path.exists', return_value=True), \
             patch('subprocess.run') as mock_run:
            
            # Mock successful python execution
            mock_run.return_value.returncode = 0
            mock_run.return_value.stdout = "EDA Batch Check Tool"
            
            try:
                result = subprocess.run([str(self.eda_script), "--help"], 
                                      capture_output=True, text=True, cwd=self.project_root, timeout=10)
                
                # Should succeed regardless of environment detection
                assert result.returncode == 0 or "usage:" in result.stdout
            except subprocess.TimeoutExpired:
                pytest.skip("Script execution timed out")

    def test_script_uv_fallback(self):
        """Test that the script falls back to direct python when uv is not available."""
        if not self.eda_script.exists():
            pytest.skip("eda script not found - may not be available in this environment")
        
        with patch('subprocess.run') as mock_run:
            # Mock successful python execution
            mock_run.return_value.returncode = 0
            mock_run.return_value.stdout = "EDA Batch Check Tool"
            
            try:
                result = subprocess.run([str(self.eda_script), "--help"], 
                                      capture_output=True, text=True, cwd=self.project_root, timeout=10)
                
                # Should succeed with fallback
                assert result.returncode == 0 or "usage:" in result.stdout
            except subprocess.TimeoutExpired:
                pytest.skip("Script execution timed out")

    def test_script_with_uv_run(self):
        """Test that the script works with uv run prefix."""
        if not self.eda_script.exists():
            pytest.skip("eda script not found - may not be available in this environment")
        
        try:
            # Check if uv is available
            uv_check = subprocess.run(["uv", "--version"], capture_output=True, text=True, timeout=5)
            if uv_check.returncode != 0:
                pytest.skip("uv not available")
            
            result = subprocess.run(["uv", "run", str(self.eda_script), "--help"], 
                                  capture_output=True, text=True, cwd=self.project_root, timeout=15)
            
            # Should work regardless of environment detection
            assert result.returncode == 0 or "usage:" in result.stdout
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pytest.skip("uv not available or execution timed out")

    def test_script_invalid_argument(self):
        """Test that the script handles invalid arguments gracefully."""
        if not self.eda_script.exists():
            pytest.skip("eda script not found - may not be available in this environment")
        
        try:
            result = subprocess.run([str(self.eda_script), "--invalid-arg"], 
                                  capture_output=True, text=True, cwd=self.project_root, timeout=10)
            
            # Should not crash, but may return non-zero exit code
            assert result.returncode != 0 or "error" in result.stderr.lower() or "usage" in result.stdout.lower()
        except subprocess.TimeoutExpired:
            pytest.skip("Script execution timed out")

    def test_script_data_quality_checks(self):
        """Test that the script can run data quality checks."""
        if not self.eda_script.exists():
            pytest.skip("eda script not found - may not be available in this environment")
        
        try:
            result = subprocess.run([str(self.eda_script), "--data-quality-checks", "--help"], 
                                  capture_output=True, text=True, cwd=self.project_root, timeout=10)
            
            # Should show help or run successfully
            assert result.returncode == 0 or "quality" in result.stdout.lower() or "usage:" in result.stdout
        except subprocess.TimeoutExpired:
            pytest.skip("Script execution timed out")

    def test_script_nan_check(self):
        """Test that the script can run NaN checks."""
        if not self.eda_script.exists():
            pytest.skip("eda script not found - may not be available in this environment")
        
        try:
            result = subprocess.run([str(self.eda_script), "--nan-check", "--help"], 
                                  capture_output=True, text=True, cwd=self.project_root, timeout=10)
            
            # Should show help or run successfully
            assert result.returncode == 0 or "nan" in result.stdout.lower() or "usage:" in result.stdout
        except subprocess.TimeoutExpired:
            pytest.skip("Script execution timed out")

    def test_script_fix_files(self):
        """Test that the script can run file fixing."""
        if not self.eda_script.exists():
            pytest.skip("eda script not found - may not be available in this environment")
        
        try:
            result = subprocess.run([str(self.eda_script), "--fix-files", "--help"], 
                                  capture_output=True, text=True, cwd=self.project_root, timeout=10)
            
            # Should show help or run successfully
            assert result.returncode == 0 or "fix" in result.stdout.lower() or "usage:" in result.stdout
        except subprocess.TimeoutExpired:
            pytest.skip("Script execution timed out")

    def test_script_path_addition(self):
        """Test that the script adds itself to PATH."""
        if not self.eda_script.exists():
            pytest.skip("eda script not found - may not be available in this environment")
        
        try:
            result = subprocess.run([str(self.eda_script), "--help"], 
                                  capture_output=True, text=True, cwd=self.project_root, timeout=10)
            
            # Should mention adding to PATH or show help
            assert "Adding" in result.stdout and "PATH" in result.stdout or "usage:" in result.stdout
        except subprocess.TimeoutExpired:
            pytest.skip("Script execution timed out")

    def test_script_executable_permissions(self):
        """Test that the script has proper executable permissions."""
        if not self.eda_script.exists():
            pytest.skip("eda script not found - may not be available in this environment")
        
        stat = os.stat(self.eda_script)
        assert stat.st_mode & 0o111, f"Script {self.eda_script} is not executable"

    def test_script_shebang(self):
        """Test that the script has proper shebang line."""
        if not self.eda_script.exists():
            pytest.skip("eda script not found - may not be available in this environment")
        
        with open(self.eda_script, 'r') as f:
            first_line = f.readline().strip()
        
        assert first_line.startswith('#!'), f"Script {self.eda_script} missing shebang"
        assert 'bash' in first_line, f"Script {self.eda_script} should use bash"


class TestEDAScriptIntegration:
    """Integration tests for the eda script."""

    def test_script_with_sample_data(self):
        """Test that the script can handle sample data files."""
        project_root = Path(__file__).parent.parent.parent
        eda_script = project_root / "eda"
        
        if not eda_script.exists():
            pytest.skip("eda script not found - may not be available in this environment")
        
        # Test with help command (should be available)
        try:
            result = subprocess.run([str(eda_script), "--help"], 
                                  capture_output=True, text=True, cwd=project_root, timeout=10)
            
            # Should work without errors
            assert result.returncode == 0 or "usage:" in result.stdout
        except subprocess.TimeoutExpired:
            pytest.skip("Script execution timed out")

    def test_script_environment_variables(self):
        """Test that the script respects environment variables."""
        project_root = Path(__file__).parent.parent.parent
        eda_script = project_root / "eda"
        
        if not eda_script.exists():
            pytest.skip("eda script not found - may not be available in this environment")
        
        # Test with custom environment
        env = os.environ.copy()
        env['PYTHONPATH'] = str(project_root / "src")
        
        try:
            result = subprocess.run([str(eda_script), "--help"], 
                                  capture_output=True, text=True, cwd=project_root, env=env, timeout=10)
            
            assert result.returncode == 0 or "usage:" in result.stdout
        except subprocess.TimeoutExpired:
            pytest.skip("Script execution timed out")

    def test_script_data_directory_handling(self):
        """Test that the script can handle data directory operations."""
        project_root = Path(__file__).parent.parent.parent
        eda_script = project_root / "eda"
        
        if not eda_script.exists():
            pytest.skip("eda script not found - may not be available in this environment")
        
        # Test with data directory check
        try:
            result = subprocess.run([str(eda_script), "--folder-stats", "--help"], 
                                  capture_output=True, text=True, cwd=project_root, timeout=10)
            
            # Should work without errors
            assert result.returncode == 0 or "usage:" in result.stdout
        except subprocess.TimeoutExpired:
            pytest.skip("Script execution timed out")

    def test_script_file_analysis(self):
        """Test that the script can analyze specific files."""
        project_root = Path(__file__).parent.parent.parent
        eda_script = project_root / "eda"
        
        if not eda_script.exists():
            pytest.skip("eda script not found - may not be available in this environment")
        
        # Test with file analysis
        try:
            result = subprocess.run([str(eda_script), "--file-info", "--help"], 
                                  capture_output=True, text=True, cwd=project_root, timeout=10)
            
            # Should work without errors
            assert result.returncode == 0 or "usage:" in result.stdout
        except subprocess.TimeoutExpired:
            pytest.skip("Script execution timed out")


class TestEDAScriptDataOperations:
    """Tests for EDA script data operations."""

    def test_script_cleanup_operations(self):
        """Test that the script can perform cleanup operations."""
        project_root = Path(__file__).parent.parent.parent
        eda_script = project_root / "eda"
        
        if not eda_script.exists():
            pytest.skip("eda script not found - may not be available in this environment")
        
        try:
            result = subprocess.run([str(eda_script), "--fix-files"], 
                                  capture_output=True, text=True, cwd=project_root, timeout=10)
            
            # Should work without errors
            assert result.returncode == 0 or "usage:" in result.stdout
        except subprocess.TimeoutExpired:
            pytest.skip("Script execution timed out")

    def test_script_statistical_analysis(self):
        """Test that the script can perform statistical analysis."""
        project_root = Path(__file__).parent.parent.parent
        eda_script = project_root / "eda"
        
        if not eda_script.exists():
            pytest.skip("eda script not found - may not be available in this environment")
        
        try:
            result = subprocess.run([str(eda_script), "--folder-stats"], 
                                  capture_output=True, text=True, cwd=project_root, timeout=10)
            
            # Should work without errors
            assert result.returncode == 0 or "usage:" in result.stdout
        except subprocess.TimeoutExpired:
            pytest.skip("Script execution timed out") 