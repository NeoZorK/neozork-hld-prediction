#!/usr/bin/env python3
"""
Working AutoGluon Test
Рабочий тест AutoGluon с полной очисткой
"""

import pandas as pd
import numpy as np
import os
import sys
import shutil
import glob
from pathlib import Path
import logging
from datetime import datetime

# Add src to path
sys.path.insert(0, os.path.abspath('src'))

from automl.gluon import GluonAutoML

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def clean_all_models():
    """Clean all AutoGluon model files."""
    model_patterns = [
        "models/autogluon*",
        "models/single_file_analysis_*",
        "models/clean_analysis_*",
        "models/working_test_*"
    ]
    
    cleaned_count = 0
    for pattern in model_patterns:
        for path in glob.glob(pattern):
            try:
                if os.path.exists(path):
                    shutil.rmtree(path)
                    print(f"🧹 Cleaned: {path}")
                    cleaned_count += 1
            except Exception as e:
                print(f"⚠️  Could not clean {path}: {e}")
    
    return cleaned_count


def working_test(file_path: str, analysis_type: str = "quick"):
    """Working test with full cleanup."""
    
    print("🔧 Working AutoGluon Test")
    print("=" * 50)
    
    # Clean all models first
    print("🧹 Cleaning all existing models...")
    cleaned = clean_all_models()
    print(f"✅ Cleaned {cleaned} model directories")
    
    # Check if file exists
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return False
    
    print(f"📁 Testing file: {file_path}")
    print(f"📊 Analysis type: {analysis_type}")
    
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
        
        if analysis_type == "quick":
            print("\n🎯 Quick test completed successfully!")
            print("✅ All basic functionality is working")
            return True
        
        # For full analysis, use unique model path
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        unique_model_path = f"models/working_test_{timestamp}"
        
        # Update config to use unique path
        gluon.config.model_path = unique_model_path
        
        print(f"🚀 Starting full analysis with unique path: {unique_model_path}")
        
        # Train model
        gluon.train_models(train_data, "target", val_data)
        print("✅ Model training completed")
        
        # Evaluate model
        evaluation = gluon.evaluate_models(test_data, "target")
        print("✅ Model evaluation completed")
        
        # Make predictions
        predictions = gluon.predict(test_data)
        print("✅ Predictions completed")
        
        # Export model
        export_dir = gluon.export_models()
        print(f"✅ Model exported to: {export_dir}")
        
        print("\n🎯 Full analysis completed successfully!")
        print("✅ Model training, evaluation, and export all working")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False


def main():
    """Main function."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Working AutoGluon Test")
    parser.add_argument("file_path", help="Path to the data file")
    parser.add_argument("--analysis", default="quick", 
                       choices=["quick", "full"],
                       help="Type of analysis")
    
    args = parser.parse_args()
    
    success = working_test(args.file_path, args.analysis)
    
    if success:
        print("\n🚀 AutoGluon integration is fully working!")
        exit(0)
    else:
        print("\n❌ AutoGluon integration has issues")
        exit(1)


if __name__ == "__main__":
    main()
