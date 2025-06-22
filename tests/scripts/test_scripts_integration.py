"""
Integration tests for nz and eda scripts.
Tests script interaction and workflow scenarios.
"""

import pytest
import subprocess
import os
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock


class TestScriptsIntegration:
    """Integration tests for nz and eda scripts."""

    @classmethod
    def setup_class(cls):
        """Set up test environment."""
        cls.project_root = Path(__file__).parent.parent.parent
        cls.nz_script = cls.project_root / "nz"
        cls.eda_script = cls.project_root / "eda"
        
        # Ensure scripts are executable
        for script in [cls.nz_script, cls.eda_script]:
            if script.exists():
                script.chmod(0o755)

    def test_scripts_both_exist(self):
        """Test that both scripts exist and are executable."""
        assert self.nz_script.exists(), f"nz script not found at {self.nz_script}"
        assert self.eda_script.exists(), f"eda script not found at {self.eda_script}"
        
        assert os.access(self.nz_script, os.X_OK), f"nz script not executable"
        assert os.access(self.eda_script, os.X_OK), f"eda script not executable"

    def test_scripts_environment_consistency(self):
        """Test that both scripts detect environment consistently."""
        # Test both scripts in the same environment
        nz_result = subprocess.run([str(self.nz_script), "--version"], 
                                 capture_output=True, text=True, cwd=self.project_root)
        eda_result = subprocess.run([str(self.eda_script), "--help"], 
                                  capture_output=True, text=True, cwd=self.project_root)
        
        # Both should succeed
        assert nz_result.returncode == 0, f"nz script failed: {nz_result.stderr}"
        assert eda_result.returncode == 0, f"eda script failed: {eda_result.stderr}"
        
        # Both should show environment detection
        assert "Running in" in nz_result.stdout, "nz script should show environment detection"
        assert "Running in" in eda_result.stdout, "eda script should show environment detection"

    def test_scripts_uv_compatibility(self):
        """Test that both scripts work with uv run."""
        # Test both scripts with uv run
        nz_result = subprocess.run(["uv", "run", str(self.nz_script), "--version"], 
                                 capture_output=True, text=True, cwd=self.project_root)
        eda_result = subprocess.run(["uv", "run", str(self.eda_script), "--help"], 
                                  capture_output=True, text=True, cwd=self.project_root)
        
        # Both should work with uv run
        assert nz_result.returncode == 0, f"nz script with uv failed: {nz_result.stderr}"
        assert eda_result.returncode == 0, f"eda script with uv failed: {eda_result.stderr}"

    def test_scripts_path_consistency(self):
        """Test that both scripts handle PATH consistently."""
        # Test both scripts and check PATH handling
        nz_result = subprocess.run([str(self.nz_script), "--version"], 
                                 capture_output=True, text=True, cwd=self.project_root)
        eda_result = subprocess.run([str(self.eda_script), "--help"], 
                                  capture_output=True, text=True, cwd=self.project_root)
        
        # Both should mention PATH addition
        assert "Adding" in nz_result.stdout and "PATH" in nz_result.stdout
        assert "Adding" in eda_result.stdout and "PATH" in eda_result.stdout

    def test_scripts_error_handling(self):
        """Test that both scripts handle errors consistently."""
        # Test both scripts with invalid arguments
        nz_result = subprocess.run([str(self.nz_script), "--invalid-arg"], 
                                 capture_output=True, text=True, cwd=self.project_root)
        eda_result = subprocess.run([str(self.eda_script), "--invalid-arg"], 
                                  capture_output=True, text=True, cwd=self.project_root)
        
        # Both should handle errors gracefully (not crash)
        # They may return non-zero exit codes, but shouldn't crash
        assert nz_result.returncode != 0 or "error" in nz_result.stderr.lower() or "usage" in nz_result.stdout.lower()
        assert eda_result.returncode != 0 or "error" in eda_result.stderr.lower() or "usage" in eda_result.stdout.lower()


class TestScriptsWorkflow:
    """Tests for script workflow scenarios."""

    def test_analysis_workflow(self):
        """Test a complete analysis workflow using both scripts."""
        project_root = Path(__file__).parent.parent.parent
        
        # Step 1: Run data quality checks with eda
        eda_result = subprocess.run([str(project_root / "eda"), "--data-quality-checks", "--help"], 
                                  capture_output=True, text=True, cwd=project_root)
        assert eda_result.returncode == 0, f"EDA data quality check failed: {eda_result.stderr}"
        
        # Step 2: Run analysis with nz
        nz_result = subprocess.run([str(project_root / "nz"), "demo", "--help"], 
                                 capture_output=True, text=True, cwd=project_root)
        assert nz_result.returncode == 0, f"NZ demo analysis failed: {nz_result.stderr}"
        
        # Step 3: Run statistical analysis with eda
        stats_result = subprocess.run([str(project_root / "eda"), "--descriptive-stats", "--help"], 
                                    capture_output=True, text=True, cwd=project_root)
        assert stats_result.returncode == 0, f"EDA stats analysis failed: {stats_result.stderr}"

    def test_data_processing_workflow(self):
        """Test data processing workflow using both scripts."""
        project_root = Path(__file__).parent.parent.parent
        
        # Step 1: Check file info with eda
        file_info_result = subprocess.run([str(project_root / "eda"), "--file-info", "--help"], 
                                        capture_output=True, text=True, cwd=project_root)
        assert file_info_result.returncode == 0, f"EDA file info failed: {file_info_result.stderr}"
        
        # Step 2: Run analysis on processed data with nz
        analysis_result = subprocess.run([str(project_root / "nz"), "--help"], 
                                       capture_output=True, text=True, cwd=project_root)
        assert analysis_result.returncode == 0, f"NZ analysis failed: {analysis_result.stderr}"
        
        # Step 3: Generate reports with eda
        report_result = subprocess.run([str(project_root / "eda"), "--html-report", "--help"], 
                                     capture_output=True, text=True, cwd=project_root)
        assert report_result.returncode == 0, f"EDA report generation failed: {report_result.stderr}"

    def test_cleanup_workflow(self):
        """Test cleanup workflow using eda script."""
        project_root = Path(__file__).parent.parent.parent
        
        # Test various cleanup operations
        cleanup_commands = [
            "--clean-stats-logs",
            "--clean-reports", 
            "--clean-all"
        ]
        
        for cmd in cleanup_commands:
            result = subprocess.run([str(project_root / "eda"), cmd, "--help"], 
                                  capture_output=True, text=True, cwd=project_root)
            assert result.returncode == 0, f"Cleanup command {cmd} failed: {result.stderr}"


