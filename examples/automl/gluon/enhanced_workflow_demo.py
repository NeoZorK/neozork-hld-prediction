#!/usr/bin/env python3
"""
Enhanced AutoGluon Workflow Demo with 13 Custom Features
Демонстрация расширенного workflow с 13 пользовательскими признаками
"""

import pandas as pd
import numpy as np
import os
import sys
from pathlib import Path
import logging
from datetime import datetime

# Add src to path
sys.path.insert(0, os.path.abspath('src'))

from automl.gluon import GluonAutoML

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def print_step(step: int, title: str):
    """Print step header."""
    print(f"\n{'='*60}")
    print(f"STEP {step}: {title}")
    print(f"{'='*60}")


def enhanced_workflow_demo():
    """Enhanced workflow demonstration with 13 custom features."""
    
    print("🚀 Enhanced AutoGluon Workflow Demo with 13 Custom Features")
    print("=" * 60)
    
    # Step 1: Initialize AutoGluon
    print_step(1, "Initialize AutoGluon")
    
    try:
        gluon = GluonAutoML()
        print("✅ AutoGluon initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize AutoGluon: {e}")
        return
    
    # Step 2: Load data
    print_step(2, "Load Data")
    
    try:
        # Use BTCUSD data for demonstration
        data_path = "data/cache/csv_converted/CSVExport_BTCUSD_PERIOD_D1.parquet"
        
        if not os.path.exists(data_path):
            print(f"❌ Data file not found: {data_path}")
            return
        
        data = gluon.load_data(data_path)
        print(f"✅ Data loaded successfully")
        print(f"📊 Data shape: {data.shape}")
        print(f"📊 Columns: {list(data.columns)}")
        print(f"📊 Date range: {data.index.min()} to {data.index.max()}")
        
    except Exception as e:
        print(f"❌ Failed to load data: {e}")
        return
    
    # Step 3: Create custom features
    print_step(3, "Create 13 Custom Features")
    
    try:
        # Create custom features
        data_with_features = gluon.create_custom_features(data, use_13_features=True)
        
        print(f"✅ Custom features created successfully")
        print(f"📊 Original features: {len(data.columns)}")
        print(f"📊 Features with custom: {len(data_with_features.columns)}")
        print(f"📊 Custom features added: {len(data_with_features.columns) - len(data.columns)}")
        
        # Show some custom features
        custom_feature_cols = [col for col in data_with_features.columns if 'prob' in col]
        print(f"📊 Custom feature examples: {custom_feature_cols[:5]}...")
        
    except Exception as e:
        print(f"❌ Failed to create custom features: {e}")
        return
    
    # Step 4: Prepare data for ML
    print_step(4, "Prepare Data for ML")
    
    try:
        # Create target variable (simplified for demo)
        data_with_features['target'] = np.where(
            data_with_features['Close'].diff() > 0, 1, 0
        )
        
        # Remove rows with NaN target
        data_with_features = data_with_features.dropna(subset=['target'])
        
        print(f"✅ Data prepared for ML")
        print(f"📊 Final data shape: {data_with_features.shape}")
        print(f"📊 Target distribution: {data_with_features['target'].value_counts().to_dict()}")
        
    except Exception as e:
        print(f"❌ Failed to prepare data: {e}")
        return
    
    # Step 5: Time series split
    print_step(5, "Time Series Split")
    
    try:
        train_data, val_data, test_data = gluon.create_time_series_split(data_with_features)
        
        print(f"✅ Time series split completed")
        print(f"📊 Train: {len(train_data)} rows ({len(train_data)/len(data_with_features)*100:.1f}%)")
        print(f"📊 Validation: {len(val_data)} rows ({len(val_data)/len(data_with_features)*100:.1f}%)")
        print(f"📊 Test: {len(test_data)} rows ({len(test_data)/len(data_with_features)*100:.1f}%)")
        
    except Exception as e:
        print(f"❌ Failed in time series split: {e}")
        return
    
    # Step 6: Train models
    print_step(6, "Train Models")
    
    try:
        gluon.train_models(train_data, "target", val_data)
        print(f"✅ Model training completed successfully")
        
    except Exception as e:
        print(f"❌ Failed in model training: {e}")
        return
    
    # Step 7: Evaluate models
    print_step(7, "Evaluate Models")
    
    try:
        evaluation = gluon.evaluate_models(test_data, "target")
        print(f"✅ Model evaluation completed")
        
        # Display evaluation results
        if 'accuracy' in evaluation:
            print(f"📊 Accuracy: {evaluation['accuracy']:.4f}")
        if 'rmse' in evaluation:
            print(f"📊 RMSE: {evaluation['rmse']:.4f}")
        
        # Display value scores
        if 'value_scores' in evaluation and evaluation['value_scores']:
            print(f"📊 Value Scores:")
            for metric, value in evaluation['value_scores'].items():
                print(f"   {metric}: {value:.4f}")
        
    except Exception as e:
        print(f"❌ Failed in model evaluation: {e}")
        return
    
    # Step 8: Make predictions
    print_step(8, "Make Predictions")
    
    try:
        predictions = gluon.predict(test_data)
        probabilities = gluon.predict_proba(test_data)
        
        print(f"✅ Predictions completed")
        print(f"📊 Predictions shape: {predictions.shape}")
        print(f"📊 Sample predictions: {predictions.head()}")
        
        if not probabilities.empty:
            print(f"📊 Probabilities shape: {probabilities.shape}")
            print(f"📊 Sample probabilities: {probabilities.head()}")
        
    except Exception as e:
        print(f"❌ Failed in making predictions: {e}")
        return
    
    # Step 9: Export models
    print_step(9, "Export Models")
    
    try:
        export_dir = gluon.export_models()
        print(f"✅ Models exported successfully")
        print(f"📁 Export directory: {export_dir}")
        
    except Exception as e:
        print(f"❌ Failed in model export: {e}")
        return
    
    # Step 10: Summary
    print_step(10, "Summary")
    
    print(f"🎯 Enhanced workflow completed successfully!")
    print(f"📊 Data processed: {len(data_with_features)} rows")
    print(f"📊 Features created: {len(data_with_features.columns)} total")
    print(f"📊 Custom features: {len([col for col in data_with_features.columns if 'prob' in col])}")
    print(f"📊 Model performance: {evaluation.get('accuracy', evaluation.get('rmse', 'N/A'))}")
    print(f"📁 Models saved to: {export_dir}")
    
    # Feature importance analysis
    try:
        if hasattr(gluon.predictor, 'feature_importance'):
            feature_importance = gluon.predictor.feature_importance()
            print(f"\n📊 Top 10 Most Important Features:")
            for i, (feature, importance) in enumerate(feature_importance.head(10).items()):
                print(f"   {i+1}. {feature}: {importance:.4f}")
    except Exception as e:
        print(f"⚠️ Could not get feature importance: {e}")
    
    print(f"\n🚀 The enhanced AutoGluon integration with 13 custom features is working!")
    print(f"📈 Ready for robust profitable ML models with custom trading features!")


if __name__ == "__main__":
    enhanced_workflow_demo()
