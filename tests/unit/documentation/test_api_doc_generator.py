"""
Unit tests for API Documentation Generator
"""

import pytest
import asyncio
from datetime import datetime
from unittest.mock import AsyncMock, MagicMock, patch
from fastapi import FastAPI
from fastapi.routing import APIRoute

from src.pocket_hedge_fund.documentation.generators.api_doc_generator import APIDocGenerator


@pytest.fixture
def sample_fastapi_app():
    """Create a sample FastAPI app for testing."""
    app = FastAPI(
        title="Test API",
        description="Test API for documentation generation",
        version="1.0.0"
    )
    
    @app.get("/health")
    async def health_check():
        """Health check endpoint."""
        return {"status": "healthy"}
    
    @app.post("/portfolios")
    async def create_portfolio(portfolio_data: dict):
        """Create a new portfolio."""
        return {"id": "portfolio_123", "name": portfolio_data.get("name")}
    
    return app


@pytest.fixture
def api_doc_generator():
    """Create API documentation generator instance for testing."""
    config = {
        'output_dir': './docs/api',
        'include_examples': True,
        'include_schemas': True,
        'include_auth': True,
        'theme': 'default'
    }
    
    return APIDocGenerator(config)


@pytest.mark.asyncio
async def test_api_doc_generator_initialization(api_doc_generator):
    """Test API documentation generator initialization."""
    assert api_doc_generator is not None
    assert api_doc_generator.output_dir == './docs/api'
    assert api_doc_generator.include_examples is True
    assert api_doc_generator.include_schemas is True
    assert api_doc_generator.include_auth is True
    assert api_doc_generator.theme == 'default'
    assert api_doc_generator.generated_docs == {}


@pytest.mark.asyncio
async def test_generate_documentation(api_doc_generator, sample_fastapi_app):
    """Test complete documentation generation."""
    docs = await api_doc_generator.generate_documentation(sample_fastapi_app)
    
    assert 'metadata' in docs
    assert 'sections' in docs
    
    # Check metadata
    metadata = docs['metadata']
    assert metadata['title'] == 'Test API'
    assert metadata['description'] == 'Test API for documentation generation'
    assert metadata['version'] == '1.0.0'
    assert 'generated_at' in metadata
    assert metadata['total_endpoints'] == 2  # health and portfolios endpoints
    
    # Check sections
    sections = docs['sections']
    assert 'overview' in sections
    assert 'authentication' in sections
    assert 'endpoints' in sections
    assert 'schemas' in sections
    assert 'examples' in sections
    assert 'errors' in sections
    assert 'rate_limiting' in sections
    assert 'changelog' in sections


@pytest.mark.asyncio
async def test_extract_api_info(api_doc_generator, sample_fastapi_app):
    """Test API information extraction."""
    api_info = await api_doc_generator._extract_api_info(sample_fastapi_app)
    
    assert api_info['title'] == 'Test API'
    assert api_info['description'] == 'Test API for documentation generation'
    assert api_info['version'] == '1.0.0'
    assert api_info['openapi_version'] == '3.0.2'
    assert api_info['total_endpoints'] == 2
    assert 'generated_at' in api_info


@pytest.mark.asyncio
async def test_generate_overview(api_doc_generator, sample_fastapi_app):
    """Test overview section generation."""
    overview = await api_doc_generator._generate_overview(sample_fastapi_app)
    
    assert overview['title'] == 'API Overview'
    assert 'content' in overview
    
    content = overview['content']
    assert 'introduction' in content
    assert 'base_url' in content
    assert 'api_version' in content
    assert 'supported_formats' in content
    assert 'rate_limits' in content
    assert 'features' in content
    
    assert content['base_url'] == 'https://api.pockethedgefund.com'
    assert content['api_version'] == '1.0.0'
    assert 'Portfolio Management' in content['features']


@pytest.mark.asyncio
async def test_generate_auth_docs(api_doc_generator, sample_fastapi_app):
    """Test authentication documentation generation."""
    auth_docs = await api_doc_generator._generate_auth_docs(sample_fastapi_app)
    
    assert auth_docs['title'] == 'Authentication'
    assert 'content' in auth_docs
    
    content = auth_docs['content']
    assert 'methods' in content
    assert 'security_schemes' in content
    assert 'getting_started' in content
    
    # Check authentication methods
    methods = content['methods']
    assert 'jwt' in methods
    assert 'api_key' in methods
    
    jwt_method = methods['jwt']
    assert jwt_method['description'] == 'JSON Web Token authentication'
    assert jwt_method['header'] == 'Authorization: Bearer <token>'
    assert jwt_method['token_type'] == 'JWT'


