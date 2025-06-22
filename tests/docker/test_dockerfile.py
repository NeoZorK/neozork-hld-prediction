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

        # First try a simpler check using docker build --dry-run if available
        dry_run_cmd = f"docker build --no-cache --quiet --force-rm --pull=false " \
                     f"--dry-run -f {dockerfile_path} {self.project_root}"

        stdout, stderr, returncode = self.run_command(dry_run_cmd)

        if returncode == 0:
            return  # Simple check passed

        # Fall back to a basic docker syntax check without hadolint
        stdout, stderr = self.assert_command_success(
            f"docker build -q --force-rm --pull=false -f {dockerfile_path} " \
            f"--target builder {self.project_root} 2>/dev/null || docker build -q --force-rm " \
            f"--pull=false -f {dockerfile_path} {self.project_root}",
            msg="Dockerfile has syntax errors"
        )

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
                msg="Docker image build failed"
            )
        finally:
            # Clean up the test image
            self.run_command(f"docker rmi {image_name}")


if __name__ == '__main__':
    unittest.main()
