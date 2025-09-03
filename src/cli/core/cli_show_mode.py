# -*- coding: utf-8 -*-
# src/cli/core/cli_show_mode.py

"""
Main CLI show mode functionality.
"""

from pathlib import Path
import pyarrow.parquet as pq
import pandas as pd
import sys
import time
import traceback
import os
from colorama import init, Fore, Style

# Initialize colorama for cross-platform colored output
init(autoreset=True)

# Import for indicator calculation; fallback for different relative import
try:
    from src.calculation.indicator_calculation import calculate_indicator
    from src.export.parquet_export import export_indicator_to_parquet
    from src.export.csv_export import export_indicator_to_csv
    from src.export.json_export import export_indicator_to_json
except ImportError:
    try:
        from src.calculation.indicator_calculation import calculate_indicator
        from src.export.parquet_export import export_indicator_to_parquet
        from src.export.csv_export import export_indicator_to_csv
        from src.export.json_export import export_indicator_to_json
    except ImportError:
        # Last resort: assume running from src directory
        calculate_indicator = None
        export_indicator_to_parquet = None
        export_indicator_to_csv = None
        export_indicator_to_json = None

# Import the new AUTO fastest plot function
try:
    from src.plotting.fastest_auto_plot import plot_auto_fastest_parquet
except ImportError:
    plot_auto_fastest_parquet = None

# Import auto_plot_from_parquet for seaborn/sb
try:
    from src.plotting.seaborn_auto_plot import auto_plot_from_parquet
except ImportError:
    auto_plot_from_parquet = None

# Import auto_plot_from_parquet for mpl/mplfinance
try:
    from src.plotting.mplfinance_auto_plot import auto_plot_from_parquet as mpl_auto_plot_from_parquet
except ImportError:
    mpl_auto_plot_from_parquet = None

# Import terminal auto plot function for AUTO mode
try:
    from src.plotting.term_auto_plot import auto_plot_from_dataframe
except ImportError:
    auto_plot_from_dataframe = None

try:
    from src.calculation.universal_trading_metrics import display_universal_trading_metrics
except ImportError:
    display_universal_trading_metrics = None

# Import plot utilities for interactive backend setup
try:
    from src.plotting.plot_utils import setup_interactive_backend
except ImportError:
    setup_interactive_backend = None


def _force_terminal_mode_in_docker(args):
    """
    Force terminal mode in Docker environment for show commands.
    This ensures that show csv gbp commands always use -d term in Docker/container.
    """
    # Check if running in Docker
    IN_DOCKER = os.environ.get('DOCKER_CONTAINER', False) or os.path.exists('/.dockerenv')
    disable_docker_detection = os.environ.get('DISABLE_DOCKER_DETECTION', 'false').lower() == 'true'
    
    if IN_DOCKER and not disable_docker_detection:
        draw_method = getattr(args, 'draw', 'fastest')
        if draw_method not in ['term']:
            print(f"Docker detected: forcing draw mode from '{draw_method}' to 'term' (terminal plotting)")
            args.draw = 'term'
            return True
        else:
            print("Docker detected: already using 'term' mode")
            return True
    return False


