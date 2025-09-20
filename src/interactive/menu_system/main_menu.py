# -*- coding: utf-8 -*-
"""
Main Menu System for NeoZork Interactive ML Trading Strategy Development.

This module provides the main interactive menu system with modern, colorful UI
and progress indicators for the comprehensive ML trading strategy development workflow.
"""

import os
import sys
import time
from typing import Dict, Any, Optional, Callable
from pathlib import Path
import colorama
from colorama import Fore, Back, Style, init

# Initialize colorama for cross-platform colored output
init(autoreset=True)

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.common.logger import print_info, print_warning, print_error, print_success, print_debug

class InteractiveMenuSystem:
    """
    Modern interactive menu system with colorful UI and progress indicators.
    
    Features:
    - Colorful modern interface
    - Progress bars with ETA
    - Smooth navigation
    - Error handling
    - Graceful exit
    """
    
    def __init__(self):
        """Initialize the interactive menu system."""
        self.running = True
        self.current_data = None
        self.current_features = None
        self.current_model = None
        
        # Menu configuration
        self.main_menu_items = {
            "1": {"title": "📊 Load Data", "handler": self._load_data_menu},
            "2": {"title": "🔍 EDA Analysis", "handler": self._eda_analysis_menu},
            "3": {"title": "⚙️ Feature Engineering", "handler": self._feature_engineering_menu},
            "4": {"title": "🤖 ML Model Development", "handler": self._ml_development_menu},
            "5": {"title": "📈 Backtesting & Validation", "handler": self._backtesting_menu},
            "6": {"title": "🚀 Deployment & Monitoring", "handler": self._deployment_menu},
            "7": {"title": "📊 Data Visualization", "handler": self._visualization_menu},
            "8": {"title": "⚙️ System Configuration", "handler": self._configuration_menu},
            "9": {"title": "❓ Help & Documentation", "handler": self._help_menu},
            "0": {"title": "🚪 Exit", "handler": self._exit_system}
        }
    
    def run(self):
        """Run the main interactive menu system."""
        self._clear_screen()
        self._show_welcome()
        
        while self.running:
            try:
                self._show_main_menu()
                choice = self._get_user_input("Enter your choice: ")
                
                if choice in self.main_menu_items:
                    handler = self.main_menu_items[choice]["handler"]
                    if handler:
                        handler()
                else:
                    self._show_invalid_choice()
                    
            except KeyboardInterrupt:
                self._exit_system()
            except Exception as e:
                print_error(f"❌ Unexpected error: {e}")
                time.sleep(2)
    
    def _clear_screen(self):
        """Clear the terminal screen."""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def _show_welcome(self):
        """Display welcome message."""
        print(f"\n{Fore.CYAN}{'='*80}")
        print(f"{Fore.YELLOW}🚀 NeoZork Interactive ML Trading Strategy Development System")
        print(f"{Fore.CYAN}{'='*80}")
        print(f"{Fore.GREEN}Welcome to the comprehensive platform for developing profitable trading strategies!")
        print(f"{Fore.BLUE}Features: Data Loading • EDA Analysis • Feature Engineering • ML Development")
        print(f"{Fore.MAGENTA}• Monte Carlo Simulations • Walk Forward Optimization • Real-time Monitoring")
        print(f"{Fore.CYAN}{'='*80}\n")
    
    def _show_main_menu(self):
        """Display the main menu."""
        print(f"\n{Fore.YELLOW}📋 MAIN MENU")
        print(f"{Fore.CYAN}{'─'*50}")
        
        for key, item in self.main_menu_items.items():
            if key == "0":
                print(f"{Fore.RED}{key}. {item['title']}")
            else:
                print(f"{Fore.WHITE}{key}. {item['title']}")
        
        print(f"{Fore.CYAN}{'─'*50}")
        print(f"{Fore.YELLOW}💡 Tip: Press CTRL+C or type 'exit' to quit anytime")
        print(f"{Fore.CYAN}{'─'*50}\n")
    
    def _get_user_input(self, prompt: str) -> str:
        """Get user input with colored prompt."""
        return input(f"{Fore.GREEN}{prompt}{Style.RESET_ALL}").strip()
    
    def _show_invalid_choice(self):
        """Show invalid choice message."""
        print(f"\n{Fore.RED}❌ Invalid choice! Please try again.")
        time.sleep(1)
    
    def _show_progress(self, message: str, progress: float = 0.0, eta: str = ""):
        """Show progress with ETA and percentage."""
        bar_length = 30
        filled_length = int(bar_length * progress)
        bar = "█" * filled_length + "░" * (bar_length - filled_length)
        percentage = int(progress * 100)
        
        if eta:
            print(f"\r{Fore.CYAN}{message} [{bar}] {percentage}% ETA: {eta}", end="", flush=True)
        else:
            print(f"\r{Fore.CYAN}{message} [{bar}] {percentage}%", end="", flush=True)
    
    # Menu handlers (stubs for now)
    def _load_data_menu(self):
        """Handle data loading menu."""
        from .data_loading_menu import DataLoadingMenu
        menu = DataLoadingMenu()
        menu.run()
    
    def _eda_analysis_menu(self):
        """Handle EDA analysis menu."""
        from .eda_menu import EDAMenu
        menu = EDAMenu()
        menu.run()
    
    def _feature_engineering_menu(self):
        """Handle feature engineering menu."""
        from .feature_engineering_menu import FeatureEngineeringMenu
        menu = FeatureEngineeringMenu()
        menu.run()
    
    def _ml_development_menu(self):
        """Handle ML development menu."""
        from .ml_development_menu import MLDevelopmentMenu
        menu = MLDevelopmentMenu()
        menu.run()
    
    def _backtesting_menu(self):
        """Handle backtesting menu."""
        from .backtesting_menu import BacktestingMenu
        menu = BacktestingMenu()
        menu.run()
    
    def _deployment_menu(self):
        """Handle deployment menu."""
        from .deployment_menu import DeploymentMenu
        menu = DeploymentMenu()
        menu.run()
    
    def _visualization_menu(self):
        """Handle visualization menu."""
        print(f"\n{Fore.YELLOW}📊 Data Visualization Menu")
        print(f"{Fore.CYAN}This feature will be implemented in the next phase...")
        time.sleep(2)
    
    def _configuration_menu(self):
        """Handle configuration menu."""
        from .configuration_menu import ConfigurationMenu
        menu = ConfigurationMenu()
        menu.run()
    
    def _help_menu(self):
        """Handle help menu."""
        print(f"\n{Fore.YELLOW}❓ Help & Documentation")
        print(f"{Fore.CYAN}This feature will be implemented in the next phase...")
        time.sleep(2)
    
    def _exit_system(self):
        """Exit the system gracefully."""
        print(f"\n{Fore.YELLOW}👋 Thank you for using NeoZork Interactive System!")
        print(f"{Fore.GREEN}Goodbye! 🚀")
        self.running = False
