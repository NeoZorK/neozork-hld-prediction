# -*- coding: utf-8 -*-
"""
Base Menu class for NeoZork Interactive ML Trading Strategy Development.

This module provides the base functionality for all menu classes.
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
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.common.logger import print_info, print_warning, print_error, print_success, print_debug

class BaseMenu:
    """
    Base class for all menu implementations.
    
    Provides common functionality for:
    - Menu display
    - User input handling
    - Progress indicators
    - Error handling
    """
    
    def __init__(self):
        """Initialize the base menu."""
        self.running = True
        self.menu_items = {}
    
    def run(self):
        """Run the menu system."""
        while self.running:
            try:
                self.show_menu()
                choice = self._get_user_input("Enter your choice: ")
                
                if choice in self.menu_items:
                    handler = self.menu_items[choice]["handler"]
                    if handler:
                        handler()
                    elif choice == "0":
                        break
                else:
                    self._show_invalid_choice()
                    
            except KeyboardInterrupt:
                self._exit_system()
            except Exception as e:
                print_error(f"❌ Unexpected error: {e}")
                time.sleep(2)
    
    def show_menu(self):
        """Display the menu. Must be implemented by subclasses."""
        raise NotImplementedError("Subclasses must implement show_menu method")
    
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
    
    def _exit_system(self):
        """Exit the system gracefully."""
        print(f"\n{Fore.YELLOW}👋 Thank you for using NeoZork Interactive System!")
        print(f"{Fore.GREEN}Goodbye! 🚀")
        self.running = False
        sys.exit(0)
