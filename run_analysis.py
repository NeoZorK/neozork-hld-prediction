# /run_analysis.py (in NeoZorK HLD/ root folder)

import argparse
import pandas as pd
import numpy as np # Needed for point size estimation
import yfinance as yf
import sys
from datetime import date, timedelta
import time # Needed for timing measurements

# Use absolute imports from the src package
from src.constants import TradingRule
from src.indicator import calculate_pressure_vector
from src.plotting import plot_indicator_results
from src import __version__

# --- Helper Functions ---

def get_demo_data() -> pd.DataFrame:
    """Returns the demonstration DataFrame."""
    print("Generating demo data...")
    # Simulate a short delay for "loading"
    time.sleep(0.5)
    data = {
        'Open': [1.1, 1.11, 1.12, 1.115, 1.125, 1.13, 1.128, 1.135, 1.14, 1.138,
                 1.142, 1.145, 1.140, 1.135, 1.130, 1.132, 1.138, 1.145, 1.148, 1.150,
                 1.152, 1.155, 1.153, 1.158, 1.160, 1.157, 1.162, 1.165, 1.163, 1.160],
        'High': [1.105, 1.115, 1.125, 1.12, 1.13, 1.135, 1.133, 1.14, 1.145, 1.142,
                 1.146, 1.148, 1.143, 1.139, 1.136, 1.137, 1.142, 1.150, 1.152, 1.155,
                 1.156, 1.159, 1.158, 1.161, 1.163, 1.160, 1.165, 1.168, 1.166, 1.164],
        'Low': [1.095, 1.105, 1.115, 1.11, 1.12, 1.125, 1.125, 1.13, 1.135, 1.136,
                1.140, 1.142, 1.138, 1.133, 1.128, 1.130, 1.135, 1.143, 1.146, 1.148,
                1.150, 1.152, 1.151, 1.155, 1.157, 1.154, 1.159, 1.161, 1.160, 1.158],
        'Close': [1.1, 1.11, 1.118, 1.118, 1.128, 1.128, 1.131, 1.138, 1.138, 1.14,
                  1.145, 1.141, 1.136, 1.131, 1.131, 1.136, 1.144, 1.149, 1.151, 1.149,
                  1.155, 1.154, 1.157, 1.160, 1.159, 1.158, 1.163, 1.164, 1.161, 1.159],
        # Use 'Volume' as provided by yfinance; indicator logic should handle it
        'Volume': [1000, 1200, 1100, 1300, 1500, 1400, 1600, 1700, 1550, 1650,
                   1750, 1800, 1600, 1900, 2000, 1850, 1950, 2100, 2050, 2200,
                   2150, 2250, 2100, 2300, 2400, 2350, 2450, 2500, 2400, 2300]
    }
    # Create a longer index
    start_date = date.today() - timedelta(days=len(data['Open'])-1)
    index = pd.date_range(start=start_date, periods=len(data['Open']), freq='D')
    df = pd.DataFrame(data, index=index)

    # Rename columns for mplfinance compatibility (it expects capitalized names)
    df.columns = ['Open', 'High', 'Low', 'Close', 'Volume']
    return df

def map_interval(tf_input: str) -> str:
    """Maps user-friendly timeframe input to yfinance interval string."""
    tf_input = tf_input.upper()
    # Mapping from user input (like M1, D1) to yfinance interval (like 1m, 1d)
    mapping = {
        "M1": "1m", "M5": "5m", "M15": "15m", "M30": "30m",
        "H1": "1h", "H4": "4h",
        "D1": "1d", "D": "1d",
        "W1": "1wk", "W": "1wk", "WK": "1wk",
        "MN1": "1mo", "MN": "1mo", "MO": "1mo"
    }
    # Valid intervals directly accepted by yfinance
    valid_yf_intervals = ["1m", "2m", "5m", "15m", "30m", "60m", "90m", "1h", "1d", "5d", "1wk", "1mo", "3mo"]

    if tf_input in mapping:
        return mapping[tf_input]
    elif tf_input.lower() in valid_yf_intervals:
         # Allow direct use of yfinance intervals
         return tf_input.lower()
    else:
        raise ValueError(f"Invalid timeframe input: '{tf_input}'. Use formats like 'M1', 'H1', 'D1', 'W1', 'MN1' or yfinance intervals like '1m', '1h', '1d', '1wk', '1mo'.")

