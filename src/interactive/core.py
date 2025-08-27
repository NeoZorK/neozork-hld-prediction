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
        self.analysis_runner = AnalysisRunner()
        self.visualization_manager = VisualizationManager()
        self.feature_engineering_manager = FeatureEngineeringManager()
        
        # Core state
        self.current_data = None
        self.current_results = {}
        self.feature_generator = None
    
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
    
    def load_data(self) -> bool:
        """Load data using the data manager."""
        return self.data_manager.load_data(self)
    
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
            elif choice == '0':
                print("\n👋 Thank you for using NeoZorK HLD Prediction Interactive System!")
                print("   Goodbye!")
                break
            else:
                print("❌ Invalid choice. Please select 0-9.")
            
            if choice != '0':
                if self.safe_input() is None:
                    break
