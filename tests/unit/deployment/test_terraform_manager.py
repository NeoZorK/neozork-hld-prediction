"""
Unit tests for Terraform Manager
"""

import pytest
import asyncio
import json
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

from src.pocket_hedge_fund.deployment.terraform.terraform_manager import TerraformManager


@pytest.fixture
async def terraform_manager():
    """Create Terraform manager instance for testing."""
    config = {
        'working_dir': './test-terraform',
        'environment': 'test',
        'region': 'us-west-2',
        'project_name': 'test-project'
    }
    
    manager = TerraformManager(config)
    
    # Mock the subprocess calls
    with patch('asyncio.create_subprocess_exec') as mock_subprocess:
        mock_process = AsyncMock()
        mock_process.returncode = 0
        mock_process.communicate.return_value = (b'{"version": "1.0.0"}', b'')
        mock_subprocess.return_value = mock_process
        
        await manager.initialize()
    
    return manager


@pytest.fixture
def sample_terraform_output():
    """Sample Terraform output for testing."""
    return {
        'vpc_id': {
            'value': 'vpc-12345678'
        },
        'cluster_endpoint': {
            'value': 'https://test-cluster.us-west-2.eks.amazonaws.com'
        },
        'db_endpoint': {
            'value': 'test-db.cluster-xyz.us-west-2.rds.amazonaws.com'
        }
    }


@pytest.mark.asyncio
async def test_terraform_manager_initialization(terraform_manager):
    """Test Terraform manager initialization."""
    assert terraform_manager is not None
    assert terraform_manager.working_dir == './test-terraform'
    assert terraform_manager.environment == 'test'
    assert terraform_manager.region == 'us-west-2'
    assert terraform_manager.project_name == 'test-project'
    assert terraform_manager.state == {}
    assert terraform_manager.outputs == {}


@pytest.mark.asyncio
async def test_terraform_manager_config(terraform_manager):
    """Test Terraform manager configuration."""
    # Test provider configurations
    assert 'aws' in terraform_manager.providers
    assert 'kubernetes' in terraform_manager.providers
    assert 'helm' in terraform_manager.providers
    
    aws_provider = terraform_manager.providers['aws']
    assert aws_provider['source'] == 'hashicorp/aws'
    assert aws_provider['version'] == '~> 5.0'
    assert aws_provider['region'] == 'us-west-2'
    
    # Test resource configurations
    assert 'vpc' in terraform_manager.resources
    assert 'subnets' in terraform_manager.resources
    assert 'eks_cluster' in terraform_manager.resources
    assert 'rds' in terraform_manager.resources
    assert 'elasticache' in terraform_manager.resources
    
    vpc_config = terraform_manager.resources['vpc']
    assert vpc_config['name'] == 'test-project-vpc'
    assert vpc_config['cidr_block'] == '10.0.0.0/16'
    assert vpc_config['enable_dns_hostnames'] is True


@pytest.mark.asyncio
async def test_create_main_config(terraform_manager):
    """Test main configuration file creation."""
    config_file = Path(terraform_manager.working_dir) / 'main.tf'
    assert config_file.exists()
    
    config_content = config_file.read_text()
    assert 'Pocket Hedge Fund Infrastructure' in config_content
    assert 'provider "aws"' in config_content
    assert 'provider "kubernetes"' in config_content
    assert 'provider "helm"' in config_content
    assert 'resource "aws_vpc" "main"' in config_content
    assert 'resource "aws_eks_cluster" "cluster"' in config_content
    assert 'resource "aws_db_instance" "main"' in config_content


@pytest.mark.asyncio
async def test_create_variables_file(terraform_manager):
    """Test variables file creation."""
    variables_file = Path(terraform_manager.working_dir) / 'variables.tf'
    assert variables_file.exists()
    
    variables_content = variables_file.read_text()
    assert 'variable "project_name"' in variables_content
    assert 'variable "environment"' in variables_content
    assert 'variable "aws_region"' in variables_content
    assert 'variable "vpc_cidr"' in variables_content
    assert 'variable "cluster_name"' in variables_content
    assert 'variable "db_engine"' in variables_content


