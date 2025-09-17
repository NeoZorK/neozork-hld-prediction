"""
Developer Guide Generator

Generates comprehensive developer documentation and guides.
"""

import asyncio
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any, Union
from pathlib import Path

logger = logging.getLogger(__name__)


class DeveloperGuideGenerator:
    """
    Generates comprehensive developer documentation and guides.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize developer guide generator."""
        self.config = config or {}
        self.output_dir = self.config.get('output_dir', './docs/developer_guide')
        self.include_code_examples = self.config.get('include_code_examples', True)
        self.include_architecture_diagrams = self.config.get('include_architecture_diagrams', True)
        self.language = self.config.get('language', 'en')
        
        # Guide sections
        self.sections = {
            'getting_started': True,
            'architecture_overview': True,
            'api_development': True,
            'database_design': True,
            'authentication': True,
            'testing': True,
            'deployment': True,
            'contributing': True,
            'troubleshooting': True
        }
        
        self.generated_guides = {}
    
    async def generate_developer_guides(self) -> Dict[str, Any]:
        """Generate complete developer guide documentation."""
        try:
            logger.info("Starting developer guide generation")
            
            guides = {
                'metadata': {
                    'title': 'Pocket Hedge Fund Developer Guide',
                    'version': '1.0.0',
                    'language': self.language,
                    'generated_at': datetime.now().isoformat(),
                    'total_sections': len(self.sections)
                },
                'sections': {}
            }
            
            # Generate each section
            if self.sections['getting_started']:
                guides['sections']['getting_started'] = await self._generate_getting_started()
            
            if self.sections['architecture_overview']:
                guides['sections']['architecture_overview'] = await self._generate_architecture_overview()
            
            if self.sections['api_development']:
                guides['sections']['api_development'] = await self._generate_api_development()
            
            if self.sections['database_design']:
                guides['sections']['database_design'] = await self._generate_database_design()
            
            if self.sections['authentication']:
                guides['sections']['authentication'] = await self._generate_authentication()
            
            if self.sections['testing']:
                guides['sections']['testing'] = await self._generate_testing()
            
            if self.sections['deployment']:
                guides['sections']['deployment'] = await self._generate_deployment()
            
            if self.sections['contributing']:
                guides['sections']['contributing'] = await self._generate_contributing()
            
            if self.sections['troubleshooting']:
                guides['sections']['troubleshooting'] = await self._generate_troubleshooting()
            
            self.generated_guides = guides
            logger.info("Developer guide generation completed")
            
            return guides
            
        except Exception as e:
            logger.error(f"Failed to generate developer guides: {e}")
            raise
    
    async def _generate_getting_started(self) -> Dict[str, Any]:
        """Generate getting started guide for developers."""
        try:
            return {
                'title': 'Getting Started',
                'content': {
                    'introduction': 'Welcome to the Pocket Hedge Fund development environment. This guide will help you set up your development environment and start contributing.',
                    'prerequisites': {
                        'title': 'Prerequisites',
                        'requirements': [
                            'Python 3.11 or higher',
                            'Node.js 18 or higher',
                            'Docker and Docker Compose',
                            'Git',
                            'PostgreSQL 15 or higher',
                            'Redis 7 or higher'
                        ]
                    },
                    'setup_steps': [
                        {
                            'step': 1,
                            'title': 'Clone the Repository',
                            'description': 'Get the source code',
                            'code': '''
git clone https://github.com/pockethedgefund/neozork-hld-prediction.git
cd neozork-hld-prediction
''',
                            'language': 'bash'
                        },
                        {
                            'step': 2,
                            'title': 'Set Up Python Environment',
                            'description': 'Create and activate virtual environment',
                            'code': '''
python -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate
pip install -r requirements.txt
''',
                            'language': 'bash'
                        },
                        {
                            'step': 3,
                            'title': 'Set Up Environment Variables',
                            'description': 'Configure your development environment',
                            'code': '''
cp .env.example .env
# Edit .env with your configuration
''',
                            'language': 'bash'
                        },
                        {
                            'step': 4,
                            'title': 'Start Development Services',
                            'description': 'Launch database and Redis',
                            'code': '''
docker-compose up -d postgres redis
''',
                            'language': 'bash'
                        },
                        {
                            'step': 5,
                            'title': 'Run Database Migrations',
                            'description': 'Set up the database schema',
                            'code': '''
alembic upgrade head
''',
                            'language': 'bash'
                        },
                        {
                            'step': 6,
                            'title': 'Start the Development Server',
                            'description': 'Launch the FastAPI application',
                            'code': '''
uvicorn src.pocket_hedge_fund.main:app --reload --host 0.0.0.0 --port 8000
''',
                            'language': 'bash'
                        }
                    ],
                    'verification': {
                        'title': 'Verify Installation',
                        'steps': [
                            'Visit http://localhost:8000/docs to see the API documentation',
                            'Run the test suite: pytest',
                            'Check that all services are running: docker-compose ps'
                        ]
                    }
                }
            }
        except Exception as e:
            logger.error(f"Failed to generate getting started guide: {e}")
            return {}
    
    async def _generate_architecture_overview(self) -> Dict[str, Any]:
        """Generate architecture overview guide."""
        try:
            return {
                'title': 'Architecture Overview',
                'content': {
                    'introduction': 'Pocket Hedge Fund follows a microservices architecture with clear separation of concerns and modular design.',
                    'system_architecture': {
                        'title': 'System Architecture',
                        'description': 'High-level system architecture and components',
                        'components': {
                            'api_gateway': {
                                'name': 'API Gateway',
                                'description': 'FastAPI-based gateway handling routing, authentication, and rate limiting',
                                'technology': 'FastAPI, Uvicorn'
                            },
                            'core_services': {
                                'name': 'Core Services',
                                'description': 'Business logic services for portfolio management, analytics, and user management',
                                'technology': 'Python, FastAPI, SQLAlchemy'
                            },
                            'database_layer': {
                                'name': 'Database Layer',
                                'description': 'PostgreSQL database with Redis for caching',
                                'technology': 'PostgreSQL, Redis, SQLAlchemy'
                            },
                            'notification_service': {
                                'name': 'Notification Service',
                                'description': 'Multi-channel notification system',
                                'technology': 'Python, Celery, Redis'
                            },
                            'admin_panel': {
                                'name': 'Admin Panel',
                                'description': 'Administrative interface for system management',
                                'technology': 'FastAPI, Jinja2, JavaScript'
                            }
                        }
                    },
                    'data_flow': {
                        'title': 'Data Flow',
                        'description': 'How data flows through the system',
                        'flow': [
                            'Client requests → API Gateway',
                            'API Gateway → Authentication & Authorization',
                            'Authenticated requests → Core Services',
                            'Core Services → Database Layer',
                            'Database responses → Core Services',
                            'Core Services → API Gateway',
                            'API Gateway → Client responses'
                        ]
                    },
                    'design_patterns': {
                        'title': 'Design Patterns',
                        'patterns': [
                            {
                                'name': 'Repository Pattern',
                                'description': 'Data access abstraction layer',
                                'implementation': 'SQLAlchemy repositories for database operations'
                            },
                            {
                                'name': 'Service Layer Pattern',
                                'description': 'Business logic encapsulation',
                                'implementation': 'Service classes handling business rules'
                            },
                            {
                                'name': 'Dependency Injection',
                                'description': 'Loose coupling through dependency injection',
                                'implementation': 'FastAPI dependency system'
                            },
                            {
                                'name': 'Observer Pattern',
                                'description': 'Event-driven architecture',
                                'implementation': 'Event handlers for system events'
                            }
                        ]
                    }
                }
            }
        except Exception as e:
            logger.error(f"Failed to generate architecture overview: {e}")
            return {}
    
    async def _generate_api_development(self) -> Dict[str, Any]:
        """Generate API development guide."""
        try:
            return {
                'title': 'API Development',
                'content': {
                    'introduction': 'Guidelines for developing and maintaining the Pocket Hedge Fund API.',
                    'api_design_principles': {
                        'title': 'API Design Principles',
                        'principles': [
                            'RESTful design with clear resource-based URLs',
                            'Consistent HTTP status codes and error responses',
                            'Comprehensive input validation and error handling',
                            'Versioned APIs for backward compatibility',
                            'Comprehensive documentation and examples'
                        ]
                    },
                    'endpoint_development': {
                        'title': 'Creating New Endpoints',
                        'steps': [
                            {
                                'step': 1,
                                'title': 'Define the Route',
                                'description': 'Create the endpoint in the appropriate router',
                                'code': '''
from fastapi import APIRouter, Depends, HTTPException
from ..models.portfolio_models import PortfolioCreate, PortfolioResponse
from ..services.portfolio_service import PortfolioService

router = APIRouter(prefix="/portfolios", tags=["portfolios"])

@router.post("/", response_model=PortfolioResponse)
async def create_portfolio(
    portfolio_data: PortfolioCreate,
    portfolio_service: PortfolioService = Depends(get_portfolio_service)
):
    """Create a new portfolio."""
    return await portfolio_service.create_portfolio(portfolio_data)
''',
                                'language': 'python'
                            },
                            {
                                'step': 2,
                                'title': 'Add Input Validation',
                                'description': 'Define Pydantic models for request/response validation',
                                'code': '''
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class PortfolioCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    risk_tolerance: str = Field(..., regex="^(conservative|moderate|aggressive)$")
    
class PortfolioResponse(BaseModel):
    id: str
    name: str
    description: Optional[str]
    risk_tolerance: str
    created_at: datetime
    updated_at: datetime
''',
                                'language': 'python'
                            },
                            {
                                'step': 3,
                                'title': 'Implement Business Logic',
                                'description': 'Add the business logic in the service layer',
                                'code': '''
class PortfolioService:
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
    
    async def create_portfolio(self, portfolio_data: PortfolioCreate) -> PortfolioResponse:
        """Create a new portfolio with validation."""
        # Validate business rules
        await self._validate_portfolio_creation(portfolio_data)
        
        # Create portfolio in database
        portfolio = await self.db_manager.create_portfolio(portfolio_data)
        
        # Return response
        return PortfolioResponse.from_orm(portfolio)
''',
                                'language': 'python'
                            }
                        ]
                    },
                    'error_handling': {
                        'title': 'Error Handling',
                        'description': 'Consistent error handling across the API',
                        'code': '''
from fastapi import HTTPException
from typing import Dict, Any

class APIException(HTTPException):
    def __init__(self, status_code: int, detail: str, error_code: str = None):
        super().__init__(status_code=status_code, detail=detail)
        self.error_code = error_code

# Usage
if not portfolio:
    raise APIException(
        status_code=404,
        detail="Portfolio not found",
        error_code="PORTFOLIO_NOT_FOUND"
    )
''',
                        'language': 'python'
                    },
                    'testing_apis': {
                        'title': 'Testing APIs',
                        'description': 'How to write tests for API endpoints',
                        'code': '''
import pytest
from fastapi.testclient import TestClient
from src.pocket_hedge_fund.main import app

client = TestClient(app)

def test_create_portfolio():
    """Test portfolio creation endpoint."""
    portfolio_data = {
        "name": "Test Portfolio",
        "description": "A test portfolio",
        "risk_tolerance": "moderate"
    }
    
    response = client.post("/api/v1/portfolios/", json=portfolio_data)
    
    assert response.status_code == 201
    assert response.json()["name"] == "Test Portfolio"
    assert "id" in response.json()
''',
                        'language': 'python'
                    }
                }
            }
        except Exception as e:
            logger.error(f"Failed to generate API development guide: {e}")
            return {}
    
    async def _generate_database_design(self) -> Dict[str, Any]:
        """Generate database design guide."""
        try:
            return {
                'title': 'Database Design',
                'content': {
                    'introduction': 'Database design principles and implementation for Pocket Hedge Fund.',
                    'database_architecture': {
                        'title': 'Database Architecture',
                        'description': 'PostgreSQL with Redis caching layer',
                        'components': {
                            'primary_database': {
                                'name': 'PostgreSQL',
                                'description': 'Primary relational database for transactional data',
                                'version': '15+',
                                'features': ['ACID compliance', 'JSON support', 'Full-text search']
                            },
                            'cache_layer': {
                                'name': 'Redis',
                                'description': 'In-memory cache for performance optimization',
                                'version': '7+',
                                'features': ['Session storage', 'Rate limiting', 'Real-time data']
                            }
                        }
                    },
                    'schema_design': {
                        'title': 'Schema Design Principles',
                        'principles': [
                            'Normalized design for data integrity',
                            'Proper indexing for performance',
                            'Audit trails for all critical data',
                            'Soft deletes for data retention',
                            'Versioning for schema evolution'
                        ]
                    },
                    'migration_management': {
                        'title': 'Database Migrations',
                        'description': 'Using Alembic for database schema management',
                        'commands': [
                            {
                                'command': 'alembic revision --autogenerate -m "description"',
                                'description': 'Create a new migration'
                            },
                            {
                                'command': 'alembic upgrade head',
                                'description': 'Apply all pending migrations'
                            },
                            {
                                'command': 'alembic downgrade -1',
                                'description': 'Rollback one migration'
                            },
                            {
                                'command': 'alembic current',
                                'description': 'Show current migration version'
                            }
                        ]
                    },
                    'performance_optimization': {
                        'title': 'Performance Optimization',
                        'techniques': [
                            'Proper indexing strategy',
                            'Query optimization',
                            'Connection pooling',
                            'Read replicas for scaling',
                            'Caching frequently accessed data'
                        ]
                    }
                }
            }
        except Exception as e:
            logger.error(f"Failed to generate database design guide: {e}")
            return {}
    
    async def _generate_authentication(self) -> Dict[str, Any]:
        """Generate authentication guide."""
        try:
            return {
                'title': 'Authentication and Authorization',
                'content': {
                    'introduction': 'Authentication and authorization implementation in Pocket Hedge Fund.',
                    'authentication_methods': {
                        'title': 'Authentication Methods',
                        'methods': {
                            'jwt_tokens': {
                                'name': 'JWT Tokens',
                                'description': 'JSON Web Tokens for stateless authentication',
                                'implementation': 'PyJWT library with RS256 algorithm'
                            },
                            'api_keys': {
                                'name': 'API Keys',
                                'description': 'API key authentication for server-to-server communication',
                                'implementation': 'Custom API key validation middleware'
                            },
                            'oauth2': {
                                'name': 'OAuth 2.0',
                                'description': 'OAuth 2.0 for third-party integrations',
                                'implementation': 'FastAPI OAuth2PasswordBearer'
                            }
                        }
                    },
                    'authorization_levels': {
                        'title': 'Authorization Levels',
                        'levels': [
                            {
                                'level': 'Public',
                                'description': 'No authentication required',
                                'examples': ['Health checks', 'Public market data']
                            },
                            {
                                'level': 'Authenticated',
                                'description': 'Valid authentication required',
                                'examples': ['User profile', 'Portfolio data']
                            },
                            {
                                'level': 'Admin',
                                'description': 'Administrative privileges required',
                                'examples': ['User management', 'System configuration']
                            }
                        ]
                    },
                    'security_best_practices': {
                        'title': 'Security Best Practices',
                        'practices': [
                            'Use HTTPS for all communications',
                            'Implement rate limiting',
                            'Validate and sanitize all inputs',
                            'Use secure password hashing (bcrypt)',
                            'Implement proper session management',
                            'Regular security audits and updates'
                        ]
                    }
                }
            }
        except Exception as e:
            logger.error(f"Failed to generate authentication guide: {e}")
            return {}
    
    async def _generate_testing(self) -> Dict[str, Any]:
        """Generate testing guide."""
        try:
            return {
                'title': 'Testing',
                'content': {
                    'introduction': 'Testing strategies and implementation for Pocket Hedge Fund.',
                    'testing_pyramid': {
                        'title': 'Testing Pyramid',
                        'levels': [
                            {
                                'level': 'Unit Tests',
                                'description': 'Test individual functions and methods',
                                'coverage': '80%+',
                                'tools': ['pytest', 'pytest-asyncio', 'pytest-mock']
                            },
                            {
                                'level': 'Integration Tests',
                                'description': 'Test component interactions',
                                'coverage': '60%+',
                                'tools': ['pytest', 'TestClient', 'Docker']
                            },
                            {
                                'level': 'End-to-End Tests',
                                'description': 'Test complete user workflows',
                                'coverage': '40%+',
                                'tools': ['Playwright', 'Selenium']
                            }
                        ]
                    },
                    'test_structure': {
                        'title': 'Test Structure',
                        'organization': [
                            'tests/unit/ - Unit tests',
                            'tests/integration/ - Integration tests',
                            'tests/e2e/ - End-to-end tests',
                            'tests/fixtures/ - Test fixtures and data',
                            'tests/conftest.py - Pytest configuration'
                        ]
                    },
                    'running_tests': {
                        'title': 'Running Tests',
                        'commands': [
                            {
                                'command': 'pytest',
                                'description': 'Run all tests'
                            },
                            {
                                'command': 'pytest tests/unit/',
                                'description': 'Run only unit tests'
                            },
                            {
                                'command': 'pytest --cov=src',
                                'description': 'Run tests with coverage'
                            },
                            {
                                'command': 'pytest -n auto',
                                'description': 'Run tests in parallel'
                            }
                        ]
                    }
                }
            }
        except Exception as e:
            logger.error(f"Failed to generate testing guide: {e}")
            return {}
    
    async def _generate_deployment(self) -> Dict[str, Any]:
        """Generate deployment guide."""
        try:
            return {
                'title': 'Deployment',
                'content': {
                    'introduction': 'Deployment strategies and infrastructure for Pocket Hedge Fund.',
                    'deployment_environments': {
                        'title': 'Deployment Environments',
                        'environments': [
                            {
                                'name': 'Development',
                                'description': 'Local development environment',
                                'infrastructure': 'Docker Compose',
                                'database': 'Local PostgreSQL'
                            },
                            {
                                'name': 'Staging',
                                'description': 'Pre-production testing environment',
                                'infrastructure': 'Kubernetes',
                                'database': 'Managed PostgreSQL'
                            },
                            {
                                'name': 'Production',
                                'description': 'Live production environment',
                                'infrastructure': 'Kubernetes with auto-scaling',
                                'database': 'High-availability PostgreSQL cluster'
                            }
                        ]
                    },
                    'deployment_process': {
                        'title': 'Deployment Process',
                        'steps': [
                            'Code review and approval',
                            'Automated testing pipeline',
                            'Build Docker images',
                            'Deploy to staging environment',
                            'Integration testing',
                            'Deploy to production',
                            'Health checks and monitoring'
                        ]
                    },
                    'infrastructure_as_code': {
                        'title': 'Infrastructure as Code',
                        'tools': [
                            'Terraform for cloud infrastructure',
                            'Kubernetes manifests for container orchestration',
                            'Helm charts for application deployment',
                            'Ansible for configuration management'
                        ]
                    }
                }
            }
        except Exception as e:
            logger.error(f"Failed to generate deployment guide: {e}")
            return {}
    
    async def _generate_contributing(self) -> Dict[str, Any]:
        """Generate contributing guide."""
        try:
            return {
                'title': 'Contributing',
                'content': {
                    'introduction': 'How to contribute to the Pocket Hedge Fund project.',
                    'contribution_process': {
                        'title': 'Contribution Process',
                        'steps': [
                            'Fork the repository',
                            'Create a feature branch',
                            'Make your changes',
                            'Write tests for your changes',
                            'Ensure all tests pass',
                            'Submit a pull request',
                            'Address review feedback'
                        ]
                    },
                    'coding_standards': {
                        'title': 'Coding Standards',
                        'standards': [
                            'Follow PEP 8 for Python code',
                            'Use type hints for all functions',
                            'Write comprehensive docstrings',
                            'Maintain test coverage above 80%',
                            'Use meaningful variable and function names'
                        ]
                    },
                    'commit_guidelines': {
                        'title': 'Commit Guidelines',
                        'format': 'type(scope): description',
                        'types': [
                            'feat: New feature',
                            'fix: Bug fix',
                            'docs: Documentation changes',
                            'style: Code style changes',
                            'refactor: Code refactoring',
                            'test: Test additions or changes',
                            'chore: Build or tool changes'
                        ]
                    }
                }
            }
        except Exception as e:
            logger.error(f"Failed to generate contributing guide: {e}")
            return {}
    
    async def _generate_troubleshooting(self) -> Dict[str, Any]:
        """Generate troubleshooting guide."""
        try:
            return {
                'title': 'Troubleshooting',
                'content': {
                    'introduction': 'Common development issues and their solutions.',
                    'common_issues': {
                        'title': 'Common Issues',
                        'issues': [
                            {
                                'problem': 'Database connection errors',
                                'solution': 'Check PostgreSQL is running and connection string is correct',
                                'commands': ['docker-compose ps', 'docker-compose logs postgres']
                            },
                            {
                                'problem': 'Import errors',
                                'solution': 'Ensure virtual environment is activated and dependencies are installed',
                                'commands': ['source venv/bin/activate', 'pip install -r requirements.txt']
                            },
                            {
                                'problem': 'Test failures',
                                'solution': 'Check test database setup and environment variables',
                                'commands': ['pytest -v', 'pytest --tb=short']
                            }
                        ]
                    },
                    'debugging_tools': {
                        'title': 'Debugging Tools',
                        'tools': [
                            'Python debugger (pdb)',
                            'FastAPI debug mode',
                            'Database query logging',
                            'Application performance monitoring'
                        ]
                    }
                }
            }
        except Exception as e:
            logger.error(f"Failed to generate troubleshooting guide: {e}")
            return {}
    
    async def save_guides(self, format: str = 'markdown') -> str:
        """Save generated guides to files."""
        try:
            output_path = Path(self.output_dir)
            output_path.mkdir(parents=True, exist_ok=True)
            
            if format == 'markdown':
                return await self._save_as_markdown(output_path)
            elif format == 'html':
                return await self._save_as_html(output_path)
            else:
                raise ValueError(f"Unsupported format: {format}")
                
        except Exception as e:
            logger.error(f"Failed to save guides: {e}")
            raise
    
    async def _save_as_markdown(self, output_path: Path) -> str:
        """Save guides as Markdown files."""
        try:
            # Save main guide index
            main_file = output_path / 'README.md'
            main_content = self._generate_guide_index()
            main_file.write_text(main_content)
            
            # Save individual sections
            for section_name, section_content in self.generated_guides.get('sections', {}).items():
                section_file = output_path / f'{section_name}.md'
                section_markdown = self._format_guide_section_as_markdown(section_name, section_content)
                section_file.write_text(section_markdown)
            
            logger.info(f"Developer guides saved as Markdown to {output_path}")
            return str(output_path)
            
        except Exception as e:
            logger.error(f"Failed to save as Markdown: {e}")
            raise
    
    def _generate_guide_index(self) -> str:
        """Generate main guide index."""
        metadata = self.generated_guides.get('metadata', {})
        
        content = f"""# {metadata.get('title', 'Developer Guide')}

Welcome to the Pocket Hedge Fund Developer Guide! This comprehensive guide will help you understand the codebase, contribute effectively, and maintain the system.

## Table of Contents

- [Getting Started](getting_started.md)
- [Architecture Overview](architecture_overview.md)
- [API Development](api_development.md)
- [Database Design](database_design.md)
- [Authentication](authentication.md)
- [Testing](testing.md)
- [Deployment](deployment.md)
- [Contributing](contributing.md)
- [Troubleshooting](troubleshooting.md)

## Quick Start

1. **Clone the Repository** - Get the source code
2. **Set Up Environment** - Install dependencies and configure
3. **Start Services** - Launch database and application
4. **Run Tests** - Verify everything is working
5. **Start Developing** - Make your first contribution

## Development Environment

- **Python**: 3.11+
- **Database**: PostgreSQL 15+
- **Cache**: Redis 7+
- **Container**: Docker & Docker Compose
- **Testing**: pytest with async support

## Getting Help

- Check the [Troubleshooting](troubleshooting.md) guide
- Review existing issues on GitHub
- Join our developer community
- Contact the development team

## Version Information

- **Guide Version**: {metadata.get('version', '1.0.0')}
- **Language**: {metadata.get('language', 'en')}
- **Last Updated**: {metadata.get('generated_at', '')}
"""
        return content
    
    def _format_guide_section_as_markdown(self, section_name: str, section_content: Dict[str, Any]) -> str:
        """Format a guide section as Markdown."""
        title = section_content.get('title', section_name.replace('_', ' ').title())
        content = section_content.get('content', {})
        
        markdown = f"# {title}\n\n"
        
        # Add introduction if available
        if 'introduction' in content:
            markdown += f"{content['introduction']}\n\n"
        
        # Format content based on section type
        if 'setup_steps' in content:
            for step in content['setup_steps']:
                markdown += f"## {step['title']}\n\n"
                markdown += f"{step['description']}\n\n"
                if 'code' in step:
                    markdown += f"```{step.get('language', 'bash')}\n{step['code']}\n```\n\n"
        
        return markdown
    
    async def _save_as_html(self, output_path: Path) -> str:
        """Save guides as HTML files."""
        # Implementation would convert Markdown to HTML
        pass
