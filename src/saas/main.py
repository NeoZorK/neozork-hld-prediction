"""
NeoZork SaaS Platform Main Entry Point

This module provides the main entry point for the NeoZork SaaS platform,
initializing all services and starting the API server.
"""

import asyncio
import logging
import signal
import sys
from pathlib import Path
from typing import Dict, Any

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.saas.api import SaaSAPI
from src.saas.services import (
    TenantService,
    SubscriptionService,
    BillingService,
    CustomerService,
    UsageService,
    PlanService
)
from src.saas.models.plan import Plan, PlanType, PlanStatus
from src.saas.models.feature import Feature, FeatureType, FeatureAccess

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class NeoZorkSaaSPlatform:
    """
    Main SaaS Platform class that orchestrates all services and components.
    
    This class provides:
    - Service initialization and configuration
    - Default data setup (plans, features)
    - API server management
    - Graceful shutdown handling
    """
    
    def __init__(self):
        self.api = None
        self.services = {}
        self.running = False
        
        # Setup signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
    
    async def initialize(self):
        """Initialize all SaaS services and components."""
        try:
            logger.info("Initializing NeoZork SaaS Platform...")
            
            # Initialize services
            self.services['tenant'] = TenantService()
            self.services['subscription'] = SubscriptionService()
            self.services['billing'] = BillingService()
            self.services['customer'] = CustomerService()
            self.services['usage'] = UsageService()
            self.services['plan'] = PlanService()
            
            # Initialize API
            self.api = SaaSAPI()
            
            # Setup default data
            await self._setup_default_data()
            
            logger.info("NeoZork SaaS Platform initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize SaaS platform: {e}")
            raise
    
    async def _setup_default_data(self):
        """Setup default plans and features."""
        try:
            logger.info("Setting up default plans and features...")
            
            # Create default features
            features = await self._create_default_features()
            
            # Create default plans
            plans = await self._create_default_plans(features)
            
            logger.info(f"Created {len(features)} features and {len(plans)} plans")
            
        except Exception as e:
            logger.error(f"Failed to setup default data: {e}")
            raise
    
    async def _create_default_features(self) -> Dict[str, Feature]:
        """Create default features for the platform."""
        features = {}
        
        # Core features
        core_features = [
            {
                "name": "basic_trading",
                "display_name": "Basic Trading",
                "description": "Basic trading functionality with paper trading",
                "feature_type": FeatureType.CORE,
                "access_level": FeatureAccess.FREE,
                "category": "trading"
            },
            {
                "name": "technical_indicators",
                "display_name": "Technical Indicators",
                "description": "Access to basic technical indicators",
                "feature_type": FeatureType.CORE,
                "access_level": FeatureAccess.FREE,
                "category": "analysis"
            },
            {
                "name": "data_export",
                "display_name": "Data Export",
                "description": "Export trading data to CSV/JSON",
                "feature_type": FeatureType.CORE,
                "access_level": FeatureAccess.FREE,
                "category": "data"
            }
        ]
        
        # Premium features
        premium_features = [
            {
                "name": "live_trading",
                "display_name": "Live Trading",
                "description": "Execute live trades on real markets",
                "feature_type": FeatureType.PREMIUM,
                "access_level": FeatureAccess.PAID,
                "category": "trading",
                "price": 50.0
            },
            {
                "name": "advanced_indicators",
                "display_name": "Advanced Indicators",
                "description": "Access to advanced technical indicators and custom indicators",
                "feature_type": FeatureType.PREMIUM,
                "access_level": FeatureAccess.PAID,
                "category": "analysis",
                "price": 25.0
            },
            {
                "name": "ml_models",
                "display_name": "ML Models",
                "description": "Access to machine learning models for trading",
                "feature_type": FeatureType.PREMIUM,
                "access_level": FeatureAccess.PAID,
                "category": "ai",
                "price": 100.0
            },
            {
                "name": "backtesting",
                "display_name": "Backtesting",
                "description": "Advanced backtesting capabilities",
                "feature_type": FeatureType.PREMIUM,
                "access_level": FeatureAccess.PAID,
                "category": "analysis",
                "price": 75.0
            }
        ]
        
        # Enterprise features
        enterprise_features = [
            {
                "name": "api_access",
                "display_name": "API Access",
                "description": "Full API access for programmatic trading",
                "feature_type": FeatureType.ENTERPRISE,
                "access_level": FeatureAccess.PAID,
                "category": "api",
                "price": 200.0
            },
            {
                "name": "white_label",
                "display_name": "White Label",
                "description": "White label solution for resellers",
                "feature_type": FeatureType.ENTERPRISE,
                "access_level": FeatureAccess.PAID,
                "category": "business",
                "price": 1000.0
            },
            {
                "name": "dedicated_support",
                "display_name": "Dedicated Support",
                "description": "Dedicated customer support and account manager",
                "feature_type": FeatureType.ENTERPRISE,
                "access_level": FeatureAccess.PAID,
                "category": "support",
                "price": 500.0
            }
        ]
        
        # Create all features
        all_features = core_features + premium_features + enterprise_features
        
        for feature_data in all_features:
            feature = Feature(**feature_data)
            features[feature.name] = feature
        
        return features
    
    async def _create_default_plans(self, features: Dict[str, Feature]) -> Dict[str, Plan]:
        """Create default subscription plans."""
        plans = {}
        
        # Starter Plan
        starter_plan = Plan(
            name="starter",
            display_name="Starter",
            description="Perfect for individual traders getting started",
            plan_type=PlanType.STARTER,
            status=PlanStatus.ACTIVE,
            monthly_price=49.0,
            annual_price=490.0,
            currency="USD",
            features=[
                "basic_trading",
                "technical_indicators",
                "data_export"
            ],
            limits={
                "api_calls": 10000,
                "storage": 1000,
                "users": 1,
                "strategies": 5,
                "backtests": 10
            },
            trial_days=14,
            support_level="standard",
            sla_uptime=99.5
        )
        plans["starter"] = starter_plan
        
        # Professional Plan
        professional_plan = Plan(
            name="professional",
            display_name="Professional",
            description="Advanced features for serious traders",
            plan_type=PlanType.PROFESSIONAL,
            status=PlanStatus.ACTIVE,
            monthly_price=199.0,
            annual_price=1990.0,
            currency="USD",
            features=[
                "basic_trading",
                "technical_indicators",
                "data_export",
                "live_trading",
                "advanced_indicators",
                "ml_models",
                "backtesting"
            ],
            limits={
                "api_calls": 100000,
                "storage": 10000,
                "users": 5,
                "strategies": 25,
                "backtests": 100
            },
            trial_days=14,
            support_level="priority",
            sla_uptime=99.9
        )
        plans["professional"] = professional_plan
        
        # Enterprise Plan
        enterprise_plan = Plan(
            name="enterprise",
            display_name="Enterprise",
            description="Full-featured solution for teams and organizations",
            plan_type=PlanType.ENTERPRISE,
            status=PlanStatus.ACTIVE,
            monthly_price=999.0,
            annual_price=9990.0,
            currency="USD",
            features=[
                "basic_trading",
                "technical_indicators",
                "data_export",
                "live_trading",
                "advanced_indicators",
                "ml_models",
                "backtesting",
                "api_access",
                "dedicated_support"
            ],
            limits={
                "api_calls": 1000000,
                "storage": 100000,
                "users": 50,
                "strategies": -1,  # unlimited
                "backtests": -1  # unlimited
            },
            trial_days=30,
            support_level="dedicated",
            sla_uptime=99.99,
            custom_pricing_available=True
        )
        plans["enterprise"] = enterprise_plan
        
        # Institutional Plan
        institutional_plan = Plan(
            name="institutional",
            display_name="Institutional",
            description="Custom solution for large institutions and hedge funds",
            plan_type=PlanType.INSTITUTIONAL,
            status=PlanStatus.ACTIVE,
            monthly_price=0.0,  # Custom pricing
            annual_price=0.0,  # Custom pricing
            currency="USD",
            features=[
                "basic_trading",
                "technical_indicators",
                "data_export",
                "live_trading",
                "advanced_indicators",
                "ml_models",
                "backtesting",
                "api_access",
                "white_label",
                "dedicated_support"
            ],
            limits={
                "api_calls": -1,  # unlimited
                "storage": -1,  # unlimited
                "users": -1,  # unlimited
                "strategies": -1,  # unlimited
                "backtests": -1  # unlimited
            },
            trial_days=60,
            support_level="dedicated",
            sla_uptime=99.99,
            custom_pricing_available=True,
            minimum_commitment="1 year"
        )
        plans["institutional"] = institutional_plan
        
        return plans
    
    async def start(self, host: str = '0.0.0.0', port: int = 8080):
        """Start the SaaS platform."""
        try:
            if not self.api:
                await self.initialize()
            
            self.running = True
            logger.info(f"Starting NeoZork SaaS Platform on {host}:{port}")
            
            # Start the API server
            await self.api.app.runner.setup()
            site = web.TCPSite(self.api.app.runner, host, port)
            await site.start()
            
            logger.info("NeoZork SaaS Platform started successfully")
            
            # Keep running until shutdown
            while self.running:
                await asyncio.sleep(1)
                
        except Exception as e:
            logger.error(f"Failed to start SaaS platform: {e}")
            raise
    
    async def stop(self):
        """Stop the SaaS platform gracefully."""
        try:
            logger.info("Stopping NeoZork SaaS Platform...")
            
            self.running = False
            
            if self.api and self.api.app.runner:
                await self.api.app.runner.cleanup()
            
            logger.info("NeoZork SaaS Platform stopped successfully")
            
        except Exception as e:
            logger.error(f"Error stopping SaaS platform: {e}")
    
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals."""
        logger.info(f"Received signal {signum}, initiating graceful shutdown...")
        asyncio.create_task(self.stop())


async def main():
    """Main entry point for the SaaS platform."""
    try:
        platform = NeoZorkSaaSPlatform()
        
        # Get configuration from environment or use defaults
        host = '0.0.0.0'
        port = 8080
        
        # Start the platform
        await platform.start(host=host, port=port)
        
    except KeyboardInterrupt:
        logger.info("Received keyboard interrupt, shutting down...")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    # Run the SaaS platform
    asyncio.run(main())
