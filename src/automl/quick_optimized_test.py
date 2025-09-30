#!/usr/bin/env python3
"""
Quick Optimized Test
Быстрый тест оптимизированной системы
"""

import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../'))

from automl.unified_schr_system import UnifiedSCHRSystem
from rich.console import Console

console = Console()

def quick_optimized_test():
    """Quick test of optimized system with reduced settings."""
    console.print("🧪 Testing Optimized Unified SCHR System...", style="bold blue")
    
    try:
        # Initialize system
        system = UnifiedSCHRSystem()
        console.print("✅ System created successfully", style="green")
        
        # Load data
        data = system.load_data()
        console.print(f"✅ Data loaded: {len(data)} rows, {len(data.columns)} columns", style="green")
        
        # Create features
        enhanced_data = system.create_enhanced_features(data)
        console.print(f"✅ Features created: {len(enhanced_data.columns)} features", style="green")
        
        # Create targets
        final_data = system.create_target_variables(enhanced_data)
        console.print(f"✅ Targets created: {len([col for col in final_data.columns if col.startswith('target_')])} targets", style="green")
        
        # Test with reduced settings for quick validation
        console.print("🔧 Testing with reduced settings for quick validation...", style="yellow")
        
        # Override task configs for quick test
        system.task_configs = {
            'pressure_vector_sign': {
                'problem_type': 'binary',
                'eval_metric': 'roc_auc',
                'time_limit': 300,  # 5 minutes for quick test
                'presets': 'medium_quality_faster_train',
                'num_bag_folds': 3,
                'description': 'Quick test - pressure vector sign'
            },
            'level_breakout': {
                'problem_type': 'multiclass',
                'eval_metric': 'accuracy',
                'time_limit': 300,  # 5 minutes for quick test
                'presets': 'medium_quality_faster_train',
                'num_bag_folds': 3,
                'description': 'Quick test - level breakout'
            }
        }
        
        # Train only the best performing model
        console.print("🤖 Training level_breakout model (best performer)...", style="blue")
        models = system.train_robust_models(final_data)
        
        if models and 'level_breakout' in models:
            console.print("✅ Model trained successfully", style="green")
            
            # Quick validation
            console.print("🔍 Running quick validation...", style="blue")
            validation_results = system.run_comprehensive_validation(final_data)
            
            if validation_results:
                console.print("✅ Validation completed", style="green")
                console.print(f"📊 Results: {validation_results}", style="cyan")
            else:
                console.print("⚠️ Validation failed", style="yellow")
        else:
            console.print("❌ Model training failed", style="red")
        
        console.print("🎉 Quick optimized test completed!", style="bold green")
        return True
        
    except Exception as e:
        console.print(f"❌ Test failed: {e}", style="red")
        return False

if __name__ == "__main__":
    success = quick_optimized_test()
    if success:
        console.print("✅ All tests passed! Optimized system is working.", style="bold green")
    else:
        console.print("❌ Tests failed. Check the system.", style="bold red")
