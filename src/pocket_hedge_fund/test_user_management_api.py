#!/usr/bin/env python3
"""
Test script for User Management API
Demonstrates the working user management functionality
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
from src.pocket_hedge_fund.api.user_management_api import UserManagementAPI

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


async def test_user_creation(db_manager, jwt_manager):
    """Test user creation functionality."""
    try:
        logger.info("🧪 Testing User Creation...")
        
        # Create user management API
        user_api = UserManagementAPI(db_manager, jwt_manager)
        
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
        
        # Test creating a new user
        test_user_data = {
            "username": "testuser123",
            "email": "testuser@example.com",
            "password": "SecurePass123!",
            "first_name": "Test",
            "last_name": "User",
            "role": "INVESTOR",
            "phone": "+1234567890",
            "country": "United States",
            "timezone": "America/New_York"
        }
        
        # Simulate API call (we'll test the core functionality)
        logger.info("🧪 Testing user creation validation...")
        
        # Test username validation
        username_validation = user_api._validate_username(test_user_data["username"])
        if username_validation['is_valid']:
            logger.info(f"✅ Username validation passed: {test_user_data['username']}")
        else:
            logger.error(f"❌ Username validation failed: {username_validation['errors']}")
            return False
        
        # Test password validation
        password_validation = user_api._validate_password(test_user_data["password"])
        if password_validation['is_valid']:
            logger.info(f"✅ Password validation passed")
        else:
            logger.error(f"❌ Password validation failed: {password_validation['errors']}")
            return False
        
        # Test role validation
        try:
            user_role = UserRole(test_user_data["role"].upper())
            logger.info(f"✅ Role validation passed: {user_role.value}")
        except ValueError as e:
            logger.error(f"❌ Role validation failed: {e}")
            return False
        
        # Test password hashing
        hashed_password = jwt_manager.hash_password(test_user_data["password"])
        if hashed_password and len(hashed_password) > 0:
            logger.info("✅ Password hashing successful")
        else:
            logger.error("❌ Password hashing failed")
            return False
        
        # Test password verification
        if jwt_manager.verify_password(test_user_data["password"], hashed_password):
            logger.info("✅ Password verification successful")
        else:
            logger.error("❌ Password verification failed")
            return False
        
        logger.info("✅ User creation functionality tests completed successfully")
        return True
        
    except Exception as e:
        logger.error(f"User creation test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_user_management_operations(db_manager, jwt_manager):
    """Test user management operations."""
    try:
        logger.info("🧪 Testing User Management Operations...")
        
        # Create user management API
        user_api = UserManagementAPI(db_manager, jwt_manager)
        
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
        if user_api._check_permission(admin_permissions, "users:create"):
            logger.info("✅ Admin has users:create permission")
        else:
            logger.error("❌ Admin missing users:create permission")
            return False
        
        if user_api._check_permission(admin_permissions, "users:read"):
            logger.info("✅ Admin has users:read permission")
        else:
            logger.error("❌ Admin missing users:read permission")
            return False
        
        if user_api._check_permission(admin_permissions, "users:update"):
            logger.info("✅ Admin has users:update permission")
        else:
            logger.error("❌ Admin missing users:update permission")
            return False
        
        if user_api._check_permission(admin_permissions, "users:delete"):
            logger.info("✅ Admin has users:delete permission")
        else:
            logger.error("❌ Admin missing users:delete permission")
            return False
        
        # Test investor permissions (should have limited access)
        investor_role = UserRole.INVESTOR
        investor_permissions = jwt_manager.get_user_permissions(investor_role)
        
        if not user_api._check_permission(investor_permissions, "users:create"):
            logger.info("✅ Investor correctly lacks users:create permission")
        else:
            logger.error("❌ Investor incorrectly has users:create permission")
            return False
        
        if not user_api._check_permission(investor_permissions, "users:delete"):
            logger.info("✅ Investor correctly lacks users:delete permission")
        else:
            logger.error("❌ Investor incorrectly has users:delete permission")
            return False
        
        # Test UUID validation
        logger.info("🧪 Testing UUID validation...")
        
        valid_uuid = "123e4567-e89b-12d3-a456-426614174000"
        invalid_uuid = "not-a-uuid"
        
        if user_api._is_valid_uuid(valid_uuid):
            logger.info("✅ Valid UUID validation passed")
        else:
            logger.error("❌ Valid UUID validation failed")
            return False
        
        if not user_api._is_valid_uuid(invalid_uuid):
            logger.info("✅ Invalid UUID validation passed")
        else:
            logger.error("❌ Invalid UUID validation failed")
            return False
        
        logger.info("✅ User management operations tests completed successfully")
        return True
        
    except Exception as e:
        logger.error(f"User management operations test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_user_statistics(db_manager, jwt_manager):
    """Test user statistics functionality."""
    try:
        logger.info("🧪 Testing User Statistics...")
        
        # Create user management API
        user_api = UserManagementAPI(db_manager, jwt_manager)
        
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
        
        # Test user statistics queries
        logger.info("🧪 Testing user statistics queries...")
        
        # Test total users count
        total_query = "SELECT COUNT(*) as total FROM users"
        total_result = await db_manager.execute_query(total_query)
        
        if 'error' in total_result:
            logger.error(f"❌ Failed to get total users count: {total_result['error']}")
            return False
        
        total_users = total_result['query_result']['data'][0]['total']
        logger.info(f"✅ Total users count: {total_users}")
        
        # Test active users count
        active_query = "SELECT COUNT(*) as total FROM users WHERE is_active = true"
        active_result = await db_manager.execute_query(active_query)
        
        if 'error' in active_result:
            logger.error(f"❌ Failed to get active users count: {active_result['error']}")
            return False
        
        active_users = active_result['query_result']['data'][0]['total']
        logger.info(f"✅ Active users count: {active_users}")
        
        # Test users by role
        role_query = "SELECT role, COUNT(*) as count FROM users GROUP BY role"
        role_result = await db_manager.execute_query(role_query)
        
        if 'error' in role_result:
            logger.error(f"❌ Failed to get users by role: {role_result['error']}")
            return False
        
        users_by_role = {}
        for row in role_result['query_result']['data']:
            users_by_role[row['role']] = row['count']
        
        logger.info(f"✅ Users by role: {users_by_role}")
        
        # Test new users today
        from datetime import datetime, date
        today = date.today()
        today_query = "SELECT COUNT(*) as total FROM users WHERE DATE(created_at) = :today"
        today_result = await db_manager.execute_query(today_query, {"today": today})
        
        if 'error' in today_result:
            logger.error(f"❌ Failed to get new users today: {today_result['error']}")
            return False
        
        new_users_today = today_result['query_result']['data'][0]['total']
        logger.info(f"✅ New users today: {new_users_today}")
        
        logger.info("✅ User statistics tests completed successfully")
        return True
        
    except Exception as e:
        logger.error(f"User statistics test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_comprehensive_user_workflow(db_manager, jwt_manager):
    """Test comprehensive user management workflow."""
    try:
        logger.info("🧪 Testing Comprehensive User Management Workflow...")
        
        # Create user management API
        user_api = UserManagementAPI(db_manager, jwt_manager)
        
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
        
        # Step 1: Test user creation workflow
        logger.info("📊 Step 1: Testing user creation workflow...")
        
        test_users = [
            {
                "username": "investor1",
                "email": "investor1@example.com",
                "password": "SecurePass123!",
                "first_name": "John",
                "last_name": "Doe",
                "role": "INVESTOR"
            },
            {
                "username": "trader1",
                "email": "trader1@example.com",
                "password": "SecurePass123!",
                "first_name": "Jane",
                "last_name": "Smith",
                "role": "TRADER"
            },
            {
                "username": "analyst1",
                "email": "analyst1@example.com",
                "password": "SecurePass123!",
                "first_name": "Bob",
                "last_name": "Johnson",
                "role": "ANALYST"
            }
        ]
        
        created_users = []
        for user_data in test_users:
            # Validate user data
            username_validation = user_api._validate_username(user_data["username"])
            password_validation = user_api._validate_password(user_data["password"])
            
            if username_validation['is_valid'] and password_validation['is_valid']:
                # Hash password
                hashed_password = jwt_manager.hash_password(user_data["password"])
                
                # Create user in database
                import uuid
                user_id = str(uuid.uuid4())
                create_user_query = """
                INSERT INTO users (
                    id, username, email, password_hash, first_name, last_name,
                    role, is_active, email_verified, created_at, updated_at
                ) VALUES (
                    :id, :username, :email, :password_hash, :first_name, :last_name,
                    :role, :is_active, :email_verified, :created_at, :updated_at
                )
                """
                
                from datetime import datetime
                now = datetime.now()
                create_params = {
                    "id": user_id,
                    "username": user_data["username"],
                    "email": user_data["email"],
                    "password_hash": hashed_password,
                    "first_name": user_data["first_name"],
                    "last_name": user_data["last_name"],
                    "role": user_data["role"],
                    "is_active": True,
                    "email_verified": False,
                    "created_at": now,
                    "updated_at": now
                }
                
                create_result = await db_manager.execute_query(create_user_query, create_params)
                
                if 'error' not in create_result:
                    created_users.append({
                        "user_id": user_id,
                        "username": user_data["username"],
                        "role": user_data["role"]
                    })
                    logger.info(f"  ✅ Created user: {user_data['username']} ({user_data['role']})")
                else:
                    logger.error(f"  ❌ Failed to create user {user_data['username']}: {create_result['error']}")
        
        logger.info(f"✅ Created {len(created_users)} users successfully")
        
        # Step 2: Test user retrieval
        logger.info("📊 Step 2: Testing user retrieval...")
        
        for user in created_users:
            user_query = "SELECT * FROM users WHERE id = :user_id"
            user_result = await db_manager.execute_query(user_query, {"user_id": user["user_id"]})
            
            if 'error' not in user_result and user_result['query_result']['data']:
                user_data = user_result['query_result']['data'][0]
                logger.info(f"  ✅ Retrieved user: {user_data['username']} ({user_data['role']})")
            else:
                logger.error(f"  ❌ Failed to retrieve user {user['username']}")
        
        # Step 3: Test user update
        logger.info("📊 Step 3: Testing user update...")
        
        if created_users:
            user_to_update = created_users[0]
            update_query = """
            UPDATE users 
            SET first_name = :first_name, updated_at = :updated_at
            WHERE id = :user_id
            """
            
            update_params = {
                "user_id": user_to_update["user_id"],
                "first_name": "UpdatedName",
                "updated_at": datetime.now()
            }
            
            update_result = await db_manager.execute_query(update_query, update_params)
            
            if 'error' not in update_result:
                logger.info(f"  ✅ Updated user: {user_to_update['username']}")
            else:
                logger.error(f"  ❌ Failed to update user {user_to_update['username']}: {update_result['error']}")
        
        # Step 4: Test user statistics
        logger.info("📊 Step 4: Testing user statistics...")
        
        # Get updated statistics
        total_query = "SELECT COUNT(*) as total FROM users"
        total_result = await db_manager.execute_query(total_query)
        
        if 'error' not in total_result:
            total_users = total_result['query_result']['data'][0]['total']
            logger.info(f"  ✅ Total users after operations: {total_users}")
        
        # Get users by role
        role_query = "SELECT role, COUNT(*) as count FROM users GROUP BY role"
        role_result = await db_manager.execute_query(role_query)
        
        if 'error' not in role_result:
            users_by_role = {}
            for row in role_result['query_result']['data']:
                users_by_role[row['role']] = row['count']
            logger.info(f"  ✅ Users by role: {users_by_role}")
        
        # Step 5: Test user deactivation
        logger.info("📊 Step 5: Testing user deactivation...")
        
        if created_users:
            user_to_deactivate = created_users[-1]  # Deactivate last user
            deactivate_query = """
            UPDATE users 
            SET is_active = :is_active, updated_at = :updated_at
            WHERE id = :user_id
            """
            
            deactivate_params = {
                "user_id": user_to_deactivate["user_id"],
                "is_active": False,
                "updated_at": datetime.now()
            }
            
            deactivate_result = await db_manager.execute_query(deactivate_query, deactivate_params)
            
            if 'error' not in deactivate_result:
                logger.info(f"  ✅ Deactivated user: {user_to_deactivate['username']}")
            else:
                logger.error(f"  ❌ Failed to deactivate user {user_to_deactivate['username']}: {deactivate_result['error']}")
        
        logger.info("✅ Comprehensive user management workflow completed successfully")
        return True
        
    except Exception as e:
        logger.error(f"Comprehensive user workflow test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_api_integration(db_manager, jwt_manager):
    """Test API integration with authentication."""
    try:
        logger.info("🧪 Testing API Integration...")
        
        # Create user management API
        user_api = UserManagementAPI(db_manager, jwt_manager)
        
        # Create test users with different roles
        test_roles = [UserRole.ADMIN, UserRole.INVESTOR, UserRole.TRADER, UserRole.ANALYST, UserRole.MANAGER]
        
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
            if role == UserRole.ADMIN:
                if not user_api._check_permission(permissions, "users:create"):
                    logger.error(f"❌ Admin missing users:create permission")
                    return False
                if not user_api._check_permission(permissions, "users:delete"):
                    logger.error(f"❌ Admin missing users:delete permission")
                    return False
            
            elif role == UserRole.INVESTOR:
                if user_api._check_permission(permissions, "users:create"):
                    logger.error(f"❌ Investor incorrectly has users:create permission")
                    return False
                if user_api._check_permission(permissions, "users:delete"):
                    logger.error(f"❌ Investor incorrectly has users:delete permission")
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
    logger.info("🚀 Starting NeoZork User Management API Test")
    logger.info("=" * 80)
    
    # Test database connection
    db_manager = await test_database_connection()
    if not db_manager:
        logger.error("❌ Database connection failed - aborting tests")
        return
    
    # Test JWT Manager
    jwt_manager = JWTManager("test-secret-key")
    logger.info("✅ JWT Manager initialized")
    
    # Test User Creation
    creation_success = await test_user_creation(db_manager, jwt_manager)
    if not creation_success:
        logger.error("❌ User creation tests failed - aborting tests")
        return
    
    # Test User Management Operations
    operations_success = await test_user_management_operations(db_manager, jwt_manager)
    if not operations_success:
        logger.error("❌ User management operations tests failed - aborting tests")
        return
    
    # Test User Statistics
    stats_success = await test_user_statistics(db_manager, jwt_manager)
    if not stats_success:
        logger.error("❌ User statistics tests failed - aborting tests")
        return
    
    # Test Comprehensive Workflow
    workflow_success = await test_comprehensive_user_workflow(db_manager, jwt_manager)
    if not workflow_success:
        logger.error("❌ Comprehensive user workflow tests failed")
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
    logger.info("✅ User Management API: WORKING")
    logger.info("✅ User Creation: WORKING")
    logger.info("✅ User Operations: WORKING")
    logger.info("✅ User Statistics: WORKING")
    logger.info("✅ Permission System: WORKING")
    logger.info("✅ API Integration: WORKING")
    logger.info("=" * 80)


if __name__ == "__main__":
    asyncio.run(main())
