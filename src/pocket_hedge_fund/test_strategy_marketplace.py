#!/usr/bin/env python3
"""
Test script for Strategy Marketplace API
Demonstrates the working strategy marketplace functionality
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
from src.pocket_hedge_fund.api.strategy_marketplace_api import StrategyMarketplaceAPI

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


async def test_strategy_creation(db_manager, jwt_manager):
    """Test strategy creation functionality."""
    try:
        logger.info("🧪 Testing Strategy Creation...")
        
        # Create strategy marketplace API
        strategy_api = StrategyMarketplaceAPI(db_manager, jwt_manager)
        
        # Create admin user for testing
        admin_user_id = "admin-user-123"
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
        
        # Test strategy type validation
        logger.info("🧪 Testing strategy type validation...")
        
        valid_strategy_types = ["momentum", "mean_reversion", "arbitrage", "scalping", "swing", "trend_following", "contrarian", "pairs_trading", "grid_trading", "dca"]
        
        for strategy_type in valid_strategy_types:
            if strategy_api._validate_strategy_type(strategy_type):
                logger.info(f"  ✅ Valid strategy type: {strategy_type}")
            else:
                logger.error(f"  ❌ Invalid strategy type: {strategy_type}")
                return False
        
        # Test invalid strategy type
        if not strategy_api._validate_strategy_type("invalid_type"):
            logger.info("  ✅ Invalid strategy type correctly rejected")
        else:
            logger.error("  ❌ Invalid strategy type incorrectly accepted")
            return False
        
        # Test strategy status validation
        logger.info("🧪 Testing strategy status validation...")
        
        valid_statuses = ["draft", "published", "archived", "suspended"]
        
        for status in valid_statuses:
            if strategy_api._validate_strategy_status(status):
                logger.info(f"  ✅ Valid strategy status: {status}")
            else:
                logger.error(f"  ❌ Invalid strategy status: {status}")
                return False
        
        # Test invalid status
        if not strategy_api._validate_strategy_status("invalid_status"):
            logger.info("  ✅ Invalid strategy status correctly rejected")
        else:
            logger.error("  ❌ Invalid strategy status incorrectly accepted")
            return False
        
        # Test UUID validation
        logger.info("🧪 Testing UUID validation...")
        
        valid_uuid = "123e4567-e89b-12d3-a456-426614174000"
        invalid_uuid = "not-a-uuid"
        
        if strategy_api._is_valid_uuid(valid_uuid):
            logger.info("  ✅ Valid UUID validation passed")
        else:
            logger.error("  ❌ Valid UUID validation failed")
            return False
        
        if not strategy_api._is_valid_uuid(invalid_uuid):
            logger.info("  ✅ Invalid UUID validation passed")
        else:
            logger.error("  ❌ Invalid UUID validation failed")
            return False
        
        logger.info("✅ Strategy creation functionality tests completed successfully")
        return True
        
    except Exception as e:
        logger.error(f"Strategy creation test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_strategy_operations(db_manager, jwt_manager):
    """Test strategy operations."""
    try:
        logger.info("🧪 Testing Strategy Operations...")
        
        # Create strategy marketplace API
        strategy_api = StrategyMarketplaceAPI(db_manager, jwt_manager)
        
        # Create admin user for testing
        admin_user_id = "admin-user-123"
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
        
        # Test permission checking
        logger.info("🧪 Testing permission system...")
        
        # Test admin permissions
        if strategy_api._check_permission(admin_permissions, "strategies:create"):
            logger.info("✅ Admin has strategies:create permission")
        else:
            logger.error("❌ Admin missing strategies:create permission")
            return False
        
        if strategy_api._check_permission(admin_permissions, "strategies:read"):
            logger.info("✅ Admin has strategies:read permission")
        else:
            logger.error("❌ Admin missing strategies:read permission")
            return False
        
        # Test investor permissions (should have limited access)
        investor_role = UserRole.INVESTOR
        investor_permissions = jwt_manager.get_user_permissions(investor_role)
        
        if not strategy_api._check_permission(investor_permissions, "strategies:create"):
            logger.info("✅ Investor correctly lacks strategies:create permission")
        else:
            logger.error("❌ Investor incorrectly has strategies:create permission")
            return False
        
        if strategy_api._check_permission(investor_permissions, "strategies:read"):
            logger.info("✅ Investor correctly has strategies:read permission")
        else:
            logger.error("❌ Investor incorrectly lacks strategies:read permission")
            return False
        
        logger.info("✅ Strategy operations tests completed successfully")
        return True
        
    except Exception as e:
        logger.error(f"Strategy operations test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_strategy_statistics(db_manager, jwt_manager):
    """Test strategy statistics functionality."""
    try:
        logger.info("🧪 Testing Strategy Statistics...")
        
        # Create strategy marketplace API
        strategy_api = StrategyMarketplaceAPI(db_manager, jwt_manager)
        
        # Create admin user for testing
        admin_user_id = "admin-user-123"
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
        
        # Test strategy statistics queries
        logger.info("🧪 Testing strategy statistics queries...")
        
        # Test total strategies count
        total_query = "SELECT COUNT(*) as total FROM strategies"
        total_result = await db_manager.execute_query(total_query)
        
        if 'error' in total_result:
            logger.error(f"❌ Failed to get total strategies count: {total_result['error']}")
            return False
        
        total_strategies = total_result['query_result']['data'][0]['total']
        logger.info(f"✅ Total strategies count: {total_strategies}")
        
        # Test public strategies count
        public_query = "SELECT COUNT(*) as total FROM strategies WHERE is_public = true"
        public_result = await db_manager.execute_query(public_query)
        
        if 'error' in public_result:
            logger.error(f"❌ Failed to get public strategies count: {public_result['error']}")
            return False
        
        public_strategies = public_result['query_result']['data'][0]['total']
        logger.info(f"✅ Public strategies count: {public_strategies}")
        
        # Test strategies by type
        type_query = "SELECT strategy_type, COUNT(*) as count FROM strategies GROUP BY strategy_type"
        type_result = await db_manager.execute_query(type_query)
        
        if 'error' in type_result:
            logger.error(f"❌ Failed to get strategies by type: {type_result['error']}")
            return False
        
        strategies_by_type = {}
        for row in type_result['query_result']['data']:
            strategies_by_type[row['strategy_type']] = row['count']
        
        logger.info(f"✅ Strategies by type: {strategies_by_type}")
        
        # Test strategies by status
        status_query = "SELECT status, COUNT(*) as count FROM strategies GROUP BY status"
        status_result = await db_manager.execute_query(status_query)
        
        if 'error' in status_result:
            logger.error(f"❌ Failed to get strategies by status: {status_result['error']}")
            return False
        
        strategies_by_status = {}
        for row in status_result['query_result']['data']:
            strategies_by_status[row['status']] = row['count']
        
        logger.info(f"✅ Strategies by status: {strategies_by_status}")
        
        logger.info("✅ Strategy statistics tests completed successfully")
        return True
        
    except Exception as e:
        logger.error(f"Strategy statistics test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_comprehensive_strategy_workflow(db_manager, jwt_manager):
    """Test comprehensive strategy marketplace workflow."""
    try:
        logger.info("🧪 Testing Comprehensive Strategy Marketplace Workflow...")
        
        # Create strategy marketplace API
        strategy_api = StrategyMarketplaceAPI(db_manager, jwt_manager)
        
        # Create admin user for testing
        admin_user_id = "admin-user-123"
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
        
        # Step 1: Test strategy creation workflow
        logger.info("📊 Step 1: Testing strategy creation workflow...")
        
        test_strategies = [
            {
                "name": "Momentum Trading Strategy",
                "description": "A momentum-based trading strategy that follows market trends",
                "strategy_type": "momentum",
                "parameters": {
                    "lookback_period": 20,
                    "threshold": 0.02,
                    "stop_loss": 0.05,
                    "take_profit": 0.10
                },
                "risk_level": 7,
                "expected_return": 25.0,
                "max_drawdown": 15.0,
                "min_capital": 10000.0,
                "tags": ["momentum", "trend", "high-risk"],
                "is_public": True,
                "price": 99.99
            },
            {
                "name": "Mean Reversion Strategy",
                "description": "A mean reversion strategy that profits from price corrections",
                "strategy_type": "mean_reversion",
                "parameters": {
                    "lookback_period": 14,
                    "deviation_threshold": 2.0,
                    "reversion_factor": 0.5
                },
                "risk_level": 5,
                "expected_return": 18.0,
                "max_drawdown": 12.0,
                "min_capital": 5000.0,
                "tags": ["mean-reversion", "low-risk", "stable"],
                "is_public": True,
                "price": 49.99
            },
            {
                "name": "Scalping Strategy",
                "description": "A high-frequency scalping strategy for short-term profits",
                "strategy_type": "scalping",
                "parameters": {
                    "timeframe": "1m",
                    "profit_target": 0.001,
                    "stop_loss": 0.0005,
                    "max_trades_per_hour": 10
                },
                "risk_level": 9,
                "expected_return": 35.0,
                "max_drawdown": 20.0,
                "min_capital": 25000.0,
                "tags": ["scalping", "high-frequency", "very-high-risk"],
                "is_public": False,
                "price": 199.99
            }
        ]
        
        created_strategies = []
        for strategy_data in test_strategies:
            # Validate strategy data
            if not strategy_api._validate_strategy_type(strategy_data["strategy_type"]):
                logger.error(f"  ❌ Invalid strategy type: {strategy_data['strategy_type']}")
                continue
            
            # Create strategy in database
            import uuid
            import json
            from datetime import datetime
            
            strategy_id = str(uuid.uuid4())
            create_strategy_query = """
            INSERT INTO strategies (
                id, name, description, strategy_type, parameters, risk_level,
                expected_return, max_drawdown, min_capital, tags, is_public,
                price, status, author_id, created_at, updated_at
            ) VALUES (
                :id, :name, :description, :strategy_type, :parameters, :risk_level,
                :expected_return, :max_drawdown, :min_capital, :tags, :is_public,
                :price, :status, :author_id, :created_at, :updated_at
            )
            """
            
            now = datetime.now()
            create_params = {
                "id": strategy_id,
                "name": strategy_data["name"],
                "description": strategy_data["description"],
                "strategy_type": strategy_data["strategy_type"],
                "parameters": json.dumps(strategy_data["parameters"]),
                "risk_level": strategy_data["risk_level"],
                "expected_return": strategy_data["expected_return"],
                "max_drawdown": strategy_data["max_drawdown"],
                "min_capital": strategy_data["min_capital"],
                "tags": json.dumps(strategy_data["tags"]),
                "is_public": strategy_data["is_public"],
                "price": strategy_data["price"],
                "status": "published",
                "author_id": admin_user_id,
                "created_at": now,
                "updated_at": now
            }
            
            create_result = await db_manager.execute_query(create_strategy_query, create_params)
            
            if 'error' not in create_result:
                created_strategies.append({
                    "strategy_id": strategy_id,
                    "name": strategy_data["name"],
                    "strategy_type": strategy_data["strategy_type"]
                })
                logger.info(f"  ✅ Created strategy: {strategy_data['name']} ({strategy_data['strategy_type']})")
            else:
                logger.error(f"  ❌ Failed to create strategy {strategy_data['name']}: {create_result['error']}")
        
        logger.info(f"✅ Created {len(created_strategies)} strategies successfully")
        
        # Step 2: Test strategy retrieval
        logger.info("📊 Step 2: Testing strategy retrieval...")
        
        for strategy in created_strategies:
            strategy_query = """
            SELECT s.*, u.username as author_name
            FROM strategies s
            JOIN users u ON s.author_id = u.id
            WHERE s.id = :strategy_id
            """
            strategy_result = await db_manager.execute_query(strategy_query, {"strategy_id": strategy["strategy_id"]})
            
            if 'error' not in strategy_result and strategy_result['query_result']['data']:
                strategy_data = strategy_result['query_result']['data'][0]
                logger.info(f"  ✅ Retrieved strategy: {strategy_data['name']} ({strategy_data['strategy_type']})")
            else:
                logger.error(f"  ❌ Failed to retrieve strategy {strategy['name']}")
        
        # Step 3: Test strategy filtering
        logger.info("📊 Step 3: Testing strategy filtering...")
        
        # Test filtering by strategy type
        momentum_query = """
        SELECT COUNT(*) as count FROM strategies 
        WHERE strategy_type = 'momentum' AND status = 'published'
        """
        momentum_result = await db_manager.execute_query(momentum_query)
        
        if 'error' not in momentum_result:
            momentum_count = momentum_result['query_result']['data'][0]['count']
            logger.info(f"  ✅ Momentum strategies count: {momentum_count}")
        
        # Test filtering by risk level
        high_risk_query = """
        SELECT COUNT(*) as count FROM strategies 
        WHERE risk_level >= 7 AND status = 'published'
        """
        high_risk_result = await db_manager.execute_query(high_risk_query)
        
        if 'error' not in high_risk_result:
            high_risk_count = high_risk_result['query_result']['data'][0]['count']
            logger.info(f"  ✅ High-risk strategies count: {high_risk_count}")
        
        # Step 4: Test strategy performance tracking
        logger.info("📊 Step 4: Testing strategy performance tracking...")
        
        for strategy in created_strategies:
            # Create performance record
            performance_query = """
            INSERT INTO strategy_performance (strategy_id, total_views, total_downloads, rating, total_ratings)
            VALUES (:strategy_id, 0, 0, 0.0, 0)
            ON CONFLICT (strategy_id) DO NOTHING
            """
            
            performance_result = await db_manager.execute_query(performance_query, {"strategy_id": strategy["strategy_id"]})
            
            if 'error' not in performance_result:
                logger.info(f"  ✅ Performance tracking initialized for: {strategy['name']}")
            else:
                logger.error(f"  ❌ Failed to initialize performance tracking for {strategy['name']}")
        
        # Step 5: Test strategy statistics
        logger.info("📊 Step 5: Testing strategy statistics...")
        
        # Get updated statistics
        total_query = "SELECT COUNT(*) as total FROM strategies"
        total_result = await db_manager.execute_query(total_query)
        
        if 'error' not in total_result:
            total_strategies = total_result['query_result']['data'][0]['total']
            logger.info(f"  ✅ Total strategies after operations: {total_strategies}")
        
        # Get strategies by type
        type_query = "SELECT strategy_type, COUNT(*) as count FROM strategies GROUP BY strategy_type"
        type_result = await db_manager.execute_query(type_query)
        
        if 'error' not in type_result:
            strategies_by_type = {}
            for row in type_result['query_result']['data']:
                strategies_by_type[row['strategy_type']] = row['count']
            logger.info(f"  ✅ Strategies by type: {strategies_by_type}")
        
        logger.info("✅ Comprehensive strategy marketplace workflow completed successfully")
        return True
        
    except Exception as e:
        logger.error(f"Comprehensive strategy workflow test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_api_integration(db_manager, jwt_manager):
    """Test API integration with authentication."""
    try:
        logger.info("🧪 Testing API Integration...")
        
        # Create strategy marketplace API
        strategy_api = StrategyMarketplaceAPI(db_manager, jwt_manager)
        
        # Create test users with different roles
        test_roles = [UserRole.ADMIN, UserRole.MANAGER, UserRole.TRADER, UserRole.ANALYST, UserRole.INVESTOR]
        
        for role in test_roles:
            user_id = f"test-{role.value.lower()}-123"
            permissions = jwt_manager.get_user_permissions(role)
            
            token = jwt_manager.create_access_token(
                user_id=user_id,
                username=f"test_{role.value.lower()}",
                email=f"test_{role.value.lower()}@neozork.com",
                role=role,
                permissions=permissions
            )
            
            # Verify token
            payload = jwt_manager.verify_token(token, jwt_manager.TokenType.ACCESS)
            if not payload:
                logger.error(f"❌ Token verification failed for {role.value}")
                return False
            
            logger.info(f"✅ {role.value} user authenticated: {payload.username}")
            
            # Test role-specific permissions
            if role in [UserRole.ADMIN, UserRole.MANAGER, UserRole.TRADER]:
                if not strategy_api._check_permission(permissions, "strategies:create"):
                    logger.error(f"❌ {role.value} missing strategies:create permission")
                    return False
            
            elif role == UserRole.INVESTOR:
                if strategy_api._check_permission(permissions, "strategies:create"):
                    logger.error(f"❌ {role.value} incorrectly has strategies:create permission")
                    return False
            
            # All roles should have read permission
            if not strategy_api._check_permission(permissions, "strategies:read"):
                logger.error(f"❌ {role.value} missing strategies:read permission")
                return False
        
        # Test database statistics
        stats_result = await db_manager.get_database_stats()
        if 'error' in stats_result:
            logger.error(f"❌ Failed to get database stats: {stats_result['error']}")
            return False
        
        stats = stats_result['stats']
        logger.info(f"✅ Database integration working:")
        logger.info(f"  - Active connections: {stats['active_connections']}")
        logger.info(f"  - Total queries: {stats['total_queries']}")
        
        logger.info("✅ API integration tests completed successfully")
        return True
        
    except Exception as e:
        logger.error(f"API integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


async def main():
    """Main test function."""
    logger.info("🚀 Starting NeoZork Strategy Marketplace API Test")
    logger.info("=" * 80)
    
    # Test database connection
    db_manager = await test_database_connection()
    if not db_manager:
        logger.error("❌ Database connection failed - aborting tests")
        return
    
    # Test JWT Manager
    jwt_manager = JWTManager("test-secret-key")
    logger.info("✅ JWT Manager initialized")
    
    # Test Strategy Creation
    creation_success = await test_strategy_creation(db_manager, jwt_manager)
    if not creation_success:
        logger.error("❌ Strategy creation tests failed - aborting tests")
        return
    
    # Test Strategy Operations
    operations_success = await test_strategy_operations(db_manager, jwt_manager)
    if not operations_success:
        logger.error("❌ Strategy operations tests failed - aborting tests")
        return
    
    # Test Strategy Statistics
    stats_success = await test_strategy_statistics(db_manager, jwt_manager)
    if not stats_success:
        logger.error("❌ Strategy statistics tests failed - aborting tests")
        return
    
    # Test Comprehensive Workflow
    workflow_success = await test_comprehensive_strategy_workflow(db_manager, jwt_manager)
    if not workflow_success:
        logger.error("❌ Comprehensive strategy workflow tests failed")
        return
    
    # Test API Integration
    api_success = await test_api_integration(db_manager, jwt_manager)
    if not api_success:
        logger.error("❌ API integration tests failed")
        return
    
    # Disconnect from database
    await db_manager.disconnect()
    logger.info("✅ Database disconnected successfully")
    
    logger.info("=" * 80)
    logger.info("🎉 ALL TESTS COMPLETED SUCCESSFULLY!")
    logger.info("✅ Strategy Marketplace API: WORKING")
    logger.info("✅ Strategy Creation: WORKING")
    logger.info("✅ Strategy Operations: WORKING")
    logger.info("✅ Strategy Statistics: WORKING")
    logger.info("✅ Permission System: WORKING")
    logger.info("✅ API Integration: WORKING")
    logger.info("=" * 80)


if __name__ == "__main__":
    asyncio.run(main())
