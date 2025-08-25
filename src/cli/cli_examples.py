# -*- coding: utf-8 -*-
# src/cli/cli_examples.py

"""
CLI examples and help text for the analysis tool.
All comments and text are in English.
"""

from colorama import Fore, Style


def show_cli_examples_colored():
    """
    Show command line interface (CLI) examples for the analysis tool.
    """
    print(f"{Fore.CYAN}{Style.BRIGHT}EXAMPLES (run: python run_analysis.py --examples):{Style.RESET_ALL}\n")
    
    print(f"{Fore.YELLOW}{Style.BRIGHT}1. INDICATOR DISCOVERY & HELP{Style.RESET_ALL}")
    print(f"  {Fore.GREEN}List all indicators:{Style.RESET_ALL}        python run_analysis.py --indicators")
    print(f"  {Fore.GREEN}Show oscillators:{Style.RESET_ALL}           python run_analysis.py --indicators oscillators")
    print(f"  {Fore.GREEN}Show RSI info:{Style.RESET_ALL}              python run_analysis.py --indicators oscillators rsi")
    print(f"  {Fore.GREEN}Show trend indicators:{Style.RESET_ALL}      python run_analysis.py --indicators trend")
    print(f"  {Fore.GREEN}Show MACD info:{Style.RESET_ALL}             python run_analysis.py --indicators momentum macd")
    print(f"  {Fore.GREEN}Interactive mode:{Style.RESET_ALL}           python run_analysis.py interactive")
    print(f"  {Fore.GREEN}Interactive mode (flag):{Style.RESET_ALL}    python run_analysis.py --interactive")
    print(f"  {Fore.GREEN}Interactive mode (short):{Style.RESET_ALL}   python run_analysis.py -i")
    print()

    print(f"{Fore.YELLOW}{Style.BRIGHT}2. TRADING METRICS ENCYCLOPEDIA{Style.RESET_ALL}")
    print(f"  {Fore.GREEN}Show all metrics and tips:{Style.RESET_ALL}  python run_analysis.py --metric")
    print(f"  {Fore.GREEN}Show only metrics:{Style.RESET_ALL}          python run_analysis.py --metric metrics")
    print(f"  {Fore.GREEN}Show only tips:{Style.RESET_ALL}             python run_analysis.py --metric tips")
    print(f"  {Fore.GREEN}Search for winrate:{Style.RESET_ALL}         python run_analysis.py --metric winrate")
    print(f"  {Fore.GREEN}Search for profit factor:{Style.RESET_ALL}   python run_analysis.py --metric profit factor")
    print(f"  {Fore.GREEN}Filter metrics by keyword:{Style.RESET_ALL}  python run_analysis.py --metric metrics sharpe")
    print(f"  {Fore.GREEN}Filter tips by keyword:{Style.RESET_ALL}     python run_analysis.py --metric tips monte carlo")
    print(f"  {Fore.GREEN}Interactive encyclopedia:{Style.RESET_ALL}   python run_analysis.py -i (then select option 10)")
    print()

    print(f"{Fore.YELLOW}{Style.BRIGHT}3. DEMO DATA MODES{Style.RESET_ALL}")
    print(f"  {Fore.GREEN}Run with demo data (default rule):{Style.RESET_ALL}     python run_analysis.py demo")
    print(f"  {Fore.GREEN}Run with demo data using mplfinance:{Style.RESET_ALL}    python run_analysis.py demo -d mpl")
    print(f"  {Fore.GREEN}Run with demo data and RSI rule:{Style.RESET_ALL}       python run_analysis.py demo --rule RSI")
    print(f"  {Fore.GREEN}Run with demo data and RSI, plotly backend:{Style.RESET_ALL} python run_analysis.py demo --rule RSI -d plotly")
    print(f"  {Fore.GREEN}Run with demo data using terminal backend:{Style.RESET_ALL} python run_analysis.py demo -d term")
    print(f"  {Fore.GREEN}Export demo results:{Style.RESET_ALL}                   python run_analysis.py demo --rule RSI --export-parquet --export-csv")
    print()

    print(f"{Fore.YELLOW}{Style.BRIGHT}4. CSV FILE MODES{Style.RESET_ALL}")
    print(f"  {Fore.GREEN}Basic CSV mode:{Style.RESET_ALL}                       python run_analysis.py csv --csv-file data.csv --point 0.01")
    print(f"  {Fore.GREEN}CSV with RSI rule:{Style.RESET_ALL}                    python run_analysis.py csv --csv-file data.csv --point 0.01 --rule RSI")
    print(f"  {Fore.GREEN}CSV with mplfinance backend:{Style.RESET_ALL}          python run_analysis.py csv --csv-file data.csv --point 0.01 -d mplfinance")
    print(f"  {Fore.GREEN}CSV with PV rule, fastest backend:{Style.RESET_ALL}     python run_analysis.py csv --csv-file data.csv --point 0.01 --rule PV -d fastest")
    print(f"  {Fore.GREEN}CSV with PV rule, seaborn backend:{Style.RESET_ALL}     python run_analysis.py csv --csv-file data.csv --point 0.01 --rule PV -d seaborn")
    print(f"  {Fore.GREEN}CSV with PV rule, terminal backend:{Style.RESET_ALL}    python run_analysis.py csv --csv-file data.csv --point 0.01 --rule PV -d term")
    print()
    print(f"{Fore.YELLOW}{Style.BRIGHT}4b. CSV FOLDER MODES (NEW){Style.RESET_ALL}")
    print(f"  {Fore.GREEN}Process all CSV files in folder:{Style.RESET_ALL}       python run_analysis.py csv --csv-folder mql5_feed --point 0.00001")
    print(f"  {Fore.GREEN}Process folder with RSI rule:{Style.RESET_ALL}          python run_analysis.py csv --csv-folder mql5_feed --point 0.00001 --rule RSI")
    print(f"  {Fore.GREEN}Process folder with fastest backend:{Style.RESET_ALL}    python run_analysis.py csv --csv-folder mql5_feed --point 0.00001 -d fastest")
    print(f"  {Fore.GREEN}Process folder with export:{Style.RESET_ALL}            python run_analysis.py csv --csv-folder mql5_feed --point 0.00001 --export-parquet")
    print()

    print(f"{Fore.YELLOW}{Style.BRIGHT}5. YAHOO FINANCE (YF) MODES{Style.RESET_ALL}")
    print(f"  {Fore.GREEN}EURUSD=X, 1mo, point size:{Style.RESET_ALL}            python run_analysis.py yf -t EURUSD=X --period 1mo --point 0.00001")
    print(f"  {Fore.GREEN}AAPL, 6mo, point size:{Style.RESET_ALL}                python run_analysis.py yfinance -t AAPL --period 6mo --point 0.01")
    print(f"  {Fore.GREEN}BTC-USD, date range, point size:{Style.RESET_ALL}       python run_analysis.py yf -t BTC-USD --start 2023-01-01 --end 2023-12-31 --point 0.01")
    print(f"  {Fore.GREEN}EURUSD=X, date range, mpl backend:{Style.RESET_ALL}     python run_analysis.py yf -t EURUSD=X --start 2024-01-01 --end 2024-04-18 --point 0.00001 -d mpl")
    print(f"  {Fore.GREEN}AAPL, 1y, RSI rule:{Style.RESET_ALL}                   python run_analysis.py yf -t AAPL --period 1y --rule RSI")
    print()

    print(f"{Fore.YELLOW}{Style.BRIGHT}6. POLYGON.IO MODES{Style.RESET_ALL}")
    print(f"  {Fore.GREEN}AAPL, D1, date range, point size:{Style.RESET_ALL}      python run_analysis.py polygon --ticker AAPL --interval D1 --start 2023-01-01 --end 2023-12-31 --point 0.01")
    print(f"  {Fore.GREEN}EURUSD, H1, date range, RSI rule:{Style.RESET_ALL}      python run_analysis.py polygon --ticker EURUSD --interval H1 --start 2022-01-01 --end 2022-06-01 --point 0.00001 --rule RSI")
    print()

    print(f"{Fore.YELLOW}{Style.BRIGHT}7. BINANCE MODES{Style.RESET_ALL}")
    print(f"  {Fore.GREEN}BTCUSDT, H1, date range, point size:{Style.RESET_ALL}   python run_analysis.py binance --ticker BTCUSDT --interval H1 --start 2024-01-01 --end 2024-04-18 --point 0.01")
    print(f"  {Fore.GREEN}ETHUSDT, D1, date range, RSI rule:{Style.RESET_ALL}     python run_analysis.py binance --ticker ETHUSDT --interval D1 --start 2023-01-01 --end 2023-12-31 --point 0.01 --rule RSI")
    print(f"  {Fore.GREEN}ETHUSDT, D1, date range, RSI rule with SeaBorn plot:{Style.RESET_ALL} python run_analysis.py binance --ticker ETHUSDT --interval D1 --start 2023-01-01 --end 2023-12-31 --point 0.01 --rule RSI -d sb")
    print()

    print(f"{Fore.YELLOW}{Style.BRIGHT}8. EXCHANGE RATE API MODES{Style.RESET_ALL}")
    print(f"  {Fore.GREEN}Free Plan - Current rates only:{Style.RESET_ALL}        python run_analysis.py exrate --ticker EURUSD --interval D1 --point 0.00001")
    print(f"  {Fore.GREEN}Paid Plan - Historical data with date range:{Style.RESET_ALL} python run_analysis.py exrate --ticker GBPJPY --interval D1 --start 2023-01-01 --end 2023-12-31 --point 0.01 --rule RSI")
    print(f"  {Fore.GREEN}Paid Plan - Historical data with RSI rule, plotly backend:{Style.RESET_ALL} python run_analysis.py exrate --ticker USDCAD --interval D1 --start 2024-01-01 --end 2024-06-01 --point 0.00001 --rule RSI -d plotly")
    print(f"  {Fore.GREEN}Free Plan - Current rate with terminal plotting:{Style.RESET_ALL} python run_analysis.py exrate --ticker AUDUSD --interval D1 --point 0.00001 -d term")
    print()

    print(f"{Fore.YELLOW}{Style.BRIGHT}9. SHOW MODE (CACHE/FILES){Style.RESET_ALL}")
    print(f"  {Fore.GREEN}Show all YFinance files:{Style.RESET_ALL}               python run_analysis.py show yf")
    print(f"  {Fore.GREEN}Show YFinance files with 'aapl' and 'mn1' in name:{Style.RESET_ALL} python run_analysis.py show yf aapl mn1")
    print(f"  {Fore.GREEN}Show Binance files with 'btc' in name:{Style.RESET_ALL}  python run_analysis.py show binance btc")
    print(f"  {Fore.GREEN}Show Binance files with 'btc' in name with SeaBorn plot:{Style.RESET_ALL} python run_analysis.py show binance btc -d seaborn")
    print(f"  {Fore.GREEN}Show CSV files with EURUSD MN1:{Style.RESET_ALL}        python run_analysis.py show csv EURUSD MN1")
    print(f"  {Fore.GREEN}Show Polygon files with AAPL 2023:{Style.RESET_ALL}     python run_analysis.py show polygon AAPL 2023")
    print(f"  {Fore.GREEN}Show YF files with RSI rule:{Style.RESET_ALL}           python run_analysis.py show yf --show-rule RSI")
    print(f"  {Fore.GREEN}Show YF files for date range:{Style.RESET_ALL}          python run_analysis.py show yf --show-start 2023-01-01 --show-end 2023-12-31")
    print(f"  {Fore.GREEN}Show CSV with Fibo standard levels:{Style.RESET_ALL}    python run_analysis.py show csv mn1 -d fast --rule fibo:all")
    print(f"  {Fore.GREEN}Show CSV with Fibo custom levels:{Style.RESET_ALL}      python run_analysis.py show csv mn1 -d fast --rule fibo:0.382,0.618,0.786")
    print(f"  {Fore.GREEN}Show CSV with Donchian Channel:{Style.RESET_ALL}        python run_analysis.py show csv mn1 -d fast --rule donchain:20")
    print()

    print(f"{Fore.YELLOW}{Style.BRIGHT}10. EXPORT EXAMPLES{Style.RESET_ALL}")
    print(f"  {Fore.GREEN}Export to parquet:{Style.RESET_ALL}                     python run_analysis.py demo --rule RSI --export-parquet")
    print(f"  {Fore.GREEN}Export to CSV:{Style.RESET_ALL}                         python run_analysis.py demo --rule RSI --export-csv")
    print(f"  {Fore.GREEN}Export to JSON:{Style.RESET_ALL}                        python run_analysis.py demo --rule RSI --export-json")
    print(f"  {Fore.GREEN}Export indicator metadata:{Style.RESET_ALL}             python run_analysis.py demo --rule RSI --export-indicators-info")
    print(f"  {Fore.GREEN}Export to all formats:{Style.RESET_ALL}                 python run_analysis.py demo --rule RSI --export-parquet --export-csv --export-json --export-indicators-info")
    print()

    print(f"{Fore.YELLOW}{Style.BRIGHT}11. OHLCV & AUTO RULE EXAMPLES{Style.RESET_ALL}")
    print(f"  {Fore.GREEN}CSV file, OHLCV rule (candlestick only):{Style.RESET_ALL} python run_analysis.py csv --csv-file data.csv --point 0.01 --rule OHLCV")
    print(f"  {Fore.GREEN}CSV file, AUTO rule (all columns, auto-plot, mpl backend):{Style.RESET_ALL} python run_analysis.py csv --csv-file data.csv --point 0.01 --rule AUTO -d mpl")
    print(f"  {Fore.GREEN}CSV file, AUTO rule (all columns, auto-plot, terminal backend):{Style.RESET_ALL} python run_analysis.py csv --csv-file data.csv --point 0.01 --rule AUTO -d term")
    print(f"  {Fore.GREEN}Show mode, OHLCV rule (candlestick only):{Style.RESET_ALL} python run_analysis.py show csv EURUSD MN1 --rule OHLCV")
    print(f"  {Fore.GREEN}Show mode, AUTO rule (all columns, auto-plot, mpl backend):{Style.RESET_ALL} python run_analysis.py show csv EURUSD MN1 --rule AUTO -d mpl")
    print(f"  {Fore.GREEN}Show mode, AUTO rule (all columns, auto-plot, terminal backend):{Style.RESET_ALL} python run_analysis.py show csv EURUSD MN1 --rule AUTO -d term")
    print()

    print(f"{Fore.YELLOW}{Style.BRIGHT}12. INTERACTIVE MODE EXAMPLES{Style.RESET_ALL}")
    print(f"  {Fore.GREEN}Start interactive mode:{Style.RESET_ALL}                python run_analysis.py interactive")
    print(f"  {Fore.GREEN}Start interactive mode (flag):{Style.RESET_ALL}         python run_analysis.py --interactive")
    print(f"  {Fore.GREEN}Start interactive mode (short):{Style.RESET_ALL}        python run_analysis.py -i")
    print(f"  {Fore.GREEN}Access metrics encyclopedia in interactive mode:{Style.RESET_ALL} Select option 10 from main menu")
    print()

    print(f"{Fore.YELLOW}{Style.BRIGHT}13. TROUBLESHOOTING & DIAGNOSTICS{Style.RESET_ALL}")
    print(f"  {Fore.GREEN}Show help:{Style.RESET_ALL}                             python run_analysis.py --help")
    print(f"  {Fore.GREEN}Show version:{Style.RESET_ALL}                          python run_analysis.py --version")
    print(f"  {Fore.GREEN}Show examples:{Style.RESET_ALL}                         python run_analysis.py --examples")
    print(f"  {Fore.GREEN}List all indicators:{Style.RESET_ALL}                   python run_analysis.py --indicators")
    print(f"  {Fore.GREEN}Search for specific indicator:{Style.RESET_ALL}         python run_analysis.py --indicators oscillators rsi")
    print(f"  {Fore.GREEN}Show trading metrics encyclopedia:{Style.RESET_ALL}     python run_analysis.py --metric")
    print()

    print(f"{Fore.YELLOW}{Style.BRIGHT}USAGE NOTES:{Style.RESET_ALL}")
    print(f"{Fore.CYAN}- Use -d to select plotting backend: fastest, fast, plotly, mplfinance, seaborn, sb, term, etc.")
    print(f"- Use --rule to select trading rule: OHLCV, PV, SR, PHLD, RSI, RSI_MOM, RSI_DIV, AUTO.")
    print(f"- Use --indicators to discover and learn about available indicators.")
    print(f"- Use --metric to explore trading metrics encyclopedia and strategy tips.")
    print(f"- Use interactive mode for guided setup and analysis.")
    print(f"- SHOW mode allows filtering cached files by source, keywords, date, and rule.")
    print(f"- Export flags are only allowed in 'demo' and 'show' modes (except 'show ind').")
    print(f"- For more details, see README.md or run with -h for full help.{Style.RESET_ALL}")
    print()

    print(f"{Fore.YELLOW}{Style.BRIGHT}QUICK START WORKFLOW:{Style.RESET_ALL}")
    print(f"1. {Fore.GREEN}Discover indicators:{Style.RESET_ALL}                  python run_analysis.py --indicators")
    print(f"2. {Fore.GREEN}Explore trading metrics:{Style.RESET_ALL}             python run_analysis.py --metric")
    print(f"3. {Fore.GREEN}Try interactive mode:{Style.RESET_ALL}                 python run_analysis.py -i")
    print(f"4. {Fore.GREEN}Run with demo data:{Style.RESET_ALL}                   python run_analysis.py demo --rule RSI")
    print(f"5. {Fore.GREEN}Download real data:{Style.RESET_ALL}                   python run_analysis.py yfinance --ticker AAPL --period 1mo --point 0.01")
    print(f"6. {Fore.GREEN}Analyze downloaded data:{Style.RESET_ALL}              python run_analysis.py show yfinance AAPL --rule RSI")
    print(f"7. {Fore.GREEN}Export results:{Style.RESET_ALL}                       python run_analysis.py show yfinance AAPL --rule RSI --export-parquet --export-csv")
    print()


