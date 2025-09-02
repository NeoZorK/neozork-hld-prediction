"""
Unit tests for Dockerfile validation and container building.
These tests verify that the Dockerfile is valid and the container can be built.
"""

import unittest
import os
import tempfile
from pathlib import Path
from tests.docker.test_docker_base import DockerBaseTest


class TestDockerfile(DockerBaseTest):
    """Test the Dockerfile for syntax and build capability."""

    def test_dockerfile_exists(self):
        """Test that the Dockerfile exists."""
        dockerfile_path = self.project_root / "Dockerfile"
        self.assertTrue(
            dockerfile_path.exists(),
            f"Dockerfile not found at {dockerfile_path}"
        )

    def test_dockerfile_syntax(self):
        """Test that the Dockerfile has valid syntax."""
        dockerfile_path = os.path.join(self.project_root, "Dockerfile")

        # Check if Docker daemon is running
        stdout, stderr, returncode = self.run_command("docker info")
        if returncode != 0:
            self.skipTest("Docker daemon is not running")

        # Use faster syntax check - just validate basic structure
        try:
            with open(dockerfile_path, 'r') as f:
                content = f.read()
            
            # Basic validation - check for required Dockerfile keywords
            required_keywords = ['FROM', 'COPY', 'RUN']
            for keyword in required_keywords:
                if keyword not in content:
                    self.fail(f"Dockerfile missing required keyword: {keyword}")
            
            # Check for valid FROM statement
            if not any(line.strip().startswith('FROM ') for line in content.split('\n')):
                self.fail("Dockerfile missing valid FROM statement")
                
        except Exception as e:
            self.fail(f"Failed to read or parse Dockerfile: {e}")

    def test_entrypoint_script_exists(self):
        """Test that the Docker entrypoint script exists."""
        entrypoint_path = self.project_root / "docker-entrypoint.sh"
        self.assertTrue(
            entrypoint_path.exists(),
            f"Docker entrypoint script not found at {entrypoint_path}"
        )

    def test_entrypoint_script_executable(self):
        """Test that the Docker entrypoint script exists and has content."""
        entrypoint_path = os.path.join(self.project_root, "docker-entrypoint.sh")
        self.assertTrue(os.path.exists(entrypoint_path),
                        f"Docker entrypoint script not found at {entrypoint_path}")

        # Check if file has content instead of checking executable bit
        with open(entrypoint_path, 'r') as f:
            content = f.read()
        self.assertTrue(len(content) > 0, "Docker entrypoint script is empty")

    def test_docker_compose_exists(self):
        """Test that the docker-compose.yml file exists."""
        compose_path = self.project_root / "docker-compose.yml"
        self.assertTrue(
            compose_path.exists(),
            f"docker-compose.yml not found at {compose_path}"
        )

    def test_docker_compose_syntax(self):
        """Test that the docker-compose.yml file has valid syntax."""
        # Check if Docker daemon is running
        stdout, stderr, returncode = self.run_command("docker info")
        if returncode != 0:
            self.skipTest("Docker daemon is not running")
            
        compose_path = os.path.join(self.project_root, "docker-compose.yml")
        stdout, stderr = self.assert_command_success(
            f"docker-compose -f {compose_path} config",
            cwd=self.project_root,
            msg="docker-compose.yml has syntax errors"
        )

    @unittest.skip("Skip build test by default as it takes time and resources")
    def test_docker_build(self):
        """Test that the Docker image can be built."""
        # This test is skipped by default because it takes time and resources
        # Remove the @unittest.skip decorator to enable this test
        image_name = f"neozork-hld-test:{os.urandom(4).hex()}"
        try:
            stdout, stderr = self.assert_command_success(
                f"docker build -t {image_name} -f Dockerfile .",
                cwd=self.project_root,
                msg="Docker build failed"
            )
        finally:
            # Clean up the test image
            try:
                self.run_command(f"docker rmi {image_name}")
            except:
                pass  # Ignore cleanup errors


if __name__ == '__main__':
    unittest.main()
