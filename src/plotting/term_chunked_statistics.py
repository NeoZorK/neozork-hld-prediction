# -*- coding: utf-8 -*-
# src/plotting/term_chunked_statistics.py

"""
Statistics functions for terminal chunked plotting.
Contains functions for displaying chunk and field statistics.
"""

import pandas as pd
import numpy as np

# Use absolute imports when possible, fallback to relative
try:
    from common import logger
    from common.constants import TradingRule, BUY, SELL, NOTRADE
except ImportError:
    # Fallback to relative imports when run as module
    from ..common import logger
    from ..common.constants import TradingRule, BUY, SELL, NOTRADE


def _show_chunk_statistics(chunk: pd.DataFrame, title: str, start_idx: int, end_idx: int) -> None:
    """
    Show statistics for a chunk.
    
    Args:
        chunk (pd.DataFrame): DataFrame chunk
        title (str): Chunk title
        start_idx (int): Start index
        end_idx (int): End index
    """
    try:
        header_line = "=" * 80
        print(f"\n{header_line}")
        print(f"{title.upper():^80}")
        print(f"Candles {start_idx+1}-{end_idx} ({len(chunk)} bars)")
        print(f"{header_line}")
        
        # OHLC statistics
        ohlc_columns = ['Open', 'High', 'Low', 'Close']
        has_ohlc = all(col in chunk.columns for col in ohlc_columns)
        
        if has_ohlc:
            print(f"OHLC STATISTICS:")
            print(f"   Open:  {chunk['Open'].min():.5f} - {chunk['Open'].max():.5f}")
            print(f"   High:  {chunk['High'].min():.5f} - {chunk['High'].max():.5f}")
            print(f"   Low:   {chunk['Low'].min():.5f} - {chunk['Low'].max():.5f}")
            print(f"   Close: {chunk['Close'].min():.5f} - {chunk['Close'].max():.5f}")
        
        # Volume statistics
        if 'Volume' in chunk.columns:
            volume = chunk['Volume'].fillna(0)
            print(f"VOLUME STATISTICS:")
            print(f"   Total: {volume.sum():.0f}")
            print(f"   Avg:   {volume.mean():.0f}")
            print(f"   Max:   {volume.max():.0f}")
        
        # Trading signals
        if 'Direction' in chunk.columns:
            buy_count = (chunk['Direction'] == BUY).sum()
            sell_count = (chunk['Direction'] == SELL).sum()
            notrade_count = (chunk['Direction'] == NOTRADE).sum()
            
            print(f"TRADING SIGNALS:")
            print(f"   BUY:     {buy_count}")
            print(f"   SELL:    {sell_count}")
            print(f"   NO TRADE: {notrade_count}")
        
        # RSI statistics
        if 'RSI' in chunk.columns:
            rsi = chunk['RSI'].dropna()
            if len(rsi) > 0:
                print(f"RSI STATISTICS:")
                print(f"   Min: {rsi.min():.2f}")
                print(f"   Max: {rsi.max():.2f}")
                print(f"   Avg: {rsi.mean():.2f}")
        
        print(f"{header_line}\n")
        
    except Exception as e:
        logger.print_error(f"Error showing chunk statistics: {e}")


def _show_field_statistics(field_series: pd.Series, field_name: str) -> None:
    """
    Show statistics for a single field.
    
    Args:
        field_series (pd.Series): Field data
        field_name (str): Field name
    """
    try:
        clean_data = field_series.dropna()
        if len(clean_data) == 0:
            return
        
        print(f"\n{field_name.upper()} STATISTICS:")
        print(f"   Min: {clean_data.min():.5f}")
        print(f"   Max: {clean_data.max():.5f}")
        print(f"   Avg: {clean_data.mean():.5f}")
        print(f"   Std: {clean_data.std():.5f}")
        
    except Exception as e:
        logger.print_error(f"Error showing field statistics: {e}") 