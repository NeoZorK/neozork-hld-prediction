"""
Unit tests for Docker Manager
"""

import pytest
import asyncio
from datetime import datetime
from unittest.mock import AsyncMock, MagicMock, patch

from src.pocket_hedge_fund.deployment.docker.docker_manager import DockerManager


@pytest.fixture
async def docker_manager():
    """Create Docker manager instance for testing."""
    config = {
        'project_name': 'test-project',
        'environment': 'test',
        'registry_url': 'localhost:5000'
    }
    
    manager = DockerManager(config)
    
    # Mock the subprocess calls
    with patch('asyncio.create_subprocess_exec') as mock_subprocess:
        mock_process = AsyncMock()
        mock_process.returncode = 0
        mock_process.communicate.return_value = (b'{"Server": {"Version": "20.10.0"}}', b'')
        mock_subprocess.return_value = mock_process
        
        await manager.initialize()
    
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


@pytest.mark.asyncio
async def test_docker_manager_initialization(docker_manager):
    """Test Docker manager initialization."""
    assert docker_manager is not None
    assert docker_manager.is_initialized is True
    assert docker_manager.project_name == 'test-project'
    assert docker_manager.environment == 'test'
    assert docker_manager.registry_url == 'localhost:5000'
    assert docker_manager.containers == {}
    assert docker_manager.images == {}
    assert docker_manager.networks == {}
    assert docker_manager.volumes == {}


@pytest.mark.asyncio
async def test_docker_manager_config(docker_manager):
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


@pytest.mark.asyncio
async def test_build_image_success(docker_manager):
    """Test successful image building."""
    with patch.object(docker_manager, '_run_command') as mock_run:
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = 'Successfully built abc123def456'
        mock_run.return_value = mock_result
        
        image_id = await docker_manager.build_image(
            service_name='api',
            dockerfile_path='./Dockerfile',
            build_args={'ENV': 'test'},
            tags=['latest', 'test']
        )
        
        assert image_id == 'abc123def456'
        assert 'test-project-api' in docker_manager.images
        assert docker_manager.images['test-project-api']['service'] == 'api'
        assert docker_manager.images['test-project-api']['tags'] == ['latest', 'test']


@pytest.mark.asyncio
async def test_build_image_unknown_service(docker_manager):
    """Test building image for unknown service."""
    with pytest.raises(ValueError, match="Unknown service"):
        await docker_manager.build_image(
            service_name='unknown-service',
            dockerfile_path='./Dockerfile'
        )


@pytest.mark.asyncio
async def test_build_image_failure(docker_manager):
    """Test image building failure."""
    with patch.object(docker_manager, '_run_command') as mock_run:
        mock_result = MagicMock()
        mock_result.returncode = 1
        mock_result.stderr = 'Build failed'
        mock_run.return_value = mock_result
        
        with pytest.raises(RuntimeError, match="Failed to build image"):
            await docker_manager.build_image(
                service_name='api',
                dockerfile_path='./Dockerfile'
            )


@pytest.mark.asyncio
async def test_run_container_success(docker_manager):
    """Test successful container running."""
    with patch.object(docker_manager, '_run_command') as mock_run:
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = 'container123'
        mock_run.return_value = mock_result
        
        container_id = await docker_manager.run_container(
            service_name='api',
            environment_vars={'ENV': 'test'},
            ports={'8000': '8000'},
            volumes=['test-volume:/data']
        )
        
        assert container_id == 'container123'
        assert 'test-project-api' in docker_manager.containers
        assert docker_manager.containers['test-project-api']['service'] == 'api'
        assert docker_manager.containers['test-project-api']['status'] == 'running'


@pytest.mark.asyncio
async def test_run_container_unknown_service(docker_manager):
    """Test running container for unknown service."""
    with pytest.raises(ValueError, match="Unknown service"):
        await docker_manager.run_container(
            service_name='unknown-service'
        )


@pytest.mark.asyncio
async def test_run_container_failure(docker_manager):
    """Test container running failure."""
    with patch.object(docker_manager, '_run_command') as mock_run:
        mock_result = MagicMock()
        mock_result.returncode = 1
        mock_result.stderr = 'Container failed to start'
        mock_run.return_value = mock_result
        
        with pytest.raises(RuntimeError, match="Failed to run container"):
            await docker_manager.run_container(
                service_name='api'
            )


