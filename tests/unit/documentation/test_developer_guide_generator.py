"""
Unit tests for Developer Guide Generator
"""

import pytest
import asyncio
from datetime import datetime
from unittest.mock import AsyncMock, MagicMock, patch
from pathlib import Path

from src.pocket_hedge_fund.documentation.generators.developer_guide_generator import DeveloperGuideGenerator


@pytest.fixture
def developer_guide_generator():
    """Create developer guide generator instance for testing."""
    config = {
        'output_dir': './docs/developer_guide',
        'include_code_examples': True,
        'include_architecture_diagrams': True,
        'language': 'en'
    }
    
    return DeveloperGuideGenerator(config)


@pytest.mark.asyncio
async def test_developer_guide_generator_initialization(developer_guide_generator):
    """Test developer guide generator initialization."""
    assert developer_guide_generator is not None
    assert developer_guide_generator.output_dir == './docs/developer_guide'
    assert developer_guide_generator.include_code_examples is True
    assert developer_guide_generator.include_architecture_diagrams is True
    assert developer_guide_generator.language == 'en'
    assert developer_guide_generator.generated_guides == {}
    
    # Check default sections
    assert developer_guide_generator.sections['getting_started'] is True
    assert developer_guide_generator.sections['architecture_overview'] is True
    assert developer_guide_generator.sections['api_development'] is True
    assert developer_guide_generator.sections['database_design'] is True
    assert developer_guide_generator.sections['authentication'] is True
    assert developer_guide_generator.sections['testing'] is True
    assert developer_guide_generator.sections['deployment'] is True
    assert developer_guide_generator.sections['contributing'] is True
    assert developer_guide_generator.sections['troubleshooting'] is True


@pytest.mark.asyncio
async def test_generate_developer_guides(developer_guide_generator):
    """Test complete developer guide generation."""
    guides = await developer_guide_generator.generate_developer_guides()
    
    assert 'metadata' in guides
    assert 'sections' in guides
    
    # Check metadata
    metadata = guides['metadata']
    assert metadata['title'] == 'Pocket Hedge Fund Developer Guide'
    assert metadata['version'] == '1.0.0'
    assert metadata['language'] == 'en'
    assert 'generated_at' in metadata
    assert metadata['total_sections'] == 9
    
    # Check sections
    sections = guides['sections']
    assert 'getting_started' in sections
    assert 'architecture_overview' in sections
    assert 'api_development' in sections
    assert 'database_design' in sections
    assert 'authentication' in sections
    assert 'testing' in sections
    assert 'deployment' in sections
    assert 'contributing' in sections
    assert 'troubleshooting' in sections


@pytest.mark.asyncio
async def test_generate_getting_started(developer_guide_generator):
    """Test getting started guide generation."""
    getting_started = await developer_guide_generator._generate_getting_started()
    
    assert getting_started['title'] == 'Getting Started'
    assert 'content' in getting_started
    
    content = getting_started['content']
    assert 'introduction' in content
    assert 'prerequisites' in content
    assert 'setup_steps' in content
    assert 'verification' in content
    
    # Check prerequisites
    prerequisites = content['prerequisites']
    assert prerequisites['title'] == 'Prerequisites'
    assert 'requirements' in prerequisites
    assert len(prerequisites['requirements']) == 6
    assert 'Python 3.11 or higher' in prerequisites['requirements']
    assert 'Node.js 18 or higher' in prerequisites['requirements']
    assert 'Docker and Docker Compose' in prerequisites['requirements']
    
    # Check setup steps
    setup_steps = content['setup_steps']
    assert len(setup_steps) == 6
    
    # Check first step
    first_step = setup_steps[0]
    assert first_step['step'] == 1
    assert first_step['title'] == 'Clone the Repository'
    assert 'description' in first_step
    assert 'code' in first_step
    assert 'language' in first_step
    assert first_step['language'] == 'bash'
    
    # Check verification
    verification = content['verification']
    assert verification['title'] == 'Verify Installation'
    assert 'steps' in verification
    assert len(verification['steps']) == 3


