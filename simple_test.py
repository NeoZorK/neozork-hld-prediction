#!/usr/bin/env python3
"""
Simple terminal plotting test to verify functionality.
"""

import sys
import os
import pandas as pd
import traceback

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_plotext_basic():
    """Test basic plotext functionality."""
    try:
        import plotext as plt
        print("✓ Plotext imported successfully")
        
        # Simple test plot
        plt.plot([1, 2, 3, 4], [1, 4, 2, 3])
        plt.title("Basic Test Plot")
        plt.xlabel("X axis")
        plt.ylabel("Y axis")
        plt.show()
        print("✓ Basic plotext plot displayed")
        return True
    except Exception as e:
        print(f"✗ Plotext basic test failed: {e}")
        traceback.print_exc()
        return False

def test_imports():
    """Test imports of our modules."""
    try:
        from common.constants import TradingRule
        print("✓ TradingRule imported")
        
        from common import logger
        print("✓ Logger imported")
        
        from plotting.term_plot import plot_indicator_results_term
        print("✓ Terminal plotting function imported")
        
        return True
    except Exception as e:
        print(f"✗ Import test failed: {e}")
        traceback.print_exc()
        return False

def test_data_loading():
    """Test loading sample data."""
    try:
        df = pd.read_csv('data/test_data.csv')
        print(f"✓ Loaded test data: {len(df)} rows, columns: {list(df.columns)}")
        return df
    except Exception as e:
        print(f"✗ Data loading failed: {e}")
        return None

def test_simple_terminal_plot():
    """Test simple terminal plotting with sample data."""
    try:
        # Import modules
        from plotting.term_plot import plot_indicator_results_term
        from common.constants import TradingRule
        
        # Load data
        df = pd.read_csv('data/test_data.csv')
        
        # Try a simple plot
        print("\nAttempting terminal plot...")
        result = plot_indicator_results_term(df, TradingRule.Predict_High_Low_Direction, "Simple Test Plot")
        print(f"✓ Terminal plot completed, result: {result}")
        return True
        
    except Exception as e:
        print(f"✗ Terminal plot test failed: {e}")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("SIMPLE TERMINAL PLOTTING TEST")
    print("=" * 60)
    
    # Test 1: Basic plotext
    print("\n1. Testing basic plotext functionality...")
    test_plotext_basic()
    
    # Test 2: Imports
    print("\n2. Testing module imports...")
    test_imports()
    
    # Test 3: Data loading
    print("\n3. Testing data loading...")
    test_data_loading()
    
    # Test 4: Simple terminal plot
    print("\n4. Testing simple terminal plot...")
    test_simple_terminal_plot()
    
    print("\n" + "=" * 60)
    print("TESTS COMPLETED")
    print("=" * 60)