@pytest.mark.asyncio
async def test_stop_container_success(docker_manager):
    """Test successful container stopping."""
    # Add container to manager
    docker_manager.containers['test-project-api'] = {
        'id': 'container123',
        'service': 'api',
        'status': 'running'
    }
    
    with patch.object(docker_manager, '_run_command') as mock_run:
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_run.return_value = mock_result
        
        result = await docker_manager.stop_container('api')
        
        assert result is True
        assert docker_manager.containers['test-project-api']['status'] == 'stopped'


@pytest.mark.asyncio
async def test_stop_container_not_found(docker_manager):
    """Test stopping non-existent container."""
    result = await docker_manager.stop_container('unknown-service')
    assert result is False


@pytest.mark.asyncio
async def test_stop_container_failure(docker_manager):
    """Test container stopping failure."""
    # Add container to manager
    docker_manager.containers['test-project-api'] = {
        'id': 'container123',
        'service': 'api',
        'status': 'running'
    }
    
    with patch.object(docker_manager, '_run_command') as mock_run:
        mock_result = MagicMock()
        mock_result.returncode = 1
        mock_result.stderr = 'Failed to stop container'
        mock_run.return_value = mock_result
        
        result = await docker_manager.stop_container('api')
        
        assert result is False


@pytest.mark.asyncio
async def test_remove_container_success(docker_manager):
    """Test successful container removal."""
    # Add container to manager
    docker_manager.containers['test-project-api'] = {
        'id': 'container123',
        'service': 'api',
        'status': 'running'
    }
    
    with patch.object(docker_manager, '_run_command') as mock_run:
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_run.return_value = mock_result
        
        result = await docker_manager.remove_container('api')
        
        assert result is True
        assert 'test-project-api' not in docker_manager.containers


@pytest.mark.asyncio
async def test_remove_container_not_found(docker_manager):
    """Test removing non-existent container."""
    with pytest.raises(ValueError, match="Container not found"):
        await docker_manager.remove_container('unknown-service')


@pytest.mark.asyncio
async def test_get_container_status_success(docker_manager):
    """Test getting container status."""
    with patch.object(docker_manager, '_run_command') as mock_run:
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = '''[{
            "State": {
                "Status": "running",
                "Running": true,
                "RestartCount": 0
            },
            "Created": "2024-01-01T00:00:00Z",
            "Config": {
                "Image": "test-project-api:test"
            }
        }]'''
        mock_run.return_value = mock_result
        
        status = await docker_manager.get_container_status('api')
        
        assert status['name'] == 'test-project-api'
        assert status['status'] == 'running'
        assert status['running'] is True
        assert status['restart_count'] == 0
        assert status['image'] == 'test-project-api:test'


@pytest.mark.asyncio
async def test_get_container_status_not_found(docker_manager):
    """Test getting status for non-existent container."""
    with patch.object(docker_manager, '_run_command') as mock_run:
        mock_result = MagicMock()
        mock_result.returncode = 1
        mock_run.return_value = mock_result
        
        status = await docker_manager.get_container_status('unknown-service')
        
        assert status['name'] == 'test-project-unknown-service'
        assert status['status'] == 'not_found'


@pytest.mark.asyncio
async def test_get_container_logs_success(docker_manager):
    """Test getting container logs."""
    with patch.object(docker_manager, '_run_command') as mock_run:
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = 'Container log line 1\\nContainer log line 2'
        mock_run.return_value = mock_result
        
        logs = await docker_manager.get_container_logs('api', lines=50)
        
        assert 'Container log line 1' in logs
        assert 'Container log line 2' in logs


@pytest.mark.asyncio
async def test_get_container_logs_failure(docker_manager):
    """Test getting container logs failure."""
    with patch.object(docker_manager, '_run_command') as mock_run:
        mock_result = MagicMock()
        mock_result.returncode = 1
        mock_result.stderr = 'Failed to get logs'
        mock_run.return_value = mock_result
        
        logs = await docker_manager.get_container_logs('api')
        
        assert 'Failed to get logs' in logs


