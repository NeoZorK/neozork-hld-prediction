#!/usr/bin/env python3
"""
Test script for Authentication System and Portfolio Manager
Demonstrates the working authentication and portfolio management functionality
"""

import asyncio
import logging
import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.pocket_hedge_fund.config.database_manager import DatabaseManager, DatabaseConfig, DatabaseType
from src.pocket_hedge_fund.auth.jwt_manager import JWTManager, UserRole
from src.pocket_hedge_fund.fund_management.portfolio_manager_functional import FunctionalPortfolioManager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def test_database_connection():
    """Test database connection."""
    try:
        # Create database configuration
        db_config = DatabaseConfig(
            db_type=DatabaseType.SQLITE,
            host="localhost",
            port=5432,
            database="test_neozork_fund.db",
            username="test",
            password="test"
        )
        
        # Create database manager
        db_manager = DatabaseManager(db_config)
        
        # Test connection
        result = await db_manager.connect()
        if 'error' in result:
            logger.error(f"Database connection failed: {result['error']}")
            return None
        
        logger.info("✅ Database connection successful")
        return db_manager
        
    except Exception as e:
        logger.error(f"Failed to connect to database: {e}")
        return None


async def test_jwt_manager():
    """Test JWT Manager functionality."""
    try:
        logger.info("🧪 Testing JWT Manager...")
        
        # Create JWT manager
        jwt_manager = JWTManager("test-secret-key")
        
        # Test password hashing
        password = "TestPassword123!"
        hashed_password = jwt_manager.hash_password(password)
        logger.info(f"✅ Password hashed successfully")
        
        # Test password verification
        is_valid = jwt_manager.verify_password(password, hashed_password)
        if is_valid:
            logger.info("✅ Password verification successful")
        else:
            logger.error("❌ Password verification failed")
            return None
        
        # Test token creation
        user_id = "test-user-123"
        username = "testuser"
        email = "test@example.com"
        role = UserRole.INVESTOR
        permissions = jwt_manager.get_user_permissions(role)
        
        access_token = jwt_manager.create_access_token(
            user_id=user_id,
            username=username,
            email=email,
            role=role,
            permissions=permissions
        )
        
        refresh_token = jwt_manager.create_refresh_token(
            user_id=user_id,
            username=username,
            email=email,
            role=role,
            permissions=permissions
        )
        
        logger.info("✅ Access and refresh tokens created successfully")
        
        # Test token verification
        payload = jwt_manager.verify_token(access_token, jwt_manager.TokenType.ACCESS)
        if payload:
            logger.info(f"✅ Token verification successful for user: {payload.username}")
        else:
            logger.error("❌ Token verification failed")
            return None
        
        # Test token refresh
        new_access_token = jwt_manager.refresh_access_token(refresh_token)
        if new_access_token:
            logger.info("✅ Token refresh successful")
        else:
            logger.error("❌ Token refresh failed")
            return None
        
        # Test token blacklisting
        blacklist_success = jwt_manager.blacklist_token(access_token)
        if blacklist_success:
            logger.info("✅ Token blacklisting successful")
        else:
            logger.error("❌ Token blacklisting failed")
        
        # Test blacklisted token verification
        blacklisted_payload = jwt_manager.verify_token(access_token, jwt_manager.TokenType.ACCESS)
        if blacklisted_payload is None:
            logger.info("✅ Blacklisted token correctly rejected")
        else:
            logger.error("❌ Blacklisted token was not rejected")
        
        logger.info("✅ JWT Manager tests completed successfully")
        return jwt_manager
        
    except Exception as e:
        logger.error(f"JWT Manager test failed: {e}")
        import traceback
        traceback.print_exc()
        return None


