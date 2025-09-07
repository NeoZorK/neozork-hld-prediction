#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NeoZork SaaS Platform Launcher

This script launches the NeoZork SaaS platform with proper configuration
and environment setup.
"""

import os
import sys
import asyncio
import logging
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.saas.main import NeoZorkSaaSPlatform

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('logs/saas_platform.log')
    ]
)

logger = logging.getLogger(__name__)


def main():
    """Main entry point for the SaaS platform launcher."""
    try:
        logger.info("🚀 Starting NeoZork SaaS Platform...")
        
        # Get configuration from environment variables
        host = os.getenv('SAAS_HOST', '0.0.0.0')
        port = int(os.getenv('SAAS_PORT', '8080'))
        
        logger.info(f"Configuration:")
        logger.info(f"  Host: {host}")
        logger.info(f"  Port: {port}")
        logger.info(f"  Environment: {os.getenv('ENVIRONMENT', 'development')}")
        
        # Create and run the platform
        platform = NeoZorkSaaSPlatform()
        
        # Run the platform
        asyncio.run(platform.start(host=host, port=port))
        
    except KeyboardInterrupt:
        logger.info("Received keyboard interrupt, shutting down...")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
