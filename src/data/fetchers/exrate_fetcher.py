# src/../data/fetchers/exrate_fetcher.py

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

# Use absolute import for logger
from src.common import logger


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


def fetch_exrate_data(ticker: str, interval: str, start_date: str = None, end_date: str = None) -> tuple[pd.DataFrame | None, dict]:
    """
    Downloads exchange rate data from Exchange Rate API.
    
    - Free plan: Provides only current exchange rates (interval used for validation only)
    - Paid plan: Provides historical data for the specified interval and date range
    
    Args:
        ticker (str): The currency pair (e.g., 'EURUSD', 'GBPJPY')
        interval (str): The data interval (used for paid plan historical data)
        start_date (str, optional): Start date (YYYY-MM-DD) for historical data (paid plan only)
        end_date (str, optional): End date (YYYY-MM-DD) for historical data (paid plan only)
        
    Returns:
        tuple[pd.DataFrame | None, dict]: DataFrame with OHLCV data and metrics
    """
    # Map ticker and interval
    ticker_mapping = map_exrate_ticker(ticker)
    if ticker_mapping is None:
        return None, {"error_message": f"Invalid ticker format: {ticker}"}
    
    base_currency, target_currency = ticker_mapping
    exrate_interval = map_exrate_interval(interval)
    
    if exrate_interval is None:
        return None, {"error_message": f"Invalid interval: {interval}"}
    
    logger.print_info(f"Fetching Exchange Rate data for: {base_currency}/{target_currency}")
    
    # Initialize metrics
    metrics = {"latency_sec": 0.0, "error_message": None, "api_calls": 0, "rows_fetched": 0}
    
    # Get API key from environment
    api_key = os.getenv("EXCHANGE_RATE_API_KEY")
    if not api_key:
        error_msg = "EXCHANGE_RATE_API_KEY not found in environment variables. Please add it to .env file."
        logger.print_error(error_msg)
        metrics["error_message"] = error_msg
        return None, metrics
    
    # Determine if we should try historical data (paid plan) or current data (free plan)
    use_historical = start_date is not None and end_date is not None
    
    if use_historical:
        logger.print_info(f"Attempting to fetch historical data from {start_date} to {end_date}")
        logger.print_info("Note: Historical data requires a paid Exchange Rate API plan")
        return _fetch_historical_exrate_data(base_currency, target_currency, api_key, start_date, end_date, metrics)
    else:
        logger.print_info("Fetching current exchange rate (free plan compatible)")
        return _fetch_current_exrate_data(base_currency, target_currency, api_key, metrics)


def _fetch_current_exrate_data(base_currency: str, target_currency: str, api_key: str, metrics: dict) -> tuple[pd.DataFrame | None, dict]:
    """Fetch current exchange rate data (free plan compatible)."""
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


def _fetch_historical_exrate_data(base_currency: str, target_currency: str, api_key: str, start_date: str, end_date: str, metrics: dict) -> tuple[pd.DataFrame | None, dict]:
    """Fetch historical exchange rate data (paid plan required)."""
    try:
        # Parse dates
        start_dt = datetime.strptime(start_date, '%Y-%m-%d')
        end_dt = datetime.strptime(end_date, '%Y-%m-%d')
        
        # Validate date range
        if start_dt > end_dt:
            error_msg = "Start date must be before end date"
            logger.print_error(error_msg)
            metrics["error_message"] = error_msg
            return None, metrics
        
        # Generate date range for daily data (Exchange Rate API provides daily rates)
        date_range = pd.date_range(start=start_dt, end=end_dt, freq='D')
        
        all_data = []
        total_calls = 0
        total_latency = 0.0
        
        # Progress bar for multiple API calls
        with tqdm(total=len(date_range), desc="Fetching historical rates") as pbar:
            for date in date_range:
                date_str = date.strftime('%Y-%m-%d')
                
                # Use historical endpoint (requires paid plan)
                url = f"https://v6.exchangerate-api.com/v6/{api_key}/history/{base_currency}/{date_str}"
                
                start_time = time.perf_counter()
                response = requests.get(url, timeout=30)
                end_time = time.perf_counter()
                
                total_calls += 1
                total_latency += (end_time - start_time)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    if data.get("result") == "success":
                        conversion_rates = data.get("conversion_rates", {})
                        
                        if target_currency in conversion_rates:
                            rate = conversion_rates[target_currency]
                            
                            # Create OHLCV data (all same for daily rate)
                            row_data = {
                                'Open': rate,
                                'High': rate,
                                'Low': rate,
                                'Close': rate,
                                'Volume': 0
                            }
                            
                            all_data.append((date, row_data))
                        else:
                            logger.print_warning(f"No {target_currency} rate for {date_str}")
                    elif data.get("error-type") == "invalid-key":
                        error_msg = "Invalid API key. Please check your EXCHANGE_RATE_API_KEY in .env file."
                        logger.print_error(error_msg)
                        metrics["error_message"] = error_msg
                        return None, metrics
                    elif data.get("error-type") == "inactive-account":
                        error_msg = "Historical data requires a paid Exchange Rate API plan. Current account is on free plan."
                        logger.print_error(error_msg)
                        logger.print_info("Falling back to current rate only...")
                        metrics["error_message"] = error_msg
                        # Fall back to current data
                        return _fetch_current_exrate_data(base_currency, target_currency, api_key, metrics)
                    else:
                        error_detail = data.get("error-type", "Unknown error")
                        logger.print_warning(f"API Error for {date_str}: {error_detail}")
                else:
                    logger.print_warning(f"HTTP Error {response.status_code} for {date_str}")
                
                pbar.update(1)
                
                # Small delay to respect rate limits
                time.sleep(0.1)
        
        metrics["api_calls"] = total_calls
        metrics["latency_sec"] = total_latency
        
        if not all_data:
            error_msg = "No historical data retrieved"
            logger.print_error(error_msg)
            metrics["error_message"] = error_msg
            return None, metrics
        
        # Create DataFrame from collected data
        dates, rows = zip(*all_data)
        df = pd.DataFrame(list(rows), index=list(dates))
        df.index.name = 'DateTime'
        df.index = pd.to_datetime(df.index)
        
        # Ensure numeric columns
        for col in ['Open', 'High', 'Low', 'Close', 'Volume']:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        
        metrics["rows_fetched"] = len(df)
        
        logger.print_success(f"Successfully fetched {len(df)} historical exchange rates: {base_currency}/{target_currency}")
        return df, metrics
        
    except ValueError as e:
        error_msg = f"Date parsing error: {e}"
        logger.print_error(error_msg)
        metrics["error_message"] = error_msg
        return None, metrics
    except requests.exceptions.RequestException as e:
        error_msg = f"Network error: {e}"
        logger.print_error(error_msg)
        metrics["error_message"] = error_msg
        return None, metrics
    except Exception as e:
        error_msg = f"Unexpected error in historical Exchange Rate API fetch: {e}"
        logger.print_error(error_msg)
        traceback.print_exc()
        metrics["error_message"] = error_msg
        return None, metrics
