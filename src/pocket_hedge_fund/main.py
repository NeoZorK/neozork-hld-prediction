"""NeoZork Pocket Hedge Fund - Main Application Entry Point"""

import logging
import asyncio
import signal
import sys
from typing import Dict, Any, List, Optional
from datetime import datetime
from contextlib import asynccontextmanager
import uvicorn
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse

# Import configuration
from .config.config_manager import ConfigManager, ConfigEnvironment
from .config.database_manager import DatabaseManager, DatabaseConfig, DatabaseType

# Import core components
from .fund_management.fund_manager import FundManager
from .fund_management.portfolio_manager import PortfolioManager
from .fund_management.performance_tracker import PerformanceTracker
from .fund_management.risk_analytics import RiskAnalytics
from .fund_management.reporting_system import ReportingSystem

# Import investor portal
from .investor_portal.dashboard import Dashboard
from .investor_portal.monitoring_system import MonitoringSystem
from .investor_portal.communication_system import CommunicationSystem
from .investor_portal.report_generator import ReportGenerator

# Import strategy marketplace
from .strategy_marketplace.strategy_sharing import StrategySharing
from .strategy_marketplace.licensing_system import LicensingSystem
from .strategy_marketplace.revenue_sharing import RevenueSharing
from .strategy_marketplace.marketplace_analytics import MarketplaceAnalytics

# Import community features
from .community.social_trading import SocialTrading
from .community.leaderboard_system import LeaderboardSystem
from .community.forum_system import ForumSystem
from .community.gamification_system import GamificationSystem

# Import autonomous bot
from .autonomous_bot.self_learning_engine import SelfLearningEngine
from .autonomous_bot.adaptive_strategy_manager import AdaptiveStrategyManager
from .autonomous_bot.self_monitoring_system import SelfMonitoringSystem
from .autonomous_bot.self_retraining_system import SelfRetrainingSystem

# Import blockchain integration
from .blockchain_integration.multi_chain_manager import MultiChainManager
from .blockchain_integration.tokenization_system import TokenizationSystem
from .blockchain_integration.dao_governance import DAOGovernance

# Import API endpoints
from .api.fund_api import router as fund_router
from .api.investor_api import router as investor_router
from .api.strategy_api import router as strategy_router
from .api.community_api import router as community_router

logger = logging.getLogger(__name__)


