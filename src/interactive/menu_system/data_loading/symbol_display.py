# -*- coding: utf-8 -*-
"""
Symbol Display for NeoZork Interactive ML Trading Strategy Development.

This module provides utilities for displaying symbol information in a
modern, formatted way with tables and progress indicators.
"""

from typing import Dict, Any, List
import pandas as pd
from colorama import Fore, Style


class SymbolDisplay:
    """
    Display utilities for symbol information.
    
    Features:
    - Modern table formatting
    - Symbol selection interface
    - Timeframe information display
    - Progress indicators
    """
    
    def __init__(self):
        """Initialize the symbol display."""
        pass
    
    def display_symbols_table(self, symbol_info: Dict[str, Any], total_size: float):
        """
        Display symbols information in a modern table format.
        
        Args:
            symbol_info: Dictionary with symbol analysis results
            total_size: Total size of all symbols in MB
        """
        print(f"\n{Fore.GREEN}📈 Available Symbols ({len(symbol_info)}):")
        print(f"{Fore.CYAN}{'─'*80}")
        
        # Display symbol information in a modern table format
        print(f"{Fore.WHITE}{'Symbol':<12} {'Size (MB)':<10} {'Files':<6} {'Timeframes':<20} {'Start Date':<12} {'End Date':<12}")
        print(f"{Fore.CYAN}{'─'*80}")
        
        for symbol_name, info in symbol_info.items():
            timeframes_str = ', '.join(info['timeframes'][:3])
            if len(info['timeframes']) > 3:
                timeframes_str += f" +{len(info['timeframes'])-3} more"
            
            start_date = info['start_date'][:10] if info['start_date'] != "No data" else "No data"
            end_date = info['end_date'][:10] if info['end_date'] != "No data" else "No data"
            
            print(f"{Fore.WHITE}{symbol_name:<12} {info['total_size_mb']:<10.1f} {info['file_count']:<6} {timeframes_str:<20} {start_date:<12} {end_date:<12}")
        
        print(f"{Fore.CYAN}{'─'*80}")
        print(f"{Fore.YELLOW}Total: {len(symbol_info)} symbols, {total_size:.1f} MB")
    
    def display_timeframes_info(self, symbol: str, timeframes: List[str], 
                              timeframe_details: Dict[str, Any]):
        """
        Display timeframes information for a selected symbol.
        
        Args:
            symbol: Symbol name
            timeframes: List of available timeframes
            timeframe_details: Dictionary with timeframe details
        """
        print(f"\n{Fore.GREEN}📈 {symbol} - Available Timeframes ({len(timeframes)}):")
        print(f"{Fore.CYAN}{'─'*60}")
        
        for i, tf in enumerate(timeframes, 1):
            tf_info = timeframe_details[tf]
            print(f"{Fore.WHITE}{i:2d}. {tf:<4} │ {tf_info['size_mb']:>6.1f}MB │ "
                  f"{tf_info['rows']:>8,} rows │ {tf_info['start_date'][:10]} to {tf_info['end_date'][:10]}")
        
        print(f"{Fore.CYAN}{'─'*60}")
    
    def get_symbol_choice(self, available_symbols: List[str]) -> str:
        """
        Get symbol choice from user.
        
        Args:
            available_symbols: List of available symbol names
            
        Returns:
            Selected symbol name
        """
        print(f"\n{Fore.GREEN}📊 Choose Symbol to Load into Memory")
        print(f"{Fore.CYAN}{'─'*50}")
        
        symbol_choice = input(f"{Fore.GREEN}Enter symbol name (e.g., 'eurusd') [default: eurusd]: {Style.RESET_ALL}").strip().lower()
        if not symbol_choice:
            symbol_choice = "eurusd"
        
        symbol_choice_upper = symbol_choice.upper()
        
        if symbol_choice_upper not in available_symbols:
            print(f"{Fore.RED}❌ Symbol '{symbol_choice_upper}' not found")
            print(f"{Fore.YELLOW}Available symbols: {', '.join(available_symbols)}")
            return None
        
        return symbol_choice
    
    def display_loading_start(self, symbol: str, timeframes: List[str]):
        """
        Display loading start message.
        
        Args:
            symbol: Symbol name
            timeframes: List of timeframes to load
        """
        print(f"\n{Fore.GREEN}✅ Selected: {symbol.upper()}")
        print(f"{Fore.CYAN}📊 Loading all {len(timeframes)} timeframes: {', '.join(timeframes)}")
        print(f"{Fore.YELLOW}💡 All timeframes will be loaded for comprehensive analysis")
    
    def display_loading_complete(self, symbol: str, result: Dict[str, Any]):
        """
        Display loading completion message.
        
        Args:
            symbol: Symbol name
            result: Loading result dictionary
        """
        if result['status'] == 'success':
            print(f"\n{Fore.GREEN}🎯 Loading completed successfully!")
            print(f"  • Symbol: {symbol.upper()}")
            print(f"  • Timeframes: {len(result['loaded_data'])}")
            print(f"  • Memory used: {result['memory_used']:.1f} MB")
            print(f"  • Loading time: {result['loading_time']:.2f} seconds")
        else:
            print(f"\n{Fore.RED}❌ Loading failed: {result.get('message', 'Unknown error')}")
    
    def display_error(self, message: str):
        """
        Display error message.
        
        Args:
            message: Error message to display
        """
        print(f"\n{Fore.RED}❌ Error: {message}")
    
    def display_no_symbols_found(self):
        """Display message when no symbols are found."""
        print(f"{Fore.RED}❌ No symbol folders found in cleaned data")
    
    def display_no_cleaned_data(self):
        """Display message when cleaned data directory is not found."""
        print(f"{Fore.RED}❌ Cleaned data directory not found")
    
    def display_symbol_not_found(self, symbol: str, available_symbols: List[str]):
        """
        Display message when selected symbol is not found.
        
        Args:
            symbol: Selected symbol name
            available_symbols: List of available symbols
        """
        print(f"{Fore.RED}❌ Symbol '{symbol}' not found")
        print(f"{Fore.YELLOW}Available symbols: {', '.join(available_symbols)}")
    
    def display_loading_summary(self, symbol: str, loaded_data: Dict[str, Any], 
                              memory_used: float, loading_time: float):
        """
        Display detailed loading summary.
        
        Args:
            symbol: Symbol name
            loaded_data: Dictionary with loaded data
            memory_used: Memory used in MB
            loading_time: Loading time in seconds
        """
        print(f"\n{Fore.GREEN}📊 Loading Summary for {symbol.upper()}:")
        print(f"{Fore.CYAN}{'─'*50}")
        print(f"  • Timeframes loaded: {len(loaded_data)}")
        print(f"  • Total rows: {sum(len(df) for df in loaded_data.values()):,}")
        print(f"  • Memory used: {memory_used:.1f} MB")
        print(f"  • Loading time: {loading_time:.2f} seconds")
        print(f"  • Average speed: {len(loaded_data) / loading_time:.1f} tf/s")
        print(f"{Fore.CYAN}{'─'*50}")
    
    def display_timeframe_summary(self, loaded_data: Dict[str, Any], 
                                timeframe_details: Dict[str, Any]):
        """
        Display timeframe summary.
        
        Args:
            loaded_data: Dictionary with loaded data
            timeframe_details: Dictionary with timeframe details
        """
        print(f"\n{Fore.YELLOW}📋 Timeframe Summary:")
        for tf, df in loaded_data.items():
            tf_info = timeframe_details[tf]
            print(f"  • {tf:<4}: {len(df):>8,} rows, {tf_info['size_mb']:>6.1f} MB, "
                  f"{tf_info['start_date'][:10]} to {tf_info['end_date'][:10]}")
    
    def display_mtf_info(self, mtf_data: Dict[str, Any]):
        """
        Display MTF structure information.
        
        Args:
            mtf_data: MTF data structure
        """
        print(f"\n{Fore.GREEN}🔧 MTF Structure Created:")
        print(f"  • Main timeframe: {mtf_data.get('main_timeframe', 'N/A')}")
        print(f"  • Available timeframes: {', '.join(mtf_data.get('timeframes', []))}")
        print(f"  • Main data shape: {mtf_data.get('main_data', pd.DataFrame()).shape}")
        print(f"  • Cross-timeframe features: {len(mtf_data.get('cross_timeframe_features', {}))}")
    
    def display_save_info(self, symbol: str, file_path: str):
        """
        Display save information.
        
        Args:
            symbol: Symbol name
            file_path: Path where data was saved
        """
        print(f"\n{Fore.GREEN}💾 Data saved successfully!")
        print(f"  • Symbol: {symbol.upper()}")
        print(f"  • Location: {file_path}")
        print(f"  • Format: Parquet (ML-optimized)")
        print(f"  • Ready for EDA, feature engineering, ML, backtesting, and monitoring")
        print(f"  • Use generated ML loader: {symbol.lower()}_ml_loader.py")
