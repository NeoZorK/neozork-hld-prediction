#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# scripts/demo_feature_engineering.py

"""
Demo script for the Feature Engineering system.

This script demonstrates the complete feature engineering pipeline:
1. Load sample data
2. Generate features using all generators
3. Perform feature selection
4. Export reports
5. Display results
"""

import sys
import os
import pandas as pd
import numpy as np
import time
from datetime import datetime, timedelta

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from ml.feature_engineering.feature_generator import FeatureGenerator, MasterFeatureConfig
from ml.feature_engineering.proprietary_features import ProprietaryFeatureConfig
from ml.feature_engineering.technical_features import TechnicalFeatureConfig
from ml.feature_engineering.statistical_features import StatisticalFeatureConfig
from ml.feature_engineering.temporal_features import TemporalFeatureConfig
from ml.feature_engineering.cross_timeframe_features import CrossTimeframeFeatureConfig


def create_sample_data(rows=1000):
    """
    Create sample OHLCV data for demonstration.
    
    Args:
        rows: Number of rows to generate
        
    Returns:
        DataFrame with sample OHLCV data
    """
    print(f"Creating sample data with {rows} rows...")
    
    # Generate time index
    start_date = datetime(2020, 1, 1)
    dates = [start_date + timedelta(hours=i) for i in range(rows)]
    
    # Generate price data with some realistic patterns
    np.random.seed(42)  # For reproducibility
    
    # Base price
    base_price = 100.0
    prices = [base_price]
    
    # Generate price movements
    for i in range(1, rows):
        # Random walk with trend
        change = np.random.normal(0.001, 0.02)  # Small daily change with volatility
        if i % 24 == 0:  # Daily trend
            change += np.random.normal(0.002, 0.01)
        new_price = prices[-1] * (1 + change)
        prices.append(max(new_price, 0.01))  # Ensure positive prices
    
    # Create OHLCV data
    data = []
    for i, (date, close) in enumerate(zip(dates, prices)):
        # Generate realistic OHLC from close price
        volatility = close * 0.01  # 1% volatility
        
        high = close + np.random.uniform(0, volatility)
        low = close - np.random.uniform(0, volatility)
        open_price = np.random.uniform(low, high)
        
        # Ensure proper OHLC relationship
        high = max(high, open_price, close)
        low = min(low, open_price, close)
        
        # Generate volume (correlated with price movement)
        volume = np.random.uniform(1000, 10000)
        if abs(close - open_price) > volatility * 0.5:
            volume *= 1.5  # Higher volume for larger moves
        
        data.append({
            'DateTime': date,
            'Open': round(open_price, 5),
            'High': round(high, 5),
            'Low': round(low, 5),
            'Close': round(close, 5),
            'Volume': int(volume)
        })
    
    df = pd.DataFrame(data)
    df.set_index('DateTime', inplace=True)
    
    print(f"Sample data created: {df.shape}")
    print(f"Date range: {df.index.min()} to {df.index.max()}")
    print(f"Price range: ${df['Low'].min():.2f} to ${df['High'].max():.2f}")
    
    return df


def configure_feature_generators():
    """
    Configure all feature generators with optimized settings.
    
    Returns:
        MasterFeatureConfig object
    """
    print("Configuring feature generators...")
    
    # Proprietary features configuration
    proprietary_config = ProprietaryFeatureConfig(
        phld_point_size=0.00001,  # Forex point size
        phld_trading_rules=['PV_HighLow', 'PV_Momentum'],
        wave_parameter_sets=[
            # Conservative set
            {'long1': 200, 'fast1': 8, 'trend1': 2, 'long2': 20, 'fast2': 10, 'trend2': 3, 'sma_period': 20},
            # Balanced set
            {'long1': 100, 'fast1': 5, 'trend1': 1, 'long2': 15, 'fast2': 8, 'trend2': 2, 'sma_period': 15}
        ],
        wave_trading_rules=['TR_Fast', 'TR_Zone'],
        create_derivative_features=True,
        create_interaction_features=True,
        create_momentum_features=True
    )
    
    # Technical features configuration
    technical_config = TechnicalFeatureConfig(
        short_periods=[5, 10, 14],
        medium_periods=[20, 50],
        long_periods=[100, 200],
        price_types=['open', 'high', 'low', 'close'],
        ma_types=['sma', 'ema'],
        rsi_periods=[14, 21],
        macd_fast_periods=[12, 26],
        macd_slow_periods=[26, 52],
        macd_signal_periods=[9],
        bb_periods=[20],
        bb_std_devs=[2.0],
        atr_periods=[14, 20],
        stoch_k_periods=[14],
        stoch_d_periods=[3]
    )
    
    # Statistical features configuration
    statistical_config = StatisticalFeatureConfig(
        short_periods=[5, 10, 14],
        medium_periods=[20, 50],
        long_periods=[100, 200],
        price_types=['open', 'high', 'low', 'close'],
        rolling_periods=[10, 20, 50],
        percentile_levels=[5, 10, 25, 75, 90, 95],
        zscore_thresholds=[2.0, 3.0],
        distribution_periods=[20, 50]
    )
    
    # Temporal features configuration
    temporal_config = TemporalFeatureConfig(
        short_periods=[5, 10, 14],
        medium_periods=[20, 50],
        long_periods=[100, 200],
        price_types=['open', 'high', 'low', 'close'],
        enable_time_features=True,
        enable_date_features=True,
        enable_seasonal_features=True,
        enable_cyclical_features=True,
        cyclical_periods={'hour': 24, 'day': 7, 'month': 12},
        seasonal_periods=[24, 168, 720]  # Hour, week, month
    )
    
    # Cross-timeframe features configuration
    cross_timeframe_config = CrossTimeframeFeatureConfig(
        short_periods=[5, 10, 14],
        medium_periods=[20, 50],
        long_periods=[100, 200],
        price_types=['open', 'high', 'low', 'close'],
        timeframes=['1h', '4h', '1d'],
        aggregation_methods=['mean', 'std', 'min', 'max'],
        feature_types=['ratio', 'difference', 'momentum', 'volatility'],
        lookback_periods=[5, 10, 20, 50]
    )
    
    # Master configuration
    master_config = MasterFeatureConfig(
        enable_proprietary=True,
        enable_technical=True,
        enable_statistical=True,
        enable_temporal=True,
        enable_cross_timeframe=True,
        max_features=150,  # Limit to 150 features for demo
        min_importance=0.2,
        correlation_threshold=0.95,
        parallel_processing=False,
        memory_limit_gb=4.0,
        proprietary_config=proprietary_config,
        technical_config=technical_config,
        statistical_config=statistical_config,
        temporal_config=temporal_config,
        cross_timeframe_config=cross_timeframe_config
    )
    
    print("Feature generators configured successfully")
    return master_config