@pytest.mark.asyncio
async def test_generate_endpoints_docs(api_doc_generator, sample_fastapi_app):
    """Test endpoints documentation generation."""
    endpoints_docs = await api_doc_generator._generate_endpoints_docs(sample_fastapi_app)
    
    assert endpoints_docs['title'] == 'API Endpoints'
    assert 'content' in endpoints_docs
    
    content = endpoints_docs['content']
    assert 'groups' in content
    
    # Check that endpoints are grouped
    groups = content['groups']
    assert len(groups) > 0
    
    # Check that each group has endpoints
    for group_name, group_data in groups.items():
        assert 'description' in group_data
        assert 'endpoints' in group_data
        assert len(group_data['endpoints']) > 0


@pytest.mark.asyncio
async def test_document_endpoint(api_doc_generator, sample_fastapi_app):
    """Test individual endpoint documentation."""
    # Get the first route from the app
    route = sample_fastapi_app.routes[1]  # Skip the first route (OpenAPI schema)
    
    if isinstance(route, APIRoute):
        endpoint_doc = await api_doc_generator._document_endpoint(route)
        
        assert 'path' in endpoint_doc
        assert 'methods' in endpoint_doc
        assert 'summary' in endpoint_doc
        assert 'description' in endpoint_doc
        assert 'operation_id' in endpoint_doc
        assert 'tags' in endpoint_doc
        assert 'parameters' in endpoint_doc
        assert 'responses' in endpoint_doc
        assert 'security' in endpoint_doc
        assert 'examples' in endpoint_doc
        
        assert endpoint_doc['path'] == route.path
        assert list(route.methods) in [endpoint_doc['methods']]


@pytest.mark.asyncio
async def test_generate_response_example(api_doc_generator, sample_fastapi_app):
    """Test response example generation."""
    # Get a route from the app
    route = sample_fastapi_app.routes[1]  # Skip the first route (OpenAPI schema)
    
    if isinstance(route, APIRoute):
        example = await api_doc_generator._generate_response_example(route)
        
        assert isinstance(example, dict)
        assert len(example) > 0


@pytest.mark.asyncio
async def test_generate_schemas_docs(api_doc_generator, sample_fastapi_app):
    """Test schemas documentation generation."""
    schemas_docs = await api_doc_generator._generate_schemas_docs(sample_fastapi_app)
    
    assert schemas_docs['title'] == 'Data Schemas'
    assert 'content' in schemas_docs
    
    content = schemas_docs['content']
    assert 'models' in content


@pytest.mark.asyncio
async def test_generate_examples_docs(api_doc_generator, sample_fastapi_app):
    """Test examples documentation generation."""
    examples_docs = await api_doc_generator._generate_examples_docs(sample_fastapi_app)
    
    assert examples_docs['title'] == 'Code Examples'
    assert 'content' in examples_docs
    
    content = examples_docs['content']
    assert 'languages' in content
    
    languages = content['languages']
    assert 'python' in languages
    assert 'javascript' in languages
    assert 'curl' in languages
    
    # Check that each language has examples
    for language, lang_data in languages.items():
        assert 'description' in lang_data
        assert 'examples' in lang_data
        assert len(lang_data['examples']) > 0


@pytest.mark.asyncio
async def test_generate_errors_docs(api_doc_generator, sample_fastapi_app):
    """Test error documentation generation."""
    errors_docs = await api_doc_generator._generate_errors_docs(sample_fastapi_app)
    
    assert errors_docs['title'] == 'Error Handling'
    assert 'content' in errors_docs
    
    content = errors_docs['content']
    assert 'error_format' in content
    assert 'error_codes' in content
    assert 'validation_errors' in content
    
    # Check error codes
    error_codes = content['error_codes']
    assert '400' in error_codes
    assert '401' in error_codes
    assert '404' in error_codes
    assert '500' in error_codes


@pytest.mark.asyncio
async def test_generate_rate_limiting_docs(api_doc_generator):
    """Test rate limiting documentation generation."""
    rate_limiting_docs = await api_doc_generator._generate_rate_limiting_docs()
    
    assert rate_limiting_docs['title'] == 'Rate Limiting'
    assert 'content' in rate_limiting_docs
    
    content = rate_limiting_docs['content']
    assert 'limits' in content
    assert 'headers' in content
    assert 'best_practices' in content
    
    # Check rate limits
    limits = content['limits']
    assert 'authenticated_users' in limits
    assert 'unauthenticated_users' in limits
    
    auth_limits = limits['authenticated_users']
    assert 'requests_per_minute' in auth_limits
    assert 'requests_per_hour' in auth_limits
    assert 'burst_limit' in auth_limits


