# -*- coding: utf-8 -*-
"""
Advanced usage example for AutoGluon integration.

This example demonstrates advanced features like custom features,
drift monitoring, and model retraining.
"""

import pandas as pd
import numpy as np
from pathlib import Path
import sys
import time

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent.parent))

from gluon import GluonAutoML


def create_advanced_sample_data():
    """Create advanced sample data with custom features."""
    np.random.seed(42)
    n_samples = 2000
    
    # Create base features
    data = pd.DataFrame({
        # SCHR Levels features
        'schr_level_1': np.random.randn(n_samples),
        'schr_level_2': np.random.randn(n_samples),
        'schr_pv': np.random.randn(n_samples),
        'schr_direction': np.random.choice([1, 2, 3, 4], n_samples),
        
        # SHORT3 features
        'short3_signal': np.random.choice([1, 2, 3, 4], n_samples),
        'short3_direction': np.random.choice([1, 2, 3, 4], n_samples),
        'short3_ma': np.random.randn(n_samples),
        
        # WAVE2 features
        'wave2_signal': np.random.choice([0, 1], n_samples),
        'wave2_ma': np.random.randn(n_samples),
        'wave2_reverse': np.random.randn(n_samples),
        
        # Price features
        'open': 100 + np.cumsum(np.random.randn(n_samples) * 0.1),
        'high': 100 + np.cumsum(np.random.randn(n_samples) * 0.1) + np.random.rand(n_samples),
        'low': 100 + np.cumsum(np.random.randn(n_samples) * 0.1) - np.random.rand(n_samples),
        'close': 100 + np.cumsum(np.random.randn(n_samples) * 0.1),
        'volume': np.random.randint(1000, 10000, n_samples),
    })
    
    # Add datetime index
    data.index = pd.date_range('2023-01-01', periods=n_samples, freq='H')
    
    # Create custom features (13 types as specified)
    data = create_custom_features(data)
    
    # Create target variable
    data['target'] = create_target_variable(data)
    
    return data


def create_custom_features(data):
    """Create custom features based on the 13 types specified."""
    
    # 1. Trend probability (simplified)
    data['trend_probability'] = np.where(
        data['close'] > data['close'].shift(1), 1, 0
    )
    
    # 2. Level breakout yellow (simplified)
    data['level_breakout_yellow'] = np.where(
        data['schr_level_1'] > data['schr_level_1'].shift(1), 1, 0
    )
    
    # 3. Level breakout blue (simplified)
    data['level_breakout_blue'] = np.where(
        data['schr_level_2'] < data['schr_level_2'].shift(1), 1, 0
    )
    
    # 4. PV sign
    data['pv_sign'] = np.where(data['schr_pv'] > 0, 1, 0)
    
    # 5. Wave signal 1 - 5 candles (simplified)
    data['wave_signal_1_candles'] = np.where(
        (data['wave2_signal'] == 1) & 
        (data['close'] > data['close'].shift(5)), 1, 0
    )
    
    # 6. Wave signal 1 - distance (simplified)
    data['wave_signal_1_distance'] = np.where(
        (data['wave2_signal'] == 1) & 
        (data['close'] > data['close'].shift(1) * 1.05), 1, 0
    )
    
    # 7. Wave signal 1 MA - 5 candles (simplified)
    data['wave_signal_1_ma_candles'] = np.where(
        (data['wave2_signal'] == 1) & 
        (data['wave2_ma'] < data['open']) & 
        (data['close'] > data['close'].shift(5)), 1, 0
    )
    
    # 8. Wave signal 1 MA - distance (simplified)
    data['wave_signal_1_ma_distance'] = np.where(
        (data['wave2_signal'] == 1) & 
        (data['wave2_ma'] < data['open']) & 
        (data['close'] > data['close'].shift(1) * 1.05), 1, 0
    )
    
    # 9. Short3 signal 1 (simplified)
    data['short3_signal_1'] = np.where(
        (data['short3_signal'] == 1) & 
        (data['close'] > data['close'].shift(1) * 1.05), 1, 0
    )
    
    # 10. Short3 signal 4 (simplified)
    data['short3_signal_4'] = np.where(
        (data['short3_signal'] == 4) & 
        (data['close'] < data['close'].shift(1) * 0.9), 1, 0
    )
    
    # 11. Short3 direction change (simplified)
    data['short3_direction_change'] = np.where(
        (data['short3_direction'].shift(1).isin([1, 4])) & 
        (data['short3_direction'].isin([2, 3])), 1, 0
    )
    
    # 12. Wave reverse peak sign (simplified)
    data['wave_reverse_peak_sign'] = np.where(
        data['wave2_reverse'] > 0, 1, 0
    )
    
    # 13. Wave reverse peak time (simplified)
    data['wave_reverse_peak_time'] = np.where(
        data['wave2_reverse'].rolling(10).max() > 0, 1, 0
    )
    
    return data


