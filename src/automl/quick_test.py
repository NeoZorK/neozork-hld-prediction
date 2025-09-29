#!/usr/bin/env python3
"""
Quick Test for Unified SCHR System
Быстрый тест единой системы
"""

import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../'))

from automl.unified_schr_system import UnifiedSCHRSystem
from rich.console import Console

console = Console()

def quick_test():
    """Quick test with minimal training time."""
    
    console.print("🧪 Quick Test of Unified SCHR System...", style="bold blue")
    
    try:
        # Create system
        system = UnifiedSCHRSystem()
        
        # Load data
        data = system.load_data("BTCUSD", "MN1")
        console.print(f"✅ Data loaded: {len(data)} rows", style="green")
        
        # Create features
        features = system.create_enhanced_features(data)
        console.print(f"✅ Features created: {len(features.columns)} features", style="green")
        
        # Create targets
        targets = system.create_target_variables(features)
        console.print(f"✅ Targets created: {len([col for col in targets.columns if col.startswith('target_')])} targets", style="green")
        
        # Show target columns
        target_cols = [col for col in targets.columns if col.startswith('target_')]
        console.print(f"Target columns: {target_cols}", style="cyan")
        
        # Quick training with minimal time
        console.print("🤖 Quick training (2 minutes per model)...", style="blue")
        
        # Override time limits for quick test
        original_configs = system.task_configs.copy()
        for task in system.task_configs:
            system.task_configs[task]['time_limit'] = 120  # 2 minutes
        
        # Train only one model for quick test
        test_data = targets.dropna(subset=['target_price_direction_1period'])
        if len(test_data) > 50:
            console.print("🎯 Training price_direction_1period model...", style="blue")
            
            # Simple training
            from autogluon.tabular import TabularPredictor
            import tempfile
            import shutil
            
            with tempfile.TemporaryDirectory() as temp_dir:
                predictor = TabularPredictor(
                    label='target_price_direction_1period',
                    problem_type='multiclass',
                    eval_metric='accuracy',
                    path=temp_dir
                )
                
                # Quick training
                predictor.fit(
                    test_data,
                    time_limit=120,
                    presets='medium_quality_faster_train',
                    excluded_model_types=['NN_TORCH', 'NN_FASTAI', 'FASTAI', 'NeuralNetFastAI'],
                    verbosity=0
                )
                
                # Test prediction
                predictions = predictor.predict(test_data.tail(10))
                console.print(f"✅ Model trained successfully!", style="green")
                console.print(f"Sample predictions: {predictions.tolist()}", style="cyan")
        
        console.print("🎉 Quick test completed successfully!", style="bold green")
        
    except Exception as e:
        console.print(f"❌ Quick test failed: {e}", style="red")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    quick_test()
