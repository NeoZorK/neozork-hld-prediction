"""
NeoZork Pocket Hedge Fund - Revolutionary AI-Powered Fund

This module provides the core functionality for the Pocket Hedge Fund system,
including autonomous trading bots, blockchain integration, fund management,
and investor portal capabilities.

Key Components:
- Autonomous trading bot with self-learning capabilities
- Blockchain-native fund with smart contract automation
- Multi-tier fund management (Mini, Standard, Premium)
- AI Strategy Marketplace for strategy trading
- Community features and social trading
- Investor portal with real-time monitoring
"""

__version__ = "1.0.0"
__author__ = "NeoZork Team"

# Import core components
from .autonomous_bot import (
    SelfLearningEngine,
    AdaptiveStrategyManager,
    SelfMonitoringSystem,
    SelfRetrainingSystem
)

from .blockchain_integration import (
    MultiChainManager,
    TokenizationSystem,
    DAOGovernance
)

from .fund_management import (
    FundManager,
    PortfolioManager,
    PerformanceTracker,
    RiskAnalytics,
    ReportingSystem
)

from .investor_portal import (
    InvestorPortal,
    Dashboard,
    MonitoringSystem,
    ReportGenerator,
    CommunicationSystem
)

from .strategy_marketplace import (
    StrategyMarketplace,
    StrategySharing,
    LicensingSystem,
    RevenueSharing,
    MarketplaceAnalytics
)

from .community import (
    CommunityManager,
    SocialTrading,
    LeaderboardSystem,
    ForumSystem,
    GamificationSystem
)

from .api import (
    FundAPI,
    InvestorAPI,
    StrategyAPI,
    CommunityAPI
)

__all__ = [
    # Autonomous Bot
    "SelfLearningEngine",
    "AdaptiveStrategyManager", 
    "SelfMonitoringSystem",
    "SelfRetrainingSystem",
    
    # Blockchain Integration
    "MultiChainManager",
    "TokenizationSystem",
    "DAOGovernance",
    
    # Fund Management
    "FundManager",
    "PortfolioManager",
    "PerformanceTracker",
    "RiskAnalytics",
    "ReportingSystem",
    
    # Investor Portal
    "InvestorPortal",
    "Dashboard",
    "MonitoringSystem",
    "ReportGenerator",
    "CommunicationSystem",
    
    # Strategy Marketplace
    "StrategyMarketplace",
    "StrategySharing",
    "LicensingSystem",
    "RevenueSharing",
    "MarketplaceAnalytics",
    
    # Community
    "CommunityManager",
    "SocialTrading",
    "LeaderboardSystem",
    "ForumSystem",
    "GamificationSystem",
    
    # API
    "FundAPI",
    "InvestorAPI",
    "StrategyAPI",
    "CommunityAPI"
]
