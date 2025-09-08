#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pocket Hedge Fund Launcher

This script launches the NeoZork Pocket Hedge Fund system.
"""

import asyncio
import logging
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from pocket_hedge_fund import PocketHedgeFund

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/pocket_hedge_fund.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


async def main():
    """Main function to launch Pocket Hedge Fund."""
    try:
        logger.info("🚀 Starting NeoZork Pocket Hedge Fund...")
        
        # Fund configuration
        fund_config = {
            'fund_id': 'pocket_hedge_fund_001',
            'fund_name': 'NeoZork Pocket Hedge Fund',
            'initial_capital': 100000,  # $100k initial capital
            'blockchain_configs': [
                {
                    'chain_type': 'ethereum',
                    'rpc_url': 'https://mainnet.infura.io/v3/YOUR_KEY',
                    'chain_id': 1,
                    'enabled': True
                },
                {
                    'chain_type': 'polygon',
                    'rpc_url': 'https://polygon-rpc.com',
                    'chain_id': 137,
                    'enabled': True
                }
            ]
        }
        
        # Initialize Pocket Hedge Fund
        fund = PocketHedgeFund(fund_config)
        
        # Start autonomous trading
        start_result = await fund.start_autonomous_trading()
        logger.info(f"Fund started: {start_result}")
        
        # Get initial status
        status = await fund.get_fund_status()
        logger.info(f"Fund status: {status}")
        
        # Run trading cycle (example)
        logger.info("Running trading cycle...")
        cycle_result = await fund.execute_trading_cycle()
        logger.info(f"Trading cycle result: {cycle_result}")
        
        # Keep running (in production, this would be a continuous loop)
        logger.info("✅ Pocket Hedge Fund is running successfully!")
        logger.info("Press Ctrl+C to stop...")
        
        # Keep the system running
        while True:
            await asyncio.sleep(60)  # Check every minute
            
            # Process market data (placeholder)
            market_data = {
                'timestamp': asyncio.get_event_loop().time(),
                'price': 100.0,
                'volume': 1000,
                'volatility': 0.02
            }
            
            processing_result = await fund.process_market_data(market_data)
            logger.info(f"Market data processed: {processing_result}")
            
    except KeyboardInterrupt:
        logger.info("🛑 Stopping Pocket Hedge Fund...")
        
        # Stop autonomous trading
        if 'fund' in locals():
            stop_result = await fund.stop_autonomous_trading()
            logger.info(f"Fund stopped: {stop_result}")
        
        logger.info("✅ Pocket Hedge Fund stopped successfully!")
        
    except Exception as e:
        logger.error(f"❌ Pocket Hedge Fund failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    # Create logs directory if it doesn't exist
    Path("logs").mkdir(exist_ok=True)
    
    # Run the main function
    asyncio.run(main())
