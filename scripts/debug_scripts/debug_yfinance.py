# debug_yfinance.py
import yfinance as yf
import pandas as pd
import json
import time
import requests
import random
import logging
import os
import sys
from requests.exceptions import RequestException
from typing import List, Dict, Optional, Union, Tuple
from datetime import datetime
from urllib.parse import urlencode
import urllib3

# Disable InsecureRequestWarning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Define log directory
LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "logs")
# Ensure log directory exists
os.makedirs(LOG_DIR, exist_ok=True)
# Log file path
LOG_FILE = os.path.join(LOG_DIR, "yfinance_debug.log")

# Setup basic logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(LOG_FILE)
    ]
)
logger = logging.getLogger('yfinance_debug')

# User agent list to rotate and avoid blocking
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1'
]

# List of tickers to download - a mix of stocks, forex, crypto, and ETFs
# Format for forex pairs is typically "EURUSD=X" in yfinance
# Crypto is usually formatted as "BTC-USD" or "ETH-USD"
# Note: Maximum 5 tickers as per requirements
DEFAULT_TICKERS = [
    'AAPL',     # Apple (stock)
    'EURUSD=X', # Euro/USD (forex)
    'BTC-USD',  # Bitcoin/USD (crypto)
    'GLD',      # SPDR Gold Shares (ETF)
    'CL=F'      # Crude Oil Futures
]
PERIOD = '1mo'
INTERVAL = '1d'

# Create cache directory if it doesn't exist
CACHE_DIR = ".yf_cache"
os.makedirs(CACHE_DIR, exist_ok=True)

# Alternative direct API URL for testing connectivity
YF_API_URL = "https://query1.finance.yahoo.com/v8/finance/chart/"

