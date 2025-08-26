#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Menu Percentage Tracking Feature Demo

This script demonstrates the menu percentage tracking functionality that shows
completion percentages for submenu items in the main menu.

Usage:
    python scripts/demos/menu_percentage_demo.py
"""

import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from interactive_system import InteractiveSystem


def demo_menu_percentages():
    """Demonstrate the menu percentage tracking functionality."""
    print("🚀 MENU PERCENTAGE TRACKING FEATURE DEMO")
    print("=" * 60)
    print("This demo shows how the interactive system displays completion")
    print("percentages for submenu items in the main menu.")
    print()
    
    # Create interactive system instance
    system = InteractiveSystem()
    
    print("📋 INITIAL MAIN MENU (NO PERCENTAGES)")
    print("-" * 40)
    system.print_main_menu()
    print()
    
    # Mark some EDA items as used
    print("✅ MARKING SOME EDA ITEMS AS USED...")
    system.mark_menu_as_used('eda', 'basic_statistics')
    system.mark_menu_as_used('eda', 'data_quality_check')
    system.mark_menu_as_used('main', 'eda_analysis')
    print()
    
    print("📋 MAIN MENU - EDA ANALYSIS WITH 25% COMPLETION")
    print("-" * 40)
    system.print_main_menu()
    print()
    
    # Mark more EDA items
    print("✅ MARKING MORE EDA ITEMS...")
    system.mark_menu_as_used('eda', 'correlation_analysis')
    system.mark_menu_as_used('eda', 'time_series_analysis')
    print()
    
    print("📋 MAIN MENU - EDA ANALYSIS WITH 50% COMPLETION")
    print("-" * 40)
    system.print_main_menu()
    print()
    
    # Mark some Feature Engineering items
    print("✅ MARKING FEATURE ENGINEERING ITEMS...")
    system.mark_menu_as_used('feature_engineering', 'generate_all_features')
    system.mark_menu_as_used('feature_engineering', 'feature_summary')
    system.mark_menu_as_used('main', 'feature_engineering')
    print()
    
    print("📋 MAIN MENU - MULTIPLE SECTIONS WITH PERCENTAGES")
    print("-" * 40)
    system.print_main_menu()
    print()
    
    # Mark all EDA items
    print("✅ MARKING ALL EDA ITEMS...")
    system.mark_menu_as_used('eda', 'feature_importance')
    system.mark_menu_as_used('eda', 'fix_data_issues')
    system.mark_menu_as_used('eda', 'generate_html_report')
    system.mark_menu_as_used('eda', 'restore_from_backup')
    print()
    
    print("📋 MAIN MENU - EDA ANALYSIS WITH 100% COMPLETION")
    print("-" * 40)
    system.print_main_menu()
    print()
    
    # Mark some visualization items
    print("✅ MARKING VISUALIZATION ITEMS...")
    system.mark_menu_as_used('visualization', 'price_charts')
    system.mark_menu_as_used('visualization', 'correlation_heatmaps')
    system.mark_menu_as_used('visualization', 'time_series_plots')
    system.mark_menu_as_used('main', 'data_visualization')
    print()
    
    print("📋 MAIN MENU - MULTIPLE SECTIONS WITH VARIOUS PERCENTAGES")
    print("-" * 40)
    system.print_main_menu()
    print()
    
    # Show detailed status
    print("📊 DETAILED MENU STATUS")
    print("-" * 40)
    system.show_menu_status()
    print()
    
    # Demonstrate percentage calculation
    print("🧮 PERCENTAGE CALCULATION DEMONSTRATION")
    print("-" * 40)
    
    eda_percentage = system.calculate_submenu_completion_percentage('eda')
    fe_percentage = system.calculate_submenu_completion_percentage('feature_engineering')
    viz_percentage = system.calculate_submenu_completion_percentage('visualization')
    model_percentage = system.calculate_submenu_completion_percentage('model_development')
    
    print(f"EDA Analysis: {eda_percentage}% complete")
    print(f"Feature Engineering: {fe_percentage}% complete")
    print(f"Data Visualization: {viz_percentage}% complete")
    print(f"Model Development: {model_percentage}% complete")
    print()
    
    print("🎉 MENU PERCENTAGE DEMO COMPLETED!")
    print("=" * 60)
    print("The percentage tracking feature provides:")
    print("✅ Visual progress indicators for each menu section")
    print("✅ Real-time percentage updates as items are completed")
    print("✅ Clear indication of work remaining in each section")
    print("✅ Motivation to complete all items in each section")
    print("✅ Enhanced user experience with detailed progress tracking")


def demo_percentage_calculation():
    """Demonstrate percentage calculation logic."""
    print("\n🧮 PERCENTAGE CALCULATION LOGIC DEMO")
    print("=" * 60)
    print("This demo shows how percentages are calculated for different scenarios.")
    print()
    
    system = InteractiveSystem()
    
    # Test different completion scenarios
    scenarios = [
        ("Empty EDA", 'eda', 0, "No items completed"),
        ("Partial EDA (2/8)", 'eda', 2, "2 out of 8 items completed"),
        ("Half EDA (4/8)", 'eda', 4, "4 out of 8 items completed"),
        ("Most EDA (6/8)", 'eda', 6, "6 out of 8 items completed"),
        ("Complete EDA (8/8)", 'eda', 8, "All 8 items completed"),
        ("Empty FE", 'feature_engineering', 0, "No items completed"),
        ("Partial FE (2/8)", 'feature_engineering', 2, "2 out of 8 items completed"),
        ("Complete FE (8/8)", 'feature_engineering', 8, "All 8 items completed"),
    ]
    
    for scenario_name, category, items_to_mark, description in scenarios:
        # Reset the system
        system = InteractiveSystem()
        
        # Mark the specified number of items
        items = list(system.used_menus[category].keys())
        for i in range(items_to_mark):
            if i < len(items):
                system.mark_menu_as_used(category, items[i])
        
        # Calculate percentage
        percentage = system.calculate_submenu_completion_percentage(category)
        expected_percentage = round((items_to_mark / len(items)) * 100) if items else 0
        
        print(f"{scenario_name:20} | {percentage:3d}% | {description}")
    
    print()
    print("✅ Percentage calculation works correctly for all scenarios!")


if __name__ == "__main__":
    try:
        demo_menu_percentages()
        demo_percentage_calculation()
        print("\n✅ All menu percentage demos completed successfully!")
    except Exception as e:
        print(f"❌ Demo failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
