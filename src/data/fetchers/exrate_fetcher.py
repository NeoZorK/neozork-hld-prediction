# src/data/fetchers/exrate_fetcher.py

"""
Contains functions related to fetching data from Exchange Rate API (exchangerate-api.com).
Provides historical exchange rate data for currency pairs.
All comments are in English.
"""

import pandas as pd
import numpy as np
import os
import time
import traceback
import requests
from datetime import datetime, timedelta
from tqdm import tqdm  # Import tqdm

# Use relative import for logger
from ...common import logger


def map_exrate_interval(tf_input: str) -> str | None:
    """
    Maps user-friendly timeframe input to Exchange Rate API supported intervals.
    Note: Exchange Rate API only provides daily data, so all intervals will be mapped to daily.
    """
    tf_input_upper = tf_input.upper()
    
    # Exchange Rate API only supports daily data
    # All intervals will be mapped to daily (D1)
    supported_intervals = ["D1", "D", "W1", "W", "WK", "MN1", "MN", "MO"]
    
    # Warn for unsupported intervals
    if tf_input_upper in ["M1", "M5", "M15", "M30", "H1", "H4"]:
        logger.print_warning(f"Exchange Rate API does not support intraday intervals. '{tf_input}' will be mapped to daily (D1).")
        return "D1"
    
    if tf_input_upper in supported_intervals:
        return "D1"  # Always return D1 as Exchange Rate API provides daily data
    elif tf_input.lower() in ["d1", "d", "1d"]:
        return "D1"
    else:
        logger.print_error(f"Invalid or unsupported Exchange Rate API timeframe input: '{tf_input}'. Supported: D1, W1, MN1")
        return None


def map_exrate_ticker(ticker_input: str) -> tuple[str, str] | None:
    """
    Maps user-provided ticker to Exchange Rate API format (base/target currencies).
    
    Args:
        ticker_input (str): User ticker like 'EURUSD', 'BTCUSDT', 'GBPJPY'
        
    Returns:
        tuple[str, str] | None: (base_currency, target_currency) or None if invalid
    """
    ticker = ticker_input.upper().strip()
    
    # Common currency codes for Exchange Rate API
    supported_currencies = {
        'USD', 'EUR', 'GBP', 'JPY', 'CHF', 'CAD', 'AUD', 'NZD', 'CNY', 'INR',
        'BRL', 'RUB', 'KRW', 'SGD', 'HKD', 'MXN', 'NOK', 'SEK', 'DKK', 'PLN',
        'CZK', 'HUF', 'THB', 'MYR', 'PHP', 'IDR', 'VND', 'ZAR', 'TRY', 'ILS',
        'AED', 'SAR', 'EGP', 'QAR', 'KWD', 'BHD', 'OMR', 'JOD', 'LBP', 'PKR',
        'BGN', 'HRK', 'RON', 'ISK', 'UYU', 'CLP', 'COP', 'PEN', 'ARS', 'BOB',
        'PYG', 'VES', 'GYD', 'SRD', 'FKP', 'GIP', 'SHP', 'JEP', 'GGP', 'IMP'
    }
    
    # Handle different ticker formats
    if len(ticker) == 6 and ticker.isalpha():
        # Format like EURUSD -> EUR/USD
        base = ticker[:3]
        target = ticker[3:]
        if base in supported_currencies and target in supported_currencies:
            logger.print_info(f"Mapped ticker '{ticker_input}' to {base}/{target}")
            return base, target
    elif '/' in ticker:
        # Format like EUR/USD
        parts = ticker.split('/')
        if len(parts) == 2:
            base, target = parts[0].strip(), parts[1].strip()
            if base in supported_currencies and target in supported_currencies:
                logger.print_info(f"Mapped ticker '{ticker_input}' to {base}/{target}")
                return base, target
    elif '_' in ticker:
        # Format like EUR_USD
        parts = ticker.split('_')
        if len(parts) == 2:
            base, target = parts[0].strip(), parts[1].strip()
            if base in supported_currencies and target in supported_currencies:
                logger.print_info(f"Mapped ticker '{ticker_input}' to {base}/{target}")
                return base, target
    
    # Special handling for crypto-like tickers (but only if they're actual currency pairs)
    if ticker.endswith('USDT') and len(ticker) > 4:
        # This might be a crypto ticker, but Exchange Rate API doesn't support crypto
        logger.print_warning(f"Exchange Rate API does not support cryptocurrency pairs. '{ticker_input}' may not be available.")
        return None
    
    logger.print_error(f"Could not map ticker '{ticker_input}' to Exchange Rate API format. Supported currencies: {sorted(list(supported_currencies)[:10])}...")
    return None


