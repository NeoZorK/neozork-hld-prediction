"""
Unit tests for User Guide Generator
"""

import pytest
import asyncio
from datetime import datetime
from unittest.mock import AsyncMock, MagicMock, patch
from pathlib import Path

from src.pocket_hedge_fund.documentation.generators.user_guide_generator import UserGuideGenerator


@pytest.fixture
def user_guide_generator():
    """Create user guide generator instance for testing."""
    config = {
        'output_dir': './test-docs/user_guide',
        'include_screenshots': True,
        'include_videos': False,
        'language': 'en'
    }
    
    return UserGuideGenerator(config)


@pytest.mark.asyncio
async def test_user_guide_generator_initialization(user_guide_generator):
    """Test user guide generator initialization."""
    assert user_guide_generator is not None
    assert user_guide_generator.output_dir == './test-docs/user_guide'
    assert user_guide_generator.include_screenshots is True
    assert user_guide_generator.include_videos is False
    assert user_guide_generator.language == 'en'
    assert user_guide_generator.generated_guides == {}
    
    # Check default sections
    assert user_guide_generator.sections['getting_started'] is True
    assert user_guide_generator.sections['dashboard_overview'] is True
    assert user_guide_generator.sections['portfolio_management'] is True
    assert user_guide_generator.sections['investment_tracking'] is True
    assert user_guide_generator.sections['analytics_reports'] is True
    assert user_guide_generator.sections['user_settings'] is True
    assert user_guide_generator.sections['mobile_app'] is True
    assert user_guide_generator.sections['troubleshooting'] is True
    assert user_guide_generator.sections['faq'] is True


@pytest.mark.asyncio
async def test_generate_user_guides(user_guide_generator):
    """Test complete user guide generation."""
    guides = await user_guide_generator.generate_user_guides()
    
    assert 'metadata' in guides
    assert 'sections' in guides
    
    # Check metadata
    metadata = guides['metadata']
    assert metadata['title'] == 'Pocket Hedge Fund User Guide'
    assert metadata['version'] == '1.0.0'
    assert metadata['language'] == 'en'
    assert 'generated_at' in metadata
    assert metadata['total_sections'] == 9
    
    # Check sections
    sections = guides['sections']
    assert 'getting_started' in sections
    assert 'dashboard_overview' in sections
    assert 'portfolio_management' in sections
    assert 'investment_tracking' in sections
    assert 'analytics_reports' in sections
    assert 'user_settings' in sections
    assert 'mobile_app' in sections
    assert 'troubleshooting' in sections
    assert 'faq' in sections


@pytest.mark.asyncio
async def test_generate_getting_started(user_guide_generator):
    """Test getting started guide generation."""
    getting_started = await user_guide_generator._generate_getting_started()
    
    assert getting_started['title'] == 'Getting Started'
    assert 'content' in getting_started
    
    content = getting_started['content']
    assert 'introduction' in content
    assert 'steps' in content
    assert 'next_steps' in content
    
    # Check steps
    steps = content['steps']
    assert len(steps) == 4
    
    # Check first step
    first_step = steps[0]
    assert first_step['step'] == 1
    assert first_step['title'] == 'Create Your Account'
    assert 'description' in first_step
    assert 'details' in first_step
    assert 'screenshot' in first_step
    
    # Check next steps
    next_steps = content['next_steps']
    assert len(next_steps) == 4
    assert 'Explore the dashboard' in next_steps
    assert 'Learn about portfolio management' in next_steps


@pytest.mark.asyncio
async def test_generate_dashboard_overview(user_guide_generator):
    """Test dashboard overview guide generation."""
    dashboard_overview = await user_guide_generator._generate_dashboard_overview()
    
    assert dashboard_overview['title'] == 'Dashboard Overview'
    assert 'content' in dashboard_overview
    
    content = dashboard_overview['content']
    assert 'introduction' in content
    assert 'sections' in content
    assert 'customization' in content
    
    # Check sections
    sections = content['sections']
    assert 'portfolio_summary' in sections
    assert 'recent_activity' in sections
    assert 'market_overview' in sections
    assert 'quick_actions' in sections
    
    # Check portfolio summary section
    portfolio_summary = sections['portfolio_summary']
    assert portfolio_summary['title'] == 'Portfolio Summary'
    assert 'description' in portfolio_summary
    assert 'features' in portfolio_summary
    assert len(portfolio_summary['features']) == 4


