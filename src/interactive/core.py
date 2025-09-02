#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Core Interactive System for NeoZorK HLD Prediction

This module contains the main InteractiveSystem class that orchestrates
all interactive functionality.
"""

import sys
import time
from pathlib import Path
from typing import Dict, Any, Optional

import pandas as pd
import numpy as np

from .menu_manager import MenuManager
from .data_manager import DataManager
from .analysis_runner import AnalysisRunner
from .visualization_manager import VisualizationManager
from .feature_engineering_manager import FeatureEngineeringManager


class InteractiveSystem:
    """Interactive system interface for NeoZorK HLD Prediction."""
    
    def __init__(self):
        """Initialize the interactive system."""
        # Initialize managers
        self.menu_manager = MenuManager()
        self.data_manager = DataManager()
        self.analysis_runner = AnalysisRunner(self)
        self.visualization_manager = VisualizationManager()
        self.feature_engineering_manager = FeatureEngineeringManager()
        
        # Core state
        self.current_data = None
        self.current_results = {}
        self.feature_generator = None
        
        # For backward compatibility with tests
        self.used_menus = self.menu_manager.used_menus
    
    def print_banner(self):
        """Print system banner."""
        print("\n" + "="*80)
        print("🚀 NEOZORk HLD PREDICTION - INTERACTIVE SYSTEM")
        print("="*80)
        print("🎯 Advanced Feature Engineering & EDA Platform")
        print("🔧 ML-Ready Trading System Development")
        print("📊 Comprehensive Data Analysis & Visualization")
        print("="*80)
    
    def safe_input(self, prompt="\nPress Enter to continue..."):
        """Safely handle input with EOF protection."""
        try:
            return input(prompt)
        except EOFError:
            print("\n👋 Goodbye!")
            return None
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            return None
    
    # Menu management methods for backward compatibility
    def calculate_submenu_completion_percentage(self, menu_category: str) -> int:
        """Calculate completion percentage for a submenu category."""
        return self.menu_manager.calculate_submenu_completion_percentage(menu_category)
    
    def mark_menu_as_used(self, menu_category: str, menu_item: str):
        """Mark a submenu item as successfully used."""
        return self.menu_manager.mark_menu_as_used(menu_category, menu_item)
    
    def reset_menu_status(self, menu_category: str = None):
        """Reset menu status for all or specific category."""
        return self.menu_manager.reset_menu_status(menu_category)
    
    def show_menu_status(self):
        """Show current menu usage status."""
        return self.menu_manager.show_menu_status()
    
    def print_main_menu(self, system=None):
        """Print main menu options with green checkmarks and completion percentages for used items."""
        if system is None:
            system = self
        return self.menu_manager.print_main_menu(system)
    
    def print_eda_menu(self):
        """Print EDA menu options with green checkmarks for used items."""
        return self.menu_manager.print_eda_menu()
    
    def print_feature_engineering_menu(self):
        """Print Feature Engineering menu options with green checkmarks for used items."""
        return self.menu_manager.print_feature_engineering_menu()
    
    def print_visualization_menu(self):
        """Print visualization menu options with green checkmarks for used items."""
        return self.menu_manager.print_visualization_menu()
    
    def print_model_development_menu(self):
        """Print model development menu options with green checkmarks for used items."""
        return self.menu_manager.print_model_development_menu()
    
    # Data management methods for backward compatibility
    def load_data_from_file(self, file_path: str) -> pd.DataFrame:
        """Load data from file path."""
        return self.data_manager.load_data_from_file(file_path)
    
    def load_data_from_folder(self, folder_path: str) -> list:
        """Load data files from folder path."""
        return self.data_manager.load_data_from_folder(folder_path)
    
    def load_data(self) -> bool:
        """Load data using the data manager."""
        return self.data_manager.load_data(self)
    
    # Analysis methods for backward compatibility
    def run_basic_statistics(self):
        """Run comprehensive basic statistical analysis."""
        return self.analysis_runner.run_basic_statistics(self)
    

    
    def run_comprehensive_data_quality_check(self):
        """Run comprehensive data quality check using eda_batch_check functionality."""
        return self.analysis_runner.run_comprehensive_data_quality_check(self)
    
    def run_data_quality_check(self):
        """Run data quality check (alias for comprehensive data quality check)."""
        return self.analysis_runner.run_comprehensive_data_quality_check(self)
    
    def run_correlation_analysis(self):
        """Run correlation analysis."""
        return self.analysis_runner.run_correlation_analysis(self)
    
    def run_time_series_analysis(self):
        """Run time series analysis."""
        return self.analysis_runner.run_time_series_analysis(self)
    
    def run_outlier_detection(self):
        """Run outlier detection analysis."""
        return self.analysis_runner.run_outlier_detection(self)
    
    def fix_data_issues(self):
        """Fix common data quality issues in the current dataset."""
        # Get data quality summaries first
        if hasattr(self, 'current_data') and self.current_data is not None:
            from .eda_analyzer import EDAAnalyzer
            eda_analyzer = EDAAnalyzer()
            nan_summary, dupe_summary, gap_summary = eda_analyzer.run_comprehensive_data_quality_check(self)
            return self.analysis_runner.fix_data_issues(self, nan_summary, dupe_summary, gap_summary)
        else:
            print("❌ No data loaded. Please load data first.")
            return False
    
    def fix_all_data_issues(self):
        """Fix all data issues."""
        # Get data quality summaries first
        if hasattr(self, 'current_data') and self.current_data is not None:
            from .eda_analyzer import EDAAnalyzer
            eda_analyzer = EDAAnalyzer()
            nan_summary, dupe_summary, gap_summary = eda_analyzer.run_comprehensive_data_quality_check(self)
            return self.analysis_runner.fix_data_issues(self, nan_summary, dupe_summary, gap_summary)
        else:
            print("❌ No data loaded. Please load data first.")
            return False
    
    def generate_html_report(self):
        """Generate comprehensive HTML report for current data and analysis."""
        return self.analysis_runner.generate_html_report(self)
    
    def restore_from_backup(self):
        """Restore data from backup file."""
        return self.data_manager.restore_from_backup(self)
    
    def clear_data_backup(self):
        """Clear all backup files from the backup directory."""
        return self.data_manager.clear_data_backup(self)
    
    def _create_statistics_plots(self, data=None):
        """Create statistics plots using visualization manager."""
        return self.visualization_manager.create_statistics_plots(self, data)
    
    def _show_plots_in_browser(self):
        """Show plots in browser using visualization manager."""
        return self.visualization_manager.show_plots_in_browser(self)
    
    def run_eda_analysis(self):
        """Run EDA analysis using the analysis runner."""
        self.analysis_runner.run_eda_analysis(self)
    
    def run_feature_engineering_analysis(self):
        """Run Feature Engineering analysis using the feature engineering manager."""
        self.feature_engineering_manager.run_feature_engineering_analysis(self)
    
    def run_visualization_analysis(self):
        """Run visualization analysis using the visualization manager."""
        self.visualization_manager.run_visualization_analysis(self)
    
    def run_model_development(self):
        """Run model development using the analysis runner."""
        self.analysis_runner.run_model_development(self)
    
    # Feature engineering methods for backward compatibility
    def generate_all_features(self):
        """Generate all features."""
        return self.feature_engineering_manager.generate_all_features(self)
    
    def show_feature_summary(self):
        """Show feature summary."""
        return self.feature_engineering_manager.show_feature_summary(self)
    
    def show_help(self):
        """Show help information."""
        self.menu_manager.show_help()
        self.safe_input()
    
    def show_system_info(self):
        """Show system information."""
        self.menu_manager.show_system_info(self)
        self.safe_input()
    
    def export_results(self):
        """Export current results to files."""
        self.data_manager.export_results(self)
    
    def run(self):
        """Run the interactive system."""
        self.print_banner()
        
        while True:
            self.menu_manager.print_main_menu(self)
            try:
                choice = input("Select option (0-9): ").strip()
            except EOFError:
                print("\n👋 Goodbye!")
                break
            
            # Handle exit commands
            if choice.lower() in ['exit', 'quit', 'q']:
                print("\n👋 Thank you for using NeoZorK HLD Prediction Interactive System!")
                print("   Goodbye!")
                break
            
            if choice == '1':
                self.load_data()
                self.menu_manager.mark_menu_as_used('main', 'load_data')
            elif choice == '2':
                self.run_eda_analysis()
                self.menu_manager.mark_menu_as_used('main', 'eda_analysis')
            elif choice == '3':
                self.run_feature_engineering_analysis()
                self.menu_manager.mark_menu_as_used('main', 'feature_engineering')
            elif choice == '4':
                self.run_visualization_analysis()
                self.menu_manager.mark_menu_as_used('main', 'data_visualization')
            elif choice == '5':
                self.run_model_development()
                self.menu_manager.mark_menu_as_used('main', 'model_development')
            elif choice == '6':
                print("⏳ Testing & Validation - Coming soon!")
                self.menu_manager.mark_menu_as_used('main', 'testing_validation')
            elif choice == '7':
                self.show_help()
                self.menu_manager.mark_menu_as_used('main', 'documentation_help')
            elif choice == '8':
                self.show_system_info()
                self.menu_manager.mark_menu_as_used('main', 'system_configuration')
            elif choice == '9':
                self.menu_manager.show_menu_status()
                self.menu_manager.mark_menu_as_used('main', 'menu_status')
            elif choice == '0' or choice == '00':
                print("\n👋 Thank you for using NeoZorK HLD Prediction Interactive System!")
                print("   Goodbye!")
                break
            else:
                print("❌ Invalid choice. Please select 0-9.")
            
            if choice not in ['0', '00']:
                try:
                    if self.safe_input() is None:
                        break
                except EOFError:
                    print("\n👋 Goodbye!")
                    break
