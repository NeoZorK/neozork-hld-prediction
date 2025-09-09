"""
Kubernetes Manager

Main orchestrator for Kubernetes deployment and management.
"""

import asyncio
import logging
import yaml
import json
from datetime import datetime
from typing import Dict, List, Optional, Any, Union
from pathlib import Path

logger = logging.getLogger(__name__)


class KubernetesManager:
    """
    Main Kubernetes manager for deployment and orchestration.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize Kubernetes manager."""
        self.config = config or {}
        self.namespace = self.config.get('namespace', 'pocket-hedge-fund')
        self.environment = self.config.get('environment', 'production')
        self.cluster_name = self.config.get('cluster_name', 'pocket-hedge-fund-cluster')
        
        # Service configurations
        self.services = {
            'api': {
                'image': 'pocket-hedge-fund-api',
                'port': 8000,
                'replicas': 3,
                'resources': {
                    'requests': {'cpu': '100m', 'memory': '256Mi'},
                    'limits': {'cpu': '500m', 'memory': '512Mi'}
                },
                'health_check': {
                    'path': '/health',
                    'port': 8000
                }
            },
            'database': {
                'image': 'postgres:15',
                'port': 5432,
                'replicas': 1,
                'resources': {
                    'requests': {'cpu': '200m', 'memory': '512Mi'},
                    'limits': {'cpu': '1000m', 'memory': '2Gi'}
                },
                'persistent_volume': True,
                'storage_size': '20Gi'
            },
            'redis': {
                'image': 'redis:7-alpine',
                'port': 6379,
                'replicas': 2,
                'resources': {
                    'requests': {'cpu': '50m', 'memory': '128Mi'},
                    'limits': {'cpu': '200m', 'memory': '256Mi'}
                }
            },
            'nginx': {
                'image': 'nginx:alpine',
                'port': 80,
                'replicas': 2,
                'resources': {
                    'requests': {'cpu': '50m', 'memory': '64Mi'},
                    'limits': {'cpu': '200m', 'memory': '128Mi'}
                }
            }
        }
        
        self.deployments = {}
        self.services_k8s = {}
        self.configmaps = {}
        self.secrets = {}
        self.ingresses = {}
    
    async def initialize(self):
        """Initialize Kubernetes manager."""
        try:
            # Check kubectl availability
            await self._check_kubectl_availability()
            
            # Create namespace
            await self._create_namespace()
            
            # Create ConfigMaps
            await self._create_configmaps()
            
            # Create Secrets
            await self._create_secrets()
            
            logger.info("Kubernetes manager initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Kubernetes manager: {e}")
            raise
    
    async def _check_kubectl_availability(self):
        """Check if kubectl is available and cluster is accessible."""
        try:
            result = await self._run_kubectl_command(['version', '--output=json'])
            if result.returncode != 0:
                raise RuntimeError("kubectl is not available or cluster is not accessible")
            
            version_info = json.loads(result.stdout)
            logger.info(f"Kubernetes version: {version_info.get('serverVersion', {}).get('gitVersion', 'unknown')}")
        except Exception as e:
            logger.error(f"Kubectl availability check failed: {e}")
            raise
    
    async def _create_namespace(self):
        """Create Kubernetes namespace."""
        try:
            namespace_manifest = {
                'apiVersion': 'v1',
                'kind': 'Namespace',
                'metadata': {
                    'name': self.namespace,
                    'labels': {
                        'app': 'pocket-hedge-fund',
                        'environment': self.environment
                    }
                }
            }
            
            await self._apply_manifest(namespace_manifest)
            logger.info(f"Created namespace: {self.namespace}")
        except Exception as e:
            logger.error(f"Failed to create namespace: {e}")
            raise
    
    async def _create_configmaps(self):
        """Create ConfigMaps for application configuration."""
        try:
            configmaps = {
                'app-config': {
                    'apiVersion': 'v1',
                    'kind': 'ConfigMap',
                    'metadata': {
                        'name': 'app-config',
                        'namespace': self.namespace
                    },
                    'data': {
                        'ENVIRONMENT': self.environment,
                        'LOG_LEVEL': 'INFO',
                        'DATABASE_HOST': 'postgres-service',
                        'DATABASE_PORT': '5432',
                        'REDIS_HOST': 'redis-service',
                        'REDIS_PORT': '6379'
                    }
                },
                'nginx-config': {
                    'apiVersion': 'v1',
                    'kind': 'ConfigMap',
                    'metadata': {
                        'name': 'nginx-config',
                        'namespace': self.namespace
                    },
                    'data': {
                        'nginx.conf': self._get_nginx_config()
                    }
                }
            }
            
            for name, configmap in configmaps.items():
                await self._apply_manifest(configmap)
                self.configmaps[name] = configmap
                logger.info(f"Created ConfigMap: {name}")
                
        except Exception as e:
            logger.error(f"Failed to create ConfigMaps: {e}")
            raise
    
    async def _create_secrets(self):
        """Create Secrets for sensitive data."""
        try:
            secrets = {
                'app-secrets': {
                    'apiVersion': 'v1',
                    'kind': 'Secret',
                    'metadata': {
                        'name': 'app-secrets',
                        'namespace': self.namespace
                    },
                    'type': 'Opaque',
                    'data': {
                        'DATABASE_PASSWORD': 'cGFzc3dvcmQ=',  # base64 encoded 'password'
                        'SECRET_KEY': 'c2VjcmV0LWtleQ==',  # base64 encoded 'secret-key'
                        'JWT_SECRET': 'and0LXNlY3JldA=='  # base64 encoded 'jwt-secret'
                    }
                },
                'tls-secret': {
                    'apiVersion': 'v1',
                    'kind': 'Secret',
                    'metadata': {
                        'name': 'tls-secret',
                        'namespace': self.namespace
                    },
                    'type': 'kubernetes.io/tls',
                    'data': {
                        'tls.crt': '',  # Will be populated with actual certificate
                        'tls.key': ''   # Will be populated with actual key
                    }
                }
            }
            
            for name, secret in secrets.items():
                await self._apply_manifest(secret)
                self.secrets[name] = secret
                logger.info(f"Created Secret: {name}")
                
        except Exception as e:
            logger.error(f"Failed to create Secrets: {e}")
            raise
    
    def _get_nginx_config(self) -> str:
        """Get Nginx configuration."""
        return """
events {
    worker_connections 1024;
}

http {
    upstream api {
        server api-service:8000;
    }
    
    server {
        listen 80;
        server_name _;
        
        location / {
            proxy_pass http://api;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
        
        location /health {
            access_log off;
            return 200 "healthy\\n";
            add_header Content-Type text/plain;
        }
    }
}
"""
    
    async def deploy_service(self, service_name: str) -> Dict[str, Any]:
        """Deploy a service to Kubernetes."""
        try:
            if service_name not in self.services:
                raise ValueError(f"Unknown service: {service_name}")
            
            service_config = self.services[service_name]
            
            # Create deployment
            deployment = await self._create_deployment(service_name, service_config)
            
            # Create service
            service = await self._create_service(service_name, service_config)
            
            # Create ingress if needed
            if service_name == 'nginx':
                ingress = await self._create_ingress(service_name, service_config)
            
            result = {
                'service': service_name,
                'deployment': deployment['metadata']['name'],
                'service_k8s': service['metadata']['name'],
                'status': 'deployed'
            }
            
            self.deployments[service_name] = deployment
            self.services_k8s[service_name] = service
            
            logger.info(f"Deployed service: {service_name}")
            return result
            
        except Exception as e:
            logger.error(f"Failed to deploy service {service_name}: {e}")
            raise
    
    async def _create_deployment(self, service_name: str, service_config: Dict[str, Any]) -> Dict[str, Any]:
        """Create Kubernetes deployment."""
        deployment = {
            'apiVersion': 'apps/v1',
            'kind': 'Deployment',
            'metadata': {
                'name': f'{service_name}-deployment',
                'namespace': self.namespace,
                'labels': {
                    'app': service_name,
                    'environment': self.environment
                }
            },
            'spec': {
                'replicas': service_config.get('replicas', 1),
                'selector': {
                    'matchLabels': {
                        'app': service_name
                    }
                },
                'template': {
                    'metadata': {
                        'labels': {
                            'app': service_name,
                            'environment': self.environment
                        }
                    },
                    'spec': {
                        'containers': [{
                            'name': service_name,
                            'image': f"{service_config['image']}:{self.environment}",
                            'ports': [{
                                'containerPort': service_config['port']
                            }],
                            'envFrom': [{
                                'configMapRef': {
                                    'name': 'app-config'
                                }
                            }],
                            'resources': service_config.get('resources', {}),
                            'livenessProbe': self._get_liveness_probe(service_config),
                            'readinessProbe': self._get_readiness_probe(service_config)
                        }]
                    }
                }
            }
        }
        
        # Add volume mounts for persistent storage
        if service_config.get('persistent_volume'):
            deployment['spec']['template']['spec']['volumes'] = [{
                'name': 'data',
                'persistentVolumeClaim': {
                    'claimName': f'{service_name}-pvc'
                }
            }]
            deployment['spec']['template']['spec']['containers'][0]['volumeMounts'] = [{
                'name': 'data',
                'mountPath': '/var/lib/postgresql/data'
            }]
        
        await self._apply_manifest(deployment)
        return deployment
    
    async def _create_service(self, service_name: str, service_config: Dict[str, Any]) -> Dict[str, Any]:
        """Create Kubernetes service."""
        service = {
            'apiVersion': 'v1',
            'kind': 'Service',
            'metadata': {
                'name': f'{service_name}-service',
                'namespace': self.namespace,
                'labels': {
                    'app': service_name,
                    'environment': self.environment
                }
            },
            'spec': {
                'selector': {
                    'app': service_name
                },
                'ports': [{
                    'port': service_config['port'],
                    'targetPort': service_config['port'],
                    'protocol': 'TCP'
                }],
                'type': 'ClusterIP'
            }
        }
        
        await self._apply_manifest(service)
        return service
    
    async def _create_ingress(self, service_name: str, service_config: Dict[str, Any]) -> Dict[str, Any]:
        """Create Kubernetes ingress."""
        ingress = {
            'apiVersion': 'networking.k8s.io/v1',
            'kind': 'Ingress',
            'metadata': {
                'name': f'{service_name}-ingress',
                'namespace': self.namespace,
                'annotations': {
                    'nginx.ingress.kubernetes.io/rewrite-target': '/',
                    'nginx.ingress.kubernetes.io/ssl-redirect': 'true'
                }
            },
            'spec': {
                'tls': [{
                    'hosts': ['pocket-hedge-fund.com'],
                    'secretName': 'tls-secret'
                }],
                'rules': [{
                    'host': 'pocket-hedge-fund.com',
                    'http': {
                        'paths': [{
                            'path': '/',
                            'pathType': 'Prefix',
                            'backend': {
                                'service': {
                                    'name': f'{service_name}-service',
                                    'port': {
                                        'number': service_config['port']
                                    }
                                }
                            }
                        }]
                    }
                }]
            }
        }
        
        await self._apply_manifest(ingress)
        self.ingresses[service_name] = ingress
        return ingress
    
    def _get_liveness_probe(self, service_config: Dict[str, Any]) -> Dict[str, Any]:
        """Get liveness probe configuration."""
        if 'health_check' in service_config:
            return {
                'httpGet': {
                    'path': service_config['health_check']['path'],
                    'port': service_config['health_check']['port']
                },
                'initialDelaySeconds': 30,
                'periodSeconds': 10,
                'timeoutSeconds': 5,
                'failureThreshold': 3
            }
        return {}
    
    def _get_readiness_probe(self, service_config: Dict[str, Any]) -> Dict[str, Any]:
        """Get readiness probe configuration."""
        if 'health_check' in service_config:
            return {
                'httpGet': {
                    'path': service_config['health_check']['path'],
                    'port': service_config['health_check']['port']
                },
                'initialDelaySeconds': 5,
                'periodSeconds': 5,
                'timeoutSeconds': 3,
                'failureThreshold': 3
            }
        return {}
    
    async def scale_deployment(self, service_name: str, replicas: int) -> bool:
        """Scale deployment to specified number of replicas."""
        try:
            deployment_name = f'{service_name}-deployment'
            
            result = await self._run_kubectl_command([
                'scale', 'deployment', deployment_name,
                f'--replicas={replicas}',
                f'--namespace={self.namespace}'
            ])
            
            if result.returncode == 0:
                logger.info(f"Scaled {service_name} to {replicas} replicas")
                return True
            else:
                logger.error(f"Failed to scale {service_name}: {result.stderr}")
                return False
                
        except Exception as e:
            logger.error(f"Failed to scale deployment {service_name}: {e}")
            return False
    
    async def get_deployment_status(self, service_name: str) -> Dict[str, Any]:
        """Get deployment status."""
        try:
            deployment_name = f'{service_name}-deployment'
            
            result = await self._run_kubectl_command([
                'get', 'deployment', deployment_name,
                f'--namespace={self.namespace}',
                '--output=json'
            ])
            
            if result.returncode == 0:
                deployment_info = json.loads(result.stdout)
                return {
                    'name': deployment_name,
                    'replicas': deployment_info['spec']['replicas'],
                    'ready_replicas': deployment_info['status'].get('readyReplicas', 0),
                    'available_replicas': deployment_info['status'].get('availableReplicas', 0),
                    'conditions': deployment_info['status'].get('conditions', [])
                }
            else:
                return {'name': deployment_name, 'status': 'not_found'}
                
        except Exception as e:
            logger.error(f"Failed to get deployment status for {service_name}: {e}")
            return {'name': service_name, 'status': 'error', 'error': str(e)}
    
    async def get_pod_logs(self, service_name: str, lines: int = 100) -> str:
        """Get pod logs for service."""
        try:
            result = await self._run_kubectl_command([
                'logs', f'--selector=app={service_name}',
                f'--namespace={self.namespace}',
                f'--tail={lines}'
            ])
            
            if result.returncode == 0:
                return result.stdout
            else:
                return f"Failed to get logs: {result.stderr}"
                
        except Exception as e:
            logger.error(f"Failed to get logs for {service_name}: {e}")
            return f"Error: {str(e)}"
    
    async def delete_service(self, service_name: str) -> bool:
        """Delete service from Kubernetes."""
        try:
            # Delete deployment
            deployment_name = f'{service_name}-deployment'
            await self._run_kubectl_command([
                'delete', 'deployment', deployment_name,
                f'--namespace={self.namespace}'
            ])
            
            # Delete service
            service_name_k8s = f'{service_name}-service'
            await self._run_kubectl_command([
                'delete', 'service', service_name_k8s,
                f'--namespace={self.namespace}'
            ])
            
            # Delete ingress if exists
            if service_name in self.ingresses:
                ingress_name = f'{service_name}-ingress'
                await self._run_kubectl_command([
                    'delete', 'ingress', ingress_name,
                    f'--namespace={self.namespace}'
                ])
            
            # Remove from local state
            if service_name in self.deployments:
                del self.deployments[service_name]
            if service_name in self.services_k8s:
                del self.services_k8s[service_name]
            if service_name in self.ingresses:
                del self.ingresses[service_name]
            
            logger.info(f"Deleted service: {service_name}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to delete service {service_name}: {e}")
            return False
    
    async def _apply_manifest(self, manifest: Dict[str, Any]):
        """Apply Kubernetes manifest."""
        try:
            # Convert to YAML
            yaml_content = yaml.dump(manifest, default_flow_style=False)
            
            # Apply using kubectl
            result = await self._run_kubectl_command(['apply', '-f', '-'], input=yaml_content)
            
            if result.returncode != 0:
                raise RuntimeError(f"Failed to apply manifest: {result.stderr}")
                
        except Exception as e:
            logger.error(f"Failed to apply manifest: {e}")
            raise
    
    async def _run_kubectl_command(self, cmd: List[str], input: str = None) -> Any:
        """Run kubectl command."""
        try:
            full_cmd = ['kubectl'] + cmd
            
            if input:
                process = await asyncio.create_subprocess_exec(
                    *full_cmd,
                    stdin=asyncio.subprocess.PIPE,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE
                )
                stdout, stderr = await process.communicate(input=input.encode())
            else:
                process = await asyncio.create_subprocess_exec(
                    *full_cmd,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE
                )
                stdout, stderr = await process.communicate()
            
            return type('Result', (), {
                'returncode': process.returncode,
                'stdout': stdout.decode('utf-8'),
                'stderr': stderr.decode('utf-8')
            })()
            
        except Exception as e:
            logger.error(f"Kubectl command execution failed: {e}")
            raise
    
    async def cleanup(self):
        """Cleanup Kubernetes resources."""
        try:
            # Delete all deployments
            for service_name in list(self.deployments.keys()):
                await self.delete_service(service_name)
            
            # Delete namespace
            await self._run_kubectl_command(['delete', 'namespace', self.namespace])
            
            self.deployments.clear()
            self.services_k8s.clear()
            self.configmaps.clear()
            self.secrets.clear()
            self.ingresses.clear()
            
            logger.info("Kubernetes manager cleanup completed")
        except Exception as e:
            logger.error(f"Error during Kubernetes manager cleanup: {e}")
