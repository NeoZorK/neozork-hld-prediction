# -*- coding: utf-8 -*-
# src/cli/core/show_universal.py

"""
Universal show mode handling for CLI that scans all data folders.
"""

import os
import sys
from pathlib import Path
import pandas as pd
import pyarrow.parquet as pq
from colorama import Fore, Style
from collections import defaultdict
import re

from .cli_show_mode import (
    plot_auto_fastest_parquet,
    auto_plot_from_parquet,
    mpl_auto_plot_from_parquet,
    auto_plot_from_dataframe,
    display_universal_trading_metrics,
    setup_interactive_backend,
    export_indicator_to_parquet,
    export_indicator_to_csv,
    export_indicator_to_json
)


def handle_universal_show_mode(args):
    """
    Handle universal show mode operations that scans all data folders.
    """
    data_dir = Path("data")
    
    if not data_dir.exists():
        print(f"{Fore.RED}Data directory not found: {data_dir}{Style.RESET_ALL}")
        return
    
    # Scan all data folders
    all_data = scan_all_data_folders(data_dir)
    
    if not all_data:
        print(f"{Fore.YELLOW}No data files found in {data_dir}{Style.RESET_ALL}")
        return
    
    # Filter by source if specified
    if hasattr(args, 'source') and args.source and args.source != 'yfinance':
        filtered_data = filter_by_source(all_data, args.source)
        if not filtered_data:
            print(f"{Fore.YELLOW}No data found for source: {args.source}{Style.RESET_ALL}")
            return
        all_data = filtered_data
    
    # Filter by keywords if provided
    if hasattr(args, 'keywords') and args.keywords:
        all_data = filter_by_keywords(all_data, args.keywords)
        if not all_data:
            print(f"{Fore.YELLOW}No data found matching keywords: {args.keywords}{Style.RESET_ALL}")
            return
    
    # Display organized results
    display_organized_data(all_data, args)


def scan_all_data_folders(data_dir):
    """
    Scan all folders in data directory and organize files by source and symbol.
    """
    all_data = defaultdict(lambda: defaultdict(list))
    
    # Define folder mappings
    folder_mappings = {
        'raw_parquet': 'raw',
        'cleaned_data': 'yfinance',
        'cache/csv_converted': 'csv',
        'indicators/parquet': 'indicators',
        'indicators/csv': 'indicators_csv',
        'indicators/json': 'indicators_json'
    }
    
    # Scan each folder
    for folder_name, source_type in folder_mappings.items():
        folder_path = data_dir / folder_name
        if folder_path.exists():
            scan_folder(folder_path, source_type, all_data)
    
    # Also scan root data directory for loose files
    scan_folder(data_dir, 'root', all_data)
    
    return all_data


def scan_folder(folder_path, source_type, all_data):
    """
    Scan a specific folder for data files.
    """
    # Get all parquet, csv, and json files
    for pattern in ['*.parquet', '*.csv', '*.json']:
        for file_path in folder_path.glob(pattern):
            if file_path.is_file():
                # Parse file information
                file_info = parse_file_info(file_path, source_type)
                if file_info:
                    symbol = file_info['symbol']
                    all_data[source_type][symbol].append(file_info)


