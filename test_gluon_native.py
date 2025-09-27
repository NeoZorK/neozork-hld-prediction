#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Native testing script for AutoGluon integration.

This script tests the AutoGluon integration without pytest.
"""

import sys
import os
import traceback
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def test_imports():
    """Test that all modules can be imported."""
    print("=== Testing Imports ===")
    
    try:
        from src.automl.gluon.config import GluonConfig, ExperimentConfig, load_gluon_config
        print("✅ Config imports OK")
    except Exception as e:
        print(f"❌ Config imports failed: {e}")
        return False
    
    try:
        from src.automl.gluon.data import UniversalDataLoader, GluonPreprocessor
        print("✅ Data imports OK")
    except Exception as e:
        print(f"❌ Data imports failed: {e}")
        return False
    
    try:
        from src.automl.gluon.utils import GluonLogger, ValueScoreAnalyzer
        print("✅ Utils imports OK")
    except Exception as e:
        print(f"❌ Utils imports failed: {e}")
        return False
    
    try:
        from src.automl.gluon import GluonAutoML
        print("✅ Main GluonAutoML import OK")
    except Exception as e:
        print(f"❌ Main import failed: {e}")
        return False
    
    return True

def test_config_creation():
    """Test configuration creation."""
    print("\n=== Testing Configuration Creation ===")
    
    try:
        from src.automl.gluon.config import GluonConfig, ExperimentConfig
        
        # Test GluonConfig
        config = GluonConfig()
        print(f"✅ GluonConfig created: {config.time_limit}s, {len(config.presets)} presets")
        
        # Test ExperimentConfig
        exp_config = ExperimentConfig()
        print(f"✅ ExperimentConfig created: {exp_config.experiment_name}")
        
        # Test custom config
        custom_config = ExperimentConfig(
            experiment_name="test_experiment",
            target_column="target",
            problem_type="binary"
        )
        print(f"✅ Custom ExperimentConfig created: {custom_config.experiment_name}")
        
        return True
    except Exception as e:
        print(f"❌ Configuration creation failed: {e}")
        traceback.print_exc()
        return False

def test_data_loading():
    """Test data loading functionality."""
    print("\n=== Testing Data Loading ===")
    
    try:
        from src.automl.gluon.data import UniversalDataLoader, GluonPreprocessor
        import pandas as pd
        import numpy as np
        import tempfile
        
        # Create sample data
        np.random.seed(42)
        sample_data = pd.DataFrame({
            'feature_1': np.random.randn(100),
            'feature_2': np.random.randn(100),
            'target': np.random.randn(100)
        })
        sample_data.index = pd.date_range('2023-01-01', periods=100, freq='D')
        
        # Test UniversalDataLoader
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create test files
            parquet_path = Path(temp_dir) / "test.parquet"
            csv_path = Path(temp_dir) / "test.csv"
            json_path = Path(temp_dir) / "test.json"
            
            sample_data.to_parquet(parquet_path)
            sample_data.to_csv(csv_path)
            sample_data.to_json(json_path, orient='records')
            
            # Test loader
            loader = UniversalDataLoader(temp_dir)
            files = loader.discover_data_files()
            print(f"✅ Discovered {len(files)} files")
            
            # Test loading
            parquet_data = loader.load_parquet(parquet_path)
            csv_data = loader.load_csv(csv_path)
            json_data = loader.load_json(json_path)
            
            print(f"✅ Parquet: {len(parquet_data)} rows")
            print(f"✅ CSV: {len(csv_data)} rows")
            print(f"✅ JSON: {len(json_data)} rows")
        
        # Test preprocessor
        preprocessor = GluonPreprocessor()
        prepared_data = preprocessor.prepare_for_gluon(sample_data, 'target')
        print(f"✅ Data prepared: {len(prepared_data)} rows")
        
        # Test time series split
        train, val, test = preprocessor.create_time_series_split(sample_data)
        print(f"✅ Time series split: {len(train)}/{len(val)}/{len(test)}")
        
        # Test data summary
        summary = preprocessor.get_data_summary(sample_data)
        print(f"✅ Data summary: {summary['shape']}")
        
        return True
    except Exception as e:
        print(f"❌ Data loading failed: {e}")
        traceback.print_exc()
        return False

def test_utils():
    """Test utility functions."""
    print("\n=== Testing Utils ===")
    
    try:
        from src.automl.gluon.utils import GluonLogger, ValueScoreAnalyzer
        import pandas as pd
        import numpy as np
        
        # Test logger
        logger = GluonLogger("INFO")
        logger.info("Test log message")
        print("✅ Logger created and working")
        
        # Test value score analyzer
        analyzer = ValueScoreAnalyzer()
        
        # Create sample data
        y_true = pd.Series([1, 0, 1, 0, 1])
        y_pred = pd.Series([0.8, 0.2, 0.9, 0.1, 0.7])
        
        value_scores = analyzer.analyze_predictions(y_true, y_pred)
        print(f"✅ Value scores calculated: {len(value_scores)} metrics")
        
        robustness = analyzer.get_robustness_score(value_scores)
        print(f"✅ Robustness score: {robustness:.3f}")
        
        report = analyzer.generate_report(value_scores)
        print(f"✅ Report generated: {len(report)} characters")
        
        return True
    except Exception as e:
        print(f"❌ Utils failed: {e}")
        traceback.print_exc()
        return False

def test_gluon_automl():
    """Test GluonAutoML initialization."""
    print("\n=== Testing GluonAutoML ===")
    
    try:
        from src.automl.gluon import GluonAutoML
        
        # Test initialization
        experiment_config = {
            'experiment_name': 'test_experiment',
            'target_column': 'target',
            'problem_type': 'binary',
            'time_limit': 60
        }
        
        gluon = GluonAutoML(experiment_config=experiment_config)
        print("✅ GluonAutoML initialized")
        
        # Test data loading
        import pandas as pd
        import numpy as np
        
        sample_data = pd.DataFrame({
            'feature_1': np.random.randn(100),
            'feature_2': np.random.randn(100),
            'target': np.random.choice([0, 1], 100)
        })
        sample_data.index = pd.date_range('2023-01-01', periods=100, freq='D')
        
        # Test time series split
        train, val, test = gluon.create_time_series_split(sample_data)
        print(f"✅ Time series split: {len(train)}/{len(val)}/{len(test)}")
        
        # Test data summary
        summary = gluon.get_data_summary(sample_data)
        print(f"✅ Data summary: {summary['shape']}")
        
        return True
    except Exception as e:
        print(f"❌ GluonAutoML failed: {e}")
        traceback.print_exc()
        return False

def test_examples():
    """Test example scripts."""
    print("\n=== Testing Examples ===")
    
    try:
        # Test basic usage example
        example_path = Path("src/automl/gluon/examples/basic_usage.py")
        if example_path.exists():
            print("✅ Basic usage example exists")
        else:
            print("❌ Basic usage example not found")
            return False
        
        # Test advanced usage example
        example_path = Path("src/automl/gluon/examples/advanced_usage.py")
        if example_path.exists():
            print("✅ Advanced usage example exists")
        else:
            print("❌ Advanced usage example not found")
            return False
        
        return True
    except Exception as e:
        print(f"❌ Examples test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("🚀 Starting Native AutoGluon Integration Tests")
    print("=" * 60)
    
    tests = [
        ("Imports", test_imports),
        ("Configuration", test_config_creation),
        ("Data Loading", test_data_loading),
        ("Utils", test_utils),
        ("GluonAutoML", test_gluon_automl),
        ("Examples", test_examples)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name} PASSED")
            else:
                print(f"❌ {test_name} FAILED")
        except Exception as e:
            print(f"❌ {test_name} FAILED with exception: {e}")
    
    print("\n" + "=" * 60)
    print(f"📊 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! AutoGluon integration is working correctly.")
        return True
    else:
        print("⚠️  Some tests failed. Check the output above for details.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
