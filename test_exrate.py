#!/usr/bin/env python3
"""
Simple test script to check Exchange Rate API connectivity.
"""

import os
import sys
from dotenv import load_dotenv

sys.path.append('/workspaces/neozork-hld-prediction')

# Load environment variables
load_dotenv()

from src.data.fetchers.exrate_current_fetcher import fetch_exrate_current_data

def test_exrate_current():
    """Test current exchange rate fetching."""
    print("Testing Exchange Rate API current data fetching...")
    
    # Test current rate fetching
    df, metrics = fetch_exrate_current_data("EURUSD", "D1")
    
    if df is not None and not df.empty:
        print("✅ SUCCESS: Current rate fetching works!")
        print(f"Data shape: {df.shape}")
        print(f"Columns: {list(df.columns)}")
        print(f"Current EUR/USD rate: {df.iloc[0]['Close']}")
        print(f"API calls: {metrics['api_calls']}")
        print(f"Latency: {metrics['latency_sec']:.2f}s")
        return True
    else:
        print("❌ FAILED: Current rate fetching failed")
        print(f"Error: {metrics.get('error_message', 'Unknown error')}")
        return False

if __name__ == "__main__":
    success = test_exrate_current()
    sys.exit(0 if success else 1)