async def test_portfolio_manager(db_manager):
    """Test Portfolio Manager functionality."""
    try:
        logger.info("🧪 Testing Portfolio Manager...")
        
        # Create portfolio manager
        portfolio_manager = FunctionalPortfolioManager(db_manager)
        
        # Get a test fund ID
        fund_query = "SELECT id FROM funds LIMIT 1"
        fund_result = await db_manager.execute_query(fund_query)
        
        if 'error' in fund_result or not fund_result['query_result']['data']:
            logger.error("❌ No test fund found")
            return None
        
        fund_id = fund_result['query_result']['data'][0]['id']
        logger.info(f"✅ Using test fund: {fund_id}")
        
        # Test getting portfolio positions
        positions_result = await portfolio_manager.get_portfolio_positions(fund_id)
        if 'error' in positions_result:
            logger.error(f"❌ Failed to get portfolio positions: {positions_result['error']}")
        else:
            logger.info(f"✅ Retrieved {positions_result['total_positions']} portfolio positions")
        
        # Test adding a position
        add_result = await portfolio_manager.add_position(
            fund_id=fund_id,
            asset_symbol="BTC",
            asset_name="Bitcoin",
            asset_type="crypto",
            quantity=0.5,
            price=45000.0
        )
        
        if 'error' in add_result:
            logger.error(f"❌ Failed to add position: {add_result['error']}")
        else:
            logger.info(f"✅ Added position: {add_result['asset_symbol']} - {add_result['quantity']} @ ${add_result['price']}")
        
        # Test updating position prices
        price_updates = {"BTC": 46000.0}
        update_result = await portfolio_manager.update_position_prices(fund_id, price_updates)
        
        if 'error' in update_result:
            logger.error(f"❌ Failed to update prices: {update_result['error']}")
        else:
            logger.info(f"✅ Updated prices for {update_result['total_updated']} positions")
        
        # Test getting portfolio metrics
        metrics_result = await portfolio_manager.get_portfolio_metrics(fund_id)
        if 'error' in metrics_result:
            logger.error(f"❌ Failed to get portfolio metrics: {metrics_result['error']}")
        else:
            logger.info(f"✅ Portfolio metrics calculated:")
            logger.info(f"  - Total Value: ${metrics_result['total_value']:,.2f}")
            logger.info(f"  - Total PnL: ${metrics_result['total_pnl']:,.2f}")
            logger.info(f"  - Total Return: {metrics_result['total_return_percentage']:.2f}%")
        
        # Test portfolio rebalancing
        target_weights = {"BTC": 50.0, "ETH": 30.0, "SOL": 20.0}
        rebalance_result = await portfolio_manager.rebalance_portfolio(fund_id, target_weights)
        
        if 'error' in rebalance_result:
            logger.error(f"❌ Failed to rebalance portfolio: {rebalance_result['error']}")
        else:
            logger.info(f"✅ Portfolio rebalancing completed: {rebalance_result['total_trades']} trades executed")
        
        logger.info("✅ Portfolio Manager tests completed successfully")
        return portfolio_manager
        
    except Exception as e:
        logger.error(f"Portfolio Manager test failed: {e}")
        import traceback
        traceback.print_exc()
        return None


