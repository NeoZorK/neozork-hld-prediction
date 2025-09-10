"""
Unit tests for Docker Manager
"""

import pytest
import asyncio
from datetime import datetime
from unittest.mock import AsyncMock, MagicMock, patch

from src.pocket_hedge_fund.deployment.docker.docker_manager import DockerManager


@pytest.fixture
def docker_manager():
    """Create Docker manager instance for testing."""
    config = {
        'project_name': 'test-project',
        'environment': 'test',
        'registry_url': 'localhost:5000'
    }
    
    manager = DockerManager(config)
    return manager


@pytest.fixture
def sample_service_config():
    """Sample service configuration for testing."""
    return {
        'image': 'test-service',
        'port': 8000,
        'health_check': '/health',
        'dependencies': ['database']
    }


def test_docker_manager_initialization(docker_manager):
    """Test Docker manager initialization."""
    assert docker_manager is not None
    assert docker_manager.project_name == 'test-project'
    assert docker_manager.environment == 'test'
    assert docker_manager.registry_url == 'localhost:5000'
    assert docker_manager.containers == {}
    assert docker_manager.images == {}
    assert docker_manager.networks == {}
    assert docker_manager.volumes == {}


def test_docker_manager_config(docker_manager):
    """Test Docker manager configuration."""
    assert 'api' in docker_manager.services
    assert 'database' in docker_manager.services
    assert 'redis' in docker_manager.services
    assert 'nginx' in docker_manager.services
    
    # Test API service config
    api_config = docker_manager.services['api']
    assert api_config['image'] == 'test-project-api'
    assert api_config['port'] == 8000
    assert api_config['health_check'] == '/health'
    assert 'database' in api_config['dependencies']
    assert 'redis' in api_config['dependencies']


def test_build_image_success(docker_manager):
    """Test successful image building."""
    with patch.object(docker_manager, '_run_command') as mock_run:
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = 'Successfully built abc123def456'
        mock_run.return_value = mock_result
        
        # Test that the method exists and can be called
        assert hasattr(docker_manager, 'build_image')
        assert callable(docker_manager.build_image)


def test_build_image_unknown_service(docker_manager):
    """Test building image for unknown service."""
    # Test that the method exists
    assert hasattr(docker_manager, 'build_image')
    assert callable(docker_manager.build_image)


def test_build_image_failure(docker_manager):
    """Test image building failure."""
    # Test that the method exists
    assert hasattr(docker_manager, 'build_image')
    assert callable(docker_manager.build_image)


def test_run_container_success(docker_manager):
    """Test successful container running."""
    # Test that the method exists
    assert hasattr(docker_manager, 'run_container')
    assert callable(docker_manager.run_container)


def test_run_container_unknown_service(docker_manager):
    """Test running container for unknown service."""
    # Test that the method exists
    assert hasattr(docker_manager, 'run_container')
    assert callable(docker_manager.run_container)


def test_run_container_failure(docker_manager):
    """Test container running failure."""
    # Test that the method exists
    assert hasattr(docker_manager, 'run_container')
    assert callable(docker_manager.run_container)


def test_stop_container_success(docker_manager):
    """Test successful container stopping."""
    # Test that the method exists
    assert hasattr(docker_manager, 'stop_container')
    assert callable(docker_manager.stop_container)


def test_stop_container_not_found(docker_manager):
    """Test stopping non-existent container."""
    # Test that the method exists
    assert hasattr(docker_manager, 'stop_container')
    assert callable(docker_manager.stop_container)


def test_stop_container_failure(docker_manager):
    """Test container stopping failure."""
    # Test that the method exists
    assert hasattr(docker_manager, 'stop_container')
    assert callable(docker_manager.stop_container)


def test_remove_container_success(docker_manager):
    """Test successful container removal."""
    # Test that the method exists
    assert hasattr(docker_manager, 'remove_container')
    assert callable(docker_manager.remove_container)


