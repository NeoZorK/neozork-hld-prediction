#!/usr/bin/env python3
"""
Complete AutoGluon Integration Workflow Demo
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
logger = logging.getLogger("workflow_demo")

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
    """Complete workflow demonstration."""
    print_section("AutoGluon Integration Complete Workflow Demo")
    print("Using real data from data/cache/csv_converted/")
    
    # Step 1: Initialize AutoGluon
    print_step(1, "Initialize AutoGluon Integration")
    try:
        gluon = GluonAutoML()
        print("✅ GluonAutoML initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize GluonAutoML: {e}")
        return
    
    # Step 2: Explore available data
    print_step(2, "Explore Available Data")
    data_dir = "data/cache/csv_converted"
    
    if not os.path.exists(data_dir):
        print(f"❌ Data directory not found: {data_dir}")
        return
    
    # List available files
    files = list(Path(data_dir).glob("*.parquet"))
    print(f"📁 Found {len(files)} parquet files")
    
    # Show some examples
    print("\n📊 Sample files:")
    for i, file in enumerate(files[:5]):
        print(f"  {i+1}. {file.name}")
    
    # Step 3: Load data
    print_step(3, "Load Data")
    
    # Let's use BTCUSD D1 data as an example
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
        print(f"📊 Data types:\n{data.dtypes}")
        
        # Show first few rows
        print(f"\n📋 First 5 rows:")
        print(data.head())
        
    except Exception as e:
        print(f"❌ Failed to load data: {e}")
        return
    
    # Step 4: Data exploration and preparation
    print_step(4, "Data Exploration and Preparation")
    
    try:
        # Get basic data summary
        print(f"📊 Data Summary:")
        print(f"  - Shape: {data.shape}")
        print(f"  - Missing values: {data.isnull().sum().sum()}")
        print(f"  - Memory usage: {data.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
        
        # Check for timestamp column
        timestamp_cols = [col for col in data.columns if 'time' in col.lower() or 'date' in col.lower()]
        if timestamp_cols:
            print(f"📅 Timestamp columns found: {timestamp_cols}")
            timestamp_col = timestamp_cols[0]
        else:
            print("⚠️ No timestamp column found, using index")
            timestamp_col = None
        
        # Check for target column (we'll need to create one)
        print("🎯 Creating target variable for demonstration...")
        
        # Create a simple target: price change direction
        if 'close' in data.columns:
            data['target'] = (data['close'].shift(-1) > data['close']).astype(int)
            data = data.dropna()  # Remove rows with NaN target
            print(f"✅ Target variable created: price change direction")
        else:
            print("⚠️ No 'close' column found, using first numeric column")
            numeric_cols = data.select_dtypes(include=[np.number]).columns
            if len(numeric_cols) > 0:
                data['target'] = (data[numeric_cols[0]].shift(-1) > data[numeric_cols[0]]).astype(int)
                data = data.dropna()
                print(f"✅ Target variable created using {numeric_cols[0]}")
            else:
                print("❌ No numeric columns found for target creation")
                return
        
        print(f"📊 Final data shape: {data.shape}")
        print(f"📊 Target distribution: {data['target'].value_counts()}")
        
    except Exception as e:
        print(f"❌ Failed in data preparation: {e}")
        return
    
    # Step 5: Time series split
    print_step(5, "Time Series Split")
    
    try:
        # Create time series split
        train, val, test = gluon.create_time_series_split(data)
        
        print(f"✅ Time series split completed")
        print(f"📊 Train set: {train.shape}")
        print(f"📊 Validation set: {val.shape}")
        print(f"📊 Test set: {test.shape}")
        
        # Check target distribution in each set
        print(f"📊 Train target distribution: {train['target'].value_counts()}")
        print(f"📊 Val target distribution: {val['target'].value_counts()}")
        print(f"📊 Test target distribution: {test['target'].value_counts()}")
        
    except Exception as e:
        print(f"❌ Failed in time series split: {e}")
        return
    
    # Step 6: Model training
    print_step(6, "Model Training")
    
    try:
        print("🚀 Starting model training...")
        print("⏳ This may take a few minutes...")
        
        # Train model
        model = gluon.train_models(train, "target", val)
        print("✅ Model training completed successfully")
        
        # Get model info
        try:
            leaderboard = model.leaderboard()
            print(f"📊 Model leaderboard:")
            print(leaderboard.head())
        except:
            print("📊 Model leaderboard not available")
        
        try:
            importance = model.feature_importance()
            print(f"📊 Top 10 most important features:")
            print(importance.head(10))
        except:
            print("📊 Feature importance not available")
        
    except Exception as e:
        print(f"❌ Failed in model training: {e}")
        print("💡 This might be due to AutoGluon not being fully installed")
        return
    
    # Step 7: Model evaluation
    print_step(7, "Model Evaluation")
    
    try:
        # Evaluate model
        evaluation = gluon.evaluate_models(model, test, "target")
        print(f"✅ Model evaluation completed")
        print(f"📊 Evaluation results:")
        for metric, value in evaluation.items():
            print(f"  - {metric}: {value:.4f}")
        
    except Exception as e:
        print(f"❌ Failed in model evaluation: {e}")
        return
    
    # Step 8: Make predictions
    print_step(8, "Make Predictions")
    
    try:
        # Make predictions
        predictions = gluon.predict(model, test)
        probabilities = gluon.predict_proba(model, test)
        
        print(f"✅ Predictions completed")
        print(f"📊 Predictions shape: {predictions.shape}")
        print(f"📊 Probabilities shape: {probabilities.shape}")
        print(f"📊 Sample predictions: {predictions.head()}")
        print(f"📊 Sample probabilities:\n{probabilities.head()}")
        
    except Exception as e:
        print(f"❌ Failed in making predictions: {e}")
        return
    
    # Step 9: Value scores analysis
    print_step(9, "Value Scores Analysis")
    
    try:
        # Analyze value scores
        value_scores = gluon.analyze_value_scores(predictions, test["target"])
        print(f"✅ Value scores analysis completed")
        print(f"📊 Value scores:")
        for metric, value in value_scores.items():
            print(f"  - {metric}: {value}")
        
    except Exception as e:
        print(f"❌ Failed in value scores analysis: {e}")
        return
    
    # Step 10: Model deployment
    print_step(10, "Model Deployment")
    
    try:
        # Export model
        export_dir = "models/btc_demo"
        os.makedirs(export_dir, exist_ok=True)
        
        export_paths = gluon.export_models(model, export_dir)
        print(f"✅ Model exported successfully")
        print(f"📁 Export paths:")
        for key, path in export_paths.items():
            print(f"  - {key}: {path}")
        
    except Exception as e:
        print(f"❌ Failed in model export: {e}")
        return
    
    # Step 11: Drift monitoring
    print_step(11, "Drift Monitoring")
    
    try:
        # Monitor for drift
        drift_results = gluon.monitor_drift(model, test, train)
        print(f"✅ Drift monitoring completed")
        print(f"📊 Drift results:")
        for feature, result in drift_results.items():
            if isinstance(result, dict):
                print(f"  - {feature}: PSI = {result.get('psi', 'N/A'):.4f}, Drift = {result.get('drift_detected', 'N/A')}")
            else:
                print(f"  - {feature}: {result}")
        
    except Exception as e:
        print(f"❌ Failed in drift monitoring: {e}")
        return
    
    # Step 12: Summary
    print_section("Workflow Summary")
    
    print("🎉 Complete workflow demonstration finished!")
    print("\n📊 What we accomplished:")
    print("✅ 1. Initialized AutoGluon integration")
    print("✅ 2. Explored available data")
    print("✅ 3. Loaded real trading data")
    print("✅ 4. Prepared data for ML")
    print("✅ 5. Created time series split")
    print("✅ 6. Trained ML model")
    print("✅ 7. Evaluated model performance")
    print("✅ 8. Made predictions")
    print("✅ 9. Analyzed value scores")
    print("✅ 10. Exported model for deployment")
    print("✅ 11. Monitored for data drift")
    
    print(f"\n🚀 The AutoGluon integration is ready for production use!")
    print(f"📁 Model exported to: {export_dir}")
    print(f"📊 Model performance: {evaluation.get('accuracy', 'N/A'):.4f} accuracy")

if __name__ == "__main__":
    main()
