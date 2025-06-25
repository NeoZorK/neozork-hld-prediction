#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# scripts/demo_universal_metrics.py

"""
Demo script for Universal Trading Metrics Module
Demonstrates how to use the universal trading metrics calculator with different rules and parameters.
"""

import sys
import os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.calculation.universal_trading_metrics import (
    UniversalTradingMetrics, 
    display_universal_trading_metrics
)
from src.common.constants import BUY, SELL, NOTRADE


def create_demo_data(periods: int = 200) -> pd.DataFrame:
    """
    Create realistic demo trading data for testing.
    
    Args:
        periods (int): Number of data points to generate
    
    Returns:
        pd.DataFrame: DataFrame with OHLCV data and trading signals
    """
    print(f"📊 Creating demo data with {periods} periods...")
    
    # Generate dates
    start_date = datetime(2023, 1, 1)
    dates = [start_date + timedelta(days=i) for i in range(periods)]
    
    # Generate realistic price data with trend and volatility
    np.random.seed(42)  # For reproducible results
    
    # Create trending price series
    trend = np.linspace(0, 0.2, periods)  # 20% uptrend
    noise = np.random.normal(0, 0.02, periods)  # 2% daily volatility
    returns = trend + noise
    
    # Calculate prices
    prices = [100.0]  # Starting price
    for ret in returns[1:]:
        prices.append(prices[-1] * (1 + ret))
    
    # Create OHLCV data
    ohlcv_data = []
    for i, price in enumerate(prices):
        open_price = price
        close_price = price * (1 + np.random.normal(0, 0.005))
        high_price = max(open_price, close_price) * (1 + abs(np.random.normal(0, 0.003)))
        low_price = min(open_price, close_price) * (1 - abs(np.random.normal(0, 0.003)))
        
        ohlcv_data.append({
            'Open': open_price,
            'High': high_price,
            'Low': low_price,
            'Close': close_price,
            'Volume': np.random.randint(5000, 15000)
        })
    
    df = pd.DataFrame(ohlcv_data, index=dates)
    
    # Add realistic trading signals based on momentum
    signals = []
    for i in range(periods):
        if i < 20:
            signals.append(NOTRADE)  # Initial period
        else:
            # Simple momentum-based strategy
            momentum = (df['Close'].iloc[i] - df['Close'].iloc[i-5]) / df['Close'].iloc[i-5]
            if momentum > 0.015:  # 1.5% positive momentum
                signals.append(BUY)
            elif momentum < -0.015:  # 1.5% negative momentum
                signals.append(SELL)
            else:
                signals.append(NOTRADE)
    
    df['Direction'] = signals
    
    print(f"✅ Demo data created successfully!")
    print(f"   📅 Date range: {df.index[0].strftime('%Y-%m-%d')} to {df.index[-1].strftime('%Y-%m-%d')}")
    print(f"   📊 Total bars: {len(df)}")
    print(f"   🎯 Buy signals: {(df['Direction'] == BUY).sum()}")
    print(f"   🎯 Sell signals: {(df['Direction'] == SELL).sum()}")
    print(f"   ⚪ No trade: {(df['Direction'] == NOTRADE).sum()}")
    
    return df


def demo_basic_usage():
    """Demonstrate basic usage of universal trading metrics."""
    print("\n" + "="*80)
    print("🎯 DEMO 1: BASIC USAGE")
    print("="*80)
    
    # Create demo data
    df = create_demo_data(100)
    
    # Use the convenience function
    print("\n📈 Using convenience function...")
    metrics = display_universal_trading_metrics(
        df=df,
        rule="MOMENTUM_STRATEGY",
        lot_size=1.0,
        risk_reward_ratio=2.0,
        fee_per_trade=0.07
    )
    
    print(f"\n✅ Metrics calculated successfully!")
    print(f"   📊 Number of metrics: {len(metrics)}")
    print(f"   🎯 Win ratio: {metrics.get('win_ratio', 0):.1f}%")
    print(f"   💰 Profit factor: {metrics.get('profit_factor', 0):.2f}")