@pytest.mark.asyncio
async def test_create_outputs_file(terraform_manager):
    """Test outputs file creation."""
    outputs_file = Path(terraform_manager.working_dir) / 'outputs.tf'
    assert outputs_file.exists()
    
    outputs_content = outputs_file.read_text()
    assert 'output "vpc_id"' in outputs_content
    assert 'output "cluster_endpoint"' in outputs_content
    assert 'output "db_endpoint"' in outputs_content
    assert 'output "cache_endpoint"' in outputs_content


@pytest.mark.asyncio
async def test_plan_success(terraform_manager):
    """Test successful Terraform plan."""
    with patch.object(terraform_manager, '_run_terraform_command') as mock_run:
        mock_result = MagicMock()
        mock_result.stdout = 'Plan: 10 to add, 0 to change, 0 to destroy.'
        mock_run.return_value = mock_result
        
        result = await terraform_manager.plan()
        
        assert 'Plan: 10 to add, 0 to change, 0 to destroy.' in result
        mock_run.assert_called_once_with(['plan'])


@pytest.mark.asyncio
async def test_plan_failure(terraform_manager):
    """Test Terraform plan failure."""
    with patch.object(terraform_manager, '_run_terraform_command') as mock_run:
        mock_run.side_effect = RuntimeError('Terraform plan failed')
        
        with pytest.raises(RuntimeError, match="Terraform plan failed"):
            await terraform_manager.plan()


@pytest.mark.asyncio
async def test_apply_success(terraform_manager):
    """Test successful Terraform apply."""
    with patch.object(terraform_manager, '_run_terraform_command') as mock_run:
        mock_result = MagicMock()
        mock_result.stdout = 'Apply complete! Resources: 10 added, 0 changed, 0 destroyed.'
        mock_run.return_value = mock_result
        
        result = await terraform_manager.apply()
        
        assert 'Apply complete! Resources: 10 added, 0 changed, 0 destroyed.' in result
        mock_run.assert_called_once_with(['apply'])


@pytest.mark.asyncio
async def test_apply_auto_approve(terraform_manager):
    """Test Terraform apply with auto-approve."""
    with patch.object(terraform_manager, '_run_terraform_command') as mock_run:
        mock_result = MagicMock()
        mock_result.stdout = 'Apply complete!'
        mock_run.return_value = mock_result
        
        result = await terraform_manager.apply(auto_approve=True)
        
        assert 'Apply complete!' in result
        mock_run.assert_called_once_with(['apply', '-auto-approve'])


@pytest.mark.asyncio
async def test_apply_failure(terraform_manager):
    """Test Terraform apply failure."""
    with patch.object(terraform_manager, '_run_terraform_command') as mock_run:
        mock_run.side_effect = RuntimeError('Terraform apply failed')
        
        with pytest.raises(RuntimeError, match="Terraform apply failed"):
            await terraform_manager.apply()


@pytest.mark.asyncio
async def test_destroy_success(terraform_manager):
    """Test successful Terraform destroy."""
    with patch.object(terraform_manager, '_run_terraform_command') as mock_run:
        mock_result = MagicMock()
        mock_result.stdout = 'Destroy complete! Resources: 10 destroyed.'
        mock_run.return_value = mock_result
        
        result = await terraform_manager.destroy()
        
        assert 'Destroy complete! Resources: 10 destroyed.' in result
        mock_run.assert_called_once_with(['destroy'])


@pytest.mark.asyncio
async def test_destroy_auto_approve(terraform_manager):
    """Test Terraform destroy with auto-approve."""
    with patch.object(terraform_manager, '_run_terraform_command') as mock_run:
        mock_result = MagicMock()
        mock_result.stdout = 'Destroy complete!'
        mock_run.return_value = mock_result
        
        result = await terraform_manager.destroy(auto_approve=True)
        
        assert 'Destroy complete!' in result
        mock_run.assert_called_once_with(['destroy', '-auto-approve'])


