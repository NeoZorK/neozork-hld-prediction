# -*- coding: utf-8 -*-
# src/cli/core/show_yfinance.py

"""
Yahoo Finance show mode handling for CLI.
"""

import os
import sys
from pathlib import Path
import pandas as pd
import pyarrow.parquet as pq
from colorama import Fore, Style

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


def handle_yfinance_show_mode(args):
    """
    Handle Yahoo Finance show mode operations.
    """
    yf_dir = Path("data/cleaned_data")
    
    if not yf_dir.exists():
        print(f"{Fore.RED}Yahoo Finance data directory not found: {yf_dir}{Style.RESET_ALL}")
        return
    
    # Get yfinance files (all parquet files in cleaned_data)
    yf_files = list(yf_dir.glob("*.parquet"))
    
    if not yf_files:
        print(f"{Fore.YELLOW}No Yahoo Finance files found in {yf_dir}{Style.RESET_ALL}")
        return
    
    # Filter by keywords if provided
    if args.keywords:
        filtered_files = []
        for file in yf_files:
            if any(keyword.lower() in file.stem.lower() for keyword in args.keywords):
                filtered_files.append(file)
        yf_files = filtered_files
        
        if not yf_files:
            print(f"{Fore.YELLOW}No Yahoo Finance files found matching keywords: {args.keywords}{Style.RESET_ALL}")
            return
    
    # Display files
    print(f"\n{Fore.CYAN}{Style.BRIGHT}Found {len(yf_files)} Yahoo Finance file(s):{Style.RESET_ALL}")
    for i, file in enumerate(yf_files, 1):
        print(f"  {i}. {file.name}")
    
    # If only one file and plotting is requested, plot it
    if len(yf_files) == 1 and hasattr(args, 'draw') and args.draw != 'fastest':
        file_path = yf_files[0]
        print(f"\n{Fore.YELLOW}Plotting single Yahoo Finance file: {file_path.name}{Style.RESET_ALL}")
        plot_yfinance_file(file_path, args)
    elif len(yf_files) > 1:
        # Multiple files - show selection or process all
        if hasattr(args, 'draw') and args.draw != 'fastest':
            print(f"\n{Fore.YELLOW}Multiple files found. Use specific keywords to select one file for plotting.{Style.RESET_ALL}")
        else:
            # Process all files for export if requested
            process_multiple_yfinance_files(yf_files, args)


def plot_yfinance_file(file_path, args):
    """
    Plot a single Yahoo Finance file.
    """
    try:
        # Read the parquet file
        df = pq.read_table(file_path).to_pandas()
        
        # Set up plotting backend
        if setup_interactive_backend:
            setup_interactive_backend()
        
        # Plot based on draw method
        draw_method = getattr(args, 'draw', 'fastest')
        
        if draw_method == 'fastest':
            if plot_auto_fastest_parquet:
                plot_auto_fastest_parquet(str(file_path))
            else:
                print(f"{Fore.RED}Fastest plotting not available{Style.RESET_ALL}")
        elif draw_method in ['plotly', 'plt']:
            if auto_plot_from_parquet:
                auto_plot_from_parquet(str(file_path))
            else:
                print(f"{Fore.RED}Plotly plotting not available{Style.RESET_ALL}")
        elif draw_method in ['mplfinance', 'mpl']:
            if mpl_auto_plot_from_parquet:
                mpl_auto_plot_from_parquet(str(file_path))
            else:
                print(f"{Fore.RED}Matplotlib plotting not available{Style.RESET_ALL}")
        elif draw_method in ['seaborn', 'sb']:
            if auto_plot_from_parquet:
                auto_plot_from_parquet(str(file_path))
            else:
                print(f"{Fore.RED}Seaborn plotting not available{Style.RESET_ALL}")
        elif draw_method == 'term':
            if auto_plot_from_dataframe:
                auto_plot_from_dataframe(df)
            else:
                print(f"{Fore.RED}Terminal plotting not available{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}Unknown plotting method: {draw_method}{Style.RESET_ALL}")
            
    except Exception as e:
        print(f"{Fore.RED}Error plotting Yahoo Finance file: {e}{Style.RESET_ALL}")
        import traceback
        traceback.print_exc()


def process_multiple_yfinance_files(yf_files, args):
    """
    Process multiple Yahoo Finance files for export operations.
    """
    export_parquet = getattr(args, 'export_parquet', False)
    export_csv = getattr(args, 'export_csv', False)
    export_json = getattr(args, 'export_json', False)
    export_info = getattr(args, 'export_indicators_info', False)
    
    if not any([export_parquet, export_csv, export_json, export_info]):
        return
    
    print(f"\n{Fore.YELLOW}Processing {len(yf_files)} Yahoo Finance files for export...{Style.RESET_ALL}")
    
    for i, file_path in enumerate(yf_files, 1):
        print(f"\n{Fore.CYAN}Processing file {i}/{len(yf_files)}: {file_path.name}{Style.RESET_ALL}")
        
        try:
            # Read the file
            df = pq.read_table(file_path).to_pandas()
            
            # Calculate indicators if rule is specified
            if hasattr(args, 'rule') and args.rule:
                from src.calculation.indicator_calculation import calculate_indicator
                if calculate_indicator:
                    # This would need to be implemented based on the specific rule
                    print(f"  Calculating indicators with rule: {args.rule}")
                    # TODO: Implement indicator calculation
            
            # Export if requested
            if export_parquet:
                export_path = f"../data/indicators/parquet/{file_path.stem}_indicators.parquet"
                if export_indicator_to_parquet:
                    export_indicator_to_parquet(df, export_path)
                    print(f"  Exported to parquet: {export_path}")
            
            if export_csv:
                export_path = f"../data/indicators/csv/{file_path.stem}_indicators.csv"
                if export_indicator_to_csv:
                    export_indicator_to_csv(df, export_path)
                    print(f"  Exported to CSV: {export_path}")
            
            if export_json:
                export_path = f"../data/indicators/json/{file_path.stem}_indicators.json"
                if export_indicator_to_json:
                    export_indicator_to_json(df, export_path)
                    print(f"  Exported to JSON: {export_path}")
            
            if export_info:
                # Export metadata
                metadata = {
                    'filename': file_path.name,
                    'rows': len(df),
                    'columns': list(df.columns),
                    'data_types': df.dtypes.to_dict()
                }
                export_path = f"../data/indicators/metadata/{file_path.stem}_metadata.json"
                os.makedirs(os.path.dirname(export_path), exist_ok=True)
                import json
                with open(export_path, 'w') as f:
                    json.dump(metadata, f, indent=2, default=str)
                print(f"  Exported metadata to: {export_path}")
                
        except Exception as e:
            print(f"{Fore.RED}  Error processing file {file_path.name}: {e}{Style.RESET_ALL}")
            import traceback
            traceback.print_exc()
    
    print(f"\n{Fore.GREEN}Finished processing {len(yf_files)} Yahoo Finance files{Style.RESET_ALL}")