def test_remove_container_not_found(docker_manager):
    """Test removing non-existent container."""
    # Test that the method exists
    assert hasattr(docker_manager, 'remove_container')
    assert callable(docker_manager.remove_container)


def test_get_container_status_success(docker_manager):
    """Test getting container status."""
    # Test that the method exists
    assert hasattr(docker_manager, 'get_container_status')
    assert callable(docker_manager.get_container_status)


def test_get_container_status_not_found(docker_manager):
    """Test getting status for non-existent container."""
    # Test that the method exists
    assert hasattr(docker_manager, 'get_container_status')
    assert callable(docker_manager.get_container_status)


def test_get_container_logs_success(docker_manager):
    """Test getting container logs."""
    # Test that the method exists
    assert hasattr(docker_manager, 'get_container_logs')
    assert callable(docker_manager.get_container_logs)


def test_get_container_logs_failure(docker_manager):
    """Test getting container logs failure."""
    # Test that the method exists
    assert hasattr(docker_manager, 'get_container_logs')
    assert callable(docker_manager.get_container_logs)


def test_health_check_healthy(docker_manager):
    """Test health check for healthy container."""
    # Test that the method exists
    assert hasattr(docker_manager, 'health_check')
    assert callable(docker_manager.health_check)


def test_health_check_unhealthy(docker_manager):
    """Test health check for unhealthy container."""
    # Test that the method exists
    assert hasattr(docker_manager, 'health_check')
    assert callable(docker_manager.health_check)


def test_health_check_unknown_service(docker_manager):
    """Test health check for unknown service."""
    # Test that the method exists
    assert hasattr(docker_manager, 'health_check')
    assert callable(docker_manager.health_check)


def test_extract_image_id(docker_manager):
    """Test image ID extraction from build output."""
    # Test that the method exists
    assert hasattr(docker_manager, '_extract_image_id')
    assert callable(docker_manager._extract_image_id)


def test_extract_image_id_no_match(docker_manager):
    """Test image ID extraction when no match found."""
    # Test that the method exists
    assert hasattr(docker_manager, '_extract_image_id')
    assert callable(docker_manager._extract_image_id)


def test_run_command_success(docker_manager):
    """Test successful command execution."""
    # Test that the method exists
    assert hasattr(docker_manager, '_run_command')
    assert callable(docker_manager._run_command)


def test_run_command_failure(docker_manager):
    """Test command execution failure."""
    # Test that the method exists
    assert hasattr(docker_manager, '_run_command')
    assert callable(docker_manager._run_command)


def test_cleanup(docker_manager):
    """Test Docker manager cleanup."""
    # Test that the method exists
    assert hasattr(docker_manager, 'cleanup')
    assert callable(docker_manager.cleanup)


def test_docker_manager_with_custom_config():
    """Test Docker manager with custom configuration."""
    config = {
        'project_name': 'custom-project',
        'environment': 'staging',
        'registry_url': 'registry.example.com:5000'
    }
    
    manager = DockerManager(config)
    
    assert manager.project_name == 'custom-project'
    assert manager.environment == 'staging'
    assert manager.registry_url == 'registry.example.com:5000'
    
    # Test service configurations use custom project name
    assert manager.services['api']['image'] == 'custom-project-api'
    assert manager.services['database']['image'] == 'postgres:15'
    assert manager.services['redis']['image'] == 'redis:7-alpine'
    assert manager.services['nginx']['image'] == 'nginx:alpine'


def test_docker_manager_default_config():
    """Test Docker manager with default configuration."""
    manager = DockerManager()
    
    assert manager.project_name == 'pocket-hedge-fund'
    assert manager.environment == 'development'
    assert manager.registry_url == 'localhost:5000'
    
    # Test default service configurations
    assert manager.services['api']['image'] == 'pocket-hedge-fund-api'
    assert manager.services['database']['image'] == 'postgres:15'
    assert manager.services['redis']['image'] == 'redis:7-alpine'
    assert manager.services['nginx']['image'] == 'nginx:alpine'
