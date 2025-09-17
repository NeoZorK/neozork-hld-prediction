"""
Terraform Manager

Main orchestrator for Infrastructure as Code with Terraform.
"""

import asyncio
import logging
import json
import os
from datetime import datetime
from typing import Dict, List, Optional, Any, Union
from pathlib import Path

logger = logging.getLogger(__name__)


class TerraformManager:
    """
    Main Terraform manager for infrastructure provisioning.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize Terraform manager."""
        self.config = config or {}
        self.working_dir = self.config.get('working_dir', './terraform')
        self.environment = self.config.get('environment', 'production')
        self.region = self.config.get('region', 'us-west-2')
        self.project_name = self.config.get('project_name', 'pocket-hedge-fund')
        
        # Provider configurations
        self.providers = {
            'aws': {
                'source': 'hashicorp/aws',
                'version': '~> 5.0',
                'region': self.region
            },
            'kubernetes': {
                'source': 'hashicorp/kubernetes',
                'version': '~> 2.0'
            },
            'helm': {
                'source': 'hashicorp/helm',
                'version': '~> 2.0'
            }
        }
        
        # Resource configurations
        self.resources = {
            'vpc': {
                'type': 'aws_vpc',
                'name': f'{self.project_name}-vpc',
                'cidr_block': '10.0.0.0/16',
                'enable_dns_hostnames': True,
                'enable_dns_support': True
            },
            'subnets': {
                'public': [
                    {'cidr': '10.0.1.0/24', 'az': 'a'},
                    {'cidr': '10.0.2.0/24', 'az': 'b'}
                ],
                'private': [
                    {'cidr': '10.0.10.0/24', 'az': 'a'},
                    {'cidr': '10.0.20.0/24', 'az': 'b'}
                ]
            },
            'eks_cluster': {
                'name': f'{self.project_name}-cluster',
                'version': '1.28',
                'node_groups': {
                    'general': {
                        'instance_types': ['t3.medium'],
                        'min_size': 1,
                        'max_size': 3,
                        'desired_size': 2
                    }
                }
            },
            'rds': {
                'instance_class': 'db.t3.micro',
                'engine': 'postgres',
                'engine_version': '15.4',
                'allocated_storage': 20,
                'storage_encrypted': True
            },
            'elasticache': {
                'node_type': 'cache.t3.micro',
                'engine': 'redis',
                'num_cache_nodes': 1
            }
        }
        
        self.state = {}
        self.outputs = {}
    
    async def initialize(self):
        """Initialize Terraform workspace."""
        try:
            # Create working directory
            Path(self.working_dir).mkdir(parents=True, exist_ok=True)
            
            # Initialize Terraform
            await self._run_terraform_command(['init'])
            
            # Create main configuration
            await self._create_main_config()
            
            # Create variables file
            await self._create_variables_file()
            
            # Create outputs file
            await self._create_outputs_file()
            
            logger.info("Terraform manager initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Terraform manager: {e}")
            raise
    
    async def _create_main_config(self):
        """Create main Terraform configuration file."""
        try:
            config_content = f"""
# Pocket Hedge Fund Infrastructure
terraform {{
  required_version = ">= 1.0"
  
  required_providers {{
    aws = {{
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }}
    kubernetes = {{
      source  = "hashicorp/kubernetes"
      version = "~> 2.0"
    }}
    helm = {{
      source  = "hashicorp/helm"
      version = "~> 2.0"
    }}
  }}
  
  backend "s3" {{
    bucket = "{self.project_name}-terraform-state"
    key    = "{self.environment}/terraform.tfstate"
    region = "{self.region}"
  }}
}}

# AWS Provider
provider "aws" {{
  region = var.aws_region
  
  default_tags {{
    tags = {{
      Project     = var.project_name
      Environment = var.environment
      ManagedBy   = "terraform"
    }}
  }}
}}

# Kubernetes Provider
provider "kubernetes" {{
  host                   = aws_eks_cluster.cluster.endpoint
  cluster_ca_certificate = base64decode(aws_eks_cluster.cluster.certificate_authority[0].data)
  
  exec {{
    api_version = "client.authentication.k8s.io/v1beta1"
    command     = "aws"
    args        = ["eks", "get-token", "--cluster-name", aws_eks_cluster.cluster.name]
  }}
}}

# Helm Provider
provider "helm" {{
  kubernetes {{
    host                   = aws_eks_cluster.cluster.endpoint
    cluster_ca_certificate = base64decode(aws_eks_cluster.cluster.certificate_authority[0].data)
    
    exec {{
      api_version = "client.authentication.k8s.io/v1beta1"
      command     = "aws"
      args        = ["eks", "get-token", "--cluster-name", aws_eks_cluster.cluster.name]
    }}
  }}
}}

# Data sources
data "aws_availability_zones" "available" {{
  state = "available"
}}

data "aws_caller_identity" "current" {{}}

# VPC
resource "aws_vpc" "main" {{
  cidr_block           = var.vpc_cidr
  enable_dns_hostnames = true
  enable_dns_support   = true
  
  tags = {{
    Name = "${{var.project_name}}-vpc"
  }}
}}

# Internet Gateway
resource "aws_internet_gateway" "main" {{
  vpc_id = aws_vpc.main.id
  
  tags = {{
    Name = "${{var.project_name}}-igw"
  }}
}}

# Public Subnets
resource "aws_subnet" "public" {{
  count = length(var.public_subnet_cidrs)
  
  vpc_id                  = aws_vpc.main.id
  cidr_block              = var.public_subnet_cidrs[count.index]
  availability_zone       = data.aws_availability_zones.available.names[count.index]
  map_public_ip_on_launch = true
  
  tags = {{
    Name = "${{var.project_name}}-public-subnet-${{count.index + 1}}"
    Type = "public"
  }}
}}

# Private Subnets
resource "aws_subnet" "private" {{
  count = length(var.private_subnet_cidrs)
  
  vpc_id            = aws_vpc.main.id
  cidr_block        = var.private_subnet_cidrs[count.index]
  availability_zone = data.aws_availability_zones.available.names[count.index]
  
  tags = {{
    Name = "${{var.project_name}}-private-subnet-${{count.index + 1}}"
    Type = "private"
  }}
}}

# NAT Gateway
resource "aws_eip" "nat" {{
  count = length(aws_subnet.public)
  
  domain = "vpc"
  
  tags = {{
    Name = "${{var.project_name}}-nat-eip-${{count.index + 1}}"
  }}
}}

resource "aws_nat_gateway" "main" {{
  count = length(aws_subnet.public)
  
  allocation_id = aws_eip.nat[count.index].id
  subnet_id     = aws_subnet.public[count.index].id
  
  tags = {{
    Name = "${{var.project_name}}-nat-gateway-${{count.index + 1}}"
  }}
  
  depends_on = [aws_internet_gateway.main]
}}

# Route Tables
resource "aws_route_table" "public" {{
  vpc_id = aws_vpc.main.id
  
  route {{
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.main.id
  }}
  
  tags = {{
    Name = "${{var.project_name}}-public-rt"
  }}
}}

resource "aws_route_table" "private" {{
  count = length(aws_subnet.private)
  
  vpc_id = aws_vpc.main.id
  
  route {{
    cidr_block     = "0.0.0.0/0"
    nat_gateway_id = aws_nat_gateway.main[count.index].id
  }}
  
  tags = {{
    Name = "${{var.project_name}}-private-rt-${{count.index + 1}}"
  }}
}}

# Route Table Associations
resource "aws_route_table_association" "public" {{
  count = length(aws_subnet.public)
  
  subnet_id      = aws_subnet.public[count.index].id
  route_table_id = aws_route_table.public.id
}}

resource "aws_route_table_association" "private" {{
  count = length(aws_subnet.private)
  
  subnet_id      = aws_subnet.private[count.index].id
  route_table_id = aws_route_table.private[count.index].id
}}

# EKS Cluster
resource "aws_eks_cluster" "cluster" {{
  name     = var.cluster_name
  role_arn = aws_iam_role.eks_cluster.arn
  version  = var.cluster_version
  
  vpc_config {{
    subnet_ids = concat(aws_subnet.public[*].id, aws_subnet.private[*].id)
  }}
  
  depends_on = [
    aws_cloudwatch_log_group.eks_cluster,
    aws_iam_role_policy_attachment.eks_cluster_AmazonEKSClusterPolicy,
  ]
}}

# EKS Cluster IAM Role
resource "aws_iam_role" "eks_cluster" {{
  name = "${{var.project_name}}-eks-cluster-role"
  
  assume_role_policy = jsonencode({{
    Statement = [{{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {{
        Service = "eks.amazonaws.com"
      }}
    }}]
    Version = "2012-10-17"
  }})
}}

resource "aws_iam_role_policy_attachment" "eks_cluster_AmazonEKSClusterPolicy" {{
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSClusterPolicy"
  role       = aws_iam_role.eks_cluster.name
}}

# EKS Node Group
resource "aws_eks_node_group" "general" {{
  cluster_name    = aws_eks_cluster.cluster.name
  node_group_name = "general"
  node_role_arn   = aws_iam_role.eks_node_group.arn
  subnet_ids      = aws_subnet.private[*].id
  
  scaling_config {{
    desired_size = var.node_group_desired_size
    max_size     = var.node_group_max_size
    min_size     = var.node_group_min_size
  }}
  
  instance_types = var.node_group_instance_types
  
  depends_on = [
    aws_iam_role_policy_attachment.eks_node_group_AmazonEKSWorkerNodePolicy,
    aws_iam_role_policy_attachment.eks_node_group_AmazonEKS_CNI_Policy,
    aws_iam_role_policy_attachment.eks_node_group_AmazonEC2ContainerRegistryReadOnly,
  ]
}}

# EKS Node Group IAM Role
resource "aws_iam_role" "eks_node_group" {{
  name = "${{var.project_name}}-eks-node-group-role"
  
  assume_role_policy = jsonencode({{
    Statement = [{{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {{
        Service = "ec2.amazonaws.com"
      }}
    }}]
    Version = "2012-10-17"
  }})
}}

resource "aws_iam_role_policy_attachment" "eks_node_group_AmazonEKSWorkerNodePolicy" {{
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSWorkerNodePolicy"
  role       = aws_iam_role.eks_node_group.name
}}

resource "aws_iam_role_policy_attachment" "eks_node_group_AmazonEKS_CNI_Policy" {{
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy"
  role       = aws_iam_role.eks_node_group.name
}}

resource "aws_iam_role_policy_attachment" "eks_node_group_AmazonEC2ContainerRegistryReadOnly" {{
  policy_arn = "arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly"
  role       = aws_iam_role.eks_node_group.name
}}

# CloudWatch Log Group
resource "aws_cloudwatch_log_group" "eks_cluster" {{
  name              = "/aws/eks/${{var.cluster_name}}/cluster"
  retention_in_days = 7
}}

# RDS Subnet Group
resource "aws_db_subnet_group" "main" {{
  name       = "${{var.project_name}}-db-subnet-group"
  subnet_ids = aws_subnet.private[*].id
  
  tags = {{
    Name = "${{var.project_name}}-db-subnet-group"
  }}
}}

# RDS Instance
resource "aws_db_instance" "main" {{
  identifier = "${{var.project_name}}-db"
  
  engine         = var.db_engine
  engine_version = var.db_engine_version
  instance_class = var.db_instance_class
  
  allocated_storage     = var.db_allocated_storage
  max_allocated_storage = var.db_max_allocated_storage
  storage_encrypted     = true
  
  db_name  = var.db_name
  username = var.db_username
  password = var.db_password
  
  vpc_security_group_ids = [aws_security_group.rds.id]
  db_subnet_group_name   = aws_db_subnet_group.main.name
  
  backup_retention_period = 7
  backup_window          = "03:00-04:00"
  maintenance_window     = "sun:04:00-sun:05:00"
  
  skip_final_snapshot = var.environment != "production"
  
  tags = {{
    Name = "${{var.project_name}}-db"
  }}
}}

# ElastiCache Subnet Group
resource "aws_elasticache_subnet_group" "main" {{
  name       = "${{var.project_name}}-cache-subnet-group"
  subnet_ids = aws_subnet.private[*].id
}}

# ElastiCache Cluster
resource "aws_elasticache_replication_group" "main" {{
  replication_group_id       = "${{var.project_name}}-redis"
  description                = "Redis cluster for ${{var.project_name}}"
  
  node_type            = var.cache_node_type
  port                 = 6379
  parameter_group_name = "default.redis7"
  
  num_cache_clusters = var.cache_num_nodes
  
  subnet_group_name  = aws_elasticache_subnet_group.main.name
  security_group_ids = [aws_security_group.elasticache.id]
  
  at_rest_encryption_enabled = true
  transit_encryption_enabled = true
  
  tags = {{
    Name = "${{var.project_name}}-redis"
  }}
}}

# Security Groups
resource "aws_security_group" "eks_cluster" {{
  name_prefix = "${{var.project_name}}-eks-cluster-"
  vpc_id      = aws_vpc.main.id
  
  egress {{
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }}
  
  tags = {{
    Name = "${{var.project_name}}-eks-cluster-sg"
  }}
}}

resource "aws_security_group" "rds" {{
  name_prefix = "${{var.project_name}}-rds-"
  vpc_id      = aws_vpc.main.id
  
  ingress {{
    from_port       = 5432
    to_port         = 5432
    protocol        = "tcp"
    security_groups = [aws_security_group.eks_cluster.id]
  }}
  
  egress {{
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }}
  
  tags = {{
    Name = "${{var.project_name}}-rds-sg"
  }}
}}

resource "aws_security_group" "elasticache" {{
  name_prefix = "${{var.project_name}}-elasticache-"
  vpc_id      = aws_vpc.main.id
  
  ingress {{
    from_port       = 6379
    to_port         = 6379
    protocol        = "tcp"
    security_groups = [aws_security_group.eks_cluster.id]
  }}
  
  egress {{
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }}
  
  tags = {{
    Name = "${{var.project_name}}-elasticache-sg"
  }}
}}
"""
            
            config_file = Path(self.working_dir) / 'main.tf'
            config_file.write_text(config_content)
            
            logger.info("Created main Terraform configuration")
        except Exception as e:
            logger.error(f"Failed to create main configuration: {e}")
            raise
    
    async def _create_variables_file(self):
        """Create variables file."""
        try:
            variables_content = f"""
# Project Configuration
variable "project_name" {{
  description = "Name of the project"
  type        = string
  default     = "{self.project_name}"
}}

variable "environment" {{
  description = "Environment name"
  type        = string
  default     = "{self.environment}"
}}

variable "aws_region" {{
  description = "AWS region"
  type        = string
  default     = "{self.region}"
}}

# VPC Configuration
variable "vpc_cidr" {{
  description = "CIDR block for VPC"
  type        = string
  default     = "10.0.0.0/16"
}}

variable "public_subnet_cidrs" {{
  description = "CIDR blocks for public subnets"
  type        = list(string)
  default     = ["10.0.1.0/24", "10.0.2.0/24"]
}}

variable "private_subnet_cidrs" {{
  description = "CIDR blocks for private subnets"
  type        = list(string)
  default     = ["10.0.10.0/24", "10.0.20.0/24"]
}}

# EKS Configuration
variable "cluster_name" {{
  description = "Name of the EKS cluster"
  type        = string
  default     = "{self.project_name}-cluster"
}}

variable "cluster_version" {{
  description = "Kubernetes version for EKS cluster"
  type        = string
  default     = "1.28"
}}

variable "node_group_instance_types" {{
  description = "Instance types for EKS node group"
  type        = list(string)
  default     = ["t3.medium"]
}}

variable "node_group_desired_size" {{
  description = "Desired number of nodes in EKS node group"
  type        = number
  default     = 2
}}

variable "node_group_max_size" {{
  description = "Maximum number of nodes in EKS node group"
  type        = number
  default     = 3
}}

variable "node_group_min_size" {{
  description = "Minimum number of nodes in EKS node group"
  type        = number
  default     = 1
}}

# Database Configuration
variable "db_engine" {{
  description = "Database engine"
  type        = string
  default     = "postgres"
}}

variable "db_engine_version" {{
  description = "Database engine version"
  type        = string
  default     = "15.4"
}}

variable "db_instance_class" {{
  description = "Database instance class"
  type        = string
  default     = "db.t3.micro"
}}

variable "db_allocated_storage" {{
  description = "Database allocated storage in GB"
  type        = number
  default     = 20
}}

variable "db_max_allocated_storage" {{
  description = "Database maximum allocated storage in GB"
  type        = number
  default     = 100
}}

variable "db_name" {{
  description = "Database name"
  type        = string
  default     = "pocket_hedge_fund"
}}

variable "db_username" {{
  description = "Database username"
  type        = string
  default     = "postgres"
}}

variable "db_password" {{
  description = "Database password"
  type        = string
  sensitive   = true
}}

# Cache Configuration
variable "cache_node_type" {{
  description = "ElastiCache node type"
  type        = string
  default     = "cache.t3.micro"
}}

variable "cache_num_nodes" {{
  description = "Number of cache nodes"
  type        = number
  default     = 1
}}
"""
            
            variables_file = Path(self.working_dir) / 'variables.tf'
            variables_file.write_text(variables_content)
            
            logger.info("Created variables file")
        except Exception as e:
            logger.error(f"Failed to create variables file: {e}")
            raise
    
    async def _create_outputs_file(self):
        """Create outputs file."""
        try:
            outputs_content = f"""
# VPC Outputs
output "vpc_id" {{
  description = "ID of the VPC"
  value       = aws_vpc.main.id
}}

output "vpc_cidr_block" {{
  description = "CIDR block of the VPC"
  value       = aws_vpc.main.cidr_block
}}

# Subnet Outputs
output "public_subnet_ids" {{
  description = "IDs of the public subnets"
  value       = aws_subnet.public[*].id
}}

output "private_subnet_ids" {{
  description = "IDs of the private subnets"
  value       = aws_subnet.private[*].id
}}

# EKS Outputs
output "cluster_id" {{
  description = "ID of the EKS cluster"
  value       = aws_eks_cluster.cluster.id
}}

output "cluster_arn" {{
  description = "ARN of the EKS cluster"
  value       = aws_eks_cluster.cluster.arn
}}

output "cluster_endpoint" {{
  description = "Endpoint of the EKS cluster"
  value       = aws_eks_cluster.cluster.endpoint
}}

output "cluster_security_group_id" {{
  description = "Security group ID of the EKS cluster"
  value       = aws_eks_cluster.cluster.vpc_config[0].cluster_security_group_id
}}

output "cluster_certificate_authority_data" {{
  description = "Certificate authority data of the EKS cluster"
  value       = aws_eks_cluster.cluster.certificate_authority[0].data
}}

# Database Outputs
output "db_endpoint" {{
  description = "Endpoint of the RDS instance"
  value       = aws_db_instance.main.endpoint
}}

output "db_port" {{
  description = "Port of the RDS instance"
  value       = aws_db_instance.main.port
}}

output "db_name" {{
  description = "Name of the database"
  value       = aws_db_instance.main.db_name
}}

# Cache Outputs
output "cache_endpoint" {{
  description = "Endpoint of the ElastiCache cluster"
  value       = aws_elasticache_replication_group.main.primary_endpoint_address
}}

output "cache_port" {{
  description = "Port of the ElastiCache cluster"
  value       = aws_elasticache_replication_group.main.port
}}
"""
            
            outputs_file = Path(self.working_dir) / 'outputs.tf'
            outputs_file.write_text(outputs_content)
            
            logger.info("Created outputs file")
        except Exception as e:
            logger.error(f"Failed to create outputs file: {e}")
            raise
    
    async def plan(self) -> str:
        """Run Terraform plan."""
        try:
            result = await self._run_terraform_command(['plan'])
            return result.stdout
        except Exception as e:
            logger.error(f"Terraform plan failed: {e}")
            raise
    
    async def apply(self, auto_approve: bool = False) -> str:
        """Run Terraform apply."""
        try:
            cmd = ['apply']
            if auto_approve:
                cmd.append('-auto-approve')
            
            result = await self._run_terraform_command(cmd)
            return result.stdout
        except Exception as e:
            logger.error(f"Terraform apply failed: {e}")
            raise
    
    async def destroy(self, auto_approve: bool = False) -> str:
        """Run Terraform destroy."""
        try:
            cmd = ['destroy']
            if auto_approve:
                cmd.append('-auto-approve')
            
            result = await self._run_terraform_command(cmd)
            return result.stdout
        except Exception as e:
            logger.error(f"Terraform destroy failed: {e}")
            raise
    
    async def get_outputs(self) -> Dict[str, Any]:
        """Get Terraform outputs."""
        try:
            result = await self._run_terraform_command(['output', '-json'])
            outputs = json.loads(result.stdout)
            self.outputs = outputs
            return outputs
        except Exception as e:
            logger.error(f"Failed to get Terraform outputs: {e}")
            return {}
    
    async def get_state(self) -> Dict[str, Any]:
        """Get Terraform state."""
        try:
            result = await self._run_terraform_command(['show', '-json'])
            state = json.loads(result.stdout)
            self.state = state
            return state
        except Exception as e:
            logger.error(f"Failed to get Terraform state: {e}")
            return {}
    
    async def _run_terraform_command(self, cmd: List[str]) -> Any:
        """Run Terraform command."""
        try:
            full_cmd = ['terraform'] + cmd
            
            process = await asyncio.create_subprocess_exec(
                *full_cmd,
                cwd=self.working_dir,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await process.communicate()
            
            if process.returncode != 0:
                raise RuntimeError(f"Terraform command failed: {stderr.decode()}")
            
            return type('Result', (), {
                'returncode': process.returncode,
                'stdout': stdout.decode('utf-8'),
                'stderr': stderr.decode('utf-8')
            })()
            
        except Exception as e:
            logger.error(f"Terraform command execution failed: {e}")
            raise
    
    async def cleanup(self):
        """Cleanup Terraform resources."""
        try:
            # Destroy infrastructure
            await self.destroy(auto_approve=True)
            
            # Clean up working directory
            import shutil
            if Path(self.working_dir).exists():
                shutil.rmtree(self.working_dir)
            
            self.state = {}
            self.outputs = {}
            
            logger.info("Terraform manager cleanup completed")
        except Exception as e:
            logger.error(f"Error during Terraform manager cleanup: {e}")
