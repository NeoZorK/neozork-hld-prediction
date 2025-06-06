#!/usr/bin/env python3
"""
Test script for terminal plotting functionality.
This script tests the implemented terminal plotting features with sample data.
"""

import sys
import os
import pandas as pd

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.plotting.plotting import plot_indicator_results
from src.common.constants import TradingRule
from src.common import logger

def test_terminal_plotting():
    """Test terminal plotting with sample data."""
    
    print("=" * 80)
    print("TESTING TERMINAL PLOTTING FUNCTIONALITY")
    print("=" * 80)
    
    # Test 1: Load and test with test_data.csv
    try:
        print("\n1. Testing with test_data.csv...")
        df_test = pd.read_csv('data/test_data.csv')
        print(f"   Loaded {len(df_test)} rows of test data")
        print(f"   Columns: {list(df_test.columns)}")
        
        # Test PHLD mode
        print("\n   Testing PHLD mode...")
        result = plot_indicator_results(
            df_test, 
            TradingRule.Predict_High_Low_Direction, 
            title="Test Data - PHLD Terminal Plot", 
            mode="term"
        )
        print(f"   PHLD plot result: {result}")
        
        # Test AUTO mode
        print("\n   Testing AUTO mode...")
        result = plot_indicator_results(
            df_test, 
            TradingRule.AUTO,
            title="Test Data - AUTO Terminal Plot", 
            mode="term"
        )
        print(f"   AUTO plot result: {result}")
        
        # Test PV mode
        print("\n   Testing PV mode...")
        result = plot_indicator_results(
            df_test, 
            TradingRule.Pressure_Vector, 
            title="Test Data - PV Terminal Plot", 
            mode="term"
        )
        print(f"   PV plot result: {result}")
        
    except Exception as e:
        print(f"   ERROR with test_data.csv: {e}")
    
    # Test 2: Load and test with mn1.csv
    try:
        print("\n2. Testing with mn1.csv...")
        df_mn1 = pd.read_csv('data/mn1.csv')
        print(f"   Loaded {len(df_mn1)} rows of MN1 data")
        print(f"   Columns: {list(df_mn1.columns)}")
        
        # Test PHLD mode with datetime index
        print("\n   Testing PHLD mode with datetime data...")
        if 'Date' in df_mn1.columns:
            df_mn1['Date'] = pd.to_datetime(df_mn1['Date'])
            df_mn1.set_index('Date', inplace=True)
        
        result = plot_indicator_results(
            df_mn1, 
            TradingRule.Predict_High_Low_Direction, 
            title="MN1 Data - PHLD Terminal Plot", 
            mode="term"
        )
        print(f"   PHLD plot result: {result}")
        
    except Exception as e:
        print(f"   ERROR with mn1.csv: {e}")
    
    # Test 3: Test Docker detection override
    try:
        print("\n3. Testing Docker detection and mode switching...")
        
        # Temporarily set Docker environment
        os.environ['DOCKER_CONTAINER'] = 'true'
        
        print("   Testing auto-switch to terminal mode in Docker...")
        result = plot_indicator_results(
            df_test, 
            TradingRule.Predict_High_Low_Direction, 
            title="Docker Test - Auto Terminal Plot", 
            mode="plotly"  # Should be overridden to 'term'
        )
        print(f"   Docker auto-switch result: {result}")
        
        # Test with Docker detection disabled
        os.environ['DISABLE_DOCKER_DETECTION'] = 'true'
        print("   Testing with Docker detection disabled...")
        result = plot_indicator_results(
            df_test, 
            TradingRule.Predict_High_Low_Direction, 
            title="Docker Disabled Test", 
            mode="term"  # Should still work
        )
        print(f"   Docker disabled result: {result}")
        
        # Clean up environment
        del os.environ['DOCKER_CONTAINER']
        del os.environ['DISABLE_DOCKER_DETECTION']
        
    except Exception as e:
        print(f"   ERROR with Docker detection test: {e}")
    
    # Test 4: Test error handling
    try:
        print("\n4. Testing error handling...")
        
        # Test with missing required columns
        df_bad = pd.DataFrame({
            'Date': ['2024-01-01', '2024-01-02'],
            'Price': [100, 102]  # Missing OHLC columns
        })
        
        result = plot_indicator_results(
            df_bad, 
            TradingRule.Predict_High_Low_Direction, 
            title="Error Test - Missing OHLC", 
            mode="term"
        )
        print(f"   Error handling result: {result}")
        
    except Exception as e:
        print(f"   ERROR handling test: {e}")
    
    print("\n" + "=" * 80)
    print("TERMINAL PLOTTING TESTS COMPLETED")
    print("=" * 80)

def test_individual_plotting_functions():
    """Test individual terminal plotting functions directly."""
    
    print("\n" + "=" * 80)
    print("TESTING INDIVIDUAL TERMINAL PLOTTING FUNCTIONS")
    print("=" * 80)
    
    try:
        # Load test data
        df_test = pd.read_csv('data/test_data.csv')
        
        # Test term_plot directly
        print("\n1. Testing term_plot.py directly...")
        from src.plotting.term_plot import plot_indicator_results_term
        result = plot_indicator_results_term(df_test, TradingRule.Predict_High_Low_Direction, "Direct Term Plot Test")
        print(f"   Direct term_plot result: {result}")
        
        # Test term_auto_plot directly
        print("\n2. Testing term_auto_plot.py directly...")
        from src.plotting.term_auto_plot import auto_plot_from_dataframe
        result = auto_plot_from_dataframe(df_test, "Direct Auto Plot Test")
        print(f"   Direct auto_plot result: {result}")
        
        # Test term_phld_plot directly
        print("\n3. Testing term_phld_plot.py directly...")
        from src.plotting.term_phld_plot import plot_phld_indicator_terminal
        result = plot_phld_indicator_terminal(df_test, TradingRule.Predict_High_Low_Direction, "Direct PHLD Plot Test")
        print(f"   Direct PHLD_plot result: {result}")
        
    except Exception as e:
        print(f"   ERROR in individual function tests: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    # Set up logging
    logger.print_info("Starting terminal plotting tests...")
    
    # Run tests
    test_terminal_plotting()
    test_individual_plotting_functions()
    
    print("\nAll tests completed!")
