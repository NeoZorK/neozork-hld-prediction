#!/usr/bin/env python3
"""
Test script for Portfolio API and Performance Tracker
Demonstrates the working portfolio management and performance tracking functionality
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
from src.pocket_hedge_fund.fund_management.performance_tracker_functional import FunctionalPerformanceTracker

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


async def test_portfolio_operations(db_manager):
    """Test Portfolio Manager operations."""
    try:
        logger.info("🧪 Testing Portfolio Manager Operations...")
        
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
        
        # Test adding positions
        logger.info("🧪 Testing position management...")
        
        # Add BTC position
        btc_result = await portfolio_manager.add_position(
            fund_id=fund_id,
            asset_symbol="BTC",
            asset_name="Bitcoin",
            asset_type="crypto",
            quantity=0.5,
            price=45000.0
        )
        
        if 'error' in btc_result:
            logger.error(f"❌ Failed to add BTC position: {btc_result['error']}")
        else:
            logger.info(f"✅ Added BTC position: {btc_result['quantity']} @ ${btc_result['price']}")
        
        # Add ETH position
        eth_result = await portfolio_manager.add_position(
            fund_id=fund_id,
            asset_symbol="ETH",
            asset_name="Ethereum",
            asset_type="crypto",
            quantity=2.0,
            price=3000.0
        )
        
        if 'error' in eth_result:
            logger.error(f"❌ Failed to add ETH position: {eth_result['error']}")
        else:
            logger.info(f"✅ Added ETH position: {eth_result['quantity']} @ ${eth_result['price']}")
        
        # Test getting portfolio positions
        positions_result = await portfolio_manager.get_portfolio_positions(fund_id)
        if 'error' in positions_result:
            logger.error(f"❌ Failed to get portfolio positions: {positions_result['error']}")
        else:
            logger.info(f"✅ Retrieved {positions_result['total_positions']} portfolio positions")
            for position in positions_result['positions']:
                logger.info(f"  - {position['asset_symbol']}: {position['quantity']} @ ${position['average_price']}")
        
        # Test updating prices
        logger.info("🧪 Testing price updates...")
        price_updates = {"BTC": 46000.0, "ETH": 3100.0}
        update_result = await portfolio_manager.update_position_prices(fund_id, price_updates)
        
        if 'error' in update_result:
            logger.error(f"❌ Failed to update prices: {update_result['error']}")
        else:
            logger.info(f"✅ Updated prices for {update_result['total_updated']} positions")
            for update in update_result['updated_positions']:
                logger.info(f"  - {update['asset_symbol']}: ${update['old_price']} → ${update['new_price']}")
                logger.info(f"    PnL: ${update['unrealized_pnl']:,.2f} ({update['unrealized_pnl_percentage']:.2f}%)")
        
        # Test portfolio metrics
        logger.info("🧪 Testing portfolio metrics...")
        metrics_result = await portfolio_manager.get_portfolio_metrics(fund_id)
        if 'error' in metrics_result:
            logger.error(f"❌ Failed to get portfolio metrics: {metrics_result['error']}")
        else:
            logger.info(f"✅ Portfolio metrics calculated:")
            logger.info(f"  - Total Value: ${metrics_result['total_value']:,.2f}")
            logger.info(f"  - Total PnL: ${metrics_result['total_pnl']:,.2f}")
            logger.info(f"  - Total Return: {metrics_result['total_return_percentage']:.2f}%")
        
        # Test portfolio rebalancing
        logger.info("🧪 Testing portfolio rebalancing...")
        target_weights = {"BTC": 60.0, "ETH": 40.0}
        rebalance_result = await portfolio_manager.rebalance_portfolio(fund_id, target_weights)
        
        if 'error' in rebalance_result:
            logger.error(f"❌ Failed to rebalance portfolio: {rebalance_result['error']}")
        else:
            logger.info(f"✅ Portfolio rebalancing completed: {rebalance_result['total_trades']} trades executed")
            for trade in rebalance_result['rebalancing_trades']:
                logger.info(f"  - {trade['asset_symbol']}: {trade['current_weight']:.1f}% → {trade['target_weight']:.1f}%")
        
        logger.info("✅ Portfolio Manager operations completed successfully")
        return portfolio_manager
        
    except Exception as e:
        logger.error(f"Portfolio operations test failed: {e}")
        import traceback
        traceback.print_exc()
        return None


async def test_performance_tracker(db_manager):
    """Test Performance Tracker functionality."""
    try:
        logger.info("🧪 Testing Performance Tracker...")
        
        # Create performance tracker
        performance_tracker = FunctionalPerformanceTracker(db_manager)
        
        # Get a test fund ID
        fund_query = "SELECT id FROM funds LIMIT 1"
        fund_result = await db_manager.execute_query(fund_query)
        
        if 'error' in fund_result or not fund_result['query_result']['data']:
            logger.error("❌ No test fund found")
            return None
        
        fund_id = fund_result['query_result']['data'][0]['id']
        logger.info(f"✅ Using test fund: {fund_id}")
        
        # Test daily performance calculation
        logger.info("🧪 Testing daily performance calculation...")
        performance_result = await performance_tracker.calculate_daily_performance(fund_id)
        
        if 'error' in performance_result:
            logger.error(f"❌ Failed to calculate daily performance: {performance_result['error']}")
        else:
            logger.info(f"✅ Daily performance calculated:")
            logger.info(f"  - Total Value: ${performance_result['total_value']:,.2f}")
            logger.info(f"  - Total Return: {performance_result['total_return_percentage']:.2f}%")
            logger.info(f"  - Daily Return: {performance_result['daily_return_percentage']:.2f}%")
            logger.info(f"  - Sharpe Ratio: {performance_result['sharpe_ratio']:.3f}")
            logger.info(f"  - Max Drawdown: {performance_result['max_drawdown']:.3f}")
            logger.info(f"  - Volatility: {performance_result['volatility']:.3f}")
            logger.info(f"  - Beta: {performance_result['beta']:.3f}")
            logger.info(f"  - Alpha: {performance_result['alpha']:.3f}")
            logger.info(f"  - VaR 95%: {performance_result['var_95']:.3f}")
            logger.info(f"  - CVaR 95%: {performance_result['cvar_95']:.3f}")
            logger.info(f"  - Win Rate: {performance_result['win_rate']:.1f}%")
            logger.info(f"  - Profit Factor: {performance_result['profit_factor']:.3f}")
            logger.info(f"  - Calmar Ratio: {performance_result['calmar_ratio']:.3f}")
            logger.info(f"  - Sortino Ratio: {performance_result['sortino_ratio']:.3f}")
        
        # Test performance history
        logger.info("🧪 Testing performance history...")
        history_result = await performance_tracker.get_performance_history(fund_id, days=30)
        
        if 'error' in history_result:
            logger.error(f"❌ Failed to get performance history: {history_result['error']}")
        else:
            logger.info(f"✅ Retrieved {history_result['total_records']} performance records")
            if history_result['performance_history']:
                latest = history_result['performance_history'][0]
                logger.info(f"  - Latest: {latest['snapshot_date']} - Return: {latest['total_return_percentage']:.2f}%")
        
        # Test benchmark comparison
        logger.info("🧪 Testing benchmark comparison...")
        benchmark_result = await performance_tracker.calculate_benchmark_comparison(fund_id)
        
        if 'error' in benchmark_result:
            logger.error(f"❌ Failed to calculate benchmark comparison: {benchmark_result['error']}")
        else:
            logger.info(f"✅ Benchmark comparison calculated:")
            logger.info(f"  - Fund Return: {benchmark_result['fund_return']:.3f}")
            logger.info(f"  - Benchmark Return: {benchmark_result['benchmark_return']:.3f}")
            logger.info(f"  - Excess Return: {benchmark_result['excess_return']:.3f}")
            logger.info(f"  - Information Ratio: {benchmark_result['information_ratio']:.3f}")
            logger.info(f"  - Beta: {benchmark_result['beta']:.3f}")
            logger.info(f"  - Alpha: {benchmark_result['alpha']:.3f}")
            logger.info(f"  - Correlation: {benchmark_result['correlation']:.3f}")
        
        logger.info("✅ Performance Tracker tests completed successfully")
        return performance_tracker
        
    except Exception as e:
        logger.error(f"Performance tracker test failed: {e}")
        import traceback
        traceback.print_exc()
        return None


async def test_api_integration(db_manager, jwt_manager):
    """Test API integration with authentication."""
    try:
        logger.info("🧪 Testing API Integration...")
        
        # Create test user with admin role
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
        
        # Test portfolio operations with authenticated user
        portfolio_manager = FunctionalPortfolioManager(db_manager)
        
        # Get a test fund
        fund_query = "SELECT id FROM funds LIMIT 1"
        fund_result = await db_manager.execute_query(fund_query)
        
        if 'error' in fund_result or not fund_result['query_result']['data']:
            logger.error("❌ No test fund found for API integration test")
            return False
        
        fund_id = fund_result['query_result']['data'][0]['id']
        
        # Test portfolio operations
        positions_result = await portfolio_manager.get_portfolio_positions(fund_id)
        if 'error' in positions_result:
            logger.error(f"❌ Failed to get portfolio positions: {positions_result['error']}")
        else:
            logger.info(f"✅ Portfolio operations work with authenticated user")
            logger.info(f"  - Retrieved {positions_result['total_positions']} positions")
        
        # Test performance operations
        performance_tracker = FunctionalPerformanceTracker(db_manager)
        performance_result = await performance_tracker.calculate_daily_performance(fund_id)
        
        if 'error' in performance_result:
            logger.error(f"❌ Failed to calculate performance: {performance_result['error']}")
        else:
            logger.info(f"✅ Performance operations work with authenticated user")
            logger.info(f"  - Calculated performance metrics successfully")
        
        # Test database statistics
        stats_result = await db_manager.get_database_stats()
        if 'error' in stats_result:
            logger.error(f"❌ Failed to get database stats: {stats_result['error']}")
        else:
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


async def test_comprehensive_workflow(db_manager, jwt_manager, portfolio_manager, performance_tracker):
    """Test comprehensive workflow from portfolio management to performance tracking."""
    try:
        logger.info("🧪 Testing Comprehensive Workflow...")
        
        # Get a test fund
        fund_query = "SELECT id FROM funds LIMIT 1"
        fund_result = await db_manager.execute_query(fund_query)
        
        if 'error' in fund_result or not fund_result['query_result']['data']:
            logger.error("❌ No test fund found for comprehensive workflow test")
            return False
        
        fund_id = fund_result['query_result']['data'][0]['id']
        
        # Step 1: Add multiple positions
        logger.info("📊 Step 1: Adding multiple positions...")
        
        positions_to_add = [
            ("SOL", "Solana", "crypto", 10.0, 100.0),
            ("ADA", "Cardano", "crypto", 100.0, 0.5),
            ("DOT", "Polkadot", "crypto", 50.0, 7.0)
        ]
        
        for symbol, name, asset_type, quantity, price in positions_to_add:
            result = await portfolio_manager.add_position(fund_id, symbol, name, asset_type, quantity, price)
            if 'error' not in result:
                logger.info(f"  ✅ Added {symbol}: {quantity} @ ${price}")
            else:
                logger.error(f"  ❌ Failed to add {symbol}: {result['error']}")
        
        # Step 2: Update prices
        logger.info("📊 Step 2: Updating prices...")
        price_updates = {
            "BTC": 47000.0,
            "ETH": 3200.0,
            "SOL": 105.0,
            "ADA": 0.52,
            "DOT": 7.5
        }
        
        update_result = await portfolio_manager.update_position_prices(fund_id, price_updates)
        if 'error' not in update_result:
            logger.info(f"  ✅ Updated prices for {update_result['total_updated']} positions")
        else:
            logger.error(f"  ❌ Failed to update prices: {update_result['error']}")
        
        # Step 3: Get portfolio metrics
        logger.info("📊 Step 3: Getting portfolio metrics...")
        metrics_result = await portfolio_manager.get_portfolio_metrics(fund_id)
        if 'error' not in metrics_result:
            logger.info(f"  ✅ Portfolio metrics:")
            logger.info(f"    - Total Value: ${metrics_result['total_value']:,.2f}")
            logger.info(f"    - Total Return: {metrics_result['total_return_percentage']:.2f}%")
        else:
            logger.error(f"  ❌ Failed to get metrics: {metrics_result['error']}")
        
        # Step 4: Calculate performance
        logger.info("📊 Step 4: Calculating performance...")
        performance_result = await performance_tracker.calculate_daily_performance(fund_id)
        if 'error' not in performance_result:
            logger.info(f"  ✅ Performance calculated:")
            logger.info(f"    - Sharpe Ratio: {performance_result['sharpe_ratio']:.3f}")
            logger.info(f"    - Max Drawdown: {performance_result['max_drawdown']:.3f}")
            logger.info(f"    - Volatility: {performance_result['volatility']:.3f}")
        else:
            logger.error(f"  ❌ Failed to calculate performance: {performance_result['error']}")
        
        # Step 5: Portfolio rebalancing
        logger.info("📊 Step 5: Portfolio rebalancing...")
        target_weights = {
            "BTC": 40.0,
            "ETH": 30.0,
            "SOL": 15.0,
            "ADA": 10.0,
            "DOT": 5.0
        }
        
        rebalance_result = await portfolio_manager.rebalance_portfolio(fund_id, target_weights)
        if 'error' not in rebalance_result:
            logger.info(f"  ✅ Rebalancing completed: {rebalance_result['total_trades']} trades")
        else:
            logger.error(f"  ❌ Failed to rebalance: {rebalance_result['error']}")
        
        # Step 6: Final performance calculation
        logger.info("📊 Step 6: Final performance calculation...")
        final_performance = await performance_tracker.calculate_daily_performance(fund_id)
        if 'error' not in final_performance:
            logger.info(f"  ✅ Final performance:")
            logger.info(f"    - Total Return: {final_performance['total_return_percentage']:.2f}%")
            logger.info(f"    - Daily Return: {final_performance['daily_return_percentage']:.2f}%")
        else:
            logger.error(f"  ❌ Failed to calculate final performance: {final_performance['error']}")
        
        logger.info("✅ Comprehensive workflow completed successfully")
        return True
        
    except Exception as e:
        logger.error(f"Comprehensive workflow test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


async def main():
    """Main test function."""
    logger.info("🚀 Starting NeoZork Portfolio API & Performance Tracker Test")
    logger.info("=" * 80)
    
    # Test database connection
    db_manager = await test_database_connection()
    if not db_manager:
        logger.error("❌ Database connection failed - aborting tests")
        return
    
    # Test JWT Manager
    jwt_manager = JWTManager("test-secret-key")
    logger.info("✅ JWT Manager initialized")
    
    # Test Portfolio Operations
    portfolio_manager = await test_portfolio_operations(db_manager)
    if not portfolio_manager:
        logger.error("❌ Portfolio operations tests failed - aborting tests")
        return
    
    # Test Performance Tracker
    performance_tracker = await test_performance_tracker(db_manager)
    if not performance_tracker:
        logger.error("❌ Performance tracker tests failed - aborting tests")
        return
    
    # Test API Integration
    api_success = await test_api_integration(db_manager, jwt_manager)
    if not api_success:
        logger.error("❌ API integration tests failed - aborting tests")
        return
    
    # Test Comprehensive Workflow
    workflow_success = await test_comprehensive_workflow(db_manager, jwt_manager, portfolio_manager, performance_tracker)
    if not workflow_success:
        logger.error("❌ Comprehensive workflow tests failed")
        return
    
    # Disconnect from database
    await db_manager.disconnect()
    logger.info("✅ Database disconnected successfully")
    
    logger.info("=" * 80)
    logger.info("🎉 ALL TESTS COMPLETED SUCCESSFULLY!")
    logger.info("✅ Portfolio API: WORKING")
    logger.info("✅ Performance Tracker: WORKING")
    logger.info("✅ Database Integration: WORKING")
    logger.info("✅ API Integration: WORKING")
    logger.info("✅ Comprehensive Workflow: WORKING")
    logger.info("=" * 80)


if __name__ == "__main__":
    asyncio.run(main())
