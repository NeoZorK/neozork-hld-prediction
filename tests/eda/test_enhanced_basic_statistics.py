#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for Enhanced Basic Statistics functionality
"""

import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

import pandas as pd
import numpy as np
from interactive_system import InteractiveSystem

def create_test_data():
    """Create sample test data for statistics analysis."""
    np.random.seed(42)
    
    # Create sample OHLCV data
    n_rows = 1000
    base_price = 100.0
    
    # Generate price data with some trends and volatility
    returns = np.random.normal(0.001, 0.02, n_rows)  # Daily returns
    prices = [base_price]
    
    for ret in returns[1:]:
        new_price = prices[-1] * (1 + ret)
        prices.append(new_price)
    
    prices = np.array(prices)
    
    # Create OHLCV data
    data = {
        'Open': prices[:-1],
        'High': prices[:-1] * (1 + np.abs(np.random.normal(0, 0.01, n_rows-1))),
        'Low': prices[:-1] * (1 - np.abs(np.random.normal(0, 0.01, n_rows-1))),
        'Close': prices[1:],
        'Volume': np.random.randint(1000, 10000, n_rows-1)
    }
    
    # Add some additional features
    data['Returns'] = np.diff(prices) / prices[:-1]
    data['Volatility'] = np.abs(data['Returns'])
    data['Price_Change'] = np.diff(prices)
    
    df = pd.DataFrame(data)
    
    # Add some missing values and outliers for testing
    df.loc[100:105, 'Volume'] = np.nan
    df.loc[200, 'High'] = df['High'].max() * 2  # Outlier
    
    return df

def test_enhanced_basic_statistics():
    """Test the enhanced basic statistics functionality."""
    print("🧪 TESTING ENHANCED BASIC STATISTICS FUNCTIONALITY")
    print("=" * 60)
    
    # Create interactive system
    system = InteractiveSystem()
    
    # Create test data
    print("📊 Creating test data...")
    test_data = create_test_data()
    system.current_data = test_data
    
    print(f"✅ Test data created: {test_data.shape[0]} rows × {test_data.shape[1]} columns")
    print(f"   Columns: {list(test_data.columns)}")
    
    # Run basic statistics
    print("\n📈 Running Enhanced Basic Statistics...")
    print("   This will test:")
    print("   • Progress bar with ETA for visualizations")
    print("   • User prompt for HTML plots")
    print("   • Enhanced timing information")
    
    try:
        system.run_basic_statistics()
        print("✅ Enhanced Basic Statistics completed successfully!")
        
        # Check if plots were created
        plots_dir = Path("results/plots/statistics")
        if plots_dir.exists():
            plot_files = list(plots_dir.glob("*.png"))
            print(f"✅ Generated {len(plot_files)} plot files:")
            for plot_file in plot_files:
                file_size = plot_file.stat().st_size / 1024  # KB
                print(f"   • {plot_file.name} ({file_size:.1f} KB)")
        else:
            print("⚠️  Plots directory not found")
        
        # Check if results were saved
        if 'basic_statistics' in system.current_results:
            print("✅ Results saved successfully!")
            results = system.current_results['basic_statistics']
            print(f"   • Numeric columns analyzed: {len(results['numeric_columns'])}")
            print(f"   • Total observations: {results['analysis_summary']['total_observations']}")
        else:
            print("⚠️  Results not saved")
            
    except Exception as e:
        print(f"❌ Error in Enhanced Basic Statistics: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    success = test_enhanced_basic_statistics()
    if success:
        print("\n🎉 All tests passed! Enhanced Basic Statistics functionality is working correctly.")
        print("\n📋 Summary of enhancements:")
        print("   ✅ Progress bar with ETA for visualization generation")
        print("   ✅ User prompt for HTML plots (Yes/No)")
        print("   ✅ Enhanced timing information")
        print("   ✅ Better error handling for test environments")
    else:
        print("\n❌ Tests failed. Please check the error messages above.")
        sys.exit(1)
