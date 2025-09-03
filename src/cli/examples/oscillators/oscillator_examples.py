# -*- coding: utf-8 -*-
"""
Oscillator CLI Examples

This module provides CLI examples for oscillator indicators.
"""

from colorama import Fore, Style

class OscillatorExamples:
    """CLI examples for oscillator indicators."""
    
    @staticmethod
    def show_rsi_examples():
        """Show RSI CLI examples."""
        print(f"{Fore.CYAN}{Style.BRIGHT}RSI (Relative Strength Index) Examples:{Style.RESET_ALL}\n")
        
        print(f"{Fore.YELLOW}Basic RSI Analysis:{Style.RESET_ALL}")
        print(f"  {Fore.GREEN}RSI with default settings:{Style.RESET_ALL}        python run_analysis.py csv --csv-file data.csv --rule RSI")
        print(f"  {Fore.GREEN}RSI with custom period:{Style.RESET_ALL}          python run_analysis.py csv --csv-file data.csv --rule RSI:14")
        print(f"  {Fore.GREEN}RSI with custom overbought/oversold:{Style.RESET_ALL} python run_analysis.py csv --csv-file data.csv --rule RSI:14,70,30")
        print()
        
        print(f"{Fore.YELLOW}RSI with Different Data Sources:{Style.RESET_ALL}")
        print(f"  {Fore.GREEN}YFinance data:{Style.RESET_ALL}                    python run_analysis.py yf -t EURUSD=X --period 6mo --rule RSI")
        print(f"  {Fore.GREEN}Binance data:{Style.RESET_ALL}                    python run_analysis.py binance --ticker BTCUSDT --interval H1 --rule RSI")
        print(f"  {Fore.GREEN}Polygon data:{Style.RESET_ALL}                    python run_analysis.py polygon --ticker AAPL --interval D1 --rule RSI")
        print()
        
        print(f"{Fore.YELLOW}RSI Visualization:{Style.RESET_ALL}")
        print(f"  {Fore.GREEN}Plotly backend:{Style.RESET_ALL}                  python run_analysis.py csv --csv-file data.csv --rule RSI -d plotly")
        print(f"  {Fore.GREEN}Seaborn backend:{Style.RESET_ALL}                 python run_analysis.py csv --csv-file data.csv --rule RSI -d seaborn")
        print(f"  {Fore.GREEN}Terminal backend:{Style.RESET_ALL}                python run_analysis.py csv --csv-file data.csv --rule RSI -d term")
        print()
    
    @staticmethod
    def show_stochastic_examples():
        """Show Stochastic CLI examples."""
        print(f"{Fore.CYAN}{Style.BRIGHT}Stochastic Oscillator Examples:{Style.RESET_ALL}\n")
        
        print(f"{Fore.YELLOW}Basic Stochastic Analysis:{Style.RESET_ALL}")
        print(f"  {Fore.GREEN}Stochastic with default settings:{Style.RESET_ALL}  python run_analysis.py csv --csv-file data.csv --rule STOCH")
        print(f"  {Fore.GREEN}Stochastic with custom periods:{Style.RESET_ALL}    python run_analysis.py csv --csv-file data.csv --rule STOCH:14,3,3")
        print()
        
        print(f"{Fore.YELLOW}Stochastic with Different Data Sources:{Style.RESET_ALL}")
        print(f"  {Fore.GREEN}YFinance data:{Style.RESET_ALL}                    python run_analysis.py yf -t AAPL --period 3mo --rule STOCH")
        print(f"  {Fore.GREEN}Binance data:{Style.RESET_ALL}                    python run_analysis.py binance --ticker ETHUSDT --interval D1 --rule STOCH")
        print()
        
        print(f"{Fore.YELLOW}Stochastic Visualization:{Style.RESET_ALL}")
        print(f"  {Fore.GREEN}Plotly backend:{Style.RESET_ALL}                  python run_analysis.py csv --csv-file data.csv --rule STOCH -d plotly")
        print(f"  {Fore.GREEN}Seaborn backend:{Style.RESET_ALL}                 python run_analysis.py csv --csv-file data.csv --rule STOCH -d seaborn")
        print()
    
    @staticmethod
    def show_cci_examples():
        """Show CCI CLI examples."""
        print(f"{Fore.CYAN}{Style.BRIGHT}CCI (Commodity Channel Index) Examples:{Style.RESET_ALL}\n")
        
        print(f"{Fore.YELLOW}Basic CCI Analysis:{Style.RESET_ALL}")
        print(f"  {Fore.GREEN}CCI with default settings:{Style.RESET_ALL}        python run_analysis.py csv --csv-file data.csv --rule CCI")
        print(f"  {Fore.GREEN}CCI with custom period:{Style.RESET_ALL}          python run_analysis.py csv --csv-file data.csv --rule CCI:20")
        print()
        
        print(f"{Fore.YELLOW}CCI with Different Data Sources:{Style.RESET_ALL}")
        print(f"  {Fore.GREEN}YFinance data:{Style.RESET_ALL}                    python run_analysis.py yf -t GBPUSD=X --period 1y --rule CCI")
        print(f"  {Fore.GREEN}Binance data:{Style.RESET_ALL}                    python run_analysis.py binance --ticker ADAUSDT --interval 4H --rule CCI")
        print()
    
    @staticmethod
    def show_williams_r_examples():
        """Show Williams %R CLI examples."""
        print(f"{Fore.CYAN}{Style.BRIGHT}Williams %R Examples:{Style.RESET_ALL}\n")
        
        print(f"{Fore.YELLOW}Basic Williams %R Analysis:{Style.RESET_ALL}")
        print(f"  {Fore.GREEN}Williams %R with default settings:{Style.RESET_ALL} python run_analysis.py csv --csv-file data.csv --rule WILLIAMS_R")
        print(f"  {Fore.GREEN}Williams %R with custom period:{Style.RESET_ALL}   python run_analysis.py csv --csv-file data.csv --rule WILLIAMS_R:14")
        print()
        
        print(f"{Fore.YELLOW}Williams %R with Different Data Sources:{Style.RESET_ALL}")
        print(f"  {Fore.GREEN}YFinance data:{Style.RESET_ALL}                    python run_analysis.py yf -t USDJPY=X --period 6mo --rule WILLIAMS_R")
        print(f"  {Fore.GREEN}Binance data:{Style.RESET_ALL}                    python run_analysis.py binance --ticker DOTUSDT --interval H1 --rule WILLIAMS_R")
        print()
    
    @staticmethod
    def show_all_oscillator_examples():
        """Show all oscillator CLI examples."""
        print(f"{Fore.CYAN}{Style.BRIGHT}OSCILLATOR INDICATORS - CLI EXAMPLES{Style.RESET_ALL}")
        print("=" * 60)
        
        OscillatorExamples.show_rsi_examples()
        print("-" * 40)
        
        OscillatorExamples.show_stochastic_examples()
        print("-" * 40)
        
        OscillatorExamples.show_cci_examples()
        print("-" * 40)
        
        OscillatorExamples.show_williams_r_examples()
        print("-" * 40)
        
        print(f"{Fore.YELLOW}General Oscillator Tips:{Style.RESET_ALL}")
        print(f"  {Fore.GREEN}Combine multiple oscillators:{Style.RESET_ALL}      python run_analysis.py csv --csv-file data.csv --rule RSI,STOCH")
        print(f"  {Fore.GREEN}Use with volume confirmation:{Style.RESET_ALL}      python run_analysis.py csv --csv-file data.csv --rule RSI --volume")
        print(f"  {Fore.GREEN}Multiple timeframe analysis:{Style.RESET_ALL}       python run_analysis.py csv --csv-file data.csv --rule RSI --timeframes H1,D1")
        print()