def run_feature_generation_demo():
    """Run the complete feature generation demo."""
    print("=" * 80)
    print("NEOZORk HLD PREDICTION - FEATURE ENGINEERING DEMO")
    print("=" * 80)
    print()
    
    try:
        # Step 1: Create sample data
        df = create_sample_data(rows=500)  # Reduced for demo speed
        print()
        
        # Step 2: Configure feature generators
        config = configure_feature_generators()
        print()
        
        # Step 3: Initialize feature generator
        print("Initializing feature generator...")
        feature_generator = FeatureGenerator(config)
        print("Feature generator initialized successfully")
        print()
        
        # Step 4: Generate features
        print("Starting feature generation...")
        start_time = time.time()
        
        df_with_features = feature_generator.generate_features(df)
        
        generation_time = time.time() - start_time
        print(f"Feature generation completed in {generation_time:.2f} seconds")
        print()
        
        # Step 5: Display results
        print("FEATURE GENERATION RESULTS:")
        print("-" * 40)
        
        # Original data info
        print(f"Original data shape: {df.shape}")
        print(f"Original columns: {list(df.columns)}")
        print()
        
        # Features info
        print(f"Data with features shape: {df_with_features.shape}")
        print(f"Total features generated: {feature_generator.get_feature_count()}")
        print()
        
        # Feature categories
        categories = feature_generator.get_feature_categories()
        for category, features in categories.items():
            if features:
                print(f"{category.capitalize()} features: {len(features)}")
                if len(features) <= 10:  # Show all if <= 10
                    for feature in features[:10]:
                        print(f"  - {feature}")
                else:  # Show first 5 and last 5
                    for feature in features[:5]:
                        print(f"  - {feature}")
                    print(f"  ... ({len(features) - 10} more features)")
                    for feature in features[-5:]:
                        print(f"  - {feature}")
                print()
        
        # Feature importance (top 10)
        importance = feature_generator.get_feature_importance()
        if importance:
            print("Top 10 features by importance:")
            sorted_importance = sorted(importance.items(), key=lambda x: x[1], reverse=True)[:10]
            for i, (feature, score) in enumerate(sorted_importance, 1):
                print(f"  {i:2d}. {feature:<40} {score:.4f}")
            print()
        
        # Step 6: Export reports
        print("Exporting reports...")
        
        # Feature generation report
        feature_report_path = feature_generator.export_feature_report()
        if feature_report_path:
            print(f"Feature report exported to: {feature_report_path}")
        
        # Feature selection report
        if hasattr(feature_generator.feature_selector, 'export_selection_report'):
            selection_report_path = feature_generator.feature_selector.export_selection_report()
            if selection_report_path:
                print(f"Feature selection report exported to: {selection_report_path}")
        
        print()
        
        # Step 7: Memory usage
        memory_info = feature_generator.get_memory_usage()
        if 'error' not in memory_info:
            print("Memory usage:")
            print(f"  RSS: {memory_info['rss_mb']:.1f} MB")
            print(f"  VMS: {memory_info['vms_mb']:.1f} MB")
            print(f"  Percent: {memory_info['percent']:.1f}%")
        else:
            print("Memory usage: psutil not available")
        
        print()
        
        # Step 8: Summary
        print("DEMO SUMMARY:")
        print("-" * 20)
        print(f"✓ Generated {feature_generator.get_feature_count()} features")
        print(f"✓ Used {len(feature_generator.generators)} feature generators")
        print(f"✓ Processing time: {generation_time:.2f} seconds")
        print(f"✓ Data shape: {df.shape} → {df_with_features.shape}")
        print(f"✓ Reports exported to logs/ directory")
        
        # Step 9: Cleanup
        print("\nCleaning up...")
        feature_generator.cleanup()
        print("Cleanup completed")
        
        print("\n" + "=" * 80)
        print("FEATURE ENGINEERING DEMO COMPLETED SUCCESSFULLY!")
        print("=" * 80)
        
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        print(f"Traceback:\n{traceback.format_exc()}")
        return False


def main():
    """Main function."""
    try:
        success = run_feature_generation_demo()
        if success:
            print("\n🎉 Demo completed successfully!")
            sys.exit(0)
        else:
            print("\n💥 Demo failed!")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n\n⚠️  Demo interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        import traceback
        print(f"Traceback:\n{traceback.format_exc()}")
        sys.exit(1)


if __name__ == "__main__":
    main()