def show_indicator_help():
    """Show help information about indicators."""
    print(f"\n{Fore.CYAN}{Style.BRIGHT}=== INDICATOR HELP ==={Style.RESET_ALL}")
    print("This tool supports various technical indicators organized by categories:")
    print()
    
    print(f"{Fore.YELLOW}{Style.BRIGHT}Available Categories:{Style.RESET_ALL}")
    print("• trend - Trend following indicators (EMA, ADX, SAR, SuperTrend)")
    print("• momentum - Momentum indicators (RSI, MACD, Stochastic)")
    print("• oscillators - Oscillator indicators (RSI, Stochastic, CCI)")
    print("• volatility - Volatility indicators (Bollinger Bands, ATR, Standard Deviation)")
    print("• volume - Volume-based indicators (OBV, VWAP)")
    print("• support/resistance - Support and resistance indicators (Pivot, Fibonacci, Donchian)")
    print("• sentiment - Market sentiment indicators (Put/Call Ratio, COT, Fear/Greed)")
    print("• predictive - Predictive indicators (HMA, Time Series Forecast)")
    print("• probability - Probability-based indicators (Monte Carlo, Kelly Criterion)")
    print()
    
    print(f"{Fore.YELLOW}{Style.BRIGHT}How to Use Indicators:{Style.RESET_ALL}")
    print("1. List all indicators: python run_analysis.py --indicators")
    print("2. Browse by category: python run_analysis.py --indicators oscillators")
    print("3. Search specific indicator: python run_analysis.py --indicators oscillators rsi")
    print("4. Use in analysis: python run_analysis.py demo --rule RSI")
    print("5. Interactive selection: python run_analysis.py interactive")
    print()
    
    print(f"{Fore.YELLOW}{Style.BRIGHT}Adding Your Own Indicators:{Style.RESET_ALL}")
    print("1. Create indicator file in src/calculation/indicators/[category]/")
    print("2. Add INDICATOR INFO section with metadata")
    print("3. Implement calculation logic")
    print("4. Register in TradingRule enum")
    print("5. Test with: python run_analysis.py --indicators [category]")
    print()
    
    print(f"{Fore.YELLOW}{Style.BRIGHT}Common Issues:{Style.RESET_ALL}")
    print("• Indicator not found: Check spelling and category")
    print("• Invalid parameters: Use --indicators to see required parameters")
    print("• Data format issues: Ensure OHLCV columns are present")
    print("• Export errors: Export only available in demo/show modes")
    print()