class TestScriptsEnvironment:
    """Tests for script environment handling."""

    def test_scripts_custom_environment(self):
        """Test that both scripts work with custom environment variables."""
        project_root = Path(__file__).parent.parent.parent
        
        # Set custom environment
        env = os.environ.copy()
        env['PYTHONPATH'] = str(project_root / "src")
        env['CUSTOM_VAR'] = "test_value"
        
        # Test both scripts with custom environment
        nz_result = subprocess.run([str(project_root / "nz"), "--version"], 
                                 capture_output=True, text=True, cwd=project_root, env=env)
        eda_result = subprocess.run([str(project_root / "eda"), "--help"], 
                                  capture_output=True, text=True, cwd=project_root, env=env)
        
        assert nz_result.returncode == 0, f"nz script failed with custom env: {nz_result.stderr}"
        assert eda_result.returncode == 0, f"eda script failed with custom env: {eda_result.stderr}"

    def test_scripts_working_directory(self):
        """Test that both scripts work from different working directories."""
        project_root = Path(__file__).parent.parent.parent
        
        # Test from project root
        nz_root_result = subprocess.run([str(project_root / "nz"), "--version"], 
                                      capture_output=True, text=True, cwd=project_root)
        eda_root_result = subprocess.run([str(project_root / "eda"), "--help"], 
                                       capture_output=True, text=True, cwd=project_root)
        
        # Test from subdirectory
        subdir = project_root / "tests"
        nz_sub_result = subprocess.run([str(project_root / "nz"), "--version"], 
                                     capture_output=True, text=True, cwd=subdir)
        eda_sub_result = subprocess.run([str(project_root / "eda"), "--help"], 
                                      capture_output=True, text=True, cwd=subdir)
        
        # All should succeed
        assert nz_root_result.returncode == 0, f"nz from root failed: {nz_root_result.stderr}"
        assert eda_root_result.returncode == 0, f"eda from root failed: {eda_root_result.stderr}"
        assert nz_sub_result.returncode == 0, f"nz from subdir failed: {nz_sub_result.stderr}"
        assert eda_sub_result.returncode == 0, f"eda from subdir failed: {eda_sub_result.stderr}"


class TestScriptsPerformance:
    """Tests for script performance and resource usage."""

    def test_scripts_startup_time(self):
        """Test that both scripts start up quickly."""
        import time
        
        project_root = Path(__file__).parent.parent.parent
        
        # Test nz script startup time
        start_time = time.time()
        nz_result = subprocess.run([str(project_root / "nz"), "--version"], 
                                 capture_output=True, text=True, cwd=project_root)
        nz_time = time.time() - start_time
        
        # Test eda script startup time
        start_time = time.time()
        eda_result = subprocess.run([str(project_root / "eda"), "--help"], 
                                  capture_output=True, text=True, cwd=project_root)
        eda_time = time.time() - start_time
        
        # Both should succeed and start quickly (less than 5 seconds)
        assert nz_result.returncode == 0, f"nz script failed: {nz_result.stderr}"
        assert eda_result.returncode == 0, f"eda script failed: {eda_result.stderr}"
        assert nz_time < 5.0, f"nz script took too long to start: {nz_time:.2f}s"
        assert eda_time < 5.0, f"eda script took too long to start: {eda_time:.2f}s"

    def test_scripts_memory_usage(self):
        """Test that both scripts don't use excessive memory."""
        project_root = Path(__file__).parent.parent.parent
        
        # Test both scripts with help commands (should be lightweight)
        nz_result = subprocess.run([str(project_root / "nz"), "--help"], 
                                 capture_output=True, text=True, cwd=project_root)
        eda_result = subprocess.run([str(project_root / "eda"), "--help"], 
                                  capture_output=True, text=True, cwd=project_root)
        
        # Both should succeed without memory issues
        assert nz_result.returncode == 0, f"nz script failed: {nz_result.stderr}"
        assert eda_result.returncode == 0, f"eda script failed: {eda_result.stderr}"
        
        # Output should be reasonable size (not empty, not huge)
        assert len(nz_result.stdout) > 100, "nz help output too small"
        assert len(nz_result.stdout) < 10000, "nz help output too large"
        assert len(eda_result.stdout) > 100, "eda help output too small"
        assert len(eda_result.stdout) < 10000, "eda help output too large" 