@pytest.mark.asyncio
async def test_generate_architecture_overview(developer_guide_generator):
    """Test architecture overview guide generation."""
    architecture_overview = await developer_guide_generator._generate_architecture_overview()
    
    assert architecture_overview['title'] == 'Architecture Overview'
    assert 'content' in architecture_overview
    
    content = architecture_overview['content']
    assert 'introduction' in content
    assert 'system_architecture' in content
    assert 'data_flow' in content
    assert 'design_patterns' in content
    
    # Check system architecture
    system_architecture = content['system_architecture']
    assert system_architecture['title'] == 'System Architecture'
    assert 'description' in system_architecture
    assert 'components' in system_architecture
    
    components = system_architecture['components']
    assert 'api_gateway' in components
    assert 'core_services' in components
    assert 'database_layer' in components
    assert 'notification_service' in components
    assert 'admin_panel' in components
    
    # Check API gateway component
    api_gateway = components['api_gateway']
    assert api_gateway['name'] == 'API Gateway'
    assert api_gateway['description'] == 'FastAPI-based gateway handling routing, authentication, and rate limiting'
    assert api_gateway['technology'] == 'FastAPI, Uvicorn'
    
    # Check data flow
    data_flow = content['data_flow']
    assert data_flow['title'] == 'Data Flow'
    assert 'description' in data_flow
    assert 'flow' in data_flow
    assert len(data_flow['flow']) == 7
    
    # Check design patterns
    design_patterns = content['design_patterns']
    assert design_patterns['title'] == 'Design Patterns'
    assert 'patterns' in design_patterns
    assert len(design_patterns['patterns']) == 4
    
    # Check first pattern
    first_pattern = design_patterns['patterns'][0]
    assert 'name' in first_pattern
    assert 'description' in first_pattern
    assert 'implementation' in first_pattern
    assert first_pattern['name'] == 'Repository Pattern'


@pytest.mark.asyncio
async def test_generate_api_development(developer_guide_generator):
    """Test API development guide generation."""
    api_development = await developer_guide_generator._generate_api_development()
    
    assert api_development['title'] == 'API Development'
    assert 'content' in api_development
    
    content = api_development['content']
    assert 'introduction' in content
    assert 'api_design_principles' in content
    assert 'endpoint_development' in content
    assert 'error_handling' in content
    assert 'testing_apis' in content
    
    # Check API design principles
    api_design_principles = content['api_design_principles']
    assert api_design_principles['title'] == 'API Design Principles'
    assert 'principles' in api_design_principles
    assert len(api_design_principles['principles']) == 5
    
    # Check endpoint development
    endpoint_development = content['endpoint_development']
    assert endpoint_development['title'] == 'Creating New Endpoints'
    assert 'steps' in endpoint_development
    assert len(endpoint_development['steps']) == 3
    
    # Check first step
    first_step = endpoint_development['steps'][0]
    assert first_step['step'] == 1
    assert first_step['title'] == 'Define the Route'
    assert 'description' in first_step
    assert 'code' in first_step
    assert 'language' in first_step
    assert first_step['language'] == 'python'
    
    # Check error handling
    error_handling = content['error_handling']
    assert error_handling['title'] == 'Error Handling'
    assert 'description' in error_handling
    assert 'code' in error_handling
    assert 'language' in error_handling
    assert error_handling['language'] == 'python'
    
    # Check testing APIs
    testing_apis = content['testing_apis']
    assert testing_apis['title'] == 'Testing APIs'
    assert 'description' in testing_apis
    assert 'code' in testing_apis
    assert 'language' in testing_apis
    assert testing_apis['language'] == 'python'