def show_export_help():
    """Show help information about export options."""
    print(f"\n{Fore.CYAN}{Style.BRIGHT}=== EXPORT HELP ==={Style.RESET_ALL}")
    print("Export options allow you to save analysis results in various formats:")
    print()
    
    print(f"{Fore.YELLOW}{Style.BRIGHT}Available Export Formats:{Style.RESET_ALL}")
    print("• --export-parquet: Save as Parquet file (fast, compressed)")
    print("• --export-csv: Save as CSV file (human-readable)")
    print("• --export-json: Save as JSON file (structured data)")
    print("• --export-indicators-info: Save indicator metadata as JSON")
    print()
    
    print(f"{Fore.YELLOW}{Style.BRIGHT}Export Locations:{Style.RESET_ALL}")
    print("• Indicator results: data/indicators/parquet/, data/indicators/csv/, data/indicators/json/")
    print("• Indicator metadata: data/indicators/metadata/")
    print()
    
    print(f"{Fore.YELLOW}{Style.BRIGHT}Export Restrictions:{Style.RESET_ALL}")
    print("• Export flags are only allowed in 'demo' and 'show' modes")
    print("• Export is forbidden in 'show ind' mode")
    print("• Export is forbidden in data download modes (yfinance, csv, polygon, binance, exrate)")
    print()
    
    print(f"{Fore.YELLOW}{Style.BRIGHT}Recommended Workflow:{Style.RESET_ALL}")
    print("1. Download data: python run_analysis.py yfinance --ticker AAPL --period 1mo --point 0.01")
    print("2. Analyze and export: python run_analysis.py show yfinance AAPL --rule RSI --export-parquet --export-csv")
    print("3. View exported files: python run_analysis.py show ind")
    print()


