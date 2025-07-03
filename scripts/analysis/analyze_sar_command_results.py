#!/usr/bin/env python3
"""
Analysis script for SAR command results:
uv run run_analysis.py show csv mn1 -d fastest --rule sar:0.000002,0.00005

This script analyzes the SAR indicator performance and signal generation.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from calculation.indicators.trend.sar_ind import calculate_sar, calculate_sar_signals, apply_rule_sar
from common.constants import BUY, SELL, NOTRADE


def load_mn1_data():
    """Load the mn1.csv data file."""
    data_path = Path("data/mn1.csv")
    if not data_path.exists():
        print(f"Error: {data_path} not found")
        return None
    
    df = pd.read_csv(data_path)
    df['DateTime'] = pd.to_datetime(df['Date'])
    df = df.set_index('DateTime')
    return df


def analyze_sar_performance(df, acceleration=0.000002, maximum=0.00005):
    """Analyze SAR indicator performance."""
    print("=== SAR INDICATOR ANALYSIS ===")
    print(f"Parameters: acceleration={acceleration}, maximum={maximum}")
    print(f"Data points: {len(df)}")
    print()
    
    # Calculate SAR
    sar_values = calculate_sar(df, acceleration, maximum)
    
    # Calculate signals
    signals = calculate_sar_signals(df['Close'], sar_values)
    
    # Analyze signals
    signal_counts = signals.value_counts()
    buy_signals = signal_counts.get(BUY, 0)
    sell_signals = signal_counts.get(SELL, 0)
    no_trade = signal_counts.get(NOTRADE, 0)
    
    print("=== SIGNAL ANALYSIS ===")
    print(f"Buy signals: {buy_signals}")
    print(f"Sell signals: {sell_signals}")
    print(f"No trade signals: {no_trade}")
    print(f"Total signals: {buy_signals + sell_signals}")
    print(f"Signal ratio (buy/sell): {buy_signals/sell_signals if sell_signals > 0 else 'N/A'}")
    print()
    
    # Analyze SAR values
    print("=== SAR VALUES ANALYSIS ===")
    print(f"SAR min: {sar_values.min():.6f}")
    print(f"SAR max: {sar_values.max():.6f}")
    print(f"SAR mean: {sar_values.mean():.6f}")
    print(f"SAR std: {sar_values.std():.6f}")
    print()
    
    # Analyze price vs SAR relationship
    price_above_sar = (df['Close'] > sar_values).sum()
    price_below_sar = (df['Close'] < sar_values).sum()
    price_equal_sar = (df['Close'] == sar_values).sum()
    
    print("=== PRICE vs SAR ANALYSIS ===")
    print(f"Price above SAR: {price_above_sar} ({price_above_sar/len(df)*100:.1f}%)")
    print(f"Price below SAR: {price_below_sar} ({price_below_sar/len(df)*100:.1f}%)")
    print(f"Price equal SAR: {price_equal_sar} ({price_equal_sar/len(df)*100:.1f}%)")
    print()
    
    return sar_values, signals


def analyze_signal_timing(df, signals, sar_values):
    """Analyze signal timing and effectiveness."""
    print("=== SIGNAL TIMING ANALYSIS ===")
    
    # Find signal points
    buy_points = signals[signals == BUY].index
    sell_points = signals[signals == SELL].index
    
    print(f"Buy signal points: {len(buy_points)}")
    print(f"Sell signal points: {len(sell_points)}")
    
    if len(buy_points) > 0:
        print("\nBuy signal analysis:")
        for i, point in enumerate(buy_points[:5]):  # Show first 5
            price = df.loc[point, 'Close']
            sar = sar_values.loc[point]
            print(f"  {point}: Price={price:.6f}, SAR={sar:.6f}, Diff={price-sar:.6f}")
    
    if len(sell_points) > 0:
        print("\nSell signal analysis:")
        for i, point in enumerate(sell_points[:5]):  # Show first 5
            price = df.loc[point, 'Close']
            sar = sar_values.loc[point]
            print(f"  {point}: Price={price:.6f}, SAR={sar:.6f}, Diff={price-sar:.6f}")
    
    print()


def analyze_parameter_sensitivity(df):
    """Analyze SAR sensitivity to different parameters."""
    print("=== PARAMETER SENSITIVITY ANALYSIS ===")
    
    # Test different parameter combinations
    param_combinations = [
        (0.000002, 0.00005),  # Original command parameters
        (0.02, 0.2),          # Standard parameters
        (0.01, 0.1),          # Medium parameters
        (0.05, 0.3),          # Aggressive parameters
    ]
    
    results = []
    
    for acc, max_val in param_combinations:
        sar_values = calculate_sar(df, acc, max_val)
        signals = calculate_sar_signals(df['Close'], sar_values)
        
        buy_signals = (signals == BUY).sum()
        sell_signals = (signals == SELL).sum()
        total_signals = buy_signals + sell_signals
        
        sar_range = sar_values.max() - sar_values.min()
        
        results.append({
            'acceleration': acc,
            'maximum': max_val,
            'buy_signals': buy_signals,
            'sell_signals': sell_signals,
            'total_signals': total_signals,
            'sar_range': sar_range,
            'signal_density': total_signals / len(df) * 100
        })
    
    # Display results
    results_df = pd.DataFrame(results)
    print(results_df.to_string(index=False, float_format='%.6f'))
    print()


def create_visualization(df, sar_values, signals):
    """Create visualization of SAR analysis."""
    print("=== CREATING VISUALIZATION ===")
    
    # Create figure with subplots
    fig, axes = plt.subplots(2, 1, figsize=(15, 10))
    
    # Plot 1: Price and SAR
    axes[0].plot(df.index, df['Close'], label='Close Price', alpha=0.7)
    axes[0].plot(df.index, sar_values, label='SAR', alpha=0.7)
    
    # Highlight signal points
    buy_points = signals[signals == BUY].index
    sell_points = signals[signals == SELL].index
    
    if len(buy_points) > 0:
        axes[0].scatter(buy_points, df.loc[buy_points, 'Close'], 
                       color='green', marker='^', s=50, label='Buy Signal', alpha=0.8)
    if len(sell_points) > 0:
        axes[0].scatter(sell_points, df.loc[sell_points, 'Close'], 
                       color='red', marker='v', s=50, label='Sell Signal', alpha=0.8)
    
    axes[0].set_title('SAR Indicator Analysis')
    axes[0].set_ylabel('Price')
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)
    
    # Plot 2: Signal distribution
    signal_counts = signals.value_counts()
    signal_names = ['No Trade', 'Buy', 'Sell']
    signal_values = [signal_counts.get(NOTRADE, 0), 
                    signal_counts.get(BUY, 0), 
                    signal_counts.get(SELL, 0)]
    
    colors = ['gray', 'green', 'red']
    axes[1].bar(signal_names, signal_values, color=colors, alpha=0.7)
    axes[1].set_title('Signal Distribution')
    axes[1].set_ylabel('Count')
    
    # Add value labels on bars
    for i, v in enumerate(signal_values):
        axes[1].text(i, v + max(signal_values) * 0.01, str(v), 
                    ha='center', va='bottom')
    
    plt.tight_layout()
    
    # Save plot
    output_path = Path("results/plots/sar_analysis.png")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"Visualization saved to: {output_path}")
    
    plt.show()


def main():
    """Main analysis function."""
    print("SAR Command Analysis")
    print("Command: uv run run_analysis.py show csv mn1 -d fastest --rule sar:0.000002,0.00005")
    print("=" * 80)
    
    # Load data
    df = load_mn1_data()
    if df is None:
        return
    
    # Analyze SAR performance
    sar_values, signals = analyze_sar_performance(df)
    
    # Analyze signal timing
    analyze_signal_timing(df, signals, sar_values)
    
    # Analyze parameter sensitivity
    analyze_parameter_sensitivity(df)
    
    # Create visualization
    try:
        create_visualization(df, sar_values, signals)
    except Exception as e:
        print(f"Visualization failed: {e}")
    
    print("=== ANALYSIS COMPLETE ===")


if __name__ == "__main__":
    main() 