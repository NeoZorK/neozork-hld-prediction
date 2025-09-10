# -*- coding: utf-8 -*-
"""
Data Loading Menu for NeoZork Interactive ML Trading Strategy Development.

This module provides the data loading submenu with support for multiple data sources.
"""

from typing import Dict, Any, Optional
import time
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
        
        # Get symbol filter from user
        symbol_filter = input(f"{Fore.GREEN}Enter symbol filter (optional, e.g., 'eurusd'): {Style.RESET_ALL}").strip()
        if not symbol_filter:
            symbol_filter = None
        
        # Load data
        from src.interactive.data_management import DataLoader
        loader = DataLoader()
        result = loader.load_csv_converted_data(symbol_filter)
        
        if result["status"] == "success":
            self._display_loaded_data(result)
        else:
            print(f"{Fore.RED}❌ Error: {result['message']}")
        
        input(f"\n{Fore.CYAN}Press Enter to continue...")
    
    def _display_loaded_data(self, result: Dict[str, Any]):
        """Display loaded data information."""
        metadata = result["metadata"]
        data = result["data"]
        
        print(f"\n{Fore.GREEN}📊 Data Loaded Successfully!")
        print(f"{Fore.CYAN}{'─'*50}")
        print(f"{Fore.YELLOW}📈 Summary:")
        print(f"  • Total files: {metadata['total_files']}")
        print(f"  • Total size: {metadata['total_size_mb']} MB")
        print(f"  • Total rows: {metadata['total_rows']:,}")
        print(f"  • Symbols: {', '.join(metadata['symbols'])}")
        
        print(f"\n{Fore.YELLOW}📋 Detailed Information:")
        for symbol, info in data.items():
            print(f"\n{Fore.WHITE}🔸 {symbol}:")
            print(f"  • File: {info['file_path'].split('/')[-1]}")
            print(f"  • Size: {info['size_mb']} MB")
            print(f"  • Rows: {info['rows']:,}")
            print(f"  • Time range: {info['start_time']} to {info['end_time']}")
            print(f"  • Columns: {len(info['columns'])} ({', '.join(info['columns'][:5])}{'...' if len(info['columns']) > 5 else ''})")
    
    def _load_raw_parquet(self):
        """Load raw parquet data."""
        print(f"\n{Fore.YELLOW}📊 Loading Raw Parquet Data...")
        
        # Get symbol filter from user
        symbol_filter = input(f"{Fore.GREEN}Enter symbol filter (optional, e.g., 'btcusdt'): {Style.RESET_ALL}").strip()
        if not symbol_filter:
            symbol_filter = None
        
        # Load data
        from src.interactive.data_management import DataLoader
        loader = DataLoader()
        result = loader.load_raw_parquet_data(symbol_filter)
        
        if result["status"] == "success":
            self._display_loaded_data(result)
        else:
            print(f"{Fore.RED}❌ Error: {result['message']}")
        
        input(f"\n{Fore.CYAN}Press Enter to continue...")
    
    def _load_indicators(self):
        """Load indicators data."""
        print(f"\n{Fore.YELLOW}📈 Loading Indicators Data...")
        
        # Get symbol filter from user
        symbol_filter = input(f"{Fore.GREEN}Enter symbol filter (optional, e.g., 'aapl'): {Style.RESET_ALL}").strip()
        if not symbol_filter:
            symbol_filter = None
        
        # Load data
        from src.interactive.data_management import DataLoader
        loader = DataLoader()
        result = loader.load_indicators_data(symbol_filter)
        
        if result["status"] == "success":
            self._display_loaded_data(result)
        else:
            print(f"{Fore.RED}❌ Error: {result['message']}")
        
        input(f"\n{Fore.CYAN}Press Enter to continue...")
    
    def _load_cleaned_data(self):
        """Load cleaned data."""
        print(f"\n{Fore.YELLOW}✨ Loading Cleaned Data...")
        
        # Get symbol filter from user
        symbol_filter = input(f"{Fore.GREEN}Enter symbol filter (optional, e.g., 'eurusd'): {Style.RESET_ALL}").strip()
        if not symbol_filter:
            symbol_filter = None
        
        # Load data
        from src.interactive.data_management import DataLoader
        loader = DataLoader()
        result = loader.load_cleaned_data(symbol_filter)
        
        if result["status"] == "success":
            self._display_loaded_data(result)
        else:
            print(f"{Fore.RED}❌ Error: {result['message']}")
        
        input(f"\n{Fore.CYAN}Press Enter to continue...")
