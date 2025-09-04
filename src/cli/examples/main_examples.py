# -*- coding: utf-8 -*-
"""
Main CLI Examples Module

This module provides access to all CLI examples organized by indicator groups.
"""

from colorama import Fore, Style
from .oscillators import OscillatorExamples
from .trend import TrendExamples
from .momentum import MomentumExamples

def show_all_cli_examples():
    """Show all CLI examples organized by indicator groups."""
    print(f"{Fore.CYAN}{Style.BRIGHT}COMPREHENSIVE CLI EXAMPLES - NEOZORk HLD PREDICTION{Style.RESET_ALL}")
    print("=" * 80)
    print(f"{Fore.YELLOW}This guide provides CLI examples for all indicator types and data sources{Style.RESET_ALL}")
    print()
    
    # Show oscillator examples
    OscillatorExamples.show_all_oscillator_examples()
    print("=" * 80)
    
    # Show trend examples
    TrendExamples.show_all_trend_examples()
    print("=" * 80)
    
    # Show momentum examples
    MomentumExamples.show_all_momentum_examples()
    print("=" * 80)
    
    # Show general usage tips
    show_general_usage_tips()

def show_general_usage_tips():
    """Show general CLI usage tips."""
    print(f"{Fore.CYAN}{Style.BRIGHT}GENERAL CLI USAGE TIPS{Style.RESET_ALL}")
    print("=" * 60)
    
    print(f"{Fore.YELLOW}Data Source Selection:{Style.RESET_ALL}")
    print(f"  {Fore.GREEN}CSV files:{Style.RESET_ALL}                        python run_analysis.py csv --csv-file data.csv --rule RSI")
    print(f"  {Fore.GREEN}YFinance:{Style.RESET_ALL}                         python run_analysis.py yf -t EURUSD=X --period 6mo --rule RSI")
    print(f"  {Fore.GREEN}Binance:{Style.RESET_ALL}                          python run_analysis.py binance --ticker BTCUSDT --interval H1 --rule RSI")
    print(f"  {Fore.GREEN}Polygon:{Style.RESET_ALL}                          python run_analysis.py polygon --ticker AAPL --interval D1 --rule RSI")
    print()
    
    print(f"{Fore.YELLOW}Visualization Backends:{Style.RESET_ALL}")
    print(f"  {Fore.GREEN}Plotly (interactive):{Style.RESET_ALL}              python run_analysis.py csv --csv-file data.csv --rule RSI -d plotly")
    print(f"  {Fore.GREEN}Seaborn (static):{Style.RESET_ALL}                  python run_analysis.py csv --csv-file data.csv --rule RSI -d seaborn")
    print(f"  {Fore.GREEN}MPLFinance (candlestick):{Style.RESET_ALL}          python run_analysis.py csv --csv-file data.csv --rule RSI -d mpl")
    print(f"  {Fore.GREEN}Terminal (text):{Style.RESET_ALL}                   python run_analysis.py csv --csv-file data.csv --rule RSI -d term")
    print(f"  {Fore.GREEN}Fastest (no plot):{Style.RESET_ALL}                 python run_analysis.py csv --csv-file data.csv --rule RSI -d fastest")
    print()
    
    print(f"{Fore.YELLOW}Export Options:{Style.RESET_ALL}")
    print(f"  {Fore.GREEN}Export to Parquet:{Style.RESET_ALL}                 python run_analysis.py csv --csv-file data.csv --rule RSI --export-parquet")
    print(f"  {Fore.GREEN}Export to CSV:{Style.RESET_ALL}                     python run_analysis.py csv --csv-file data.csv --rule RSI --export-csv")
    print(f"  {Fore.GREEN}Export both formats:{Style.RESET_ALL}                python run_analysis.py csv --csv-file data.csv --rule RSI --export-parquet --export-csv")
    print()
    
    print(f"{Fore.YELLOW}Advanced Features:{Style.RESET_ALL}")
    print(f"  {Fore.GREEN}Multiple indicators:{Style.RESET_ALL}                python run_analysis.py csv --csv-file data.csv --rule RSI,EMA,MACD")
    print(f"  {Fore.GREEN}Custom parameters:{Style.RESET_ALL}                  python run_analysis.py csv --csv-file data.csv --rule RSI:14,70,30")
    print(f"  {Fore.GREEN}Point size specification:{Style.RESET_ALL}           python run_analysis.py csv --csv-file data.csv --point 0.00001 --rule RSI")
    print(f"  {Fore.GREEN}Interactive mode:{Style.RESET_ALL}                  python run_analysis.py interactive")
    print()
    
    print(f"{Fore.YELLOW}Help and Information:{Style.RESET_ALL}")
    print(f"  {Fore.GREEN}Show all indicators:{Style.RESET_ALL}                python run_analysis.py --indicators")
    print(f"  {Fore.GREEN}Show specific group:{Style.RESET_ALL}                python run_analysis.py --indicators oscillators")
    print(f"  {Fore.GREEN}Show specific indicator:{Style.RESET_ALL}            python run_analysis.py --indicators oscillators rsi")
    print(f"  {Fore.GREEN}Show trading metrics:{Style.RESET_ALL}               python run_analysis.py --metric")
    print(f"  {Fore.GREEN}Show trading tips:{Style.RESET_ALL}                  python run_analysis.py --metric tips")
    print()

def show_indicator_group_examples(group_name: str):
    """Show examples for a specific indicator group."""
    group_name = group_name.lower()
    
    if group_name == 'oscillators':
        OscillatorExamples.show_all_oscillator_examples()
    elif group_name == 'trend':
        TrendExamples.show_all_trend_examples()
    elif group_name == 'momentum':
        MomentumExamples.show_all_momentum_examples()
    else:
        print(f"{Fore.RED}Unknown indicator group: {group_name}{Style.RESET_ALL}")
        print(f"Available groups: oscillators, trend, momentum")
        show_all_cli_examples()

if __name__ == "__main__":
    show_all_cli_examples()
