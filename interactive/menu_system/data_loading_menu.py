# -*- coding: utf-8 -*-
"""
Data Loading Menu for NeoZork Interactive ML Trading Strategy Development.

This module provides the data loading submenu with support for multiple data sources.
"""

from typing import Dict, Any, Optional
from .base_menu import BaseMenu

class DataLoadingMenu(BaseMenu):
    """
    Data loading submenu with support for multiple data sources.
    
    Features:
    - CSV converted data loading
    - Raw parquet data loading
    - Indicators data loading
    - Cleaned data loading
    - Progress tracking with ETA
    """
    
    def __init__(self):
        """Initialize the data loading menu."""
        super().__init__()
        self.menu_items = {
            "1": {"title": "📁 CSV Converted (.parquet)", "handler": self._load_csv_converted},
            "2": {"title": "📊 Raw Parquet", "handler": self._load_raw_parquet},
            "3": {"title": "📈 Indicators", "handler": self._load_indicators},
            "4": {"title": "✨ Cleaned Data", "handler": self._load_cleaned_data},
            "0": {"title": "🔙 Back", "handler": None},
            "00": {"title": "🚪 Exit", "handler": self._exit_system}
        }
    
    def show_menu(self):
        """Display the data loading menu."""
        print(f"\n{Fore.YELLOW}📊 LOAD DATA")
        print(f"{Fore.CYAN}{'─'*50}")
        
        for key, item in self.menu_items.items():
            if key in ["0", "00"]:
                print(f"{Fore.RED}{key}. {item['title']}")
            else:
                print(f"{Fore.WHITE}{key}. {item['title']}")
        
        print(f"{Fore.CYAN}{'─'*50}")
        print(f"{Fore.YELLOW}💡 Choose data source to load into memory")
        print(f"{Fore.CYAN}{'─'*50}\n")
    
    def _load_csv_converted(self):
        """Load CSV converted data."""
        print(f"\n{Fore.YELLOW}📁 Loading CSV Converted Data...")
        print(f"{Fore.CYAN}This feature will be implemented in the next phase...")
        time.sleep(2)
    
    def _load_raw_parquet(self):
        """Load raw parquet data."""
        print(f"\n{Fore.YELLOW}📊 Loading Raw Parquet Data...")
        print(f"{Fore.CYAN}This feature will be implemented in the next phase...")
        time.sleep(2)
    
    def _load_indicators(self):
        """Load indicators data."""
        print(f"\n{Fore.YELLOW}📈 Loading Indicators Data...")
        print(f"{Fore.CYAN}This feature will be implemented in the next phase...")
        time.sleep(2)
    
    def _load_cleaned_data(self):
        """Load cleaned data."""
        print(f"\n{Fore.YELLOW}✨ Loading Cleaned Data...")
        print(f"{Fore.CYAN}This feature will be implemented in the next phase...")
        time.sleep(2)