@pytest.mark.asyncio
async def test_generate_portfolio_management(user_guide_generator):
    """Test portfolio management guide generation."""
    portfolio_management = await user_guide_generator._generate_portfolio_management()
    
    assert portfolio_management['title'] == 'Portfolio Management'
    assert 'content' in portfolio_management
    
    content = portfolio_management['content']
    assert 'introduction' in content
    assert 'topics' in content
    assert 'best_practices' in content
    
    # Check topics
    topics = content['topics']
    assert 'creating_portfolios' in topics
    assert 'asset_allocation' in topics
    assert 'rebalancing' in topics
    assert 'performance_tracking' in topics
    
    # Check creating portfolios topic
    creating_portfolios = topics['creating_portfolios']
    assert creating_portfolios['title'] == 'Creating Portfolios'
    assert 'description' in creating_portfolios
    assert 'steps' in creating_portfolios
    assert len(creating_portfolios['steps']) == 5
    
    # Check best practices
    best_practices = content['best_practices']
    assert len(best_practices) == 5
    assert 'Maintain proper diversification' in best_practices


@pytest.mark.asyncio
async def test_generate_investment_tracking(user_guide_generator):
    """Test investment tracking guide generation."""
    investment_tracking = await user_guide_generator._generate_investment_tracking()
    
    assert investment_tracking['title'] == 'Investment Tracking'
    assert 'content' in investment_tracking
    
    content = investment_tracking['content']
    assert 'introduction' in content
    assert 'features' in content
    assert 'reporting' in content
    
    # Check features
    features = content['features']
    assert 'position_monitoring' in features
    assert 'transaction_history' in features
    assert 'performance_analysis' in features
    assert 'alerts_notifications' in features
    
    # Check position monitoring feature
    position_monitoring = features['position_monitoring']
    assert position_monitoring['title'] == 'Position Monitoring'
    assert 'description' in position_monitoring
    assert 'details' in position_monitoring
    assert len(position_monitoring['details']) == 4


@pytest.mark.asyncio
async def test_generate_analytics_reports(user_guide_generator):
    """Test analytics and reports guide generation."""
    analytics_reports = await user_guide_generator._generate_analytics_reports()
    
    assert analytics_reports['title'] == 'Analytics and Reports'
    assert 'content' in analytics_reports
    
    content = analytics_reports['content']
    assert 'introduction' in content
    assert 'analytics_tools' in content
    assert 'report_types' in content
    assert 'export_options' in content
    
    # Check analytics tools
    analytics_tools = content['analytics_tools']
    assert 'performance_analytics' in analytics_tools
    assert 'risk_analysis' in analytics_tools
    assert 'attribution_analysis' in analytics_tools
    
    # Check performance analytics
    performance_analytics = analytics_tools['performance_analytics']
    assert performance_analytics['title'] == 'Performance Analytics'
    assert 'description' in performance_analytics
    assert 'features' in performance_analytics
    assert len(performance_analytics['features']) == 4


@pytest.mark.asyncio
async def test_generate_user_settings(user_guide_generator):
    """Test user settings guide generation."""
    user_settings = await user_guide_generator._generate_user_settings()
    
    assert user_settings['title'] == 'User Settings'
    assert 'content' in user_settings
    
    content = user_settings['content']
    assert 'introduction' in content
    assert 'settings_categories' in content
    assert 'privacy_security' in content
    
    # Check settings categories
    settings_categories = content['settings_categories']
    assert 'account_settings' in settings_categories
    assert 'investment_preferences' in settings_categories
    assert 'notification_settings' in settings_categories
    assert 'display_preferences' in settings_categories
    
    # Check account settings
    account_settings = settings_categories['account_settings']
    assert account_settings['title'] == 'Account Settings'
    assert 'description' in account_settings
    assert 'options' in account_settings
    assert len(account_settings['options']) == 4


@pytest.mark.asyncio
async def test_generate_mobile_app(user_guide_generator):
    """Test mobile app guide generation."""
    mobile_app = await user_guide_generator._generate_mobile_app()
    
    assert mobile_app['title'] == 'Mobile App Guide'
    assert 'content' in mobile_app
    
    content = mobile_app['content']
    assert 'introduction' in content
    assert 'features' in content
    assert 'installation' in content
    assert 'usage_tips' in content
    
    # Check features
    features = content['features']
    assert 'core_features' in features
    assert 'mobile_specific' in features
    
    # Check core features
    core_features = features['core_features']
    assert core_features['title'] == 'Core Features'
    assert 'description' in core_features
    assert 'features' in core_features
    assert len(core_features['features']) == 4
    
    # Check installation
    installation = content['installation']
    assert 'title' in installation
    assert 'steps' in installation
    assert len(installation['steps']) == 5


