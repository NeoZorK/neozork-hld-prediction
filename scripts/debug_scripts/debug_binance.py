"""
Debug script for Binance API connection and data fetching.

This script tests the Binance API connection and fetches sample data
to verify that the API is working correctly.
"""

import os
import sys
import asyncio
from pathlib import Path

# Add the src directory to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from data.fetchers.binance_fetcher import BinanceFetcher


def test_binance_connection():
    """Test Binance API connection."""
    print("Testing Binance API connection...")
    
    # Check if API keys are available
    api_key = os.environ.get('BINANCE_API_KEY')
    api_secret = os.environ.get('BINANCE_API_SECRET')
    
    if not api_key or not api_secret:
        print("❌ BINANCE_API_KEY and/or BINANCE_API_SECRET not found in environment variables")
        print("Please set these environment variables to test Binance API")
        return False
    
    try:
        # Create Binance fetcher instance
        fetcher = BinanceFetcher()
        
        # Test connection
        print("✅ Binance fetcher created successfully")
        
        # Test fetching recent data
        print("Fetching recent BTCUSDT data...")
        data = fetcher.fetch_recent_data("BTCUSDT", "1h", limit=10)
        
        if data is not None and len(data) > 0:
            print(f"✅ Successfully fetched {len(data)} records from Binance")
            print(f"Latest data: {data.iloc[-1]}")
            return True
        else:
            print("❌ Failed to fetch data from Binance")
            return False
            
    except Exception as e:
        print(f"❌ Error testing Binance connection: {e}")
        return False


def main():
    """Main function to run Binance debug tests."""
    print("=" * 50)
    print("BINANCE API DEBUG TEST")
    print("=" * 50)
    
    success = test_binance_connection()
    
    if success:
        print("\n✅ All Binance tests passed!")
        return 0
    else:
        print("\n❌ Some Binance tests failed!")
        return 1


if __name__ == "__main__":
    exit(main()) 