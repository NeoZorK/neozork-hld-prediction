#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Menu Manager for Interactive System

This module handles all menu-related functionality including menu display,
progress tracking, and user interaction.
"""

import sys
from pathlib import Path
from typing import Dict, Any

import pandas as pd
import numpy as np


class MenuManager:
    """Manages menu display and progress tracking."""
    
    def __init__(self):
        """Initialize the menu manager."""
        # Track used submenus for showing green checkmarks
        self.used_menus = {
            'main': {
                'load_data': False,
                'eda_analysis': False,
                'feature_engineering': False,
                'data_visualization': False,
                'model_development': False,
                'testing_validation': False,
                'documentation_help': False,
                'system_configuration': False,
                'menu_status': False
            },
            'eda': {
                'basic_statistics': False,
                'comprehensive_data_quality_check': False,
                'correlation_analysis': False,
                'time_series_analysis': False,
                'feature_importance': False,
                'fix_data_issues': False,
                'generate_html_report': False,
                'restore_from_backup': False,
                'clear_data_backup': False
            },
            'feature_engineering': {
                'generate_all_features': False,
                'proprietary_features': False,
                'technical_indicators': False,
                'statistical_features': False,
                'temporal_features': False,
                'cross_timeframe_features': False,
                'feature_selection': False,
                'feature_summary': False
            },
            'visualization': {
                'price_charts': False,
                'feature_distributions': False,
                'correlation_heatmaps': False,
                'time_series_plots': False,
                'feature_importance_charts': False,
                'export_visualizations': False
            },
            'model_development': {
                'data_preparation': False,
                'feature_engineering_pipeline': False,
                'ml_model_training': False,
                'model_evaluation': False,
                'hyperparameter_tuning': False,
                'model_report': False
            }
        }
    
    def calculate_submenu_completion_percentage(self, menu_category: str) -> int:
        """Calculate completion percentage for a submenu category."""
        if menu_category not in self.used_menus:
            return 0
        
        items = self.used_menus[menu_category]
        if not items:
            return 0
        
        completed_items = sum(1 for item in items.values() if item)
        total_items = len(items)
        
        return round((completed_items / total_items) * 100) if total_items > 0 else 0
    
    def mark_menu_as_used(self, menu_category: str, menu_item: str):
        """Mark a submenu item as successfully used."""
        if menu_category in self.used_menus and menu_item in self.used_menus[menu_category]:
            self.used_menus[menu_category][menu_item] = True
            print(f"✅ {menu_item.replace('_', ' ').title()} marked as completed!")
    
    def reset_menu_status(self, menu_category: str = None):
        """Reset menu status for all or specific category."""
        if menu_category:
            if menu_category in self.used_menus:
                for item in self.used_menus[menu_category]:
                    self.used_menus[menu_category][item] = False
                print(f"🔄 Reset status for {menu_category} menu")
        else:
            for category in self.used_menus:
                for item in self.used_menus[category]:
                    self.used_menus[category][item] = False
            print("🔄 Reset status for all menus")
    
    def show_menu_status(self):
        """Show current menu usage status."""
        print("\n📊 MENU USAGE STATUS")
        print("-" * 30)
        
        for category, items in self.used_menus.items():
            print(f"\n{category.upper().replace('_', ' ')}:")
            used_count = sum(1 for item in items.values() if item)
            total_count = len(items)
            print(f"  Progress: {used_count}/{total_count} items completed")
            
            for item, used in items.items():
                status = "✅" if used else "⏳"
                item_name = item.replace('_', ' ').title()
                print(f"    {status} {item_name}")
    
    def print_main_menu(self, system):
        """Print main menu options with green checkmarks and completion percentages for used items."""
        print("\n📋 MAIN MENU:")
        
        # Load Data
        checkmark = " ✅" if self.used_menus['main']['load_data'] else ""
        print(f"1. 📁 Load Data{checkmark}")
        
        # EDA Analysis
        checkmark = " ✅" if self.used_menus['main']['eda_analysis'] else ""
        eda_percentage = self.calculate_submenu_completion_percentage('eda')
        percentage_text = f" ({eda_percentage}%)" if eda_percentage > 0 else ""
        print(f"2. 🔍 EDA Analysis{checkmark}{percentage_text}")
        
        # Feature Engineering
        checkmark = " ✅" if self.used_menus['main']['feature_engineering'] else ""
        fe_percentage = self.calculate_submenu_completion_percentage('feature_engineering')
        percentage_text = f" ({fe_percentage}%)" if fe_percentage > 0 else ""
        print(f"3. ⚙️  Feature Engineering{checkmark}{percentage_text}")
        
        # Data Visualization
        checkmark = " ✅" if self.used_menus['main']['data_visualization'] else ""
        viz_percentage = self.calculate_submenu_completion_percentage('visualization')
        percentage_text = f" ({viz_percentage}%)" if viz_percentage > 0 else ""
        print(f"4. 📊 Data Visualization{checkmark}{percentage_text}")
        
        # Model Development
        checkmark = " ✅" if self.used_menus['main']['model_development'] else ""
        model_percentage = self.calculate_submenu_completion_percentage('model_development')
        percentage_text = f" ({model_percentage}%)" if model_percentage > 0 else ""
        print(f"5. 📈 Model Development{checkmark}{percentage_text}")
        
        # Testing & Validation
        checkmark = " ✅" if self.used_menus['main']['testing_validation'] else ""
        print(f"6. 🧪 Testing & Validation{checkmark}")
        
        # Documentation & Help
        checkmark = " ✅" if self.used_menus['main']['documentation_help'] else ""
        print(f"7. 📚 Documentation & Help{checkmark}")
        
        # System Configuration
        checkmark = " ✅" if self.used_menus['main']['system_configuration'] else ""
        print(f"8. ⚙️  System Configuration{checkmark}")
        
        # Menu Status
        checkmark = " ✅" if self.used_menus['main']['menu_status'] else ""
        print(f"9. 📊 Menu Status{checkmark}")
        
        print("0. 🚪 Exit")
        print("-" * 50)
        print("💡 Exit or CTRL+C to Exit")
    
    def print_eda_menu(self):
        """Print EDA menu options with green checkmarks for used items."""
        print("\n🔍 EDA ANALYSIS MENU:")
        print("00. 🏠 Main Menu")
        print("0. 🔙 Back to Main Menu")
        
        # Comprehensive Data Quality Check (new enhanced version)
        checkmark = " ✅" if self.used_menus['eda']['comprehensive_data_quality_check'] else ""
        print(f"1. 🧹 Comprehensive Data Quality Check{checkmark}")
        
        # Basic Statistics
        checkmark = " ✅" if self.used_menus['eda']['basic_statistics'] else ""
        print(f"2. 📊 Basic Statistics{checkmark}")
        
        # Correlation Analysis
        checkmark = " ✅" if self.used_menus['eda']['correlation_analysis'] else ""
        print(f"3. 🔗 Correlation Analysis{checkmark}")
        
        # Time Series Analysis
        checkmark = " ✅" if self.used_menus['eda']['time_series_analysis'] else ""
        print(f"4. 📈 Time Series Analysis{checkmark}")
        
        # Feature Importance
        checkmark = " ✅" if self.used_menus['eda']['feature_importance'] else ""
        print(f"5. 🎯 Feature Importance{checkmark}")
        
        # Generate HTML Report
        checkmark = " ✅" if self.used_menus['eda']['generate_html_report'] else ""
        print(f"6. 📋 Generate HTML Report{checkmark}")
        
        # Restore from Backup
        checkmark = " ✅" if self.used_menus['eda']['restore_from_backup'] else ""
        print(f"7. 🔄 Restore from Backup{checkmark}")
        
        # Clear Data Backup
        checkmark = " ✅" if self.used_menus['eda']['clear_data_backup'] else ""
        print(f"8. 🗑️  Clear Data Backup{checkmark}")
        
        print("-" * 50)
        print("💡 Exit or CTRL+C to Exit")
    
    def print_feature_engineering_menu(self):
        """Print Feature Engineering menu options with green checkmarks for used items."""
        print("\n⚙️  FEATURE ENGINEERING MENU:")
        print("00. 🏠 Main Menu")
        print("0. 🔙 Back to Main Menu")
        
        # Generate All Features
        checkmark = " ✅" if self.used_menus['feature_engineering']['generate_all_features'] else ""
        print(f"1. 🚀 Generate All Features{checkmark}")
        
        # Proprietary Features
        checkmark = " ✅" if self.used_menus['feature_engineering']['proprietary_features'] else ""
        print(f"2. 🎯 Proprietary Features (PHLD/Wave){checkmark}")
        
        # Technical Indicators
        checkmark = " ✅" if self.used_menus['feature_engineering']['technical_indicators'] else ""
        print(f"3. 📊 Technical Indicators{checkmark}")
        
        # Statistical Features
        checkmark = " ✅" if self.used_menus['feature_engineering']['statistical_features'] else ""
        print(f"4. 📈 Statistical Features{checkmark}")
        
        # Temporal Features
        checkmark = " ✅" if self.used_menus['feature_engineering']['temporal_features'] else ""
        print(f"5. ⏰ Temporal Features{checkmark}")
        
        # Cross-Timeframe Features
        checkmark = " ✅" if self.used_menus['feature_engineering']['cross_timeframe_features'] else ""
        print(f"6. 🔄 Cross-Timeframe Features{checkmark}")
        
        # Feature Selection
        checkmark = " ✅" if self.used_menus['feature_engineering']['feature_selection'] else ""
        print(f"7. 🎛️  Feature Selection & Optimization{checkmark}")
        
        # Feature Summary
        checkmark = " ✅" if self.used_menus['feature_engineering']['feature_summary'] else ""
        print(f"8. 📋 Feature Summary Report{checkmark}")
        
        print("-" * 50)
        print("💡 Exit or CTRL+C to Exit")
    
    def print_visualization_menu(self):
        """Print visualization menu options with green checkmarks for used items."""
        print("\n📊 DATA VISUALIZATION MENU:")
        print("00. 🏠 Main Menu")
        print("0. 🔙 Back to Main Menu")
        
        # Price Charts
        checkmark = " ✅" if self.used_menus['visualization']['price_charts'] else ""
        print(f"1. 📈 Price Charts (OHLCV){checkmark}")
        
        # Feature Distribution Plots
        checkmark = " ✅" if self.used_menus['visualization']['feature_distributions'] else ""
        print(f"2. 📊 Feature Distribution Plots{checkmark}")
        
        # Correlation Heatmaps
        checkmark = " ✅" if self.used_menus['visualization']['correlation_heatmaps'] else ""
        print(f"3. 🔗 Correlation Heatmaps{checkmark}")
        
        # Time Series Plots
        checkmark = " ✅" if self.used_menus['visualization']['time_series_plots'] else ""
        print(f"4. 📈 Time Series Plots{checkmark}")
        
        # Feature Importance Charts
        checkmark = " ✅" if self.used_menus['visualization']['feature_importance_charts'] else ""
        print(f"5. 🎯 Feature Importance Charts{checkmark}")
        
        # Export Visualizations
        checkmark = " ✅" if self.used_menus['visualization']['export_visualizations'] else ""
        print(f"6. 📋 Export Visualizations{checkmark}")
        
        print("-" * 50)
        print("💡 Exit or CTRL+C to Exit")
    
    def print_model_development_menu(self):
        """Print model development menu options with green checkmarks for used items."""
        print("\n📈 MODEL DEVELOPMENT MENU:")
        print("00. 🏠 Main Menu")
        print("0. 🔙 Back to Main Menu")
        
        # Data Preparation
        checkmark = " ✅" if self.used_menus['model_development']['data_preparation'] else ""
        print(f"1. 🎯 Data Preparation{checkmark}")
        
        # Feature Engineering Pipeline
        checkmark = " ✅" if self.used_menus['model_development']['feature_engineering_pipeline'] else ""
        print(f"2. 🔄 Feature Engineering Pipeline{checkmark}")
        
        # ML Model Training
        checkmark = " ✅" if self.used_menus['model_development']['ml_model_training'] else ""
        print(f"3. 🤖 ML Model Training{checkmark}")
        
        # Model Evaluation
        checkmark = " ✅" if self.used_menus['model_development']['model_evaluation'] else ""
        print(f"4. 📊 Model Evaluation{checkmark}")
        
        # Hyperparameter Tuning
        checkmark = " ✅" if self.used_menus['model_development']['hyperparameter_tuning'] else ""
        print(f"5. 🧪 Hyperparameter Tuning{checkmark}")
        
        # Model Report
        checkmark = " ✅" if self.used_menus['model_development']['model_report'] else ""
        print(f"6. 📋 Model Report{checkmark}")
        
        print("-" * 50)
        print("💡 Exit or CTRL+C to Exit")
    
    def show_help(self):
        """Show help information."""
        print("\n📚 HELP & DOCUMENTATION")
        print("-" * 30)
        print("🔗 Available Resources:")
        print("   • Feature Engineering Guide: docs/ml/feature_engineering_guide.md")
        print("   • EDA Examples: docs/examples/eda-examples.md")
        print("   • Usage Examples: docs/examples/usage-examples.md")
        print("   • ML Module README: src/ml/README.md")
        print("\n🚀 Quick Start:")
        print("   1. Load your data file (CSV, Parquet, etc.)")
        print("   2. Run EDA analysis to understand your data")
        print("   3. Generate features using the Feature Engineering system")
        print("   4. Export results for further analysis")
        print("\n💡 Tips:")
        print("   • Ensure your data has at least 500 rows for optimal feature generation")
        print("   • Use OHLCV (Open, High, Low, Close, Volume) format for best results")
        print("   • The system automatically handles missing values and data validation")
    
    def show_system_info(self, system):
        """Show system information."""
        print("\n⚙️  SYSTEM INFORMATION")
        print("-" * 30)
        print(f"🔧 Python version: {sys.version}")
        print(f"📦 Pandas version: {pd.__version__}")
        print(f"🔢 NumPy version: {np.__version__}")
        print(f"📁 Project root: {Path(__file__).parent.parent.parent}")
        print(f"📊 Current data: {'Loaded' if system.current_data is not None else 'None'}")
        if system.current_data is not None:
            print(f"   Shape: {system.current_data.shape}")
        print(f"📋 Results available: {len(system.current_results)}")
