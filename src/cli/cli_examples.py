# src/cli/cli_examples.py


def show_cli_examples(terminal_console):
    """
    Show command line interface (CLI) examples for the analysis tool.
    :param terminal_console:
    :return:
    """
    console = terminal_console()
    console.print("[bold cyan]\nEXAMPLES (run: python run_analysis.py --examples):[/bold cyan]\n")
    console.print("[bold]1. DEMO DATA MODES[/bold]")
    console.print(
        "[dim]# Run with demo data (default rule)[/dim]\n[bold green]python run_analysis.py demo[/bold green]")
    console.print(
        "[dim]# Run with demo data using mplfinance[/dim]\n[bold green]python run_analysis.py demo -d mpl[/bold green]")
    console.print(
        "[dim]# Run with demo data and PV_HighLow rule[/dim]\n[bold green]python run_analysis.py demo --rule PV_HighLow[/bold green]")
    console.print(
        "[dim]# Run with demo data and PHLD rule, plotly backend[/dim]\n[bold green]python run_analysis.py demo --rule PHLD -d plotly[/bold green]\n")

    console.print("[bold]2. CSV FILE MODES[/bold]")
    console.print(
        "[dim]# Basic CSV mode[/dim]\n[bold green]python run_analysis.py csv --csv-file data.csv --point 0.01[/bold green]")
    console.print(
        "[dim]# CSV with Support_Resistants rule[/dim]\n[bold green]python run_analysis.py csv --csv-file data.csv --point 0.01 --rule SR[/bold green]")
    console.print(
        "[dim]# CSV with mplfinance backend[/dim]\n[bold green]python run_analysis.py csv --csv-file data.csv --point 0.01 -d mplfinance[/bold green]")
    console.print(
        "[dim]# CSV with PV rule, fastest backend[/dim]\n[bold green]python run_analysis.py csv --csv-file data.csv --point 0.01 --rule PV --draw fastest[/bold green]\n")
    console.print(
        "[dim]# CSV with PV rule, seaborn backend[/dim]\n[bold green]python run_analysis.py csv --csv-file data.csv --point 0.01 --rule PV --draw seaborn[/bold green]\n")

    console.print("[bold]3. YAHOO FINANCE (YF) MODES[/bold]")
    console.print(
        "[dim]# EURUSD=X, 1mo, point size[/dim]\n[bold green]python run_analysis.py yf -t EURUSD=X --period 1mo --point 0.00001[/bold green]")
    console.print(
        "[dim]# AAPL, 6mo, point size[/dim]\n[bold green]python run_analysis.py yfinance -t AAPL --period 6mo --point 0.01[/bold green]")
    console.print(
        "[dim]# BTC-USD, date range, point size[/dim]\n[bold green]python run_analysis.py yf -t BTC-USD --start 2023-01-01 --end 2023-12-31 --point 0.01[/bold green]")
    console.print(
        "[dim]# EURUSD=X, date range, mpl backend[/dim]\n[bold green]python run_analysis.py yf -t EURUSD=X --start 2024-01-01 --end 2024-04-18 --point 0.00001 -d mpl[/bold green]")
    console.print(
        "[dim]# AAPL, 1y, Support_Resistants rule[/dim]\n[bold green]python run_analysis.py yf -t AAPL --period 1y --rule SR[/bold green]\n")

    console.print("[bold]4. POLYGON.IO MODES[/bold]")
    console.print(
        "[dim]# AAPL, D1, date range, point size[/dim]\n[bold green]python run_analysis.py polygon --ticker AAPL --interval D1 --start 2023-01-01 --end 2023-12-31 --point 0.01[/bold green]")
    console.print(
        "[dim]# EURUSD, H1, date range, PV rule[/dim]\n[bold green]python run_analysis.py polygon --ticker EURUSD --interval H1 --start 2022-01-01 --end 2022-06-01 --point 0.00001 --rule PV[/bold green]\n")

    console.print("[bold]5. BINANCE MODES[/bold]")
    console.print(
        "[dim]# BTCUSDT, H1, date range, point size[/dim]\n[bold green]python run_analysis.py binance --ticker BTCUSDT --interval H1 --start 2024-01-01 --end 2024-04-18 --point 0.01[/bold green]")
    console.print(
        "[dim]# ETHUSDT, D1, date range, Support_Resistants rule[/dim]\n[bold green]python run_analysis.py binance --ticker ETHUSDT --interval D1 --start 2023-01-01 --end 2023-12-31 --point 0.01 --rule SR[/bold green]\n")
    console.print(
        "[dim]# ETHUSDT, D1, date range, Support_Resistants rule with SeaBorn plot[/dim]\n[bold green]python run_analysis.py binance --ticker ETHUSDT --interval D1 --start 2023-01-01 --end 2023-12-31 --point 0.01 --rule SR -d sb[/bold green]\n")

    console.print("[bold]6. SHOW MODE (CACHE/FILES)[/bold]")
    console.print(
        "[dim]# Show all YFinance files[/dim]\n[bold green]python run_analysis.py show yf[/bold green]")
    console.print(
        "[dim]# Show YFinance files with 'aapl' and 'mn1' in name[/dim]\n[bold green]python run_analysis.py show yf aapl mn1[/bold green]")
    console.print(
        "[dim]# Show Binance files with 'btc' in name[/dim]\n[bold green]python run_analysis.py show binance btc[/bold green]")
    console.print(
        "[dim]# Show Binance files with 'btc' in name with SeaBorn plot[/dim]\n[bold green]python run_analysis.py show binance btc -d seaborn[/bold green]")
    console.print(
        "[dim]# Show CSV files with EURUSD MN1[/dim]\n[bold green]python run_analysis.py show csv EURUSD MN1[/bold green]")
    console.print(
        "[dim]# Show Polygon files with AAPL 2023[/dim]\n[bold green]python run_analysis.py show polygon AAPL 2023[/bold green]")
    console.print(
        "[dim]# Show YF files with PV rule[/dim]\n[bold green]python run_analysis.py show yf --show-rule PV[/bold green]")
    console.print(
        "[dim]# Show YF files for date range[/dim]\n[bold green]python run_analysis.py show yf --show-start 2023-01-01 --show-end 2023-12-31[/bold green]\n")

    console.print("[bold]7. ADVANCED/EDGE CASES[/bold]")
    console.print(
        "[dim]# CSV, PHLD rule, plotly backend[/dim]\n[bold green]python run_analysis.py csv --csv-file data.csv --point 0.01 --rule PHLD --draw plotly[/bold green]")
    console.print(
        "[dim]# YF, PV rule, fastest backend[/dim]\n[bold green]python run_analysis.py yf -t EURUSD=X --period 1mo --point 0.00001 --rule PV --draw fastest[/bold green]")
    console.print(
        "[dim]# Polygon, SR rule, mpl backend[/dim]\n[bold green]python run_analysis.py polygon --ticker EURUSD --interval D1 --start 2022-01-01 --end 2022-12-31 --point 0.00001 --rule SR --draw mpl[/bold green]")
    console.print(
        "[dim]# Binance, M1, PHLD rule[/dim]\n[bold green]python run_analysis.py binance --ticker BTCUSDT --interval M1 --start 2023-01-01 --end 2023-01-31 --point 0.01 --rule PHLD[/bold green]\n")

    console.print("[bold]8. HELP, VERSION, EXAMPLES[/bold]")
    console.print("[dim]# Show help, version, or all examples[/dim]")
    console.print("[bold green]python run_analysis.py -h[/bold green]")
    console.print("[bold green]python run_analysis.py --version[/bold green]")
    console.print("[bold green]python run_analysis.py --examples[/bold green]\n")

    console.print("[bold]9. CACHE/DEBUG[/bold]")
    console.print("[dim]# Remove cache and rerun[/dim]")
    console.print("[bold green]rm data/cache/csv_converted/*.parquet[/bold green]")
    console.print("[bold green]python run_analysis.py csv --csv-file data.csv --point 0.01[/bold green]\n")

    console.print("[bold]10. ERROR CASES (will show error/help)[/bold]")
    console.print("[dim]# Missing required arguments[/dim]")
    console.print(
        "[bold green]python run_analysis.py csv --csv-file data.csv[/bold green]   [dim]# (missing --point)[/dim]")
    console.print(
        "[bold green]python run_analysis.py yf -t EURUSD=X[/bold green]            [dim]# (missing --period or --start/--end)[/dim]\n")
    console.print(
        "[bold yellow]Note:[/bold yellow] For all API modes (yfinance, polygon, binance), the --point parameter is required to specify the instrument's point size (e.g., 0.00001 for EURUSD, 0.01 for stocks/crypto).\n")
    console.print(
        "[yellow]- Use -d/--draw to select plotting backend: fastest, fast, plotly, mplfinance, seaborn, sb, etc.")
    console.print(
        "- Use --rule to select trading rule: PV_HighLow, Support_Resistants, Pressure_Vector, Predict_High_Low_Direction, PHLD, PV, SR.")
    console.print("- SHOW mode allows filtering cached files by source, keywords, date, and rule.")
    console.print("- For more details, see README.md or run with -h for full help.\n")


