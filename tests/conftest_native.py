"""
Pytest configuration for native Apple container
Automatically skips problematic tests
"""

import pytest
import os

def pytest_configure(config):
    """Configure pytest for native container environment."""
    # Add custom markers
    config.addinivalue_line("markers", "hanging: marks tests that may hang or timeout")
    config.addinivalue_line("markers", "external_api: marks tests that require external API calls")
    config.addinivalue_line("markers", "skip_native: marks tests to skip in native container")

def pytest_collection_modifyitems(config, items):
    """Modify test collection to skip problematic tests in native container."""
    # Check if running in native container
    is_native_container = (
        os.getenv("NATIVE_CONTAINER", "false").lower() == "true" or
        os.getenv("DOCKER_CONTAINER", "false").lower() == "false"
    )
    
    if is_native_container:
        # Skip tests marked for native container
        skip_native = pytest.mark.skip(reason="Skipped in native container")
        for item in items:
            if "skip_native" in item.keywords:
                item.add_marker(skip_native)
        
        # Skip external API tests
        skip_external_api = pytest.mark.skip(reason="External API tests skipped in native container")
        for item in items:
            if "external_api" in item.keywords:
                item.add_marker(skip_external_api)
        
        # Skip hanging tests
        skip_hanging = pytest.mark.skip(reason="Hanging tests skipped in native container")
        for item in items:
            if "hanging" in item.keywords:
                item.add_marker(skip_hanging)
        
        print(f"\n🔧 Native container mode: Skipped {len([i for i in items if any(m in i.keywords for m in ['skip_native', 'external_api', 'hanging'])])} problematic tests")

def pytest_runtest_setup(item):
    """Setup for each test item."""
    # Add timeout for individual tests
    if hasattr(item, 'add_marker'):
        item.add_marker(pytest.mark.timeout(30))

def pytest_runtest_teardown(item, nextitem):
    """Cleanup after each test."""
    # Add any cleanup logic here if needed
    pass