def map_ticker(ticker_input: str) -> str:
    """Optional: Adds standard suffixes for common yfinance ticker patterns."""
    ticker = ticker_input.upper()
    # Example: Add '=X' for 6-char currency pairs without a suffix
    if len(ticker) == 6 and '=' not in ticker and '-' not in ticker:
         # Simple heuristic, may need refinement
         is_likely_forex = all(c.isalpha() for c in ticker)
         if is_likely_forex:
             print(f"[Info] Assuming '{ticker}' is Forex, appending '=X'. -> '{ticker}=X'")
             return f"{ticker}=X"
    # Example: Add '-USD' for some common crypto tickers without a pair
    # common_crypto = ['BTC', 'ETH', 'XRP', 'LTC', 'ADA', 'SOL'] # Add more if needed
    # if ticker in common_crypto:
    #     print(f"[Info] Assuming '{ticker}' is Crypto, appending '-USD'. -> '{ticker}-USD'")
    #     return f"{ticker}-USD"

    # Return the ticker as is if no rules matched
    return ticker

def determine_point_size(ticker: str, df: pd.DataFrame) -> float:
    """Estimates the instrument's point size based on ticker and price data."""
    print("[Info] Estimating point size...")
    ticker = ticker.upper()

    # 1. Forex Heuristic (ticker ends with =X)
    if ticker.endswith("=X"):
        print("[Info] Ticker ends with '=X', assuming Forex point size: 0.00001")
        return 0.00001

    # 2. Calculate minimum non-zero High-Low difference
    min_hl_diff = np.nan
    if 'High' in df.columns and 'Low' in df.columns:
        hl_diff = (df['High'] - df['Low']).abs()
        min_hl_diff = hl_diff.replace(0, np.nan).min()

    if pd.notna(min_hl_diff) and min_hl_diff > 0:
        print(f"[Debug] Minimum non-zero H-L difference: {min_hl_diff}")
        # 3. Estimate based on order of magnitude of min H-L difference
        if min_hl_diff < 0.001: # e.g., 0.00015 -> 0.00001
            estimated_point = 10**(np.floor(np.log10(min_hl_diff)) - 1) # Go one order lower
            # Clamp to reasonable minimum (e.g., 0.00001)
            estimated_point = max(0.00001, estimated_point)
            print(f"[Info] Low H-L diff suggests high precision, estimating point size: {estimated_point}")
            return estimated_point
        elif min_hl_diff < 0.1: # e.g., 0.05 -> 0.01
             print("[Info] Moderate H-L diff suggests stock/index/crypto precision, estimating point size: 0.01")
             return 0.01
        elif min_hl_diff < 1.0: # e.g., 0.5 -> 0.1
             print("[Info] Higher H-L diff, estimating point size: 0.1")
             return 0.1
        else: # Large diff -> 1.0
             print("[Info] Large H-L diff, estimating point size: 1.0")
             return 1.0

    # 4. Fallback / Default (e.g., for stocks if H-L diff calculation failed)
    print("[Warning] Could not reliably estimate point size from H-L difference. Falling back to default: 0.01")
    return 0.01