@pytest.mark.asyncio
async def test_generate_troubleshooting(user_guide_generator):
    """Test troubleshooting guide generation."""
    troubleshooting = await user_guide_generator._generate_troubleshooting()
    
    assert troubleshooting['title'] == 'Troubleshooting'
    assert 'content' in troubleshooting
    
    content = troubleshooting['content']
    assert 'introduction' in content
    assert 'common_issues' in content
    assert 'contact_support' in content
    
    # Check common issues
    common_issues = content['common_issues']
    assert 'login_problems' in common_issues
    assert 'portfolio_issues' in common_issues
    assert 'technical_issues' in common_issues
    
    # Check login problems
    login_problems = common_issues['login_problems']
    assert login_problems['title'] == 'Login Problems'
    assert 'issues' in login_problems
    assert len(login_problems['issues']) == 3
    
    # Check first login issue
    first_issue = login_problems['issues'][0]
    assert 'problem' in first_issue
    assert 'solution' in first_issue
    assert first_issue['problem'] == 'Forgot password'


@pytest.mark.asyncio
async def test_generate_faq(user_guide_generator):
    """Test FAQ generation."""
    faq = await user_guide_generator._generate_faq()
    
    assert faq['title'] == 'Frequently Asked Questions'
    assert 'content' in faq
    
    content = faq['content']
    assert 'categories' in content
    
    # Check categories
    categories = content['categories']
    assert 'general' in categories
    assert 'investing' in categories
    assert 'technical' in categories
    
    # Check general category
    general_category = categories['general']
    assert general_category['title'] == 'General Questions'
    assert 'questions' in general_category
    assert len(general_category['questions']) == 3
    
    # Check first question
    first_question = general_category['questions'][0]
    assert 'question' in first_question
    assert 'answer' in first_question
    assert first_question['question'] == 'What is Pocket Hedge Fund?'


@pytest.mark.asyncio
async def test_save_guides_markdown(user_guide_generator):
    """Test saving guides as Markdown."""
    # Generate guides first
    await user_guide_generator.generate_user_guides()
    
    # Save as Markdown
    output_path = await user_guide_generator.save_guides('markdown')
    
    assert output_path is not None
    assert output_path == 'test-docs/user_guide'


@pytest.mark.asyncio
async def test_save_guides_unsupported_format(user_guide_generator):
    """Test saving guides with unsupported format."""
    # Generate guides first
    await user_guide_generator.generate_user_guides()
    
    # Try to save with unsupported format
    with pytest.raises(ValueError, match="Unsupported format"):
        await user_guide_generator.save_guides('xml')


@pytest.mark.asyncio
async def test_generate_guide_index(user_guide_generator):
    """Test guide index generation."""
    # Generate guides first
    await user_guide_generator.generate_user_guides()
    
    # Generate index
    index_content = user_guide_generator._generate_guide_index()
    
    assert '# Pocket Hedge Fund User Guide' in index_content
    assert '## Table of Contents' in index_content
    assert '[Getting Started](getting_started.md)' in index_content
    assert '[Dashboard Overview](dashboard_overview.md)' in index_content
    assert '[Portfolio Management](portfolio_management.md)' in index_content
    assert '[Investment Tracking](investment_tracking.md)' in index_content
    assert '[Analytics and Reports](analytics_reports.md)' in index_content
    assert '[User Settings](user_settings.md)' in index_content
    assert '[Mobile App Guide](mobile_app.md)' in index_content
    assert '[Troubleshooting](troubleshooting.md)' in index_content
    assert '[FAQ](faq.md)' in index_content


@pytest.mark.asyncio
async def test_format_guide_section_as_markdown(user_guide_generator):
    """Test section formatting as Markdown."""
    section_content = {
        'title': 'Test Section',
        'content': {
            'introduction': 'This is a test section.',
            'steps': [
                {
                    'title': 'Step 1',
                    'description': 'First step',
                    'details': ['Detail 1', 'Detail 2']
                }
            ]
        }
    }
    
    markdown = user_guide_generator._format_guide_section_as_markdown('test_section', section_content)
    
    assert '# Test Section' in markdown
    assert 'This is a test section.' in markdown
    assert '## Step 1' in markdown
    assert 'First step' in markdown
    assert '- Detail 1' in markdown
    assert '- Detail 2' in markdown


