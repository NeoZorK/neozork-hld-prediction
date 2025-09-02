"""
Unit tests for Docker configuration and functionality.
Tests in this module verify that the Docker setup works correctly,
including Dockerfile validity, container building, and basic functionality.
"""

import unittest
import subprocess
import os
import sys
import tempfile
from pathlib import Path


class DockerBaseTest(unittest.TestCase):
    """Base class for Docker tests with common utility methods."""

    @classmethod
    def setUpClass(cls):
        """Set up the test environment before any tests run."""
        # Get the project root directory
        cls.project_root = Path(__file__).parent.parent.parent.absolute()

        # Check if Docker is installed and available
        try:
            subprocess.run(
                ["docker", "--version"],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            cls.docker_available = True
        except (subprocess.SubprocessError, FileNotFoundError):
            cls.docker_available = False
            print("Docker is not available. Some tests will be skipped.")

    def setUp(self):
        """Set up before each test."""
        if not self.docker_available:
            self.skipTest("Docker is not available")

    @staticmethod
    def run_command(command, cwd=None):
        """Run a shell command and return stdout, stderr, and return code."""
        process = subprocess.run(
            command,
            shell=True,
            cwd=cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        return process.stdout, process.stderr, process.returncode

    def assert_command_success(self, command, cwd=None, msg=None):
        """Assert that a command runs successfully."""
        stdout, stderr, returncode = self.run_command(command, cwd)
        self.assertEqual(
            returncode, 0,
            msg=msg or f"Command failed: {command}\nStdout: {stdout}\nStderr: {stderr}"
        )
        return stdout, stderr


if __name__ == '__main__':
    unittest.main()