def fetch_yfinance_data(ticker: str, interval: str, period: str = None, start_date: str = None, end_date: str = None) -> pd.DataFrame | None:
    """Downloads data from Yahoo Finance with progress bar and error handling."""
    print(f"[Info] Attempting to fetch data for ticker: {ticker} | interval: {interval}")
    try:
        # Use yfinance's built-in progress bar (based on tqdm)
        df = yf.download(
            tickers=ticker,
            period=period,
            interval=interval,
            start=start_date,
            end=end_date,
            progress=True,       # Show progress bar
            auto_adjust=False,   # Crucial for getting raw OHLC prices
            actions=False        # Don't download dividends/splits into main table
        )

        if df.empty:
            print(f"[Warning] No data returned for ticker '{ticker}' with specified parameters.")
            return None

        # Check for required columns
        required_cols = ['Open', 'High', 'Low', 'Close', 'Volume']
        if not all(col in df.columns for col in required_cols):
             print(f"[Warning] Downloaded data for '{ticker}' is missing required columns (needs Open, High, Low, Close, Volume). Available: {df.columns.tolist()}")
             # Attempt to rename if possible? (e.g., Adj Close -> Close) - Risky
             return None # Better to return None if essential data is missing

        # yfinance might return rows with NaNs if there were no trades (e.g., weekends for daily data)
        # Drop rows where all essential price columns are NaN
        df.dropna(subset=['Open', 'High', 'Low', 'Close'], how='all', inplace=True)

        if df.empty:
            print(f"[Warning] Data for '{ticker}' became empty after removing NaN rows.")
            return None

        print(f"[Info] Successfully fetched {len(df)} rows.")
        return df

    except Exception as e:
        print(f"\n--- ERROR DOWNLOADING ---")
        print(f"An error occurred during yfinance download for ticker '{ticker}': {e}")
        # Provide hints for common issues
        if "No data found" in str(e):
             print("Hint: Check if the ticker symbol is correct and data exists for the requested period/interval.")
        elif "invalid interval" in str(e):
             print("Hint: Check if the interval format is valid for the requested period (e.g., minute data often has limited history).")
        print(f"--- END ERROR DOWNLOADING ---")
        return None

