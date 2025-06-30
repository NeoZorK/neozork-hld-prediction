"""
Debug script for Polygon API connection and data fetching.

This script tests the Polygon API connection and fetches sample data
to verify that the API is working correctly.
"""

import os
import sys
import asyncio
from pathlib import Path

# Add the src directory to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from data.fetchers.polygon_fetcher import PolygonFetcher


def test_polygon_connection():
    """Test Polygon API connection."""
    print("Testing Polygon API connection...")
    
    # Check if API key is available
    api_key = os.environ.get('POLYGON_API_KEY')
    
    if not api_key:
        print("❌ POLYGON_API_KEY not found in environment variables")
        print("Please set this environment variable to test Polygon API")
        return False
    
    try:
        # Create Polygon fetcher instance
        fetcher = PolygonFetcher()
        
        # Test connection
        print("✅ Polygon fetcher created successfully")
        
        # Test fetching recent data
        print("Fetching recent AAPL data...")
        data = fetcher.fetch_recent_data("AAPL", "1", "day", limit=10)
        
        if data is not None and len(data) > 0:
            print(f"✅ Successfully fetched {len(data)} records from Polygon")
            print(f"Latest data: {data.iloc[-1]}")
            return True
        else:
            print("❌ Failed to fetch data from Polygon")
            return False
            
    except Exception as e:
        print(f"❌ Error testing Polygon connection: {e}")
        return False


def main():
    """Main function to run Polygon debug tests."""
    print("=" * 50)
    print("POLYGON API DEBUG TEST")
    print("=" * 50)
    
    success = test_polygon_connection()
    
    if success:
        print("\n✅ All Polygon tests passed!")
        return 0
    else:
        print("\n❌ Some Polygon tests failed!")
        return 1


if __name__ == "__main__":
    exit(main()) 