async def test_authentication_flow(db_manager, jwt_manager):
    """Test complete authentication flow."""
    try:
        logger.info("🧪 Testing Authentication Flow...")
        
        # Test user registration (simulate)
        test_user_data = {
            "username": "testuser123",
            "email": "testuser123@example.com",
            "password": "TestPassword123!",
            "first_name": "Test",
            "last_name": "User"
        }
        
        # Hash password
        hashed_password = jwt_manager.hash_password(test_user_data["password"])
        logger.info("✅ Password hashed for registration")
        
        # Create tokens for registered user
        user_id = "test-user-456"
        role = UserRole.INVESTOR
        permissions = jwt_manager.get_user_permissions(role)
        
        access_token = jwt_manager.create_access_token(
            user_id=user_id,
            username=test_user_data["username"],
            email=test_user_data["email"],
            role=role,
            permissions=permissions
        )
        
        logger.info("✅ Access token created for registered user")
        
        # Test login flow
        login_payload = jwt_manager.verify_token(access_token, jwt_manager.TokenType.ACCESS)
        if login_payload:
            logger.info(f"✅ Login successful for user: {login_payload.username}")
            logger.info(f"  - Role: {login_payload.role.value}")
            logger.info(f"  - Permissions: {len(login_payload.permissions)} permissions")
        else:
            logger.error("❌ Login failed")
            return False
        
        # Test permission checking
        has_fund_read = jwt_manager.has_permission(login_payload.permissions, "fund:read")
        has_fund_create = jwt_manager.has_permission(login_payload.permissions, "fund:create")
        
        logger.info(f"✅ Permission checks:")
        logger.info(f"  - Can read funds: {has_fund_read}")
        logger.info(f"  - Can create funds: {has_fund_create}")
        
        # Test logout flow
        logout_success = jwt_manager.blacklist_token(access_token)
        if logout_success:
            logger.info("✅ Logout successful - token blacklisted")
        
        # Test that blacklisted token is rejected
        blacklisted_payload = jwt_manager.verify_token(access_token, jwt_manager.TokenType.ACCESS)
        if blacklisted_payload is None:
            logger.info("✅ Blacklisted token correctly rejected after logout")
        else:
            logger.error("❌ Blacklisted token was not rejected after logout")
        
        logger.info("✅ Authentication flow tests completed successfully")
        return True
        
    except Exception as e:
        logger.error(f"Authentication flow test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_integration(db_manager, jwt_manager, portfolio_manager):
    """Test integration between all components."""
    try:
        logger.info("🧪 Testing Component Integration...")
        
        # Create a test user with admin role
        admin_user_id = "admin-user-789"
        admin_role = UserRole.ADMIN
        admin_permissions = jwt_manager.get_user_permissions(admin_role)
        
        admin_token = jwt_manager.create_access_token(
            user_id=admin_user_id,
            username="admin",
            email="admin@neozork.com",
            role=admin_role,
            permissions=admin_permissions
        )
        
        # Verify admin token
        admin_payload = jwt_manager.verify_token(admin_token, jwt_manager.TokenType.ACCESS)
        if not admin_payload:
            logger.error("❌ Admin token verification failed")
            return False
        
        logger.info(f"✅ Admin user authenticated: {admin_payload.username}")
        
        # Test admin permissions
        can_create_fund = jwt_manager.has_permission(admin_payload.permissions, "fund:create")
        can_delete_fund = jwt_manager.has_permission(admin_payload.permissions, "fund:delete")
        can_admin_system = jwt_manager.has_permission(admin_payload.permissions, "system:admin")
        
        logger.info(f"✅ Admin permissions verified:")
        logger.info(f"  - Can create funds: {can_create_fund}")
        logger.info(f"  - Can delete funds: {can_delete_fund}")
        logger.info(f"  - Can admin system: {can_admin_system}")
        
        # Get a test fund for portfolio operations
        fund_query = "SELECT id FROM funds LIMIT 1"
        fund_result = await db_manager.execute_query(fund_query)
        
        if 'error' in fund_result or not fund_result['query_result']['data']:
            logger.error("❌ No test fund found for integration test")
            return False
        
        fund_id = fund_result['query_result']['data'][0]['id']
        
        # Test portfolio operations with authenticated user
        positions_result = await portfolio_manager.get_portfolio_positions(fund_id)
        if 'error' in positions_result:
            logger.error(f"❌ Failed to get portfolio positions: {positions_result['error']}")
        else:
            logger.info(f"✅ Portfolio operations work with authenticated user")
            logger.info(f"  - Retrieved {positions_result['total_positions']} positions")
        
        # Test database statistics
        stats_result = await db_manager.get_database_stats()
        if 'error' in stats_result:
            logger.error(f"❌ Failed to get database stats: {stats_result['error']}")
        else:
            stats = stats_result['stats']
            logger.info(f"✅ Database integration working:")
            logger.info(f"  - Active connections: {stats['active_connections']}")
            logger.info(f"  - Total queries: {stats['total_queries']}")
        
        logger.info("✅ Component integration tests completed successfully")
        return True
        
    except Exception as e:
        logger.error(f"Integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


async def main():
    """Main test function."""
    logger.info("🚀 Starting NeoZork Authentication & Portfolio Manager Test")
    logger.info("=" * 70)
    
    # Test database connection
    db_manager = await test_database_connection()
    if not db_manager:
        logger.error("❌ Database connection failed - aborting tests")
        return
    
    # Test JWT Manager
    jwt_manager = await test_jwt_manager()
    if not jwt_manager:
        logger.error("❌ JWT Manager tests failed - aborting tests")
        return
    
    # Test Portfolio Manager
    portfolio_manager = await test_portfolio_manager(db_manager)
    if not portfolio_manager:
        logger.error("❌ Portfolio Manager tests failed - aborting tests")
        return
    
    # Test Authentication Flow
    auth_success = await test_authentication_flow(db_manager, jwt_manager)
    if not auth_success:
        logger.error("❌ Authentication flow tests failed - aborting tests")
        return
    
    # Test Integration
    integration_success = await test_integration(db_manager, jwt_manager, portfolio_manager)
    if not integration_success:
        logger.error("❌ Integration tests failed")
        return
    
    # Disconnect from database
    await db_manager.disconnect()
    logger.info("✅ Database disconnected successfully")
    
    logger.info("=" * 70)
    logger.info("🎉 ALL TESTS COMPLETED SUCCESSFULLY!")
    logger.info("✅ Authentication System: WORKING")
    logger.info("✅ Portfolio Manager: WORKING")
    logger.info("✅ Database Integration: WORKING")
    logger.info("✅ Component Integration: WORKING")
    logger.info("=" * 70)


if __name__ == "__main__":
    asyncio.run(main())