class NeoZorkPocketHedgeFund:
    """Main NeoZork Pocket Hedge Fund application class."""
    
    def __init__(self, environment: str = "development"):
        self.environment = ConfigEnvironment(environment)
        self.config_manager = None
        self.database_manager = None
        self.fastapi_app = None
        
        # Core components
        self.fund_manager = None
        self.portfolio_manager = None
        self.performance_tracker = None
        self.risk_analytics = None
        self.reporting_system = None
        
        # Investor portal
        self.dashboard = None
        self.monitoring_system = None
        self.communication_system = None
        self.report_generator = None
        
        # Strategy marketplace
        self.strategy_sharing = None
        self.licensing_system = None
        self.revenue_sharing = None
        self.marketplace_analytics = None
        
        # Community features
        self.social_trading = None
        self.leaderboard_system = None
        self.forum_system = None
        self.gamification_system = None
        
        # Autonomous bot
        self.self_learning_engine = None
        self.adaptive_strategy_manager = None
        self.self_monitoring_system = None
        self.self_retraining_system = None
        
        # Blockchain integration
        self.multi_chain_manager = None
        self.tokenization_system = None
        self.dao_governance = None
        
        # Application state
        self.is_initialized = False
        self.is_running = False
        self.startup_time = None
        
    async def initialize(self) -> Dict[str, Any]:
        """Initialize the application."""
        try:
            logger.info("Initializing NeoZork Pocket Hedge Fund...")
            
            # Initialize configuration manager
            self.config_manager = ConfigManager(self.environment)
            await self.config_manager.load_config_from_environment()
            
            # Initialize database manager
            db_config = await self._get_database_config()
            self.database_manager = DatabaseManager(db_config)
            await self.database_manager.connect()
            
            # Initialize core components
            await self._initialize_core_components()
            
            # Initialize investor portal
            await self._initialize_investor_portal()
            
            # Initialize strategy marketplace
            await self._initialize_strategy_marketplace()
            
            # Initialize community features
            await self._initialize_community_features()
            
            # Initialize autonomous bot
            await self._initialize_autonomous_bot()
            
            # Initialize blockchain integration
            await self._initialize_blockchain_integration()
            
            # Initialize FastAPI application
            await self._initialize_fastapi_app()
            
            self.is_initialized = True
            self.startup_time = datetime.now()
            
            logger.info("NeoZork Pocket Hedge Fund initialized successfully")
            return {
                'status': 'success',
                'message': 'Application initialized successfully',
                'startup_time': self.startup_time,
                'environment': self.environment.value
            }
            
        except Exception as e:
            logger.error(f"Failed to initialize application: {e}")
            return {'error': str(e)}
    
    async def _get_database_config(self) -> DatabaseConfig:
        """Get database configuration from config manager."""
        try:
            db_config = await self.config_manager.get_config_section("database")
            if 'error' in db_config:
                # Use default configuration
                return DatabaseConfig(
                    db_type=DatabaseType.POSTGRESQL,
                    host="localhost",
                    port=5432,
                    database="neozork_fund",
                    username="postgres",
                    password=""
                )
            
            db_data = db_config['data']
            return DatabaseConfig(
                db_type=DatabaseType(db_data.get('type', 'postgresql')),
                host=db_data.get('host', 'localhost'),
                port=int(db_data.get('port', 5432)),
                database=db_data.get('name', 'neozork_fund'),
                username=db_data.get('username', 'postgres'),
                password=db_data.get('password', '')
            )
            
        except Exception as e:
            logger.error(f"Failed to get database config: {e}")
            # Return default configuration
            return DatabaseConfig(
                db_type=DatabaseType.POSTGRESQL,
                host="localhost",
                port=5432,
                database="neozork_fund",
                username="postgres",
                password=""
            )
    
    async def _initialize_core_components(self):
        """Initialize core fund management components."""
        try:
            # Initialize fund manager
            self.fund_manager = FundManager()
            await self.fund_manager.initialize()
            
            # Initialize portfolio manager
            self.portfolio_manager = PortfolioManager()
            await self.portfolio_manager.initialize()
            
            # Initialize performance tracker
            self.performance_tracker = PerformanceTracker()
            await self.performance_tracker.initialize()
            
            # Initialize risk analytics
            self.risk_analytics = RiskAnalytics()
            await self.risk_analytics.initialize()
            
            # Initialize reporting system
            self.reporting_system = ReportingSystem()
            await self.reporting_system.initialize()
            
            logger.info("Core components initialized")
            
        except Exception as e:
            logger.error(f"Failed to initialize core components: {e}")
            raise
    
    async def _initialize_investor_portal(self):
        """Initialize investor portal components."""
        try:
            # Initialize dashboard
            self.dashboard = Dashboard()
            await self.dashboard.initialize()
            
            # Initialize monitoring system
            self.monitoring_system = MonitoringSystem()
            await self.monitoring_system.initialize()
            
            # Initialize communication system
            self.communication_system = CommunicationSystem()
            await self.communication_system.initialize()
            
            # Initialize report generator
            self.report_generator = ReportGenerator()
            await self.report_generator.initialize()
            
            logger.info("Investor portal components initialized")
            
        except Exception as e:
            logger.error(f"Failed to initialize investor portal: {e}")
            raise
    
    async def _initialize_strategy_marketplace(self):
        """Initialize strategy marketplace components."""
        try:
            # Initialize strategy sharing
            self.strategy_sharing = StrategySharing()
            await self.strategy_sharing.initialize()
            
            # Initialize licensing system
            self.licensing_system = LicensingSystem()
            await self.licensing_system.initialize()
            
            # Initialize revenue sharing
            self.revenue_sharing = RevenueSharing()
            await self.revenue_sharing.initialize()
            
            # Initialize marketplace analytics
            self.marketplace_analytics = MarketplaceAnalytics()
            await self.marketplace_analytics.initialize()
            
            logger.info("Strategy marketplace components initialized")
            
        except Exception as e:
            logger.error(f"Failed to initialize strategy marketplace: {e}")
            raise
    
    async def _initialize_community_features(self):
        """Initialize community features."""
        try:
            # Initialize social trading
            self.social_trading = SocialTrading()
            await self.social_trading.initialize()
            
            # Initialize leaderboard system
            self.leaderboard_system = LeaderboardSystem()
            await self.leaderboard_system.initialize()
            
            # Initialize forum system
            self.forum_system = ForumSystem()
            await self.forum_system.initialize()
            
            # Initialize gamification system
            self.gamification_system = GamificationSystem()
            await self.gamification_system.initialize()
            
            logger.info("Community features initialized")
            
        except Exception as e:
            logger.error(f"Failed to initialize community features: {e}")
            raise
    
    async def _initialize_autonomous_bot(self):
        """Initialize autonomous bot components."""
        try:
            # Initialize self-learning engine
            self.self_learning_engine = SelfLearningEngine()
            await self.self_learning_engine.initialize()
            
            # Initialize adaptive strategy manager
            self.adaptive_strategy_manager = AdaptiveStrategyManager()
            await self.adaptive_strategy_manager.initialize()
            
            # Initialize self-monitoring system
            self.self_monitoring_system = SelfMonitoringSystem()
            await self.self_monitoring_system.initialize()
            
            # Initialize self-retraining system
            self.self_retraining_system = SelfRetrainingSystem()
            await self.self_retraining_system.initialize()
            
            logger.info("Autonomous bot components initialized")
            
        except Exception as e:
            logger.error(f"Failed to initialize autonomous bot: {e}")
            raise
    
    async def _initialize_blockchain_integration(self):
        """Initialize blockchain integration components."""
        try:
            # Initialize multi-chain manager
            self.multi_chain_manager = MultiChainManager()
            await self.multi_chain_manager.initialize()
            
            # Initialize tokenization system
            self.tokenization_system = TokenizationSystem()
            await self.tokenization_system.initialize()
            
            # Initialize DAO governance
            self.dao_governance = DAOGovernance()
            await self.dao_governance.initialize()
            
            logger.info("Blockchain integration components initialized")
            
        except Exception as e:
            logger.error(f"Failed to initialize blockchain integration: {e}")
            raise
    
    async def _initialize_fastapi_app(self):
        """Initialize FastAPI application."""
        try:
            # Get API configuration
            api_config = await self.config_manager.get_config_section("api")
            api_data = api_config.get('data', {}) if 'data' in api_config else {}
            
            # Create FastAPI app
            self.fastapi_app = FastAPI(
                title="NeoZork Pocket Hedge Fund API",
                description="AI-powered autonomous hedge fund platform",
                version="1.0.0",
                debug=api_data.get('debug', False)
            )
            
            # Add middleware
            self.fastapi_app.add_middleware(
                CORSMiddleware,
                allow_origins=api_data.get('cors_origins', ["*"]),
                allow_credentials=True,
                allow_methods=["*"],
                allow_headers=["*"]
            )
            self.fastapi_app.add_middleware(GZipMiddleware, minimum_size=1000)
            
            # Add routes
            self.fastapi_app.include_router(fund_router, prefix="/api/v1")
            self.fastapi_app.include_router(investor_router, prefix="/api/v1")
            self.fastapi_app.include_router(strategy_router, prefix="/api/v1")
            self.fastapi_app.include_router(community_router, prefix="/api/v1")
            
            # Add health check endpoint
            @self.fastapi_app.get("/health")
            async def health_check():
                return {
                    'status': 'healthy',
                    'timestamp': datetime.now(),
                    'uptime': (datetime.now() - self.startup_time).total_seconds() if self.startup_time else 0,
                    'environment': self.environment.value
                }
            
            # Add system status endpoint
            @self.fastapi_app.get("/status")
            async def system_status():
                return await self.get_system_status()
            
            logger.info("FastAPI application initialized")
            
        except Exception as e:
            logger.error(f"Failed to initialize FastAPI app: {e}")
            raise
    
    async def start(self) -> Dict[str, Any]:
        """Start the application."""
        try:
            if not self.is_initialized:
                init_result = await self.initialize()
                if 'error' in init_result:
                    return init_result
            
            # Get API configuration
            api_config = await self.config_manager.get_config_section("api")
            api_data = api_config.get('data', {}) if 'data' in api_config else {}
            
            host = api_data.get('host', '0.0.0.0')
            port = int(api_data.get('port', 8000))
            
            # Start the server
            config = uvicorn.Config(
                app=self.fastapi_app,
                host=host,
                port=port,
                log_level="info" if self.environment == ConfigEnvironment.PRODUCTION else "debug"
            )
            server = uvicorn.Server(config)
            
            self.is_running = True
            logger.info(f"Starting NeoZork Pocket Hedge Fund on {host}:{port}")
            
            # Run the server
            await server.serve()
            
        except Exception as e:
            logger.error(f"Failed to start application: {e}")
            return {'error': str(e)}
    
    async def stop(self) -> Dict[str, Any]:
        """Stop the application."""
        try:
            logger.info("Stopping NeoZork Pocket Hedge Fund...")
            
            # Stop autonomous bot components
            if self.self_learning_engine:
                await self.self_learning_engine.stop()
            
            if self.adaptive_strategy_manager:
                await self.adaptive_strategy_manager.stop()
            
            if self.self_monitoring_system:
                await self.self_monitoring_system.stop()
            
            if self.self_retraining_system:
                await self.self_retraining_system.stop()
            
            # Disconnect from database
            if self.database_manager:
                await self.database_manager.disconnect()
            
            self.is_running = False
            logger.info("NeoZork Pocket Hedge Fund stopped successfully")
            
            return {
                'status': 'success',
                'message': 'Application stopped successfully'
            }
            
        except Exception as e:
            logger.error(f"Failed to stop application: {e}")
            return {'error': str(e)}
    
    async def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive system status."""
        try:
            status = {
                'application': {
                    'status': 'running' if self.is_running else 'stopped',
                    'initialized': self.is_initialized,
                    'startup_time': self.startup_time,
                    'uptime': (datetime.now() - self.startup_time).total_seconds() if self.startup_time else 0,
                    'environment': self.environment.value
                },
                'components': {}
            }
            
            # Get component statuses
            if self.fund_manager:
                status['components']['fund_manager'] = self.fund_manager.get_fund_manager_summary()
            
            if self.portfolio_manager:
                status['components']['portfolio_manager'] = self.portfolio_manager.get_portfolio_summary()
            
            if self.performance_tracker:
                status['components']['performance_tracker'] = self.performance_tracker.get_performance_summary()
            
            if self.self_learning_engine:
                status['components']['self_learning_engine'] = self.self_learning_engine.get_learning_engine_summary()
            
            if self.adaptive_strategy_manager:
                status['components']['adaptive_strategy_manager'] = self.adaptive_strategy_manager.get_adaptive_strategy_summary()
            
            if self.multi_chain_manager:
                status['components']['multi_chain_manager'] = self.multi_chain_manager.get_multi_chain_summary()
            
            if self.database_manager:
                status['components']['database_manager'] = self.database_manager.get_database_summary()
            
            return {
                'status': 'success',
                'system_status': status
            }
            
        except Exception as e:
            logger.error(f"Failed to get system status: {e}")
            return {'error': str(e)}


# Global application instance
app_instance = None


async def create_app(environment: str = "development") -> NeoZorkPocketHedgeFund:
    """Create and initialize the application."""
    global app_instance
    
    if app_instance is None:
        app_instance = NeoZorkPocketHedgeFund(environment)
        await app_instance.initialize()
    
    return app_instance


async def main():
    """Main entry point."""
    try:
        # Get environment from command line or default
        environment = sys.argv[1] if len(sys.argv) > 1 else "development"
        
        # Create application
        app = await create_app(environment)
        
        # Setup signal handlers
        def signal_handler(signum, frame):
            logger.info(f"Received signal {signum}, shutting down...")
            asyncio.create_task(app.stop())
        
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
        
        # Start application
        await app.start()
        
    except KeyboardInterrupt:
        logger.info("Received keyboard interrupt, shutting down...")
    except Exception as e:
        logger.error(f"Application error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Run the application
    asyncio.run(main())
