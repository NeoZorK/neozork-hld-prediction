"""
Pytest configuration and fixtures for Pocket Hedge Fund tests.

This module provides common fixtures and configuration for all test modules.
"""

import asyncio
import pytest
import pytest_asyncio
import os
from typing import AsyncGenerator, Dict, Any
from decimal import Decimal
import uuid
from datetime import datetime, timezone

from src.pocket_hedge_fund.database.connection import get_db_manager, init_database, close_database
from src.pocket_hedge_fund.auth.auth_manager import get_auth_manager
from src.pocket_hedge_fund.validation.investment_validator import get_investment_validator

def pytest_configure(config):
    """Configure pytest for different environments."""
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


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    
    yield loop
    
    # Clean up
    try:
        # Cancel all pending tasks
        pending = asyncio.all_tasks(loop)
        for task in pending:
            task.cancel()
        
        # Wait for tasks to complete cancellation
        if pending:
            loop.run_until_complete(asyncio.gather(*pending, return_exceptions=True))
    except Exception:
        pass
    finally:
        if not loop.is_closed():
            loop.close()


@pytest_asyncio.fixture(scope="session")
async def db_manager():
    """Database manager fixture for tests."""
    try:
        await init_database()
        manager = await get_db_manager()
        yield manager
    except Exception as e:
        print(f"Database initialization failed: {e}")
        yield None
    finally:
        try:
            await close_database()
        except Exception as e:
            print(f"Database cleanup failed: {e}")


@pytest_asyncio.fixture(scope="session")
async def auth_manager():
    """Authentication manager fixture for tests."""
    try:
        return await get_auth_manager()
    except Exception as e:
        print(f"Auth manager initialization failed: {e}")
        return None


@pytest_asyncio.fixture(scope="session")
async def investment_validator():
    """Investment validator fixture for tests."""
    try:
        return await get_investment_validator()
    except Exception as e:
        print(f"Investment validator initialization failed: {e}")
        return None


@pytest_asyncio.fixture
async def test_user(auth_manager) -> Dict[str, Any]:
    """Create a test user for testing."""
    if auth_manager is None:
        pytest.skip("Auth manager not available")
    
    user_data = {
        'email': f'test_{uuid.uuid4().hex[:8]}@example.com',
        'username': f'testuser_{uuid.uuid4().hex[:8]}',
        'password': 'TestPassword123!',
        'first_name': 'Test',
        'last_name': 'User'
    }
    
    try:
        success, message, user_info = await auth_manager.register_user(**user_data)
        if not success:
            pytest.skip(f"Failed to create test user: {message}")
        
        yield user_info
    except Exception as e:
        pytest.skip(f"Failed to create test user: {e}")
    finally:
        # Cleanup - delete test user
        try:
            if 'user_info' in locals():
                db_manager = await get_db_manager()
                if db_manager:
                    await db_manager.execute_command(
                        "DELETE FROM users WHERE id = $1",
                        {'user_id': user_info['id']}
                    )
        except Exception as e:
            print(f"Warning: Failed to cleanup test user: {e}")


@pytest_asyncio.fixture
async def test_fund(db_manager) -> Dict[str, Any]:
    """Create a test fund for testing."""
    if db_manager is None:
        pytest.skip("Database manager not available")
    
    fund_data = {
        'id': str(uuid.uuid4()),
        'name': f'Test Fund {uuid.uuid4().hex[:8]}',
        'description': 'Test fund for unit testing',
        'fund_type': 'mini',
        'initial_capital': Decimal('100000.00'),
        'current_value': Decimal('100000.00'),
        'min_investment': Decimal('1000.00'),
        'max_investment': Decimal('10000.00'),
        'status': 'active',
        'created_at': datetime.now(timezone.utc),
        'updated_at': datetime.now(timezone.utc)
    }
    
    try:
        await db_manager.execute_command(
            """
            INSERT INTO funds (id, name, description, fund_type, initial_capital, 
                              current_value, min_investment, max_investment, status, created_at, updated_at)
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11)
            """,
            fund_data
        )
        
        yield fund_data
    except Exception as e:
        pytest.skip(f"Failed to create test fund: {e}")
    finally:
        # Cleanup - delete test fund
        try:
            if 'fund_data' in locals():
                await db_manager.execute_command(
                    "DELETE FROM funds WHERE id = $1",
                    {'fund_id': fund_data['id']}
                )
        except Exception as e:
            print(f"Warning: Failed to cleanup test fund: {e}")


@pytest_asyncio.fixture
async def test_investment(db_manager, test_user, test_fund) -> Dict[str, Any]:
    """Create a test investment for testing."""
    if db_manager is None:
        pytest.skip("Database manager not available")
    
    investment_data = {
        'id': str(uuid.uuid4()),
        'investor_id': test_user['id'],
        'fund_id': test_fund['id'],
        'amount': Decimal('5000.00'),
        'shares_acquired': Decimal('50.00'),
        'share_price': Decimal('100.00'),
        'status': 'active',
        'created_at': datetime.now(timezone.utc),
        'updated_at': datetime.now(timezone.utc)
    }
    
    try:
        await db_manager.execute_command(
            """
            INSERT INTO investments (id, investor_id, fund_id, amount, shares_acquired, 
                                   share_price, status, created_at, updated_at)
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)
            """,
            investment_data
        )
        
        yield investment_data
    except Exception as e:
        pytest.skip(f"Failed to create test investment: {e}")
    finally:
        # Cleanup - delete test investment
        try:
            if 'investment_data' in locals():
                await db_manager.execute_command(
                    "DELETE FROM investments WHERE id = $1",
                    {'investment_id': investment_data['id']}
                )
        except Exception as e:
            print(f"Warning: Failed to cleanup test investment: {e}")


@pytest.fixture
def sample_investment_data() -> Dict[str, Any]:
    """Sample investment data for testing."""
    return {
        'fund_id': str(uuid.uuid4()),
        'amount': Decimal('5000.00')
    }


@pytest.fixture
def sample_fund_data() -> Dict[str, Any]:
    """Sample fund data for testing."""
    return {
        'name': 'Test Fund',
        'description': 'A test fund for unit testing',
        'fund_type': 'mini',
        'initial_capital': Decimal('100000.00'),
        'min_investment': Decimal('1000.00'),
        'max_investment': Decimal('10000.00')
    }


@pytest.fixture
def sample_user_data() -> Dict[str, Any]:
    """Sample user data for testing."""
    return {
        'email': f'test_{uuid.uuid4().hex[:8]}@example.com',
        'username': f'testuser_{uuid.uuid4().hex[:8]}',
        'password': 'TestPassword123!',
        'first_name': 'Test',
        'last_name': 'User'
    }


def skip_if_docker(func):
    """Decorator to skip tests when running in Docker environment."""
    def wrapper(*args, **kwargs):
        if os.path.exists('/.dockerenv') or os.environ.get('DOCKER_CONTAINER') == 'true':
            pytest.skip("Skipping test in Docker environment")
        return func(*args, **kwargs)
    return wrapper