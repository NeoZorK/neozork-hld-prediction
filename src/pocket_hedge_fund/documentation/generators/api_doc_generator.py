"""
API Documentation Generator

Generates comprehensive API documentation from FastAPI applications.
"""

import asyncio
import logging
import json
import inspect
from datetime import datetime
from typing import Dict, List, Optional, Any, Union
from pathlib import Path

from fastapi import FastAPI
from fastapi.routing import APIRoute

logger = logging.getLogger(__name__)


class APIDocGenerator:
    """
    Generates comprehensive API documentation from FastAPI applications.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize API documentation generator."""
        self.config = config or {}
        self.output_dir = self.config.get('output_dir', './docs/api')
        self.include_examples = self.config.get('include_examples', True)
        self.include_schemas = self.config.get('include_schemas', True)
        self.include_auth = self.config.get('include_auth', True)
        self.theme = self.config.get('theme', 'default')
        
        # Documentation sections
        self.sections = {
            'overview': True,
            'authentication': True,
            'endpoints': True,
            'schemas': True,
            'examples': True,
            'errors': True,
            'rate_limiting': True,
            'changelog': True
        }
        
        self.generated_docs = {}
    
    async def generate_documentation(self, app: FastAPI) -> Dict[str, Any]:
        """Generate complete API documentation."""
        try:
            logger.info("Starting API documentation generation")
            
            # Extract API information
            api_info = await self._extract_api_info(app)
            
            # Generate documentation sections
            docs = {
                'metadata': api_info,
                'sections': {}
            }
            
            if self.sections['overview']:
                docs['sections']['overview'] = await self._generate_overview(app)
            
            if self.sections['authentication']:
                docs['sections']['authentication'] = await self._generate_auth_docs(app)
            
            if self.sections['endpoints']:
                docs['sections']['endpoints'] = await self._generate_endpoints_docs(app)
            
            if self.sections['schemas']:
                docs['sections']['schemas'] = await self._generate_schemas_docs(app)
            
            if self.sections['examples']:
                docs['sections']['examples'] = await self._generate_examples_docs(app)
            
            if self.sections['errors']:
                docs['sections']['errors'] = await self._generate_errors_docs(app)
            
            if self.sections['rate_limiting']:
                docs['sections']['rate_limiting'] = await self._generate_rate_limiting_docs()
            
            if self.sections['changelog']:
                docs['sections']['changelog'] = await self._generate_changelog_docs()
            
            self.generated_docs = docs
            logger.info("API documentation generation completed")
            
            return docs
            
        except Exception as e:
            logger.error(f"Failed to generate API documentation: {e}")
            raise
    
    async def _extract_api_info(self, app: FastAPI) -> Dict[str, Any]:
        """Extract basic API information."""
        try:
            return {
                'title': app.title,
                'description': app.description,
                'version': app.version,
                'openapi_version': app.openapi_version,
                'docs_url': app.docs_url,
                'redoc_url': app.redoc_url,
                'generated_at': datetime.now().isoformat(),
                'total_endpoints': len(app.routes),
                'tags': [tag.name for tag in app.openapi_tags] if app.openapi_tags else []
            }
        except Exception as e:
            logger.error(f"Failed to extract API info: {e}")
            return {}
    
    async def _generate_overview(self, app: FastAPI) -> Dict[str, Any]:
        """Generate API overview section."""
        try:
            overview = {
                'title': 'API Overview',
                'content': {
                    'introduction': app.description or 'Pocket Hedge Fund API provides comprehensive hedge fund management capabilities.',
                    'base_url': 'https://api.pockethedgefund.com',
                    'api_version': app.version,
                    'supported_formats': ['JSON'],
                    'character_encoding': 'UTF-8',
                    'rate_limits': {
                        'requests_per_minute': 1000,
                        'requests_per_hour': 10000,
                        'burst_limit': 100
                    }
                }
            }
            
            # Add feature highlights
            overview['content']['features'] = [
                'Portfolio Management',
                'Advanced Analytics',
                'Risk Assessment',
                'Real-time Monitoring',
                'User Management',
                'Notification System',
                'Admin Panel',
                'Deployment Management'
            ]
            
            return overview
            
        except Exception as e:
            logger.error(f"Failed to generate overview: {e}")
            return {}
    
    async def _generate_auth_docs(self, app: FastAPI) -> Dict[str, Any]:
        """Generate authentication documentation."""
        try:
            auth_docs = {
                'title': 'Authentication',
                'content': {
                    'methods': {
                        'jwt': {
                            'description': 'JSON Web Token authentication',
                            'header': 'Authorization: Bearer <token>',
                            'token_type': 'JWT',
                            'expiration': '24 hours',
                            'refresh_token': True
                        },
                        'api_key': {
                            'description': 'API Key authentication',
                            'header': 'X-API-Key: <api_key>',
                            'usage': 'For server-to-server communication'
                        }
                    },
                    'security_schemes': {
                        'bearer_auth': {
                            'type': 'http',
                            'scheme': 'bearer',
                            'bearer_format': 'JWT'
                        },
                        'api_key_auth': {
                            'type': 'apiKey',
                            'in': 'header',
                            'name': 'X-API-Key'
                        }
                    },
                    'getting_started': {
                        'step1': 'Register for an account',
                        'step2': 'Generate API credentials',
                        'step3': 'Include credentials in requests',
                        'step4': 'Handle authentication errors'
                    }
                }
            }
            
            return auth_docs
            
        except Exception as e:
            logger.error(f"Failed to generate auth docs: {e}")
            return {}
    
    async def _generate_endpoints_docs(self, app: FastAPI) -> Dict[str, Any]:
        """Generate endpoints documentation."""
        try:
            endpoints = {
                'title': 'API Endpoints',
                'content': {
                    'groups': {}
                }
            }
            
            # Group endpoints by tags
            for route in app.routes:
                if isinstance(route, APIRoute):
                    tag = route.tags[0] if route.tags else 'default'
                    
                    if tag not in endpoints['content']['groups']:
                        endpoints['content']['groups'][tag] = {
                            'description': f'{tag.title()} endpoints',
                            'endpoints': []
                        }
                    
                    endpoint_doc = await self._document_endpoint(route)
                    endpoints['content']['groups'][tag]['endpoints'].append(endpoint_doc)
            
            return endpoints
            
        except Exception as e:
            logger.error(f"Failed to generate endpoints docs: {e}")
            return {}
    
    async def _document_endpoint(self, route: APIRoute) -> Dict[str, Any]:
        """Document a single endpoint."""
        try:
            endpoint_doc = {
                'path': route.path,
                'methods': list(route.methods),
                'summary': route.summary or route.name,
                'description': route.description or '',
                'operation_id': route.operation_id or route.name,
                'tags': route.tags or [],
                'parameters': [],
                'request_body': None,
                'responses': {},
                'security': [],
                'examples': []
            }
            
            # Extract parameters
            if route.dependant:
                for param in route.dependant.query_params:
                    endpoint_doc['parameters'].append({
                        'name': param.name,
                        'type': param.annotation.__name__ if hasattr(param.annotation, '__name__') else str(param.annotation),
                        'required': param.is_required,
                        'description': getattr(param, 'description', ''),
                        'in': 'query'
                    })
                
                for param in route.dependant.path_params:
                    endpoint_doc['parameters'].append({
                        'name': param.name,
                        'type': param.annotation.__name__ if hasattr(param.annotation, '__name__') else str(param.annotation),
                        'required': True,
                        'description': getattr(param, 'description', ''),
                        'in': 'path'
                    })
            
            # Extract request body
            if route.dependant and route.dependant.body_params:
                body_param = route.dependant.body_params[0]
                endpoint_doc['request_body'] = {
                    'type': body_param.annotation.__name__ if hasattr(body_param.annotation, '__name__') else str(body_param.annotation),
                    'required': body_param.is_required,
                    'description': getattr(body_param, 'description', '')
                }
            
            # Generate example responses
            endpoint_doc['responses'] = {
                '200': {
                    'description': 'Successful response',
                    'content': {
                        'application/json': {
                            'example': await self._generate_response_example(route)
                        }
                    }
                },
                '400': {
                    'description': 'Bad request',
                    'content': {
                        'application/json': {
                            'example': {'error': 'Bad request', 'detail': 'Invalid input data'}
                        }
                    }
                },
                '401': {
                    'description': 'Unauthorized',
                    'content': {
                        'application/json': {
                            'example': {'error': 'Unauthorized', 'detail': 'Invalid or missing authentication'}
                        }
                    }
                },
                '500': {
                    'description': 'Internal server error',
                    'content': {
                        'application/json': {
                            'example': {'error': 'Internal server error', 'detail': 'An unexpected error occurred'}
                        }
                    }
                }
            }
            
            return endpoint_doc
            
        except Exception as e:
            logger.error(f"Failed to document endpoint {route.path}: {e}")
            return {}
    
    async def _generate_response_example(self, route: APIRoute) -> Dict[str, Any]:
        """Generate example response for endpoint."""
        try:
            # This would analyze the route's response model and generate appropriate examples
            # For now, return generic examples based on endpoint path
            if 'portfolio' in route.path:
                return {
                    'id': 'portfolio_123',
                    'name': 'My Portfolio',
                    'value': 100000.00,
                    'created_at': '2024-01-01T00:00:00Z',
                    'updated_at': '2024-01-01T00:00:00Z'
                }
            elif 'user' in route.path:
                return {
                    'id': 'user_123',
                    'username': 'john_doe',
                    'email': 'john@example.com',
                    'role': 'investor',
                    'created_at': '2024-01-01T00:00:00Z'
                }
            else:
                return {
                    'success': True,
                    'data': {},
                    'message': 'Operation completed successfully'
                }
                
        except Exception as e:
            logger.error(f"Failed to generate response example: {e}")
            return {}
    
    async def _generate_schemas_docs(self, app: FastAPI) -> Dict[str, Any]:
        """Generate schemas documentation."""
        try:
            schemas = {
                'title': 'Data Schemas',
                'content': {
                    'models': {}
                }
            }
            
            # Extract Pydantic models from the app
            if hasattr(app, 'openapi_schema') and app.openapi_schema:
                openapi_schema = app.openapi_schema
                if 'components' in openapi_schema and 'schemas' in openapi_schema['components']:
                    for model_name, model_schema in openapi_schema['components']['schemas'].items():
                        schemas['content']['models'][model_name] = {
                            'type': model_schema.get('type', 'object'),
                            'properties': model_schema.get('properties', {}),
                            'required': model_schema.get('required', []),
                            'description': model_schema.get('description', ''),
                            'example': model_schema.get('example', {})
                        }
            
            return schemas
            
        except Exception as e:
            logger.error(f"Failed to generate schemas docs: {e}")
            return {}
    
    async def _generate_examples_docs(self, app: FastAPI) -> Dict[str, Any]:
        """Generate examples documentation."""
        try:
            examples = {
                'title': 'Code Examples',
                'content': {
                    'languages': {
                        'python': {
                            'description': 'Python examples using requests library',
                            'examples': []
                        },
                        'javascript': {
                            'description': 'JavaScript examples using fetch API',
                            'examples': []
                        },
                        'curl': {
                            'description': 'cURL command examples',
                            'examples': []
                        }
                    }
                }
            }
            
            # Generate examples for common operations
            common_examples = [
                {
                    'title': 'Create Portfolio',
                    'endpoint': 'POST /api/v1/portfolios',
                    'python': '''
import requests

response = requests.post(
    'https://api.pockethedgefund.com/api/v1/portfolios',
    headers={'Authorization': 'Bearer your_token'},
    json={'name': 'My Portfolio', 'description': 'Investment portfolio'}
)
print(response.json())
''',
                    'javascript': '''
fetch('https://api.pockethedgefund.com/api/v1/portfolios', {
    method: 'POST',
    headers: {
        'Authorization': 'Bearer your_token',
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({
        name: 'My Portfolio',
        description: 'Investment portfolio'
    })
})
.then(response => response.json())
.then(data => console.log(data));
''',
                    'curl': '''
curl -X POST "https://api.pockethedgefund.com/api/v1/portfolios" \\
  -H "Authorization: Bearer your_token" \\
  -H "Content-Type: application/json" \\
  -d '{"name": "My Portfolio", "description": "Investment portfolio"}'
'''
                }
            ]
            
            for example in common_examples:
                examples['content']['languages']['python']['examples'].append({
                    'title': example['title'],
                    'code': example['python']
                })
                examples['content']['languages']['javascript']['examples'].append({
                    'title': example['title'],
                    'code': example['javascript']
                })
                examples['content']['languages']['curl']['examples'].append({
                    'title': example['title'],
                    'code': example['curl']
                })
            
            return examples
            
        except Exception as e:
            logger.error(f"Failed to generate examples docs: {e}")
            return {}
    
    async def _generate_errors_docs(self, app: FastAPI) -> Dict[str, Any]:
        """Generate error documentation."""
        try:
            errors = {
                'title': 'Error Handling',
                'content': {
                    'error_format': {
                        'description': 'All errors follow a consistent format',
                        'example': {
                            'error': 'Error type',
                            'detail': 'Detailed error message',
                            'code': 'ERROR_CODE',
                            'timestamp': '2024-01-01T00:00:00Z',
                            'request_id': 'req_123456'
                        }
                    },
                    'error_codes': {
                        '400': 'Bad Request - Invalid input data',
                        '401': 'Unauthorized - Authentication required',
                        '403': 'Forbidden - Insufficient permissions',
                        '404': 'Not Found - Resource not found',
                        '409': 'Conflict - Resource already exists',
                        '422': 'Unprocessable Entity - Validation error',
                        '429': 'Too Many Requests - Rate limit exceeded',
                        '500': 'Internal Server Error - Server error',
                        '503': 'Service Unavailable - Service temporarily unavailable'
                    },
                    'validation_errors': {
                        'description': 'Validation errors include field-specific details',
                        'example': {
                            'error': 'Validation Error',
                            'detail': [
                                {
                                    'field': 'email',
                                    'message': 'Invalid email format',
                                    'value': 'invalid-email'
                                }
                            ]
                        }
                    }
                }
            }
            
            return errors
            
        except Exception as e:
            logger.error(f"Failed to generate errors docs: {e}")
            return {}
    
    async def _generate_rate_limiting_docs(self) -> Dict[str, Any]:
        """Generate rate limiting documentation."""
        try:
            rate_limiting = {
                'title': 'Rate Limiting',
                'content': {
                    'limits': {
                        'authenticated_users': {
                            'requests_per_minute': 1000,
                            'requests_per_hour': 10000,
                            'burst_limit': 100
                        },
                        'unauthenticated_users': {
                            'requests_per_minute': 100,
                            'requests_per_hour': 1000,
                            'burst_limit': 10
                        }
                    },
                    'headers': {
                        'X-RateLimit-Limit': 'Request limit per time window',
                        'X-RateLimit-Remaining': 'Remaining requests in current window',
                        'X-RateLimit-Reset': 'Time when the rate limit resets (Unix timestamp)',
                        'X-RateLimit-Retry-After': 'Seconds to wait before retrying (when rate limited)'
                    },
                    'best_practices': [
                        'Implement exponential backoff for retries',
                        'Cache responses when possible',
                        'Use webhooks for real-time updates instead of polling',
                        'Monitor rate limit headers in responses'
                    ]
                }
            }
            
            return rate_limiting
            
        except Exception as e:
            logger.error(f"Failed to generate rate limiting docs: {e}")
            return {}
    
    async def _generate_changelog_docs(self) -> Dict[str, Any]:
        """Generate changelog documentation."""
        try:
            changelog = {
                'title': 'API Changelog',
                'content': {
                    'versions': [
                        {
                            'version': '1.0.0',
                            'date': '2024-01-01',
                            'changes': {
                                'added': [
                                    'Initial API release',
                                    'Portfolio management endpoints',
                                    'User authentication',
                                    'Basic analytics'
                                ],
                                'changed': [],
                                'deprecated': [],
                                'removed': [],
                                'fixed': [],
                                'security': []
                            }
                        }
                    ]
                }
            }
            
            return changelog
            
        except Exception as e:
            logger.error(f"Failed to generate changelog docs: {e}")
            return {}
    
    async def save_documentation(self, format: str = 'markdown') -> str:
        """Save generated documentation to files."""
        try:
            output_path = Path(self.output_dir)
            output_path.mkdir(parents=True, exist_ok=True)
            
            if format == 'markdown':
                return await self._save_as_markdown(output_path)
            elif format == 'html':
                return await self._save_as_html(output_path)
            elif format == 'json':
                return await self._save_as_json(output_path)
            else:
                raise ValueError(f"Unsupported format: {format}")
                
        except Exception as e:
            logger.error(f"Failed to save documentation: {e}")
            raise
    
    async def _save_as_markdown(self, output_path: Path) -> str:
        """Save documentation as Markdown files."""
        try:
            # Save main API documentation
            main_file = output_path / 'README.md'
            main_content = self._generate_markdown_content()
            main_file.write_text(main_content)
            
            # Save individual sections
            for section_name, section_content in self.generated_docs.get('sections', {}).items():
                section_file = output_path / f'{section_name}.md'
                section_markdown = self._format_section_as_markdown(section_name, section_content)
                section_file.write_text(section_markdown)
            
            logger.info(f"Documentation saved as Markdown to {output_path}")
            return str(output_path)
            
        except Exception as e:
            logger.error(f"Failed to save as Markdown: {e}")
            raise
    
    def _generate_markdown_content(self) -> str:
        """Generate main Markdown content."""
        metadata = self.generated_docs.get('metadata', {})
        
        content = f"""# {metadata.get('title', 'API Documentation')}

{metadata.get('description', '')}

## Quick Start

- **Base URL**: https://api.pockethedgefund.com
- **API Version**: {metadata.get('version', '1.0.0')}
- **Authentication**: Bearer Token
- **Content Type**: application/json

## Table of Contents

- [Overview](overview.md)
- [Authentication](authentication.md)
- [Endpoints](endpoints.md)
- [Schemas](schemas.md)
- [Examples](examples.md)
- [Error Handling](errors.md)
- [Rate Limiting](rate_limiting.md)
- [Changelog](changelog.md)

## Getting Started

1. Register for an account
2. Generate API credentials
3. Include credentials in requests
4. Start building!

For detailed information, see the individual documentation sections.
"""
        return content
    
    def _format_section_as_markdown(self, section_name: str, section_content: Dict[str, Any]) -> str:
        """Format a section as Markdown."""
        title = section_content.get('title', section_name.title())
        content = section_content.get('content', {})
        
        markdown = f"# {title}\n\n"
        
        # This would format the content based on the section type
        # For now, return basic structure
        markdown += f"Content for {title} section.\n\n"
        
        return markdown
    
    async def _save_as_html(self, output_path: Path) -> str:
        """Save documentation as HTML files."""
        # Implementation would convert Markdown to HTML
        pass
    
    async def _save_as_json(self, output_path: Path) -> str:
        """Save documentation as JSON file."""
        try:
            json_file = output_path / 'api-docs.json'
            json_file.write_text(json.dumps(self.generated_docs, indent=2))
            
            logger.info(f"Documentation saved as JSON to {json_file}")
            return str(json_file)
            
        except Exception as e:
            logger.error(f"Failed to save as JSON: {e}")
            raise
