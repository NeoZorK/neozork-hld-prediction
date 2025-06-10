# src/data/fetchers/demo_fetcher.py

"""
Contains the function to generate demonstration OHLCV data.
"""

import pandas as pd
import time
from datetime import date, timedelta
from ...common import logger # Relative import


# Definition of the get_demo_data function
def get_demo_data() -> pd.DataFrame:
    """Returns the demonstration DataFrame."""
    logger.print_info("Generating demo data...")
    time.sleep(0.5) # Simulate delay
    data = {
        'Open': [1.1, 1.11, 1.12, 1.115, 1.125, 1.13, 1.128, 1.135, 1.14, 1.138, 1.142, 1.145, 1.140, 1.135, 1.130, 1.132, 1.138, 1.145, 1.148, 1.150, 1.152, 1.155, 1.153, 1.158, 1.160, 1.157, 1.162, 1.165, 1.163, 1.160],
        'High': [1.105, 1.115, 1.125, 1.12, 1.13, 1.135, 1.133, 1.14, 1.145, 1.142, 1.146, 1.148, 1.143, 1.139, 1.136, 1.137, 1.142, 1.150, 1.152, 1.155, 1.156, 1.159, 1.158, 1.161, 1.163, 1.160, 1.165, 1.168, 1.166, 1.164],
        'Low': [1.095, 1.105, 1.115, 1.11, 1.12, 1.125, 1.125, 1.13, 1.135, 1.136, 1.140, 1.142, 1.138, 1.133, 1.128, 1.130, 1.135, 1.143, 1.146, 1.148, 1.150, 1.152, 1.151, 1.155, 1.157, 1.154, 1.159, 1.161, 1.160, 1.158],
        'Close': [1.1, 1.11, 1.118, 1.118, 1.128, 1.128, 1.131, 1.138, 1.138, 1.14, 1.145, 1.141, 1.136, 1.131, 1.131, 1.136, 1.144, 1.149, 1.151, 1.149, 1.155, 1.154, 1.157, 1.160, 1.159, 1.158, 1.163, 1.164, 1.161, 1.159],
        'Volume': [1000, 1200, 1100, 1300, 1500, 1400, 1600, 1700, 1550, 1650, 1750, 1800, 1600, 1900, 2000, 1850, 1950, 2100, 2050, 2200, 2150, 2250, 2100, 2300, 2400, 2350, 2450, 2500, 2400, 2300]
    }
    # Generate index based on current date
    start_date_idx = date.today() - timedelta(days=len(data['Open'])-1)
    index = pd.date_range(start=start_date_idx, periods=len(data['Open']), freq='D')
    df = pd.DataFrame(data, index=index)
    # Standardize column names
    df.columns = ['Open', 'High', 'Low', 'Close', 'Volume']
    return df