#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Menu Tracking Feature Demo

This script demonstrates the new menu tracking functionality with green checkmarks
in the interactive system. It shows how menu items are marked as used and how
the visual feedback works.

Usage:
    python scripts/demos/menu_tracking_demo.py
"""

import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from interactive_system import InteractiveSystem


def demo_menu_tracking():
    """Demonstrate the menu tracking functionality."""
    print("🚀 MENU TRACKING FEATURE DEMO")
    print("=" * 50)
    print("This demo shows how the interactive system tracks menu usage")
    print("with green checkmarks (✅) for completed items.")
    print()
    
    # Create interactive system instance
    system = InteractiveSystem()
    
    print("📋 INITIAL MENU STATUS")
    print("-" * 30)
    system.show_menu_status()
    print()
    
    print("🔍 EDA MENU - BEFORE MARKING")
    print("-" * 30)
    system.print_eda_menu()
    print()
    
    # Mark some EDA items as used
    print("✅ MARKING SOME EDA ITEMS AS USED...")
    system.mark_menu_as_used('eda', 'basic_statistics')
    system.mark_menu_as_used('eda', 'data_quality_check')
    system.mark_menu_as_used('eda', 'correlation_analysis')
    print()
    
    print("🔍 EDA MENU - AFTER MARKING")
    print("-" * 30)
    system.print_eda_menu()
    print()
    
    # Mark some Feature Engineering items
    print("✅ MARKING FEATURE ENGINEERING ITEMS...")
    system.mark_menu_as_used('feature_engineering', 'generate_all_features')
    system.mark_menu_as_used('feature_engineering', 'feature_summary')
    print()
    
    print("⚙️  FEATURE ENGINEERING MENU")
    print("-" * 30)
    system.print_feature_engineering_menu()
    print()
    
    # Mark some visualization items
    print("✅ MARKING VISUALIZATION ITEMS...")
    system.mark_menu_as_used('visualization', 'price_charts')
    system.mark_menu_as_used('visualization', 'correlation_heatmaps')
    print()
    
    print("📊 VISUALIZATION MENU")
    print("-" * 30)
    system.print_visualization_menu()
    print()
    
    # Mark some model development items
    print("✅ MARKING MODEL DEVELOPMENT ITEMS...")
    system.mark_menu_as_used('model_development', 'data_preparation')
    system.mark_menu_as_used('model_development', 'ml_model_training')
    print()
    
    print("📈 MODEL DEVELOPMENT MENU")
    print("-" * 30)
    system.print_model_development_menu()
    print()
    
    print("📊 UPDATED MENU STATUS")
    print("-" * 30)
    system.show_menu_status()
    print()
    
    # Demonstrate reset functionality
    print("🔄 DEMONSTRATING RESET FUNCTIONALITY")
    print("-" * 30)
    print("Resetting EDA menu status...")
    system.reset_menu_status('eda')
    print()
    
    print("🔍 EDA MENU - AFTER RESET")
    print("-" * 30)
    system.print_eda_menu()
    print()
    
    print("📊 STATUS AFTER EDA RESET")
    print("-" * 30)
    system.show_menu_status()
    print()
    
    # Demonstrate full reset
    print("🔄 RESETTING ALL MENUS...")
    system.reset_menu_status()
    print()
    
    print("📊 FINAL STATUS (ALL RESET)")
    print("-" * 30)
    system.show_menu_status()
    print()
    
    print("🎉 DEMO COMPLETED!")
    print("=" * 50)
    print("The menu tracking feature provides:")
    print("✅ Visual feedback on completed items")
    print("✅ Session persistence of progress")
    print("✅ Easy progress tracking")
    print("✅ Reset capabilities for testing")
    print("✅ Enhanced user experience")


def demo_error_handling():
    """Demonstrate error handling in menu tracking."""
    print("\n🛡️  ERROR HANDLING DEMO")
    print("=" * 50)
    
    system = InteractiveSystem()
    
    print("Testing invalid menu category...")
    system.mark_menu_as_used('invalid_category', 'some_item')
    
    print("Testing invalid menu item...")
    system.mark_menu_as_used('eda', 'invalid_item')
    
    print("Testing reset with invalid category...")
    system.reset_menu_status('invalid_category')
    
    print("✅ Error handling works correctly - no crashes!")


if __name__ == "__main__":
    try:
        demo_menu_tracking()
        demo_error_handling()
        print("\n✅ All demos completed successfully!")
    except Exception as e:
        print(f"❌ Demo failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
