#!/usr/bin/env python3
"""
Quick test for AutoGluon integration
Быстрый тест без обучения модели
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


def quick_test(file_path: str):
    """Quick test without model training."""
    
    print("🧪 Quick AutoGluon Test")
    print("=" * 50)
    
    # Check if file exists
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return False
    
    print(f"📁 Testing file: {file_path}")
    
    try:
        # Initialize AutoGluon
        gluon = GluonAutoML()
        print("✅ AutoGluon initialized")
        
        # Load data
        data = gluon.load_data(file_path)
        print(f"✅ Data loaded: {data.shape}")
        
        # Create target variable
        data['target'] = np.where(data['Close'].diff() > 0, 1, 0)
        data = data.dropna(subset=['target'])
        print(f"✅ Target created: {data['target'].value_counts().to_dict()}")
        
        # Create time series split
        train_data, val_data, test_data = gluon.create_time_series_split(data)
        print(f"✅ Split completed: Train={len(train_data)}, Val={len(val_data)}, Test={len(test_data)}")
        
        # Test custom features
        data_with_features = gluon.create_custom_features(data, use_13_features=True)
        print(f"✅ Custom features: {len(data_with_features.columns)} total columns")
        
        print("\n🎯 Quick test completed successfully!")
        print("✅ All basic functionality is working")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False


def main():
    """Main function."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Quick AutoGluon Test")
    parser.add_argument("file_path", help="Path to the data file")
    
    args = parser.parse_args()
    
    success = quick_test(args.file_path)
    
    if success:
        print("\n🚀 AutoGluon integration is working!")
        exit(0)
    else:
        print("\n❌ AutoGluon integration has issues")
        exit(1)


if __name__ == "__main__":
    main()