@pytest.mark.asyncio
async def test_destroy_failure(terraform_manager):
    """Test Terraform destroy failure."""
    with patch.object(terraform_manager, '_run_terraform_command') as mock_run:
        mock_run.side_effect = RuntimeError('Terraform destroy failed')
        
        with pytest.raises(RuntimeError, match="Terraform destroy failed"):
            await terraform_manager.destroy()


@pytest.mark.asyncio
async def test_get_outputs_success(terraform_manager, sample_terraform_output):
    """Test successful Terraform outputs retrieval."""
    with patch.object(terraform_manager, '_run_terraform_command') as mock_run:
        mock_result = MagicMock()
        mock_result.stdout = json.dumps(sample_terraform_output)
        mock_run.return_value = mock_result
        
        outputs = await terraform_manager.get_outputs()
        
        assert outputs == sample_terraform_output
        assert terraform_manager.outputs == sample_terraform_output
        mock_run.assert_called_once_with(['output', '-json'])


@pytest.mark.asyncio
async def test_get_outputs_failure(terraform_manager):
    """Test Terraform outputs retrieval failure."""
    with patch.object(terraform_manager, '_run_terraform_command') as mock_run:
        mock_run.side_effect = RuntimeError('Failed to get outputs')
        
        outputs = await terraform_manager.get_outputs()
        
        assert outputs == {}


@pytest.mark.asyncio
async def test_get_state_success(terraform_manager):
    """Test successful Terraform state retrieval."""
    sample_state = {
        'values': {
            'root_module': {
                'resources': [
                    {
                        'type': 'aws_vpc',
                        'name': 'main',
                        'values': {
                            'id': 'vpc-12345678',
                            'cidr_block': '10.0.0.0/16'
                        }
                    }
                ]
            }
        }
    }
    
    with patch.object(terraform_manager, '_run_terraform_command') as mock_run:
        mock_result = MagicMock()
        mock_result.stdout = json.dumps(sample_state)
        mock_run.return_value = mock_result
        
        state = await terraform_manager.get_state()
        
        assert state == sample_state
        assert terraform_manager.state == sample_state
        mock_run.assert_called_once_with(['show', '-json'])


@pytest.mark.asyncio
async def test_get_state_failure(terraform_manager):
    """Test Terraform state retrieval failure."""
    with patch.object(terraform_manager, '_run_terraform_command') as mock_run:
        mock_run.side_effect = RuntimeError('Failed to get state')
        
        state = await terraform_manager.get_state()
        
        assert state == {}


@pytest.mark.asyncio
async def test_run_terraform_command_success(terraform_manager):
    """Test successful Terraform command execution."""
    with patch('asyncio.create_subprocess_exec') as mock_subprocess:
        mock_process = AsyncMock()
        mock_process.returncode = 0
        mock_process.communicate.return_value = (b'Success', b'')
        mock_subprocess.return_value = mock_process
        
        result = await terraform_manager._run_terraform_command(['plan'])
        
        assert result.returncode == 0
        assert result.stdout == 'Success'
        assert result.stderr == ''


@pytest.mark.asyncio
async def test_run_terraform_command_failure(terraform_manager):
    """Test Terraform command execution failure."""
    with patch('asyncio.create_subprocess_exec') as mock_subprocess:
        mock_process = AsyncMock()
        mock_process.returncode = 1
        mock_process.communicate.return_value = (b'', b'Command failed')
        mock_subprocess.return_value = mock_process
        
        with pytest.raises(RuntimeError, match="Terraform command failed"):
            await terraform_manager._run_terraform_command(['invalid'])


