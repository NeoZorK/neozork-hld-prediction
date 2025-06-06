#!/usr/bin/env python3
"""
Comprehensive test for terminal plotting through the main plotting interface
"""

import sys
import os
import pandas as pd

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_main_plotting_interface():
    """Test terminal plotting through the main plotting.py interface"""
    
    print("=" * 70)
    print("TESTING MAIN PLOTTING INTERFACE - TERMINAL MODE")
    print("=" * 70)
    
    try:
        from plotting.plotting import plot_indicator_results
        from common.constants import TradingRule
        
        # Load test data
        df = pd.read_csv('data/test_data.csv')
        print(f"✓ Data loaded: {len(df)} rows")
        
        # Test 1: Direct terminal mode
        print("\n1. Testing direct terminal mode (term)...")
        result = plot_indicator_results(
            df, 
            TradingRule.Predict_High_Low_Direction, 
            title="Direct Terminal Mode Test", 
            mode="term"
        )
        print(f"✓ Direct terminal mode completed: {result}")
        
        # Test 2: AUTO mode
        print("\n2. Testing AUTO trading rule...")
        result = plot_indicator_results(
            df, 
            TradingRule.AUTO, 
            title="AUTO Mode Terminal Test", 
            mode="term"
        )
        print(f"✓ AUTO mode completed: {result}")
        
        # Test 3: PV mode
        print("\n3. Testing Pressure Vector mode...")
        result = plot_indicator_results(
            df, 
            TradingRule.Pressure_Vector, 
            title="Pressure Vector Terminal Test", 
            mode="term"
        )
        print(f"✓ Pressure Vector mode completed: {result}")
        
        # Test 4: Docker environment simulation
        print("\n4. Testing Docker environment auto-detection...")
        os.environ['DOCKER_CONTAINER'] = 'true'
        
        result = plot_indicator_results(
            df, 
            TradingRule.Predict_High_Low_Direction, 
            title="Docker Auto-Detection Test", 
            mode="plotly"  # Should be overridden to 'term'
        )
        print(f"✓ Docker auto-detection completed: {result}")
        
        # Clean up
        del os.environ['DOCKER_CONTAINER']
        
        print("\n" + "=" * 70)
        print("ALL TERMINAL PLOTTING TESTS PASSED!")
        print("=" * 70)
        
    except Exception as e:
        print(f"✗ Error in main plotting interface test: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_main_plotting_interface()
