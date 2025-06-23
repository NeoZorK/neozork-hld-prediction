"""
Test Docker test runner functionality.

This module contains tests to verify that the Docker-specific
test runner works correctly in containerized environment.
"""

import os
import pytest
import subprocess
import sys
from pathlib import Path


class TestDockerTestRunner:
    """Test Docker test runner functionality."""

    def test_run_tests_docker_exists(self):
        """Test that run_tests_docker.py exists."""
        test_runner_path = Path("tests/run_tests_docker.py")
        assert test_runner_path.exists(), "run_tests_docker.py should exist"
        assert test_runner_path.is_file(), "run_tests_docker.py should be a file"

    def test_run_tests_docker_executable(self):
        """Test that run_tests_docker.py is executable."""
        test_runner_path = Path("tests/run_tests_docker.py")
        
        # Make it executable
        os.chmod(test_runner_path, 0o755)
        
        # Test that it can be executed
        try:
            result = subprocess.run(
                [sys.executable, str(test_runner_path), "--help"],
                capture_output=True,
                text=True,
                timeout=10
            )
            assert result.returncode == 0, "run_tests_docker.py should execute successfully"
        except subprocess.TimeoutExpired:
            pytest.fail("run_tests_docker.py execution timed out")

    def test_run_tests_docker_help(self):
        """Test that run_tests_docker.py shows help."""
        test_runner_path = Path("tests/run_tests_docker.py")
        
        result = subprocess.run(
            [sys.executable, str(test_runner_path), "--help"],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        assert result.returncode == 0, "Help command should succeed"
        assert "Run various test categories in Docker environment" in result.stdout, "Help should contain description"

    def test_run_tests_docker_all_flag(self):
        """Test that --all flag is recognized."""
        test_runner_path = Path("tests/run_tests_docker.py")
        
        result = subprocess.run(
            [sys.executable, str(test_runner_path), "--all"],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        # Should not crash, even if tests fail
        assert result.returncode in [0, 1], "Should exit with 0 or 1"

    def test_run_tests_docker_categories(self):
        """Test that --categories flag is recognized."""
        test_runner_path = Path("tests/run_tests_docker.py")
        
        result = subprocess.run(
            [sys.executable, str(test_runner_path), "--categories", "yfinance"],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        # Should not crash, even if tests fail
        assert result.returncode in [0, 1], "Should exit with 0 or 1"

    def test_run_tests_docker_no_args(self):
        """Test that running without args works."""
        test_runner_path = Path("tests/run_tests_docker.py")
        
        result = subprocess.run(
            [sys.executable, str(test_runner_path)],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        # Should not crash, even if tests fail
        assert result.returncode in [0, 1], "Should exit with 0 or 1"

    def test_required_test_scripts_exist(self):
        """Test that all required test scripts exist."""
        required_scripts = [
            "scripts/debug_scripts/debug_yfinance.py",
            "scripts/debug_scripts/debug_binance.py",
            "scripts/debug_scripts/debug_polygon.py",
            "scripts/debug_scripts/examine_parquet.py",
        ]
        
        for script in required_scripts:
            script_path = Path(script)
            assert script_path.exists(), f"Required test script {script} should exist"
            assert script_path.is_file(), f"Required test script {script} should be a file"

    def test_test_categories_defined(self):
        """Test that test categories are properly defined."""
        # Import the test runner module
        import sys
        sys.path.insert(0, str(Path("tests")))
        
        try:
            import run_tests_docker
            assert hasattr(run_tests_docker, 'TEST_CATEGORIES'), "TEST_CATEGORIES should be defined"
            assert isinstance(run_tests_docker.TEST_CATEGORIES, dict), "TEST_CATEGORIES should be a dict"
            
            expected_categories = ["yfinance", "binance", "polygon", "parquet"]
            for category in expected_categories:
                assert category in run_tests_docker.TEST_CATEGORIES, f"Category {category} should be defined"
                
        except ImportError as e:
            pytest.fail(f"Could not import run_tests_docker: {e}")


class TestDockerTestScripts:
    """Test individual test scripts that are run by the Docker test runner."""

    def test_debug_yfinance_script(self):
        """Test that debug_yfinance.py script exists and is runnable."""
        script_path = Path("scripts/debug_scripts/debug_yfinance.py")
        assert script_path.exists(), "debug_yfinance.py should exist"
        
        # Test that it can be imported (basic syntax check)
        try:
            result = subprocess.run(
                [sys.executable, "-m", "py_compile", str(script_path)],
                capture_output=True,
                text=True,
                timeout=10
            )
            assert result.returncode == 0, "debug_yfinance.py should have valid Python syntax"
        except subprocess.TimeoutExpired:
            pytest.fail("debug_yfinance.py compilation timed out")

    def test_debug_binance_script(self):
        """Test that debug_binance.py script exists and is runnable."""
        script_path = Path("scripts/debug_scripts/debug_binance.py")
        assert script_path.exists(), "debug_binance.py should exist"
        
        # Test that it can be imported (basic syntax check)
        try:
            result = subprocess.run(
                [sys.executable, "-m", "py_compile", str(script_path)],
                capture_output=True,
                text=True,
                timeout=10
            )
            assert result.returncode == 0, "debug_binance.py should have valid Python syntax"
        except subprocess.TimeoutExpired:
            pytest.fail("debug_binance.py compilation timed out")

    def test_debug_polygon_script(self):
        """Test that debug_polygon.py script exists and is runnable."""
        script_path = Path("scripts/debug_scripts/debug_polygon.py")
        assert script_path.exists(), "debug_polygon.py should exist"
        
        # Test that it can be imported (basic syntax check)
        try:
            result = subprocess.run(
                [sys.executable, "-m", "py_compile", str(script_path)],
                capture_output=True,
                text=True,
                timeout=10
            )
            assert result.returncode == 0, "debug_polygon.py should have valid Python syntax"
        except subprocess.TimeoutExpired:
            pytest.fail("debug_polygon.py compilation timed out")

    def test_examine_parquet_script(self):
        """Test that examine_parquet.py script exists and is runnable."""
        script_path = Path("scripts/debug_scripts/examine_parquet.py")
        assert script_path.exists(), "examine_parquet.py should exist"
        
        # Test that it can be imported (basic syntax check)
        try:
            result = subprocess.run(
                [sys.executable, "-m", "py_compile", str(script_path)],
                capture_output=True,
                text=True,
                timeout=10
            )
            assert result.returncode == 0, "examine_parquet.py should have valid Python syntax"
        except subprocess.TimeoutExpired:
            pytest.fail("examine_parquet.py compilation timed out")


if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 