def demo_different_parameters():
    """Demonstrate usage with different strategy parameters."""
    print("\n" + "="*80)
    print("🎯 DEMO 2: DIFFERENT STRATEGY PARAMETERS")
    print("="*80)
    
    # Create demo data
    df = create_demo_data(150)
    
    # Conservative strategy
    print("\n🛡️  Conservative Strategy (Low risk):")
    conservative_calc = UniversalTradingMetrics(
        lot_size=0.5,
        risk_reward_ratio=1.5,
        fee_per_trade=0.05
    )
    
    with open(os.devnull, 'w') as fnull:
        import sys
        old_stdout = sys.stdout
        sys.stdout = fnull
        
        conservative_metrics = conservative_calc.calculate_and_display_metrics(
            df, "CONSERVATIVE_STRATEGY"
        )
        
        sys.stdout = old_stdout
    
    print(f"   📊 Position size: {conservative_calc.lot_size}")
    print(f"   ⚖️  Risk/Reward: {conservative_calc.risk_reward_ratio}")
    print(f"   💸 Fee per trade: {conservative_calc.fee_per_trade}%")
    print(f"   🎯 Kelly fraction: {conservative_metrics.get('kelly_fraction', 0):.3f}")
    print(f"   📈 Strategy efficiency: {conservative_metrics.get('strategy_efficiency', 0):.1f}%")
    
    # Aggressive strategy
    print("\n🚀 Aggressive Strategy (High risk):")
    aggressive_calc = UniversalTradingMetrics(
        lot_size=2.0,
        risk_reward_ratio=3.0,
        fee_per_trade=0.1
    )
    
    with open(os.devnull, 'w') as fnull:
        import sys
        old_stdout = sys.stdout
        sys.stdout = fnull
        
        aggressive_metrics = aggressive_calc.calculate_and_display_metrics(
            df, "AGGRESSIVE_STRATEGY"
        )
        
        sys.stdout = old_stdout
    
    print(f"   📊 Position size: {aggressive_calc.lot_size}")
    print(f"   ⚖️  Risk/Reward: {aggressive_calc.risk_reward_ratio}")
    print(f"   💸 Fee per trade: {aggressive_calc.fee_per_trade}%")
    print(f"   🎯 Kelly fraction: {aggressive_metrics.get('kelly_fraction', 0):.3f}")
    print(f"   📈 Strategy efficiency: {aggressive_metrics.get('strategy_efficiency', 0):.1f}%")


def demo_different_rules():
    """Demonstrate usage with different rule types."""
    print("\n" + "="*80)
    print("🎯 DEMO 3: DIFFERENT RULE TYPES")
    print("="*80)
    
    # Create demo data
    df = create_demo_data(120)
    
    # String rule
    print("\n📝 String Rule:")
    with open(os.devnull, 'w') as fnull:
        import sys
        old_stdout = sys.stdout
        sys.stdout = fnull
        
        metrics1 = display_universal_trading_metrics(df, "RSI_STRATEGY")
        
        sys.stdout = old_stdout
    
    print(f"   🎯 Rule type: String")
    print(f"   📊 Win ratio: {metrics1.get('win_ratio', 0):.1f}%")
    print(f"   💰 Profit factor: {metrics1.get('profit_factor', 0):.2f}")
    
    # Object rule
    print("\n🔧 Object Rule:")
    class TestRule:
        def __init__(self, name):
            self.name = name
    
    test_rule = TestRule("MACD_STRATEGY")
    
    with open(os.devnull, 'w') as fnull:
        import sys
        old_stdout = sys.stdout
        sys.stdout = fnull
        
        metrics2 = display_universal_trading_metrics(df, test_rule)
        
        sys.stdout = old_stdout
    
    print(f"   🎯 Rule type: Object")
    print(f"   📊 Rule name: {test_rule.name}")
    print(f"   📊 Win ratio: {metrics2.get('win_ratio', 0):.1f}%")
    print(f"   💰 Profit factor: {metrics2.get('profit_factor', 0):.2f}")
    
    # Class rule
    print("\n🏗️  Class Rule:")
    class TradingStrategy:
        def __init__(self, name, parameters):
            self.name = name
            self.parameters = parameters
    
    strategy = TradingStrategy("BOLLINGER_BANDS", {"period": 20, "std": 2})
    
    with open(os.devnull, 'w') as fnull:
        import sys
        old_stdout = sys.stdout
        sys.stdout = fnull
        
        metrics3 = display_universal_trading_metrics(df, strategy)
        
        sys.stdout = old_stdout
    
    print(f"   🎯 Rule type: Class")
    print(f"   📊 Rule name: {strategy.name}")
    print(f"   📊 Parameters: {strategy.parameters}")
    print(f"   📊 Win ratio: {metrics3.get('win_ratio', 0):.1f}%")
    print(f"   💰 Profit factor: {metrics3.get('profit_factor', 0):.2f}")