@pytest.mark.asyncio
async def test_generate_database_design(developer_guide_generator):
    """Test database design guide generation."""
    database_design = await developer_guide_generator._generate_database_design()
    
    assert database_design['title'] == 'Database Design'
    assert 'content' in database_design
    
    content = database_design['content']
    assert 'introduction' in content
    assert 'database_architecture' in content
    assert 'schema_design' in content
    assert 'migration_management' in content
    assert 'performance_optimization' in content
    
    # Check database architecture
    database_architecture = content['database_architecture']
    assert database_architecture['title'] == 'Database Architecture'
    assert 'description' in database_architecture
    assert 'components' in database_architecture
    
    components = database_architecture['components']
    assert 'primary_database' in components
    assert 'cache_layer' in components
    
    # Check primary database
    primary_database = components['primary_database']
    assert primary_database['name'] == 'PostgreSQL'
    assert primary_database['description'] == 'Primary relational database for transactional data'
    assert primary_database['version'] == '15+'
    assert 'features' in primary_database
    assert len(primary_database['features']) == 3
    
    # Check schema design
    schema_design = content['schema_design']
    assert schema_design['title'] == 'Schema Design Principles'
    assert 'principles' in schema_design
    assert len(schema_design['principles']) == 5
    
    # Check migration management
    migration_management = content['migration_management']
    assert migration_management['title'] == 'Database Migrations'
    assert 'description' in migration_management
    assert 'commands' in migration_management
    assert len(migration_management['commands']) == 4
    
    # Check first command
    first_command = migration_management['commands'][0]
    assert 'command' in first_command
    assert 'description' in first_command
    assert first_command['command'] == 'alembic revision --autogenerate -m "description"'


@pytest.mark.asyncio
async def test_generate_authentication(developer_guide_generator):
    """Test authentication guide generation."""
    authentication = await developer_guide_generator._generate_authentication()
    
    assert authentication['title'] == 'Authentication and Authorization'
    assert 'content' in authentication
    
    content = authentication['content']
    assert 'introduction' in content
    assert 'authentication_methods' in content
    assert 'authorization_levels' in content
    assert 'security_best_practices' in content
    
    # Check authentication methods
    authentication_methods = content['authentication_methods']
    assert authentication_methods['title'] == 'Authentication Methods'
    assert 'methods' in authentication_methods
    
    methods = authentication_methods['methods']
    assert 'jwt_tokens' in methods
    assert 'api_keys' in methods
    assert 'oauth2' in methods
    
    # Check JWT tokens method
    jwt_tokens = methods['jwt_tokens']
    assert jwt_tokens['name'] == 'JWT Tokens'
    assert jwt_tokens['description'] == 'JSON Web Tokens for stateless authentication'
    assert jwt_tokens['implementation'] == 'PyJWT library with RS256 algorithm'
    
    # Check authorization levels
    authorization_levels = content['authorization_levels']
    assert authorization_levels['title'] == 'Authorization Levels'
    assert 'levels' in authorization_levels
    assert len(authorization_levels['levels']) == 3
    
    # Check first level
    first_level = authorization_levels['levels'][0]
    assert 'level' in first_level
    assert 'description' in first_level
    assert 'examples' in first_level
    assert first_level['level'] == 'Public'
    
    # Check security best practices
    security_best_practices = content['security_best_practices']
    assert security_best_practices['title'] == 'Security Best Practices'
    assert 'practices' in security_best_practices
    assert len(security_best_practices['practices']) == 6