def show_interactive_help():
    """Show help information about interactive mode."""
    print(f"\n{Fore.CYAN}{Style.BRIGHT}=== INTERACTIVE MODE HELP ==={Style.RESET_ALL}")
    print("Interactive mode provides a guided interface for setting up and running analysis:")
    print()
    
    print(f"{Fore.YELLOW}{Style.BRIGHT}Starting Interactive Mode:{Style.RESET_ALL}")
    print("• python run_analysis.py interactive")
    print("• python run_analysis.py --interactive")
    print()
    
    print(f"{Fore.YELLOW}{Style.BRIGHT}Interactive Menu Options:{Style.RESET_ALL}")
    print("1. Select Analysis Mode - Choose data source (demo, csv, yfinance, etc.)")
    print("2. Select Indicator - Browse and choose technical indicator")
    print("3. Configure Data Source - Set up data source parameters")
    print("4. Configure Plotting - Choose visualization method")
    print("5. Configure Export - Select export formats")
    print("6. Show Current Configuration - Review your settings")
    print("7. Run Analysis - Execute the analysis")
    print("8. Help - Show this help")
    print("9. List Available Indicators - Browse indicator categories")
    print("0. Exit - Leave interactive mode")
    print()
    
    print(f"{Fore.YELLOW}{Style.BRIGHT}Interactive Mode Features:{Style.RESET_ALL}")
    print("• Guided setup process")
    print("• Real-time validation")
    print("• Preview of final command")
    print("• Easy indicator discovery")
    print("• Configuration review")
    print("• One-click analysis execution")
    print()
    
    print(f"{Fore.YELLOW}{Style.BRIGHT}Tips for Interactive Mode:{Style.RESET_ALL}")
    print("• Use option 9 to explore available indicators")
    print("• Review configuration before running analysis")
    print("• Interactive mode works with all data sources")
    print("• You can exit and restart at any time")
    print("• Configuration is not saved between sessions")
    print()