def print_cli_examples():
    """
    Print command line interface (CLI) examples for the analysis tool.
    :return: None
    """
    print("""
    EXAMPLES (run: python run_analysis.py --examples):

      # 1. DEMO DATA MODES
      python run_analysis.py demo
      python run_analysis.py demo -d mpl
      python run_analysis.py demo --rule PV_HighLow
      python run_analysis.py demo --rule PHLD -d plotly
      python run_analysis.py demo --rule SR -d seaborn

      # 2. CSV FILE MODES
      python run_analysis.py csv --csv-file data.csv --point 0.01
      python run_analysis.py csv --csv-file data.csv --point 0.01 --rule SR
      python run_analysis.py csv --csv-file data.csv --point 0.01 -d mplfinance
      python run_analysis.py csv --csv-file data.csv --point 0.01 --rule PV --draw fastest
      python run_analysis.py csv --csv-file data.csv --point 0.01 --rule PV --draw sb

      # 3. YAHOO FINANCE (YF) MODES
      python run_analysis.py yf -t EURUSD=X --period 1mo --point 0.00001
      python run_analysis.py yfinance -t AAPL --period 6mo --point 0.01
      python run_analysis.py yf -t BTC-USD --start 2023-01-01 --end 2023-12-31 --point 0.01
      python run_analysis.py yf -t EURUSD=X --start 2024-01-01 --end 2024-04-18 --point 0.00001 -d mpl
      python run_analysis.py yf -t AAPL --period 1y --rule SR
      python run_analysis.py yf -t AAPL --period 1y --rule SR -d seaborn

      # 4. POLYGON.IO MODES
      python run_analysis.py polygon --ticker AAPL --interval D1 --start 2023-01-01 --end 2023-12-31 --point 0.01
      python run_analysis.py polygon --ticker EURUSD --interval H1 --start 2022-01-01 --end 2022-06-01 --point 0.00001 --rule PV
      python run_analysis.py polygon --ticker EURUSD --interval H1 --start 2022-01-01 --end 2022-06-01 --point 0.00001 --rule PV --sb

      # 5. BINANCE MODES
      python run_analysis.py binance --ticker BTCUSDT --interval H1 --start 2024-01-01 --end 2024-04-18 --point 0.01
      python run_analysis.py binance --ticker ETHUSDT --interval D1 --start 2023-01-01 --end 2023-12-31 --point 0.01 --rule SR
      python run_analysis.py binance --ticker ETHUSDT --interval D1 --start 2023-01-01 --end 2023-12-31 --point 0.01 --rule SR -d seaborn

      # 6. SHOW MODE (CACHE/FILES)
      python run_analysis.py show yf
      python run_analysis.py show yf aapl mn1
      python run_analysis.py show binance btc
      python run_analysis.py show csv EURUSD MN1
      python run_analysis.py show polygon AAPL 2023
      python run_analysis.py show polygon AAPL 2023 -d seaborn
      python run_analysis.py show yf --show-rule PV
      python run_analysis.py show yf --show-start 2023-01-01 --show-end 2023-12-31

      # 7. ADVANCED/EDGE CASES
      python run_analysis.py csv --csv-file data.csv --point 0.01 --rule PHLD --draw plotly
      python run_analysis.py yf -t EURUSD=X --period 1mo --point 0.00001 --rule PV --draw fastest
      python run_analysis.py polygon --ticker EURUSD --interval D1 --start 2022-01-01 --end 2022-12-31 --point 0.00001 --rule SR --draw mpl
      python run_analysis.py binance --ticker BTCUSDT --interval M1 --start 2023-01-01 --end 2023-01-31 --point 0.01 --rule PHLD

      # 8. HELP, VERSION, EXAMPLES
      python run_analysis.py -h
      python run_analysis.py --version
      python run_analysis.py --examples

      # 9. CACHE/DEBUG
      # Remove cache and rerun
      rm data/cache/csv_converted/*.parquet
      python run_analysis.py csv --csv-file data.csv --point 0.01

      # 10. ERROR CASES (will show error/help)
      python run_analysis.py csv --csv-file data.csv   # (missing --point)
      python run_analysis.py yf -t EURUSD=X            # (missing --period or --start/--end)

    Note:
    - For all API modes (yfinance, polygon, binance), the --point parameter is required to specify the instrument's point size (e.g., 0.00001 for EURUSD, 0.01 for stocks/crypto).
    - Use -d/--draw to select plotting backend: fastest, fast, plotly, mplfinance, seaborn, sb etc.
    - Use --rule to select trading rule: PV_HighLow, Support_Resistants, Pressure_Vector, Predict_High_Low_Direction, PHLD, PV, SR.
    - SHOW mode allows filtering cached files by source, keywords, date, and rule.
    - For more details, see README.md or run with -h for full help.\n""")