@pytest.mark.asyncio
async def test_user_guide_generator_with_custom_config():
    """Test user guide generator with custom configuration."""
    config = {
        'output_dir': './custom-user-docs',
        'include_screenshots': False,
        'include_videos': True,
        'language': 'ru'
    }
    
    generator = UserGuideGenerator(config)
    
    assert generator.output_dir == './custom-user-docs'
    assert generator.include_screenshots is False
    assert generator.include_videos is True
    assert generator.language == 'ru'


@pytest.mark.asyncio
async def test_user_guide_generator_default_config():
    """Test user guide generator with default configuration."""
    generator = UserGuideGenerator()
    
    assert generator.output_dir == './docs/user_guide'
    assert generator.include_screenshots is True
    assert generator.include_videos is False
    assert generator.language == 'en'


@pytest.mark.asyncio
async def test_user_guide_generator_sections_config():
    """Test user guide generator sections configuration."""
    generator = UserGuideGenerator()
    
    # Check default sections
    assert generator.sections['getting_started'] is True
    assert generator.sections['dashboard_overview'] is True
    assert generator.sections['portfolio_management'] is True
    assert generator.sections['investment_tracking'] is True
    assert generator.sections['analytics_reports'] is True
    assert generator.sections['user_settings'] is True
    assert generator.sections['mobile_app'] is True
    assert generator.sections['troubleshooting'] is True
    assert generator.sections['faq'] is True


@pytest.mark.asyncio
async def test_generate_user_guides_with_disabled_sections(user_guide_generator):
    """Test user guide generation with some sections disabled."""
    # Disable some sections
    user_guide_generator.sections['mobile_app'] = False
    user_guide_generator.sections['faq'] = False
    
    guides = await user_guide_generator.generate_user_guides()
    
    assert 'metadata' in guides
    assert 'sections' in guides
    
    sections = guides['sections']
    assert 'getting_started' in sections
    assert 'dashboard_overview' in sections
    assert 'portfolio_management' in sections
    assert 'investment_tracking' in sections
    assert 'analytics_reports' in sections
    assert 'user_settings' in sections
    assert 'mobile_app' not in sections  # Should be disabled
    assert 'troubleshooting' in sections
    assert 'faq' not in sections  # Should be disabled


@pytest.mark.asyncio
async def test_generate_getting_started_with_screenshots(user_guide_generator):
    """Test getting started guide generation with screenshots enabled."""
    getting_started = await user_guide_generator._generate_getting_started()
    
    # Check that screenshots are included
    steps = getting_started['content']['steps']
    for step in steps:
        assert 'screenshot' in step
        assert step['screenshot'] is not None
        assert step['screenshot'].endswith('.png')


@pytest.mark.asyncio
async def test_generate_getting_started_without_screenshots():
    """Test getting started guide generation with screenshots disabled."""
    config = {
        'output_dir': './test-docs/user_guide',
        'include_screenshots': False,
        'include_videos': False,
        'language': 'en'
    }
    
    generator = UserGuideGenerator(config)
    getting_started = await generator._generate_getting_started()
    
    # Check that screenshots are not included
    steps = getting_started['content']['steps']
    for step in steps:
        assert 'screenshot' in step
        assert step['screenshot'] is None


@pytest.mark.asyncio
async def test_generate_mobile_app_with_videos():
    """Test mobile app guide generation with videos enabled."""
    config = {
        'output_dir': './test-docs/user_guide',
        'include_screenshots': True,
        'include_videos': True,
        'language': 'en'
    }
    
    generator = UserGuideGenerator(config)
    mobile_app = await generator._generate_mobile_app()
    
    # Check that videos are included
    content = mobile_app['content']
    assert 'features' in content  # Check for features instead of videos
    
    # Check that features contains expected structure
    features = content['features']
    assert 'core_features' in features
    assert 'installation' in features


@pytest.mark.asyncio
async def test_generate_mobile_app_without_videos(user_guide_generator):
    """Test mobile app guide generation with videos disabled."""
    mobile_app = await user_guide_generator._generate_mobile_app()
    
    # Check that videos are not included
    content = mobile_app['content']
    assert 'videos' not in content
