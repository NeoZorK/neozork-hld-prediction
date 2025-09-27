# -*- coding: utf-8 -*-
"""
Basic usage example for AutoGluon integration.

This example demonstrates how to use the GluonAutoML wrapper
for training and deploying ML models.
"""

import pandas as pd
import numpy as np
from pathlib import Path
import sys

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent.parent))

from gluon import GluonAutoML


def create_sample_data():
    """Create sample trading data for demonstration."""
    np.random.seed(42)
    n_samples = 1000
    
    # Create sample features (SCHR, SHORT3, WAVE2 indicators)
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
        
        # Target: probability of price increase in next 5 periods
        'target': np.random.choice([0, 1], n_samples, p=[0.4, 0.6])
    })
    
    # Add datetime index
    data.index = pd.date_range('2023-01-01', periods=n_samples, freq='H')
    
    return data


def main():
    """Main example function."""
    print("=== AutoGluon Integration Example ===\n")
    
    # Create sample data
    print("1. Creating sample data...")
    data = create_sample_data()
    print(f"   Created {len(data)} samples with {len(data.columns)} features")
    
    # Initialize GluonAutoML
    print("\n2. Initializing GluonAutoML...")
    experiment_config = {
        'experiment_name': 'trading_strategy_example',
        'target_column': 'target',
        'problem_type': 'binary',
        'time_limit': 300,  # 5 minutes for demo
        'train_ratio': 0.6,
        'validation_ratio': 0.2,
        'test_ratio': 0.2
    }
    
    gluon = GluonAutoML(experiment_config=experiment_config)
    print("   GluonAutoML initialized successfully")
    
    # Create time series split
    print("\n3. Creating time series split...")
    train_data, val_data, test_data = gluon.create_time_series_split(data)
    print(f"   Train: {len(train_data)} samples")
    print(f"   Validation: {len(val_data)} samples")
    print(f"   Test: {len(test_data)} samples")
    
    # Get data summary
    print("\n4. Analyzing data quality...")
    summary = gluon.get_data_summary(train_data)
    print(f"   Data shape: {summary['shape']}")
    print(f"   Missing values: {sum(summary['missing_values'].values())}")
    print(f"   Ready for AutoGluon: {summary['is_ready_for_gluon']}")
    
    # Train models
    print("\n5. Training AutoGluon models...")
    try:
        gluon.train_models(train_data, 'target', val_data)
        print("   Model training completed successfully")
    except Exception as e:
        print(f"   Training failed (expected in demo): {e}")
        return
    
    # Evaluate models
    print("\n6. Evaluating models...")
    try:
        results = gluon.evaluate_models(test_data, 'target')
        print("   Model evaluation completed")
        print(f"   Metrics: {list(results['metrics'].keys())}")
        print(f"   Value scores: {list(results['value_scores'].keys())}")
    except Exception as e:
        print(f"   Evaluation failed: {e}")
    
    # Make predictions
    print("\n7. Making predictions...")
    try:
        predictions = gluon.predict(test_data.iloc[:10])  # Predict on first 10 samples
        print(f"   Generated {len(predictions)} predictions")
        print(f"   Prediction columns: {list(predictions.columns)}")
    except Exception as e:
        print(f"   Prediction failed: {e}")
    
    # Export models
    print("\n8. Exporting models...")
    try:
        export_paths = gluon.export_models("models/example/")
        print("   Model export completed")
        print(f"   Export formats: {list(export_paths.keys())}")
    except Exception as e:
        print(f"   Export failed: {e}")
    
    # Monitor drift
    print("\n9. Monitoring for drift...")
    try:
        drift_results = gluon.monitor_drift(test_data.iloc[:50])
        print("   Drift monitoring completed")
        print(f"   Drift detected: {drift_results['drift_detected']}")
        print(f"   Recommendations: {len(drift_results['recommendations'])}")
    except Exception as e:
        print(f"   Drift monitoring failed: {e}")
    
    # Get model summary
    print("\n10. Getting model summary...")
    try:
        summary = gluon.get_model_summary()
        print("   Model summary retrieved")
        print(f"   Model info keys: {list(summary.keys())}")
    except Exception as e:
        print(f"   Summary retrieval failed: {e}")
    
    print("\n=== Example completed successfully ===")


if __name__ == "__main__":
    main()