def parse_file_info(file_path, source_type):
    """
    Parse file information to extract source, symbol, timeframe, etc.
    """
    filename = file_path.stem
    file_ext = file_path.suffix
    
    # Get file size
    try:
        file_size = file_path.stat().st_size
        file_size_mb = file_size / (1024 * 1024)
    except:
        file_size = 0
        file_size_mb = 0
    
    # Parse different file naming patterns
    if source_type == 'raw':
        # Pattern: source_SYMBOL_TIMEFRAME.parquet
        match = re.match(r'^(\w+)_([A-Z0-9.]+)_([A-Z0-9]+)\.parquet$', filename)
        if match:
            source, symbol, timeframe = match.groups()
            return {
                'file_path': file_path,
                'filename': file_path.name,
                'source': source,
                'symbol': symbol,
                'timeframe': timeframe,
                'file_type': 'parquet',
                'file_size': file_size,
                'file_size_mb': file_size_mb,
                'folder': 'raw_parquet'
            }
        else:
            # Try alternative pattern: source_SYMBOL_TIMEFRAME.parquet
            # For files like yfinance_AAPL_D1.parquet, binance_BTCUSDT_H1.parquet
            parts = filename.split('_')
            if len(parts) >= 3:
                source = parts[0]
                symbol = parts[1]
                timeframe = parts[2].replace('.parquet', '')
                return {
                    'file_path': file_path,
                    'filename': file_path.name,
                    'source': source,
                    'symbol': symbol,
                    'timeframe': timeframe,
                    'file_type': 'parquet',
                    'file_size': file_size,
                    'file_size_mb': file_size_mb,
                    'folder': 'raw_parquet'
                }
            else:
                # Fallback for files that don't match any pattern
                return {
                    'file_path': file_path,
                    'filename': file_path.name,
                    'source': 'raw',
                    'symbol': 'UNKNOWN',
                    'timeframe': 'UNKNOWN',
                    'file_type': 'parquet',
                    'file_size': file_size,
                    'file_size_mb': file_size_mb,
                    'folder': 'raw_parquet'
                }
    
    elif source_type == 'csv':
        # Pattern: CSVExport_SYMBOL_PERIOD_TIMEFRAME.parquet
        match = re.match(r'^CSVExport_([A-Z0-9.]+)_PERIOD_([A-Z0-9]+)\.parquet$', filename)
        if match:
            symbol, timeframe = match.groups()
            return {
                'file_path': file_path,
                'filename': file_path.name,
                'source': 'csv',
                'symbol': symbol,
                'timeframe': timeframe,
                'file_type': 'parquet',
                'file_size': file_size,
                'file_size_mb': file_size_mb,
                'folder': 'cache/csv_converted'
            }
    
    elif source_type == 'yfinance':
        # Pattern: cleaned_*_dataset_*.parquet
        if 'cleaned' in filename and 'dataset' in filename:
            # Try to extract timeframe from filename
            timeframe = 'UNKNOWN'
            if 'h1' in filename:
                timeframe = 'H1'
            elif 'm5' in filename:
                timeframe = 'M5'
            elif 'main' in filename:
                timeframe = 'D1'
            
            return {
                'file_path': file_path,
                'filename': file_path.name,
                'source': 'yfinance',
                'symbol': 'MIXED',
                'timeframe': timeframe,
                'file_type': 'parquet',
                'file_size': file_size,
                'file_size_mb': file_size_mb,
                'folder': 'cleaned_data'
            }
    
    elif source_type == 'indicators':
        # Pattern: SYMBOL_TIMEFRAME_INDICATOR.parquet
        match = re.match(r'^([A-Z0-9.]+)_([A-Z0-9]+)_([A-Za-z]+)\.parquet$', filename)
        if match:
            symbol, timeframe, indicator = match.groups()
            return {
                'file_path': file_path,
                'filename': file_path.name,
                'source': 'indicators',
                'symbol': symbol,
                'timeframe': timeframe,
                'indicator': indicator,
                'file_type': 'parquet',
                'file_size': file_size,
                'file_size_mb': file_size_mb,
                'folder': 'indicators/parquet'
            }
        else:
            # Fallback for other indicator files
            return {
                'file_path': file_path,
                'filename': file_path.name,
                'source': 'indicators',
                'symbol': 'UNKNOWN',
                'timeframe': 'UNKNOWN',
                'indicator': 'UNKNOWN',
                'file_type': 'parquet',
                'file_size': file_size,
                'file_size_mb': file_size_mb,
                'folder': 'indicators/parquet'
            }
    
    elif source_type == 'root':
        # Handle loose files in root data directory
        if file_ext in ['.parquet', '.csv']:
            return {
                'file_path': file_path,
                'filename': file_path.name,
                'source': 'root',
                'symbol': 'UNKNOWN',
                'timeframe': 'UNKNOWN',
                'file_type': file_ext[1:],
                'file_size': file_size,
                'file_size_mb': file_size_mb,
                'folder': 'root'
            }
    
    return None


def filter_by_source(all_data, source_filter):
    """
    Filter data by source type.
    """
    filtered_data = defaultdict(lambda: defaultdict(list))
    
    for source_type, symbols in all_data.items():
        # Check if source_filter matches source_type exactly
        if source_filter.lower() == source_type.lower():
            filtered_data[source_type] = symbols
        else:
            # Check individual files for exact source match
            for symbol, files in symbols.items():
                matching_files = []
                for file_info in files:
                    if source_filter.lower() == file_info.get('source', '').lower():
                        matching_files.append(file_info)
                if matching_files:
                    filtered_data[source_type][symbol] = matching_files
    
    return filtered_data


def filter_by_keywords(all_data, keywords):
    """
    Filter data by keywords in filename or symbol.
    """
    filtered_data = defaultdict(lambda: defaultdict(list))
    
    for source_type, symbols in all_data.items():
        for symbol, files in symbols.items():
            filtered_files = []
            for file_info in files:
                # Check if any keyword matches filename or symbol
                if any(keyword.lower() in file_info['filename'].lower() or 
                       keyword.lower() in symbol.lower() for keyword in keywords):
                    filtered_files.append(file_info)
            
            if filtered_files:
                filtered_data[source_type][symbol] = filtered_files
    
    return filtered_data


