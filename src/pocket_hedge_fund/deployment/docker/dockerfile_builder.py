"""
Dockerfile Builder

Generates optimized Dockerfiles for different services and environments.
"""

import logging
from typing import Dict, List, Optional, Any
from pathlib import Path

logger = logging.getLogger(__name__)


class DockerfileBuilder:
    """
    Builder for generating optimized Dockerfiles.
    """
    
    def __init__(self, base_config: Optional[Dict[str, Any]] = None):
        """Initialize Dockerfile builder."""
        self.base_config = base_config or {}
        self.templates = self._load_templates()
    
    def _load_templates(self) -> Dict[str, Dict[str, Any]]:
        """Load Dockerfile templates for different service types."""
        return {
            'python_fastapi': {
                'base_image': 'python:3.11-slim',
                'stages': ['builder', 'runtime'],
                'dependencies': ['uv', 'build-essential', 'libpq-dev'],
                'runtime_deps': ['libpq5'],
                'optimizations': ['multi_stage', 'non_root_user', 'health_check']
            },
            'python_django': {
                'base_image': 'python:3.11-slim',
                'stages': ['builder', 'runtime'],
                'dependencies': ['uv', 'build-essential', 'libpq-dev', 'gettext'],
                'runtime_deps': ['libpq5'],
                'optimizations': ['multi_stage', 'non_root_user', 'static_files']
            },
            'node_react': {
                'base_image': 'node:18-alpine',
                'stages': ['builder', 'runtime'],
                'dependencies': ['npm', 'yarn'],
                'runtime_deps': ['nginx'],
                'optimizations': ['multi_stage', 'nginx_serve', 'compression']
            },
            'postgres': {
                'base_image': 'postgres:15-alpine',
                'stages': ['runtime'],
                'dependencies': [],
                'runtime_deps': ['postgresql-client'],
                'optimizations': ['custom_config', 'backup_scripts']
            },
            'redis': {
                'base_image': 'redis:7-alpine',
                'stages': ['runtime'],
                'dependencies': [],
                'runtime_deps': [],
                'optimizations': ['custom_config', 'persistence']
            },
            'nginx': {
                'base_image': 'nginx:alpine',
                'stages': ['runtime'],
                'dependencies': [],
                'runtime_deps': ['openssl'],
                'optimizations': ['ssl_config', 'compression', 'security_headers']
            }
        }
    
    def build_dockerfile(
        self,
        service_type: str,
        service_config: Dict[str, Any],
        output_path: str
    ) -> str:
        """Build Dockerfile for specific service type."""
        try:
            if service_type not in self.templates:
                raise ValueError(f"Unknown service type: {service_type}")
            
            template = self.templates[service_type]
            dockerfile_content = self._generate_dockerfile(template, service_config)
            
            # Write to file
            output_file = Path(output_path)
            output_file.parent.mkdir(parents=True, exist_ok=True)
            output_file.write_text(dockerfile_content)
            
            logger.info(f"Generated Dockerfile for {service_type} at {output_path}")
            return dockerfile_content
            
        except Exception as e:
            logger.error(f"Failed to build Dockerfile for {service_type}: {e}")
            raise
    
    def _generate_dockerfile(
        self,
        template: Dict[str, Any],
        service_config: Dict[str, Any]
    ) -> str:
        """Generate Dockerfile content from template."""
        try:
            lines = []
            
            # Add header comment
            lines.append("# Generated Dockerfile for Pocket Hedge Fund")
            lines.append(f"# Service: {service_config.get('name', 'unknown')}")
            lines.append(f"# Environment: {service_config.get('environment', 'production')}")
            lines.append("")
            
            # Multi-stage build
            if 'multi_stage' in template.get('optimizations', []):
                lines.extend(self._generate_multi_stage_dockerfile(template, service_config))
            else:
                lines.extend(self._generate_single_stage_dockerfile(template, service_config))
            
            return '\n'.join(lines)
            
        except Exception as e:
            logger.error(f"Failed to generate Dockerfile content: {e}")
            raise
    
    def _generate_multi_stage_dockerfile(
        self,
        template: Dict[str, Any],
        service_config: Dict[str, Any]
    ) -> List[str]:
        """Generate multi-stage Dockerfile."""
        lines = []
        
        # Builder stage
        lines.append("# Builder stage")
        lines.append(f"FROM {template['base_image']} AS builder")
        lines.append("")
        
        # Set working directory
        lines.append("WORKDIR /app")
        lines.append("")
        
        # Install build dependencies
        if template.get('dependencies'):
            deps = ' '.join(template['dependencies'])
            lines.append(f"RUN apt-get update && apt-get install -y {deps} && rm -rf /var/lib/apt/lists/*")
            lines.append("")
        
        # Copy dependency files
        if service_config.get('dependency_files'):
            for file in service_config['dependency_files']:
                lines.append(f"COPY {file} ./")
        lines.append("")
        
        # Install dependencies
        if service_config.get('package_manager') == 'uv':
            lines.append("RUN uv pip install --system --no-cache -r requirements.txt")
        elif service_config.get('package_manager') == 'pip':
            lines.append("RUN pip install --no-cache-dir -r requirements.txt")
        elif service_config.get('package_manager') == 'npm':
            lines.append("RUN npm ci --only=production")
        lines.append("")
        
        # Copy source code
        lines.append("COPY . .")
        lines.append("")
        
        # Build application
        if service_config.get('build_command'):
            lines.append(f"RUN {service_config['build_command']}")
            lines.append("")
        
        # Runtime stage
        lines.append("# Runtime stage")
        lines.append(f"FROM {template['base_image']} AS runtime")
        lines.append("")
        
        # Install runtime dependencies
        if template.get('runtime_deps'):
            deps = ' '.join(template['runtime_deps'])
            lines.append(f"RUN apt-get update && apt-get install -y {deps} && rm -rf /var/lib/apt/lists/*")
            lines.append("")
        
        # Create non-root user
        if 'non_root_user' in template.get('optimizations', []):
            lines.append("RUN groupadd -r appuser && useradd -r -g appuser appuser")
            lines.append("")
        
        # Set working directory
        lines.append("WORKDIR /app")
        lines.append("")
        
        # Copy from builder stage
        if service_config.get('copy_from_builder'):
            for src, dst in service_config['copy_from_builder'].items():
                lines.append(f"COPY --from=builder {src} {dst}")
        else:
            lines.append("COPY --from=builder /app .")
        lines.append("")
        
        # Set ownership
        if 'non_root_user' in template.get('optimizations', []):
            lines.append("RUN chown -R appuser:appuser /app")
            lines.append("USER appuser")
            lines.append("")
        
        # Expose port
        if service_config.get('port'):
            lines.append(f"EXPOSE {service_config['port']}")
            lines.append("")
        
        # Health check
        if 'health_check' in template.get('optimizations', []):
            health_cmd = service_config.get('health_check_command', 'curl -f http://localhost:8000/health || exit 1')
            lines.append(f"HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \\")
            lines.append(f"  CMD {health_cmd}")
            lines.append("")
        
        # Start command
        start_cmd = service_config.get('start_command', 'python main.py')
        lines.append(f"CMD [\"{start_cmd}\"]")
        
        return lines
    
    def _generate_single_stage_dockerfile(
        self,
        template: Dict[str, Any],
        service_config: Dict[str, Any]
    ) -> List[str]:
        """Generate single-stage Dockerfile."""
        lines = []
        
        # Base image
        lines.append(f"FROM {template['base_image']}")
        lines.append("")
        
        # Set working directory
        lines.append("WORKDIR /app")
        lines.append("")
        
        # Install dependencies
        if template.get('dependencies'):
            deps = ' '.join(template['dependencies'])
            lines.append(f"RUN apt-get update && apt-get install -y {deps} && rm -rf /var/lib/apt/lists/*")
            lines.append("")
        
        # Copy dependency files
        if service_config.get('dependency_files'):
            for file in service_config['dependency_files']:
                lines.append(f"COPY {file} ./")
        lines.append("")
        
        # Install application dependencies
        if service_config.get('package_manager') == 'uv':
            lines.append("RUN uv pip install --system --no-cache -r requirements.txt")
        elif service_config.get('package_manager') == 'pip':
            lines.append("RUN pip install --no-cache-dir -r requirements.txt")
        elif service_config.get('package_manager') == 'npm':
            lines.append("RUN npm ci --only=production")
        lines.append("")
        
        # Copy source code
        lines.append("COPY . .")
        lines.append("")
        
        # Build application
        if service_config.get('build_command'):
            lines.append(f"RUN {service_config['build_command']}")
            lines.append("")
        
        # Create non-root user
        if 'non_root_user' in template.get('optimizations', []):
            lines.append("RUN groupadd -r appuser && useradd -r -g appuser appuser")
            lines.append("RUN chown -R appuser:appuser /app")
            lines.append("USER appuser")
            lines.append("")
        
        # Expose port
        if service_config.get('port'):
            lines.append(f"EXPOSE {service_config['port']}")
            lines.append("")
        
        # Health check
        if 'health_check' in template.get('optimizations', []):
            health_cmd = service_config.get('health_check_command', 'curl -f http://localhost:8000/health || exit 1')
            lines.append(f"HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \\")
            lines.append(f"  CMD {health_cmd}")
            lines.append("")
        
        # Start command
        start_cmd = service_config.get('start_command', 'python main.py')
        lines.append(f"CMD [\"{start_cmd}\"]")
        
        return lines
    
    def build_python_fastapi_dockerfile(
        self,
        service_name: str,
        output_path: str,
        environment: str = 'production'
    ) -> str:
        """Build Dockerfile for Python FastAPI service."""
        service_config = {
            'name': service_name,
            'environment': environment,
            'package_manager': 'uv',
            'dependency_files': ['requirements.txt', 'pyproject.toml'],
            'port': 8000,
            'start_command': 'uvicorn src.pocket_hedge_fund.main:app --host 0.0.0.0 --port 8000',
            'health_check_command': 'curl -f http://localhost:8000/health || exit 1',
            'copy_from_builder': {
                '/app/src': '/app/src',
                '/app/requirements.txt': '/app/requirements.txt',
                '/app/pyproject.toml': '/app/pyproject.toml'
            }
        }
        
        return self.build_dockerfile('python_fastapi', service_config, output_path)
    
    def build_python_django_dockerfile(
        self,
        service_name: str,
        output_path: str,
        environment: str = 'production'
    ) -> str:
        """Build Dockerfile for Python Django service."""
        service_config = {
            'name': service_name,
            'environment': environment,
            'package_manager': 'uv',
            'dependency_files': ['requirements.txt', 'pyproject.toml'],
            'port': 8000,
            'start_command': 'python manage.py runserver 0.0.0.0:8000',
            'health_check_command': 'curl -f http://localhost:8000/health/ || exit 1',
            'build_command': 'python manage.py collectstatic --noinput',
            'copy_from_builder': {
                '/app/src': '/app/src',
                '/app/static': '/app/static',
                '/app/requirements.txt': '/app/requirements.txt'
            }
        }
        
        return self.build_dockerfile('python_django', service_config, output_path)
    
    def build_node_react_dockerfile(
        self,
        service_name: str,
        output_path: str,
        environment: str = 'production'
    ) -> str:
        """Build Dockerfile for Node.js React service."""
        service_config = {
            'name': service_name,
            'environment': environment,
            'package_manager': 'npm',
            'dependency_files': ['package.json', 'package-lock.json'],
            'port': 3000,
            'start_command': 'npm start',
            'build_command': 'npm run build',
            'copy_from_builder': {
                '/app/build': '/usr/share/nginx/html',
                '/app/nginx.conf': '/etc/nginx/nginx.conf'
            }
        }
        
        return self.build_dockerfile('node_react', service_config, output_path)
    
    def build_postgres_dockerfile(
        self,
        service_name: str,
        output_path: str,
        environment: str = 'production'
    ) -> str:
        """Build Dockerfile for PostgreSQL service."""
        service_config = {
            'name': service_name,
            'environment': environment,
            'port': 5432,
            'start_command': 'postgres',
            'copy_from_builder': {
                '/app/init.sql': '/docker-entrypoint-initdb.d/init.sql',
                '/app/postgresql.conf': '/etc/postgresql/postgresql.conf'
            }
        }
        
        return self.build_dockerfile('postgres', service_config, output_path)
    
    def build_nginx_dockerfile(
        self,
        service_name: str,
        output_path: str,
        environment: str = 'production'
    ) -> str:
        """Build Dockerfile for Nginx service."""
        service_config = {
            'name': service_name,
            'environment': environment,
            'port': 80,
            'start_command': 'nginx -g "daemon off;"',
            'copy_from_builder': {
                '/app/nginx.conf': '/etc/nginx/nginx.conf',
                '/app/ssl': '/etc/nginx/ssl'
            }
        }
        
        return self.build_dockerfile('nginx', service_config, output_path)
    
    def generate_dockerignore(self, output_path: str) -> str:
        """Generate .dockerignore file."""
        dockerignore_content = """# Git
.git
.gitignore

# Documentation
README.md
docs/
*.md

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual environments
venv/
env/
ENV/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Logs
*.log
logs/

# Environment files
.env
.env.local
.env.*.local

# Test files
tests/
test_*
*_test.py

# Coverage
.coverage
htmlcov/

# Node.js
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# Build artifacts
build/
dist/
*.tgz

# Temporary files
tmp/
temp/
"""
        
        output_file = Path(output_path)
        output_file.write_text(dockerignore_content)
        
        logger.info(f"Generated .dockerignore at {output_path}")
        return dockerignore_content
