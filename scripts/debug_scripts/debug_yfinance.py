# debug_yfinance.py
import yfinance as yf
import pandas as pd

ticker = 'GOOG'
period = '1mo'
interval = '1d'

print(f"--- Minimal YFinance Test ---")
print(f"Attempting to download: Ticker={ticker}, Period={period}, Interval={interval}")

try:
    # Set display options for pandas DataFrame
    pd.set_option('display.max_rows', 10)
    pd.set_option('display.max_columns', 10)
    yf.set_tz_cache_location(".yf_cache") # Set cache location for yfinance

    data = yf.download(
        tickers=ticker,
        period=period,
        interval=interval,
        progress=True,
        auto_adjust=False,
        actions=False
    )

    if data is None or data.empty:
        print("\n[Error] yf.download returned None or empty DataFrame.")
    else:
        print(f"\n[Success] Downloaded {len(data)} rows.")
        print("First 5 rows:")
        print(data.head())
        print("\nLast 5 rows:")
        print(data.tail())
        print("\nColumns:", data.columns.tolist())
        required_cols = ['Open', 'High', 'Low', 'Close', 'Volume']
        missing_cols = [col for col in required_cols if col not in data.columns]
        if missing_cols:
            print(f"\n[Warning] Missing required columns: {missing_cols}")
        else:
            print(f"\n[Info] All required columns present.")

except Exception as e:
    print(f"\n--- ERROR ---")
    print(f"An exception occurred during yf.download:")
    print(f"Exception Type: {type(e).__name__}")
    print(f"Exception Details: {e}")
    import traceback
    print("Traceback:")
    traceback.print_exc()
    print(f"--- END ERROR ---")

print(f"\n--- End of Test ---")