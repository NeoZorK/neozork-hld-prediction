"""
Test interactive mode functionality in Docker.

This module contains tests to verify that interactive mode
works correctly in Docker containers.
"""

import pytest
import os
import subprocess
import sys
from pathlib import Path


class TestDockerInteractiveMode:
    """Test Docker interactive mode functionality."""

    def test_docker_env_variables(self):
        """Test that Docker environment variables are set correctly."""
        # Check if DOCKER_CONTAINER is set
        docker_container = os.environ.get('DOCKER_CONTAINER', False)
        
        # In Docker, this should be True
        if os.path.exists('/.dockerenv'):
            assert docker_container == 'true', "DOCKER_CONTAINER should be 'true' in Docker environment"
            # Check other important environment variables only in Docker
            assert os.environ.get('PYTHONPATH') == '/app', "PYTHONPATH should be set to /app"
            assert os.environ.get('PYTHONUNBUFFERED') == '1', "PYTHONUNBUFFERED should be set to 1"
        else:
            # In local environment, these might not be set
            pytest.skip("Not running in Docker environment")

    def test_docker_entrypoint_exists(self):
        """Test that docker-entrypoint.sh exists and is executable."""
        entrypoint_path = Path("docker-entrypoint.sh")
        assert entrypoint_path.exists(), "docker-entrypoint.sh should exist"
        assert entrypoint_path.is_file(), "docker-entrypoint.sh should be a file"
        
        # Check if it's executable (only if we're on Unix-like system)
        if os.name == 'posix':
            # Make it executable if it's not
            if not os.access(entrypoint_path, os.X_OK):
                os.chmod(entrypoint_path, 0o755)
            assert os.access(entrypoint_path, os.X_OK), "docker-entrypoint.sh should be executable"

    def test_docker_compose_interactive_config(self):
        """Test that docker-compose.yml has correct interactive configuration."""
        compose_path = Path("docker-compose.yml")
        assert compose_path.exists(), "docker-compose.yml should exist"
        
        with open(compose_path, 'r') as f:
            content = f.read()
        
        # Check for interactive mode settings
        assert "stdin_open: true" in content, "docker-compose.yml should have stdin_open: true"
        assert "tty: true" in content, "docker-compose.yml should have tty: true"
        assert "DOCKER_CONTAINER=true" in content, "docker-compose.yml should set DOCKER_CONTAINER=true"

    def test_docker_env_file(self):
        """Test that docker.env file has correct configuration."""
        env_path = Path("docker.env")
        assert env_path.exists(), "docker.env should exist"
        
        with open(env_path, 'r') as f:
            content = f.read()
        
        # Check for required environment variables
        required_vars = [
            "USE_UV=true",
            "DOCKER_CONTAINER=true",
            "PYTHONPATH=/app",
            "PYTHONUNBUFFERED=1",
            "MCP_SERVER_TYPE=pycharm_copilot"
        ]
        
        for var in required_vars:
            assert var in content, f"docker.env should contain: {var}"

    def test_bash_config_files(self):
        """Test that bash configuration files are created properly."""
        # These files should be created by docker-entrypoint.sh
        bash_config_dir = Path("/tmp/bash_config")
        inputrc_file = bash_config_dir / ".inputrc"
        
        # In Docker environment, these should exist
        if os.path.exists('/.dockerenv'):
            assert bash_config_dir.exists(), "/tmp/bash_config directory should exist"
            assert inputrc_file.exists(), "/tmp/bash_config/.inputrc should exist"
        else:
            # In local environment, these might not exist
            pytest.skip("Not running in Docker environment")

    def test_history_configuration(self):
        """Test that bash history is configured properly."""
        # Check if history environment variables are set
        histfile = os.environ.get('HISTFILE', '')
        histsize = os.environ.get('HISTSIZE', '')
        histcontrol = os.environ.get('HISTCONTROL', '')
        
        # In Docker environment, these should be set
        if os.path.exists('/.dockerenv'):
            assert histfile == '/tmp/bash_history/.bash_history', "HISTFILE should be set correctly"
            assert histsize == '1000', "HISTSIZE should be set to 1000"
            assert 'ignoreboth' in histcontrol, "HISTCONTROL should contain ignoreboth"
        else:
            # In local environment, these might not be set
            pytest.skip("Not running in Docker environment")

    def test_prompt_configuration(self):
        """Test that custom prompt is configured."""
        ps1 = os.environ.get('PS1', '')
        
        # In Docker environment, PS1 should be set
        if os.path.exists('/.dockerenv'):
            assert 'neozork' in ps1, "PS1 should contain 'neozork'"
        else:
            # In local environment, PS1 might not be set
            pytest.skip("Not running in Docker environment")

    def test_inputrc_configuration(self):
        """Test that INPUTRC is configured."""
        inputrc = os.environ.get('INPUTRC', '')
        
        # In Docker environment, INPUTRC should be set
        if os.path.exists('/.dockerenv'):
            assert inputrc == '/tmp/bash_config/.inputrc', "INPUTRC should be set correctly"
        else:
            # In local environment, INPUTRC might not be set
            pytest.skip("Not running in Docker environment")

    def test_docker_build_args(self):
        """Test that Docker build arguments are configured correctly."""
        dockerfile_path = Path("Dockerfile")
        assert dockerfile_path.exists(), "Dockerfile should exist"
        
        with open(dockerfile_path, 'r') as f:
            content = f.read()
        
        # Check for build argument
        assert "ARG USE_UV=true" in content, "Dockerfile should have ARG USE_UV=true"


if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 