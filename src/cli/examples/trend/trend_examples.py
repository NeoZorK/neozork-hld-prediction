# -*- coding: utf-8 -*-
"""
Trend Indicator CLI Examples

This module provides CLI examples for trend indicators.
"""

from colorama import Fore, Style

class TrendExamples:
    """CLI examples for trend indicators."""
    
    @staticmethod
    def show_ema_examples():
        """Show EMA CLI examples."""
        print(f"{Fore.CYAN}{Style.BRIGHT}EMA (Exponential Moving Average) Examples:{Style.RESET_ALL}\n")
        
        print(f"{Fore.YELLOW}Basic EMA Analysis:{Style.RESET_ALL}")
        print(f"  {Fore.GREEN}EMA with default settings:{Style.RESET_ALL}        python run_analysis.py csv --csv-file data.csv --rule EMA")
        print(f"  {Fore.GREEN}EMA with custom period:{Style.RESET_ALL}          python run_analysis.py csv --csv-file data.csv --rule EMA:20")
        print(f"  {Fore.GREEN}EMA with custom alpha:{Style.RESET_ALL}           python run_analysis.py csv --csv-file data.csv --rule EMA:20,0.1")
        print()
        
        print(f"{Fore.YELLOW}EMA with Different Data Sources:{Style.RESET_ALL}")
        print(f"  {Fore.GREEN}YFinance data:{Style.RESET_ALL}                    python run_analysis.py yf -t EURUSD=X --period 6mo --rule EMA")
        print(f"  {Fore.GREEN}Binance data:{Style.RESET_ALL}                    python run_analysis.py binance --ticker BTCUSDT --interval H1 --rule EMA")
        print(f"  {Fore.GREEN}Polygon data:{Style.RESET_ALL}                    python run_analysis.py polygon --ticker AAPL --interval D1 --rule EMA")
        print()
        
        print(f"{Fore.YELLOW}EMA Visualization:{Style.RESET_ALL}")
        print(f"  {Fore.GREEN}Plotly backend:{Style.RESET_ALL}                  python run_analysis.py csv --csv-file data.csv --rule EMA -d plotly")
        print(f"  {Fore.GREEN}Seaborn backend:{Style.RESET_ALL}                 python run_analysis.py csv --csv-file data.csv --rule EMA -d seaborn")
        print(f"  {Fore.GREEN}Terminal backend:{Style.RESET_ALL}                python run_analysis.py csv --csv-file data.csv --rule EMA -d term")
        print()
    
    @staticmethod
    def show_sma_examples():
        """Show SMA CLI examples."""
        print(f"{Fore.CYAN}{Style.BRIGHT}SMA (Simple Moving Average) Examples:{Style.RESET_ALL}\n")
        
        print(f"{Fore.YELLOW}Basic SMA Analysis:{Style.RESET_ALL}")
        print(f"  {Fore.GREEN}SMA with default settings:{Style.RESET_ALL}        python run_analysis.py csv --csv-file data.csv --rule SMA")
        print(f"  {Fore.GREEN}SMA with custom period:{Style.RESET_ALL}          python run_analysis.py csv --csv-file data.csv --rule SMA:50")
        print()
        
        print(f"{Fore.YELLOW}SMA with Different Data Sources:{Style.RESET_ALL}")
        print(f"  {Fore.GREEN}YFinance data:{Style.RESET_ALL}                    python run_analysis.py yf -t AAPL --period 1y --rule SMA")
        print(f"  {Fore.GREEN}Binance data:{Style.RESET_ALL}                    python run_analysis.py binance --ticker ETHUSDT --interval D1 --rule SMA")
        print()
        
        print(f"{Fore.YELLOW}SMA Visualization:{Style.RESET_ALL}")
        print(f"  {Fore.GREEN}Plotly backend:{Style.RESET_ALL}                  python run_analysis.py csv --csv-file data.csv --rule SMA -d plotly")
        print(f"  {Fore.GREEN}Seaborn backend:{Style.RESET_ALL}                 python run_analysis.py csv --csv-file data.csv --rule SMA -d seaborn")
        print()
    
    @staticmethod
    def show_adx_examples():
        """Show ADX CLI examples."""
        print(f"{Fore.CYAN}{Style.BRIGHT}ADX (Average Directional Index) Examples:{Style.RESET_ALL}\n")
        
        print(f"{Fore.YELLOW}Basic ADX Analysis:{Style.RESET_ALL}")
        print(f"  {Fore.GREEN}ADX with default settings:{Style.RESET_ALL}        python run_analysis.py csv --csv-file data.csv --rule ADX")
        print(f"  {Fore.GREEN}ADX with custom period:{Style.RESET_ALL}          python run_analysis.py csv --csv-file data.csv --rule ADX:14")
        print()
        
        print(f"{Fore.YELLOW}ADX with Different Data Sources:{Style.RESET_ALL}")
        print(f"  {Fore.GREEN}YFinance data:{Style.RESET_ALL}                    python run_analysis.py yf -t GBPUSD=X --period 6mo --rule ADX")
        print(f"  {Fore.GREEN}Binance data:{Style.RESET_ALL}                    python run_analysis.py binance --ticker ADAUSDT --interval 4H --rule ADX")
        print()
    
    @staticmethod
    def show_sar_examples():
        """Show SAR CLI examples."""
        print(f"{Fore.CYAN}{Style.BRIGHT}SAR (Parabolic SAR) Examples:{Style.RESET_ALL}\n")
        
        print(f"{Fore.YELLOW}Basic SAR Analysis:{Style.RESET_ALL}")
        print(f"  {Fore.GREEN}SAR with default settings:{Style.RESET_ALL}        python run_analysis.py csv --csv-file data.csv --rule SAR")
        print(f"  {Fore.GREEN}SAR with custom acceleration:{Style.RESET_ALL}     python run_analysis.py csv --csv-file data.csv --rule SAR:0.02")
        print(f"  {Fore.GREEN}SAR with custom maximum:{Style.RESET_ALL}          python run_analysis.py csv --csv-file data.csv --rule SAR:0.02,0.2")
        print()
        
        print(f"{Fore.YELLOW}SAR with Different Data Sources:{Style.RESET_ALL}")
        print(f"  {Fore.GREEN}YFinance data:{Style.RESET_ALL}                    python run_analysis.py yf -t USDJPY=X --period 3mo --rule SAR")
        print(f"  {Fore.GREEN}Binance data:{Style.RESET_ALL}                    python run_analysis.py binance --ticker DOTUSDT --interval H1 --rule SAR")
        print()
    
    @staticmethod
    def show_supertrend_examples():
        """Show SuperTrend CLI examples."""
        print(f"{Fore.CYAN}{Style.BRIGHT}SuperTrend Examples:{Style.RESET_ALL}\n")
        
        print(f"{Fore.YELLOW}Basic SuperTrend Analysis:{Style.RESET_ALL}")
        print(f"  {Fore.GREEN}SuperTrend with default settings:{Style.RESET_ALL}  python run_analysis.py csv --csv-file data.csv --rule SUPERTREND")
        print(f"  {Fore.GREEN}SuperTrend with custom period:{Style.RESET_ALL}     python run_analysis.py csv --csv-file data.csv --rule SUPERTREND:10")
        print(f"  {Fore.GREEN}SuperTrend with custom multiplier:{Style.RESET_ALL} python run_analysis.py csv --csv-file data.csv --rule SUPERTREND:10,3")
        print()
        
        print(f"{Fore.YELLOW}SuperTrend with Different Data Sources:{Style.RESET_ALL}")
        print(f"  {Fore.GREEN}YFinance data:{Style.RESET_ALL}                    python run_analysis.py yf -t EURUSD=X --period 6mo --rule SUPERTREND")
        print(f"  {Fore.GREEN}Binance data:{Style.RESET_ALL}                    python run_analysis.py binance --ticker BTCUSDT --interval D1 --rule SUPERTREND")
        print()
    
    @staticmethod
    def show_wave_examples():
        """Show Wave CLI examples."""
        print(f"{Fore.CYAN}{Style.BRIGHT}Wave Examples:{Style.RESET_ALL}\n")
        
        print(f"{Fore.YELLOW}Basic Wave Analysis:{Style.RESET_ALL}")
        print(f"  {Fore.GREEN}Wave with default settings:{Style.RESET_ALL}        python run_analysis.py csv --csv-file data.csv --rule wave:339,10,2,fast,22,11,4,fast,prime,22,close")
        print(f"  {Fore.GREEN}Wave with custom parameters:{Style.RESET_ALL}       python run_analysis.py csv --csv-file data.csv --rule wave:200,10,20,fast,50,5,10,fast,prime,30,close")
        print(f"  {Fore.GREEN}Wave for short-term analysis:{Style.RESET_ALL}      python run_analysis.py csv --csv-file data.csv --rule wave:100,5,10,fast,25,3,5,fast,prime,15,close")
        print()
        
        print(f"{Fore.YELLOW}Wave with Different Data Sources:{Style.RESET_ALL}")
        print(f"  {Fore.GREEN}YFinance data:{Style.RESET_ALL}                    python run_analysis.py yf -t EURUSD=X --period 6mo --rule wave:200,10,20,fast,50,5,10,fast,prime,30,close")
        print(f"  {Fore.GREEN}Binance data:{Style.RESET_ALL}                    python run_analysis.py binance --ticker BTCUSDT --interval H1 --rule wave:300,15,30,fast,75,8,15,fast,prime,25,close")
        print(f"  {Fore.GREEN}Polygon data:{Style.RESET_ALL}                    python run_analysis.py polygon --ticker AAPL --interval D1 --rule wave:250,12,25,fast,60,6,12,fast,prime,25,close")
        print()
        
        print(f"{Fore.YELLOW}Wave Visualization:{Style.RESET_ALL}")
        print(f"  {Fore.GREEN}Plotly backend:{Style.RESET_ALL}                  python run_analysis.py csv --csv-file data.csv --rule wave:200,10,20,fast,50,5,10,fast,prime,30,close -d plotly")
        print(f"  {Fore.GREEN}Seaborn backend:{Style.RESET_ALL}                 python run_analysis.py csv --csv-file data.csv --rule wave:200,10,20,fast,50,5,10,fast,prime,30,close -d seaborn")
        print(f"  {Fore.GREEN}Terminal backend:{Style.RESET_ALL}                python run_analysis.py csv --csv-file data.csv --rule wave:200,10,20,fast,50,5,10,fast,prime,30,close -d term")
        print()
        
        print(f"{Fore.YELLOW}Wave Trading Strategies:{Style.RESET_ALL}")
        print(f"  {Fore.GREEN}Conservative strategy:{Style.RESET_ALL}            python run_analysis.py csv --csv-file data.csv --rule wave:400,25,50,slow,100,15,30,slow,tertiary,40,close")
        print(f"  {Fore.GREEN}Aggressive strategy:{Style.RESET_ALL}              python run_analysis.py csv --csv-file data.csv --rule wave:100,5,10,fast,25,3,5,fast,prime,15,close")
        print(f"  {Fore.GREEN}Balanced strategy:{Style.RESET_ALL}                python run_analysis.py csv --csv-file data.csv --rule wave:250,12,25,fast,60,6,12,fast,prime,25,close")
        print()
    
    @staticmethod
    def show_all_trend_examples():
        """Show all trend CLI examples."""
        print(f"{Fore.CYAN}{Style.BRIGHT}TREND INDICATORS - CLI EXAMPLES{Style.RESET_ALL}")
        print("=" * 60)
        
        TrendExamples.show_ema_examples()
        print("-" * 40)
        
        TrendExamples.show_sma_examples()
        print("-" * 40)
        
        TrendExamples.show_adx_examples()
        print("-" * 40)
        
        TrendExamples.show_sar_examples()
        print("-" * 40)
        
        TrendExamples.show_supertrend_examples()
        print("-" * 40)
        
        TrendExamples.show_wave_examples()
        print("-" * 40)
        
        print(f"{Fore.YELLOW}General Trend Tips:{Style.RESET_ALL}")
        print(f"  {Fore.GREEN}Combine multiple moving averages:{Style.RESET_ALL}  python run_analysis.py csv --csv-file data.csv --rule EMA,SMA")
        print(f"  {Fore.GREEN}Use with volume confirmation:{Style.RESET_ALL}      python run_analysis.py csv --csv-file data.csv --rule EMA --volume")
        print(f"  {Fore.GREEN}Multiple timeframe analysis:{Style.RESET_ALL}       python run_analysis.py csv --csv-file data.csv --rule EMA --timeframes H1,D1")
        print()
