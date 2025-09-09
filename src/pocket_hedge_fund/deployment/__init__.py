"""
Deployment Setup Module for Pocket Hedge Fund

This module provides comprehensive deployment capabilities including:
- Docker containerization and orchestration
- Kubernetes cluster management
- Infrastructure as Code with Terraform
- Configuration management with Ansible
- Monitoring and observability setup
- Security and compliance configurations
- Automated deployment scripts
- Environment-specific configurations
"""

from .docker.docker_manager import DockerManager
from .kubernetes.k8s_manager import KubernetesManager
from .terraform.terraform_manager import TerraformManager
from .ansible.ansible_manager import AnsibleManager
from .monitoring.monitoring_setup import MonitoringSetup
from .security.security_setup import SecuritySetup
from .scripts.deployment_scripts import DeploymentScripts
from .configs.environment_config import EnvironmentConfig

__version__ = "1.0.0"
__author__ = "Pocket Hedge Fund Team"

__all__ = [
    # Core deployment managers
    "DockerManager",
    "KubernetesManager", 
    "TerraformManager",
    "AnsibleManager",
    
    # Setup components
    "MonitoringSetup",
    "SecuritySetup",
    "DeploymentScripts",
    "EnvironmentConfig"
]