def show_data_source_help():
    """Show help information about data sources."""
    print(f"\n{Fore.CYAN}{Style.BRIGHT}=== DATA SOURCE HELP ==={Style.RESET_ALL}")
    print("This tool supports multiple data sources for financial analysis:")
    print()
    
    print(f"{Fore.YELLOW}{Style.BRIGHT}Available Data Sources:{Style.RESET_ALL}")
    print("• demo - Built-in demo data for testing")
    print("• csv - Local CSV files with OHLCV data")
    print("• yfinance - Yahoo Finance API (free)")
    print("• polygon - Polygon.io API (requires API key)")
    print("• binance - Binance API (free)")
    print("• exrate - Exchange Rate API (free/paid plans)")
    print("• show - Browse cached/downloaded data")
    print()
    
    print(f"{Fore.YELLOW}{Style.BRIGHT}Data Source Requirements:{Style.RESET_ALL}")
    print("• CSV: Requires --csv-file and --point")
    print("• Yahoo Finance: Requires --ticker, --point, and either --period or --start/--end")
    print("• Polygon: Requires --ticker, --point, --start, --end")
    print("• Binance: Requires --ticker, --point, --start, --end")
    print("• Exchange Rate: Requires --ticker, --point (historical data needs --start/--end)")
    print()
    
    print(f"{Fore.YELLOW}{Style.BRIGHT}Point Size Guidelines:{Style.RESET_ALL}")
    print("• Forex pairs: 0.00001 (5 decimal places)")
    print("• Stocks: 0.01 (2 decimal places)")
    print("• Cryptocurrencies: 0.01 (2 decimal places)")
    print("• Commodities: 0.01 (2 decimal places)")
    print()
    
    print(f"{Fore.YELLOW}{Style.BRIGHT}Common Ticker Formats:{Style.RESET_ALL}")
    print("• Yahoo Finance: AAPL, EURUSD=X, BTC-USD")
    print("• Polygon: AAPL, EURUSD, BTCUSD")
    print("• Binance: BTCUSDT, ETHUSDT, ADAUSDT")
    print("• Exchange Rate: EURUSD, GBPJPY, USDCAD")
    print()