def fetch_exrate_data(ticker: str, interval: str, start_date: str, end_date: str) -> tuple[pd.DataFrame | None, dict]:
    """
    Downloads current exchange rate data from Exchange Rate API.
    
    NOTE: This fetcher only provides current exchange rates (free plan limitation).
    Historical data requires a paid plan. Date parameters are ignored.
    
    Args:
        ticker (str): The currency pair (e.g., 'EURUSD', 'GBPJPY')
        interval (str): The data interval (ignored, always current)
        start_date (str): Start date (ignored for current data)
        end_date (str): End date (ignored for current data)
        
    Returns:
        tuple[pd.DataFrame | None, dict]: DataFrame with current OHLCV data and metrics
    """
    # Map ticker and interval
    ticker_mapping = map_exrate_ticker(ticker)
    if ticker_mapping is None:
        return None, {"error_message": f"Invalid ticker format: {ticker}"}
    
    base_currency, target_currency = ticker_mapping
    exrate_interval = map_exrate_interval(interval)
    
    if exrate_interval is None:
        return None, {"error_message": f"Invalid interval: {interval}"}
    
    # Warn user about date limitations
    logger.print_warning("Exchange Rate API (free plan) only provides current exchange rates.")
    logger.print_warning("Historical data requires a paid plan. Ignoring date range and fetching current rate.")
    
    logger.print_info(f"Fetching current Exchange Rate data for: {base_currency}/{target_currency}")
    
    # Initialize metrics
    metrics = {"latency_sec": 0.0, "error_message": None, "api_calls": 0, "rows_fetched": 0}
    
    # Get API key from environment
    api_key = os.getenv("EXCHANGE_RATE_API_KEY")
    if not api_key:
        error_msg = "EXCHANGE_RATE_API_KEY not found in environment variables. Please add it to .env file."
        logger.print_error(error_msg)
        metrics["error_message"] = error_msg
        return None, metrics
    
    try:
        # Use the current rates endpoint (works with free plan)
        url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/{base_currency}"
        
        logger.print_info(f"Fetching current rates from Exchange Rate API...")
        
        start_time = time.perf_counter()
        response = requests.get(url, timeout=30)
        end_time = time.perf_counter()
        
        metrics["api_calls"] = 1
        metrics["latency_sec"] = (end_time - start_time)
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get("result") == "success":
                conversion_rates = data.get("conversion_rates", {})
                
                if target_currency in conversion_rates:
                    rate = conversion_rates[target_currency]
                    current_time = datetime.now()
                    
                    # Create a single-row DataFrame with current rate
                    row_data = {
                        'Open': rate,
                        'High': rate,
                        'Low': rate,
                        'Close': rate,
                        'Volume': 0  # Exchange Rate API doesn't provide volume
                    }
                    
                    df = pd.DataFrame([row_data], index=[current_time])
                    df.index.name = 'DateTime'
                    df.index = pd.to_datetime(df.index)
                    
                    # Ensure numeric columns
                    for col in ['Open', 'High', 'Low', 'Close', 'Volume']:
                        df[col] = pd.to_numeric(df[col], errors='coerce')
                    
                    metrics["rows_fetched"] = 1
                    
                    logger.print_success(f"Successfully fetched current exchange rate: {base_currency}/{target_currency} = {rate}")
                    return df, metrics
                else:
                    error_msg = f"{target_currency} not found in current rates"
                    logger.print_error(error_msg)
                    metrics["error_message"] = error_msg
                    return None, metrics
            elif data.get("error-type") == "invalid-key":
                error_msg = "Invalid API key. Please check your EXCHANGE_RATE_API_KEY in .env file."
                logger.print_error(error_msg)
                metrics["error_message"] = error_msg
                return None, metrics
            else:
                error_detail = data.get("error-type", "Unknown error")
                error_msg = f"API Error: {error_detail}"
                logger.print_error(error_msg)
                metrics["error_message"] = error_msg
                return None, metrics
        else:
            error_msg = f"HTTP Error {response.status_code}: {response.text}"
            logger.print_error(error_msg)
            metrics["error_message"] = error_msg
            return None, metrics
            
    except requests.exceptions.RequestException as e:
        error_msg = f"Network error: {e}"
        logger.print_error(error_msg)
        metrics["error_message"] = error_msg
        return None, metrics
    except Exception as e:
        error_msg = f"Unexpected error in Exchange Rate API fetch: {e}"
        logger.print_error(error_msg)
        traceback.print_exc()
        metrics["error_message"] = error_msg
        return None, metrics