class YFinanceDownloader:
    """Class to handle downloading data from Yahoo Finance with proper rate limiting and error handling."""

    def __init__(self, cache_dir: str = CACHE_DIR, single_attempt: bool = False):
        """Initialize the downloader with cache directory and session setup."""
        self.cache_dir = cache_dir
        self.session = self._create_session()
        yf.set_tz_cache_location(cache_dir)

        # Configure pandas display
        pd.set_option('display.max_rows', 10)
        pd.set_option('display.max_columns', 10)

        # Rate limiting parameters
        self.request_delay = 3.0  # Base delay between requests in seconds
        self.retry_delay_base = 5.0  # Base delay for retry
        # Set max_retries based on input parameter
        self.max_retries = 1 if single_attempt else 2
        self.backoff_factor = 2.0
        self.jitter = 0.5  # Random jitter to add to delays

        # Results tracking
        self.successful_downloads = []
        self.failed_downloads = []

        # Check if we can reach Yahoo Finance
        self.check_connectivity()

    def check_connectivity(self) -> bool:
        """
        Check if we can reach Yahoo Finance API.
        Returns True if connected, False otherwise.
        """
        test_url = "https://finance.yahoo.com"
        try:
            logger.info(f"Testing connectivity to Yahoo Finance...")
            response = self.session.get(test_url, timeout=10)
            if response.status_code == 200:
                logger.info(f"Successfully connected to Yahoo Finance!")
                return True
            else:
                logger.warning(f"Connected to Yahoo Finance but received status code: {response.status_code}")
                return False
        except Exception as e:
            logger.error(f"Failed to connect to Yahoo Finance: {str(e)}")
            return False

    def _create_session(self) -> requests.Session:
        """Create and configure a requests session with appropriate headers."""
        session = requests.Session()
        session.headers.update({
            'User-Agent': random.choice(USER_AGENTS),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Cache-Control': 'max-age=0',
            'DNT': '1',  # Do Not Track
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Pragma': 'no-cache'
        })
        return session

    def _rotate_user_agent(self) -> None:
        """Rotate the User-Agent header to avoid detection."""
        self.session.headers.update({
            'User-Agent': random.choice(USER_AGENTS)
        })

    def _calculate_delay(self, attempt: int) -> float:
        """Calculate delay time with exponential backoff and jitter."""
        if attempt == 0:
            return self.request_delay + random.uniform(0, self.jitter)

        delay = self.retry_delay_base * (self.backoff_factor ** (attempt)) + random.uniform(0, self.jitter * attempt)
        return min(delay, 30.0)  # Cap at 30 seconds

    def direct_api_request(self, ticker: str, period: str, interval: str) -> Optional[pd.DataFrame]:
        """
        Make a direct API request to Yahoo Finance API for historical data.
        This bypasses yfinance library for troubleshooting purposes.
        """
        # Translate yfinance period to API parameters
        period_map = {
            '1d': {'range': '1d', 'interval': '1m'},
            '5d': {'range': '5d', 'interval': '15m'},
            '1mo': {'range': '1mo', 'interval': '1d'},
            '3mo': {'range': '3mo', 'interval': '1d'},
            '6mo': {'range': '6mo', 'interval': '1d'},
            '1y': {'range': '1y', 'interval': '1d'},
            '2y': {'range': '2y', 'interval': '1d'},
            '5y': {'range': '5y', 'interval': '1wk'},
            'max': {'range': 'max', 'interval': '1mo'}
        }

        # Map yfinance interval to API interval parameter
        interval_map = {
            '1m': '1m', '2m': '2m', '5m': '5m', '15m': '15m', '30m': '30m',
            '60m': '60m', '90m': '90m', '1h': '60m', '1d': '1d',
            '5d': '5d', '1wk': '1wk', '1mo': '1mo', '3mo': '3mo'
        }

        # Build API parameters
        params = {
            'range': period_map.get(period, {}).get('range', '1mo'),
            'interval': interval_map.get(interval, '1d'),
            'includePrePost': 'false',
            'events': 'div,splits',
            'lang': 'en-US',
            'region': 'US'
        }

        url = f"{YF_API_URL}{ticker}"

        try:
            logger.info(f"Making direct API request to {url} with params: {params}")
            response = self.session.get(url, params=params, timeout=15)

            if response.status_code == 200:
                data = response.json()
                logger.info(f"Received API response for {ticker}: {len(response.content)} bytes")

                # Debug - save raw response
                debug_file = f"{self.cache_dir}/{ticker}_raw_response.json"
                with open(debug_file, 'w') as f:
                    json.dump(data, f, indent=2)
                logger.info(f"Saved raw response to {debug_file}")

                # Check if we have valid chart data
                if 'chart' in data and 'result' in data['chart'] and data['chart']['result']:
                    chart_data = data['chart']['result'][0]

                    # Extract timestamps
                    timestamps = chart_data.get('timestamp', [])

                    # Extract quote data
                    quote = chart_data.get('indicators', {}).get('quote', [{}])[0]

                    if timestamps and quote and 'close' in quote:
                        # Create DataFrame
                        df = pd.DataFrame({
                            'Open': quote.get('open', []),
                            'High': quote.get('high', []),
                            'Low': quote.get('low', []),
                            'Close': quote.get('close', []),
                            'Volume': quote.get('volume', []),
                        }, index=pd.to_datetime([datetime.fromtimestamp(ts) for ts in timestamps]))

                        return df
                    else:
                        logger.error(f"No price data in response for {ticker}")
                else:
                    logger.error(f"Invalid API response format for {ticker}")
            else:
                logger.error(f"API request failed with status {response.status_code}: {response.text}")

        except Exception as e:
            logger.error(f"Error in direct API request for {ticker}: {str(e)}")

        return None

    def download_ticker(self, ticker: str, period: str, interval: str) -> Optional[pd.DataFrame]:
        """
        Download data for a single ticker with retry logic.

        Args:
            ticker: Stock symbol
            period: Time period (e.g., '1mo', '1y')
            interval: Time interval (e.g., '1d', '1h')

        Returns:
            DataFrame with price data or None if all attempts fail
        """
        logger.info(f"Starting download for ticker: {ticker}, period: {period}, interval: {interval}")

        # First try to load from existing CSV file if available
        csv_path = f"{self.cache_dir}/{ticker}_{period}_{interval}.csv"
        if os.path.exists(csv_path):
            try:
                logger.info(f"Found existing data in {csv_path}, loading...")
                data = pd.read_csv(csv_path, index_col=0, parse_dates=True)
                if not data.empty:
                    logger.info(f"Successfully loaded {len(data)} rows from cache for {ticker}")
                    self.successful_downloads.append(ticker)
                    return data
            except Exception as e:
                logger.warning(f"Failed to load cached data for {ticker}: {str(e)}")

        for attempt in range(self.max_retries):
            try:
                # Calculate and apply delay with backoff
                delay = self._calculate_delay(attempt)
                if attempt > 0:
                    logger.info(f"Retry attempt {attempt+1}/{self.max_retries} after {delay:.2f}s delay...")
                    time.sleep(delay)

                # Rotate User-Agent between attempts
                self._rotate_user_agent()

                # First, try direct API request as a new approach
                data = self.direct_api_request(ticker, period, interval)
                if data is not None and not data.empty:
                    logger.info(f"Successfully downloaded {len(data)} rows for {ticker} via direct API")
                    return data

                # If direct API failed, try using yfinance library
                logger.info(f"Direct API approach failed for {ticker}, trying yfinance library...")
                time.sleep(1.0)  # Small pause before next attempt

                # Create a new ticker object for each attempt
                ticker_obj = yf.Ticker(ticker, session=self.session)

                # Try the history method first
                data = ticker_obj.history(
                    period=period,
                    interval=interval,
                    auto_adjust=True,
                    prepost=False,
                    actions=True,
                    back_adjust=False
                )

                # If no data, try the download method as a fallback
                if data is None or data.empty:
                    logger.info(f"Ticker.history failed for {ticker}, trying yf.download()...")
                    time.sleep(1.0)  # Small pause before the second attempt

                    data = yf.download(
                        tickers=ticker,
                        period=period,
                        interval=interval,
                        progress=True,
                        auto_adjust=True,
                        prepost=False,
                        actions=True,
                        ignore_tz=False,
                        threads=False,
                        session=self.session,
                        rounding=True
                    )

                # Check if we got valid data
                if data is not None and not data.empty:
                    logger.info(f"Successfully downloaded {len(data)} rows for {ticker}")
                    return data
                else:
                    logger.error(f"No data returned for {ticker}, attempt {attempt+1}")

            except Exception as e:
                logger.error(f"Error downloading {ticker} (attempt {attempt+1}): {str(e)}")

                # Add extra delay if we hit rate limits
                if "429" in str(e) or "Too Many Requests" in str(e):
                    extra_delay = 60.0 + random.uniform(0, 30.0)  # 1-1.5 minute delay
                    logger.warning(f"Rate limit hit, waiting {extra_delay:.2f}s before next attempt")
                    time.sleep(extra_delay)

        # If we get here, all attempts failed
        logger.error(f"All {self.max_retries} attempts failed for {ticker}")
        self.failed_downloads.append(ticker)
        return None

    def download_multiple(self, tickers: List[str], period: str, interval: str) -> Dict[str, Optional[pd.DataFrame]]:
        """
        Download data for multiple tickers with appropriate delays between requests.

        Args:
            tickers: List of stock symbols (max 5)
            period: Time period
            interval: Time interval

        Returns:
            Dictionary mapping tickers to their DataFrame results (or None if failed)
        """
        # Ensure we don't exceed the maximum number of tickers
        if len(tickers) > 5:
            logger.warning(f"Too many tickers provided ({len(tickers)}). Limiting to first 5.")
            tickers = tickers[:5]

        results = {}

        for i, ticker in enumerate(tickers):
            print(f"\n[{i+1}/{len(tickers)}] Processing ticker: {ticker}")

            # Add delay between ticker requests to avoid rate limiting
            if i > 0:
                between_delay = self.request_delay * 2 + random.uniform(0, 2.0)
                logger.info(f"Waiting {between_delay:.2f}s before processing next ticker...")
                time.sleep(between_delay)

            data = self.download_ticker(ticker, period, interval)
            results[ticker] = data

            if data is not None:
                self.successful_downloads.append(ticker)

                # Save the data to CSV
                csv_path = f"{self.cache_dir}/{ticker}_{period}_{interval}.csv"
                data.to_csv(csv_path)
                logger.info(f"Saved data to {csv_path}")

        return results

    def print_summary(self) -> None:
        """Print a summary of the download results."""
        print("\n" + "="*50)
        print(f"DOWNLOAD SUMMARY ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')})")
        print("="*50)

        total = len(self.successful_downloads) + len(self.failed_downloads)
        success_rate = len(self.successful_downloads) / total * 100 if total > 0 else 0

        print(f"Total tickers processed: {total}")
        print(f"Successfully downloaded: {len(self.successful_downloads)} ({success_rate:.1f}%)")
        print(f"Failed downloads: {len(self.failed_downloads)} ({100-success_rate:.1f}%)")

        if self.successful_downloads:
            print("\nSuccessful tickers:")
            for ticker in self.successful_downloads:
                print(f"  - {ticker}")

        if self.failed_downloads:
            print("\nFailed tickers:")
            for ticker in self.failed_downloads:
                print(f"  - {ticker}")

        print("="*50)

