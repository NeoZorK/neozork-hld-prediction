"""
Docker Manager

Main orchestrator for Docker containerization and deployment.
"""

import asyncio
import logging
import subprocess
import json
from datetime import datetime
from typing import Dict, List, Optional, Any, Union
from pathlib import Path

logger = logging.getLogger(__name__)


class DockerManager:
    """
    Main Docker manager for containerization and orchestration.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize Docker manager."""
        self.config = config or {}
        self.containers = {}
        self.images = {}
        self.networks = {}
        self.volumes = {}
        self.is_initialized = False
        
        # Docker configuration
        self.registry_url = self.config.get('registry_url', 'localhost:5000')
        self.project_name = self.config.get('project_name', 'pocket-hedge-fund')
        self.environment = self.config.get('environment', 'development')
        
        # Service configurations
        self.services = {
            'api': {
                'image': f'{self.project_name}-api',
                'port': 8000,
                'health_check': '/health',
                'dependencies': ['database', 'redis']
            },
            'database': {
                'image': 'postgres:15',
                'port': 5432,
                'environment': {
                    'POSTGRES_DB': 'pocket_hedge_fund',
                    'POSTGRES_USER': 'postgres',
                    'POSTGRES_PASSWORD': 'password'
                },
                'volumes': ['postgres_data:/var/lib/postgresql/data']
            },
            'redis': {
                'image': 'redis:7-alpine',
                'port': 6379,
                'volumes': ['redis_data:/data']
            },
            'nginx': {
                'image': 'nginx:alpine',
                'port': 80,
                'dependencies': ['api'],
                'volumes': ['./nginx.conf:/etc/nginx/nginx.conf']
            }
        }
    
    async def initialize(self):
        """Initialize Docker manager."""
        try:
            # Check Docker availability
            await self._check_docker_availability()
            
            # Create Docker networks
            await self._create_networks()
            
            # Create Docker volumes
            await self._create_volumes()
            
            self.is_initialized = True
            logger.info("Docker manager initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Docker manager: {e}")
            raise
    
    async def _check_docker_availability(self):
        """Check if Docker is available and running."""
        try:
            result = await self._run_command(['docker', 'version', '--format', 'json'])
            if result.returncode != 0:
                raise RuntimeError("Docker is not available or not running")
            
            docker_info = json.loads(result.stdout)
            logger.info(f"Docker version: {docker_info.get('Server', {}).get('Version', 'unknown')}")
        except Exception as e:
            logger.error(f"Docker availability check failed: {e}")
            raise
    
    async def _create_networks(self):
        """Create Docker networks."""
        try:
            networks = [
                {
                    'name': f'{self.project_name}-network',
                    'driver': 'bridge',
                    'subnet': '172.20.0.0/16'
                },
                {
                    'name': f'{self.project_name}-frontend',
                    'driver': 'bridge'
                },
                {
                    'name': f'{self.project_name}-backend',
                    'driver': 'bridge'
                }
            ]
            
            for network_config in networks:
                await self._create_network(network_config)
                
        except Exception as e:
            logger.error(f"Failed to create networks: {e}")
            raise
    
    async def _create_network(self, network_config: Dict[str, Any]):
        """Create a Docker network."""
        try:
            network_name = network_config['name']
            
            # Check if network exists
            result = await self._run_command(['docker', 'network', 'ls', '--format', '{{.Name}}'])
            if network_name in result.stdout:
                logger.info(f"Network {network_name} already exists")
                return
            
            # Create network
            cmd = ['docker', 'network', 'create']
            if 'driver' in network_config:
                cmd.extend(['--driver', network_config['driver']])
            if 'subnet' in network_config:
                cmd.extend(['--subnet', network_config['subnet']])
            cmd.append(network_name)
            
            result = await self._run_command(cmd)
            if result.returncode == 0:
                self.networks[network_name] = network_config
                logger.info(f"Created network: {network_name}")
            else:
                raise RuntimeError(f"Failed to create network {network_name}: {result.stderr}")
                
        except Exception as e:
            logger.error(f"Failed to create network {network_config.get('name', 'unknown')}: {e}")
            raise
    
    async def _create_volumes(self):
        """Create Docker volumes."""
        try:
            volumes = [
                f'{self.project_name}-postgres-data',
                f'{self.project_name}-redis-data',
                f'{self.project_name}-logs',
                f'{self.project_name}-uploads'
            ]
            
            for volume_name in volumes:
                await self._create_volume(volume_name)
                
        except Exception as e:
            logger.error(f"Failed to create volumes: {e}")
            raise
    
    async def _create_volume(self, volume_name: str):
        """Create a Docker volume."""
        try:
            # Check if volume exists
            result = await self._run_command(['docker', 'volume', 'ls', '--format', '{{.Name}}'])
            if volume_name in result.stdout:
                logger.info(f"Volume {volume_name} already exists")
                return
            
            # Create volume
            result = await self._run_command(['docker', 'volume', 'create', volume_name])
            if result.returncode == 0:
                self.volumes[volume_name] = {'name': volume_name}
                logger.info(f"Created volume: {volume_name}")
            else:
                raise RuntimeError(f"Failed to create volume {volume_name}: {result.stderr}")
                
        except Exception as e:
            logger.error(f"Failed to create volume {volume_name}: {e}")
            raise
    
    async def build_image(
        self,
        service_name: str,
        dockerfile_path: str,
        build_args: Optional[Dict[str, str]] = None,
        tags: Optional[List[str]] = None
    ) -> str:
        """Build Docker image for service."""
        try:
            if service_name not in self.services:
                raise ValueError(f"Unknown service: {service_name}")
            
            service_config = self.services[service_name]
            image_name = service_config['image']
            
            # Prepare build command
            cmd = ['docker', 'build']
            
            # Add build args
            if build_args:
                for key, value in build_args.items():
                    cmd.extend(['--build-arg', f'{key}={value}'])
            
            # Add tags
            if tags:
                for tag in tags:
                    cmd.extend(['-t', f'{image_name}:{tag}'])
            else:
                cmd.extend(['-t', f'{image_name}:latest'])
                cmd.extend(['-t', f'{image_name}:{self.environment}'])
            
            # Add context path
            cmd.append(dockerfile_path)
            
            logger.info(f"Building image for {service_name}...")
            result = await self._run_command(cmd)
            
            if result.returncode == 0:
                image_id = self._extract_image_id(result.stdout)
                self.images[image_name] = {
                    'id': image_id,
                    'service': service_name,
                    'tags': tags or ['latest', self.environment],
                    'built_at': datetime.now()
                }
                logger.info(f"Successfully built image: {image_name}")
                return image_id
            else:
                raise RuntimeError(f"Failed to build image: {result.stderr}")
                
        except Exception as e:
            logger.error(f"Failed to build image for {service_name}: {e}")
            raise
    
    async def run_container(
        self,
        service_name: str,
        environment_vars: Optional[Dict[str, str]] = None,
        ports: Optional[Dict[str, str]] = None,
        volumes: Optional[List[str]] = None,
        restart_policy: str = 'unless-stopped'
    ) -> str:
        """Run Docker container for service."""
        try:
            if service_name not in self.services:
                raise ValueError(f"Unknown service: {service_name}")
            
            service_config = self.services[service_name]
            image_name = service_config['image']
            container_name = f'{self.project_name}-{service_name}'
            
            # Prepare run command
            cmd = ['docker', 'run', '-d']
            
            # Add container name
            cmd.extend(['--name', container_name])
            
            # Add restart policy
            cmd.extend(['--restart', restart_policy])
            
            # Add network
            cmd.extend(['--network', f'{self.project_name}-network'])
            
            # Add environment variables
            env_vars = environment_vars or {}
            if 'environment' in service_config:
                env_vars.update(service_config['environment'])
            
            for key, value in env_vars.items():
                cmd.extend(['-e', f'{key}={value}'])
            
            # Add port mappings
            port_mappings = ports or {}
            if 'port' in service_config:
                port_mappings[service_config['port']] = service_config['port']
            
            for host_port, container_port in port_mappings.items():
                cmd.extend(['-p', f'{host_port}:{container_port}'])
            
            # Add volumes
            volume_mappings = volumes or []
            if 'volumes' in service_config:
                volume_mappings.extend(service_config['volumes'])
            
            for volume in volume_mappings:
                cmd.extend(['-v', volume])
            
            # Add image
            cmd.append(f'{image_name}:{self.environment}')
            
            logger.info(f"Running container for {service_name}...")
            result = await self._run_command(cmd)
            
            if result.returncode == 0:
                container_id = result.stdout.strip()
                self.containers[container_name] = {
                    'id': container_id,
                    'service': service_name,
                    'image': image_name,
                    'status': 'running',
                    'started_at': datetime.now()
                }
                logger.info(f"Successfully started container: {container_name}")
                return container_id
            else:
                raise RuntimeError(f"Failed to run container: {result.stderr}")
                
        except Exception as e:
            logger.error(f"Failed to run container for {service_name}: {e}")
            raise
    
    async def stop_container(self, service_name: str) -> bool:
        """Stop Docker container for service."""
        try:
            container_name = f'{self.project_name}-{service_name}'
            
            if container_name not in self.containers:
                logger.warning(f"Container {container_name} not found")
                return False
            
            result = await self._run_command(['docker', 'stop', container_name])
            
            if result.returncode == 0:
                self.containers[container_name]['status'] = 'stopped'
                logger.info(f"Stopped container: {container_name}")
                return True
            else:
                logger.error(f"Failed to stop container: {result.stderr}")
                return False
                
        except Exception as e:
            logger.error(f"Failed to stop container for {service_name}: {e}")
            return False
    
    async def remove_container(self, service_name: str) -> bool:
        """Remove Docker container for service."""
        try:
            container_name = f'{self.project_name}-{service_name}'
            
            # Stop container first
            await self.stop_container(service_name)
            
            result = await self._run_command(['docker', 'rm', container_name])
            
            if result.returncode == 0:
                if container_name in self.containers:
                    del self.containers[container_name]
                logger.info(f"Removed container: {container_name}")
                return True
            else:
                logger.error(f"Failed to remove container: {result.stderr}")
                return False
                
        except Exception as e:
            logger.error(f"Failed to remove container for {service_name}: {e}")
            return False
    
    async def get_container_status(self, service_name: str) -> Dict[str, Any]:
        """Get container status and information."""
        try:
            container_name = f'{self.project_name}-{service_name}'
            
            result = await self._run_command([
                'docker', 'inspect', container_name, '--format', 'json'
            ])
            
            if result.returncode == 0:
                container_info = json.loads(result.stdout)
                return {
                    'name': container_name,
                    'status': container_info[0]['State']['Status'],
                    'running': container_info[0]['State']['Running'],
                    'restart_count': container_info[0]['RestartCount'],
                    'created': container_info[0]['Created'],
                    'image': container_info[0]['Config']['Image']
                }
            else:
                return {'name': container_name, 'status': 'not_found'}
                
        except Exception as e:
            logger.error(f"Failed to get container status for {service_name}: {e}")
            return {'name': service_name, 'status': 'error', 'error': str(e)}
    
    async def get_container_logs(self, service_name: str, lines: int = 100) -> str:
        """Get container logs."""
        try:
            container_name = f'{self.project_name}-{service_name}'
            
            result = await self._run_command([
                'docker', 'logs', '--tail', str(lines), container_name
            ])
            
            if result.returncode == 0:
                return result.stdout
            else:
                return f"Failed to get logs: {result.stderr}"
                
        except Exception as e:
            logger.error(f"Failed to get logs for {service_name}: {e}")
            return f"Error: {str(e)}"
    
    async def health_check(self, service_name: str) -> Dict[str, Any]:
        """Perform health check on service."""
        try:
            if service_name not in self.services:
                return {'status': 'unknown', 'error': 'Service not found'}
            
            service_config = self.services[service_name]
            container_status = await self.get_container_status(service_name)
            
            if not container_status.get('running', False):
                return {'status': 'unhealthy', 'reason': 'Container not running'}
            
            # Perform application health check if configured
            if 'health_check' in service_config:
                health_endpoint = service_config['health_check']
                # This would make an HTTP request to the health endpoint
                # For now, return basic container status
                return {
                    'status': 'healthy',
                    'container_status': container_status['status'],
                    'health_endpoint': health_endpoint
                }
            
            return {
                'status': 'healthy',
                'container_status': container_status['status']
            }
            
        except Exception as e:
            logger.error(f"Health check failed for {service_name}: {e}")
            return {'status': 'error', 'error': str(e)}
    
    async def _run_command(self, cmd: List[str]) -> subprocess.CompletedProcess:
        """Run shell command asynchronously."""
        try:
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await process.communicate()
            
            return subprocess.CompletedProcess(
                args=cmd,
                returncode=process.returncode,
                stdout=stdout.decode('utf-8'),
                stderr=stderr.decode('utf-8')
            )
        except Exception as e:
            logger.error(f"Command execution failed: {e}")
            raise
    
    def _extract_image_id(self, build_output: str) -> str:
        """Extract image ID from Docker build output."""
        try:
            lines = build_output.split('\n')
            for line in lines:
                if 'Successfully built' in line:
                    return line.split()[-1]
            return 'unknown'
        except Exception:
            return 'unknown'
    
    async def cleanup(self):
        """Cleanup Docker resources."""
        try:
            # Stop all containers
            for service_name in list(self.containers.keys()):
                await self.stop_container(service_name.split('-')[-1])
            
            # Remove containers
            for service_name in list(self.containers.keys()):
                await self.remove_container(service_name.split('-')[-1])
            
            self.containers.clear()
            self.images.clear()
            self.is_initialized = False
            
            logger.info("Docker manager cleanup completed")
        except Exception as e:
            logger.error(f"Error during Docker manager cleanup: {e}")
