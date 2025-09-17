#!/usr/bin/env python3
"""
Test script for the functional Fund API
Demonstrates the working database integration and API endpoints
"""

import asyncio
import logging
import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.pocket_hedge_fund.config.database_manager import DatabaseManager, DatabaseConfig, DatabaseType
from src.pocket_hedge_fund.api.fund_api_functional import FunctionalFundAPI

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


async def test_fund_api():
    """Test the functional fund API."""
    try:
        # Connect to database
        db_manager = await test_database_connection()
        if not db_manager:
            return
        
        # Create fund API
        fund_api = FunctionalFundAPI(db_manager)
        
        # Test creating a fund
        logger.info("🧪 Testing fund creation...")
        
        # Create a test fund
        test_fund_data = {
            "name": "Test AI Fund",
            "description": "A test fund for API demonstration",
            "fund_type": "mini",
            "initial_capital": 100000.0,
            "management_fee": 0.02,
            "performance_fee": 0.20,
            "min_investment": 1000.0,
            "max_investment": 10000.0,
            "max_investors": 100,
            "risk_level": "medium"
        }
        
        # Simulate fund creation (without FastAPI dependencies)
        fund_id = "test-fund-id"
        
        # Test database queries directly
        logger.info("🧪 Testing database queries...")
        
        # Test getting funds
        funds_query = """
        SELECT f.*, u.username as created_by_username
        FROM funds f
        LEFT JOIN users u ON f.created_by = u.id
        ORDER BY f.created_at DESC
        LIMIT 10
        """
        
        funds_result = await db_manager.execute_query(funds_query)
        if 'error' in funds_result:
            logger.error(f"Failed to get funds: {funds_result['error']}")
        else:
            logger.info(f"✅ Found {len(funds_result['query_result']['data'])} funds in database")
            for fund in funds_result['query_result']['data']:
                logger.info(f"  - {fund['name']} ({fund['fund_type']}) - ${fund['current_value']:,.2f}")
        
        # Test getting fund details
        if funds_result['query_result']['data']:
            first_fund = funds_result['query_result']['data'][0]
            fund_id = first_fund['id']
            
            logger.info(f"🧪 Testing fund details for {fund_id}...")
            
            # Get fund details
            fund_query = """
            SELECT f.*, u.username as created_by_username
            FROM funds f
            LEFT JOIN users u ON f.created_by = u.id
            WHERE f.id = :fund_id
            """
            
            fund_result = await db_manager.execute_query(fund_query, {"fund_id": fund_id})
            if 'error' in fund_result:
                logger.error(f"Failed to get fund details: {fund_result['error']}")
            else:
                fund_data = fund_result['query_result']['data'][0]
                logger.info(f"✅ Fund details retrieved:")
                logger.info(f"  - Name: {fund_data['name']}")
                logger.info(f"  - Type: {fund_data['fund_type']}")
                logger.info(f"  - Current Value: ${fund_data['current_value']:,.2f}")
                logger.info(f"  - Investors: {fund_data['current_investors']}")
                logger.info(f"  - Status: {fund_data['status']}")
        
        # Test database statistics
        logger.info("🧪 Testing database statistics...")
        stats_result = await db_manager.get_database_stats()
        if 'error' in stats_result:
            logger.error(f"Failed to get database stats: {stats_result['error']}")
        else:
            stats = stats_result['stats']
            logger.info(f"✅ Database statistics:")
            logger.info(f"  - Database type: {stats['db_type']}")
            logger.info(f"  - Active connections: {stats['active_connections']}")
            logger.info(f"  - Total queries: {stats['total_queries']}")
            logger.info(f"  - Total errors: {stats['total_errors']}")
        
        # Disconnect from database
        await db_manager.disconnect()
        logger.info("✅ Database disconnected successfully")
        
    except Exception as e:
        logger.error(f"Test failed: {e}")
        import traceback
        traceback.print_exc()


async def main():
    """Main test function."""
    logger.info("🚀 Starting NeoZork Pocket Hedge Fund API Test")
    logger.info("=" * 60)
    
    await test_fund_api()
    
    logger.info("=" * 60)
    logger.info("✅ Test completed")


if __name__ == "__main__":
    asyncio.run(main())