def display_organized_data(all_data, args):
    """
    Display organized data in a structured format.
    """
    total_files = sum(len(files) for symbols in all_data.values() for files in symbols.values())
    
    print(f"\n{Fore.CYAN}{Style.BRIGHT}=== DATA OVERVIEW ==={Style.RESET_ALL}")
    print(f"Total files found: {total_files}")
    print(f"Sources: {len(all_data)}")
    
    for source_type, symbols in all_data.items():
        source_files = sum(len(files) for files in symbols.values())
        print(f"\n{Fore.YELLOW}{Style.BRIGHT}📁 {source_type.upper()} ({source_files} files){Style.RESET_ALL}")
        
        for symbol, files in symbols.items():
            print(f"  {Fore.GREEN}📊 {symbol}{Style.RESET_ALL} ({len(files)} files)")
            
            # Group files by timeframe if available
            timeframes = defaultdict(list)
            for file_info in files:
                timeframe = file_info.get('timeframe', 'UNKNOWN')
                timeframes[timeframe].append(file_info)
            
            for timeframe, timeframe_files in timeframes.items():
                if timeframe != 'UNKNOWN':
                    print(f"    {Fore.BLUE}⏰ {timeframe}{Style.RESET_ALL} ({len(timeframe_files)} files)")
                
                for file_info in timeframe_files:
                    size_str = f"{file_info['file_size_mb']:.2f} MB" if file_info['file_size_mb'] > 0 else "0 MB"
                    indicator_str = f" [{file_info.get('indicator', '')}]" if file_info.get('indicator') else ""
                    print(f"      • {file_info['filename']}{indicator_str} ({size_str})")
    
    # Show summary statistics
    print(f"\n{Fore.CYAN}{Style.BRIGHT}=== SUMMARY ==={Style.RESET_ALL}")
    total_size = 0
    for symbols in all_data.values():
        for files in symbols.values():
            for file_info in files:
                total_size += file_info['file_size_mb']
    
    print(f"Total data size: {total_size:.2f} MB")
    print(f"Average file size: {total_size/total_files:.2f} MB" if total_files > 0 else "No files")
    
    # If only one file and plotting is requested, plot it
    if total_files == 1 and hasattr(args, 'draw') and args.draw != 'fastest':
        for symbols in all_data.values():
            for files in symbols.values():
                if files:
                    file_info = files[0]
                    print(f"\n{Fore.YELLOW}Plotting single file: {file_info['filename']}{Style.RESET_ALL}")
                    plot_single_file(file_info, args)
                    break
    elif total_files > 1 and hasattr(args, 'draw') and args.draw != 'fastest':
        print(f"\n{Fore.YELLOW}Multiple files found. Use specific keywords to select one file for plotting.{Style.RESET_ALL}")


def plot_single_file(file_info, args):
    """
    Plot a single file.
    """
    try:
        file_path = file_info['file_path']
        
        # Set up plotting backend
        if setup_interactive_backend:
            setup_interactive_backend()
        
        # Plot based on draw method
        draw_method = getattr(args, 'draw', 'fastest')
        
        if draw_method == 'fastest':
            if plot_auto_fastest_parquet and file_info['file_type'] == 'parquet':
                plot_auto_fastest_parquet(str(file_path))
            else:
                print(f"{Fore.RED}Fastest plotting not available for this file type{Style.RESET_ALL}")
        elif draw_method in ['plotly', 'plt']:
            if auto_plot_from_parquet and file_info['file_type'] == 'parquet':
                auto_plot_from_parquet(str(file_path))
            else:
                print(f"{Fore.RED}Plotly plotting not available for this file type{Style.RESET_ALL}")
        elif draw_method in ['mplfinance', 'mpl']:
            if mpl_auto_plot_from_parquet and file_info['file_type'] == 'parquet':
                mpl_auto_plot_from_parquet(str(file_path))
            else:
                print(f"{Fore.RED}Matplotlib plotting not available for this file type{Style.RESET_ALL}")
        elif draw_method in ['seaborn', 'sb']:
            if auto_plot_from_parquet and file_info['file_type'] == 'parquet':
                auto_plot_from_parquet(str(file_path))
            else:
                print(f"{Fore.RED}Seaborn plotting not available for this file type{Style.RESET_ALL}")
        elif draw_method == 'term':
            if auto_plot_from_dataframe:
                # Read file and plot
                if file_info['file_type'] == 'parquet':
                    df = pq.read_table(file_path).to_pandas()
                elif file_info['file_type'] == 'csv':
                    df = pd.read_csv(file_path)
                else:
                    print(f"{Fore.RED}Terminal plotting not available for {file_info['file_type']} files{Style.RESET_ALL}")
                    return
                auto_plot_from_dataframe(df)
            else:
                print(f"{Fore.RED}Terminal plotting not available{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}Unknown plotting method: {draw_method}{Style.RESET_ALL}")
            
    except Exception as e:
        print(f"{Fore.RED}Error plotting file: {e}{Style.RESET_ALL}")
        import traceback
        traceback.print_exc()
