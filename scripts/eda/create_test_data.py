#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Create Test Data Script

This script creates sample OHLCV data for testing the integrated EDA and Feature Engineering system.
"""

import pandas as pd
import numpy as np
from pathlib import Path

def create_sample_ohlcv_data(n_rows=1000):
    """Create sample OHLCV data for testing."""
    
    # Set random seed for reproducibility
    np.random.seed(42)
    
    # Create date range
    dates = pd.date_range('2023-01-01', periods=n_rows, freq='1H')
    
    # Generate realistic price data
    base_price = 100.0
    returns = np.random.normal(0, 0.02, n_rows)  # 2% daily volatility
    
    # Calculate prices
    prices = [base_price]
    for ret in returns[1:]:
        new_price = prices[-1] * (1 + ret)
        prices.append(new_price)
    
    # Create OHLCV data
    data = []
    for i, (date, price) in enumerate(zip(dates, prices)):
        # Generate realistic OHLC from close price
        volatility = np.random.uniform(0.005, 0.02)  # 0.5% to 2% intraday volatility
        
        # Open price (close from previous period with some noise)
        if i == 0:
            open_price = price * (1 + np.random.uniform(-0.01, 0.01))
        else:
            open_price = data[i-1]['Close'] * (1 + np.random.uniform(-0.005, 0.005))
        
        # High and Low prices
        high_price = max(open_price, price) * (1 + np.random.uniform(0, volatility))
        low_price = min(open_price, price) * (1 - np.random.uniform(0, volatility))
        
        # Volume (correlated with price movement)
        base_volume = 1000000  # 1M base volume
        volume = base_volume * (1 + abs(returns[i]) * 10 + np.random.uniform(-0.2, 0.2))
        
        data.append({
            'Date': date,
            'Open': round(open_price, 4),
            'High': round(high_price, 4),
            'Low': round(low_price, 4),
            'Close': round(price, 4),
            'Volume': int(volume)
        })
    
    return pd.DataFrame(data)

def create_multiple_test_files():
    """Create multiple test files for different scenarios."""
    
    # Create data directory
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    
    # 1. Standard OHLCV data (1000 rows)
    print("Creating standard OHLCV data...")
    df_standard = create_sample_ohlcv_data(1000)
    df_standard.to_csv(data_dir / "sample_ohlcv_1000.csv", index=False)
    print(f"✅ Created: {data_dir / 'sample_ohlcv_1000.csv'}")
    
    # 2. Large dataset (2000 rows)
    print("Creating large dataset...")
    df_large = create_sample_ohlcv_data(2000)
    df_large.to_csv(data_dir / "sample_ohlcv_2000.csv", index=False)
    print(f"✅ Created: {data_dir / 'sample_ohlcv_2000.csv'}")
    
    # 3. Small dataset (300 rows) - for testing padding
    print("Creating small dataset...")
    df_small = create_sample_ohlcv_data(300)
    df_small.to_csv(data_dir / "sample_ohlcv_300.csv", index=False)
    print(f"✅ Created: {data_dir / 'sample_ohlcv_300.csv'}")
    
    # 4. Data with some issues (for testing EDA)
    print("Creating dataset with issues...")
    df_issues = create_sample_ohlcv_data(800)
    
    # Add some missing values
    df_issues.loc[100:105, 'Volume'] = np.nan
    df_issues.loc[200:202, 'High'] = np.nan
    
    # Add some duplicates
    df_issues = pd.concat([df_issues, df_issues.iloc[50:55]], ignore_index=True)
    
    # Add some outliers
    df_issues.loc[400, 'Close'] = df_issues.loc[400, 'Close'] * 10  # 10x price spike
    df_issues.loc[500, 'Volume'] = df_issues.loc[500, 'Volume'] * 100  # 100x volume spike
    
    df_issues.to_csv(data_dir / "sample_ohlcv_with_issues.csv", index=False)
    print(f"✅ Created: {data_dir / 'sample_ohlcv_with_issues.csv'}")
    
    # 5. Export to Parquet format as well
    print("Creating Parquet versions...")
    df_standard.to_parquet(data_dir / "sample_ohlcv_1000.parquet")
    df_large.to_parquet(data_dir / "sample_ohlcv_2000.parquet")
    print(f"✅ Created Parquet versions")
    
    print(f"\n🎉 All test files created in {data_dir}/")
    print("\nAvailable test files:")
    for file in data_dir.glob("*.csv"):
        df = pd.read_csv(file)
        print(f"  📁 {file.name}: {df.shape[0]} rows × {df.shape[1]} columns")
    
    print("\n💡 Usage examples:")
    print("  # Test with standard data")
    print("  ./eda_fe --file data/sample_ohlcv_1000.csv --full-pipeline")
    print("\n  # Test with data issues")
    print("  ./eda_fe --file data/sample_ohlcv_with_issues.csv --full-pipeline")
    print("\n  # Test with small dataset (will be padded)")
    print("  ./eda_fe --file data/sample_ohlcv_300.csv --full-pipeline")

if __name__ == "__main__":
    create_multiple_test_files()
