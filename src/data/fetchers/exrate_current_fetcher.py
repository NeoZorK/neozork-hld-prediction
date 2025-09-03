# src/../data/fetchers/exrate_current_fetcher.py

"""
Contains functions related to fetching current exchange rate data from Exchange Rate API.
This version works with the free plan by fetching current rates only.
All comments are in English.
"""

import pandas as pd
import numpy as np
import os
import time
import traceback
import requests
from datetime import datetime, timedelta

# Use absolute import for logger
from src.common import logger


def fetch_exrate_current_data(ticker: str, interval: str = "D1") -> tuple[pd.DataFrame | None, dict]:
    """
    Downloads current exchange rate data from Exchange Rate API (works with free plan).
    Creates a single-row DataFrame with current exchange rate.
    
    Args:
        ticker (str): The currency pair (e.g., 'EURUSD', 'GBPJPY')
        interval (str): The data interval (ignored, always daily)
        
    Returns:
        tuple[pd.DataFrame | None, dict]: DataFrame with current OHLCV data and metrics
    """
    # Import the mapping functions from the main fetcher
    from .exrate_fetcher import map_exrate_ticker, map_exrate_interval
    
    # Map ticker and interval
    ticker_mapping = map_exrate_ticker(ticker)
    if ticker_mapping is None:
        return None, {"error_message": f"Invalid ticker format: {ticker}"}
    
    base_currency, target_currency = ticker_mapping
    exrate_interval = map_exrate_interval(interval)
    
    if exrate_interval is None:
        return None, {"error_message": f"Invalid interval: {interval}"}
    
    logger.print_info(f"Fetching current Exchange Rate data for: {base_currency}/{target_currency}")
    
    # Initialize metrics
    metrics = {"latency_sec": 0.0, "error_message": None, "api_calls": 0, "rows_fetched": 0}
    
    # Get API key from environment
    api_key = os.getenv("EXCHANGE_RATE_API_KEY")
    if not api_key:
        error_msg = "EXCHANGE_RATE_API_KEY not found in environment variables. Please add it to .env file."
        logger.print_error(error_msg)
        return None, {"error_message": error_msg}
    
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
                    return None, {"error_message": error_msg, **metrics}
            elif data.get("error-type") == "invalid-key":
                error_msg = "Invalid API key. Please check your EXCHANGE_RATE_API_KEY in .env file."
                logger.print_error(error_msg)
                return None, {"error_message": error_msg, **metrics}
            else:
                error_detail = data.get("error-type", "Unknown error")
                error_msg = f"API Error: {error_detail}"
                logger.print_error(error_msg)
                return None, {"error_message": error_msg, **metrics}
        else:
            error_msg = f"HTTP Error {response.status_code}: {response.text}"
            logger.print_error(error_msg)
            return None, {"error_message": error_msg, **metrics}
            
    except requests.exceptions.RequestException as e:
        error_msg = f"Network error: {e}"
        logger.print_error(error_msg)
        return None, {"error_message": error_msg, **metrics}
    except Exception as e:
        error_msg = f"Unexpected error in Exchange Rate API fetch: {e}"
        logger.print_error(error_msg)
        traceback.print_exc()
        return None, {"error_message": error_msg, **metrics}