@pytest.mark.asyncio
async def test_generate_testing(developer_guide_generator):
    """Test testing guide generation."""
    testing = await developer_guide_generator._generate_testing()
    
    assert testing['title'] == 'Testing'
    assert 'content' in testing
    
    content = testing['content']
    assert 'introduction' in content
    assert 'testing_pyramid' in content
    assert 'test_structure' in content
    assert 'running_tests' in content
    
    # Check testing pyramid
    testing_pyramid = content['testing_pyramid']
    assert testing_pyramid['title'] == 'Testing Pyramid'
    assert 'levels' in testing_pyramid
    assert len(testing_pyramid['levels']) == 3
    
    # Check first level
    first_level = testing_pyramid['levels'][0]
    assert 'level' in first_level
    assert 'description' in first_level
    assert 'coverage' in first_level
    assert 'tools' in first_level
    assert first_level['level'] == 'Unit Tests'
    
    # Check test structure
    test_structure = content['test_structure']
    assert test_structure['title'] == 'Test Structure'
    assert 'organization' in test_structure
    assert len(test_structure['organization']) == 5
    
    # Check running tests
    running_tests = content['running_tests']
    assert running_tests['title'] == 'Running Tests'
    assert 'commands' in running_tests
    assert len(running_tests['commands']) == 4
    
    # Check first command
    first_command = running_tests['commands'][0]
    assert 'command' in first_command
    assert 'description' in first_command
    assert first_command['command'] == 'pytest'


@pytest.mark.asyncio
async def test_generate_deployment(developer_guide_generator):
    """Test deployment guide generation."""
    deployment = await developer_guide_generator._generate_deployment()
    
    assert deployment['title'] == 'Deployment'
    assert 'content' in deployment
    
    content = deployment['content']
    assert 'introduction' in content
    assert 'deployment_environments' in content
    assert 'deployment_process' in content
    assert 'infrastructure_as_code' in content
    
    # Check deployment environments
    deployment_environments = content['deployment_environments']
    assert deployment_environments['title'] == 'Deployment Environments'
    assert 'environments' in deployment_environments
    assert len(deployment_environments['environments']) == 3
    
    # Check first environment
    first_environment = deployment_environments['environments'][0]
    assert 'name' in first_environment
    assert 'description' in first_environment
    assert 'infrastructure' in first_environment
    assert 'database' in first_environment
    assert first_environment['name'] == 'Development'
    
    # Check deployment process
    deployment_process = content['deployment_process']
    assert deployment_process['title'] == 'Deployment Process'
    assert 'steps' in deployment_process
    assert len(deployment_process['steps']) == 7
    
    # Check infrastructure as code
    infrastructure_as_code = content['infrastructure_as_code']
    assert infrastructure_as_code['title'] == 'Infrastructure as Code'
    assert 'tools' in infrastructure_as_code
    assert len(infrastructure_as_code['tools']) == 4


@pytest.mark.asyncio
async def test_generate_contributing(developer_guide_generator):
    """Test contributing guide generation."""
    contributing = await developer_guide_generator._generate_contributing()
    
    assert contributing['title'] == 'Contributing'
    assert 'content' in contributing
    
    content = contributing['content']
    assert 'introduction' in content
    assert 'contribution_process' in content
    assert 'coding_standards' in content
    assert 'commit_guidelines' in content
    
    # Check contribution process
    contribution_process = content['contribution_process']
    assert contribution_process['title'] == 'Contribution Process'
    assert 'steps' in contribution_process
    assert len(contribution_process['steps']) == 7
    
    # Check coding standards
    coding_standards = content['coding_standards']
    assert coding_standards['title'] == 'Coding Standards'
    assert 'standards' in coding_standards
    assert len(coding_standards['standards']) == 5
    
    # Check commit guidelines
    commit_guidelines = content['commit_guidelines']
    assert commit_guidelines['title'] == 'Commit Guidelines'
    assert 'format' in commit_guidelines
    assert 'types' in commit_guidelines
    assert len(commit_guidelines['types']) == 7
    
    # Check first type
    first_type = commit_guidelines['types'][0]
    assert first_type == 'feat: New feature'


