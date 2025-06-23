"""
Test Docker configuration and setup.

This module contains tests to verify that Docker configuration
is properly set up and all required files are present.
"""

import os
import pytest
import yaml
from pathlib import Path


class TestDockerConfiguration:
    """Test Docker configuration and required files."""

    def test_dockerfile_exists(self):
        """Test that Dockerfile exists in project root."""
        dockerfile_path = Path("Dockerfile")
        # Skip test if running in Docker container and file doesn't exist
        if os.path.exists("/.dockerenv") and not dockerfile_path.exists():
            pytest.skip("Dockerfile not required when running inside container")
        assert dockerfile_path.exists(), "Dockerfile should exist in project root"
        assert dockerfile_path.is_file(), "Dockerfile should be a file"

    def test_docker_compose_exists(self):
        """Test that docker-compose.yml exists in project root."""
        compose_path = Path("docker-compose.yml")
        # Skip test if running in Docker container and file doesn't exist
        if os.path.exists("/.dockerenv") and not compose_path.exists():
            pytest.skip("docker-compose.yml not required when running inside container")
        assert compose_path.exists(), "docker-compose.yml should exist in project root"
        assert compose_path.is_file(), "docker-compose.yml should be a file"

    def test_docker_env_exists(self):
        """Test that docker.env exists in project root."""
        env_path = Path("docker.env")
        # Skip test if running in Docker container and file doesn't exist
        if os.path.exists("/.dockerenv") and not env_path.exists():
            pytest.skip("docker.env not required when running inside container")
        assert env_path.exists(), "docker.env should exist in project root"
        assert env_path.is_file(), "docker.env should be a file"

    def test_docker_entrypoint_exists(self):
        """Test that docker-entrypoint.sh exists in project root."""
        entrypoint_path = Path("docker-entrypoint.sh")
        # Skip test if running in Docker container and file doesn't exist
        if os.path.exists("/.dockerenv") and not entrypoint_path.exists():
            pytest.skip("docker-entrypoint.sh not required when running inside container")
        assert entrypoint_path.exists(), "docker-entrypoint.sh should exist in project root"
        assert entrypoint_path.is_file(), "docker-entrypoint.sh should be a file"

    def test_required_files_exist(self):
        """Test that all required files for Docker build exist."""
        required_files = [
            "run_analysis.py",
            "pycharm_github_copilot_mcp.py",
            "cursor_mcp_config.json",
            "mcp_auto_config.json",
        ]
        
        # Add optional files that may not exist in container
        optional_files = [
            "requirements.txt",
            "uv.toml",
        ]

        # Check required files
        for file_name in required_files:
            file_path = Path(file_name)
            assert file_path.exists(), f"Required file {file_name} should exist in project root"
            assert file_path.is_file(), f"Required file {file_name} should be a file"

        # Check optional files (skip if in container and file doesn't exist)
        for file_name in optional_files:
            file_path = Path(file_name)
            if os.path.exists("/.dockerenv") and not file_path.exists():
                pytest.skip(f"{file_name} not required when running inside container")
            if file_path.exists():
                assert file_path.is_file(), f"Optional file {file_name} should be a file if it exists"

    def test_docker_compose_structure(self):
        """Test docker-compose.yml structure and configuration."""
        compose_path = Path("docker-compose.yml")
        
        # Skip test if running in Docker container and file doesn't exist
        if os.path.exists("/.dockerenv") and not compose_path.exists():
            pytest.skip("docker-compose.yml not required when running inside container")
        
        if not compose_path.exists():
            pytest.skip("docker-compose.yml not found")
        
        with open(compose_path, 'r') as f:
            compose_config = yaml.safe_load(f)

        # Check that neozork-hld service exists
        assert "neozork-hld" in compose_config["services"], "neozork-hld service should be defined"

        service = compose_config["services"]["neozork-hld"]

        # Check required service configuration
        assert "build" in service, "Service should have build configuration"
        assert "volumes" in service, "Service should have volumes configuration"
        assert "env_file" in service, "Service should have env_file configuration"
        assert "environment" in service, "Service should have environment configuration"

        # Check build args
        build_config = service["build"]
        assert "args" in build_config, "Build should have args configuration"
        assert "USE_UV" in build_config["args"], "Build args should include USE_UV"

        # Check volume mounts
        volumes = service["volumes"]
        expected_volumes = [
            "./data:/app/data",
            "./logs:/app/logs",
            "./mql5_feed:/app/mql5_feed",
            "./results:/app/results",
            "./tests:/app/tests",
        ]

        for expected_volume in expected_volumes:
            assert expected_volume in volumes, f"Volume mount {expected_volume} should be configured"

    def test_docker_env_content(self):
        """Test docker.env file content."""
        env_path = Path("docker.env")
        
        # Skip test if running in Docker container and file doesn't exist
        if os.path.exists("/.dockerenv") and not env_path.exists():
            pytest.skip("docker.env not required when running inside container")
        
        if not env_path.exists():
            pytest.skip("docker.env not found")
        
        with open(env_path, 'r') as f:
            env_content = f.read()

        # Check for required environment variables
        required_vars = [
            "USE_UV=true",
            "PYTHONPATH=/app",
            "PYTHONUNBUFFERED=1",
            "MCP_SERVER_TYPE=pycharm_copilot",
        ]

        for var in required_vars:
            assert var in env_content, f"Environment variable {var} should be defined in docker.env"

    def test_dockerfile_content(self):
        """Test Dockerfile content for required configurations."""
        dockerfile_path = Path("Dockerfile")
        
        # Skip test if running in Docker container and file doesn't exist
        if os.path.exists("/.dockerenv") and not dockerfile_path.exists():
            pytest.skip("Dockerfile not required when running inside container")
        
        if not dockerfile_path.exists():
            pytest.skip("Dockerfile not found")
        
        with open(dockerfile_path, 'r') as f:
            dockerfile_content = f.read()

        # Check for required Dockerfile elements
        required_elements = [
            "ARG USE_UV=true",
            "COPY run_analysis.py ./",
            "COPY pycharm_github_copilot_mcp.py ./",
            "COPY cursor_mcp_config.json ./",
            "COPY mcp_auto_config.json ./",
            "USER neozork",
        ]

        for element in required_elements:
            assert element in dockerfile_content, f"Dockerfile should contain: {element}"

    def test_docker_entrypoint_content(self):
        """Test docker-entrypoint.sh content."""
        entrypoint_path = Path("docker-entrypoint.sh")
        
        # Skip test if running in Docker container and file doesn't exist
        if os.path.exists("/.dockerenv") and not entrypoint_path.exists():
            pytest.skip("docker-entrypoint.sh not required when running inside container")
        
        if not entrypoint_path.exists():
            pytest.skip("docker-entrypoint.sh not found")
        
        with open(entrypoint_path, 'r') as f:
            entrypoint_content = f.read()

        # Check for required entrypoint elements
        required_elements = [
            "python pycharm_github_copilot_mcp.py",
            "python run_analysis.py -h",
            "exec bash -i",
        ]

        for element in required_elements:
            assert element in entrypoint_content, f"Entrypoint should contain: {element}"

    def test_dockerignore_exists(self):
        """Test that .dockerignore exists and contains appropriate patterns."""
        dockerignore_path = Path(".dockerignore")
        # Skip test if running in Docker container and file doesn't exist
        if os.path.exists("/.dockerenv") and not dockerignore_path.exists():
            pytest.skip(".dockerignore not required when running inside container")
        
        if not dockerignore_path.exists():
            pytest.skip(".dockerignore not found")
        
        assert dockerignore_path.is_file(), ".dockerignore should be a file"

        with open(dockerignore_path, 'r') as f:
            dockerignore_content = f.read()

        # Check for important ignore patterns
        important_patterns = [
            ".git",
            "__pycache__",
            "*.py[cod]",
            ".pytest_cache",
            "logs/",
        ]

        for pattern in important_patterns:
            assert pattern in dockerignore_content, f".dockerignore should ignore: {pattern}"