def prompt_for_tickers() -> List[str]:
    """Ask user which tickers to run tests for."""
    selected_tickers = []

    print("\n=== Ticker Selection for YFinance API Test ===")
    print("Available tickers:")

    for i, ticker in enumerate(DEFAULT_TICKERS, 1):
        print(f"{i}. {ticker}")

    print("\nFor each ticker, indicate if you want to run it (y/n):")

    for ticker in DEFAULT_TICKERS:
        while True:
            try:
                response = input(f"Run test for {ticker}? (y/n): ").strip().lower()
                print(f"Received response '{response}' for {ticker}")  # Debug output
                if response in ('y', 'n'):
                    if response == 'y':
                        selected_tickers.append(ticker)
                        print(f"Added {ticker} to selected tickers")  # Debug output
                    break
                else:
                    print("Please enter 'y' or 'n'")
            except Exception as e:
                print(f"Error reading input: {str(e)}")
                return DEFAULT_TICKERS[:1]  # Return first ticker as fallback

    print(f"Selected tickers so far: {selected_tickers}")  # Debug output

    # Allow adding custom ticker if needed
    try:
        response = input("\nAdd a custom ticker? (y/n): ").strip().lower()
        if response == 'y':
            custom_ticker = input("Enter ticker symbol: ").strip().upper()
            if custom_ticker:
                selected_tickers.append(custom_ticker)
                print(f"Added custom ticker: {custom_ticker}")  # Debug output
    except Exception as e:
        print(f"Error reading input for custom ticker: {str(e)}")

    # If no tickers selected, use first default ticker as a fallback
    if not selected_tickers:
        print(f"No tickers selected, using {DEFAULT_TICKERS[0]} as default")
        selected_tickers = [DEFAULT_TICKERS[0]]

    print(f"Final selected tickers: {selected_tickers}")  # Debug output
    return selected_tickers

