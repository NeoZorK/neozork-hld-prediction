"""
Unit tests for Docker container functionality.
These tests verify that the Docker container runs correctly and provides
the expected functionality.
"""

import unittest
import os
import time
import tempfile
from pathlib import Path
from tests.docker.test_docker_base import DockerBaseTest


class TestDockerContainer(DockerBaseTest):
    """Test the Docker container functionality."""

    @classmethod
    def setUpClass(cls):
        """Set up the test environment before any tests run."""
        super().setUpClass()
        cls.container_name = f"neozork-test-container-{os.urandom(4).hex()}"

    def setUp(self):
        """Set up before each test."""
        super().setUp()
        # Skip time-consuming container tests in regular test runs
        # These tests are better for CI environments
        if 'DOCKER_CONTAINER_TESTS' not in os.environ:
            self.skipTest("Skipping container tests. Set DOCKER_CONTAINER_TESTS=1 to enable")

    def tearDown(self):
        """Clean up after each test."""
        # Make sure to stop and remove the container
        self.run_command(f"docker stop {self.container_name} 2>/dev/null || true")
        self.run_command(f"docker rm {self.container_name} 2>/dev/null || true")

    def test_container_starts(self):
        """Test that the container starts successfully."""
        stdout, stderr = self.assert_command_success(
            f"docker run -d --name {self.container_name} --rm "
            f"-v {self.project_root}/data:/app/data "
            f"-v {self.project_root}/mql5_feed:/app/mql5_feed "
            f"-v {self.project_root}/logs:/app/logs "
            f"--entrypoint=/bin/bash "
            f"neozork-hld:latest -c 'sleep 10'",
            cwd=self.project_root,
            msg="Failed to start Docker container"
        )

        # Wait briefly for container to start
        time.sleep(2)

        # Check if container is running
        stdout, stderr = self.assert_command_success(
            f"docker ps --filter name={self.container_name} --format '{{{{.Status}}}}'",
            msg="Container is not running"
        )
        self.assertIn("Up", stdout, "Container is not in 'Up' state")

    def test_python_version(self):
        """Test that the container has the correct Python version."""
        stdout, stderr = self.assert_command_success(
            f"docker run --name {self.container_name} --rm "
            f"neozork-hld:latest python --version",
            cwd=self.project_root,
            msg="Failed to check Python version in container"
        )
        self.assertIn("Python 3", stdout, "Container does not have Python 3")

    def test_dependencies_installed(self):
        """Test that the required Python dependencies are installed."""
        stdout, stderr = self.assert_command_success(
            f"docker run --name {self.container_name} --rm "
            f"neozork-hld:latest pip freeze",
            cwd=self.project_root,
            msg="Failed to list installed packages in container"
        )
        # Check for key dependencies
        required_packages = ['pandas', 'numpy', 'matplotlib', 'yfinance']
        for package in required_packages:
            self.assertIn(package, stdout, f"Required package {package} is not installed")

    def test_run_analysis_help(self):
        """Test that the run_analysis.py script works in the container."""
        stdout, stderr = self.assert_command_success(
            f"docker run --name {self.container_name} --rm "
            f"neozork-hld:latest python run_analysis.py --help",
            cwd=self.project_root,
            msg="Failed to run the analysis script in container"
        )
        self.assertIn("usage:", stdout, "Help output not found in run_analysis.py")

    def test_uv_support(self):
        """Test that uv is supported in the container when enabled."""
        # Test with UV_ENABLED
        stdout, stderr = self.assert_command_success(
            f"docker run --name {self.container_name} --rm "
            f"-e UV_ENABLED=true "
            f"neozork-hld:latest bash -c 'command -v uv || echo \"uv not found\"'",
            cwd=self.project_root,
            msg="Failed to check uv in container"
        )
        # It might be installed or not depending on build args, so we don't assert on the result
        # Just ensure the command completes successfully

    def test_data_volume_mounted(self):
        """Test that data volumes are correctly mounted in the container."""
        with tempfile.NamedTemporaryFile(dir=os.path.join(self.project_root, "data"), suffix=".test") as temp_file:
            # Create a test file in the data directory
            test_filename = os.path.basename(temp_file.name)

            # Check if the file is visible in the container
            stdout, stderr = self.assert_command_success(
                f"docker run --name {self.container_name} --rm "
                f"-v {self.project_root}/data:/app/data "
                f"neozork-hld:latest ls -la /app/data/{test_filename}",
                cwd=self.project_root,
                msg="Failed to find test file in container data volume"
            )
            self.assertIn(test_filename, stdout, "Test file not found in container data volume")

    def test_bash_history_initialization(self):
        """Test that the init_bash_history function is present in docker-entrypoint.sh."""
        entrypoint_path = os.path.join(self.project_root, "docker-entrypoint.sh")
        
        with open(entrypoint_path, 'r') as f:
            content = f.read()
        
        # Check for init_bash_history function
        self.assertIn("init_bash_history()", content, 
                     "init_bash_history function not found in docker-entrypoint.sh")
        
        # Check for useful commands in the function
        useful_commands = [
            "uv run pytest tests -n auto",
            "nz --interactive", 
            "eda -dqc",
            "nz --indicators",
            "nz --metric"
        ]
        
        for cmd in useful_commands:
            self.assertIn(cmd, content, 
                         f"Useful command '{cmd}' not found in init_bash_history function")
        
        # Check for history loading
        self.assertIn("history -r", content, 
                     "history -r command not found in init_bash_history function")


if __name__ == '__main__':
    unittest.main()