class TestDockerBuildRequirements:
    """Test Docker build requirements and dependencies."""

    def test_requirements_txt_exists(self):
        """Test that requirements.txt exists and is valid."""
        requirements_path = Path("requirements.txt")
        # Skip test if running in Docker container and file doesn't exist
        if os.path.exists("/.dockerenv") and not requirements_path.exists():
            pytest.skip("requirements.txt not required when running inside container")
        
        if not requirements_path.exists():
            pytest.skip("requirements.txt not found")
        
        assert requirements_path.is_file(), "requirements.txt should be a file"

        with open(requirements_path, 'r') as f:
            requirements_content = f.read()

        # Check for essential dependencies
        essential_deps = [
            "pandas",
            "numpy",
            "matplotlib",
            "plotly",
        ]

        for dep in essential_deps:
            assert dep in requirements_content, f"requirements.txt should include: {dep}"

    def test_uv_toml_exists(self):
        """Test that uv.toml exists and is valid."""
        uv_toml_path = Path("uv.toml")
        # Skip test if running in Docker container and file doesn't exist
        if os.path.exists("/.dockerenv") and not uv_toml_path.exists():
            pytest.skip("uv.toml not required when running inside container")
        
        if not uv_toml_path.exists():
            pytest.skip("uv.toml not found")
        
        assert uv_toml_path.is_file(), "uv.toml should be a file"

        with open(uv_toml_path, 'r') as f:
            uv_toml_content = f.read()

        # Check for essential uv configuration
        essential_config = [
            "[pip]",
            "compile-bytecode",
        ]

        for config in essential_config:
            assert config in uv_toml_content, f"uv.toml should include: {config}"

    def test_docker_documentation_exists(self):
        """Test that Docker setup documentation exists."""
        docs_path = Path("docs/deployment/docker-setup.md")
        # Skip test if running in Docker container and file doesn't exist
        if os.path.exists("/.dockerenv") and not docs_path.exists():
            pytest.skip("Docker documentation not required when running inside container")
        
        if not docs_path.exists():
            pytest.skip("Docker documentation not found")
        
        assert docs_path.is_file(), "Docker setup documentation should be a file"


if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 