def demo_error_handling():
    """Demonstrate error handling capabilities."""
    print("\n" + "="*80)
    print("🎯 DEMO 4: ERROR HANDLING")
    print("="*80)
    
    # Test with None data
    print("\n❌ None data:")
    try:
        metrics = display_universal_trading_metrics(None, "TEST_RULE")
        print(f"   ✅ Handled gracefully: {len(metrics)} metrics returned")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test with empty DataFrame
    print("\n❌ Empty DataFrame:")
    empty_df = pd.DataFrame()
    try:
        metrics = display_universal_trading_metrics(empty_df, "TEST_RULE")
        print(f"   ✅ Handled gracefully: {len(metrics)} metrics returned")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test with missing signal column
    print("\n❌ Missing signal column:")
    df_no_signal = create_demo_data(50)
    df_no_signal = df_no_signal.drop(columns=['Direction'])
    try:
        metrics = display_universal_trading_metrics(df_no_signal, "TEST_RULE")
        print(f"   ✅ Handled gracefully: {len(metrics)} metrics returned")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test with invalid data types
    print("\n❌ Invalid data types:")
    df_invalid = create_demo_data(30)
    df_invalid['Close'] = 'invalid'  # This will cause calculation errors
    try:
        metrics = display_universal_trading_metrics(df_invalid, "TEST_RULE")
        print(f"   ✅ Handled gracefully: {len(metrics)} metrics returned")
    except Exception as e:
        print(f"   ❌ Error: {e}")


def demo_full_analysis():
    """Demonstrate full analysis with console output."""
    print("\n" + "="*80)
    print("🎯 DEMO 5: FULL ANALYSIS WITH CONSOLE OUTPUT")
    print("="*80)
    
    print("\n📊 This demo will show the complete console output...")
    print("   (Press Enter to continue)")
    input()
    
    # Create demo data
    df = create_demo_data(200)
    
    # Run full analysis with console output
    print("\n🚀 Running full universal trading metrics analysis...")
    metrics = display_universal_trading_metrics(
        df=df,
        rule="COMPREHENSIVE_ANALYSIS",
        lot_size=1.5,
        risk_reward_ratio=2.5,
        fee_per_trade=0.08
    )
    
    print(f"\n✅ Analysis completed successfully!")
    print(f"   📊 Total metrics calculated: {len(metrics)}")
    print(f"   🎯 Key metrics summary:")
    print(f"      - Win ratio: {metrics.get('win_ratio', 0):.1f}%")
    print(f"      - Profit factor: {metrics.get('profit_factor', 0):.2f}")
    print(f"      - Sharpe ratio: {metrics.get('sharpe_ratio', 0):.2f}")
    print(f"      - Max drawdown: {metrics.get('max_drawdown', 0):.1f}%")
    print(f"      - Total return: {metrics.get('total_return', 0):.1f}%")


def main():
    """Main demo function."""
    print("🎯 UNIVERSAL TRADING METRICS DEMO")
    print("="*80)
    print("This demo showcases the universal trading metrics module that:")
    print("✅ Works with any type of trading rule (string, object, class)")
    print("✅ Calculates comprehensive trading metrics")
    print("✅ Displays metrics strictly in console output")
    print("✅ Handles errors gracefully")
    print("✅ Supports different strategy parameters")
    print("="*80)
    
    # Run all demos
    demo_basic_usage()
    demo_different_parameters()
    demo_different_rules()
    demo_error_handling()
    
    # Ask user if they want to see full console output
    print("\n" + "="*80)
    print("🎯 FULL CONSOLE OUTPUT DEMO")
    print("="*80)
    print("Would you like to see the complete console output with all metrics?")
    print("This will display the full formatted analysis in the terminal.")
    print("(y/n): ", end="")
    
    response = input().lower().strip()
    if response in ['y', 'yes', 'да', 'д']:
        demo_full_analysis()
    else:
        print("Skipping full console output demo.")
    
    print("\n" + "="*80)
    print("✅ DEMO COMPLETED SUCCESSFULLY!")
    print("="*80)
    print("The universal trading metrics module is ready to use!")
    print("You can now integrate it into your trading analysis workflows.")
    print("="*80)


if __name__ == "__main__":
    main() 