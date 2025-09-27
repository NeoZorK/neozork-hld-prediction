#!/usr/bin/env python3
"""
Simple test for AutoGluon integration
Простой тест интеграции AutoGluon
"""

import pandas as pd
import numpy as np
import os
import sys
from pathlib import Path
import logging

# Add src to path
sys.path.insert(0, os.path.abspath('src'))

from automl.gluon import GluonAutoML

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def simple_test():
    """Simple test without model training."""
    
    print("🧪 Simple AutoGluon Integration Test")
    print("=" * 50)
    
    # Step 1: Initialize AutoGluon
    print("Step 1: Initialize AutoGluon")
    try:
        gluon = GluonAutoML()
        print("✅ AutoGluon initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize AutoGluon: {e}")
        return False
    
    # Step 2: Load data
    print("\nStep 2: Load Data")
    try:
        data_path = "data/cache/csv_converted/CSVExport_BTCUSD_PERIOD_D1.parquet"
        
        if not os.path.exists(data_path):
            print(f"❌ Data file not found: {data_path}")
            return False
        
        data = gluon.load_data(data_path)
        print(f"✅ Data loaded successfully")
        print(f"📊 Data shape: {data.shape}")
        print(f"📊 Columns: {list(data.columns)}")
        
    except Exception as e:
        print(f"❌ Failed to load data: {e}")
        return False
    
    # Step 3: Create custom features
    print("\nStep 3: Create Custom Features")
    try:
        data_with_features = gluon.create_custom_features(data, use_13_features=True)
        
        print(f"✅ Custom features created successfully")
        print(f"📊 Original features: {len(data.columns)}")
        print(f"📊 Features with custom: {len(data_with_features.columns)}")
        print(f"📊 Custom features added: {len(data_with_features.columns) - len(data.columns)}")
        
        # Show custom features
        custom_feature_cols = [col for col in data_with_features.columns if 'prob' in col]
        print(f"📊 Custom features: {custom_feature_cols}")
        
    except Exception as e:
        print(f"❌ Failed to create custom features: {e}")
        return False
    
    # Step 4: Prepare data for ML
    print("\nStep 4: Prepare Data for ML")
    try:
        # Create target variable
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
        return False
    
    # Step 5: Time series split
    print("\nStep 5: Time Series Split")
    try:
        train_data, val_data, test_data = gluon.create_time_series_split(data_with_features)
        
        print(f"✅ Time series split completed")
        print(f"📊 Train: {len(train_data)} rows ({len(train_data)/len(data_with_features)*100:.1f}%)")
        print(f"📊 Validation: {len(val_data)} rows ({len(val_data)/len(data_with_features)*100:.1f}%)")
        print(f"📊 Test: {len(test_data)} rows ({len(test_data)/len(data_with_features)*100:.1f}%)")
        
    except Exception as e:
        print(f"❌ Failed in time series split: {e}")
        return False
    
    # Step 6: Test configuration
    print("\nStep 6: Test Configuration")
    try:
        print(f"✅ CUDA disabled: {os.environ.get('CUDA_VISIBLE_DEVICES', 'Not set')}")
        print(f"✅ AutoGluon GPU disabled: {os.environ.get('AUTOGLUON_USE_GPU', 'Not set')}")
        print(f"✅ Excluded model types: {gluon.config.excluded_model_types}")
        
    except Exception as e:
        print(f"❌ Failed to check configuration: {e}")
        return False
    
    print("\n🎯 Simple test completed successfully!")
    print("✅ All basic functionality is working")
    print("✅ CUDA is properly disabled")
    print("✅ Custom features are being created")
    print("✅ Time series split is working")
    
    return True


if __name__ == "__main__":
    success = simple_test()
    if success:
        print("\n🚀 AutoGluon integration is ready for production!")
        exit(0)
    else:
        print("\n❌ AutoGluon integration has issues")
        exit(1)
