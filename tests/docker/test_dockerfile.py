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
        dockerfile_path = self.project_root / "docker" / "Dockerfile"
        self.assertTrue(
            dockerfile_path.exists(),
            f"Dockerfile not found at {dockerfile_path}"
        )

    def test_dockerfile_syntax(self):
        """Test that the Dockerfile has valid syntax."""
        dockerfile_path = os.path.join(self.project_root, "docker", "Dockerfile")
        stdout, stderr = self.assert_command_success(
            f"docker run --rm -v {dockerfile_path}:/Dockerfile hadolint/hadolint hadolint /Dockerfile",
            msg="Dockerfile has syntax errors"
        )

    def test_entrypoint_script_exists(self):
        """Test that the Docker entrypoint script exists."""
        entrypoint_path = self.project_root / "docker" / "docker-entrypoint.sh"
        self.assertTrue(
            entrypoint_path.exists(),
            f"Docker entrypoint script not found at {entrypoint_path}"
        )

    def test_entrypoint_script_executable(self):
        """Test that the Docker entrypoint script is executable."""
        entrypoint_path = os.path.join(self.project_root, "docker", "docker-entrypoint.sh")
        stdout, stderr = self.assert_command_success(
            f"test -x {entrypoint_path}",
            msg="Docker entrypoint script is not executable"
        )

    def test_docker_compose_exists(self):
        """Test that the docker-compose.yml file exists."""
        compose_path = self.project_root / "docker-compose.yml"
        self.assertTrue(
            compose_path.exists(),
            f"docker-compose.yml not found at {compose_path}"
        )

    def test_docker_compose_syntax(self):
        """Test that the docker-compose.yml file has valid syntax."""
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
                f"docker build -t {image_name} -f docker/Dockerfile .",
                cwd=self.project_root,
                msg="Docker image build failed"
            )
        finally:
            # Clean up the test image
            self.run_command(f"docker rmi {image_name}")


if __name__ == '__main__':
    unittest.main()
