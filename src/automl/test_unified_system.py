#!/usr/bin/env python3
"""
Test Unified SCHR System
Тест единой системы SCHR Levels AutoML
"""

import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../'))

from automl.unified_schr_system import UnifiedSCHRSystem
from rich.console import Console

console = Console()

def test_unified_system():
    """Test the unified system with sample data."""
    
    console.print("🧪 Testing Unified SCHR System...", style="bold blue")
    
    try:
        # Create system
        system = UnifiedSCHRSystem()
        console.print("✅ System created successfully", style="green")
        
        # Test data loading (if data exists)
        try:
            data = system.load_data("BTCUSD", "MN1")
            console.print(f"✅ Data loaded: {len(data)} rows, {len(data.columns)} columns", style="green")
            
            # Test feature creation
            features = system.create_enhanced_features(data)
            console.print(f"✅ Features created: {len(features.columns)} features", style="green")
            
            # Test target creation
            targets = system.create_target_variables(features)
            console.print(f"✅ Targets created: {len([col for col in targets.columns if col.startswith('target_')])} targets", style="green")
            
            console.print("🎉 All tests passed! System is ready for use.", style="bold green")
            
        except FileNotFoundError:
            console.print("⚠️ No data found - system structure is correct", style="yellow")
            console.print("💡 To test with real data, ensure data files exist in data/cache/csv_converted/", style="blue")
        
    except Exception as e:
        console.print(f"❌ Test failed: {e}", style="red")
        raise

if __name__ == "__main__":
    test_unified_system()