def show_help():
    """
    Displays help for the 'show' mode with colorful formatting.
    """
    print(f"\n{Fore.CYAN}{Style.BRIGHT}=== SHOW MODE HELP ==={Style.RESET_ALL}")
    print(f"The {Fore.GREEN}'show'{Style.RESET_ALL} mode allows you to list and inspect cached data files.")
    print(f"{Fore.YELLOW}Usage:{Style.RESET_ALL} python run_analysis.py show <source> [keywords...]")

    print(f"\n{Fore.YELLOW}{Style.BRIGHT}Available sources:{Style.RESET_ALL}")
    print(f"  - {Fore.GREEN}csv{Style.RESET_ALL}: Converted CSV data files")
    print(f"  - {Fore.GREEN}yfinance/yf{Style.RESET_ALL}: Yahoo Finance data files")
    print(f"  - {Fore.GREEN}polygon{Style.RESET_ALL}: Polygon.io data files")
    print(f"  - {Fore.GREEN}binance{Style.RESET_ALL}: Binance data files")
    print(f"  - {Fore.GREEN}exrate{Style.RESET_ALL}: Exchange Rate API data files")
    print(f"  - {Fore.GREEN}ind{Style.RESET_ALL}: Indicator files")

    print(f"\n{Fore.YELLOW}{Style.BRIGHT}Examples:{Style.RESET_ALL}")
    print(f"  python run_analysis.py show csv                    # List all CSV files")
    print(f"  python run_analysis.py show csv gbp                # List CSV files with 'gbp' in name")
    print(f"  python run_analysis.py show yfinance               # List all Yahoo Finance files")
    print(f"  python run_analysis.py show yfinance eurusd        # List Yahoo Finance files with 'eurusd'")
    print(f"  python run_analysis.py show polygon                # List all Polygon.io files")
    print(f"  python run_analysis.py show binance                # List all Binance files")
    print(f"  python run_analysis.py show exrate                 # List all Exchange Rate API files")
    print(f"  python run_analysis.py show ind                    # List all indicator files")

    print(f"\n{Fore.YELLOW}{Style.BRIGHT}Additional options:{Style.RESET_ALL}")
    print(f"  --source <source>     Filter by data source")
    print(f"  --keywords <words>    Filter by keywords")
    print(f"  --show-start <date>   Filter by start date")
    print(f"  --show-end <date>     Filter by end date")
    print(f"  --show-rule <rule>    Calculate indicators with specific rule")
    print(f"  --draw <method>       Plot method (fastest, fast, plotly, mplfinance, seaborn, term)")
    print(f"  --export-*            Export indicators to various formats")

    print(f"\n{Fore.YELLOW}{Style.BRIGHT}Plotting methods:{Style.RESET_ALL}")
    print(f"  fastest (default)     Fastest plotting method")
    print(f"  fast                  Fast plotting with more features")
    print(f"  plotly                Interactive Plotly charts")
    print(f"  mpl/mplfinance       Matplotlib/mplfinance charts")
    print(f"  seaborn/sb           Seaborn statistical plots")
    print(f"  term                 Terminal-based plotting")

    print(f"\n{Fore.YELLOW}{Style.BRIGHT}Export options:{Style.RESET_ALL}")
    print(f"  --export-parquet      Export to parquet format")
    print(f"  --export-csv          Export to CSV format")
    print(f"  --export-json         Export to JSON format")
    print(f"  --export-indicators-info  Export indicator metadata")


def main_show_mode(args):
    """
    Main entry point for show mode.
    """
    # Force terminal mode in Docker if needed
    _force_terminal_mode_in_docker(args)
    
    # Show help if no source specified
    if not args.source:
        show_help()
        return
    
    # Handle different sources
    if args.source == 'csv':
        from .show_csv import handle_csv_show_mode
        handle_csv_show_mode(args)
    elif args.source in ['yfinance', 'yf']:
        from .show_yfinance import handle_yfinance_show_mode
        handle_yfinance_show_mode(args)
    elif args.source == 'polygon':
        from .show_polygon import handle_polygon_show_mode
        handle_polygon_show_mode(args)
    elif args.source == 'binance':
        from .show_binance import handle_binance_show_mode
        handle_binance_show_mode(args)
    elif args.source == 'exrate':
        from .show_exrate import handle_exrate_show_mode
        handle_exrate_show_mode(args)
    elif args.source == 'ind':
        from .show_indicators import handle_indicators_show_mode
        handle_indicators_show_mode(args)
    else:
        print(f"{Fore.RED}Unknown source: {args.source}{Style.RESET_ALL}")
        show_help()


if __name__ == "__main__":
    # This file is meant to be imported, not run directly
    print("This module should be imported, not run directly.")
    sys.exit(1)