def main():
    """Main function to run the Yahoo Finance downloader."""
    print(f"--- YFinance Downloader Test ---")

    # Check if we're in Docker environment
    in_docker = os.environ.get('DOCKER_CONTAINER', False) or os.path.exists('/.dockerenv')
    single_attempt = in_docker  # Use single attempt in Docker

    # Determine tickers to use
    if in_docker:
        print("Running in Docker environment - using single attempt mode")
        print("Max attempts per ticker: 1")
        tickers = prompt_for_tickers()
        if not tickers:
            print("No tickers selected. Exiting.")
            return
    else:
        tickers = DEFAULT_TICKERS
        print(f"Tickers: {', '.join(tickers)}")
        print(f"Max attempts per ticker: 2")

    print(f"Period: {PERIOD}, Interval: {INTERVAL}")
    print(f"Cache directory: {CACHE_DIR}")
    print("-" * 40)

    try:
        # Create and run the downloader
        downloader = YFinanceDownloader(cache_dir=CACHE_DIR, single_attempt=single_attempt)
        results = downloader.download_multiple(tickers, PERIOD, INTERVAL)

        # Print summary of results
        downloader.print_summary()

    except Exception as e:
        logger.error(f"Fatal error in main: {str(e)}", exc_info=True)

    print("\n--- End of Test ---")


if __name__ == "__main__":
    main()