@pytest.mark.asyncio
async def test_cleanup(terraform_manager):
    """Test Terraform manager cleanup."""
    # Add some data
    terraform_manager.state = {'test': 'state'}
    terraform_manager.outputs = {'test': 'output'}
    
    with patch.object(terraform_manager, 'destroy') as mock_destroy, \
         patch('shutil.rmtree') as mock_rmtree:
        
        mock_destroy.return_value = None
        
        await terraform_manager.cleanup()
        
        # Verify cleanup
        mock_destroy.assert_called_once_with(auto_approve=True)
        mock_rmtree.assert_called_once_with(terraform_manager.working_dir)
        assert terraform_manager.state == {}
        assert terraform_manager.outputs == {}


@pytest.mark.asyncio
async def test_terraform_manager_with_custom_config():
    """Test Terraform manager with custom configuration."""
    config = {
        'working_dir': './custom-terraform',
        'environment': 'staging',
        'region': 'eu-west-1',
        'project_name': 'custom-project'
    }
    
    manager = TerraformManager(config)
    
    assert manager.working_dir == './custom-terraform'
    assert manager.environment == 'staging'
    assert manager.region == 'eu-west-1'
    assert manager.project_name == 'custom-project'
    
    # Test resource configurations use custom project name
    assert manager.resources['vpc']['name'] == 'custom-project-vpc'
    assert manager.resources['eks_cluster']['name'] == 'custom-project-cluster'
    
    # Test provider configurations use custom region
    assert manager.providers['aws']['region'] == 'eu-west-1'


@pytest.mark.asyncio
async def test_terraform_manager_default_config():
    """Test Terraform manager with default configuration."""
    manager = TerraformManager()
    
    assert manager.working_dir == './terraform'
    assert manager.environment == 'production'
    assert manager.region == 'us-west-2'
    assert manager.project_name == 'pocket-hedge-fund'
    
    # Test default resource configurations
    assert manager.resources['vpc']['name'] == 'pocket-hedge-fund-vpc'
    assert manager.resources['eks_cluster']['name'] == 'pocket-hedge-fund-cluster'
    
    # Test default provider configurations
    assert manager.providers['aws']['region'] == 'us-west-2'


@pytest.mark.asyncio
async def test_terraform_manager_resource_configurations():
    """Test Terraform manager resource configurations."""
    manager = TerraformManager()
    
    # Test VPC configuration
    vpc_config = manager.resources['vpc']
    assert vpc_config['type'] == 'aws_vpc'
    assert vpc_config['cidr_block'] == '10.0.0.0/16'
    assert vpc_config['enable_dns_hostnames'] is True
    assert vpc_config['enable_dns_support'] is True
    
    # Test EKS cluster configuration
    eks_config = manager.resources['eks_cluster']
    assert eks_config['version'] == '1.28'
    assert 'node_groups' in eks_config
    assert 'general' in eks_config['node_groups']
    
    # Test RDS configuration
    rds_config = manager.resources['rds']
    assert rds_config['engine'] == 'postgres'
    assert rds_config['engine_version'] == '15.4'
    assert rds_config['instance_class'] == 'db.t3.micro'
    assert rds_config['allocated_storage'] == 20
    assert rds_config['storage_encrypted'] is True
    
    # Test ElastiCache configuration
    cache_config = manager.resources['elasticache']
    assert cache_config['engine'] == 'redis'
    assert cache_config['node_type'] == 'cache.t3.micro'
    assert cache_config['num_cache_nodes'] == 1


@pytest.mark.asyncio
async def test_terraform_manager_provider_configurations():
    """Test Terraform manager provider configurations."""
    manager = TerraformManager()
    
    # Test AWS provider
    aws_provider = manager.providers['aws']
    assert aws_provider['source'] == 'hashicorp/aws'
    assert aws_provider['version'] == '~> 5.0'
    assert aws_provider['region'] == 'us-west-2'
    
    # Test Kubernetes provider
    k8s_provider = manager.providers['kubernetes']
    assert k8s_provider['source'] == 'hashicorp/kubernetes'
    assert k8s_provider['version'] == '~> 2.0'
    
    # Test Helm provider
    helm_provider = manager.providers['helm']
    assert helm_provider['source'] == 'hashicorp/helm'
    assert helm_provider['version'] == '~> 2.0'