def show_plotting_help():
    """Show help information about plotting options."""
    print(f"\n{Fore.CYAN}{Style.BRIGHT}=== PLOTTING HELP ==={Style.RESET_ALL}")
    print("This tool supports multiple plotting backends for visualization:")
    print()
    
    print(f"{Fore.YELLOW}{Style.BRIGHT}Available Plotting Backends:{Style.RESET_ALL}")
    print("• fastest - Fastest plotting (default, minimal dependencies)")
    print("• fast - Fast plotting with basic features")
    print("• plotly - Interactive Plotly charts (web-based)")
    print("• mplfinance - Matplotlib Finance (candlestick charts)")
    print("• seaborn - Seaborn statistical plots")
    print("• term - Terminal-based plotting (text-based)")
    print()
    
    print(f"{Fore.YELLOW}{Style.BRIGHT}Backend Features:{Style.RESET_ALL}")
    print("• fastest: Basic line plots, minimal setup")
    print("• fast: Enhanced line plots with indicators")
    print("• plotly: Interactive zoom, pan, hover tooltips")
    print("• mplfinance: Professional candlestick charts")
    print("• seaborn: Statistical analysis plots")
    print("• term: Text-based charts for terminal")
    print()
    
    print(f"{Fore.YELLOW}{Style.BRIGHT}Usage Examples:{Style.RESET_ALL}")
    print("• python run_analysis.py demo --rule RSI -d fastest")
    print("• python run_analysis.py demo --rule RSI -d plotly")
    print("• python run_analysis.py demo --rule RSI -d mplfinance")
    print("• python run_analysis.py demo --rule RSI -d seaborn")
    print("• python run_analysis.py demo --rule RSI -d term")
    print()
    
    print(f"{Fore.YELLOW}{Style.BRIGHT}Backend Selection Tips:{Style.RESET_ALL}")
    print("• Use 'fastest' for quick testing")
    print("• Use 'plotly' for interactive analysis")
    print("• Use 'mplfinance' for professional charts")
    print("• Use 'seaborn' for statistical analysis")
    print("• Use 'term' for server environments")
    print()


