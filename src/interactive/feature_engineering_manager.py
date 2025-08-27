#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Feature Engineering Manager for Interactive System

This module handles all feature engineering operations including
feature generation, selection, and analysis.
"""

import time
from pathlib import Path
from typing import Dict, Any

import pandas as pd
import numpy as np


class FeatureEngineeringManager:
    """Manages feature engineering operations and functionality."""
    
    def __init__(self):
        """Initialize the feature engineering manager."""
        pass
    
    def run_feature_engineering_analysis(self, system):
        """Run Feature Engineering analysis menu."""
        while True:
            system.menu_manager.print_feature_engineering_menu()
            try:
                choice = input("Select option (0-8): ").strip()
            except EOFError:
                print("\n👋 Goodbye!")
                break
            
            if choice == '0':
                break
            elif choice == '1':
                self.generate_all_features(system)
            elif choice == '2':
                print("⏳ Proprietary Features - Coming soon!")
            elif choice == '3':
                print("⏳ Technical Indicators - Coming soon!")
            elif choice == '4':
                print("⏳ Statistical Features - Coming soon!")
            elif choice == '5':
                print("⏳ Temporal Features - Coming soon!")
            elif choice == '6':
                print("⏳ Cross-Timeframe Features - Coming soon!")
            elif choice == '7':
                print("⏳ Feature Selection - Coming soon!")
            elif choice == '8':
                self.show_feature_summary(system)
            else:
                print("❌ Invalid choice. Please select 0-8.")
            
            if choice != '0':
                if system.safe_input() is None:
                    break
    
    def generate_all_features(self, system):
        """Generate all features using the Feature Engineering system."""
        if system.current_data is None:
            print("❌ No data loaded. Please load data first.")
            return
            
        print("\n🚀 GENERATING ALL FEATURES")
        print("-" * 30)
        
        try:
            # Ensure minimum data size
            if system.current_data.shape[0] < 500:
                print(f"⚠️  Warning: Data has only {system.current_data.shape[0]} rows, minimum recommended is 500")
                print(f"   Padding data to 500 rows for feature generation...")
                
                # Pad data by repeating last rows
                padding_needed = 500 - system.current_data.shape[0]
                padding_data = system.current_data.iloc[-padding_needed:].copy()
                system.current_data = pd.concat([system.current_data, padding_data], ignore_index=True)
                print(f"   Data padded to {system.current_data.shape[0]} rows")
            
            # Try to import feature generator
            try:
                from src.ml.feature_engineering.feature_generator import FeatureGenerator, MasterFeatureConfig
                from src.ml.feature_engineering.feature_selector import FeatureSelectionConfig
                
                # Initialize feature generator
                feature_config = MasterFeatureConfig(
                    max_features=150,
                    min_importance=0.2,
                    correlation_threshold=0.95,
                    enable_proprietary=True,
                    enable_technical=True,
                    enable_statistical=True,
                    enable_temporal=True,
                    enable_cross_timeframe=True
                )
                
                selection_config = FeatureSelectionConfig(
                    max_features=150,
                    min_importance=0.2,
                    correlation_threshold=0.95,
                    methods=['correlation', 'importance', 'mutual_info', 'lasso', 'random_forest']
                )
                
                system.feature_generator = FeatureGenerator(
                    config=feature_config
                )
                
                # Generate features
                print("   Generating features...")
                start_time = time.time()
                
                data_with_features = system.feature_generator.generate_features(system.current_data)
                
                generation_time = time.time() - start_time
                
                # Get feature summary
                feature_summary = system.feature_generator.get_feature_summary()
                
                # Get memory usage
                memory_usage = system.feature_generator.get_memory_usage()
                
                print(f"✅ Feature generation completed!")
                print(f"   Original data: {system.current_data.shape[0]} rows × {system.current_data.shape[0]} columns")
                print(f"   Final data: {data_with_features.shape[0]} rows × {data_with_features.shape[1]} columns")
                print(f"   Features generated: {data_with_features.shape[1] - system.current_data.shape[1]}")
                print(f"   Generation time: {generation_time:.2f} seconds")
                # Safe memory usage printing
                if isinstance(memory_usage, dict) and 'rss' in memory_usage:
                    print(f"   Memory usage: {memory_usage['rss']:.1f} MB")
                else:
                    print(f"   Memory usage: {memory_usage}")
                
                # Save results
                system.current_results['feature_engineering'] = {
                    'original_shape': system.current_data.shape,
                    'final_shape': data_with_features.shape,
                    'features_generated': data_with_features.shape[1] - system.current_data.shape[1],
                    'feature_summary': feature_summary,
                    'memory_usage': memory_usage,
                    'data_with_features': data_with_features,
                    'generation_time': generation_time
                }
                
                # Update current data
                system.current_data = data_with_features
                
            except ImportError as e:
                print(f"⚠️  Feature engineering module not available: {e}")
                print("   Using basic feature generation...")
                
                # Basic feature generation as fallback
                self._generate_basic_features(system)
            
            # Mark as used
            system.menu_manager.mark_menu_as_used('feature_engineering', 'generate_all_features')
            
        except Exception as e:
            print(f"❌ Error in feature generation: {e}")
            import traceback
            traceback.print_exc()
    
    def _generate_basic_features(self, system):
        """Generate basic features as fallback when advanced feature generator is not available."""
        print("   Generating basic features...")
        start_time = time.time()
        
        # Create a copy for feature generation
        data_with_features = system.current_data.copy()
        original_shape = data_with_features.shape
        
        # Generate basic statistical features
        numeric_cols = data_with_features.select_dtypes(include=[np.number]).columns
        
        for col in numeric_cols:
            if col in data_with_features.columns:
                # Rolling mean features
                data_with_features[f'{col}_rolling_mean_5'] = data_with_features[col].rolling(window=5, min_periods=1).mean()
                data_with_features[f'{col}_rolling_mean_10'] = data_with_features[col].rolling(window=10, min_periods=1).mean()
                
                # Rolling std features
                data_with_features[f'{col}_rolling_std_5'] = data_with_features[col].rolling(window=5, min_periods=1).std()
                data_with_features[f'{col}_rolling_std_10'] = data_with_features[col].rolling(window=10, min_periods=1).std()
                
                # Lag features
                data_with_features[f'{col}_lag_1'] = data_with_features[col].shift(1)
                data_with_features[f'{col}_lag_2'] = data_with_features[col].shift(2)
                
                # Difference features
                data_with_features[f'{col}_diff_1'] = data_with_features[col].diff(1)
                data_with_features[f'{col}_diff_2'] = data_with_features[col].diff(2)
                
                # Percent change features
                data_with_features[f'{col}_pct_change_1'] = data_with_features[col].pct_change(1)
                data_with_features[f'{col}_pct_change_2'] = data_with_features[col].pct_change(2)
        
        # Generate interaction features for OHLCV columns
        ohlcv_cols = [col for col in data_with_features.columns if any(x in col.lower() for x in ['open', 'high', 'low', 'close', 'volume'])]
        
        if len(ohlcv_cols) >= 4:  # At least OHLC
            # Price range features
            if 'high' in [col.lower() for col in ohlcv_cols] and 'low' in [col.lower() for col in ohlcv_cols]:
                high_col = [col for col in ohlcv_cols if 'high' in col.lower()][0]
                low_col = [col for col in ohlcv_cols if 'low' in col.lower()][0]
                data_with_features['price_range'] = data_with_features[high_col] - data_with_features[low_col]
                data_with_features['price_range_pct'] = data_with_features['price_range'] / data_with_features[low_col]
            
            # Body size features
            if 'open' in [col.lower() for col in ohlcv_cols] and 'close' in [col.lower() for col in ohlcv_cols]:
                open_col = [col for col in ohlcv_cols if 'open' in col.lower()][0]
                close_col = [col for col in ohlcv_cols if 'close' in col.lower()][0]
                data_with_features['body_size'] = abs(data_with_features[close_col] - data_with_features[open_col])
                data_with_features['body_size_pct'] = data_with_features['body_size'] / data_with_features[open_col]
        
        # Fill NaN values
        data_with_features = data_with_features.fillna(method='ffill').fillna(method='bfill').fillna(0)
        
        generation_time = time.time() - start_time
        features_generated = data_with_features.shape[1] - original_shape[1]
        
        print(f"✅ Basic feature generation completed!")
        print(f"   Original data: {original_shape[0]} rows × {original_shape[1]} columns")
        print(f"   Final data: {data_with_features.shape[0]} rows × {data_with_features.shape[1]} columns")
        print(f"   Features generated: {features_generated}")
        print(f"   Generation time: {generation_time:.2f} seconds")
        
        # Save results
        system.current_results['feature_engineering'] = {
            'original_shape': original_shape,
            'final_shape': data_with_features.shape,
            'features_generated': features_generated,
            'feature_summary': f"Generated {features_generated} basic features",
            'memory_usage': f"{data_with_features.memory_usage(deep=True).sum() / 1024 / 1024:.1f} MB",
            'data_with_features': data_with_features,
            'generation_time': generation_time
        }
        
        # Update current data
        system.current_data = data_with_features
    
    def show_feature_summary(self, system):
        """Show feature summary report."""
        if 'feature_engineering' not in system.current_results:
            print("❌ No feature engineering results available. Please generate features first.")
            return
            
        print("\n📋 FEATURE SUMMARY REPORT")
        print("-" * 30)
        
        try:
            feature_summary = system.current_results['feature_engineering']['feature_summary']
            
            if isinstance(feature_summary, dict):
                # Sort features by importance
                sorted_features = sorted(
                    feature_summary.items(),
                    key=lambda x: x[1] if isinstance(x[1], (int, float)) else 0,
                    reverse=True
                )
                
                print(f"📊 Total features: {len(feature_summary)}")
                print(f"🎯 Top 20 features by importance:")
                
                for i, (feature, importance) in enumerate(sorted_features[:20], 1):
                    if isinstance(importance, (int, float)):
                        print(f"   {i:2d}. {feature:<35} {importance:.4f}")
                    else:
                        print(f"   {i:2d}. {feature:<35} {importance}")
                
                # Feature categories
                categories = {}
                for feature in feature_summary.keys():
                    if 'phld' in feature.lower() or 'wave' in feature.lower():
                        categories['proprietary'] = categories.get('proprietary', 0) + 1
                    elif any(x in feature.lower() for x in ['sma', 'ema', 'rsi', 'macd', 'bb', 'atr']):
                        categories['technical'] = categories.get('technical', 0) + 1
                    elif any(x in feature.lower() for x in ['mean', 'std', 'skew', 'kurt', 'percentile']):
                        categories['statistical'] = categories.get('statistical', 0) + 1
                    elif any(x in feature.lower() for x in ['hour', 'day', 'month', 'season']):
                        categories['temporal'] = categories.get('temporal', 0) + 1
                    elif any(x in feature.lower() for x in ['ratio', 'diff', 'momentum', 'volatility']):
                        categories['cross_timeframe'] = categories.get('cross_timeframe', 0) + 1
                    else:
                        categories['other'] = categories.get('other', 0) + 1
                
                print(f"\n📂 Feature Categories:")
                for category, count in categories.items():
                    print(f"   {category.title()}: {count} features")
            else:
                print(f"📊 Feature Summary: {feature_summary}")
            
            # Mark as used
            system.menu_manager.mark_menu_as_used('feature_engineering', 'feature_summary')
            
        except Exception as e:
            print(f"❌ Error showing feature summary: {e}")
