#!/usr/bin/env python3
"""
Direct test for terminal plotting functionality
"""

import sys
import os
import pandas as pd

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Direct import and test
print("Testing terminal plotting...")

try:
    import plotext as plt
    print("✓ plotext imported")
    
    # Test basic plot
    plt.clear_data()
    plt.plot([1, 2, 3], [1, 4, 2])
    plt.title("Basic Test")
    plt.show()
    print("✓ Basic plotext working")
    
    # Test our modules
    from common.constants import TradingRule
    from plotting.term_plot import plot_indicator_results_term
    print("✓ Modules imported")
    
    # Load test data
    df = pd.read_csv('data/test_data.csv')
    print(f"✓ Data loaded: {len(df)} rows")
    
    # Test terminal plotting
    print("\n" + "="*60)
    print("TESTING TERMINAL PLOT")
    print("="*60)
    
    result = plot_indicator_results_term(df, TradingRule.Predict_High_Low_Direction, "Test Terminal Plot")
    
    print("\n✓ Terminal plot test completed successfully!")
    
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()