@pytest.mark.asyncio
async def test_health_check_healthy(docker_manager):
    """Test health check for healthy container."""
    with patch.object(docker_manager, 'get_container_status') as mock_status:
        mock_status.return_value = {
            'name': 'test-project-api',
            'status': 'running',
            'running': True
        }
        
        health = await docker_manager.health_check('api')
        
        assert health['status'] == 'healthy'
        assert health['container_status'] == 'running'
        assert health['health_endpoint'] == '/health'


@pytest.mark.asyncio
async def test_health_check_unhealthy(docker_manager):
    """Test health check for unhealthy container."""
    with patch.object(docker_manager, 'get_container_status') as mock_status:
        mock_status.return_value = {
            'name': 'test-project-api',
            'status': 'stopped',
            'running': False
        }
        
        health = await docker_manager.health_check('api')
        
        assert health['status'] == 'unhealthy'
        assert health['reason'] == 'Container not running'


@pytest.mark.asyncio
async def test_health_check_unknown_service(docker_manager):
    """Test health check for unknown service."""
    health = await docker_manager.health_check('unknown-service')
    
    assert health['status'] == 'unknown'
    assert health['error'] == 'Service not found'


@pytest.mark.asyncio
async def test_extract_image_id(docker_manager):
    """Test image ID extraction from build output."""
    build_output = """
Step 1/10 : FROM python:3.11-slim
 ---> abc123def456
Step 2/10 : WORKDIR /app
 ---> Running in def456ghi789
 ---> ghi789jkl012
Successfully built abc123def456
Successfully tagged test-project-api:latest
"""
    
    image_id = docker_manager._extract_image_id(build_output)
    assert image_id == 'abc123def456'


@pytest.mark.asyncio
async def test_extract_image_id_no_match(docker_manager):
    """Test image ID extraction when no match found."""
    build_output = "Build completed successfully"
    
    image_id = docker_manager._extract_image_id(build_output)
    assert image_id == 'unknown'


@pytest.mark.asyncio
async def test_run_command_success(docker_manager):
    """Test successful command execution."""
    with patch('asyncio.create_subprocess_exec') as mock_subprocess:
        mock_process = AsyncMock()
        mock_process.returncode = 0
        mock_process.communicate.return_value = (b'Success', b'')
        mock_subprocess.return_value = mock_process
        
        result = await docker_manager._run_command(['docker', 'version'])
        
        assert result.returncode == 0
        assert result.stdout == 'Success'
        assert result.stderr == ''


@pytest.mark.asyncio
async def test_run_command_failure(docker_manager):
    """Test command execution failure."""
    with patch('asyncio.create_subprocess_exec') as mock_subprocess:
        mock_process = AsyncMock()
        mock_process.returncode = 1
        mock_process.communicate.return_value = (b'', b'Command failed')
        mock_subprocess.return_value = mock_process
        
        result = await docker_manager._run_command(['docker', 'invalid'])
        
        assert result.returncode == 1
        assert result.stdout == ''
        assert result.stderr == 'Command failed'


@pytest.mark.asyncio
async def test_cleanup(docker_manager):
    """Test Docker manager cleanup."""
    # Add some data
    docker_manager.containers['test-container'] = {'id': '123', 'service': 'api'}
    docker_manager.images['test-image'] = {'id': '456', 'service': 'api'}
    docker_manager.networks['test-network'] = {'name': 'test-network'}
    docker_manager.volumes['test-volume'] = {'name': 'test-volume'}
    
    with patch.object(docker_manager, 'stop_container') as mock_stop, \
         patch.object(docker_manager, 'remove_container') as mock_remove:
        
        mock_stop.return_value = True
        mock_remove.return_value = True
        
        await docker_manager.cleanup()
        
        # Verify cleanup
        assert len(docker_manager.containers) == 0
        assert len(docker_manager.images) == 0
        assert len(docker_manager.networks) == 0
        assert len(docker_manager.volumes) == 0
        assert docker_manager.is_initialized is False


@pytest.mark.asyncio
async def test_docker_manager_with_custom_config():
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


@pytest.mark.asyncio
async def test_docker_manager_default_config():
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