def create_target_variable(data):
    """Create target variable based on future price movements."""
    # Simple target: price increase in next 5 periods
    future_returns = data['close'].shift(-5) / data['close'] - 1
    return np.where(future_returns > 0.02, 1, 0)  # 2% threshold


def main():
    """Main advanced example function."""
    print("=== Advanced AutoGluon Integration Example ===\n")
    
    # Create advanced sample data
    print("1. Creating advanced sample data with custom features...")
    data = create_advanced_sample_data()
    print(f"   Created {len(data)} samples with {len(data.columns)} features")
    print(f"   Custom features: {[col for col in data.columns if 'trend_' in col or 'level_' in col or 'wave_' in col or 'short3_' in col]}")
    
    # Initialize GluonAutoML with custom configuration
    print("\n2. Initializing GluonAutoML with custom configuration...")
    experiment_config = {
        'experiment_name': 'advanced_trading_strategy',
        'target_column': 'target',
        'problem_type': 'binary',
        'time_limit': 600,  # 10 minutes for demo
        'train_ratio': 0.6,
        'validation_ratio': 0.2,
        'test_ratio': 0.2,
        'use_custom_features': True,
        'max_auto_features': 500,
        'enable_drift_monitoring': True,
        'retrain_on_drift': True
    }
    
    gluon = GluonAutoML(experiment_config=experiment_config)
    print("   GluonAutoML initialized with advanced configuration")
    
    # Create time series split
    print("\n3. Creating time series split...")
    train_data, val_data, test_data = gluon.create_time_series_split(data)
    print(f"   Train: {len(train_data)} samples")
    print(f"   Validation: {len(val_data)} samples")
    print(f"   Test: {len(test_data)} samples")
    
    # Analyze data quality
    print("\n4. Analyzing data quality...")
    summary = gluon.get_data_summary(train_data)
    print(f"   Data shape: {summary['shape']}")
    print(f"   Missing values: {sum(summary['missing_values'].values())}")
    print(f"   Quality issues: {len(summary['quality_issues'])}")
    print(f"   Ready for AutoGluon: {summary['is_ready_for_gluon']}")
    
    # Train models with custom features
    print("\n5. Training AutoGluon models with custom features...")
    try:
        start_time = time.time()
        gluon.train_models(train_data, 'target', val_data)
        training_time = time.time() - start_time
        print(f"   Model training completed in {training_time:.2f} seconds")
    except Exception as e:
        print(f"   Training failed (expected in demo): {e}")
        return
    
    # Evaluate models with value scores
    print("\n6. Evaluating models with value scores...")
    try:
        results = gluon.evaluate_models(test_data, 'target')
        print("   Model evaluation completed")
        
        # Display metrics
        if 'metrics' in results:
            print(f"   Metrics: {list(results['metrics'].keys())}")
            for metric, value in results['metrics'].items():
                if isinstance(value, (int, float)):
                    print(f"     {metric}: {value:.4f}")
        
        # Display value scores
        if 'value_scores' in results:
            print(f"   Value scores: {list(results['value_scores'].keys())}")
            for score, value in results['value_scores'].items():
                if isinstance(value, (int, float)):
                    print(f"     {score}: {value:.4f}")
    except Exception as e:
        print(f"   Evaluation failed: {e}")
    
    # Make predictions with confidence
    print("\n7. Making predictions with confidence...")
    try:
        predictions = gluon.predict(test_data.iloc[:20])  # Predict on first 20 samples
        print(f"   Generated {len(predictions)} predictions")
        print(f"   Prediction columns: {list(predictions.columns)}")
        
        # Display sample predictions
        print("   Sample predictions:")
        print(predictions.head())
    except Exception as e:
        print(f"   Prediction failed: {e}")
    
    # Export models for walk forward and Monte Carlo
    print("\n8. Exporting models for walk forward and Monte Carlo...")
    try:
        # Export for walk forward
        wf_paths = gluon.exporter.export_for_walk_forward(gluon.predictor, "models/walk_forward/")
        print("   Walk forward export completed")
        print(f"   Walk forward files: {list(wf_paths.keys())}")
        
        # Export for Monte Carlo
        mc_paths = gluon.exporter.export_for_monte_carlo(gluon.predictor, "models/monte_carlo/")
        print("   Monte Carlo export completed")
        print(f"   Monte Carlo files: {list(mc_paths.keys())}")
        
        # Create deployment package
        deploy_paths = gluon.exporter.create_deployment_package(gluon.predictor, "models/deployment/")
        print("   Deployment package created")
        print(f"   Deployment files: {list(deploy_paths.keys())}")
    except Exception as e:
        print(f"   Export failed: {e}")
    
    # Monitor drift with new data
    print("\n9. Monitoring drift with new data...")
    try:
        # Simulate new data with some drift
        new_data = test_data.iloc[:100].copy()
        new_data['schr_level_1'] = new_data['schr_level_1'] * 1.5  # Simulate drift
        
        drift_results = gluon.monitor_drift(new_data)
        print("   Drift monitoring completed")
        print(f"   Drift detected: {drift_results['drift_detected']}")
        print(f"   High PSI features: {len(drift_results.get('psi_scores', {}))}")
        print(f"   Recommendations: {len(drift_results['recommendations'])}")
        
        if drift_results['recommendations']:
            print("   Recommendations:")
            for rec in drift_results['recommendations']:
                print(f"     - {rec}")
    except Exception as e:
        print(f"   Drift monitoring failed: {e}")
    
    # Test retraining
    print("\n10. Testing model retraining...")
    try:
        # Check retrain status
        retrain_status = gluon.retrainer.get_retrain_status()
        print(f"   Retrain status: {retrain_status}")
        
        # Simulate retraining decision
        should_retrain = gluon.retrainer.should_retrain(0.6, 0.8, 200)
        print(f"   Should retrain: {should_retrain}")
        
        if should_retrain:
            print("   Retraining would be triggered based on performance degradation")
        else:
            print("   No retraining needed at this time")
    except Exception as e:
        print(f"   Retraining test failed: {e}")
    
    # Get comprehensive model summary
    print("\n11. Getting comprehensive model summary...")
    try:
        summary = gluon.get_model_summary()
        print("   Model summary retrieved")
        print(f"   Summary keys: {list(summary.keys())}")
        
        if 'model_info' in summary:
            print(f"   Model info: {summary['model_info']}")
        
        if 'feature_importance' in summary and not summary['feature_importance'].empty:
            print("   Top 5 most important features:")
            top_features = summary['feature_importance'].head()
            for idx, row in top_features.iterrows():
                print(f"     {idx}: {row.iloc[0]:.4f}")
    except Exception as e:
        print(f"   Summary retrieval failed: {e}")
    
    print("\n=== Advanced example completed successfully ===")


if __name__ == "__main__":
    main()