@pytest.mark.asyncio
async def test_generate_changelog_docs(api_doc_generator):
    """Test changelog documentation generation."""
    changelog_docs = await api_doc_generator._generate_changelog_docs()
    
    assert changelog_docs['title'] == 'API Changelog'
    assert 'content' in changelog_docs
    
    content = changelog_docs['content']
    assert 'versions' in content
    
    versions = content['versions']
    assert len(versions) > 0
    
    # Check first version
    first_version = versions[0]
    assert 'version' in first_version
    assert 'date' in first_version
    assert 'changes' in first_version
    
    changes = first_version['changes']
    assert 'added' in changes
    assert 'changed' in changes
    assert 'deprecated' in changes
    assert 'removed' in changes
    assert 'fixed' in changes
    assert 'security' in changes


@pytest.mark.asyncio
async def test_save_documentation_markdown(api_doc_generator, sample_fastapi_app):
    """Test saving documentation as Markdown."""
    # Generate documentation first
    await api_doc_generator.generate_documentation(sample_fastapi_app)
    
    # Save as Markdown
    output_path = await api_doc_generator.save_documentation('markdown')
    
    assert output_path is not None
    assert output_path == 'docs/api'


@pytest.mark.asyncio
async def test_save_documentation_json(api_doc_generator, sample_fastapi_app):
    """Test saving documentation as JSON."""
    # Generate documentation first
    await api_doc_generator.generate_documentation(sample_fastapi_app)
    
    # Save as JSON
    output_path = await api_doc_generator.save_documentation('json')
    
    assert output_path is not None
    assert output_path.endswith('api-docs.json')


@pytest.mark.asyncio
async def test_save_documentation_unsupported_format(api_doc_generator, sample_fastapi_app):
    """Test saving documentation with unsupported format."""
    # Generate documentation first
    await api_doc_generator.generate_documentation(sample_fastapi_app)
    
    # Try to save with unsupported format
    with pytest.raises(ValueError, match="Unsupported format"):
        await api_doc_generator.save_documentation('xml')


@pytest.mark.asyncio
async def test_generate_markdown_content(api_doc_generator, sample_fastapi_app):
    """Test Markdown content generation."""
    # Generate documentation first
    await api_doc_generator.generate_documentation(sample_fastapi_app)
    
    # Generate Markdown content
    markdown_content = api_doc_generator._generate_markdown_content()
    
    assert '# Test API' in markdown_content
    assert '## Quick Start' in markdown_content
    assert '## Table of Contents' in markdown_content
    assert 'https://api.pockethedgefund.com' in markdown_content


@pytest.mark.asyncio
async def test_format_section_as_markdown(api_doc_generator):
    """Test section formatting as Markdown."""
    section_content = {
        'title': 'Test Section',
        'content': {'test': 'data'}
    }
    
    markdown = api_doc_generator._format_section_as_markdown('test_section', section_content)
    
    assert '# Test Section' in markdown
    assert 'Content for Test Section section.' in markdown


@pytest.mark.asyncio
async def test_api_doc_generator_with_custom_config():
    """Test API documentation generator with custom configuration."""
    config = {
        'output_dir': './custom-docs',
        'include_examples': False,
        'include_schemas': False,
        'include_auth': False,
        'theme': 'dark'
    }
    
    generator = APIDocGenerator(config)
    
    assert generator.output_dir == './custom-docs'
    assert generator.include_examples is False
    assert generator.include_schemas is False
    assert generator.include_auth is False
    assert generator.theme == 'dark'


@pytest.mark.asyncio
async def test_api_doc_generator_default_config():
    """Test API documentation generator with default configuration."""
    generator = APIDocGenerator()
    
    assert generator.output_dir == './docs/api'
    assert generator.include_examples is True
    assert generator.include_schemas is True
    assert generator.include_auth is True
    assert generator.theme == 'default'


@pytest.mark.asyncio
async def test_api_doc_generator_sections_config():
    """Test API documentation generator sections configuration."""
    generator = APIDocGenerator()
    
    # Check default sections
    assert generator.sections['overview'] is True
    assert generator.sections['authentication'] is True
    assert generator.sections['endpoints'] is True
    assert generator.sections['schemas'] is True
    assert generator.sections['examples'] is True
    assert generator.sections['errors'] is True
    assert generator.sections['rate_limiting'] is True
    assert generator.sections['changelog'] is True


@pytest.mark.asyncio
async def test_generate_documentation_with_disabled_sections(api_doc_generator, sample_fastapi_app):
    """Test documentation generation with some sections disabled."""
    # Disable some sections
    api_doc_generator.sections['schemas'] = False
    api_doc_generator.sections['examples'] = False
    
    docs = await api_doc_generator.generate_documentation(sample_fastapi_app)
    
    assert 'metadata' in docs
    assert 'sections' in docs
    
    sections = docs['sections']
    assert 'overview' in sections
    assert 'authentication' in sections
    assert 'endpoints' in sections
    assert 'schemas' not in sections  # Should be disabled
    assert 'examples' not in sections  # Should be disabled
    assert 'errors' in sections
    assert 'rate_limiting' in sections
    assert 'changelog' in sections