# --- Main Execution Function ---
def main():
    # Start overall timer
    start_time_total = time.perf_counter()

    # Setup argument parser
    parser = argparse.ArgumentParser(
        description="Calculate and plot Shcherbyna Pressure Vector indicator using demo data or fetching from Yahoo Finance.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter # Show default values in --help
    )

    # --- Command Line Arguments ---
    parser.add_argument('mode', choices=['demo', 'yfinance', 'yf'], # Added 'yf' alias
                        help="Operating mode: 'demo' uses built-in data, 'yfinance' or 'yf' fetches data.")

    # --- Yahoo Finance Specific Arguments ---
    # Arguments required only if mode is 'yfinance' or 'yf'
    yf_group = parser.add_argument_group('Yahoo Finance Options (required if mode=yfinance/yf)')
    yf_group.add_argument('-t', '--ticker',
                          help="Ticker symbol for yfinance (e.g., 'EURUSD=X', 'BTC-USD', 'AAPL').")
    yf_group.add_argument('-i', '--interval', default='D1',
                          help="Timeframe (e.g., 'M1', 'H1', 'D1', 'W1', 'MN1'). Will be mapped to yfinance interval.")
    # Point size is now optional, will be estimated if not provided
    yf_group.add_argument('--point', type=float,
                          help="Instrument point size (e.g., 0.00001). Overrides automatic estimation. Crucial for accuracy.")

    # --- History Selection Group (Mutually Exclusive) ---
    history_group = yf_group.add_mutually_exclusive_group()
    history_group.add_argument('-p', '--period', default='1y',
                               help="History period for yfinance (e.g., '1mo', '6mo', '1y', '5y', 'max').")
    history_group.add_argument('--start', help="Start date for yfinance data (YYYY-MM-DD). Use with --end.")
    # --end is not in the exclusive group as it's used with --start
    yf_group.add_argument('--end', help="End date for yfinance data (YYYY-MM-DD). Use with --start.")

    # --- Indicator Calculation Arguments ---
    indicator_group = parser.add_argument_group('Indicator Options')
    indicator_group.add_argument('--rule', default=TradingRule.PV_HighLow.name, choices=TradingRule.__members__.keys(),
                                 help="Trading rule to apply.")

    # --- Version Argument ---
    parser.add_argument('--version', action='version', version=f'%(prog)s {__version__}')

    # Parse the arguments
    args = parser.parse_args()

    # --- Data Acquisition ---
    start_time_data = time.perf_counter()
    ohlcv_df = None
    point_size = None
    data_source_label = ""
    estimated_point = False # Flag to track if point size was estimated

    # Handle mode selection ('yf' alias)
    effective_mode = 'yfinance' if args.mode == 'yf' else args.mode

    if effective_mode == 'demo':
        print("--- Mode: Demo ---")
        ohlcv_df = get_demo_data()
        # Use a fixed point size for demo data
        point_size = 0.00001
        data_source_label = "Demo Data"
        print(f"[Info] Using built-in demo data. Point size set to: {point_size}")

    elif effective_mode == 'yfinance':
        print("--- Mode: Yahoo Finance ---")
        # Validate required arguments for yfinance mode
        if not args.ticker:
            parser.error("Ticker (--ticker) is required for yfinance mode.")
        # Point size is no longer strictly required here, will be estimated

        data_source_label = args.ticker # Use ticker for plot title

        # Map and validate interval
        try:
            yf_interval = map_interval(args.interval)
        except ValueError as e:
            parser.error(str(e))

        # Map ticker (optional enhancement)
        yf_ticker = map_ticker(args.ticker)

        # Determine history parameters
        period_arg = args.period
        start_arg = args.start
        end_arg = args.end

        # Handle date logic
        if args.start and not args.end:
            end_arg = date.today().strftime('%Y-%m-%d')
            print(f"[Info] End date not specified, using today: {end_arg}")
        elif args.end and not args.start:
            parser.error("Start date (--start) must be specified if end date (--end) is used.")

        # Determine effective period/dates for download
        current_period = None
        current_start = None
        current_end = None
        if start_arg and end_arg:
            current_start = start_arg
            current_end = end_arg
            print(f"[Info] Fetching data for interval '{yf_interval}' from {current_start} to {current_end}")
        else:
            current_period = period_arg
            print(f"[Info] Fetching data for interval '{yf_interval}' for period '{current_period}'")

        # Fetch data
        ohlcv_df = fetch_yfinance_data(
            ticker=yf_ticker,
            interval=yf_interval,
            period=current_period,
            start_date=current_start,
            end_date=current_end
        )

        if ohlcv_df is None or ohlcv_df.empty:
            print("[Error] Could not fetch valid data from Yahoo Finance. Exiting.")
            sys.exit(1)

        # --- Point Size Determination/Override ---
        if args.point is not None:
             # User provided point size - override estimation
             if args.point <= 0:
                  parser.error("Provided point size (--point) must be positive.")
             point_size = args.point
             print(f"[Info] Using user-provided point size: {point_size}")
        else:
             # Estimate point size
             point_size = determine_point_size(yf_ticker, ohlcv_df)
             estimated_point = True
             print(f"[Warning] Automatically estimated point size: {point_size}. "
                   f"This is an estimate and might be inaccurate. "
                   f"Use the --point argument to specify it accurately for reliable calculations.")


    # Record data acquisition time and size
    end_time_data = time.perf_counter()
    data_fetch_duration = end_time_data - start_time_data
    data_size_bytes = 0
    data_size_mb = 0
    if ohlcv_df is not None:
        data_size_bytes = ohlcv_df.memory_usage(deep=True).sum()
        data_size_mb = data_size_bytes / (1024 * 1024)


    # --- Indicator Calculation ---
    result_df = None
    calc_duration = 0
    if ohlcv_df is not None and not ohlcv_df.empty:
        print(f"\nCalculating indicator using rule: {args.rule}...")
        start_time_calc = time.perf_counter()

        # Map rule string to enum
        try:
             selected_rule = TradingRule[args.rule]
        except KeyError:
             print(f"[Error] Invalid rule name '{args.rule}'. Use one of {list(TradingRule.__members__.keys())}")
             sys.exit(1)

        # Check for required columns before calling calculation
        # Indicator function expects 'TickVolume' for some internal calcs,
        # but yfinance provides 'Volume'. We need to ensure it's present.
        required_cols_indicator = ['Open', 'High', 'Low', 'Close', 'Volume']
        if not all(col in ohlcv_df.columns for col in required_cols_indicator):
            print(f"[Error] DataFrame is missing required columns for calculation: {required_cols_indicator}. Available: {ohlcv_df.columns.tolist()}")
            sys.exit(1)
        # Rename 'Volume' to 'TickVolume' right before passing, as indicator logic expects it
        ohlcv_df_renamed = ohlcv_df.rename(columns={'Volume': 'TickVolume'}, errors='ignore')


        try:
            result_df = calculate_pressure_vector(
                df=ohlcv_df_renamed.copy(), # Pass a copy of the renamed df
                point=point_size,
                tr_num=selected_rule,
            )
        except Exception as e:
             print(f"An error occurred during indicator calculation:", e)
             sys.exit(1)

        end_time_calc = time.perf_counter()
        calc_duration = end_time_calc - start_time_calc
    elif ohlcv_df is None:
         print("[Error] No data loaded, cannot calculate indicator.")
         sys.exit(1)
    else: # DataFrame exists but is empty
         print("[Warning] Loaded DataFrame is empty, skipping calculation.")


    # --- Plotting Results ---
    plot_duration = 0
    if result_df is not None and not result_df.empty:
        print("\nPlotting results...")
        start_time_plot = time.perf_counter()
        chart_title = f"{data_source_label} | {args.interval} | Rule: {selected_rule.name}"
        if estimated_point:
            chart_title += f" | Est. Point: {point_size}"

        try:
            # Pass the result_df which should have 'Volume' (renamed back from TickVolume inside indicator)
            plot_indicator_results(result_df, rule=selected_rule, title=chart_title)
            print("\nPlot displayed. Close the plot window to continue/exit.")
        except Exception as e:
             print(f"An error occurred during plotting:",e)
             # Don't exit here, timing info is still useful
        finally:
             end_time_plot = time.perf_counter()
             plot_duration = end_time_plot - start_time_plot

    elif result_df is None and ohlcv_df is not None: # Calculation failed or skipped
        print("Skipping plotting as indicator calculation did not produce results.")
    else: # No data loaded
        print("Skipping plotting as no data was loaded.")


    # --- Timing and Size Summary ---
    end_time_total = time.perf_counter()
    total_duration = end_time_total - start_time_total

    print("\n--- Execution Summary ---")
    print(f"Data Source:          {data_source_label if effective_mode != 'demo' else 'Demo'}")
    if effective_mode == 'yfinance':
        print(f"Ticker:               {yf_ticker}")
        print(f"Interval:             {yf_interval}")
        if current_start and current_end:
             print(f"Date Range:           {current_start} to {current_end}")
        else:
             print(f"Period:               {current_period}")
    print(f"Point Size Used:      {point_size:.8f}{' (Estimated)' if estimated_point else ''}")
    print("-" * 25)
    print(f"Data Size:            {data_size_mb:.3f} MB ({data_size_bytes} bytes)")
    print(f"Data Fetch/Load Time: {data_fetch_duration:.3f} seconds")
    print(f"Indicator Calc Time:  {calc_duration:.3f} seconds")
    print(f"Plotting Time:        {plot_duration:.3f} seconds")
    print("-" * 25)
    print(f"Total Execution Time: {total_duration:.3f} seconds")
    print("--- End Summary ---")


if __name__ == "__main__":
    main()