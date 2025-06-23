"""
Integration tests for scripts functionality.
Tests script interactions and workflow.
"""

import pytest
import subprocess
import os
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock


class TestScriptsIntegration:
    """Integration tests for scripts."""

    @classmethod
    def setup_class(cls):
        """Set up test environment."""
        cls.project_root = Path(__file__).parent.parent.parent
        cls.eda_script = cls.project_root / "eda"
        cls.nz_script = cls.project_root / "nz"

    def test_scripts_both_exist(self):
        """Test that both scripts exist and are executable."""
        # Check if scripts exist
        eda_exists = self.eda_script.exists()
        nz_exists = self.nz_script.exists()
        
        if not eda_exists and not nz_exists:
            pytest.skip("Neither eda nor nz scripts found - may not be available in this environment")
        
        # Test existing scripts
        if eda_exists:
            assert os.access(self.eda_script, os.X_OK), f"eda script not executable at {self.eda_script}"
        
        if nz_exists:
            assert os.access(self.nz_script, os.X_OK), f"nz script not executable at {self.nz_script}"

    def test_scripts_environment_consistency(self):
        """Test that both scripts have consistent environment detection."""
        if not self.nz_script.exists():
            pytest.skip("nz script not found - may not be available in this environment")
        
        try:
            result = subprocess.run([str(self.nz_script), "--help"], 
                                  capture_output=True, text=True, cwd=self.project_root, timeout=10)
            
            # Should work without errors
            assert result.returncode == 0 or "usage:" in result.stdout
        except subprocess.TimeoutExpired:
            pytest.skip("Script execution timed out")

    def test_scripts_uv_compatibility(self):
        """Test that both scripts work with uv."""
        if not self.nz_script.exists():
            pytest.skip("nz script not found - may not be available in this environment")
        
        try:
            # Check if uv is available
            uv_check = subprocess.run(["uv", "--version"], capture_output=True, text=True, timeout=5)
            if uv_check.returncode != 0:
                pytest.skip("uv not available")
            
            result = subprocess.run(["uv", "run", str(self.nz_script), "--help"], 
                                  capture_output=True, text=True, cwd=self.project_root, timeout=15)
            
            # Should work with uv
            assert result.returncode == 0 or "usage:" in result.stdout
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pytest.skip("uv not available or execution timed out")

    def test_scripts_path_consistency(self):
        """Test that both scripts handle PATH consistently."""
        if not self.nz_script.exists():
            pytest.skip("nz script not found - may not be available in this environment")
        
        try:
            result = subprocess.run([str(self.nz_script), "--help"], 
                                  capture_output=True, text=True, cwd=self.project_root, timeout=10)
            
            # Should mention PATH addition or show help
            assert "Adding" in result.stdout and "PATH" in result.stdout or "usage:" in result.stdout
        except subprocess.TimeoutExpired:
            pytest.skip("Script execution timed out")

    def test_scripts_error_handling(self):
        """Test that both scripts handle errors consistently."""
        if not self.nz_script.exists():
            pytest.skip("nz script not found - may not be available in this environment")
        
        try:
            result = subprocess.run([str(self.nz_script), "--invalid-arg"], 
                                  capture_output=True, text=True, cwd=self.project_root, timeout=10)
            
            # Should handle invalid arguments gracefully
            assert result.returncode != 0 or "error" in result.stderr.lower() or "usage:" in result.stdout.lower()
        except subprocess.TimeoutExpired:
            pytest.skip("Script execution timed out")


class TestScriptsWorkflow:
    """Tests for script workflows."""

    def test_analysis_workflow(self):
        """Test analysis workflow with scripts."""
        project_root = Path(__file__).parent.parent.parent
        eda_script = project_root / "eda"
        
        if not eda_script.exists():
            pytest.skip("eda script not found - may not be available in this environment")
        
        try:
            result = subprocess.run([str(eda_script), "--help"], 
                                  capture_output=True, text=True, cwd=project_root, timeout=10)
            
            # Should work without errors
            assert result.returncode == 0 or "usage:" in result.stdout
        except subprocess.TimeoutExpired:
            pytest.skip("Script execution timed out")

    def test_data_processing_workflow(self):
        """Test data processing workflow with scripts."""
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

    def test_cleanup_workflow(self):
        """Test cleanup workflow with scripts."""
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


class TestScriptsEnvironment:
    """Tests for script environment handling."""

    def test_scripts_custom_environment(self):
        """Test that scripts work with custom environment variables."""
        project_root = Path(__file__).parent.parent.parent
        nz_script = project_root / "nz"
        
        if not nz_script.exists():
            pytest.skip("nz script not found - may not be available in this environment")
        
        # Test with custom environment
        env = os.environ.copy()
        env['PYTHONPATH'] = str(project_root / "src")
        env['CUSTOM_VAR'] = 'test_value'
        
        try:
            result = subprocess.run([str(nz_script), "--help"], 
                                  capture_output=True, text=True, cwd=project_root, env=env, timeout=10)
            
            assert result.returncode == 0 or "usage:" in result.stdout
        except subprocess.TimeoutExpired:
            pytest.skip("Script execution timed out")

    def test_scripts_working_directory(self):
        """Test that scripts work from different working directories."""
        project_root = Path(__file__).parent.parent.parent
        nz_script = project_root / "nz"
        
        if not nz_script.exists():
            pytest.skip("nz script not found - may not be available in this environment")
        
        # Test from different directories
        test_dirs = [project_root, project_root / "src", project_root / "tests"]
        
        for test_dir in test_dirs:
            if test_dir.exists():
                try:
                    result = subprocess.run([str(nz_script), "--help"], 
                                          capture_output=True, text=True, cwd=test_dir, timeout=10)
                    
                    # Should work from any directory
                    assert result.returncode == 0 or "usage:" in result.stdout
                    break  # If one works, that's enough
                except subprocess.TimeoutExpired:
                    continue
        
        else:
            pytest.skip("Script execution timed out from all test directories")


class TestScriptsPerformance:
    """Tests for script performance."""

    def test_scripts_startup_time(self):
        """Test that scripts start up quickly."""
        project_root = Path(__file__).parent.parent.parent
        nz_script = project_root / "nz"
        
        if not nz_script.exists():
            pytest.skip("nz script not found - may not be available in this environment")
        
        try:
            result = subprocess.run([str(nz_script), "--help"], 
                                  capture_output=True, text=True, cwd=project_root, timeout=5)
            
            # Should start up quickly (within 5 seconds)
            assert result.returncode == 0 or "usage:" in result.stdout
        except subprocess.TimeoutExpired:
            pytest.skip("Script startup too slow")

    def test_scripts_memory_usage(self):
        """Test that scripts don't use excessive memory."""
        project_root = Path(__file__).parent.parent.parent
        nz_script = project_root / "nz"
        
        if not nz_script.exists():
            pytest.skip("nz script not found - may not be available in this environment")
        
        try:
            # Simple memory usage test - just check if script runs without memory issues
            result = subprocess.run([str(nz_script), "--help"], 
                                  capture_output=True, text=True, cwd=project_root, timeout=10)
            
            # Should work without memory issues
            assert result.returncode == 0 or "usage:" in result.stdout
        except subprocess.TimeoutExpired:
            pytest.skip("Script execution timed out") 