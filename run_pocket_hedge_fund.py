#!/usr/bin/env python3
"""
Pocket Hedge Fund - Launch Script

This script provides an easy way to launch the Pocket Hedge Fund application
with proper configuration and environment setup.
"""

import asyncio
import logging
import os
import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.pocket_hedge_fund.main import main

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def setup_environment():
    """Setup environment variables and configuration."""
    # Set default environment variables
    os.environ.setdefault('HOST', '0.0.0.0')
    os.environ.setdefault('PORT', '8080')
    os.environ.setdefault('DEBUG', 'false')
    
    # Database configuration
    os.environ.setdefault('DB_HOST', 'localhost')
    os.environ.setdefault('DB_PORT', '5432')
    os.environ.setdefault('DB_NAME', 'neozork_fund')
    os.environ.setdefault('DB_USER', 'neozork_user')
    os.environ.setdefault('DB_PASSWORD', 'neozork_password')
    os.environ.setdefault('DB_POOL_SIZE', '10')
    os.environ.setdefault('DB_MAX_OVERFLOW', '20')
    
    # JWT configuration
    os.environ.setdefault('JWT_SECRET', 'your-secret-key-change-in-production')
    
    logger.info("Environment variables configured")


def print_startup_info():
    """Print startup information."""
    print("""
🚀 NeoZork Pocket Hedge Fund - Starting Up
==========================================

📊 Features:
- AI-powered hedge fund management
- Multi-tier fund support (Mini, Standard, Premium)
- Real-time portfolio tracking
- Advanced risk management
- Investor portal
- Strategy marketplace
- Community features

🔧 Configuration:
- Host: {host}
- Port: {port}
- Database: {db_host}:{db_port}/{db_name}
- Debug Mode: {debug}

📚 API Documentation:
- Swagger UI: http://{host}:{port}/docs
- ReDoc: http://{host}:{port}/redoc
- Health Check: http://{host}:{port}/health

🎯 Quick Start:
1. Register a user: POST /api/v1/auth/register
2. Login: POST /api/v1/auth/login
3. Create a fund: POST /api/v1/funds/
4. Invest in fund: POST /api/v1/funds/{{fund_id}}/invest

==========================================
    """.format(
        host=os.getenv('HOST', '0.0.0.0'),
        port=os.getenv('PORT', '8080'),
        db_host=os.getenv('DB_HOST', 'localhost'),
        db_port=os.getenv('DB_PORT', '5432'),
        db_name=os.getenv('DB_NAME', 'neozork_fund'),
        debug=os.getenv('DEBUG', 'false')
    ))


if __name__ == "__main__":
    try:
        # Setup environment
        setup_environment()
        
        # Print startup info
        print_startup_info()
        
        # Run the application
        asyncio.run(main())
        
    except KeyboardInterrupt:
        logger.info("Application interrupted by user")
        print("\n👋 Pocket Hedge Fund stopped by user")
    except Exception as e:
        logger.error(f"Application failed: {e}")
        print(f"\n❌ Pocket Hedge Fund failed to start: {e}")
        sys.exit(1)