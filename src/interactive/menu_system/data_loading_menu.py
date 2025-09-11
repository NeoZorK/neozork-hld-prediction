# -*- coding: utf-8 -*-
"""
Data Loading Menu for NeoZork Interactive ML Trading Strategy Development.

This module provides the data loading submenu with support for multiple data sources.
"""

from typing import Dict, Any, Optional
import time
import colorama
from colorama import Fore, Back, Style
from .base_menu import BaseMenu
from src.interactive.data_management.file_analyzer import FileAnalyzer

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
        self.file_analyzer = FileAnalyzer()
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
        """Load CSV converted data with detailed folder analysis."""
        print(f"\n{Fore.YELLOW}📁 CSV Converted Data Analysis...")
        
        # Analyze folder first
        analysis = self.file_analyzer.analyze_csv_converted_folder()
        
        if analysis["status"] == "error":
            print(f"{Fore.RED}❌ Error: {analysis['message']}")
            input(f"\n{Fore.CYAN}Press Enter to continue...")
            return
        
        # Display folder information
        self._display_folder_info(analysis["folder_info"], "CSV Converted")
        
        # Display symbols found
        if analysis["symbols"]:
            print(f"\n{Fore.GREEN}📈 Available Symbols ({len(analysis['symbols'])}):")
            symbols_text = ", ".join(analysis["symbols"])
            print(f"{Fore.WHITE}  {symbols_text}")
        
        # Group files by symbol and sort
        if analysis["files_info"]:
            files_by_symbol = {}
            for filename, file_info in analysis["files_info"].items():
                # Extract symbol from filename
                symbol = self._extract_symbol_from_filename(filename)
                if symbol:
                    if symbol not in files_by_symbol:
                        files_by_symbol[symbol] = []
                    files_by_symbol[symbol].append((filename, file_info))
            
            # Sort symbols alphabetically
            sorted_symbols = sorted(files_by_symbol.keys())
            
            print(f"\n{Fore.YELLOW}📋 Files by Symbol ({len(sorted_symbols)} symbols):")
            print(f"{Fore.CYAN}{'─'*80}")
            
            for symbol in sorted_symbols:
                files = files_by_symbol[symbol]
                # Sort files by timeframe (M1, M5, M15, H1, H4, D1, W1, MN1)
                timeframe_order = {'M1': 1, 'M5': 2, 'M15': 3, 'H1': 4, 'H4': 5, 'D1': 6, 'W1': 7, 'MN1': 8}
                files.sort(key=lambda x: timeframe_order.get(x[1]['timeframes'][0] if x[1]['timeframes'] else 'Unknown', 999))
                
                print(f"\n{Fore.GREEN}🔸 {symbol} ({len(files)} files):")
                
                # Display files in compact format
                for filename, file_info in files:
                    timeframe = file_info['timeframes'][0] if file_info['timeframes'] else 'Unknown'
                    size_mb = file_info['size_mb']
                    rows = file_info['rows']
                    start_date = file_info['start_date'][:10] if file_info['start_date'] != "No time data" else "No data"
                    end_date = file_info['end_date'][:10] if file_info['end_date'] != "No time data" else "No data"
                    
                    print(f"  {Fore.WHITE}{timeframe:>4} │ {size_mb:>6.1f}MB │ {rows:>8,} rows │ {start_date} to {end_date}")
        
        # Ask if user wants to load data
        load_data = input(f"\n{Fore.GREEN}Load data into memory? (y/n): {Style.RESET_ALL}").strip().lower()
        
        if load_data == 'y':
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
        """Load raw parquet data with detailed folder analysis."""
        print(f"\n{Fore.YELLOW}📊 Raw Parquet Data Analysis...")
        
        # Analyze folder first
        analysis = self.file_analyzer.analyze_raw_parquet_folder()
        
        if analysis["status"] == "error":
            print(f"{Fore.RED}❌ Error: {analysis['message']}")
            input(f"\n{Fore.CYAN}Press Enter to continue...")
            return
        
        # Display folder information
        self._display_folder_info(analysis["folder_info"], "Raw Parquet")
        
        # Display sources found
        if analysis["sources"]:
            print(f"\n{Fore.GREEN}🏢 Available Sources:")
            sources_text = ", ".join(analysis["sources"])
            print(f"{Fore.WHITE}  {sources_text}")
        
        # Display symbols by source
        if analysis["symbols_by_source"]:
            print(f"\n{Fore.YELLOW}📈 Symbols by Source:")
            for source, symbols in analysis["symbols_by_source"].items():
                symbols_text = ", ".join(symbols)
                print(f"\n{Fore.WHITE}🔸 {source.upper()}:")
                print(f"  {symbols_text}")
        
        # Display files information
        if analysis["files_info"]:
            print(f"\n{Fore.YELLOW}📋 Files Information:")
            for filename, file_info in analysis["files_info"].items():
                print(f"\n{Fore.WHITE}🔸 {filename}:")
                print(f"  • Size: {file_info['size_mb']} MB")
                print(f"  • Rows: {file_info['rows']:,}")
                print(f"  • Date range: {file_info['start_date']} to {file_info['end_date']}")
                print(f"  • Timeframes: {', '.join(file_info['timeframes'][:3])}{'...' if len(file_info['timeframes']) > 3 else ''}")
        
        # Ask if user wants to load data
        load_data = input(f"\n{Fore.GREEN}Load data into memory? (y/n): {Style.RESET_ALL}").strip().lower()
        
        if load_data == 'y':
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
        """Load indicators data with detailed folder analysis."""
        print(f"\n{Fore.YELLOW}📈 Indicators Data Analysis...")
        
        # Analyze folder first
        analysis = self.file_analyzer.analyze_indicators_folder()
        
        if analysis["status"] == "error":
            print(f"{Fore.RED}❌ Error: {analysis['message']}")
            input(f"\n{Fore.CYAN}Press Enter to continue...")
            return
        
        # Display folder information
        self._display_folder_info(analysis["folder_info"], "Indicators")
        
        # Display indicators found
        if analysis["indicators"]:
            print(f"\n{Fore.GREEN}📊 Available Indicators:")
            indicators_text = ", ".join(analysis["indicators"])
            print(f"{Fore.WHITE}  {indicators_text}")
        
        # Display subfolders information
        if analysis["subfolders_info"]:
            print(f"\n{Fore.YELLOW}📁 Subfolders Information:")
            for subdir, subfolder_info in analysis["subfolders_info"].items():
                print(f"\n{Fore.WHITE}🔸 {subdir.upper()}:")
                print(f"  • Files: {subfolder_info['file_count']}")
                print(f"  • Size: {subfolder_info['size_mb']} MB")
                print(f"  • Modified: {subfolder_info['modified']}")
                
                # Show files in this subfolder
                if subfolder_info.get("files_info"):
                    print(f"  • Files:")
                    for filename, file_info in subfolder_info["files_info"].items():
                        print(f"    - {filename}: {file_info['size_mb']} MB, {file_info['rows']:,} rows")
        
        # Ask if user wants to load data
        load_data = input(f"\n{Fore.GREEN}Load data into memory? (y/n): {Style.RESET_ALL}").strip().lower()
        
        if load_data == 'y':
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
        """Load cleaned data with detailed folder analysis."""
        print(f"\n{Fore.YELLOW}✨ Cleaned Data Analysis...")
        
        # Analyze folder first
        analysis = self.file_analyzer.analyze_cleaned_data_folder()
        
        if analysis["status"] == "error":
            print(f"{Fore.RED}❌ Error: {analysis['message']}")
            input(f"\n{Fore.CYAN}Press Enter to continue...")
            return
        
        # Display folder information
        self._display_folder_info(analysis["folder_info"], "Cleaned Data")
        
        # Display symbols found
        if analysis["symbols"]:
            print(f"\n{Fore.GREEN}📈 Available Symbols:")
            symbols_text = ", ".join(analysis["symbols"])
            print(f"{Fore.WHITE}  {symbols_text}")
        
        # Display save dates
        if analysis["save_dates"]:
            print(f"\n{Fore.GREEN}📅 Save Dates:")
            dates_text = ", ".join(analysis["save_dates"])
            print(f"{Fore.WHITE}  {dates_text}")
        
        # Display files information
        if analysis["files_info"]:
            print(f"\n{Fore.YELLOW}📋 Files Information:")
            for filename, file_info in analysis["files_info"].items():
                print(f"\n{Fore.WHITE}🔸 {filename}:")
                print(f"  • Size: {file_info['size_mb']} MB")
                print(f"  • Rows: {file_info['rows']:,}")
                print(f"  • Date range: {file_info['start_date']} to {file_info['end_date']}")
                print(f"  • Timeframes: {', '.join(file_info['timeframes'][:3])}{'...' if len(file_info['timeframes']) > 3 else ''}")
        
        # Ask if user wants to load data
        load_data = input(f"\n{Fore.GREEN}Load data into memory? (y/n): {Style.RESET_ALL}").strip().lower()
        
        if load_data == 'y':
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
    
    def _display_folder_info(self, folder_info: Dict[str, Any], folder_name: str):
        """Display detailed folder information."""
        print(f"\n{Fore.CYAN}📁 {folder_name} Folder Information:")
        print(f"{Fore.CYAN}{'─'*50}")
        print(f"{Fore.WHITE}  • Path: {folder_info['path']}")
        print(f"{Fore.WHITE}  • Files: {folder_info['file_count']}")
        print(f"{Fore.WHITE}  • Size: {folder_info['size_mb']} MB")
        print(f"{Fore.WHITE}  • Modified: {folder_info['modified']}")
        print(f"{Fore.CYAN}{'─'*50}")
    
    def _extract_symbol_from_filename(self, filename: str) -> Optional[str]:
        """Extract symbol from filename."""
        try:
            # Remove extension
            name = filename.split('.')[0]
            
            # Look for patterns like CSVExport_SYMBOL_PERIOD_...
            if "CSVExport_" in name:
                parts = name.split("_")
                if len(parts) >= 2:
                    return parts[1].upper()
            
            # Look for patterns like cleaned_csv_converted_SYMBOL_...
            if "cleaned_csv_converted_" in name:
                parts = name.split("_")
                if len(parts) >= 4:
                    return parts[3].upper()
            
            # Look for patterns like SYMBOL_PERIOD_...
            if "_PERIOD_" in name:
                parts = name.split("_")
                if len(parts) >= 2:
                    return parts[0].upper()
            
            return None
        except Exception as e:
            print_error(f"Error extracting symbol from {filename}: {e}")
            return None
