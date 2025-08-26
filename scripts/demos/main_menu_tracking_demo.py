#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Main Menu Tracking Feature Demo

This script demonstrates the main menu tracking functionality with green checkmarks
in the interactive system. It shows how main menu items are marked as used and how
the visual feedback works.

Usage:
    python scripts/demos/main_menu_tracking_demo.py
"""

import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from interactive_system import InteractiveSystem


def demo_main_menu_tracking():
    """Demonstrate the main menu tracking functionality."""
    print("🚀 MAIN MENU TRACKING FEATURE DEMO")
    print("=" * 50)
    print("This demo shows how the interactive system tracks main menu usage")
    print("with green checkmarks (✅) for completed items.")
    print()
    
    # Create interactive system instance
    system = InteractiveSystem()
    
    print("📋 INITIAL MAIN MENU STATUS")
    print("-" * 30)
    system.show_menu_status()
    print()
    
    print("📋 MAIN MENU - BEFORE MARKING")
    print("-" * 30)
    system.print_main_menu()
    print()
    
    # Mark some main menu items as used
    print("✅ MARKING SOME MAIN MENU ITEMS AS USED...")
    system.mark_menu_as_used('main', 'load_data')
    system.mark_menu_as_used('main', 'eda_analysis')
    system.mark_menu_as_used('main', 'feature_engineering')
    system.mark_menu_as_used('main', 'data_visualization')
    print()
    
    print("📋 MAIN MENU - AFTER MARKING")
    print("-" * 30)
    system.print_main_menu()
    print()
    
    # Mark more items
    print("✅ MARKING MORE MAIN MENU ITEMS...")
    system.mark_menu_as_used('main', 'model_development')
    system.mark_menu_as_used('main', 'documentation_help')
    system.mark_menu_as_used('main', 'menu_status')
    print()
    
    print("📋 MAIN MENU - WITH MORE ITEMS MARKED")
    print("-" * 30)
    system.print_main_menu()
    print()
    
    print("📊 UPDATED MENU STATUS")
    print("-" * 30)
    system.show_menu_status()
    print()
    
    # Demonstrate reset functionality
    print("🔄 DEMONSTRATING RESET FUNCTIONALITY")
    print("-" * 30)
    print("Resetting main menu status...")
    system.reset_menu_status('main')
    print()
    
    print("📋 MAIN MENU - AFTER RESET")
    print("-" * 30)
    system.print_main_menu()
    print()
    
    print("📊 STATUS AFTER MAIN MENU RESET")
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
    
    print("🎉 MAIN MENU TRACKING DEMO COMPLETED!")
    print("=" * 50)
    print("The main menu tracking feature provides:")
    print("✅ Visual feedback on completed main menu items")
    print("✅ Session persistence of main menu progress")
    print("✅ Easy progress tracking across all menu levels")
    print("✅ Reset capabilities for testing")
    print("✅ Enhanced user experience for navigation")


def demo_combined_menu_tracking():
    """Demonstrate combined main and submenu tracking."""
    print("\n🔄 COMBINED MENU TRACKING DEMO")
    print("=" * 50)
    print("This demo shows how main menu and submenu tracking work together.")
    print()
    
    system = InteractiveSystem()
    
    print("📋 MARKING MAIN MENU ITEMS...")
    system.mark_menu_as_used('main', 'load_data')
    system.mark_menu_as_used('main', 'eda_analysis')
    system.mark_menu_as_used('main', 'feature_engineering')
    print()
    
    print("📋 MARKING SUBMENU ITEMS...")
    system.mark_menu_as_used('eda', 'basic_statistics')
    system.mark_menu_as_used('eda', 'data_quality_check')
    system.mark_menu_as_used('feature_engineering', 'generate_all_features')
    print()
    
    print("📋 MAIN MENU WITH CHECKMARKS")
    print("-" * 30)
    system.print_main_menu()
    print()
    
    print("🔍 EDA MENU WITH CHECKMARKS")
    print("-" * 30)
    system.print_eda_menu()
    print()
    
    print("⚙️  FEATURE ENGINEERING MENU WITH CHECKMARKS")
    print("-" * 30)
    system.print_feature_engineering_menu()
    print()
    
    print("📊 COMPLETE MENU STATUS")
    print("-" * 30)
    system.show_menu_status()
    print()
    
    print("✅ Combined tracking demonstrates:")
    print("   • Main menu items show overall progress")
    print("   • Submenu items show detailed progress")
    print("   • Both levels work together seamlessly")
    print("   • Users can track progress at multiple levels")


if __name__ == "__main__":
    try:
        demo_main_menu_tracking()
        demo_combined_menu_tracking()
        print("\n✅ All main menu tracking demos completed successfully!")
    except Exception as e:
        print(f"❌ Demo failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