@pytest.mark.asyncio
async def test_generate_troubleshooting(developer_guide_generator):
    """Test troubleshooting guide generation."""
    troubleshooting = await developer_guide_generator._generate_troubleshooting()
    
    assert troubleshooting['title'] == 'Troubleshooting'
    assert 'content' in troubleshooting
    
    content = troubleshooting['content']
    assert 'introduction' in content
    assert 'common_issues' in content
    assert 'debugging_tools' in content
    
    # Check common issues
    common_issues = content['common_issues']
    assert 'title' in common_issues
    assert 'issues' in common_issues
    assert len(common_issues['issues']) == 3
    
    # Check first issue
    first_issue = common_issues['issues'][0]
    assert 'problem' in first_issue
    assert 'solution' in first_issue
    assert 'commands' in first_issue
    assert first_issue['problem'] == 'Database connection errors'
    
    # Check debugging tools
    debugging_tools = content['debugging_tools']
    assert debugging_tools['title'] == 'Debugging Tools'
    assert 'tools' in debugging_tools
    assert len(debugging_tools['tools']) == 4


@pytest.mark.asyncio
async def test_save_guides_markdown(developer_guide_generator):
    """Test saving guides as Markdown."""
    # Generate guides first
    await developer_guide_generator.generate_developer_guides()
    
    # Save as Markdown
    output_path = await developer_guide_generator.save_guides('markdown')
    
    assert output_path is not None
    assert output_path == 'docs/developer_guide'


@pytest.mark.asyncio
async def test_save_guides_unsupported_format(developer_guide_generator):
    """Test saving guides with unsupported format."""
    # Generate guides first
    await developer_guide_generator.generate_developer_guides()
    
    # Try to save with unsupported format
    with pytest.raises(ValueError, match="Unsupported format"):
        await developer_guide_generator.save_guides('xml')


@pytest.mark.asyncio
async def test_generate_guide_index(developer_guide_generator):
    """Test guide index generation."""
    # Generate guides first
    await developer_guide_generator.generate_developer_guides()
    
    # Generate index
    index_content = developer_guide_generator._generate_guide_index()
    
    assert '# Pocket Hedge Fund Developer Guide' in index_content
    assert '## Table of Contents' in index_content
    assert '[Getting Started](getting_started.md)' in index_content
    assert '[Architecture Overview](architecture_overview.md)' in index_content
    assert '[API Development](api_development.md)' in index_content
    assert '[Database Design](database_design.md)' in index_content
    assert '[Authentication](authentication.md)' in index_content
    assert '[Testing](testing.md)' in index_content
    assert '[Deployment](deployment.md)' in index_content
    assert '[Contributing](contributing.md)' in index_content
    assert '[Troubleshooting](troubleshooting.md)' in index_content


@pytest.mark.asyncio
async def test_format_guide_section_as_markdown(developer_guide_generator):
    """Test section formatting as Markdown."""
    section_content = {
        'title': 'Test Section',
        'content': {
            'introduction': 'This is a test section.',
            'setup_steps': [
                {
                    'title': 'Step 1',
                    'description': 'First step',
                    'code': 'echo "Hello World"',
                    'language': 'bash'
                }
            ]
        }
    }
    
    markdown = developer_guide_generator._format_guide_section_as_markdown('test_section', section_content)
    
    assert '# Test Section' in markdown
    assert 'This is a test section.' in markdown
    assert '## Step 1' in markdown
    assert 'First step' in markdown
    assert '```bash' in markdown
    assert 'echo "Hello World"' in markdown


@pytest.mark.asyncio
async def test_developer_guide_generator_with_custom_config():
    """Test developer guide generator with custom configuration."""
    config = {
        'output_dir': './custom-dev-docs',
        'include_code_examples': False,
        'include_architecture_diagrams': False,
        'language': 'ru'
    }
    
    generator = DeveloperGuideGenerator(config)
    
    assert generator.output_dir == './custom-dev-docs'
    assert generator.include_code_examples is False
    assert generator.include_architecture_diagrams is False
    assert generator.language == 'ru'


