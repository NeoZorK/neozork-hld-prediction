# -*- coding: utf-8 -*-
"""
Demo script for gaps analysis functionality.

This script demonstrates how to use the gaps analysis with different data structures.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../../'))

from src.interactive.eda_analysis.gaps_analysis import GapsAnalyzer


def create_sample_data_with_gaps():
    """Create sample data with gaps for testing."""
    # Create base time range
    base_dates = pd.date_range('2023-01-01', periods=100, freq='1h')
    
    # Remove some dates to create gaps
    indices_to_keep = [i for i in range(100) if i not in [10, 11, 12, 25, 26, 50, 51, 52, 53, 75, 76]]
    dates = base_dates[indices_to_keep]
    
    # Create sample OHLCV data
    data = pd.DataFrame({
        'Open': 100 + np.cumsum(np.random.randn(len(dates)) * 0.1),
        'High': 101 + np.cumsum(np.random.randn(len(dates)) * 0.1),
        'Low': 99 + np.cumsum(np.random.randn(len(dates)) * 0.1),
        'Close': 100.5 + np.cumsum(np.random.randn(len(dates)) * 0.1),
        'Volume': np.random.randint(1000, 10000, len(dates))
    }, index=dates)
    
    return data


def test_standard_structure():
    """Test with standard MTF structure."""
    print("🔍 Testing Standard MTF Structure")
    print("=" * 50)
    
    # Create sample data
    h1_data = create_sample_data_with_gaps()
    d1_data = h1_data.resample('D').first()
    
    # Standard structure
    mtf_data = {
        'loaded_data': {
            'H1': h1_data,
            'D1': d1_data
        },
        'symbol': 'BTCUSD',
        'metadata': {'source': 'demo'}
    }
    
    # Initialize analyzer
    analyzer = GapsAnalyzer()
    
    # Analyze gaps
    result = analyzer.analyze_and_fix_gaps(
        mtf_data=mtf_data,
        symbol='BTCUSD',
        strategy='auto',
        create_backup=True
    )
    
    print(f"Status: {result['status']}")
    if result['status'] == 'success':
        print(f"Strategy used: {result['strategy_used']}")
        print(f"Timeframes processed: {len(result['gaps_analysis']['timeframe_gaps'])}")
        for tf, gaps_info in result['gaps_analysis']['timeframe_gaps'].items():
            print(f"  {tf}: {gaps_info['gap_count']} gaps found")
    else:
        print(f"Error: {result.get('message', 'Unknown error')}")
    
    print()


def test_direct_structure():
    """Test with direct timeframe structure."""
    print("🔍 Testing Direct Timeframe Structure")
    print("=" * 50)
    
    # Create sample data
    h1_data = create_sample_data_with_gaps()
    d1_data = h1_data.resample('D').first()
    
    # Direct structure (no loaded_data wrapper)
    mtf_data = {
        'H1': h1_data,
        'D1': d1_data,
        'symbol': 'BTCUSD',
        'metadata': {'source': 'demo'}
    }
    
    # Initialize analyzer
    analyzer = GapsAnalyzer()
    
    # Debug: Print data structure
    print(f"Data structure keys: {list(mtf_data.keys())}")
    print(f"H1 data type: {type(mtf_data['H1'])}")
    print(f"D1 data type: {type(mtf_data['D1'])}")
    
    # Analyze gaps
    result = analyzer.analyze_and_fix_gaps(
        mtf_data=mtf_data,
        symbol='BTCUSD',
        strategy='auto',
        create_backup=True
    )
    
    print(f"Status: {result['status']}")
    if result['status'] == 'success':
        print(f"Strategy used: {result['strategy_used']}")
        print(f"Timeframes processed: {len(result['gaps_analysis']['timeframe_gaps'])}")
        for tf, gaps_info in result['gaps_analysis']['timeframe_gaps'].items():
            print(f"  {tf}: {gaps_info['gap_count']} gaps found")
    else:
        print(f"Error: {result.get('message', 'Unknown error')}")
    
    print()


def test_auto_strategy_selection():
    """Test automatic strategy selection."""
    print("🤖 Testing Auto Strategy Selection")
    print("=" * 50)
    
    # Create different types of data to test strategy selection
    test_cases = [
        {
            'name': 'Trending Data',
            'data': create_trending_data(),
            'expected_strategy': 'linear_interpolation'
        },
        {
            'name': 'Volatile Data',
            'data': create_volatile_data(),
            'expected_strategy': 'spline_interpolation'
        },
        {
            'name': 'Stationary Data',
            'data': create_stationary_data(),
            'expected_strategy': 'mean_fill'
        }
    ]
    
    analyzer = GapsAnalyzer()
    
    for case in test_cases:
        print(f"Testing {case['name']}...")
        
        mtf_data = {'H1': case['data']}
        
        # Debug: Print data structure
        print(f"  Data type: {type(mtf_data['H1'])}")
        print(f"  Data shape: {mtf_data['H1'].shape}")
        
        result = analyzer.analyze_and_fix_gaps(
            mtf_data=mtf_data,
            symbol='TEST',
            strategy='auto',
            create_backup=False
        )
        
        if result['status'] == 'success':
            print(f"  ✅ Selected strategy: {result['strategy_used']}")
        else:
            print(f"  ❌ Error: {result.get('message', 'Unknown error')}")
    
    print()


def create_trending_data():
    """Create trending data for testing."""
    dates = pd.date_range('2023-01-01', periods=50, freq='1h')
    # Remove some dates to create gaps
    indices_to_keep = [i for i in range(50) if i not in [10, 11, 25, 26]]
    dates = dates[indices_to_keep]
    
    # Create trending data
    trend = np.linspace(100, 150, len(dates))
    noise = np.random.randn(len(dates)) * 0.5
    
    return pd.DataFrame({
        'Open': trend + noise,
        'High': trend + noise + 1,
        'Low': trend + noise - 1,
        'Close': trend + noise + 0.5,
        'Volume': np.random.randint(1000, 5000, len(dates))
    }, index=dates)


def create_volatile_data():
    """Create volatile data for testing."""
    dates = pd.date_range('2023-01-01', periods=30, freq='1h')
    # Remove some dates to create gaps
    indices_to_keep = [i for i in range(30) if i not in [5, 6, 15, 16]]
    dates = dates[indices_to_keep]
    
    # Create volatile data
    base_price = 100
    returns = np.random.randn(len(dates)) * 0.05  # 5% volatility
    prices = base_price * np.exp(np.cumsum(returns))
    
    return pd.DataFrame({
        'Open': prices,
        'High': prices * (1 + np.abs(np.random.randn(len(dates)) * 0.01)),
        'Low': prices * (1 - np.abs(np.random.randn(len(dates)) * 0.01)),
        'Close': prices * (1 + np.random.randn(len(dates)) * 0.005),
        'Volume': np.random.randint(2000, 8000, len(dates))
    }, index=dates)


def create_stationary_data():
    """Create stationary data for testing."""
    dates = pd.date_range('2023-01-01', periods=40, freq='1h')
    # Remove some dates to create gaps
    indices_to_keep = [i for i in range(40) if i not in [8, 9, 20, 21, 22]]
    dates = dates[indices_to_keep]
    
    # Create stationary data around 100
    base_price = 100
    noise = np.random.randn(len(dates)) * 0.1
    
    return pd.DataFrame({
        'Open': base_price + noise,
        'High': base_price + noise + 0.5,
        'Low': base_price + noise - 0.5,
        'Close': base_price + noise + 0.2,
        'Volume': np.random.randint(1500, 3000, len(dates))
    }, index=dates)


if __name__ == '__main__':
    print("🚀 Gaps Analysis Demo")
    print("=" * 60)
    print()
    
    test_standard_structure()
    test_direct_structure()
    test_auto_strategy_selection()
    
    print("✅ Demo completed successfully!")
