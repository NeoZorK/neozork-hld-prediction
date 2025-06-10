# src/utils.py

"""
General utility functions, including point size estimation using yfinance info.
All comments are in English.
"""
import yfinance as yf
from ..common import logger

def determine_point_size(ticker: str) -> float | None:
    """
    Estimates the instrument's point size based on yfinance info (quoteType, price).
    Returns None if info cannot be fetched or estimation fails.
    NOTE: This is an ESTIMATE and may be inaccurate. Use --point to override.
    """
    logger.print_info(f"Attempting to automatically determine point size for {ticker}...")
    try:
        yf_ticker_obj = yf.Ticker(ticker)
        # Fetching info can sometimes fail for various reasons
        info = yf_ticker_obj.info

        quote_type = info.get('quoteType')
        currency = info.get('currency', '').upper()
        # Try different price fields, as availability varies
        market_price = info.get('regularMarketPrice') or info.get('currentPrice') or info.get('bid') or info.get('ask')

        if quote_type == 'CURRENCY':
            # Forex pairs: 0.00001 generally, 0.001 for JPY pairs
            if 'JPY' in ticker.upper() or currency == 'JPY':
                 point = 0.001
                 logger.print_info(f"QuoteType is CURRENCY (JPY Pair?), estimating point size: {point}")
            else:
                 point = 0.00001
                 logger.print_info(f"QuoteType is CURRENCY, estimating point size: {point}")
        elif quote_type == 'CRYPTOCURRENCY':
            # Crypto point sizes vary wildly. Use price magnitude as a basic guess.
            if market_price is not None and market_price > 0:
                if market_price < 0.001: point = 0.000001
                elif market_price < 0.1: point = 0.0001
                elif market_price < 10: point = 0.001 # Adjusted for lower price crypto
                elif market_price < 1000: point = 0.01
                else: point = 0.1 # Rough guess for high value crypto (BTC)
            else:
                point = 0.01 # Default guess if price is unavailable
            logger.print_info(f"QuoteType is CRYPTOCURRENCY, estimating point size based on price/default: {point}")
        elif quote_type in ['EQUITY', 'ETF', 'INDEX', 'MUTUALFUND']:
            # Most stocks/ETFs trade in cents in major markets (like US)
            point = 0.01
            logger.print_info(f"QuoteType is {quote_type}, estimating point size: {point}")
        elif quote_type == 'FUTURE':
             # Futures vary significantly. Cannot reliably guess.
             logger.print_warning(f"Cannot reliably estimate point size for FUTURE {ticker}. Please use --point.")
             point = None # Indicate failure
        else:
            # Default guess for unknown types
            logger.print_warning(f"Unknown quoteType '{quote_type}' for {ticker}. Cannot reliably estimate point size. Please use --point.")
            point = None # Indicate failure

        # Final sanity check
        if point is not None and point <= 0:
            logger.print_warning(f"Estimated point size ({point}) is non-positive. Estimation failed.")
            return None

        return point

    except Exception as e:
        # Catch exceptions during yf.Ticker(ticker).info call
        logger.print_error(f"Could not fetch Ticker info for {ticker} to estimate point size: {type(e).__name__}: {e}")
        return None # Indicate failure to estimate