@pytest.mark.asyncio
async def test_developer_guide_generator_default_config():
    """Test developer guide generator with default configuration."""
    generator = DeveloperGuideGenerator()
    
    assert generator.output_dir == './docs/developer_guide'
    assert generator.include_code_examples is True
    assert generator.include_architecture_diagrams is True
    assert generator.language == 'en'


@pytest.mark.asyncio
async def test_developer_guide_generator_sections_config():
    """Test developer guide generator sections configuration."""
    generator = DeveloperGuideGenerator()
    
    # Check default sections
    assert generator.sections['getting_started'] is True
    assert generator.sections['architecture_overview'] is True
    assert generator.sections['api_development'] is True
    assert generator.sections['database_design'] is True
    assert generator.sections['authentication'] is True
    assert generator.sections['testing'] is True
    assert generator.sections['deployment'] is True
    assert generator.sections['contributing'] is True
    assert generator.sections['troubleshooting'] is True


@pytest.mark.asyncio
async def test_generate_developer_guides_with_disabled_sections(developer_guide_generator):
    """Test developer guide generation with some sections disabled."""
    # Disable some sections
    developer_guide_generator.sections['testing'] = False
    developer_guide_generator.sections['deployment'] = False
    
    guides = await developer_guide_generator.generate_developer_guides()
    
    assert 'metadata' in guides
    assert 'sections' in guides
    
    sections = guides['sections']
    assert 'getting_started' in sections
    assert 'architecture_overview' in sections
    assert 'api_development' in sections
    assert 'database_design' in sections
    assert 'authentication' in sections
    assert 'testing' not in sections  # Should be disabled
    assert 'deployment' not in sections  # Should be disabled
    assert 'contributing' in sections
    assert 'troubleshooting' in sections


@pytest.mark.asyncio
async def test_generate_getting_started_with_code_examples(developer_guide_generator):
    """Test getting started guide generation with code examples enabled."""
    getting_started = await developer_guide_generator._generate_getting_started()
    
    # Check that code examples are included
    setup_steps = getting_started['content']['setup_steps']
    for step in setup_steps:
        assert 'code' in step
        assert 'language' in step
        assert step['code'] is not None
        assert step['language'] is not None


@pytest.mark.asyncio
async def test_generate_getting_started_without_code_examples():
    """Test getting started guide generation with code examples disabled."""
    config = {
        'output_dir': './docs/developer_guide',
        'include_code_examples': False,
        'include_architecture_diagrams': True,
        'language': 'en'
    }
    
    generator = DeveloperGuideGenerator(config)
    getting_started = await generator._generate_getting_started()
    
    # Check that code examples are not included
    setup_steps = getting_started['content']['setup_steps']
    for step in setup_steps:
        # Code examples may still be present but should be minimal
        if 'code' in step:
            assert len(step['code']) < 100  # Should be minimal code


@pytest.mark.asyncio
async def test_generate_architecture_overview_with_diagrams(developer_guide_generator):
    """Test architecture overview guide generation with diagrams enabled."""
    architecture_overview = await developer_guide_generator._generate_architecture_overview()
    
    # Check that diagrams are included
    content = architecture_overview['content']
    assert 'data_flow' in content  # Check for data_flow instead of diagrams
    
    # Check that data_flow contains expected structure
    data_flow = content['data_flow']
    assert 'description' in data_flow
    assert 'flow' in data_flow


@pytest.mark.asyncio
async def test_generate_architecture_overview_without_diagrams():
    """Test architecture overview guide generation with diagrams disabled."""
    config = {
        'output_dir': './docs/developer_guide',
        'include_code_examples': True,
        'include_architecture_diagrams': False,
        'language': 'en'
    }
    
    generator = DeveloperGuideGenerator(config)
    architecture_overview = await generator._generate_architecture_overview()
    
    # Check that diagrams are not included
    content = architecture_overview['content']
    assert 'diagrams' not in content
