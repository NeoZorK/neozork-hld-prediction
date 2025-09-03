# -*- coding: utf-8 -*-
"""
Momentum Indicator CLI Examples

This module provides CLI examples for momentum indicators.
"""

from colorama import Fore, Style

class MomentumExamples:
    """CLI examples for momentum indicators."""
    
    @staticmethod
    def show_macd_examples():
        """Show MACD CLI examples."""
        print(f"{Fore.CYAN}{Style.BRIGHT}MACD (Moving Average Convergence Divergence) Examples:{Style.RESET_ALL}\n")
        
        print(f"{Fore.YELLOW}Basic MACD Analysis:{Style.RESET_ALL}")
        print(f"  {Fore.GREEN}MACD with default settings:{Style.RESET_ALL}        python run_analysis.py csv --csv-file data.csv --rule MACD")
        print(f"  {Fore.GREEN}MACD with custom periods:{Style.RESET_ALL}         python run_analysis.py csv --csv-file data.csv --rule MACD:12,26,9")
        print()
        
        print(f"{Fore.YELLOW}MACD with Different Data Sources:{Style.RESET_ALL}")
        print(f"  {Fore.GREEN}YFinance data:{Style.RESET_ALL}                    python run_analysis.py yf -t EURUSD=X --period 6mo --rule MACD")
        print(f"  {Fore.GREEN}Binance data:{Style.RESET_ALL}                    python run_analysis.py binance --ticker BTCUSDT --interval H1 --rule MACD")
        print(f"  {Fore.GREEN}Polygon data:{Style.RESET_ALL}                    python run_analysis.py polygon --ticker AAPL --interval D1 --rule MACD")
        print()
        
        print(f"{Fore.YELLOW}MACD Visualization:{Style.RESET_ALL}")
        print(f"  {Fore.GREEN}Plotly backend:{Style.RESET_ALL}                  python run_analysis.py csv --csv-file data.csv --rule MACD -d plotly")
        print(f"  {Fore.GREEN}Seaborn backend:{Style.RESET_ALL}                 python run_analysis.py csv --csv-file data.csv --rule MACD -d seaborn")
        print(f"  {Fore.GREEN}Terminal backend:{Style.RESET_ALL}                python run_analysis.py csv --csv-file data.csv --rule MACD -d term")
        print()
    
    @staticmethod
    def show_stoch_oscillator_examples():
        """Show Stochastic Oscillator CLI examples."""
        print(f"{Fore.CYAN}{Style.BRIGHT}Stochastic Oscillator Examples:{Style.RESET_ALL}\n")
        
        print(f"{Fore.YELLOW}Basic Stochastic Analysis:{Style.RESET_ALL}")
        print(f"  {Fore.GREEN}Stochastic with default settings:{Style.RESET_ALL}  python run_analysis.py csv --csv-file data.csv --rule STOCHOSC")
        print(f"  {Fore.GREEN}Stochastic with custom periods:{Style.RESET_ALL}    python run_analysis.py csv --csv-file data.csv --rule STOCHOSC:14,3,3")
        print()
        
        print(f"{Fore.YELLOW}Stochastic with Different Data Sources:{Style.RESET_ALL}")
        print(f"  {Fore.GREEN}YFinance data:{Style.RESET_ALL}                    python run_analysis.py yf -t AAPL --period 3mo --rule STOCHOSC")
        print(f"  {Fore.GREEN}Binance data:{Style.RESET_ALL}                    python run_analysis.py binance --ticker ETHUSDT --interval D1 --rule STOCHOSC")
        print()
        
        print(f"{Fore.YELLOW}Stochastic Visualization:{Style.RESET_ALL}")
        print(f"  {Fore.GREEN}Plotly backend:{Style.RESET_ALL}                  python run_analysis.py csv --csv-file data.csv --rule STOCHOSC -d plotly")
        print(f"  {Fore.GREEN}Seaborn backend:{Style.RESET_ALL}                 python run_analysis.py csv --csv-file data.csv --rule STOCHOSC -d seaborn")
        print()
    
    @staticmethod
    def show_roc_examples():
        """Show ROC CLI examples."""
        print(f"{Fore.CYAN}{Style.BRIGHT}ROC (Rate of Change) Examples:{Style.RESET_ALL}\n")
        
        print(f"{Fore.YELLOW}Basic ROC Analysis:{Style.RESET_ALL}")
        print(f"  {Fore.GREEN}ROC with default settings:{Style.RESET_ALL}        python run_analysis.py csv --csv-file data.csv --rule ROC")
        print(f"  {Fore.GREEN}ROC with custom period:{Style.RESET_ALL}          python run_analysis.py csv --csv-file data.csv --rule ROC:20")
        print()
        
        print(f"{Fore.YELLOW}ROC with Different Data Sources:{Style.RESET_ALL}")
        print(f"  {Fore.GREEN}YFinance data:{Style.RESET_ALL}                    python run_analysis.py yf -t GBPUSD=X --period 6mo --rule ROC")
        print(f"  {Fore.GREEN}Binance data:{Style.RESET_ALL}                    python run_analysis.py binance --ticker ADAUSDT --interval 4H --rule ROC")
        print()
    
    @staticmethod
    def show_momentum_examples():
        """Show Momentum CLI examples."""
        print(f"{Fore.CYAN}{Style.BRIGHT}Momentum Examples:{Style.RESET_ALL}\n")
        
        print(f"{Fore.YELLOW}Basic Momentum Analysis:{Style.RESET_ALL}")
        print(f"  {Fore.GREEN}Momentum with default settings:{Style.RESET_ALL}    python run_analysis.py csv --csv-file data.csv --rule MOM")
        print(f"  {Fore.GREEN}Momentum with custom period:{Style.RESET_ALL}      python run_analysis.py csv --csv-file data.csv --rule MOM:20")
        print()
        
        print(f"{Fore.YELLOW}Momentum with Different Data Sources:{Style.RESET_ALL}")
        print(f"  {Fore.GREEN}YFinance data:{Style.RESET_ALL}                    python run_analysis.py yf -t USDJPY=X --period 3mo --rule MOM")
        print(f"  {Fore.GREEN}Binance data:{Style.RESET_ALL}                    python run_analysis.py binance --ticker DOTUSDT --interval H1 --rule MOM")
        print()
    
    @staticmethod
    def show_all_momentum_examples():
        """Show all momentum CLI examples."""
        print(f"{Fore.CYAN}{Style.BRIGHT}MOMENTUM INDICATORS - CLI EXAMPLES{Style.RESET_ALL}")
        print("=" * 60)
        
        MomentumExamples.show_macd_examples()
        print("-" * 40)
        
        MomentumExamples.show_stoch_oscillator_examples()
        print("-" * 40)
        
        MomentumExamples.show_roc_examples()
        print("-" * 40)
        
        MomentumExamples.show_momentum_examples()
        print("-" * 40)
        
        print(f"{Fore.YELLOW}General Momentum Tips:{Style.RESET_ALL}")
        print(f"  {Fore.GREEN}Combine momentum indicators:{Style.RESET_ALL}       python run_analysis.py csv --csv-file data.csv --rule MACD,STOCHOSC")
        print(f"  {Fore.GREEN}Use with trend confirmation:{Style.RESET_ALL}      python run_analysis.py csv --csv-file data.csv --rule MACD --trend")
        print(f"  {Fore.GREEN}Multiple timeframe analysis:{Style.RESET_ALL}       python run_analysis.py csv --csv-file data.csv --rule MACD --timeframes H1,D1")
        print()
