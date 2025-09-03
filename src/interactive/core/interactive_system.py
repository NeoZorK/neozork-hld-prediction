# -*- coding: utf-8 -*-
# src/interactive/core/interactive_system.py
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

from ..ui.menu_manager import MenuManager
from ..data.data_manager import DataManager
from ..analysis.analysis_runner import AnalysisRunner
from ..visualization.visualization_manager import VisualizationManager
from ..analysis.feature_engineering_manager import FeatureEngineeringManager


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
        return self.visualization_manager.print_visualization_menu()
    
    def print_data_management_menu(self):
        """Print data management menu options with green checkmarks for used items."""
        return self.data_manager.print_data_management_menu()
    
    def print_analysis_menu(self):
        """Print analysis menu options with green checkmarks for used items."""
        return self.analysis_runner.print_analysis_menu()
    
    def print_feature_engineering_menu(self):
        """Print feature engineering menu options with green checkmarks for used items."""
        return self.feature_engineering_manager.print_feature_engineering_menu()
    
    def run_interactive_loop(self):
        """Main interactive loop."""
        self.print_banner()
        
        while True:
            try:
                self.print_main_menu()
                choice = self.safe_input("\nEnter your choice (or 'q' to quit): ")
                
                if choice is None or choice.lower() in ['q', 'quit', 'exit']:
                    print("\n👋 Goodbye!")
                    break
                
                if not choice.strip():
                    continue
                
                try:
                    choice_num = int(choice)
                    self.menu_manager.handle_main_menu_choice(choice_num, self)
                except ValueError:
                    print(f"❌ Invalid choice: {choice}. Please enter a number.")
                    
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
                self.safe_input("Press Enter to continue...")
    
    def get_system_info(self) -> Dict[str, Any]:
        """Get comprehensive system information."""
        return {
            'system_name': 'NeoZorK HLD Prediction Interactive System',
            'version': '1.0.0',
            'managers': {
                'menu_manager': type(self.menu_manager).__name__,
                'data_manager': type(self.data_manager).__name__,
                'analysis_runner': type(self.analysis_runner).__name__,
                'visualization_manager': type(self.visualization_manager).__name__,
                'feature_engineering_manager': type(self.feature_engineering_manager).__name__,
            },
            'current_data': self.current_data is not None,
            'current_results': len(self.current_results),
            'feature_generator': self.feature_generator is not None
        }