def show_troubleshooting_help():
    """Show help information about troubleshooting."""
    print(f"\n{Fore.CYAN}{Style.BRIGHT}=== TROUBLESHOOTING HELP ==={Style.RESET_ALL}")
    print("Common issues and solutions:")
    print()
    
    print(f"{Fore.YELLOW}{Style.BRIGHT}Data Issues:{Style.RESET_ALL}")
    print("• No data found: Check ticker symbol and date range")
    print("• Invalid point size: Use appropriate value for asset type")
    print("• Missing columns: Ensure CSV has OHLCV columns")
    print("• API errors: Check internet connection and API keys")
    print()
    
    print(f"{Fore.YELLOW}{Style.BRIGHT}Indicator Issues:{Style.RESET_ALL}")
    print("• Indicator not found: Use --indicators to list available")
    print("• Invalid parameters: Check indicator documentation")
    print("• Calculation errors: Ensure sufficient data points")
    print("• NaN values: Check data quality and indicator requirements")
    print()
    
    print(f"{Fore.YELLOW}{Style.BRIGHT}Export Issues:{Style.RESET_ALL}")
    print("• Export forbidden: Only available in demo/show modes")
    print("• File not found: Check export directory permissions")
    print("• Format errors: Ensure data is valid for export format")
    print()
    
    print(f"{Fore.YELLOW}{Style.BRIGHT}Plotting Issues:{Style.RESET_ALL}")
    print("• Backend not found: Install required dependencies")
    print("• Display errors: Check display settings and dependencies")
    print("• Memory issues: Use 'fastest' backend for large datasets")
    print()
    
    print(f"{Fore.YELLOW}{Style.BRIGHT}Getting Help:{Style.RESET_ALL}")
    print("• Run: python run_analysis.py --help")
    print("• Run: python run_analysis.py --examples")
    print("• Run: python run_analysis.py --indicators")
    print("• Check logs in logs/ directory")
    print("• Review README.md for detailed documentation")
    print()
