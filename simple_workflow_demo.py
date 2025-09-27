#!/usr/bin/env python3
"""
Simplified AutoGluon Integration Workflow Demo
Using real data from data/cache/csv_converted/
"""

import pandas as pd
import numpy as np
import os
import sys
from pathlib import Path
import logging

# Add src to path for imports
sys.path.insert(0, os.path.abspath('src'))

from automl.gluon import GluonAutoML
from automl.gluon.config import GluonConfig, ExperimentConfig

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("simple_workflow_demo")

def print_section(title):
    """Print a formatted section header."""
    print(f"\n{'='*60}")
    print(f"🎯 {title}")
    print(f"{'='*60}")

def print_step(step, description):
    """Print a formatted step."""
    print(f"\n📋 Step {step}: {description}")
    print("-" * 50)

def main():
    """Simplified workflow demonstration."""
    print_section("AutoGluon Integration Simplified Workflow Demo")
    print("Using real data from data/cache/csv_converted/")
    
    # Step 1: Initialize AutoGluon
    print_step(1, "Initialize AutoGluon Integration")
    try:
        gluon = GluonAutoML()
        print("✅ GluonAutoML initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize GluonAutoML: {e}")
        return
    
    # Step 2: Load data
    print_step(2, "Load Data")
    
    # Use BTCUSD D1 data
    btc_file = "data/cache/csv_converted/CSVExport_BTCUSD_PERIOD_D1.parquet"
    
    if not os.path.exists(btc_file):
        print(f"❌ BTCUSD file not found: {btc_file}")
        return
    
    try:
        # Load the data
        data = gluon.load_data(btc_file)
        print(f"✅ Data loaded successfully")
        print(f"📊 Data shape: {data.shape}")
        print(f"📊 Columns: {list(data.columns)}")
        
    except Exception as e:
        print(f"❌ Failed to load data: {e}")
        return
    
    # Step 3: Data preparation
    print_step(3, "Data Preparation")
    
    try:
        # Create target variable
        print("🎯 Creating target variable...")
        data['target'] = (data['Close'].shift(-1) > data['Close']).astype(int)
        data = data.dropna()
        
        print(f"✅ Target variable created")
        print(f"📊 Final data shape: {data.shape}")
        print(f"📊 Target distribution: {data['target'].value_counts()}")
        
    except Exception as e:
        print(f"❌ Failed in data preparation: {e}")
        return
    
    # Step 4: Simple train/test split
    print_step(4, "Train/Test Split")
    
    try:
        # Simple split (not time series for simplicity)
        train_size = int(0.8 * len(data))
        train_data = data.iloc[:train_size]
        test_data = data.iloc[train_size:]
        
        print(f"✅ Train/test split completed")
        print(f"📊 Train set: {train_data.shape}")
        print(f"📊 Test set: {test_data.shape}")
        
    except Exception as e:
        print(f"❌ Failed in train/test split: {e}")
        return
    
    # Step 5: Model training (without validation data)
    print_step(5, "Model Training")
    
    try:
        print("🚀 Starting model training...")
        print("⏳ This may take a few minutes...")
        
        # Train model without validation data
        model = gluon.train_models(train_data, "target")
        print("✅ Model training completed successfully")
        
    except Exception as e:
        print(f"❌ Failed in model training: {e}")
        print("💡 This might be due to AutoGluon configuration issues")
        return
    
    # Step 6: Model evaluation
    print_step(6, "Model Evaluation")
    
    try:
        # Evaluate model
        evaluation = gluon.evaluate_models(model, test_data, "target")
        print(f"✅ Model evaluation completed")
        print(f"📊 Evaluation results:")
        for metric, value in evaluation.items():
            print(f"  - {metric}: {value:.4f}")
        
    except Exception as e:
        print(f"❌ Failed in model evaluation: {e}")
        return
    
    # Step 7: Make predictions
    print_step(7, "Make Predictions")
    
    try:
        # Make predictions
        predictions = gluon.predict(model, test_data)
        probabilities = gluon.predict_proba(model, test_data)
        
        print(f"✅ Predictions completed")
        print(f"📊 Predictions shape: {predictions.shape}")
        print(f"📊 Probabilities shape: {probabilities.shape}")
        print(f"📊 Sample predictions: {predictions.head()}")
        
    except Exception as e:
        print(f"❌ Failed in making predictions: {e}")
        return
    
    # Step 8: Value scores analysis
    print_step(8, "Value Scores Analysis")
    
    try:
        # Analyze value scores
        value_scores = gluon.analyze_value_scores(predictions, test_data["target"])
        print(f"✅ Value scores analysis completed")
        print(f"📊 Value scores:")
        for metric, value in value_scores.items():
            print(f"  - {metric}: {value}")
        
    except Exception as e:
        print(f"❌ Failed in value scores analysis: {e}")
        return
    
    # Step 9: Model deployment
    print_step(9, "Model Deployment")
    
    try:
        # Export model
        export_dir = "models/btc_simple_demo"
        os.makedirs(export_dir, exist_ok=True)
        
        export_paths = gluon.export_models(model, export_dir)
        print(f"✅ Model exported successfully")
        print(f"📁 Export paths:")
        for key, path in export_paths.items():
            print(f"  - {key}: {path}")
        
    except Exception as e:
        print(f"❌ Failed in model export: {e}")
        return
    
    # Step 10: Summary
    print_section("Workflow Summary")
    
    print("🎉 Simplified workflow demonstration finished!")
    print("\n📊 What we accomplished:")
    print("✅ 1. Initialized AutoGluon integration")
    print("✅ 2. Loaded real trading data (BTCUSD)")
    print("✅ 3. Prepared data for ML")
    print("✅ 4. Created train/test split")
    print("✅ 5. Trained ML model")
    print("✅ 6. Evaluated model performance")
    print("✅ 7. Made predictions")
    print("✅ 8. Analyzed value scores")
    print("✅ 9. Exported model for deployment")
    
    print(f"\n🚀 The AutoGluon integration is working!")
    print(f"📁 Model exported to: {export_dir}")
    if 'evaluation' in locals():
        print(f"📊 Model performance: {evaluation.get('accuracy', 'N/A'):.4f} accuracy")

if __name__ == "__main__":
    main()
